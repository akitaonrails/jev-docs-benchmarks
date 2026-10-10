# Expanded open-model comparison: quality, size and deployment cost

Completed **10 October 2026**. Ten additional local configurations produced
**9,392 valid responses**, one attempt per request, with no scored API/schema
failures. Execution ran **13:37:27–14:32:02 UTC**, about 55 minutes. All benchmark
containers were stopped afterward; model weights remain cached. No workstation
GPU or additional hosted inference was used.

The expanded evidence now contains **16 v2 entrants / 8,064 classifications** and
**14 v1 entrants / 7,616 responses**. These are configurations, not independent
architectures: hosted/local Flash share a model family, and several models share
Qwen backbones. The original six entrants are reused from their archived runs.

## Business summary

**The tested open alternatives are useful candidates, but none of the local
configurations matched Jev's broad compact bilingual accuracy.** Jebadiah 4B v2
is the strongest local compact candidate by point estimate. Kev 9B benefits more
from worked examples and retains more quality with distractors than Kev 4B.
Mapika Decider is another competitive 4B candidate. The ordering changes on the
original policy suite, where local Flash remains ahead of the added local models.

**Size helps, with substantial qualifications.** Kev improves greatly from 0.8B
to 4B, then nearly ties on compact inputs at 9B. The larger model helps more on
other input conditions and has a better Brier score. Several nominal 4B models
have materially different results. Model size alone cannot select the best entrant.

**Small encoders offer a different resource tradeoff.** Multilingual Laya is the
fastest observed local configuration, about 19 ms median, but its 36.9% compact
accuracy is inadequate for this broad supplied-rule workload. That result does
not establish its performance on easy traffic, phones, CPUs or a domain-specific
fine-tune. GLiNER's native classification mapping also performs poorly here;
natural-label tasks are a separate evaluation, not covered by this opaque-ID track.

## Technical ranking

The primary metric is accuracy on **168 compact bilingual cases**, representing
84 authored families with paired translations. Numerical ranks are descriptive;
nearby scores are not automatically statistically distinguishable.

| Configuration | Compact EN / PT-BR | Combined compact | Observed median, all v2 inputs | Interpretation |
| --- | ---: | ---: | ---: | --- |
| Jev | 97.6% / 97.6% | 97.6% | 255 ms, WAN | Highest point estimate; strong across all three conditions. |
| Hosted Clef | 97.6% / 94.0% | 95.8% | 302 ms, WAN | Same leading quality group; its gap to Jev has an interval crossing zero. |
| Jebadiah 4B v2 | 91.7% / 89.3% | 90.5% | 205 ms, LAN | Highest local compact point estimate; loses ground with distractors. |
| Kev 9B | 92.9% / 83.3% | 88.1% | 561 ms, LAN | Stronger with examples; substantial compact Portuguese decline. |
| Hosted/local Flash | 91.7% / 83.3%; 89.3% / 85.7% | 87.5% each | 394 / 618 ms | Still strong on v1; equal totals conceal different answers. |
| Mapika Decider 4B | 89.3% / 85.7% | 87.5% | 186 ms, LAN | Competitive 4B quality/latency candidate. |
| Kev 4B | 88.1% / 86.9% | 87.5% | 246 ms, LAN | Near 9B on compact inputs; weaker with examples and distractors. |
| Eikos 4B | 85.7% / 79.8% | 82.7% | 235 ms, LAN | Better relative showing on v1 than on the bilingual suite. |
| Simple-Jev / stock Qwen 4B | 77.4% / 71.4% | 74.4% | 1,349 ms, LAN | Useful baseline; this fixed prompt/readout configuration trails the stronger decision fine-tunes on v2. |
| Kev 0.8B | 64.3% / 61.9% | 63.1% | 86 ms, LAN | Better accuracy than tested compact encoders, with more parameters. |
| GLiNER2.5 Decide English | 54.8% / 50.0% | 52.4% | 208 ms, LAN | Native mapping track; scores do not support broad rule-following substitution. |
| Laya / Laya-typed | 44.0% / 41.7%; 50.0% / 35.7% | 42.9% each | 41 / 43 ms, LAN | Fast; weak in these untuned supplied-policy cases. |
| Laya multilingual | 35.7% / 38.1% | 36.9% | 19 ms, LAN | Fastest observed; multilingual weights did not rescue this workload. |
| GLiNER2.5 Decide multilingual | 32.1% / 35.7% | 33.9% | 63 ms, LAN | Smallest nominal entrant, near the 30.95% uniform baseline here. |

See the [full ranking and paired intervals](ranking.md),
[task/language/condition tables](results.md), and [v1 policy results](../next-wave-comparison-v1/results.md).
LAN/WAN timings and different runtimes are not hardware-normalized speed comparisons.

Jebadiah trails Jev by **7.1 points** on combined compact cases, with a
family-clustered bootstrap 95% interval of **−12.5 to −2.4 points**. Clef trails
by 1.8 points, with **−5.4 to +1.2**. These are exploratory intervals on synthetic
families, not production guarantees or multiple-comparison-adjusted claims.
Clef is itself open weights; hosted versus local is not the same distinction as
closed versus open models. Full local Clef was not run in this wave.

## Where local models match or beat the hosted reference

- **Kev 9B gets 12/12 on English data handling versus Jev's 11/12.** It also ties
  Jev on English sentiment and current status. This is a one-case advantage in one
  small task cell, not evidence of general superiority.
- **Jebadiah ties Jev in six of the fourteen compact task/language cells**, including
  English intent, entailment and current status, and Portuguese intent. Its weakest
  compact task is threshold policy, 9/12 in each language.
- **Mapika ties Jev in five cells**, including sentiment in both languages and
  English intent/current status. Entailment, data handling and thresholds remain
  weaker areas in this sample.
- **Eikos ties English intent and retrieval**, but its EN/PT training does not
  establish broad bilingual parity: Portuguese thresholds score 7/12.
- **Simple-Jev ties Jebadiah on v1 originals, 111/130 each**, despite its much lower
  v2 compact result. It also handles the two undisputed critical-ticket originals,
  which several higher-average models miss. Those two cases cannot establish a
  reliable critical-ticket error rate.

The [support-ticket case study](../next-wave-comparison-v1/support-ticket-case-study.md)
shows the concrete policy exception: ongoing production data loss is critical even
when only one customer is affected. Several models choose degraded. This directly
answers why a supplied severity rubric still needs application-specific evaluation.

## Does larger mean better?

Among **14 known-size entrants**, excluding Jev and the duplicate local Flash
deployment, compact accuracy has **Spearman 0.920** with nominal size and
**Pearson 0.948** with log10(size). Excluding the two GLiNER mappings gives
**0.892 / 0.943** across twelve native SystemOne entrants. The association remains
positive across example and distractor conditions; the machine-readable
[condition-specific correlations](size-correlations-by-condition.json) preserve them.

This is a selected, dependent sample, not a causal scaling law. Architecture,
training, language coverage, context and runtime differ alongside parameter count.
Jev's size remains unverified. Nominal parameter labels are not exact served tensor
counts, FLOPs, memory measurements or active-MoE sizes.

The more useful same-family result is:

| Kev size | Compact | Worked examples | Distractors | v1 policy originals |
| --- | ---: | ---: | ---: | ---: |
| 0.8B | 63.1% | 60.7% | 51.8% | 63.1% |
| 4B | 87.5% | 82.7% | 74.4% | 82.3% |
| 9B | 88.1% | 92.3% | 81.5% | 87.7% |

The compact gain from 0.8B to 4B is **+24.4 points** (family bootstrap
**+16.1 to +33.3**). The 4B→9B gain is **+0.6 points** (**−6.5 to +7.1**), while
the gains with examples and distractors are +9.5 and +7.1 points. Compact Brier
also improves from **0.215 to 0.158** at the larger size. English improves while
compact Portuguese declines, so the aggregate alone hides useful differences.

See the [size analysis](../../../docs/size-vs-quality.md) for the earlier sample
and external same-family evidence. We did not run 27B Kev, PPLX or Rune, or establish
whether further scaling would justify the memory and operational requirements.

## Small models and project differences

Laya multilingual's measured speed is a real advantage on this GPU. Its checkpoint
is nominally 322M parameters; the GLiNER models are 340M/287M, versus multi-billion
parameter backbones for the stronger local models. Sources and license distinctions
are in the [verified shortlist](../../../docs/next-models.md).

However, a deployment advantage is useful only when the application accepts the
error profile. Laya multilingual scored 38.1% on compact Portuguese versus base English
Laya’s 41.7%; multilingual GLiNER scored 35.7% versus the English model’s 50.0%. Laya multilingual reported **zero
truncations across all 504 cases**; that rules out its reported context truncation
as an explanation for these particular weak results. Other new native runtimes
do not provide the same truncation telemetry; zero reported events there means
unknown, not proven absence.

GLiNER receives `text=state`, label descriptions and the rubric as its native task
prompt. Inspection of the installed SDK confirms those options are retained in the
classification schema. Its opaque-label stress result is not a measurement of its
best natural-label classifier configuration. We did not fine-tune any model on our
cases or benchmark CPU, phone, energy, high-concurrency or easy-traffic performance.

Peak PyTorch device allocations captured in the new encoder responses were
**1,653 MiB Laya multilingual, 2,348 MiB English GLiNER, and 1,466 MiB multilingual
GLiNER**. These are allocator peaks, not complete resident-memory or CPU needs.
There is no comparable measured series for all entrants.

The [resource tradeoff analysis](../../../docs/model-tradeoffs.md) therefore remains
essential: poor accuracy on broad supplied rules is a measured weakness; small-device suitability
and domain-specialized performance require their own measurements.

## Pricing and cost-benefit recommendation

Prices were rechecked on 10 October: [Jev $0.042/M input tokens](https://docs.typesafe.ai/models),
[Clef $0.24/M](https://developers.cloudflare.com/workers-ai/models/clef/), and
[Flash $0.038/M](https://developers.cloudflare.com/workers-ai/models/clef-flash/).
Outputs are free for these hosted services. Token counts differ by provider.

For the compact bilingual inputs actually measured, listed usage per 1,000
classifications is approximately **$0.01916 Jev, $0.06309 Clef, $0.00999 Flash**,
before allowances. The previous 504-case hosted v2 run totals **$0.072358812** at
these rates. This new local wave adds **$0 in hosted inference charges**; its
electricity, hardware allocation and maintenance cost were not measured. Do not
interpret that as a $0 total operating cost or a confirmed account invoice.

| Requirement | Best-supported shortlist from this experiment |
| --- | --- |
| Paid hosted quality with low operating effort | Jev remains the preferred starting point: highest accuracy point estimate and much lower list cost than full Clef. |
| Lowest hosted token spend | Flash, if the observed error profile is acceptable. |
| Quality within available Cloudflare free allowance | Full Clef; the shared daily allowance and other account usage determine the incremental bill. |
| Local compact bilingual decisions | Jebadiah 4B v2 first by accuracy point estimate; include Mapika Decider and Kev 4B as alternatives. |
| Local richer prompts / worked examples | Kev 9B earns a place despite its larger footprint; its compact Portuguese weakness still matters. |
| Original policy suite | Local Flash remains ahead of the newly added locals on both originals and all variants. |
| Tight parameter/latency budget | Evaluate compact encoders or Kev 0.8B on the actual narrow task; none meets the broad quality level of the leaders here. |

There is **no defensible complete dollar ranking of local models** from these data.
Select configurations meeting the application's quality and memory requirements,
then measure total local operating cost. The fastest classifier or smallest weights
can be a poor bargain if they add review work or misroute costly cases.

## Reproduction and limits

The protocol and adapters were frozen at local commit **`37cb19d` before scored
inference**. Later changes add reporting and documentation; the scored request
mapping is unchanged. [Protocol](../../next-wave/README.md),
[runtime evidence](../next-wave-runtime/README.md),
[interpretation rules](../next-wave-runtime/methodology.md),
[setup guide](../../../docs/setup.md).

```sh
# Offline: validate archive/request hashes and regenerate both comparisons.
sh benchmark/next-wave/score.sh
```

The cases are AI-authored, synthetic, intentionally difficult and not independently
human-adjudicated. The same v1 errata sensitivity applies to every entrant. There
are 84 paired v2 families and 130 v1 families, not 15,680 independent problems.
Results do not establish real customer-ticket accuracy, a production confidence
threshold, optimal prompting, or a benefit over existing deterministic rules and
specialist classifiers in the user's projects. [Portfolio fit](../../../docs/use-cases.md).
