# Does a larger decision model score better?

Checked 10 October 2026. **Our results show a positive association, but do not establish that size alone causes better decisions.** Same-family external results support scaling on unfamiliar tasks while also providing counterexamples on familiar tasks.

## Our measurements: a strong-looking correlation from a very small sample

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

## Same-family evidence: Kev

The current [Kev README](https://github.com/jaredpalmer/kev) publishes these results for its versioned family. They are **upstream measurements, not our runs**. The held-out index is chance-corrected and must not be mixed with accuracy percentages or with the live Decision Index's differently composed Full score.

| Kev size | Held-out breadth index | New-source test accuracy | Trained-source test accuracy |
| --- | ---: | ---: | ---: |
| 0.8B | 23.3 | 69.7% | 83.8% |
| 4B | 38.0 | 83.8% | 86.5% |
| 9B | 41.0 | 85.2% | 87.3% |
| 27B | 52.3 | 88.9% | 86.6% |

All four sizes increase monotonically on the breadth index and new-source test accuracy. The gain on new sources is +14.1 points from 0.8B to 4B, +1.4 from 4B to 9B, and +3.7 from 9B to 27B. Benefits therefore vary substantially with the size interval and metric.

**The 27B model does not beat 9B on every task distribution:** trained-source test accuracy falls from 87.3% to 86.6%. The table supplies no uncertainty interval for that difference, so it is an observed reversal, not proof that the smaller model is reliably superior. Even within this family, the 27B backbone is a different generation and post-training state; this is stronger comparative evidence than unrelated models, but still not a pure size ablation.

## What this changes in our next benchmark

Prioritize a pinned **Kev 0.8B / 4B / 9B** comparison on exactly the same frozen cases, with 27B conditional on capacity. Keep precision, input representation and runtime policy as comparable as supported. Add Jebadiah 4B/9B later as a second family, rather than drawing a universal scaling conclusion from Kev alone.

Report accuracy and paired differences separately by language, task and input condition. Also compare native probability quality, errors and truncation. Across a larger set of entrants, report both Spearman(size, score) and Pearson(log-size, score), with sensitivity to duplicate revisions, family composition and MoE total versus active parameters. Do not treat hundreds of test cases as hundreds of independent model sizes.

Size is a useful predictor of broad capability in the evidence we have. It is not a purchase criterion by itself: select models meeting the application's error requirements, then compare measured memory, latency and total cost. A smaller model that clears that bar can be preferable. See [deployment tradeoffs](model-tradeoffs.md).
