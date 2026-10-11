"""Julia-1 SystemOne server (one engine per container; device from JULIA_DEVICE = cuda | cpu).

POST /v1/systemone {"model": "julia-1", "state": ..., "questions": {...}}
     -> native engine.predict(state=, questions=) output (answers) + "usage" (strict-encoding token counts
        from the engine's own cached encoding) + "server" metadata. Strict-encoding overflow -> HTTP 400.
POST /v1/encoding  same body -> per-question strict encoding (token counts) or the native rejection; no inference.
GET  /healthz, /v1/models -> readiness, revision, device, precision, context limits.
On cuda the native runtime runs the forward pass under bf16 autocast (FP32 weights); on cpu it is pure FP32.
"""
import os
import threading
import time
from typing import Any, Optional

import torch
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

REPO = "SupersonicLabs/Julia-1"
REV = "a85b127321d580d65176c89ced8273f305745d85"
SNAPSHOT = os.path.join(os.environ.get("HF_HOME", "/models/hf"), "hub", "models--SupersonicLabs--Julia-1",
                        "snapshots", REV)
DEVICE = os.environ.get("JULIA_DEVICE", "cpu")
MAX_LENGTH, HEAD_LENGTH = int(os.environ.get("JULIA_MAX_LENGTH", "8192")), int(os.environ.get("JULIA_HEAD_LENGTH", "512"))
SERVED = {"julia-1"}
_lock = threading.Lock()
_state: dict[str, Any] = {}
app = FastAPI()


class _Captured(Exception):
    pass


class _RowProbe:
    """Stands in for the engine so julia.typed.predict_typed builds (and validates) its native rows."""
    def __init__(self):
        self.rows = None

    def logits(self, rows):
        self.rows = rows
        raise _Captured


def _rows(state, questions):
    from julia.typed import predict_typed
    probe = _RowProbe()
    try:
        predict_typed(probe, state, questions)
    except _Captured:
        return probe.rows
    raise RuntimeError("predict_typed did not request logits")


def _precision():
    return "fp32 weights, bf16 autocast forward (native julia CUDA path)" if DEVICE == "cuda" else "fp32"


@app.on_event("startup")
def _load():
    from julia import load_model
    if not os.path.isdir(SNAPSHOT):
        raise RuntimeError(f"pinned snapshot missing: {SNAPSHOT}")
    t0 = time.monotonic()
    engine = load_model(SNAPSHOT, device=DEVICE, strict_encoding=True, max_length=MAX_LENGTH, head_length=HEAD_LENGTH)
    if DEVICE == "cuda":
        torch.cuda.synchronize()
    _state.update(engine=engine, load_s=round(time.monotonic() - t0, 3), served=0,
                  param_device=str(next(engine.model.parameters()).device),
                  param_dtype=str(next(engine.model.parameters()).dtype).replace("torch.", ""))


def _meta():
    e = _state.get("engine")
    return {"model": "julia-1", "repo": REPO, "revision": REV, "ready": e is not None, "device": _state.get("param_device"),
            "weight_dtype": _state.get("param_dtype"), "precision": _precision(),
            "max_length": MAX_LENGTH, "head_length": HEAD_LENGTH, "strict_encoding": True,
            "option_token_limit": 48, "options_per_question": "2-20",
            "cpu_threads": torch.get_num_threads() if DEVICE == "cpu" else None,
            "torch": torch.__version__, "hip": torch.version.hip, "load_s": _state.get("load_s")}


@app.get("/healthz")
def healthz():
    return {"status": "ok" if "engine" in _state else "loading", **_meta()}


@app.get("/v1/models")
def models():
    return {"data": [_meta()]}


class SystemOneRequest(BaseModel):
    model: Optional[str] = "julia-1"
    state: Any
    questions: dict[str, Any]


def _check(req):
    if req.model not in SERVED:
        raise HTTPException(400, f"unknown model {req.model!r}; this server serves 'julia-1'")


@app.post("/v1/encoding")
def encoding(req: SystemOneRequest):
    _check(req)
    with _lock:
        try:
            rows = _rows(req.state, req.questions)
        except ValueError as e:
            raise HTTPException(400, f"ValueError: {e}")
        out = {}
        for qid, row in zip(req.questions, rows):
            try:
                out[qid] = {"ok": True, **_state["engine"].encoding_info([row])[0]}
            except ValueError as e:
                out[qid] = {"ok": False, "error": str(e)}
    return {"questions": out, "server": _meta()}


@app.post("/v1/systemone")
def systemone(req: SystemOneRequest):
    _check(req)
    engine = _state["engine"]
    with _lock:
        t0 = time.monotonic()
        try:
            native = engine.predict(state=req.state, questions=req.questions)
            rows = _rows(req.state, req.questions)
            info = engine.encoding_info(rows)
        except ValueError as e:
            raise HTTPException(400, f"ValueError: {e}")
        if DEVICE == "cuda":
            torch.cuda.synchronize()
        predict_s = round(time.monotonic() - t0, 3)
        cold = _state["served"] == 0
        _state["served"] += 1
    out = dict(native)
    out["usage"] = {"input_tokens": sum(i["tokens"] for i in info),
                    "per_question_tokens": {q: i["tokens"] for q, i in zip(req.questions, info)},
                    "output_tokens": 0, "state_truncated": False, "options_truncated": False}
    out["server"] = {**_meta(), "cold": cold, "predict_s": predict_s}
    return out
