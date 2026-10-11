# Real use cases and fit in my projects

## Measured follow-up: Perplexity 27B

The [latest benchmark](../benchmark/reports/perplexity-comparison-v2/analysis.md)
supports testing a local open checkpoint for supplied-rule classification: Perplexity
scores 99.4% compact and all PT-BR cases correctly. This strengthens the case for
a bounded local experiment in routing, evidence relevance or policy triage when
data locality matters. It does not measure any of the actual projects below.

Its roughly 49 GiB weights and 1.55-second observed median request time make it a
substantial shared homelab workload. Smaller Jebadiah 4B remains a practical comparison
point; deterministic parsing and exact policy rules still belong in ordinary code.
Perplexity's remaining retrieval mistake confuses notification recipients with
required approvers, so avoid treating semantic association as authorization evidence.

Research snapshot: **3 October 2026**. Project assessments are based on the top-level READMEs present in `~/Projects`, not code review, traffic measurements, or local model experiments. “Candidate” means a bounded experiment could be justified if the current path is demonstrably slow, expensive, or inaccurate. It is not a recommendation to integrate immediately. See [the alternatives comparison](alternatives.md) for how Clef's vision support and Laya's local fine-tuning affect these cases.

The project names below refer to READMEs inspected in the author’s local checkout;
those local filesystem links have been omitted from the published copy. No private
project source or customer data is included. These are project-fit hypotheses, not
measurements on those applications.

## The useful shape

A Jev-like model is most useful when **the same kind of text judgment happens many times**, the possible actions can be enumerated, the surrounding code can implement exact rules, and a wrong answer can be detected or routed to review. Examples include support-ticket department and urgency, ranking a shortlist of retrieved passages, routing agent requests to a model, or flagging a trace for review. Several questions over the same state can share one call. [TypeSafe primitives](https://docs.typesafe.ai/primitives), [patterns](https://docs.typesafe.ai/patterns).

It is a poor fit when the main input is an image or audio stream, the output needs prose or citations, an exact parser or specialist engine already solves the task, or a misclassification grants access or performs a destructive action. Jev 1.13 takes text only and TypeSafe documents numerical, date, adversarial-content, and context limitations. [Model limits](https://docs.typesafe.ai/models), [jaggedness](https://docs.typesafe.ai/model-jaggedness/jev-1.13).

| Decision type | Plausible use | Boundary |
| --- | --- | --- |
| Semantic triage | Route a short message or incident to a queue; send ambiguous cases to review | Measure against labeled tickets; include `other`/`unknown` where appropriate |
| Candidate ranking | Score already retrieved snippets or possible actions | Retrieval supplies candidates; the model does not establish the facts in them |
| Model routing | Estimate whether a request needs a stronger model | Compare final answer quality and total cost, not router speed alone |
| Agent observability | Flag traces with a bounded set of concerning patterns | Use it as a review signal; keep exact security checks in code |
| Closed-set extraction | Choose among candidate spans found by code or OCR | It cannot create arbitrary new text or replace OCR |

## README-based portfolio review

| Project | Fit | Reason and possible experiment |
| --- | --- | --- |
| `ai-jail` | **No** | OS sandbox and capability policy. A probabilistic command label must not grant filesystem, network, credential, or Docker access. At most, an optional advisory prompt outside enforcement; no evident benefit to the core product. |
| `ai-memory` | **Candidate, low priority** | It already offers zero-LLM capture, FTS/entity/vector retrieval and optional LLM consolidation. A decision model could rerank a *small shortlist* of memories for a query or flag an observation for consolidation, but it cannot write the wiki page. Test only if current retrieval misses relevant memories and compare with existing hybrid ranking and a local reranker. Hosted calls also change its zero-LLM/local ownership story. |
| `ai-memory-web` | **No** | Static marketing site with deterministic release, i18n, and accessibility checks. No recurring semantic decision in the runtime. |
| `ai-usagebar` | **No** | Reads quota and status APIs, caches and presents numbers. Provider-specific parsing and exact arithmetic belong in code. |
| `aitrepreneur-docker` | **No** | Reproducible containers for image/video generation and LoRA training, rather than a service making repeated text decisions. |
| `frank_fbi` | **Candidate, carefully bounded** | Six-layer email fraud pipeline already combines deterministic headers/URLs, reputation, entity checks, and three LLM assessments. Jev could cheaply add narrow *content signals* or an initial review queue. It cannot replace SPF/DKIM, threat feeds, identity verification, or the explanatory report. Do not use it alone to declare an email safe: the independent 2,000-email phishing test found Jev's direct verdict substantially weaker than Haiku on that dataset. Compare against the existing content rules and signal ensemble on labeled mail. [Phishing study](https://github.com/anisselbd/jev-phishing-bench). |
| `frank_go` | **No** | KataGo and solution trees evaluate board states and tsumego; a text decision model would be a weaker substitute. Arbiter's game demos show that text-state decisions are possible, not that they improve this specialist Go trainer. |
| `frank_investigator` | **Candidate for preliminary labels only** | Source-role classification, claim-type triage, or reranking evidence candidates are closed-set decisions. The product's central task—whether evidence supports a claim, with provenance, counter-evidence, and explanation—is not solved by a typed label or model consensus. Keep source authority and final verdict review anchored in evidence; test any narrow classifier against labeled sources across languages. |
| `frank_karaoke` | **No** | Live audio pitch analysis and signal processing. Jev accepts text, and a remote call is poorly matched to the live scoring loop. |
| `frank_lyrics` | **Unlikely** | The only plausible text judgment is matching a YouTube title to an LRCLIB candidate. Existing title heuristics and duration checks are simpler, local, and low volume. Compare on failed matches before considering a model. |
| `frank_mega` | **No** | File-sharing authorization, quotas, TTL, filename validation, and abuse limits require deterministic enforcement. Semantic classification is not a missing core primitive. |
| `frank_scanlation` | **Unlikely** | Site title, chapter, and page detection uses URL/HTML/image-sequence heuristics, plus MangaDex's API. A text classifier might help a few unfamiliar page layouts, but it cannot inspect image sequences directly; network dependence and repeated site calls would need a demonstrated failure rate to justify them. |
| `frank_sherlock` | **Unlikely** | Large-scale classification sounds promising until the input is examined: the primary input is images, handled by a local vision model, with Surya OCR for text. Jev could classify OCR text into fixed document types *after* extraction, but cannot replace vision, OCR, descriptions, or local-only processing. A small local text classifier is the natural baseline. |
| `frank_type` | **No** | WPM, accuracy, timing, corpus selection, and adaptive speed are exact or simple rule-based calculations. |
| `frank_yomik` | **Unlikely** | Image detection, OCR, translation, and furigana are specialist visual and generative tasks. A post-OCR text router might be possible, but the local-first design and low expected gain argue against a hosted decision call. |
| `frankclaw` | **Best candidate, still conditional** | Its 13-dimension model router and tool/trace review are recurring text decisions. A Jev-like service could supply semantic features for routing or flag a tool trace for human review. The existing router and three-tier approval policy are baselines, and a classifier must never silently upgrade a destructive action to allowed. Measure route quality and downstream task quality; keep hard permission checks in code. |

Seven matching directories have **no top-level README** and were therefore not assessed from a README: `ai-babel`, `aitrepreneur-krea2-docker`, `frank-sherlock-bin`, `frank_bazaar`, `frank_manga`, `frank_oracle`, and `frankmd_zed_extension`. Their absence is not evidence for or against Jev fit.

## A worthwhile pilot, if a bottleneck appears

1. Pick **one** decision: for example FrankClaw `small/large model` routing, ai-memory `relevant/irrelevant memory` ranking, or Frank Investigator `primary/secondary/opinion source` triage. Define the allowed outputs and the action for an uncertain result.
2. Sample real cases across easy, ambiguous, and adversarial inputs; label them independently. For multilingual work, include Portuguese and other actual languages because TypeSafe says English performs best. [Model reference](https://docs.typesafe.ai/models).
3. Compare the existing implementation, a simple rule or local classifier, Jev pinned to a version, and an inexpensive constrained-output LLM. Use the **same input and decision policy** for each.
4. Report confusion matrix, calibration by confidence band, cost per *correctly handled* case, end-to-end latency, review rate, and downstream outcomes. A routing model that is cheap but sends hard work to a weak model may cost more overall.
5. Deploy only as a reversible feature with logging, a conservative review route, and a fallback. Treat safety or authorization judgments as advisory unless an exact policy independently enforces the action.

**Overall:** The pattern is general in the sense that many applications contain semantic routing decisions. In this particular portfolio, those decisions are a **small slice** of the work. Most projects either need specialist image/audio/generative models or already have exact, cheap rules. Clef makes a few image-routing experiments possible and Laya makes local specialization practical, but their most plausible value is still operational efficiency at a repeated decision point, not a broad increase in capability.

## What the expanded benchmark changes

The [sixteen-configuration bilingual comparison](../benchmark/reports/next-wave-comparison-v2/analysis.md)
provides more local candidates, not application-level validation. Jebadiah’s intent
and entailment results make it worth considering for a bounded FrankClaw or
Frank Investigator pilot; English retrieval ties across several models justify
keeping a specialist reranker in the ai-memory comparison. Each compact task cell
has only twelve families. No actual portfolio traffic was evaluated.

For support severity, the [concrete policy-exception case](../benchmark/reports/next-wave-comparison-v1/support-ticket-case-study.md)
shows several high-scoring models downgrading confirmed production data loss for
one customer, despite the supplied rule. Extracting impact facts and applying
exact rules in code is a workflow to evaluate, not a measured improvement here.
The benchmark does not justify replacing authorization, fraud verification, OCR,
translation or source-backed investigation with a model label.
