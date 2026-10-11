# Technical and cost-benefit ranking

**Julia update:** the [19-configuration analysis](../benchmark/reports/julia-comparison-v2/analysis.md)
adds GPU and four-thread CPU results. Both score 31.5% compact. GPU median/p95
is 12/25 ms; CPU 71/197 ms. The 144.3M checkpoint is small and fast, but these
policy errors keep the existing quality recommendations unchanged. Local total
cost remains unmeasured.

## OpenAI Decisions: 11 October UTC update

The [17-configuration comparison](../benchmark/reports/openai-comparison-v2/analysis.md)
adds native OpenAI Decisions (`gpt-6-luna`). Compact bilingual accuracy is **90.5%**,
tied with Jebadiah 4B; Jev remains **97.6%**, Clef **95.8%**. OpenAI improves to
**93.1%** across all three input conditions, ahead of the tested local configurations.

| Hosted entrant | Compact accuracy | Listed USD / 1,000 compact calls | Observed median / p95, all v2 |
| --- | ---: | ---: | ---: |
| Jev | 97.6% | $0.01916 | 255 / 304 ms |
| Clef | 95.8% | $0.06309 | 302 / 683 ms |
| OpenAI Decisions | 90.5% | $0.02331 | 222 / 274 ms |
| Clef-flash | 87.5% | $0.00999 | 394 / 804 ms |

Jev retains the best-supported paid quality/price balance on these cases. OpenAI
has the lowest observed hosted latency and fits an existing OpenAI integration,
but its threshold-policy errors require attention. Timing runs are on different
dates, so the latency ordering is descriptive. Flash still minimizes listed API
spend. Cloudflare allowances can change the incremental bill; local total costs
remain unmeasured. See [usage reconciliation](../benchmark/reports/openai-comparison-v2/costs.md).

Earlier sections below preserve their dated scope and figures.

## Expanded local comparison: 10 October update

The [expanded analysis](../benchmark/reports/next-wave-comparison-v2/analysis.md)
adds ten local configurations. Jebadiah 4B v2 leads the tested local compact
bilingual point estimates (90.5%); Mapika Decider and Kev 4B tie Flash’s 87.5%.
Kev 9B helps more with examples/distractors. Local Flash remains ahead of the
added locals on the original policy suite. There is no single local winner across
all these conditions, and the local dollar costs are unmeasured.

The paid-hosted recommendation remains Jev for measured quality and low operations
effort, Flash for the lowest token spend, and full Clef within available free
allowance. This new wave incurred no hosted inference charges. The original
six-model calculations below remain a historical pricing/quality analysis; consult
the expanded report for the current local shortlist and resource tradeoffs.

## Original six-model comparison


Updated **10 October 2026**. The detailed tables below cover **v1's** frozen,
synthetic, explicit-policy text workload, with no fine-tuning. They are not universal
model rankings.

**V2 follow-up:** the [broader English / PT-BR analysis](../benchmark/reports/comparison-v2/analysis.md)
includes a separate technical and cost-benefit table. Jev scored 97.6% compact accuracy
in both languages; Clef 97.6% / 94.0%, hosted Flash 91.7% / 83.3%, and local Flash
89.3% / 85.7%. The same broad paid-cost decision order holds. Compact unit costs are
$0.01916 / 1,000 Jev decisions, $0.00999 Flash, and $0.06309 Clef. Do not combine the
two datasets into an overall accuracy ranking. Hosted/local Flash disagree on 19 v2
labels, so the exact agreement described below is specific to v1.

**Recommendation:** Jev is the strongest paid default when wrong decisions have a
meaningful cost. Clef-flash is now the cheapest hosted option at current list prices.
Full Clef is attractive for small workloads inside Cloudflare's daily free allowance.
Local Clef-flash is the best tested self-hosted option; its financial advantage is
unproven. Neither stock Laya checkpoint delivered acceptable general policy-following
in this test.

## Why the local run finished quickly

The local main archive spans **03:54:34–04:00:40 UTC**, about **6 minutes 6 seconds**.
All 1,632 requests completed: 544 per model, including 520 classifications and 24
probability probes. Models were already downloaded and loaded. Laya predictions took
roughly 36 ms server-side and Clef-flash roughly 593 ms at the median, with sequential
requests. Setup, downloads and cold starts are not included in those six minutes.
Six additional smoke calls were stored separately. See the [archive](../benchmark/reports/homelab-v1/archive.json).

## Technical ranking: classify correctly first

| Technical tier | Entrant | Original / all-variant accuracy | After gold-ambiguity exclusions | Median / p95 observed latency |
| --- | --- | ---: | ---: | ---: |
| 1, effectively tied | Jev hosted | 96.2% / 95.2% | 97.2% | 253 / 303 ms |
| 1, effectively tied | Clef hosted | 94.6% / 95.0% | 97.2% | 606 / 2,076 ms |
| 2 | Clef-flash hosted | 90.8% / 89.0% | 90.6% | 491 / 884 ms |
| 2 | Clef-flash local | 90.8% / 89.0% | 90.6% | 595 / 652 ms |
| 3 | Laya local | 43.8% / 38.5% | 38.6% | 38 / 41 ms |
| 3 | Laya-typed local | 43.8% / 38.5% | 38.6% | 38 / 41 ms |

Jev's small accuracy lead over full Clef is not robust in the original-case paired
comparison; treat them as one classification-quality tier. Local Clef-flash matched
all 520 hosted classification labels. The Laya variants tied in aggregate but differed
on 133 labels. Their speed did not compensate for their failures on the supplied rules.
[Measured comparison and limitations](../benchmark/reports/comparison-v1/analysis.md).

This ordering weights classification quality first. It is not a universal probability
ranking: Jev did best on our Noul uncertainty probes, while Clef and Laya-typed were
better on Choice uncertainty probes. Only twelve examples per primitive were tested.
LAN/AMD and WAN/cloud latency measurements are different deployment observations,
not controlled hardware speed comparisons. The dataset is 130 correlated scenario
families, not 520 independent production cases.

## Price recheck changed the budget ranking

On 9 October our audit recorded Clef-flash at **$0.09/M input tokens**. The official
model page and billing table now both say **$0.038/M**. Its output tokens are explicitly
free. This is a **57.8% reduction in the published rate we observed**; the precise
billing effective time is unconfirmed. [Clef-flash model page](https://developers.cloudflare.com/workers-ai/models/clef-flash/).

Jev remains **$0.042/M**, with free output, and Clef remains **$0.24/M**, also with free
output. [TypeSafe model pricing](https://docs.typesafe.ai/models),
[Clef model pricing](https://developers.cloudflare.com/workers-ai/models/clef/).

The old audit is preserved as a dated observation, not silently rewritten as an
invoice. At current rates, the recorded hosted main-plus-smoke usage would be valued
at **$0.057354690** rather than the previous **$0.065970726**. Actual charges remain
unverified; free allowance, credits and two Jev interrupted attempts still matter.

## Comparable unit economics

For this section, use **only the 520 classification requests per entrant**. Exclude
smoke calls and the 24 probability probes so classification accuracy and cost share
the same denominator. Dollar amounts below use current published rates before free
allowances. They are projections for this exact input mix, not any arbitrary 1,000 tickets.

| Hosted model | Actual input tokens for 520 cases | Correct labels | List value of 520 cases | USD / 1,000 classifications | USD / 1,000 correct labels |
| --- | ---: | ---: | ---: | ---: | ---: |
| Clef-flash | 160,351 | 463 | $0.006093 | **$0.011718** | **$0.013161** |
| Jev | 259,170 | 495 | $0.010885 | $0.020933 | $0.021990 |
| Clef | 160,351 | 494 | $0.038484 | $0.074008 | $0.077903 |

The last column divides spending by observed correct answers. It does **not** include
the damage caused by wrong answers, nor imply that a system can identify which answers
are correct in advance. Jev uses more reported tokens for the same inputs, so comparing
only per-token rates would miss part of the actual workload cost.

At the same length mix, one million classification requests would have list values of
about **$11.72 Clef-flash, $20.93 Jev, $74.01 Clef**. These are linear token-cost
projections; they are not evidence that the services sustain the required throughput.
[Reproducible arithmetic](../benchmark/reports/comparison-v1/classification-costs.json),
[dated rate snapshot](../benchmark/pricing/2026-10-10.json).

## Combined technical/price ranking for paid traffic

Assumption: text classification, free allowance exhausted, and accuracy matters in the
business workflow. This is a decision order, not an arbitrary weighted score.

| Rank | Entrant | Why / when to use |
| --- | --- | --- |
| **1** | **Jev hosted** | Top classification tier, lowest observed hosted median latency, and only about $0.0092 more per 1,000 cases than Flash. Best paid default when errors matter. |
| **2** | **Clef-flash hosted** | Lowest current API price, including cost per observed correct label. Best budget choice when its lower measured accuracy is acceptable. Moves to #1 if API spending is the overriding criterion. |
| **3** | **Clef hosted** | Top classification tier, but about 3.54× Jev's classification-only list cost with no demonstrated quality advantage here. Can move to #1 for cash cost inside the free allowance. |
| Conditional | **Clef-flash local** | Best measured local quality; identical labels to hosted Flash. Choose for local processing/control if required. No measured total cost justifies a dollar rank. |
| Last tier | **Laya / Laya-typed local** | Very low observed latency, but 61.5% wrong across variants. Poor untuned value for these policies; different training or tasks need another evaluation. |

A useful break-even calculation makes the first two ranks explicit. Jev made **32
fewer mistakes** than Flash across 520 cases, for **$0.004791802** extra in current
list-price inference. If each mistake has the same average downstream cost, Jev's
extra spend pays for itself above **$0.000149744 per avoided error**—about **0.015 US
cents**. This is arithmetic on the fixture outcomes, not an estimated business loss.

Full Clef versus Flash needs an average avoided-error cost above **$0.001044868**,
about **0.1045 US cents**, under the same assumptions. Jev versus full Clef has no
comparable financial trade-off demonstrated here: Jev costs less with essentially
tied classification quality. Task-specific error types can still change the choice.

A real decision should use:

`API/compute cost + review cost + false-positive losses + false-negative losses + operations`

The test does not tell us these business losses. A false allow for a destructive tool
and a misrouted routine ticket should not receive the same loss automatically.

## The free allowance changes small-volume choices

Cloudflare grants **10,000 neurons/day**, shared across the account, resetting at
00:00 UTC. The current table lists 21,818 neurons/M input tokens for Clef and 3,455
for Flash; overage is $0.011/1,000 neurons on a paid plan. [Workers AI pricing](https://developers.cloudflare.com/workers-ai/platform/pricing/).

With no competing usage and our average input lengths, the allowance corresponds to
roughly **1,500 Clef classifications/day** or **9,400 Flash classifications/day**.
These are alternative uses of one shared allowance, not two separate free quotas.
Actual capacity varies with input length, and other account workloads consume it.

For a small policy-classification workload fitting the allowance, **full Clef is the
best measured quality per incremental API dollar**, provided its latency is acceptable.
For larger free-volume coverage with tolerable errors, Flash has the advantage.
These statements do not confirm that our own account was billed $0.

## Does the homelab save money?

We cannot establish that from this run. An existing machine may have low incremental
cost, but its power, idle allocation, hardware opportunity cost and maintenance were
not measured. Local Flash accumulated **313.441 seconds of server prediction time**
for 520 classifications. At current hosted Flash prices, replacing those calls saves
only **$0.006093 before allowances**. If they fit the allowance, the hosted API saving
is zero. Local processing may still be valuable for control or data locality.

This does not rule out batching, higher utilization, another runtime or a cheaper
hardware configuration. We tested sequential warm requests on the existing homelab,
not optimized local unit economics. Download/setup work is also excluded from timing.

## Conclusion for your projects

For an actual paid text-decision bottleneck, **start the evaluation with Jev and
Clef-flash**: one prioritizes measured quality for a tiny absolute premium; the other
now has the lowest published workload cost. **Use full Clef within the available free
allowance** when quality matters and latency is acceptable. **Keep local Flash as the
self-hosted candidate**, and require evidence before treating stock Laya as a substitute.

This does not change the earlier project-fit conclusion: no portfolio-wide integration
is justified merely because calls are cheap. Deterministic rules should still handle
known thresholds, and sensitive actions need application-enforced permissions. The
benchmark establishes differences among these models, not a proven benefit over every
existing implementation in your projects.

Reproduce the valuation without inference:

```sh
benchmark/tools/offline.sh /work/tools/value.py
```

## Hardware and specialization qualify this ranking

The quality tiers above describe this untuned workload. Laya’s smaller architecture and much lower measured local latency can matter for constrained deployments. We have not measured CPU speed, peak memory or energy, so neither universal inferiority nor best local cost follows. See [model size and deployment tradeoffs](model-tradeoffs.md) for a separate resource-aware comparison and next-round requirements.
