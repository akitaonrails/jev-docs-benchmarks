# Observed homelab environment

Captured directly from the running service/container on 10 October 2026. This is
independent of the provisioning agent's readiness message.

- LAN endpoint: `http://192.168.0.90:11436/v1/systemone`.
- Server container: `decision-models-systemone`, image tag `decision-models-systemone:local`.
  Immutable local image ID: [server-image-id.txt](server-image-id.txt).
- [Server source snapshot](server-app.py) was read from `/opt/systemone/app.py`.
  It serializes loading/inference under a lock, preserves native model output, adds
  provenance/timing metadata, and synchronizes the GPU before stopping its timer.
- [Runtime versions and device properties](server-environment.json): AMD `gfx1151`,
  64 GiB GPU-addressable memory reported by PyTorch; this does not establish dedicated
  physical VRAM. Torch 2.9.1 ROCm build, HIP 7.2, Transformers 5.16.1, Laya 0.4.1.
  Package metadata and `torch.__version__` differ slightly; both strings are retained.
- Mounted model volume `decision_models_hf` at `/models`, read-only. Snapshot revisions
  match the benchmark pins and are validated again on each successful response.
- Laya uses full repo IDs with explicit revision, `fast=False`, `compile=False`.
  Clef-flash loads the local snapshot through `joint_schema_model.load_release_model`.
  No conversion to a generative GGUF or substitution of the base model was performed.
- Server metadata reports model parameters on `cuda:0`; on ROCm this names the AMD
  accelerator through PyTorch's CUDA-compatible API. This is not an NVIDIA GPU run.
- Models were already loaded before our smoke and main requests. Warm timing includes
  server overhead; the client additionally measures HTTP/LAN/serialization overhead.
- Server allocation and peak-memory fields are process-wide with all models resident.
  Peaks are not reset per request, so they cannot establish isolated per-model memory.
- Other server workloads are not controlled. The workstation RTX 5090 was not used.

The container remains managed by the homelab project; the benchmark client neither
restarts it nor changes its deployment. Its source snapshot is retained as evidence,
not as a replacement deployment recipe.
