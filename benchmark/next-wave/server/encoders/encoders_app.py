"""One encoder decision model per container, chosen by env: MODEL_KIND (laya | gliner), MODEL_REPO, MODEL_REV.

laya   -> POST /v1/systemone {"model", "state", "questions", optional "lang", "max_len", "head_max_len"}
          native Agent.predict output, untouched, plus a "server" key.
gliner -> POST /v1/classify  {"text", "tasks", optional "threshold", "include_confidence", "include_spans",
          "format_results", "max_len"} -> {"result": <raw classify_text output>, "server": {...}}.
          GLiNER scores are not a normalized distribution; nothing is converted here.
GET /healthz, GET /v1/models. Loaded at startup from the pinned local snapshot; HF_HUB_OFFLINE=1.
"""
import os
import threading
import time
from typing import Any, Optional

import torch
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

KIND = os.environ["MODEL_KIND"]
REPO = os.environ["MODEL_REPO"]
REV = os.environ["MODEL_REV"]
SNAPSHOT = os.path.join(os.environ.get("HF_HOME", "/models/hf"), "hub",
                        "models--" + REPO.replace("/", "--"), "snapshots", REV)
_lock = threading.Lock()
_state: dict[str, Any] = {}
app = FastAPI()


def _load() -> None:
    if not os.path.isdir(SNAPSHOT):
        raise RuntimeError(f"pinned snapshot missing: {SNAPSHOT}")
    t0 = time.monotonic()
    if KIND == "laya":
        import laya
        model = laya.load(REPO, revision=REV, device="cuda", fast=False, compile=False)
        if model.revision != REV:
            raise RuntimeError(f"loaded revision {model.revision!r} != pinned {REV}")
        module = model.model
    elif KIND == "gliner":
        from gliner2 import AutoExtractor
        model = AutoExtractor.from_pretrained(SNAPSHOT)
        model.to("cuda")
        model.eval()
        module = model
    else:
        raise RuntimeError(f"unknown MODEL_KIND {KIND!r}")
    torch.cuda.synchronize()
    _state.update(model=model, device=str(next(module.parameters()).device),
                  load_s=round(time.monotonic() - t0, 3), served=0)


@app.on_event("startup")
def _startup() -> None:
    _load()


@app.get("/healthz")
def healthz():
    return {"status": "ok", "kind": KIND, "repo": REPO, "revision": REV, "device": _state.get("device"),
            "load_s": _state.get("load_s"), "torch": torch.__version__, "hip": torch.version.hip}


@app.get("/v1/models")
def models():
    return {"data": [{"id": REPO.split("/")[-1], "repo": REPO, "revision": REV, "kind": KIND,
                      "device": _state.get("device")}]}


def _server_meta(t0: float) -> dict[str, Any]:
    torch.cuda.synchronize()
    cold = _state["served"] == 0
    _state["served"] += 1
    meta = {"repo": REPO, "revision": REV, "device": _state["device"], "cold": cold,
            "predict_s": round(time.monotonic() - t0, 3),
            "torch_cuda_allocated_mb": round(torch.cuda.memory_allocated() / 2**20),
            "torch_cuda_peak_mb": round(torch.cuda.max_memory_allocated() / 2**20)}
    if cold:
        meta["load_s"] = _state["load_s"]
    return meta


class SystemOneRequest(BaseModel):
    model: Optional[str] = None
    state: Any
    questions: dict[str, dict[str, Any]]
    lang: Optional[str] = None
    max_len: Optional[int] = None
    head_max_len: Optional[int] = None


@app.post("/v1/systemone")
def systemone(req: SystemOneRequest):
    if KIND != "laya":
        raise HTTPException(404, "this container serves GLiNER; use POST /v1/classify")
    if not req.questions:
        raise HTTPException(400, "questions must not be empty")
    with _lock, torch.inference_mode():
        t0 = time.monotonic()
        try:
            native = _state["model"].predict(req.state, req.questions, lang=req.lang,
                                             max_len=req.max_len, head_max_len=req.head_max_len)
        except (ValueError, TypeError, KeyError) as e:
            raise HTTPException(400, f"{type(e).__name__}: {e}")
        meta = _server_meta(t0)
    out = dict(native)
    out["server" if "server" not in out else "_server"] = meta
    return out


class ClassifyRequest(BaseModel):
    model: Optional[str] = None
    text: str
    tasks: dict[str, Any]
    threshold: float = 0.5
    include_confidence: bool = False
    include_spans: bool = False
    format_results: bool = True
    max_len: Optional[int] = None


@app.post("/v1/classify")
def classify(req: ClassifyRequest):
    if KIND != "gliner":
        raise HTTPException(404, "this container serves Laya; use POST /v1/systemone")
    if not req.tasks:
        raise HTTPException(400, "tasks must not be empty")
    with _lock, torch.inference_mode():
        t0 = time.monotonic()
        try:
            result = _state["model"].classify_text(req.text, req.tasks, threshold=req.threshold,
                                                   format_results=req.format_results,
                                                   include_confidence=req.include_confidence,
                                                   include_spans=req.include_spans, max_len=req.max_len)
        except (ValueError, TypeError, KeyError) as e:
            raise HTTPException(400, f"{type(e).__name__}: {e}")
        meta = _server_meta(t0)
    return {"result": result, "server": meta}
