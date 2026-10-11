# Does a larger decision model score better?

## Microsoft update: 11 October 2026

Adding nominal **9B Microsoft Decision-1 at 97.6% compact** gives **n=17**, Spearman
**0.943**, Pearson(log10 size, accuracy) **0.960**, excluding duplicate Flash/Julia
deployments and unknown-size Jev/OpenAI. Microsoft exceeds 27B Clef's 95.8% and
other tested 9B models, while 27B Perplexity remains first at 99.4%.

This is a strong association across selected models, not a causal size rule.
Training, serving, token accounting and task fit remain confounded.
[Recomputed coefficients and ranking](../benchmark/reports/microsoft-comparison-v2/ranking.md).
Earlier sections record prior stages and sample sizes.

## Perplexity update: 11 October 2026

The [twenty-configuration comparison](../benchmark/reports/perplexity-comparison-v2/analysis.md)
adds nominal 27B Perplexity at **99.4% compact**, ahead of the other tested entrants.
Across **sixteen known-size configurations**, after excluding duplicate Flash and
Julia deployments, Spearman is **0.946** and Pearson(log10 size, accuracy) **0.959**.
Jev and OpenAI remain excluded because their verified sizes are unavailable.

The positive association becomes slightly stronger (previous Spearman 0.935), but
this is not a controlled scaling experiment. Perplexity and Clef are both nominal
27B and score differently; 4B Jebadiah exceeds the tested 9B models on compact cases.
Training, architecture, calibration, runtime and task distribution remain confounded.
The new result shows that a larger open model can reach the top of this selected
suite; it does not imply every size increase buys proportional improvement.

Earlier sections below preserve the progression of the evidence.

Checked 10 October 2026. **Our results show a positive association, but do not establish that size alone causes better decisions.** Same-family external results support scaling on unfamiliar tasks while also providing counterexamples on familiar tasks.

**OpenAI follow-up:** the [17-configuration ranking](../benchmark/reports/openai-comparison-v2/ranking.md)
adds a 90.5% compact result for `gpt-6-luna` Decisions, but its verified parameter
count is unavailable in the cited API material. It is excluded from correlations,
like Jev. The expanded known-size Spearman remains **0.920**; this addition provides
no new size-versus-quality evidence at that stage.

**Julia follow-up:** [GPU/CPU testing](../benchmark/reports/julia-comparison-v2/analysis.md)
adds the 144.3M checkpoint at 31.5% compact. Counting its GPU configuration once
and excluding duplicate deployments yields n=15, Spearman **0.935**,
Pearson(log10 size, accuracy) **0.957**. This remains descriptive, not causal.

## Initial six-entrant run: a strong-looking correlation from a very small sample

Use v2 compact cases only: 84 English and 84 matched Portuguese cases per entrant. Count hosted Clef-flash once, rather than treating its local deployment as another independent model. Exclude Jev from the size calculation because we have no verified parameter count.

| Model | Nominal parameters | Correct / 168 | Accuracy |
| --- | ---: | ---: | ---: |
| Laya | 0.421B | 72 | 42.86% |
| Laya typed-decisions | 0.421B | 72 | 42.86% |
| Clef-flash, hosted | 9B | 147 | 87.50% |
| Clef, hosted | 27B | 161 | 95.83% |
| Jev, excluded from correlation | Undisclosed | 164 | 97.62% |

Parameter sizes are nominal published model/backbone sizes, not independently audited exact totals including every head. Sources: [Laya](https://huggingface.co/convaiinnovations/laya), [Clef-flash](https://huggingface.co/Cloudflare/clef-flash), [Clef](https://huggingface.co/Cloudflare/clef). Counts come from [our v2 analysis](../benchmark/reports/comparison-v2/analysis.md).

Across the four known-size rows, **Spearman rank correlation is 1.00** (with tied ranks), and **Pearson correlation between log10(parameters) and accuracy is approximately 0.996**. These are descriptive calculations, not a validated scaling law. There are only **three size levels**, two related Laya checkpoints and two related Clef models. Pooling the two identical Laya rows would leave only three points. No meaningful population significance claim follows from this selected, dependent sample.

Reproduce the descriptive Pearson value with Python's standard library:

```python
from math import log10
from statistics import correlation
sizes_b = [0.421, 0.421, 9, 27]
accuracy = [72 / 168, 72 / 168, 147 / 168, 161 / 168]
print(correlation([log10(n) for n in sizes_b], accuracy))
```

The most useful observed contrast is **Clef 27B versus Flash 9B: +8.33 percentage points** on compact bilingual cases, for three times the nominal parameters. However, their backbones also differ (Qwen3.8 versus Qwen3.5), so this is not a controlled experiment changing only parameter count. Comparing either to Laya additionally changes architecture, training, context handling and language coverage. Parameter count is correlated with those factors in our sample.

## New homelab measurements: the Kev size series

All three pinned Kev 1.0 configurations have now completed both frozen suites.

| Size | Compact English | Compact PT-BR | Combined compact | v1 policy originals |
| --- | ---: | ---: | ---: | ---: |
| 0.8B | 54/84 — 64.3% | 52/84 — 61.9% | 106/168 — 63.1% | 82/130 — 63.1% |
| 4B | 74/84 — 88.1% | 73/84 — 86.9% | 147/168 — 87.5% | 107/130 — 82.3% |
| 9B | 78/84 — 92.9% | 70/84 — 83.3% | 148/168 — 88.1% | 114/130 — 87.7% |

On compact bilingual cases, **4B gains 24.4 percentage points over 0.8B**, with a
family-clustered bootstrap 95% interval of **+16.1 to +33.3 points**. The **9B gain
over 4B is only 0.6 points**, with an interval of **−6.5 to +7.1 points**: these
cases do not establish a reliable improvement at that step. English improved while
Portuguese declined numerically. The v1 policy-original gain is larger, +5.4 points,
but that is another workload and should not be pooled into the bilingual result.

This gives direct evidence of a substantial benefit from 0.8B to 4B on our cases,
and diminishing observed returns on compact inputs thereafter. **The input
condition changes that conclusion:** with worked examples, 9B scores 155/168
(92.3%) versus 4B’s 139/168 (82.7%); with distractors, 137/168 (81.5%) versus
125/168 (74.4%). Across all 504 correlated rows, 9B scores 87.3% versus 4B’s
81.5%. Larger capacity helped more in those conditions; compact-input saturation
does not establish equivalence across workloads. On compact inputs, the multiclass Brier score also improves from **0.215 at 4B**
to **0.158 at 9B** (lower is better), despite the near-tied top-choice accuracy.
That is another reason to evaluate more than the winning label alone. See the [frozen protocol](../benchmark/next-wave/README.md)
and the [raw archives](../benchmark/reports/next-wave-v2/).

## External same-family evidence: Kev

The current [Kev README](https://github.com/jaredpalmer/kev) publishes these results for its versioned family. They are **upstream measurements, not our runs**. The held-out index is chance-corrected and must not be mixed with accuracy percentages or with the live Decision Index's differently composed Full score.

| Kev size | Held-out breadth index | New-source test accuracy | Trained-source test accuracy |
| --- | ---: | ---: | ---: |
| 0.8B | 23.3 | 69.7% | 83.8% |
| 4B | 38.0 | 83.8% | 86.5% |
| 9B | 41.0 | 85.2% | 87.3% |
| 27B | 52.3 | 88.9% | 86.6% |

All four sizes increase monotonically on the breadth index and new-source test accuracy. The gain on new sources is +14.1 points from 0.8B to 4B, +1.4 from 4B to 9B, and +3.7 from 9B to 27B. Benefits therefore vary substantially with the size interval and metric.

**The 27B model does not beat 9B on every task distribution:** trained-source test accuracy falls from 87.3% to 86.6%. The table supplies no uncertainty interval for that difference, so it is an observed reversal, not proof that the smaller model is reliably superior. Even within this family, the 27B backbone is a different generation and post-training state; this is stronger comparative evidence than unrelated models, but still not a pure size ablation.

## Expanded cross-model correlations

The completed expansion gives **Spearman 0.920** and **Pearson(log-size, compact accuracy) 0.948** across fourteen known-size entrants, excluding Jev and duplicate local Flash. Restricting to twelve native SystemOne entrants gives **0.892 / 0.943**. These remain descriptive associations among dependent model families. [Full ranking and intervals](../benchmark/reports/next-wave-comparison-v2/ranking.md), [condition-specific coefficients](../benchmark/reports/next-wave-comparison-v2/size-correlations-by-condition.json).

## What to test next

The pinned **Kev 0.8B / 4B / 9B** comparison is complete. A 27B run remains conditional on capacity. Jebadiah 4B/9B would supply a second size family for a future round; this run contains only Jebadiah 4B. Precision, input representation and runtime policy must remain explicit in any extension.

Report accuracy and paired differences separately by language, task and input condition. Also compare native probability quality, errors and truncation. Across a larger set of entrants, report both Spearman(size, score) and Pearson(log-size, score), with sensitivity to duplicate revisions, family composition and MoE total versus active parameters. Do not treat hundreds of test cases as hundreds of independent model sizes.

Size is a useful predictor of broad capability in the evidence we have. It is not a purchase criterion by itself: select models meeting the application's error requirements, then compare measured memory, latency and total cost. A smaller model that clears that bar can be preferable. See [deployment tradeoffs](model-tradeoffs.md).
