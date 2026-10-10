# Runtime and API verification evidence

Collected during the 10 October 2026 next-wave benchmark.

- `client-image-id.json`: local CPU benchmark client image identity.
- `smoke/`: independent, unscored ticket requests/responses, model discovery,
  container image IDs, startup commands and read-only model mounts.
- `deployment-inspect.json`: image, command, working directory, model mounts and
  device mappings rechecked for all ten installed containers.
- `kev-4b-live-models.json` and `kev-9b-live-models.json`: serving metadata captured during scored execution,
  including CUDA/ROCm device selection, BF16, head temperature and prefix cache.
- `kev-base-cache.json`: only one cached snapshot exists for each Kev base size,
  consistent with the reported revisions and offline serving.

The first Jebadiah smoke calls returned loading HTTP 503; they are retained as
readiness diagnostics. The scored runner waits for a successful independent
warm-up before submitting cases. Eikos lacks `/v1/models`; its `/health` exists,
and provenance uses the pinned image, command and offline model snapshot.

Per-run archives also include `container.json`, `resolved-deps.txt`, `warmup.json`
and `run.json`. Each request records raw output, normalized result, dataset/request
hashes, attempt count and wall time. GLiNER probabilities are not synthesized.

Latency is client-observed on a shared homelab, one benchmark model resident at
a time, with unrelated workloads left running. One warm-up does not guarantee
all subsequent input shapes avoid first-use kernel costs. Native runtime caches
are retained. These observations are not dedicated-hardware throughput or energy
measurements. The initial installation report's VRAM deltas are separate from
encoder allocator peaks captured in individual responses.
