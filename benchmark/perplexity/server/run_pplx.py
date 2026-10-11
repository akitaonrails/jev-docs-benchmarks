"""Start the release's own autojev.server with two serving-only changes and two read-only endpoints.

1. Qwen3_5Model.from_pretrained is replaced by a strict shard-by-shard loader: the model is built on cuda:0 with weight
   init skipped, then every checkpoint tensor is copied from safetensors.safe_open(device="cuda:0"), one shard file open at a
   time. Verified for this checkpoint: 1183 tensors, keys 1:1 with the model, all BF16, no fp32-kept modules, no
   transformers weight conversions for qwen3_5 -- so the result equals from_pretrained(dtype=bfloat16), without the
   ~49 GiB host-RAM staging that transformers' all-shards-mmapped loader caused (it was OOM-killed at a 24 GiB cap).
2. Model alias "pplx-decider-v1.1-27b" is accepted besides the native names (autojev-qwen3.8-27b, jev-latest, ...).
Native behavior is otherwise untouched: DecisionModel(checkpoint) with the saved noncausal_full_attention mode, last-token
pooling, separate readout.safetensors and the saved temperature applied once in autojev.server.predict;
/health, /v1/models and /v1/systemone are the release's own routes (overflow -> HTTP 422, never truncated).
Added: GET /healthz (provenance, precision, limits) and POST /v1/encoding (token count via DecisionModel.prepare, no forward).
"""
import json, os, time
import torch
from transformers.models.qwen3_5 import modeling_qwen3_5 as mq

REV = "6195aa55a72ae21e503c8a60198f7b390d42adb5"
CKPT = os.environ["AUTOJEV_CHECKPOINT"]
def _gpu_direct(cls, path, *, dtype, attn_implementation):
    from safetensors import safe_open
    from transformers import AutoConfig
    try:
        from transformers.initialization import no_init_weights
    except ImportError:
        from transformers.modeling_utils import no_init_weights
    cfg = AutoConfig.from_pretrained(path)
    with no_init_weights(), torch.device("cuda:0"):
        model = cls._from_config(cfg, dtype=dtype, attn_implementation=attn_implementation)
    params = model.state_dict()
    index = json.load(open(os.path.join(path, "model.safetensors.index.json")))["weight_map"]
    if set(index) != set(params):
        raise RuntimeError("checkpoint keys differ from the model's state_dict")
    loaded = set()
    with torch.no_grad():
        for shard in sorted(set(index.values())):
            with safe_open(os.path.join(path, shard), framework="pt", device="cuda:0") as f:
                for key in f.keys():
                    tensor, target = f.get_tensor(key), params[key]
                    if key in loaded or tensor.shape != target.shape or tensor.dtype != target.dtype:
                        raise RuntimeError(f"tensor mismatch or duplicate: {key}")
                    target.copy_(tensor)
                    loaded.add(key)
                    del tensor
    if loaded != set(params):
        raise RuntimeError(f"{len(set(params) - loaded)} model tensors were not loaded")
    model.eval()
    return model

mq.Qwen3_5Model.from_pretrained = classmethod(_gpu_direct)

import autojev.server as srv  # noqa: E402
from fastapi import HTTPException  # noqa: E402

srv.ALIASES.add("pplx-decider-v1.1-27b")
_t0 = time.monotonic()
_meta = {}

@srv.app.get("/healthz")
def healthz():
    m = srv.service.model
    if m is None:
        return {"status": "loading", "revision": REV}
    if not _meta:
        p = next(m.backbone.parameters())
        cfg = json.load(open(os.path.join(CKPT, "decision_config.json")))
        _meta.update(load_s=round(time.monotonic() - _t0, 1), device=str(p.device), weight_dtype=str(p.dtype).replace("torch.", ""),
                     readout_dtype=str(m.readout.weight.dtype).replace("torch.", ""))
        _meta.update(step=cfg.get("step"))
    return {"status": "ok", "model": srv.service.name, "aliases": sorted(srv.ALIASES), "repo": "perplexity-ai/pplx-decider-v1.1-27b",
            "revision": REV, "precision": "bf16 (reference)", "attention_mode": m.attention_mode, "pooling": m.pooling,
            "temperature": m.temperature, "max_length": 8192, "max_options": 255, "linear_attention_kernels": "transformers torch path (no flash-linear-attention)",
            "torch": torch.__version__, "hip": torch.version.hip, "gpu_mem_allocated_gb": round(torch.cuda.memory_allocated() / 2**30, 2),
            **_meta}

@srv.app.post("/v1/encoding")
def encoding(body: srv.EvaluationRequest):
    m = srv.service.model
    if m is None:
        raise HTTPException(503, "The model is not ready.")
    out = {}
    for qid, q in body.questions.items():
        row = {"state": body.state, "question": q.model_dump(exclude_none=True), "images": list(body.images)}
        try:
            b = m.prepare([row])
            out[qid] = {"ok": True, "input_tokens": b.input_tokens, "options": b.counts[0]}
        except ValueError as e:
            out[qid] = {"ok": False, "error": str(e)}
    return {"questions": out}

import uvicorn  # noqa: E402
uvicorn.run(srv.app, host="0.0.0.0", port=8000)
