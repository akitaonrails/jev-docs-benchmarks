# Perplexity Decider 1.1 27B benchmark protocol

Evaluate `perplexity-ai/pplx-decider-v1.1-27b` revision
`6195aa55a72ae21e503c8a60198f7b390d42adb5` on both unchanged suites: **504 v2 and
544 v1 requests**, serially, one attempt each. Gold labels and rationales stay
client-side. Use the native SystemOne request/response without prompt tuning,
probability recalibration or extra generation. Treat the nominal 27B label
consistently with other entries in size analysis.

## Runtime and deviations

Homelab AMD gfx1151 service `pplx-decider-27b`, port **11449**, pinned image
`sha256:1ca2a7509863a7d1de08ad5ab5e002ca28cc0f878f648f4d971712dcb8916910`.
BF16 weights and readout, no quantization or CPU offload. Model weights are mounted
read-only. Native last-token pooling, noncausal full attention and temperature
**1.0087417621345625** are preserved. The release server applies temperature once
to native logits before softmax; the benchmark never applies it again.

This is a **ROCm compatibility deployment**, not a reproduction of the publisher's
CUDA environment. Torch is 2.9.1+rocm7.2.1 instead of release-pinned 2.14.0.
Transformers 5.17.0 is preserved. Missing flash-linear-attention and causal_conv1d
use Transformers' reference PyTorch paths, with possible rounding and speed effects.
A custom loader creates the same backbone and strictly copies all checkpoint
keys with matching shapes/dtypes directly to GPU, avoiding the original loader's
host-memory OOM. The loader and runtime source are reviewed; we do not claim
numerical equivalence to a separate CUDA/reference-loader run that we did not perform.
See [handoff](installation-handoff.json) and [captured launcher](server/run_pplx.py).

## Verification before scoring

Owner: the benchmark runner here. Minimum evidence:

- Verify image/command, read-only volume, actual launcher bytes and all 46 manifest
  file hashes before scored inference.
- Review native prepare/forward/server code for unchanged options, 8,192-token
  overflow rejection, masked candidate logits and exactly-once temperature.
- Independent choice/Noul smoke plus encoding all 1,048 frozen requests. Oversized
  input must return HTTP 422. No scored inference in preflight.
- Record health provenance before and after each scored suite. Every scored token
  count must match the complete preflight encoding for the exact request hash.
- Run offline contract tests; verify archives and preserve earlier entrant summaries.

The native API does not return a per-response truncation flag. Raw responses stay
unchanged; losslessness is established separately by the pinned prepare code,
negative control and matched token counts. Common report telemetry will correctly
show that the native flag is absent. Do not mistake that absence for truncation.

## Execution and reproduction

```sh
# Existing homelab deployment; starts/stops service, unscored checks:
python benchmark/perplexity/preflight.py
# Manifest verification runs in a separate CPU container using verify_manifest.py.
# After readiness, hash verification and the protocol freeze:
python benchmark/next-wave/run.py --models pplx-decider-27b --datasets v2 v1 --execute
# Offline combined scoring:
benchmark/perplexity/score.sh
```

Leave other GPU workloads alone. Require sufficient headroom (roughly 52 GB used
by the deployment), one benchmark container at a time, then stop the service.
Start/load and independent warm-up are excluded from scored latency. Existing
hosted archives are reused; no hosted requests are part of this addition. Local
power, utilization, amortization and operations costs remain unmeasured.

[Runtime evidence](../reports/perplexity-runtime/) ·
[Published checkpoint](https://huggingface.co/perplexity-ai/pplx-decider-v1.1-27b/tree/6195aa55a72ae21e503c8a60198f7b390d42adb5).
