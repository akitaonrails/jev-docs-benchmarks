# Julia-1: GPU and CPU benchmark protocol

Test the pinned Supersonic Labs Julia-1 checkpoint on both frozen suites using its
native named-question API. Two separately labeled deployments use identical requests:

| Entrant | Device / precision | Endpoint |
| --- | --- | --- |
| `julia-1` | AMD ROCm gfx1151; FP32 weights, native BF16 autocast forward | `192.168.0.90:11447` |
| `julia-1-cpu` | CPU, FP32, four threads; 8 GiB container memory cap | `192.168.0.90:11448` |

Code and weights revision: `a85b127321d580d65176c89ced8273f305745d85`.
Both use the same Docker image, with no host package installation. This comparison
changes both device and arithmetic; differences cannot be attributed solely to precision.
The GPU track is the primary addition to the existing GPU size comparison. CPU
is shown separately and excluded from the primary parameter-count correlation
so one checkpoint is not counted twice.

## Frozen mapping and verification

The shared SystemOne adapter sends only frozen `state`, `questions`, and selector
`julia-1`. IDs, gold answers and rationales stay local. Native choice IDs, order,
descriptions, Boolean criteria and probabilities are retained. No fine-tuning or
result-guided prompt changes. Warm-up uses an independent refund ticket.

Default strict settings are fixed before inference: **8,192 combined tokens,
512-token head budget, 48 tokens per option, 2–20 options**. The independent
preflight checks both APIs and encodes all **544 v1 + 504 v2** requests on each
service without inference, plus an overflow negative control. Any overflow must
be rejected; nothing may be silently truncated.

The runner verifies the image/command before calling the service and checks
revision, device, precision, context limits and explicit non-truncation telemetry
on every response. A provenance mismatch aborts the run. Both original truncation
fields remain in raw responses; normalized `usage.truncated=false` is derived only
when both native flags are explicitly false. Generic probability validation and
all existing scoring rules remain in force.

## Execution

Start only one benchmark container at a time. Sequential seeded requests, one
attempt each, v2 then v1 for each deployment. Start/load and independent warm-up
are outside scored latency; client wall time includes LAN and serving overhead.
Each container is stopped in a `finally` block. Retain weights; do not stop unrelated
services. Existing hosted/local response archives are reused with no further API calls.

```sh
# Inspect the existing deployment first; preflight starts/stops these two services.
python benchmark/julia/preflight.py
# After preflight succeeds:
python benchmark/next-wave/run.py --models julia-1 julia-1-cpu --datasets v2 v1 --execute
# Offline combined reports:
benchmark/julia/score.sh
```

Raw archives use `benchmark/reports/next-wave-v1/julia-1[-cpu]` and
`next-wave-v2/julia-1[-cpu]`; new combined reports use `julia-comparison-v1/v2`.
Earlier comparison reports retain their dated scope. Local electricity, capital
and maintenance cost are unmeasured; no hosted per-token price is assigned.

## Deployment evidence

- [Installation handoff](installation-handoff.md) records the homelab agent's work.
- [Runtime evidence](../reports/julia-runtime/) records our independent checks.
- [Captured server code and image recipe](server/) and [resolved deployment](server/compose.json).
- [Published model card](https://huggingface.co/SupersonicLabs/Julia-1/tree/a85b127321d580d65176c89ced8273f305745d85).

The image recipe refers to a homelab ROCm base image and is not an exact portable
rebuild by itself. Use the captured image digest and resolved dependency versions
for provenance, or build a compatible environment and label it a new deployment.

## Completed results

[Analysis and 19-configuration ranking](../reports/julia-comparison-v2/analysis.md):
2,096 valid scored requests, all untruncated. Both configurations score 31.5%
compact. Run `python benchmark/julia/analyze.py` after scoring for paired-device
diagnostics and unchanged-baseline verification.
