# Business summary: should I care about decision models?

Updated 15 October 2026. **No portfolio-wide integration is justified.** Consider
a small experiment where an application repeatedly needs a bounded judgment—such
as ticket routing, retrieval relevance or model selection—and the existing path
has a measurable cost or accuracy problem. FrankClaw routing and ai-memory candidate
ranking remain plausible experiments, not demonstrated bottlenecks. [Project fit](use-cases.md).

These models apply supplied descriptions and rules using knowledge learned during
training. The classification task predates Jev; the useful product proposition is
a convenient typed API with low inference overhead. A valid choice or probability
is not proof of a correct decision. Application code still owns permissions, exact
thresholds and actions. [Mechanics, prior art and hype claims](research.md).

## CUDA deployment update

The RTX 5090 runs the fitting models 1.7×–10.3× faster than the earlier homelab
measurements, with little aggregate accuracy change. Jebadiah reaches 39 ms median
at 90.5% compact accuracy; Kev 9B and Clef Flash are stronger on some other
conditions. The 27B quality leaders cannot fit at reference BF16 precision.
This makes local experimentation quicker, but does not justify broader integration
or establish a financial saving. [Hardware comparison](cuda-rocm-comparison.md).

## What our tests support

| Candidate | Compact bilingual accuracy | Practical interpretation |
| --- | ---: | --- |
| d3 / Perplexity 27B | 99.4% each | Highest observed quality; all 504 v2 labels agree. Large GPU memory requirement. |
| Microsoft Decision-1 | 97.6% | First paid hosted candidate for this input mix: $0.00645/1,000 compact calls. |
| Jev | 97.6% | Faster observed hosted latency than Microsoft; different errors and stronger aggregate v2 count. |
| Jebadiah 4B v2 | 90.5% | A smaller local quality compromise. |
| d3-edge, nominal 0.6B | 60.7% | Small and fast, but substantial difficult-policy errors. |

The local models' dollar cost is unmeasured. Hosted values use the dated 11 October
rates and archived token usage, before allowances and account fees. Cloudflare's
available allowance can change the cash-cost choice. [Current comparison](../benchmark/reports/decision3-comparison-v2/analysis.md),
[cost-benefit detail](cost-benefit-ranking.md).

**Evaluate the whole workflow:** inference cost, review effort, false-positive and
false-negative losses, latency and operations. Start with your own labeled cases
and a deterministic baseline. Synthetic benchmark accuracy, small language/task
cells and probability outputs do not establish production reliability. Our text
suite also does not test Decision 3.0's image/video capabilities.
