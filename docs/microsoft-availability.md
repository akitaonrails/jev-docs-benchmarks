# Microsoft Decision-1: hosted access

Verified **11 October 2026**. The model is accessible with an existing funded
OpenRouter account. Our independent request returned the dated model identifier
`microsoft/microsoft-decision-1-20261009`, provider `Azure`, and a valid native
choice distribution. Authentication and inference both succeeded.

## Access paths

| Route | Requirements | API |
| --- | --- | --- |
| OpenRouter, used here | OpenRouter API key and credits | `POST https://openrouter.ai/api/alpha/decisions`, model `microsoft/microsoft-decision-1` |
| Microsoft Foundry | Azure subscription and model deployment | Foundry deployment; follow Microsoft's current deployment documentation |

The launch announcement described OpenRouter as coming soon, but the live catalog
and successful inference establish that it is available now. The default text-model
list may omit it; use `/api/v1/models?output_modalities=decisions` or
`/api/v1/models/microsoft/microsoft-decision-1/endpoints`.

Microsoft describes a model post-trained from Qwen3.5-9B for scoring fixed options.
It uses the same state/questions style as the benchmark's existing native decision
track. No chat prompt translation or label-only classification fallback is needed.
Nominal size is 9B, and the listed context window is 32,768 tokens. Public local
weights were not identified; this benchmark uses a hosted deployment.

OpenRouter lists **$0.042 per million input tokens and $0 for output**. The smoke
reported 58 input tokens and $0.000002436 cost, exactly matching that rate. Actual
request token counts matter: equal per-token rates do not imply equal per-decision
cost across vendors. Account purchase fees, taxes and local operating costs are
outside the request usage calculation.

The provider describes its probabilities as calibrated. That remains a vendor claim
until evaluated on the intended distribution; our classification, Brier and separate
known-random-outcome probes measure different aspects of probability behavior.
A dated returned model ID also does not guarantee immutable hosted weights.

## Evidence and reproduction

- [Microsoft announcement](https://commandline.microsoft.com/microsoft-decision-1-model-foundry/)
- [OpenRouter model, pricing and limits](https://openrouter.ai/microsoft/microsoft-decision-1)
- [OpenRouter native Decisions request example](https://openrouter.ai/blog/insights/what-is-jev/)
- [Captured live endpoint metadata](../benchmark/reports/microsoft-runtime/endpoints.json)
- [Frozen protocol and Docker commands](../benchmark/microsoft/README.md)
- [Benchmark analysis](../benchmark/reports/microsoft-comparison-v2/analysis.md)
