# CUDA versus ROCm reproduction

Run the frozen v1 and bilingual v2 suites against the same public checkpoints on
an RTX 5090. Preserve the earlier gfx1151 ROCm archives. Hosted Jev, Clef,
OpenAI and Microsoft services cannot be moved onto local hardware; Clef Flash's
public checkpoint is included. Julia CPU is a separate existing configuration,
not a CUDA model.

## Protocol (2026-10-15, before CUDA inference)

- Same checkpoint revisions, native request adapters, labels and dataset hashes.
- Same precision and eager/reference serving where supported. No new FLA or
  causal-conv kernels, tuning against answers, quantization, or CUDA graphs.
- PyTorch 2.9.1+cu128 versus the archived vendor PyTorch 2.9.1 ROCm build.
  Official wheel: https://pytorch.org/get-started/previous-versions/.
- Match Transformers per serving family (5.17.0 Qwen/D3, 5.16.1 encoders/Decider,
  5.0.0 Julia). Archive all resolved dependencies and actual image IDs.
- One service at a time, one request at a time, warm-up excluded, fixed order seed.
- Separate `cuda-v1` and `cuda-v2` archives, never overwrite ROCm archives.
- Compare accuracy, EN/PT-BR, conditions, paired label disagreement, probability
  differences, median/p95 latency and observed memory. Check request hashes
  before pairing results. No financial ranking for unmetered local electricity.
- 27B BF16 weights (~49 GiB) exceed the 32 GiB card before activations. Any CPU
  offload is a separate deployment track, excluded from GPU-only speed ratios.
- Latency compares whole deployments: different GPUs, CPUs, software builds,
  local loopback versus LAN and display usage. It does **not** estimate the
  causal effect of switching only ROCm to CUDA.

## Isolation and cleanup

All benchmark dependencies and inference run in **local Docker** (Unix socket).
Host Python scripts use only the standard library. Existing NVIDIA CDI support
is used with `--device nvidia.com/gpu=all`; no host driver/toolkit changes.
Only `jev-cuda-*` containers/images and `jev_cuda_*` volumes belong to this run.
Retain source, metadata and compressed responses; remove created runtime
resources after the run. Never run a global Docker prune.

## Prerequisites

Use a local Docker daemon, an existing Python 3.12 interpreter for the stdlib
controllers, a working NVIDIA driver, and NVIDIA Container Toolkit with CDI.
The measured machine had one visible RTX 5090, driver 610.57.04, Ryzen 7950X3D
and about 92 GiB host RAM. Docker accessed `unix:///var/run/docker.sock`.
For another machine, follow [NVIDIA's CDI setup documentation](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/latest/cdi-support.html).
This experiment did not install or reconfigure the host driver/toolkit.

Build the existing stdlib client image if it is not already present:

```sh
docker build -f benchmark/docker/Dockerfile.runner -t jev-benchmark-runner benchmark
```

## Initial reproduction commands

```sh
python benchmark/cuda/transfer.py  # existing pinned homelab caches, no GPU
python benchmark/cuda/build.py
python benchmark/cuda/prepare.py
python benchmark/cuda/run.py --run-id cuda-reproduction --execute
```

The frozen deployment registry records build-specific image IDs. Rebuild and run
`prepare.py` on a new machine to freeze its IDs; retain that registry with the run.

## Measured setup details

The original multi-stage Dockerfile records the bootstrap build. For repeat runs,
use `Dockerfile.locked` above: every installed Python package version is recorded
in `locks/`, including CUDA libraries and pinned upstream Git commit archives.
Package locks are version locks, not a complete supply-chain hash lock. The
measured image IDs remain in each response archive even after local cleanup.

On this host the existing CDI file had a stale UVM major number (237 versus the
host's 238). `run.py` explicitly permits and bind-mounts the actual UVM nodes,
retaining a read-only filesystem and dropped capabilities without changing CDI
or drivers. Kev explicitly sets `KEV_CUDA_GRAPHS=0` and `KEV_FUSED=0` to match
the earlier ROCm serving mode. Clef Flash and Simple-Jev additionally need Torchvision 0.24.1
with Torch 2.9.1; it is installed in their dedicated images.

`verify.py` hashes every copied snapshot file against the source volume before
its first use. The matching hashes are archived under `reports/cuda-runtime/`.

After scoring with `sh benchmark/cuda/score.sh`, use
`python benchmark/cuda/cleanup.py --execute` to remove the run's inventoried
images, model volumes and exact BuildKit cache records. This run's resource
inventory is machine-specific. `build.py` and `prepare.py` generate a fresh
local inventory at `results/cuda-resources.json` for repeat runs; cleanup prefers
that inventory. The repeat-build helper uses a dedicated local builder so its
cache can be removed without touching other projects.
The pre-existing stdlib runner image and Python base image are retained.

## Timing validity

The first six successful model runs overlapped model-cache copying and image
setup. They are preserved separately as `cuda-setup-overlap-v1/v2` validation
archives. Those deployments are rerun after all transfers/builds stop; only the
final `cuda-v1/v2` archives enter the hardware latency comparison. Unrelated host
services/builds and desktop rendering were not stopped; this is not a dedicated
whole-machine microbenchmark. This decision
was made during setup, before inspecting the full model ranking. It concerns
machine contention, not whether a model's answers improved.

## Reproduce without access to this homelab

Build the locked images first, then download the public revisions listed in the
archived SHA-256 manifests. This runs no model code and uses no GPU:

```sh
for suffix in d3_edge julia1 hf eikos4b jebadiah4b kev simplejev decider layaml gliner; do
  docker volume create --label project=jev-cuda-benchmark "jev_cuda_$suffix"
  docker run --rm -e HF_HUB_OFFLINE=0 \
    -v "jev_cuda_$suffix:/models" -v "$PWD/benchmark:/work:ro" \
    jev-cuda-d3 python /work/cuda/download.py "$suffix"
done
python benchmark/cuda/prepare.py
python benchmark/cuda/run.py --run-id cuda-reproduction --execute
sh benchmark/cuda/score.sh cuda-reproduction
```

The downloader verifies every recorded snapshot file before writing its completion
marker. It fails if an upstream file is missing or differs; it never silently
switches to a newer revision. Download availability still depends on the public
repositories retaining those revisions. The measured run used the verified
homelab-copy path; the independent downloader is provided for portability.

Use a fresh `--run-id` for another machine or measurement. Published `cuda-v1/v2`
archives are never silently skipped or overwritten when there is no matching
local run to resume. The example writes `cuda-reproduction-v1/v2` and separate
comparison reports.

## Rebuild verification

After the measured runs, the Simple-Jev environment was rebuilt using
`Dockerfile.locked`. Its full `pip freeze` matched `locks/simple.txt` exactly.
The rebuilt image imported the native server and successfully executed a CUDA
tensor operation on the 5090. See [rebuild evidence](../reports/cuda-runtime/locked-rebuild.json).
The full model suite was not repeated on this second image.

## Cleanup outcome for the published run

All benchmark containers, eight images and ten copied model volumes were removed.
Seven failed-build cache records (~7.36 GB) remain non-reclaimable in the shared
default builder despite scoped pruning and build-history removal. See the
[receipt](../reports/cuda-runtime/cleanup.json). No Docker daemon restart was
performed because other projects use it. The cleanup command fails explicitly
while these records remain; rerun it after Docker releases the references.
Future builds use the dedicated removable builder described above.
