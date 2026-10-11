# Benchmark developer guide

See the root [README](../README.md) for goals and results, and [setup guide](../docs/setup.md)
for the tested client/server workflow. This page provides implementation details.

A frozen synthetic benchmark for Jev and Cloudflare Clef/Clef-flash, with local
Laya/Laya-typed/Clef-flash on the AMD homelab. [Protocol](PROTOCOL.md) defines the scope,
metrics and limitations before inference. [Scenarios](datasets/scenarios.py) are the
readable source; [cases.jsonl](datasets/cases.jsonl) is the frozen evaluation artifact.

## OpenAI Decisions extension

The [native endpoint protocol](openai-decisions/README.md) preserves the frozen
state, instructions and option descriptions and maps Noul probes to predicates.
See the [updated comparison](reports/openai-comparison-v2/analysis.md),
[ranking](reports/openai-comparison-v2/ranking.md), and
[usage reconciliation](reports/openai-comparison-v2/costs.md).
Docker scripts run the API client and score against all existing archives.

## First hosted run

[Findings and interpretation](reports/hosted-v1/analysis.md) · [Full tables](reports/hosted-v1/results.md) · [Machine-readable metrics](reports/hosted-v1/summary.json). All 1,632 planned requests completed. Jev and Clef tied at 97.2% across variants after the explicitly disclosed gold-ambiguity exclusions; probability probes exposed different weaknesses by primitive.

[Verified pricing and cost reconciliation](reports/hosted-v1/pricing.md) distinguishes
published-rate usage value from actual charges and accounts for the daily free allowance.

## Completed homelab comparison

[Hosted versus local findings](reports/comparison-v1/analysis.md) · [Six-model tables](reports/comparison-v1/results.md) · [Local evidence](reports/homelab-v1/analysis.md).
All 1,632 local main requests completed on 10 October. Laya and Laya-typed each scored
38.5% across classification variants; pinned local Clef-flash scored 89.0% and matched
every hosted Clef-flash classification label. Workstation RTX 5090 testing remains deferred.

## Dataset

- 13 domains × 10 authored scenarios × 4 forms = **520 classifications**.
- Forms: original, reversed options, opaque option names, misleading commentary.
- **24 separate probability probes** pair Choice/Noul on unknowable uniform outcomes.
- 544 requests per model, 1,632 across Jev, Clef and Clef-flash.

These are 130 authored scenario families, not 520 independent examples. Golds were
AI-authored and reviewed against explicit fictional policies before inference. There
is no independent human annotation or claim that these cases represent production
traffic. Some cases share counterfactual policy pairs. Calibration and intervals
are diagnostics for this synthetic collection, not general deployment guarantees.
No gold answers, explanations, tags or case identifiers go into provider requests.

## Isolation

The hosted runner and scorer use Python's standard library inside a small Docker
image. No pip packages, SDKs, virtual environments or model weights are installed on
the host. The small `launch.py` helper uses existing host Python only to read three
literal credential exports and invoke Docker, without executing the secrets file.

Containers have no host home or Docker socket, no GPU on the hosted/offline paths,
no privileged mode or published ports. Inputs are read-only; results are writable.
Hosted execution uses outbound HTTPS. Offline scoring has networking disabled and
receives no credentials. The local services still require a separate profile and
`--allow-inference`; those workstation CUDA recipes have not been built or run.
The separate AMD homelab service has completed the recorded local runs.

## Credentials

Configured in `~/.config/zsh/secrets`, mode 0600:

- `JEV_API_KEY`
- `CLOUDFLARE_API_TOKEN` (confirmed Workers AI API token)
- `CLOUDFLARE_ACCOUNT_ID`

The launcher reads only those exports and passes them as environment variables.
Their values are never printed or committed. Do not print expanded Compose config;
use `docker compose -f benchmark/compose.yaml config --quiet` instead.
Users with Docker access can inspect container environments.

## Reproduce

From the repository root:

```sh
# CPU images only; no local-model image or GPU access.
docker compose -f benchmark/compose.yaml --profile hosted build runner hosted

# Offline tests; no credentials or network.
benchmark/tools/offline.sh -m unittest discover -s tests -v

# Presence check, then an optional paid 3-request smoke test.
python3 benchmark/tools/launch.py /work/tools/preflight.py
python3 benchmark/tools/launch.py /work/tools/hosted.py \
  --output /results/smoke-new --limit 1 --execute

# Paid run. Use a new directory for a genuinely new run.
python3 benchmark/tools/launch.py /work/tools/hosted.py \
  --output /results/hosted-new --cost-cap 5 --execute

# Offline scoring into a tracked report directory.
benchmark/tools/offline.sh /work/tools/score.py \
  /work/results/hosted-new --output /reports/hosted-new
```

Reusing an output directory resumes only when model set, dataset, runner hash and
configuration match. Already persisted cases, including errors, are skipped. Keep
failures visible; retries of completed errors need a separately identified run.
The sequential schedule interleaves all models using a fixed random seed. Latency
includes network/service overhead and retries; it is not a GPU microbenchmark.

The $5 flag caps a conservative input-cost reservation, not the provider invoice.
The report computes price × actual reported successful input tokens; unreported
failed-attempt charges and discounts are not knowable from that calculation.
The user's instruction to run hosted models supersedes the previous setup-only hold.

Jev is pinned to `jev-1.13.0`. Hosted Clef names are vendor-managed aliases; returned
model IDs and dates are recorded, but exact hosted weights cannot be pinned here.
The CPU base image digest and Docker image ID are recorded with the run artifacts.
No model-specific tuning is performed after seeing results.

## Results and auditability

`results/` holds resumable raw runs and is Git-ignored. Completed results are archived
under `reports/` with raw response records, run configuration, scores, every failed
classification, and analysis. The scorer verifies dataset and request hashes and
rejects duplicate responses. Probabilities are checked for allowed labels, finite
values and sum-to-one within documented rounding tolerance. Raw values are preserved;
normalized values are used for scoring. Vendor confidence is not interpreted as accuracy.

The dataset is test-only: no classifier, calibrator or threshold is fitted on it.
If future work tunes against these results, use a fresh held-out dataset and keep
related variants and policy pairs together. Post-run gold corrections must be an
explicit erratum and separate rescoring, never a silent fixture change.

## Homelab runs

The LAN adapter uses the isolated ROCm SystemOne service at `192.168.0.90:11436`.
See [local protocol](LOCAL-PROTOCOL.md). No workstation GPU or API credentials are used.
The service must already be provisioned; this client never installs or loads host packages.
It checks discovery and response snapshot metadata against `models.json`.

```sh
# Six preliminary calls, saved separately.
benchmark/tools/homelab.sh --smoke --output /results/homelab-smoke-new --execute
# All 544 frozen cases × three models. Use a new directory for a new experiment.
benchmark/tools/homelab.sh --output /results/homelab-new --execute
# Archive and score offline, with no further inference.
benchmark/tools/offline.sh /work/tools/archive.py /work/results/homelab-new /reports/homelab-new
benchmark/tools/offline.sh /work/tools/score.py /work/reports/homelab-new --output /reports/homelab-new
benchmark/tools/offline.sh /work/tools/compare.py /work/reports/hosted-v1 /work/reports/homelab-new --output /reports/comparison-new
```

`laya`, `laya-typed` and `clef-flash-local` are distinct entrant IDs. All server metadata
is retained in raw archives. Local electricity and hardware costs are unmeasured;
we do not assign a hosted token rate or claim zero operating cost.

## Deferred workstation RTX 5090 runs

[models.json](models.json) pins Laya English, Laya typed-decisions and Clef-flash
checkpoints. Treat the two Laya checkpoints as separate entrants, without automatic
routing. The original CUDA stdin worker remains preliminary plumbing; use the homelab adapter
above for the validated HTTP workflow.

Laya should have a modest memory footprint. Clef-flash's 9B BF16 backbone implies
roughly 18 GB in weights plus head/runtime/activations; actual RTX 5090 fit is untested.
Full Clef's 27B BF16 backbone implies roughly 54 GB before overhead, so use hosted
Clef initially. Quantization or offloading would be a separately named configuration.

Docker and Compose work. `nvidia-container-runtime` exists, but Docker did not list
an NVIDIA runtime during preparation. Check GPU integration later; no daemon settings
were changed and no GPU container was started. Local recipes use CUDA 12.8 Torch
wheels; local dependency resolution, runtime compatibility and pinned remote model
code still need review. Do not run these while the GPU is occupied:

```sh
docker compose -f benchmark/compose.yaml --profile local build laya clef-flash
# Future opt-in entrypoint; requires prepared state/questions-only requests.jsonl.
docker compose -f benchmark/compose.yaml --profile local run --rm -T laya \
  laya --allow-inference < requests.jsonl
```

Model caches will live in a Docker volume. Containers use no restart policy. Cleanup:
`docker compose -f benchmark/compose.yaml --profile local --profile hosted down`.
Add `--volumes` only to intentionally delete cached weights; images occupy separate
Docker storage. Credentials are not part of the published repository.

## Sources

- [TypeSafe API](https://docs.typesafe.ai/api)
- [Jev models and pricing](https://docs.typesafe.ai/models)
- [Clef API and pricing](https://developers.cloudflare.com/workers-ai/models/clef/)
- [Clef-flash API and pricing](https://developers.cloudflare.com/workers-ai/models/clef-flash/)
- [Clef-flash local model card](https://huggingface.co/Cloudflare/clef-flash)
- [Laya](https://github.com/NandhaKishorM/laya)

[Current technical and cost-benefit ranking](../docs/cost-benefit-ranking.md) adds classification-only unit economics, the 10 October Flash price change, and scenario-dependent recommendations.


## Completed bilingual expansion

V2 adds 84 new authored families × English/PT-BR × three conditions = 504 cases
per model, 3,024 new classifications. Use its [protocol](expansion-v2/README.md),
[analysis and ranking](reports/comparison-v2/analysis.md), and
[complete tables](reports/comparison-v2/results.md). It has its own `score_v2.py`;
do not feed its archives into the v1 scorer or average its scores into v1.
The [setup guide](../docs/setup.md) contains the exact v1/v2 commands.

## Next-wave open models

The [next-wave protocol](next-wave/README.md) covers ten additional configurations,
including three Kev sizes and native GLiNER classification mappings. See the
[expanded analysis](reports/next-wave-comparison-v2/analysis.md),
[ranking](reports/next-wave-comparison-v2/ranking.md), and
[expanded policy-suite tables](reports/next-wave-comparison-v1/results.md).
