# Julia-1 availability

Checked 2026-10-11 UTC / 2026-10-10 São Paulo. **Available for local testing; not yet tested here.**

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
This would extend our resource-constrained model comparison; no score or ranking
is assigned until we run it.

The published Portuguese evaluation is **pt-PT**, not evidence for our PT-BR cases.
Its reported Jev comparisons use supplied reference values rather than a new
paired Jev run.

Sources: [model card and Python API](https://huggingface.co/SupersonicLabs/Julia-1),
[publisher's runtime documentation](https://huggingface.co/SupersonicLabs/Julia-1/blob/main/julia/router/README.md).
