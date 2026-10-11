# Research and benchmark documentation

Research snapshot: **3 October 2026**. Jev and the open decision-model ecosystem are changing quickly; models, prices, and documented limits may change. The original research sections review public primary sources and published experiments. Subsequent measurements from this repository are linked below.

1. [Business summary](business-summary.md) — the short introduction and decision.
2. [Research and conclusions](research.md) — product mechanics, prior art, claims, and evidence.
3. [Alternatives: Clef, Laya, and the ecosystem](alternatives.md) — architectures, licenses, prices, benchmarks, limitations, and a decision guide.
4. [Annotation of Paulo Câmara's “O aluno que marca a letra A”](paulo-camara-article.md) — editorial assessment, argument map, claim audit, caveats, and evaluation controls derived from the article.
5. [Real use cases and project fit](use-cases.md) — where typed decisions pay off, plus a README-based review of the `ai*` and `frank*` projects in `~/Projects`.

The recommended test, if a real bottleneck appears, is to compare a pinned Jev version with existing code, a small local classifier, and a cheap constrained-output LLM on the **same labeled examples**. Include error costs, review rate, latency, and operational cost. A vendor speed multiple by itself is not a purchase decision.

## Setup and measured benchmarks

[Repository overview](../README.md) explains the goals and evidence layout.
[Setup and reproduction guide](setup.md) covers Docker, hosted credentials, pinned model downloads, and the actual AMD homelab deployment.

The [benchmark implementation](../benchmark/README.md) and [frozen protocol](../benchmark/PROTOCOL.md) cover 13 explicit-policy use cases, 520 classification variants and 24 separate uncertainty probes per model. Workstation RTX 5090 runs remain deferred; AMD homelab runs completed on 10 October. The [first hosted findings](../benchmark/reports/hosted-v1/analysis.md) and [full results](../benchmark/reports/hosted-v1/results.md) are now available.

[Pricing verification and test cost](../benchmark/reports/hosted-v1/pricing.md) (9 October) reconciles both providers’ official rates, archived usage, free allowance and billing uncertainties.

[Hosted versus local comparison](../benchmark/reports/comparison-v1/analysis.md) adds measured Laya, Laya-typed and pinned local Clef-flash results, with [six-model tables](../benchmark/reports/comparison-v1/results.md).

[Technical and cost-benefit ranking](cost-benefit-ranking.md) combines measured quality, current pricing, free allowance scenarios and unmeasured local costs. Pricing rechecked 10 October; Clef-flash is now $0.038/M input tokens.

## Bilingual expansion

The [v2 protocol](../benchmark/expansion-v2/README.md) adds 84 new scenario families in matched English and Brazilian Portuguese, with compact, worked-example, and distractor conditions. It is evaluated separately from v1.

[Completed bilingual analysis and ranking](../benchmark/reports/comparison-v2/analysis.md) and [full task/language tables](../benchmark/reports/comparison-v2/results.md) cover all 3,024 v2 classifications, including truncation and hosted/local disagreements.

## Additional models

[OpenAI Decisions integration](../benchmark/openai-decisions/README.md) records the
native adapter, pricing and execution protocol. After the account was funded,
all 1,048 scored requests completed. See the [17-configuration comparison](../benchmark/reports/openai-comparison-v2/analysis.md),
[ranking](../benchmark/reports/openai-comparison-v2/ranking.md) and
[$0.03475 usage reconciliation](../benchmark/reports/openai-comparison-v2/costs.md).

[Julia GPU/CPU results](../benchmark/reports/julia-comparison-v2/analysis.md) add two
completed deployments: [19-configuration ranking](../benchmark/reports/julia-comparison-v2/ranking.md),
[protocol](../benchmark/julia/README.md), and [availability](julia-availability.md).

[Perplexity Decider 1.1 27B](perplexity-decider-availability.md) has public weights;
installation was requested from the homelab agent and no score is assigned yet.

[Further open-model shortlist and homelab lifecycle](next-models.md) checks current releases, popularity, licenses, external benchmark evidence and priorities for the next round.

[Model size and deployment tradeoffs](model-tradeoffs.md) qualifies the rankings by resource constraints, specialization and measured versus unmeasured efficiency.

[Size versus score analysis](size-vs-quality.md) quantifies the observed association and checks same-family scaling evidence and counterexamples.

[Expanded open-model comparison](../benchmark/reports/next-wave-comparison-v2/analysis.md) adds ten configurations, with [rankings and size analysis](../benchmark/reports/next-wave-comparison-v2/ranking.md). Earlier six-model reports remain historical snapshots.
