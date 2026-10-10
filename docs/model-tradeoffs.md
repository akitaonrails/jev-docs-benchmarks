# Model quality and deployment tradeoffs

Updated 10 October 2026. Read alongside the [bilingual results](../benchmark/reports/comparison-v2/analysis.md) and [cost comparison](cost-benefit-ranking.md).

## What the ranking means

Our accuracy ranking measures stock checkpoints applying supplied policies to difficult synthetic cases. It does not rank every project's engineering quality or suitability for every device. A smaller model can be the better deployment choice when it meets the application's quality requirement within a tighter memory, latency, privacy or offline constraint. Lower accuracy still matters when that requirement is not met.

Do not collapse these dimensions into an arbitrary weighted score. First specify acceptable error rates (including critical errors), language and context requirements, and hardware limits. Then compare cost and latency among configurations that pass. An accuracy/latency frontier on this machine is not an energy-efficiency or phone-performance result.

## Laya: a different resource target

The upstream model cards identify the English Laya and typed-decisions checkpoints as **421M-parameter ModernBERT-large encoders**, and multilingual Laya as a **322M-parameter mmBERT encoder**. Their compact, non-generative architecture makes constrained local deployment a plausible advantage. The project also documents an optional ONNX runtime. These are architectural and supported-runtime facts, not measurements of battery life or throughput on our devices. [Laya model card](https://huggingface.co/convaiinnovations/laya), [typed checkpoint](https://huggingface.co/convaiinnovations/laya-typed-decisions), [multilingual checkpoint](https://huggingface.co/convaiinnovations/laya-multilingual).

For scale, 421M parameters at two bytes each imply about **0.84 GB of parameter storage**, and 322M imply **0.64 GB**. These are arithmetic estimates, not download sizes or peak process memory: activations, precision, runtime, tokenization, batching and multiple resident checkpoints add costs. A 4B model at the same precision has roughly 8 GB of parameters before those costs.

| Configuration | Measured v2 compact accuracy, EN / PT-BR | Warm local median / p95, all v2 conditions | Deployment interpretation |
| --- | --- | --- | --- |
| Laya English | 44.0% / 41.7% | 41 / 78 ms | Small, fast measured local candidate; unreliable for this broad untuned policy workload. |
| Laya typed-decisions | 50.0% / 35.7% | 43 / 190 ms | Specialized checkpoint; its training workflows do not establish broad policy or Portuguese coverage. |
| Local Clef-flash | 89.3% / 85.7% | 618 / 935 ms | Better measured general coverage, with substantially slower requests in this deployment. |
| Laya multilingual | Not tested yet | Not tested yet | A separate candidate for Portuguese; English-checkpoint results do not establish its quality. |

The latency rows use the same AMD homelab, warm sequential requests and client-observed LAN timings. They exclude startup/downloads and do not establish sustained throughput. See [captured results and limitations](../benchmark/reports/comparison-v2/analysis.md#runtime-and-reproducibility).

Laya's poor compact scores cannot all be attributed to truncation: compact inputs reported none. Conversely, all 84 Portuguese distractor requests to base Laya reported truncation, so that condition mixes context capacity with decision quality. Those are different weaknesses and should remain separately visible.

A short-text, narrowly defined local router may benefit from Laya after domain evaluation or fine-tuning. Fine-tuning is a new configuration with labeling/training costs and a held-out evaluation; the current results neither demonstrate its benefit nor rule it out. For offline/private use, local execution can be a requirement even when a hosted API is cheap.

## Compare projects within their constraints

| Family or approach | Distinction to preserve | Evidence still needed here |
| --- | --- | --- |
| Laya / GLiNER compact encoders | Smaller resource envelope; native classification interface and language specialization | CPU performance, peak memory, native label/rubric mapping, multilingual accuracy |
| Eikos / Jebadiah / Mapika / Kev around 4B | Larger backbones and different decision training/calibration; Eikos advertises EN/PT training | Frozen-case accuracy, exact checkpoint/base/runtime, memory and latency |
| Simple-Jev | Stock-model token readout wrapper; checkpoint and prompt policy define the entrant | Whether specialized training beats the fixed stock baseline at comparable resources |
| PPLX / Rune larger models | Higher weight residency; MoE active parameters do not equal total stored weights | Actual ROCm compatibility, capacity and quality gain sufficient to justify deployment |
| Hosted Jev / Clef / GLiDE | Provider operates the hardware; API price and WAN latency are relevant | Actual account costs, availability/privacy requirements; hosted hardware efficiency is unknown |

Candidate architecture and license sources are collected in the [verified shortlist](next-models.md). These rows are evaluation categories, not results for untested entrants.

## Next-round reporting requirements

Record exact weights, base/adapter and code revisions; precision/quantization; device/runtime; context and truncation; native probability semantics; cold load and warm latency separately. Measure peak host/device memory with the method stated, particularly because the homelab uses shared memory. Report disk footprint separately from resident memory.

Rank measured quality on the existing frozen cases, then provide deployment-specific recommendations: broad policy accuracy, Portuguese, constrained local execution, and hosted dollar cost. Mark missing energy, CPU and throughput measurements as unknown. Avoid declaring a small model the cheapest merely because its weights are free, or a larger model universally better because it wins accuracy.

## Installation delegation status

The next-wave installation request was queued through ai-memory to `default/homelab-docs` on 10 October, message `01a125d8-2eaa-7de2-ba47-d2f270ac0337`. It requests eight configurations: Eikos-4B, Jebadiah-4B-v2, Mapika Decider-4B, Kev-4B, fixed-Qwen Simple-Jev, Laya multilingual, and both English/multilingual GLiNER2.5-Decide. It requests Docker isolation, pinned provenance, native API contracts, sequential model residency and footprint evidence. PPLX/Rune require a capacity/runtime assessment first. A queued request is not confirmation of installation; benchmark adapter integration awaits the service contracts and smoke evidence.
