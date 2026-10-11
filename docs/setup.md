# Setup and reproduction guide

This guide separates the **CPU benchmark client** from the **AMD ROCm model server**.
All benchmark-only dependencies stay in Docker. The client does not need a GPU.
The hosted path needs credentials; the homelab path does not send those credentials.

The measured server was `192.168.0.90`, AMD `gfx1151`, with approximately 64 GiB of
GPU-addressable memory. Ollama and llama-swap were already running, but these custom
decision models use a separate SystemOne service on port 11436. They cannot be reproduced
by downloading only their generative base models into Ollama.

## 1. Clone and build the CPU client

Prerequisites: Git, Docker with Compose, and existing Python 3 for the optional credential
launcher. Python packages are installed only inside containers; no host pip install.

```sh
git clone https://github.com/akitaonrails/jev-docs-benchmarks.git
cd jev-docs-benchmarks
mkdir -p benchmark/results
docker build -t jev-benchmark-runner -f benchmark/docker/Dockerfile.runner benchmark
benchmark/tools/offline.sh -m unittest discover -s /work/tests
```

Create `benchmark/results` as your own user before Compose mounts it, so new outputs
are writable by the unprivileged client. The runner base image is pinned by digest. `offline.sh` has networking disabled and
cannot invoke a provider. The checked-in datasets and response archives allow offline
analysis without any credentials or model server.

## 2. Hosted credentials and execution

The hosted runner reads these environment variables:

```sh
export JEV_API_KEY='your-typesafe-key'
export CLOUDFLARE_API_TOKEN='your-workers-ai-token'
export CLOUDFLARE_ACCOUNT_ID='your-32-character-account-id'
```

Supply them securely in your shell; do not commit them. A Workers AI API token and
account ID are separate values. This repository contains neither. On the original
workstation they are literal exports in `~/.config/zsh/secrets` (mode 0600).
`tools/launch.py` reads only those three named exports without executing the file.
If you use another secret store, use Compose directly with the variables exported:

```sh
export BENCH_UID="$(id -u)"
export BENCH_GID="$(id -g)"
docker compose -f benchmark/compose.yaml --profile hosted build hosted
docker compose -f benchmark/compose.yaml --profile hosted run --rm -T hosted \
  /work/tools/preflight.py
# v1: 544 requests per hosted model. This command incurs provider usage.
docker compose -f benchmark/compose.yaml --profile hosted run --rm -T hosted \
  /work/tools/hosted.py --output /results/hosted-new --cost-cap 5 --execute
# v2: 504 bilingual classification requests per hosted model.
docker compose -f benchmark/compose.yaml --profile hosted run --rm -T hosted \
  /work/tools/hosted.py --dataset /work/expansion-v2 \
  --output /results/hosted-v2-new --cost-cap 5 --execute
```

On the original workstation the shorter equivalent is:

```sh
python benchmark/tools/launch.py /work/tools/hosted.py \
  --dataset /work/expansion-v2 --output /results/hosted-v2-new --cost-cap 5 --execute
```

Choose **one** launcher, not both for the same run. Use a fresh result directory for
an independent experiment. Matching interrupted runs can resume; persisted errors are
not silently retried as new experiments. The $5 cap reserves conservative bytes-based
input allowances at the original 9 October rates, including possible retries; it is
not an invoice limit. Current billing differs, particularly Flash's reduced price.
Read the [dated pricing audit](../benchmark/reports/hosted-v1/pricing.md) and
[current valuation](cost-benefit-ranking.md).

## 3. Homelab runtime: what was actually tested

The actual server used:

| Component | Observed version/configuration |
| --- | --- |
| GPU architecture | AMD `gfx1151`; PyTorch name `AMD Radeon Graphics` |
| PyTorch runtime | `2.9.1+rocm7.2.1.gitff65f5bc` |
| HIP | `7.2.53211-e1a6bc5663` |
| Transformers | `5.16.1` |
| Laya | `0.4.1` |
| Python | `3.12.3` |
| Device access | `/dev/kfd`, `/dev/dri` |
| Model volume | `decision_models_hf`, mounted read-only while serving |
| Service | `decision-models-systemone`, port 11436 |

See [captured environment](../benchmark/reports/homelab-v1/environment.md),
[exact image ID](../benchmark/reports/homelab-v1/server-image-id.txt), and
[captured serving source](../benchmark/reports/homelab-v1/server-app.py).

**Base-image limitation:** the original Dockerfile extends the homelab's existing
`localhost:3007/akitaonrails/frank-yomik-worker-rocm:latest`. That is a local registry
image, not a public dependency supplied by this repository. An outside user cannot
reproduce it by running `docker compose build` unchanged. Use an equivalent ROCm base
verified for your GPU and with the required Qwen3.5 Transformers support, or export/import
the already-tested image if you operate both machines. Record its immutable ID/digest.
A rebuild from mutable tags or unpinned transitive packages is not bit-for-bit reproduction.

The supplied [Dockerfile](../benchmark/homelab/Dockerfile),
[Compose file](../benchmark/homelab/compose.yaml), and [app](../benchmark/homelab/app.py)
make the deployment reproducible on the configured homelab while exposing that dependency.
The app matches the inspected server code. The Compose template changes the original
hardcoded address/group IDs into explicit settings and defaults to loopback. This
template was checked structurally; the running homelab was not redeployed from it.

## 4. Configure the server host

Run these steps **on the GPU server** in its checkout. Existing Docker and a working
ROCm driver/device setup are prerequisites. Do not install a second host Python stack.

```sh
export ROCM_BASE='localhost:3007/akitaonrails/frank-yomik-worker-rocm:latest'
export VIDEO_GID="$(getent group video | cut -d: -f3)"
export RENDER_GID="$(getent group render | cut -d: -f3)"
export BENCH_BIND_IP='192.168.0.90'
# Only for the tested gfx1151 setup; adapt to your actual supported hardware.
export HSA_OVERRIDE_GFX_VERSION='11.5.1'
export PYTORCH_ROCM_ARCH='gfx1151'

docker compose -f benchmark/homelab/compose.yaml build systemone
docker volume create decision_models_hf
```

The original deployment used supplemental group IDs 485 and 488. Resolve groups on
your own host rather than copying those numbers. The original service was in
`/var/opt/docker/ai/decision-models`; if it already exists, inspect/use that deployment
instead of starting another container with the same name and port.

The service has no authentication. Loopback is the default for this reason. For the
LAN deployment, allow only your intended client network with the host's Docker-aware
firewall; the tested host also had a DOCKER-USER rule blocking non-LAN forwarded traffic.
Binding a private IP alone is not a complete firewall policy. This repo does not modify
host firewall rules or expose a public endpoint.

## 5. Download the pinned checkpoints without GPU inference

The three repo/revision pairs are in [models.json](../benchmark/models.json). The full
Clef-flash snapshot includes its backbone and custom head; no separate base download
is needed. Expect tens of GB of Docker storage and verify available space first.

```sh
docker run --rm --entrypoint python \
  -e HF_HOME=/models/hf -e HF_HUB_OFFLINE=0 -e HF_HUB_DISABLE_TELEMETRY=1 \
  -v decision_models_hf:/models \
  -v "$PWD/benchmark:/bench:ro" \
  decision-models-systemone:local /bench/homelab/download.py
```

No GPU device is supplied to this download container. The script retrieves immutable
snapshots without importing their custom code. The service uses `HF_HUB_OFFLINE=1`
and loads them from the same volume. Review custom model code before running it;
our pinned Clef implementation review and runtime provenance are documented in the
[environment report](../benchmark/reports/homelab-v1/environment.md).

## 6. Start and smoke-test the homelab service

```sh
docker compose -f benchmark/homelab/compose.yaml up -d systemone
curl --fail http://192.168.0.90:11436/healthz
curl --fail http://192.168.0.90:11436/v1/models
```

Health should show CUDA availability (PyTorch uses that API name for ROCm too), the AMD
device and the runtime versions. Selectors are `laya`, `laya-typed`, `clef-flash`.
Discovery initially shows unloaded models; the first inference loads each lazily.
Models remain resident until the container stops. There is no per-model unload API
or idle timeout in this server. `docker stop decision-models-systemone` releases all
three; `docker start decision-models-systemone` brings back an empty server that
loads models on first use. The persistent weights volume is retained. Inference is serialized; provision
memory for the resident set and other workloads, not just one model's weight size.

From the client checkout:

```sh
benchmark/tools/homelab.sh --smoke --output /results/homelab-smoke-new --execute
benchmark/tools/homelab.sh --output /results/homelab-new --execute
# Separate bilingual run:
benchmark/tools/homelab.sh --dataset /work/expansion-v2 \
  --output /results/homelab-v2-new --execute
```

The adapter currently deliberately allows only `http://192.168.0.90:11436`. To use a
different server, update the explicit host/port check in `tools/homelab.py` and record
the change as a different runner revision. Supplying `--base-url` alone does not bypass
that guard. Do not pass hosted API credentials to this service.

For a direct single test, the body has this shape:

```json
{
  "model": "laya",
  "state": "Please refund the duplicate payment.",
  "questions": {
    "decision": {
      "type": "choice",
      "instructions": "Choose the requested action.",
      "criteria": {"refund": "Return money.", "access": "Restore login."}
    }
  }
}
```

POST JSON to `/v1/systemone`. `questions` is an object keyed by question ID. Preserve
native `answers`, `usage` and additional `server` metadata. The benchmark uses choice
probabilities, not Laya's separate confidence/action scores. Request payloads exclude
gold labels. A direct manual test is extra inference and is not part of frozen metrics.

## 7. Archive and score without network access

```sh
# v1 archives and combined comparison:
benchmark/tools/offline.sh /work/tools/archive.py /work/results/hosted-new /reports/hosted-new
benchmark/tools/offline.sh /work/tools/archive.py /work/results/homelab-new /reports/homelab-new
benchmark/tools/offline.sh /work/tools/score.py /work/reports/homelab-new --output /reports/homelab-new
benchmark/tools/offline.sh /work/tools/compare.py \
  /work/reports/hosted-new /work/reports/homelab-new --output /reports/comparison-new

# v2 archives and paired-language analysis (use the v2 scorer):
benchmark/tools/offline.sh /work/tools/archive.py /work/results/hosted-v2-new /reports/hosted-v2-new
benchmark/tools/offline.sh /work/tools/archive.py /work/results/homelab-v2-new /reports/homelab-v2-new
benchmark/tools/offline.sh /work/tools/score_v2.py \
  /work/reports/hosted-v2-new /work/reports/homelab-v2-new --output /reports/comparison-v2-new
```

Do not combine v1 and v2 into one overall ranking. Invalid/missing responses count as
errors. Language deltas are paired by scenario; translations are not independent
samples. See the [v2 protocol](../benchmark/expansion-v2/README.md).

## 8. Stop and clean up deliberately

On the original server, stop the owning deployment to release GPU memory:

```sh
docker compose -f /var/opt/docker/ai/decision-models/docker-compose.yml stop systemone
```

For a deployment created from this checkout, use its Compose file instead. Stop only
the benchmark service, not Ollama or llama-swap. Removing containers does not remove
the external model volume. Keep `decision_models_hf` to avoid downloading again;
remove it only when intentionally deleting those snapshots. Result directories are
ignored; published gzip archives under `benchmark/reports/` are version controlled.

## RTX 5090 status

The original `benchmark/docker/Dockerfile.local` and local Compose profile are
**untested workstation CUDA preparation**, not the measured AMD setup. They are not
used by the client/homelab commands above. No claim about RTX 5090 fit, speed or
compatibility follows from the homelab measurements.

## Next-wave ROCm services

Ten additional pinned services are installed under `/var/opt/docker/ai/decision-models-next`,
ports 11437–11446. They are separate Docker containers and must run **one at a time**.
The [captured Compose file](../benchmark/next-wave/server/docker-compose.yml) records
service names, model snapshots, read-only cache volumes, ports and device access.
The [installation handoff](homelab-installation-report.md) records runtime caveats.

Use the [next-wave protocol](../benchmark/next-wave/README.md) and lifecycle controller:

```sh
python benchmark/next-wave/run.py --execute
# Restrict an evaluation to the three sizes in one family:
python benchmark/next-wave/run.py --models kev-0.8b kev-4b kev-9b --execute
```

The controller uses host Python's standard library for SSH/Docker lifecycle only;
inference clients run inside the existing `jev-benchmark-runner` image. It verifies
the active container image and command, warms the endpoint, archives completed runs
and stops the service in a `finally` block. Run from a session that can SSH to
`192.168.0.90` and invoke server Docker with noninteractive sudo. An abrupt host crash
can bypass cleanup; inspect and stop that specific benchmark service before resuming.

Manual lifecycle, using a service name from the Compose file:

```sh
ssh 192.168.0.90 'cd /var/opt/docker/ai/decision-models-next && sudo docker compose up -d kev-4b'
ssh 192.168.0.90 'cd /var/opt/docker/ai/decision-models-next && sudo docker compose stop kev-4b'
```

Do not start the whole Compose stack. Do not stop unrelated server GPU workloads.
Perplexity is now installed; see the dedicated reproduction section below. Rune
still requires capacity/runtime work. GLiDE remains
a hosted candidate. Default context limits, Simple-Jev's prompt policy and GLiNER's
native classification mapping are part of the frozen entrant configuration.

## OpenAI Decisions extension

See the [native Decisions protocol and Docker commands](../benchmark/openai-decisions/README.md).
It uses `OPENAI_API_KEY` with Platform API billing, separately from Codex subscription
access. A funded API account is required before running the smoke check and frozen suites. No additional host
packages or GPU are needed. Earlier model archives are reused when scoring.

## Julia GPU and CPU reproduction

See the [frozen Julia protocol](../benchmark/julia/README.md) and
[captured server setup](../benchmark/julia/server/). The existing homelab services
are `julia-1` (11447) and `julia-1-cpu` (11448), in
`/var/opt/docker/ai/decision-models-next`. They share read-only weights and a pinned
image. CPU has no GPU device mounts and uses four threads. GPU keeps FP32 weights
with native BF16 autocast. The captured Compose JSON is valid Compose input;
it references the homelab's external model volume and local image prerequisites.
The Dockerfile's ROCm base is homelab-specific, so a different build is a new deployment.

```sh
# Offline recomputation; no server or provider required:
benchmark/julia/score.sh
python benchmark/julia/analyze.py
# Existing homelab deployment; these start services and consume compute:
python benchmark/julia/preflight.py
python benchmark/next-wave/run.py --models julia-1 julia-1-cpu --datasets v2 v1 --execute
```

Run orchestration checks for competing benchmark containers, starts one service,
archives results and stops it in a finally block. Do not run against output directories
containing an earlier attempt; preserve the published archives. Containers can also
be stopped with `sudo docker compose stop julia-1 julia-1-cpu` from the server's
Compose directory. Stopping retains the weights. The [completed comparison](../benchmark/reports/julia-comparison-v2/analysis.md)
records both deployments separately.

## Perplexity Decider 1.1 27B reproduction

[Protocol, verification and compatibility limits](../benchmark/perplexity/README.md).
The installed homelab service is `pplx-decider-27b`, port 11449, in the same
`/var/opt/docker/ai/decision-models-next` Compose project. Its
[captured setup](../benchmark/perplexity/server/) uses read-only volume
`decision_models_pplx`. It needs roughly 52 GB of GPU-addressable memory, including
runtime overhead. Check available VRAM before starting; do not evict unrelated work.

This deployment uses the release's native API with ROCm-compatible dependencies,
reference PyTorch fallback kernels and a strict direct-to-GPU weight loader.
The Dockerfile depends on the homelab's existing ROCm base; it is not a standalone
portable image build. Preserve the pinned source, readout and noncausal attention.
A generic Ollama chat export is a different serving configuration.

```sh
# Unscored verification; includes all manifest hashes and all input encodings:
python benchmark/perplexity/preflight.py
# Starts the model, runs both frozen suites serially, archives, then stops it:
python benchmark/next-wave/run.py --models pplx-decider-27b --datasets v2 v1 --execute
# Offline reporting; no server or credentials required:
benchmark/perplexity/score.sh
python benchmark/perplexity/analyze.py
```

The lifecycle command is `sudo docker compose up -d pplx-decider-27b`; stop with
`sudo docker compose stop pplx-decider-27b` from that server directory. Wait for
`/healthz` status `ok`. The service rejects concurrent work with HTTP 529 and
oversized inputs with HTTP 422. Use a single client request at a time. Retain
published archives when reproducing; use fresh output paths or a separate checkout.
