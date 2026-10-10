"""systemone decision-model server (Laya / Laya-typed / Clef-flash) for the jev-docs benchmark.

POST /v1/systemone  {"model": "laya" | "laya-typed" | "clef-flash", "state": <any JSON>,
                     "questions": {"<id>": {"type": "choice"|"noul"|"score", "instructions": ..., "criteria": ...}}}
  -> the model's native response, untouched, plus one added key "server" with serving metadata.
GET  /healthz       -> liveness, GPU visibility, loaded selectors
GET  /v1/models     -> selectors, repos, pinned revisions, load state, device

Models load lazily on first request; loading and inference are serialised by one lock.
HF_HUB_OFFLINE=1: everything comes from the pinned snapshots in the volume, nothing is fetched.
Laya variants are loaded by full repo id with subfolder=None: laya.load only resolves
registry aliases for bare names, and no Router is constructed, so no checkpoint routing.
"""
import os
import sys
import threading
import time
from typing import Any

import torch
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

HF_HUB = os.path.join(os.environ.get("HF_HOME", "/models/hf"), "hub")
PINS = {
    "laya":       {"repo": "convaiinnovations/laya",                 "rev": "7b928d828b7b0e022f929d9bd2e44165aa270148"},
    "laya-typed": {"repo": "convaiinnovations/laya-typed-decisions", "rev": "e929ae5cf69bc34259cd2f95c9e91145b818b1f0"},
    "clef-flash": {"repo": "Cloudflare/clef-flash",                  "rev": "fde727a287004204b7518dcc983fe64379776712"},
}
_loaded: dict[str, dict[str, Any]] = {}
_lock = threading.Lock()
app = FastAPI()


def _snapshot_path(selector: str) -> str:
    spec = PINS[selector]
    path = os.path.join(HF_HUB, "models--" + spec["repo"].replace("/", "--"), "snapshots", spec["rev"])
    if not os.path.isdir(path):
        raise HTTPException(503, f"pinned snapshot missing: {path}")
    return path


def _param_device(module: Any) -> str:
    return str(next(module.parameters()).device)


def _load(selector: str) -> dict[str, Any]:
    spec = PINS[selector]
    t0 = time.monotonic()
    if selector in ("laya", "laya-typed"):
        import laya
        agent = laya.load(spec["repo"], revision=spec["rev"], device="cuda", fast=False, compile=False)
        if agent.revision != spec["rev"]:
            raise HTTPException(500, f"{selector}: loaded revision {agent.revision!r} != pinned {spec['rev']}")
        entry = {"kind": "laya", "agent": agent, "revision": agent.revision, "device": _param_device(agent.model)}
    else:
        path = _snapshot_path(selector)
        if path not in sys.path:
            sys.path.insert(0, path)
        from joint_schema_model import load_release_model  # reviewed 2026-10-10: no network for a local dir
        model, processor = load_release_model(path, device="cuda")
        entry = {"kind": "clef", "model": model, "processor": processor,
                 "revision": spec["rev"], "device": _param_device(model)}
    torch.cuda.synchronize()
    entry["load_s"] = round(time.monotonic() - t0, 3)
    return entry


class SystemOneRequest(BaseModel):
    model: str
    state: Any
    questions: dict[str, dict[str, Any]]


@app.get("/healthz")
def healthz():
    return {"status": "ok", "cuda_available": torch.cuda.is_available(),
            "device_name": torch.cuda.get_device_name(0) if torch.cuda.is_available() else None,
            "torch": torch.__version__, "hip": torch.version.hip, "loaded": sorted(_loaded)}


@app.get("/v1/models")
def models():
    return {s: {"repo": p["repo"], "revision": p["rev"], "loaded": s in _loaded,
                "device": _loaded[s]["device"] if s in _loaded else None} for s, p in PINS.items()}


@app.post("/v1/systemone")
def systemone_endpoint(req: SystemOneRequest):
    if req.model not in PINS:
        raise HTTPException(400, f"unknown model {req.model!r}; valid: {sorted(PINS)}")
    if not req.questions:
        raise HTTPException(400, "questions must not be empty")
    with _lock:
        cold = req.model not in _loaded
        if cold:
            torch.cuda.reset_peak_memory_stats()
            _loaded[req.model] = _load(req.model)
        entry = _loaded[req.model]
        t0 = time.monotonic()
        if entry["kind"] == "laya":
            native = entry["agent"].predict(req.state, req.questions)
        else:
            from joint_schema_model import systemone
            native = systemone(entry["model"], entry["processor"],
                               {"model": req.model, "state": req.state, "questions": req.questions})
        torch.cuda.synchronize()
        predict_s = round(time.monotonic() - t0, 3)
    server = {"selector": req.model, "repo": PINS[req.model]["repo"], "revision": entry["revision"],
              "device": entry["device"], "cold": cold, "predict_s": predict_s,
              "torch_cuda_allocated_mb": round(torch.cuda.memory_allocated() / 2**20),
              "torch_cuda_peak_mb": round(torch.cuda.max_memory_allocated() / 2**20)}
    if cold:
        server["load_s"] = entry["load_s"]
    out = dict(native)
    out["server" if "server" not in out else "_server"] = server
    return out
