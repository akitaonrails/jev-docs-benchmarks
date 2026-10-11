# OpenAI Decisions: quality, latency and cost

Measured **11 October 2026 UTC / 10 October São Paulo**, using native
`POST /v1/decisions` with `gpt-6-luna`. This adds one hosted configuration to the
existing frozen suites. Earlier entrants are reused from their archives.

**1,048/1,048 scored requests were valid, with exactly one attempt each.** The
combined repository now covers **17 v2 configurations (8,568 classifications)**
and **15 v1 configurations (8,160 responses)**. These totals are repeated evaluations
of correlated cases, not independent authored problems. The new listed usage,
including the successful smoke call, is **$0.0347467 (about 3.5 US cents)**.

## Business summary

**OpenAI is competitive, with clear gaps to the quality leaders.** Its compact bilingual accuracy is **90.5%**, tied with local
Jebadiah 4B v2, behind Jev (**97.6%**) and hosted Clef (**95.8%**). The aggregate
tie hides substantial differences: OpenAI performs much better with worked
examples and long distractors than Jebadiah.

OpenAI's observed v2 median/p95 latency is **222/274 ms**, the lowest hosted
pair measured here. Jev measured **255/304 ms**, Clef **302/683 ms**, and hosted
Flash **394/804 ms**. These are client wall times from different dated runs,
including network effects, not a controlled simultaneous latency experiment.
The vendor's “10x faster than Responses” claim is outside our test: we did not
run a matched Responses API baseline.

At measured compact token consumption, OpenAI costs **$0.02331 per 1,000 calls**,
versus **$0.01916 Jev**, **$0.06309 Clef**, and **$0.00999 Flash**, before allowances.
Jev retains the stronger quality/price combination on this suite. OpenAI remains
a candidate for applications already using its API or prioritizing the observed
latency; those reasons still need validation on actual traffic.

## Rankings and input conditions

Primary ranking: **168 compact cases = 84 authored families × two languages**.
The full [17-configuration ranking](ranking.md) includes locals and paired
uncertainty. The [task tables](results.md) show every language/condition cell.

| Configuration | Compact EN | Compact PT-BR | Combined compact | Examples | Distractors | All 504 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Jev | 97.6% | 97.6% | 97.6% | 98.2% | 98.8% | 98.2% |
| Clef | 97.6% | 94.0% | 95.8% | 97.6% | 95.8% | 96.4% |
| **OpenAI Decisions** | **90.5%** | **90.5%** | **90.5%** | **93.5%** | **95.2%** | **93.1%** |
| Jebadiah 4B v2 | 91.7% | 89.3% | 90.5% | 88.1% | 81.0% | 86.5% |
| Kev 9B | 92.9% | 83.3% | 88.1% | 92.3% | 81.5% | 87.3% |
| Hosted Flash | 91.7% | 83.3% | 87.5% | 88.1% | 85.7% | 87.1% |

OpenAI gets **152/168 compact**, **157/168 examples**, and **160/168 distractors**:
**469/504 overall**, the third-highest overall total. The higher distractor score
is an observation on these fixed variants; it does not show that adding unrelated
text generally improves decisions. No prompt was selected using these results.

Against Jev, the compact difference is **−7.1 percentage points**, with a
family-clustered bootstrap 95% interval **[−13.1, −1.2]**. Against Clef it is
**−5.4 points [−11.3, +0.6]**, and against Flash **+3.0 [−5.4, +10.7]**. These are
exploratory intervals, not adjusted for multiple comparisons. English and PT-BR
translations stay together when resampling. An interval crossing zero does not
establish equivalence.

## Strengths, weaknesses and Portuguese

OpenAI ties or exceeds Jev in **9 of 14 compact task/language cells**: three
one-case wins, six ties, five losses. Every cell has only twelve families.

- **Intent, entailment and data handling:** 12/12 in both languages.
- **Retrieval:** 12/12 English, 11/12 Portuguese.
- **Current incident status:** 11/12 English, 12/12 Portuguese.
- **Sentiment:** 9/12 English, 10/12 Portuguese; mixed sentiment is troublesome.
- **Threshold policies:** 8/12 English and 7/12 Portuguese, the clearest weakness.

Equal aggregate EN/PT-BR scores conceal different errors. For example, the exact
boundary “above 3 failures” with exactly three failures should be monitor. OpenAI
chooses unknown in English and escalate in Portuguese. It also treats a range
from 8 to 12 as establishing an “at least 10” rule in both languages; that should
remain unknown.

Another error is Boolean short-circuit reasoning: “error rate >5% AND delay >30s”
is established false when delay is 20s, even if error rate is missing. OpenAI
chooses unknown in both compact languages. This supports the earlier engineering
conclusion: extract facts if necessary, then evaluate exact thresholds and Boolean
rules in ordinary code. That hybrid intervention has not been benchmarked here.

## Probabilities and confidence

Compact multiclass Brier (lower is better): **Jev 0.0346**, **Clef 0.0622**,
**OpenAI 0.1262**, **Jebadiah 0.1669**, **Flash 0.1726**. OpenAI improves the
probability diagnostic over those two nearby alternatives but trails the leaders.

OpenAI has **84/168 compact predictions at probability ≥0.9**, with zero errors
in that subset. This is only 50% coverage on a small synthetic sample, not a
production reliability guarantee. Examples have one error among 94 such
predictions; distractors one among 138. We use the native per-option distribution,
not the separate API `confidence` field, for these calculations.

### Known uncertainty: choice and predicate behave differently

On the twelve fair-random-outcome probes, OpenAI's native predicate probabilities
are **0.50, 0.25 and 0.17**, closely matching the stated 1/2, 1/4 and 1/6 event
probabilities. Mean absolute error is **0.00111**, versus Jev's **0.05778** on its
Noul primitive. The small remaining error is consistent with rounding 1/6 to 0.17.

The choice primitive does not preserve that uncertainty: its average per-option
absolute error is **0.20481**, and it picks the first presented option in **11/12**
probes. For one fair two-outcome case it returns **0.94/0.06**, although the correct
event distribution is 0.50/0.50. Full Clef's choice MAE is lower (**0.07309**).

These are distinct outputs under a frozen mapping, not evidence that a choice
score is always a well-calibrated probability of an external event. The primitive
and wording matter. There is no hidden future outcome to predict in these probes;
we score preservation of known uncertainty separately from classification accuracy.

## Original policy suite

OpenAI gets **121/130 originals (93.1%)** and **483/520 variants (92.9%)**, behind
Jev (125/130, 495/520) and full Clef (123/130, 494/520), ahead of Flash (118/130,
463/520). Excluding the same three previously disputed families gives **120/127
originals (94.5%)** and **482/508 variants (94.9%)**; labels were not changed for
this entrant. Full [15-configuration v1 results](../openai-comparison-v1/results.md)
include every task, uncertainty probe and presentation condition.

All five prespecified counterfactual policy pairs are correct. Presentation is
not completely invariant: reordered, opaque and injected variants each turn two
correct original decisions into errors, even though some other errors improve.

The support-ticket warning persists. On `support_severity-04-original`, confirmed
ongoing production data loss affecting one customer is **critical** under the
supplied rule. OpenAI chooses **degraded**. It correctly classifies the other
undisputed critical original (a multi-customer production outage). There are only
two undisputed critical originals; the third is an existing ambiguity. Neither
“one miss out of two” nor an unqualified three-case rate estimates production risk.

## Pricing and access

The [cost reconciliation](costs.md) and [machine-readable usage](costs.json) separate
scored v1/v2 calls, the successful independent smoke call, and the initial unfunded
probe. The **$20 account deposit is prepaid credit, not benchmark expense**.

OpenAI's [documented Decisions rate](https://developers.openai.com/api/docs/guides/decisions)
is **$0.10/M input tokens**, with no output charge. These short text calls use
the global endpoint; the guide notes different treatment for regional processing
and long context. We value returned usage at that rate; this is not a verified
invoice. Other hosted rates are carried forward from the 10 October audit,
explicitly dated in the [snapshot](../../pricing/2026-10-11.json).

Codex subscription authentication is separate from the Platform API credentials
used here. The initial smoke request returned exhausted API credit; after the
user funded the account, the next independent smoke request succeeded. Neither
smoke request contributes to accuracy.

## Interpretation and limits

- The local shortlist is unchanged: Jebadiah leads compact local accuracy;
  local Flash remains strong on the older suite; smaller models need a task and
  resource-specific assessment. This hosted addition did not retest local devices.
- OpenAI's verified parameter count is unavailable in the cited API material.
  It is excluded from size correlations, like Jev. The previous known-size
  Spearman correlation remains **0.920**; no new scaling evidence was added.
- Native API fields differ from SystemOne. The adapter preserves state, rubric,
  option IDs, descriptions and order; predicate probes retain event descriptions.
  It never sends expected labels or rationales. See the
  [frozen mapping and run commands](../../openai-decisions/README.md).
- The model is the returned `gpt-6-luna` alias, not a pinned immutable weight
  snapshot. The endpoint is in beta; future behavior and performance may change.
- These AI-authored synthetic cases have no independent human adjudication.
  Translations and variants are correlated. The existing v1 disputed-family
  sensitivity analysis still applies. High-stakes error costs are not captured
  by aggregate accuracy alone.

Julia-1 was pending when this OpenAI report was written. Its subsequent
[completed GPU/CPU comparison](../julia-comparison-v2/analysis.md) contains the subsequent
19-configuration ranking. The [Perplexity addition](../perplexity-comparison-v2/analysis.md)
now provides the latest twenty-configuration comparison. This report preserves
the OpenAI run's dated scope.
