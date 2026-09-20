# Real use cases and fit in my projects

Research snapshot: **20 September 2026**. Project assessments are based on the top-level READMEs present in `~/Projects` on this date, not code review, traffic measurements, or local Jev experiments. “Candidate” means a bounded experiment could be justified if the current path is demonstrably slow, expensive, or inaccurate. It is not a recommendation to integrate immediately.

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
| [ai-jail](</home/akitaonrails/Projects/ai-jail/README.md>) | **No** | OS sandbox and capability policy. A probabilistic command label must not grant filesystem, network, credential, or Docker access. At most, an optional advisory prompt outside enforcement; no evident benefit to the core product. |
| [ai-memory](</home/akitaonrails/Projects/ai-memory/README.md>) | **Candidate, low priority** | It already offers zero-LLM capture, FTS/entity/vector retrieval and optional LLM consolidation. A decision model could rerank a *small shortlist* of memories for a query or flag an observation for consolidation, but it cannot write the wiki page. Test only if current retrieval misses relevant memories and compare with existing hybrid ranking and a local reranker. Hosted calls also change its zero-LLM/local ownership story. |
| [ai-memory-web](</home/akitaonrails/Projects/ai-memory-web/README.md>) | **No** | Static marketing site with deterministic release, i18n, and accessibility checks. No recurring semantic decision in the runtime. |
| [ai-usagebar](</home/akitaonrails/Projects/ai-usagebar/README.md>) | **No** | Reads quota and status APIs, caches and presents numbers. Provider-specific parsing and exact arithmetic belong in code. |
| [aitrepreneur-docker](</home/akitaonrails/Projects/aitrepreneur-docker/README.md>) | **No** | Reproducible containers for image/video generation and LoRA training, rather than a service making repeated text decisions. |
| [frank_fbi](</home/akitaonrails/Projects/frank_fbi/README.md>) | **Candidate, carefully bounded** | Six-layer email fraud pipeline already combines deterministic headers/URLs, reputation, entity checks, and three LLM assessments. Jev could cheaply add narrow *content signals* or an initial review queue. It cannot replace SPF/DKIM, threat feeds, identity verification, or the explanatory report. Do not use it alone to declare an email safe: the independent 2,000-email phishing test found Jev's direct verdict substantially weaker than Haiku on that dataset. Compare against the existing content rules and signal ensemble on labeled mail. [Phishing study](https://github.com/anisselbd/jev-phishing-bench). |
| [frank_go](</home/akitaonrails/Projects/frank_go/README.md>) | **No** | KataGo and solution trees evaluate board states and tsumego; a text decision model would be a weaker substitute. Arbiter's game demos show that text-state decisions are possible, not that they improve this specialist Go trainer. |
| [frank_investigator](</home/akitaonrails/Projects/frank_investigator/README.md>) | **Candidate for preliminary labels only** | Source-role classification, claim-type triage, or reranking evidence candidates are closed-set decisions. The product's central task—whether evidence supports a claim, with provenance, counter-evidence, and explanation—is not solved by a typed label or model consensus. Keep source authority and final verdict review anchored in evidence; test any narrow classifier against labeled sources across languages. |
| [frank_karaoke](</home/akitaonrails/Projects/frank_karaoke/README.md>) | **No** | Live audio pitch analysis and signal processing. Jev accepts text, and a remote call is poorly matched to the live scoring loop. |
| [frank_lyrics](</home/akitaonrails/Projects/frank_lyrics/README.md>) | **Unlikely** | The only plausible text judgment is matching a YouTube title to an LRCLIB candidate. Existing title heuristics and duration checks are simpler, local, and low volume. Compare on failed matches before considering a model. |
| [frank_mega](</home/akitaonrails/Projects/frank_mega/README.md>) | **No** | File-sharing authorization, quotas, TTL, filename validation, and abuse limits require deterministic enforcement. Semantic classification is not a missing core primitive. |
| [frank_scanlation](</home/akitaonrails/Projects/frank_scanlation/README.md>) | **Unlikely** | Site title, chapter, and page detection uses URL/HTML/image-sequence heuristics, plus MangaDex's API. A text classifier might help a few unfamiliar page layouts, but it cannot inspect image sequences directly; network dependence and repeated site calls would need a demonstrated failure rate to justify them. |
| [frank_sherlock](</home/akitaonrails/Projects/frank_sherlock/README.md>) | **Unlikely** | Large-scale classification sounds promising until the input is examined: the primary input is images, handled by a local vision model, with Surya OCR for text. Jev could classify OCR text into fixed document types *after* extraction, but cannot replace vision, OCR, descriptions, or local-only processing. A small local text classifier is the natural baseline. |
| [frank_type](</home/akitaonrails/Projects/frank_type/README.md>) | **No** | WPM, accuracy, timing, corpus selection, and adaptive speed are exact or simple rule-based calculations. |
| [frank_yomik](</home/akitaonrails/Projects/frank_yomik/README.md>) | **Unlikely** | Image detection, OCR, translation, and furigana are specialist visual and generative tasks. A post-OCR text router might be possible, but the local-first design and low expected gain argue against a hosted decision call. |
| [frankclaw](</home/akitaonrails/Projects/frankclaw/README.md>) | **Best candidate, still conditional** | Its 13-dimension model router and tool/trace review are recurring text decisions. A Jev-like service could supply semantic features for routing or flag a tool trace for human review. The existing router and three-tier approval policy are baselines, and a classifier must never silently upgrade a destructive action to allowed. Measure route quality and downstream task quality; keep hard permission checks in code. |

Seven matching directories have **no top-level README** and were therefore not assessed from a README: `ai-babel`, `aitrepreneur-krea2-docker`, `frank-sherlock-bin`, `frank_bazaar`, `frank_manga`, `frank_oracle`, and `frankmd_zed_extension`. Their absence is not evidence for or against Jev fit.

## A worthwhile pilot, if a bottleneck appears

1. Pick **one** decision: for example FrankClaw `small/large model` routing, ai-memory `relevant/irrelevant memory` ranking, or Frank Investigator `primary/secondary/opinion source` triage. Define the allowed outputs and the action for an uncertain result.
2. Sample real cases across easy, ambiguous, and adversarial inputs; label them independently. For multilingual work, include Portuguese and other actual languages because TypeSafe says English performs best. [Model reference](https://docs.typesafe.ai/models).
3. Compare the existing implementation, a simple rule or local classifier, Jev pinned to a version, and an inexpensive constrained-output LLM. Use the **same input and decision policy** for each.
4. Report confusion matrix, calibration by confidence band, cost per *correctly handled* case, end-to-end latency, review rate, and downstream outcomes. A routing model that is cheap but sends hard work to a weak model may cost more overall.
5. Deploy only as a reversible feature with logging, a conservative review route, and a fallback. Treat safety or authorization judgments as advisory unless an exact policy independently enforces the action.

**Overall:** The pattern is general in the sense that many applications contain semantic routing decisions. In this particular portfolio, those decisions are a **small slice** of the work. Most projects either need specialist image/audio/generative models or already have exact, cheap rules. Jev's most plausible value is operational efficiency at a repeated decision point, not a broad increase in capability.
