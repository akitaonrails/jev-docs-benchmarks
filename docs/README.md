# Jev research

Research snapshot: **3 October 2026**. Jev and the open decision-model ecosystem are changing quickly; models, prices, and documented limits may change. The original research sections review public primary sources and published experiments. Subsequent measurements from this repository are linked below.

1. [Business summary](business-summary.md) — the short introduction and decision.
2. [Research and conclusions](research.md) — product mechanics, prior art, claims, and evidence.
3. [Alternatives: Clef, Laya, and the ecosystem](alternatives.md) — architectures, licenses, prices, benchmarks, limitations, and a decision guide.
4. [Annotation of Paulo Câmara's “O aluno que marca a letra A”](paulo-camara-article.md) — editorial assessment, argument map, claim audit, caveats, and evaluation controls derived from the article.
5. [Real use cases and project fit](use-cases.md) — where typed decisions pay off, plus a README-based review of the `ai*` and `frank*` projects in `~/Projects`.

The recommended test, if a real bottleneck appears, is to compare a pinned Jev version with existing code, a small local classifier, and a cheap constrained-output LLM on the **same labeled examples**. Include error costs, review rate, latency, and operational cost. A vendor speed multiple by itself is not a purchase decision.

## Our hosted benchmark

The [benchmark implementation](../benchmark/README.md) and [frozen protocol](../benchmark/PROTOCOL.md) cover 13 explicit-policy use cases, 520 classification variants and 24 separate uncertainty probes per model. Workstation RTX 5090 runs remain deferred; AMD homelab runs completed on 10 October. The [first hosted findings](../benchmark/reports/hosted-v1/analysis.md) and [full results](../benchmark/reports/hosted-v1/results.md) are now available.

[Pricing verification and test cost](../benchmark/reports/hosted-v1/pricing.md) (9 October) reconciles both providers’ official rates, archived usage, free allowance and billing uncertainties.

[Hosted versus local comparison](../benchmark/reports/comparison-v1/analysis.md) adds measured Laya, Laya-typed and pinned local Clef-flash results, with [six-model tables](../benchmark/reports/comparison-v1/results.md).

[Technical and cost-benefit ranking](cost-benefit-ranking.md) combines measured quality, current pricing, free allowance scenarios and unmeasured local costs. Pricing rechecked 10 October; Clef-flash is now $0.038/M input tokens.
