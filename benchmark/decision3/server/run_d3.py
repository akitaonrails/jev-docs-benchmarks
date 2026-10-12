"""Serve a pinned Decision 3.0 snapshot through its native System One runtime."""

from __future__ import annotations

import json
import os
import time
from pathlib import Path

import torch


MODEL_PATH = Path(os.environ["D3_MODEL_PATH"])
MODEL_REPO = os.environ["D3_MODEL_REPO"]
MODEL_REVISION = os.environ["D3_MODEL_REVISION"]
MODEL_NAME = os.environ["D3_MODEL_NAME"]
MAX_INPUT_TOKENS = int(os.environ.get("D3_MAX_INPUT_TOKENS", "8192"))
BATCH_SIZE = int(os.environ.get("D3_BATCH_SIZE", "1"))
DIRECT_GPU_LOAD = os.environ.get("D3_DIRECT_GPU_LOAD", "0") == "1"


def install_direct_gpu_loader() -> None:
    """Load one safetensors shard at a time directly into its final GPU tensor."""
    from safetensors import safe_open
    from transformers import AutoConfig
    from transformers.models.qwen3_5 import modeling_qwen3_5

    try:
        from transformers.initialization import no_init_weights
    except ImportError:
        from transformers.modeling_utils import no_init_weights

    def load(cls, path, *, dtype, attn_implementation, device_map=None, **kwargs):
        if kwargs:
            raise RuntimeError(f"unsupported direct-loader arguments: {sorted(kwargs)}")
        if device_map not in (None, {"": "cuda:0"}):
            raise RuntimeError(f"direct loader requires cuda:0, got device_map={device_map!r}")
        root = Path(path)
        config = AutoConfig.from_pretrained(root, local_files_only=True)
        with no_init_weights(), torch.device("cuda:0"):
            model = cls._from_config(config, dtype=dtype, attn_implementation=attn_implementation)

        targets = model.state_dict()
        index = json.loads((root / "model.safetensors.index.json").read_text(encoding="utf-8"))["weight_map"]
        if set(index) != set(targets):
            missing = sorted(set(targets) - set(index))
            extra = sorted(set(index) - set(targets))
            raise RuntimeError(f"checkpoint/model key mismatch: missing={missing[:5]}, extra={extra[:5]}")

        loaded: set[str] = set()
        with torch.no_grad():
            for shard in sorted(set(index.values())):
                with safe_open(root / shard, framework="pt", device="cuda:0") as source:
                    for key in source.keys():
                        tensor = source.get_tensor(key)
                        target = targets[key]
                        if key in loaded or tensor.shape != target.shape or tensor.dtype != target.dtype:
                            raise RuntimeError(f"tensor mismatch or duplicate: {key}")
                        target.copy_(tensor)
                        loaded.add(key)
                        del tensor
        if loaded != set(targets):
            raise RuntimeError(f"{len(set(targets) - loaded)} model tensors were not loaded")
        model.eval()
        return model

    modeling_qwen3_5.Qwen3_5Model.from_pretrained = classmethod(load)


if DIRECT_GPU_LOAD:
    install_direct_gpu_loader()

os.environ["PYTHONPATH"] = f"{MODEL_PATH}:{os.environ.get('PYTHONPATH', '')}"
os.sys.path.insert(0, str(MODEL_PATH))

from d3_runtime import D3  # noqa: E402
import d3_server  # noqa: E402


started = time.monotonic()
model = D3.from_pretrained(
    MODEL_PATH,
    device="cuda:0",
    batch_size=BATCH_SIZE,
    verify="fast",
    max_length=MAX_INPUT_TOKENS,
    model_name=MODEL_NAME,
)
model.warmup()

native_health = d3_server.Decider.health


def health(self, authentication):
    result = native_health(self, authentication)
    parameter = next(self.model.backbone.parameters())
    result.update(
        {
            "repo": MODEL_REPO,
            "revision": MODEL_REVISION,
            "device": str(parameter.device),
            "weight_dtype": str(parameter.dtype).removeprefix("torch."),
            "readout_dtype": str(self.model.readout.dtype).removeprefix("torch."),
            "context": {
                "max_input_tokens": self.model.max_length,
                "overflow": "max_length_exceeded per question; nothing is truncated",
            },
            "attention_mode": self.model.attention_mode,
            "pooling": "last",
            "temperature": self.model.temperature,
            "batch_size": self.model.batch_size,
            "loader": "direct safetensors shards to cuda:0" if DIRECT_GPU_LOAD else "transformers device_map",
            "runtime_verified": "MODEL_MANIFEST.json fast check; full hash checked at installation",
            "load_seconds": round(time.monotonic() - started, 1),
            "torch": torch.__version__,
            "hip": torch.version.hip,
            "kernels": self.model.kernels,
            "gpu_memory_allocated_gib": round(torch.cuda.memory_allocated() / 2**30, 2),
        }
    )
    return result


d3_server.Decider.health = health
server = d3_server.serve(model, "0.0.0.0", 8000)
print(
    f"d3 System One server: {MODEL_NAME}@{MODEL_REVISION} on 0.0.0.0:8000; "
    f"context={MAX_INPUT_TOKENS}, loader={'direct-gpu' if DIRECT_GPU_LOAD else 'transformers'}",
    flush=True,
)
server.serve_forever()
