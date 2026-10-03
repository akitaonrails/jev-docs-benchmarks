# Jev alternatives: Clef, Laya, and the emerging ecosystem

Research snapshot: **3 October 2026**. This comparison uses the vendors' documentation, model cards, source repositories, and the open Decision Index suite. Benchmark numbers are the publishers' results; this repository did not rerun them.

## Short conclusion

Cloudflare Clef weakens the strongest argument that Jev is a uniquely new category. Clef exposes almost the same typed-decision abstraction, publishes its weights and custom model code under Apache 2.0, and adds image input. Its architecture is also described: a frozen Qwen base, LoRA adapters, and a head that scores the supplied options directly. This makes the implementation inspectable and shows that a Jev-like product can be built from established components. [Cloudflare launch](https://blog.cloudflare.com/clef-decision-models/), [Clef model card](https://huggingface.co/Cloudflare/clef), [Clef-flash model card](https://huggingface.co/Cloudflare/clef-flash).

Laya makes the same point from the other direction. It is a small open encoder model that can run locally and be fine-tuned for a recurring decision. Its honest published limitations also show the catch: the base checkpoints are weak zero-shot decision engines, while the good headline result comes from fine-tuning on the benchmark's training split. Laya is best understood as an inexpensive foundation for a specialized classifier, rather than a drop-in universal Jev replacement. [Laya repository and model cards](https://github.com/NandhaKishorM/laya).

The practical category now has three distinct products:

- **Jev:** the cheapest listed hosted service of the three, text only, proprietary, and convenient.
- **Clef / Clef-flash:** open weights plus managed hosting, stronger published general results, and vision support, but substantially larger models and higher hosted prices.
- **Laya:** small, local, customizable models for narrow repeated tasks, with shorter context and much weaker zero-shot evidence.

The novelty is therefore less about inventing classification and more about packaging arbitrary, request-defined decisions into a fast API. Clef's published implementation makes that technical lineage much clearer than Jev's public material does.

## Capability comparison

| | Jev 1.13 | Clef | Clef-flash | Laya typed decisions |
| --- | --- | --- | --- | --- |
| Operating model | TypeSafe hosted API | Cloudflare hosted API or self-hosted weights | Cloudflare hosted API or self-hosted weights | Self-hosted Python, ONNX, or optimized runtimes |
| License / inspectability | Proprietary service; weights and architecture unpublished | Apache 2.0 weights and custom code | Apache 2.0 weights and custom code | Apache 2.0 code and weights |
| Foundation | Undisclosed | Qwen3.8-27B with vision encoder, frozen base, rank-256 LoRA and schema head | Qwen3.5-9B, frozen base, rank-256 LoRA and schema head | ModernBERT-large encoder, 421M parameters; other Laya checkpoints include a 322M multilingual model |
| Input | Text or text-bearing JSON | Text/JSON and images; the local model card also demonstrates video as frames | Text/JSON and images; the local model card also demonstrates video as frames | Text |
| Hosted context | 64k total; 32k state plus longest question | 65,536 tokens | 65,536 tokens | 1,024 tokens for the typed checkpoint; other checkpoints range from 512 to 1,024 by default |
| Questions / options | Multiple questions; up to 255 choices | Up to 64 questions per hosted request | Up to 64 questions per hosted request | Jev-compatible server; up to 100 options over HTTP, subject to head and truncation limits |
| Listed hosted input price | **$0.042 / million tokens** | **$0.24 / million tokens** | **$0.09 / million tokens** | No vendor inference fee; the operator pays hardware and maintenance |
| Customization | No account-specific fine-tuning or LoRA | Weights are available, so self-hosted adaptation is possible | Weights are available, so self-hosted adaptation is possible | Fine-tuning is a central use case; scripts cover commodity NVIDIA GPUs and Apple Silicon |
| Best fit | Cheap, hosted, high-volume text judgments | Hosted or self-hosted decisions where quality or vision justifies a large model | Lower-latency hosted decisions and lighter self-hosting than Clef | Private or offline, stable-domain decisions with labeled training data |

Sources: [Jev model reference](https://docs.typesafe.ai/models), [Jev primitives](https://docs.typesafe.ai/primitives), [Clef Workers AI reference](https://developers.cloudflare.com/workers-ai/models/clef/), [Clef-flash Workers AI reference](https://developers.cloudflare.com/workers-ai/models/clef-flash/), [Clef model card](https://huggingface.co/Cloudflare/clef), [Laya](https://github.com/NandhaKishorM/laya).

The prices are not a complete cost comparison. Jev and Workers AI are managed services; local Clef or Laya requires hardware, scaling, monitoring, and model updates. On the published input rates alone, Jev is about 2.1 times cheaper than Clef-flash and 5.7 times cheaper than Clef. Cloudflare includes a daily free allocation for Workers AI, which can dominate price at very low volume. [Workers AI pricing](https://developers.cloudflare.com/workers-ai/platform/pricing/).

## What Clef changes

Clef uses the same useful interface shape: one shared state, multiple typed questions, and a distribution over choices or ordinal scores. Cloudflare says its API is compatible with Jev/SystemOne. The response format therefore is not a durable differentiator by itself.

Its disclosed design is closer to a large, adaptable classifier than to a normal chat model. The Qwen backbone encodes the state and questions; a joint schema head assigns a logit to each allowed option. Cloudflare trains the adapters and head with classification and calibration objectives, including label-smoothed cross-entropy, Brier loss, and a secondary reinforcement-learning objective. It is still probabilistic semantic judgment. The direct option head avoids spending time generating prose and guarantees that the output belongs to the supplied schema.

Clef adds two meaningful product capabilities:

1. **Open deployment:** an organization can inspect, host, quantize, and adapt the weights instead of sending every decision to one vendor.
2. **Vision:** images can be part of the state. The local examples also represent video as a sequence of frames. This expands the pattern to document images, screenshots, moderation, and visual routing. It does not turn Clef into OCR, translation, object detection, or evidence verification.

The tradeoff is size. The model cards describe 9B and 27B BF16 models and report testing on an H200. They are far heavier than Laya's 322M–421M encoders. A local deployment should be benchmarked on the exact quantization and hardware; the hosted latency numbers do not predict a laptop deployment.

Cloudflare says Workers AI does not use customer content to train models or improve its services without consent, and content is stored when the customer explicitly uses a storage service. A self-hosted model still gives the operator stronger control over the data path. [Workers AI data usage](https://developers.cloudflare.com/workers-ai/platform/data-usage/).

## What Laya actually offers

Laya is the more revealing alternative for local use. Its checkpoints are encoder models with a choice-scoring head, not multi-billion-parameter chat models. Arbiter packages them behind a Jev-compatible service and adds batching, routing, metrics, and Mac/NVIDIA deployment. Arbiter is a serving layer; it is not a fourth decision model. [Laya](https://github.com/NandhaKishorM/laya), [Arbiter](https://github.com/0xBakeer/arbiter), [Fr3akaz0id's Arbiter fork](https://github.com/Fr3akaz0id/arbiter).

Laya's current README is unusually explicit about its limits:

- Its base checkpoints score near chance on the project's typed-decision benchmark. The reported **0.766** argmax accuracy comes from a checkpoint fine-tuned on that benchmark's training split.
- That fine-tuned run is disclosed without a committed result artifact at the time of this snapshot, so it is not independently auditable from the repository alone.
- The base checkpoints are overconfident as shipped. Post-hoc temperature fitting improves expected calibration error, but calibration must be redone for the deployment domain.
- Large choice sets consume a limited classification head budget, option text can be truncated, and labels can collapse. Laya reports Jev doing better when there are more than 50 options.
- The typed checkpoint's 1,024-token context is enough for short tickets and messages, but not a substitute for Jev or Clef on long documents without chunking or retrieval.

This profile is not a defect in the idea. It describes conventional applied machine learning: a small model can be excellent when the task is stable and labeled examples exist, while broad zero-shot behavior usually needs a much larger pretrained model. Laya is most attractive when privacy, offline operation, predictable latency, or domain fine-tuning matters more than arbitrary questions on arbitrary documents.

## Benchmark evidence

Cloudflare evaluated the models with [Decision Index](https://github.com/apolinario/decision-index), an open, unaffiliated reproduction suite containing dozens of classification, routing, retrieval, safety, and workflow tasks. The suite pins dataset hashes and counts unanswered items as wrong. This is broader evidence than a handful of product demos, but Cloudflare's published figures are still an **internal run**, and a public fixed suite can be trained or tuned against.

Selected scores from Cloudflare's 1 October launch table are below. Higher is better. These numbers compare the submitted configurations; they do not establish that every model received equivalent task-specific tuning.

| Decision Index task | Clef | Clef-flash | Jev | Laya |
| --- | ---: | ---: | ---: | ---: |
| BFCL tool selection | 98.47 | **98.76** | 95.75 | 38.13 |
| API-Bank tool use | 91.93 | **93.11** | 88.19 | 11.41 |
| Banking77 intent | **94.20** | 90.93 | 79.74 | 14.29 |
| CLINC150 plus out-of-scope | **97.43** | 66.77 | 89.27 | 3.19 |
| When2Call | 72.37 | 65.58 | **80.97** | 11.94 |
| BRIGHT retrieval | 45.91 | 39.26 | **47.52** | 19.90 |
| PhishNChips | **79.60** | 75.05 | 62.55 | 50.15 |

Cloudflare also reran TypeSafe's four workflow evaluations. Clef or Clef-flash led three workflows, while Jev led agent-trace analysis. The differences were small on several tasks. This supports a more modest conclusion than the launch headline: Clef appears broadly competitive and often stronger under Cloudflare's test setup, while Jev still wins some tasks.

Cloudflare reports median inference latency of 209 ms for Clef, 39 ms for Clef-flash, 524 ms for Jev, and 6 ms for Laya in the same internal run. Those figures mix a hosted third-party API with models running in Cloudflare's environment and should not be read as architecture-only comparisons. Laya's reported 6 ms median and 223 ms p95 also show how batching, warmup, or the input mix can distort a single latency headline. End-to-end measurements on the intended deployment are the useful numbers. [Cloudflare launch and methodology](https://blog.cloudflare.com/clef-decision-models/).

## Which one should be used?

| Situation | First candidate | Why |
| --- | --- | --- |
| Short, high-volume English text; minimal operations | **Jev** | Lowest listed hosted price and the simplest managed route |
| General zero-shot decisions where accuracy matters more than the lowest token price | **Clef-flash**, then Clef | Stronger breadth in Cloudflare's published run; validate both because the larger model did not win every task |
| Decisions over screenshots, photos, or document images | **Clef / Clef-flash** | The only options here with native vision input |
| Private, offline, or low-resource recurring classification | **Laya**, fine-tuned | Much smaller model and local control; requires task data and calibration |
| More than 50–100 candidate options or long documents | **Jev or Clef**, tested directly | Laya documents head-budget and context limitations |
| Authorization, fraud clearance, destructive tool approval | **Deterministic policy plus review** | Any model may contribute a signal; none should be the authority |
| Small fixed taxonomy with labeled examples | **A conventional local classifier as baseline** | It may be cheaper, easier to calibrate, and easier to audit than all three |

Another open implementation, [Kev-9B](https://huggingface.co/jaredpalmer/kev-9b), combines a frozen Qwen3.5-9B base, a smaller LoRA adapter, and a pointer-style decision head under Apache 2.0. Its model card says it fits a 24 GB GPU and is validated primarily on English text and shorter contexts. Its existence, along with Clef and Laya, reinforces that typed-decision models are becoming an implementation pattern rather than a single proprietary invention.

## Effect on this portfolio

The alternatives broaden a few candidate experiments, but they do not change the portfolio-wide conclusion in [Real use cases and project fit](use-cases.md): most projects need exact policy, specialist vision/audio systems, or generated content.

- **FrankClaw:** Clef-flash is a credible hosted competitor to Jev for model routing and trace triage. Laya is more interesting if enough real routing examples can be labeled and local inference matters. Hard approval rules remain deterministic.
- **Frank Sherlock:** Clef can inspect images directly, so it is a more plausible document-category or review-priority component than Jev. It still does not replace the existing vision descriptions, Surya OCR, or local-only data story. A fine-tuned local vision classifier remains the relevant baseline.
- **Frank Yomik:** Clef could classify page regions or decide which processing path an image needs. OCR, translation, and furigana generation remain specialist tasks, so the added service only makes sense if routing failures are measured.
- **Frank FBI:** Clef can incorporate a rendered email or screenshot, and Laya can be trained on a stable local fraud taxonomy. Neither should replace headers, SPF/DKIM, URL reputation, or evidence-backed review.
- **ai-memory and Frank Investigator:** all three can rank a bounded shortlist. None generates the synthesis, proves a claim, or supplies provenance. A local reranker remains the baseline.

For these projects, the category is **general as an interface but niche as a replacement**. Many applications contain bounded decisions; relatively few of the reviewed applications have enough costly, repeated, ambiguous decisions to justify another model service today.

## Final assessment

Jev was early and polished, but the public evidence now supports calling this a product category rather than a unique technical primitive. Clef demonstrates an open large-model implementation with a compatible API and wider modalities. Laya demonstrates the small, local, task-specific end of the same design space.

The useful question is no longer “is Jev novel?” It is: **for one measured decision, which combination of model quality, price, latency, privacy, context, and maintenance beats the current rule, classifier, or constrained LLM?** No vendor benchmark can answer that without the project's own labeled cases.
