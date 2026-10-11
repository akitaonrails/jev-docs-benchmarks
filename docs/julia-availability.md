# Julia-1 availability

Checked 2026-10-11 UTC / 2026-10-10 São Paulo. **Tested on GPU and CPU: 1,048 valid requests each.**
See the [completed analysis and ranking](../benchmark/reports/julia-comparison-v2/analysis.md).

The project is **Julia-1 by Supersonic Labs** (`@supersonicai`). Its published
checkpoint has **144.3M parameters**, derives from multilingual mmBERT-small,
and uses Apache-2.0 licensing. The FP32 weights occupy approximately **550.5 MiB**;
runtime memory is additional. CPU inference is supported.

Its native `predict(state=..., questions=...)` API supports named choices, scores
and Boolean probabilities. The 2–20 option limit fits our suites. The publisher
provides custom Python runtime code; this is not a standard Transformers pipeline.
The Hugging Face page lists no deployed Inference Provider. We have not established
a production hosted API or obtained any hosted credentials.

For our benchmark, use an isolated Docker runtime, pin code and weights, preserve
criteria including Boolean descriptions, and enable strict encoding. Inspect
question/option token budgets before inference: overflow must not silently discard
policy. Keep CPU latency separate from the existing homelab GPU measurements.
Both deployments scored 31.5% on compact bilingual cases. The
[protocol](../benchmark/julia/README.md) records exact precision and setup.

The published Portuguese evaluation is **pt-PT**, not evidence for our PT-BR cases.
Its reported Jev comparisons use supplied reference values rather than a new
paired Jev run.

Sources: [model card and Python API](https://huggingface.co/SupersonicLabs/Julia-1),
[publisher's runtime documentation](https://huggingface.co/SupersonicLabs/Julia-1/blob/main/julia/router/README.md).

## Installation request

The user authorized delegation to the homelab agent. The
[request and exact message ID](../benchmark/openai-decisions/julia-install-request.md)
were sent to `default/homelab-docs`. It requests a pinned Docker service, native
choice/Boolean smoke checks, explicit device/precision metadata and strict
encoding checks on both frozen suites. Installation, independent readiness checks and both scored runs are complete.
Both containers were stopped afterward; weights are retained.
