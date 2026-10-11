# Julia-1: small, fast, weak on these policy cases

Measured 11 October 2026 UTC / 10 October São Paulo. **2,096 new scored requests,
all valid, one attempt each, no truncated inputs.** Two deployments of the same
144.3M checkpoint each completed 504 bilingual classifications and 544 original-suite
requests. The combined comparison now contains **19 v2 configurations (9,576
classifications)** and **17 v1 configurations (9,248 responses)**. Repeated variants
and translations are correlated; these totals are not independent authored problems.

## Business summary

Julia's compact accuracy is **53/168 (31.5%)** on both GPU and CPU, close to the
**31.0% expected uniform-random baseline** for this mixture of three- and four-option
questions. That is a descriptive comparison, not a statistical equivalence claim.
Both deployments are tied at the bottom of this tested set. GPU median/p95 client
latency is **12/25 ms**, the lowest observed pair here; CPU is **71/197 ms** using
four threads. Julia trades very little storage and fast execution for insufficient
accuracy on our difficult cases. It is not supported as an autonomous policy engine
or critical-ticket classifier by these results.

This does not rule out narrower, simpler classification or task-specific training.
Those uses were not measured. A 144.3M model and a 27B model have very different
resource budgets; small size is a useful engineering property, not proof of decision
quality. CPU deployment also avoids reserving a GPU.

## Ranking and cost-benefit

The [complete 19-configuration ranking](ranking.md) includes task/language and
size analyses; [full tables](results.md) retain all conditions.

| Configuration | Compact bilingual | All 504 | Observed v2 median / p95 | Listed USD / 1,000 compact calls |
| --- | ---: | ---: | ---: | ---: |
| Jev | 97.6% | 98.2% | 255 / 304 ms | $0.01916 |
| Clef hosted | 95.8% | 96.4% | 302 / 683 ms | $0.06309 |
| OpenAI Decisions | 90.5% | 93.1% | 222 / 274 ms | $0.02331 |
| Jebadiah 4B v2 local | 90.5% | 86.5% | 205 / 485 ms | Unmeasured local compute |
| Clef-flash hosted | 87.5% | 87.1% | 394 / 804 ms | $0.00999 |
| Julia GPU, native BF16 autocast | 31.5% | 31.3% | 12 / 25 ms | Unmeasured local compute |
| Julia CPU, FP32, four threads | 31.5% | 31.3% | 71 / 197 ms | Unmeasured local compute |

**Quality/price conclusions remain unchanged:** Jev leads measured quality and has
lower compact list cost than Clef and OpenAI. Flash minimizes listed hosted spend.
Jebadiah remains the compact local accuracy leader; local Flash remains stronger on
the original policy suite. Julia is the fastest observed GPU configuration, but its
error rate prevents recommending it as a substitute on these workloads. There is
no defensible single dollar ranking across hosted and local models without electricity,
hardware amortization, utilization, operations and error costs.

No new hosted calls were made for Julia. Its incremental API charge is **$0**;
local compute is unmeasured, not free. Prior hosted responses and pricing are reused
unchanged. See the [dated pricing snapshot](../../pricing/2026-10-11.json) and
[OpenAI usage reconciliation](../openai-comparison-v2/costs.md); the OpenAI addition
cost $0.0347467 including its successful smoke call. Rates are list valuations,
not verified invoices. Latencies come from separate runs, devices and networks.

## English, PT-BR and input conditions

| Deployment | Compact EN | Compact PT-BR | Compact total | Examples | Distractors | All |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Julia GPU | 32/84, 38.1% | 21/84, 25.0% | 53/168 | 48/168 | 57/168 | 158/504 |
| Julia CPU | 32/84, 38.1% | 21/84, 25.0% | 53/168 | 48/168 | 57/168 | 158/504 |

Portuguese loses **13.1 percentage points** on compact inputs in both deployments.
Worked examples do not rescue aggregate performance. Equal totals conceal different
individual predictions. The native GPU and CPU configurations agree on **488/504
v2 choices (96.8%)**, with mean absolute per-option probability difference **0.0141**
and maximum **0.2841**. Their compact accuracy difference is zero, with exploratory
family-bootstrap 95% interval **[−1.8, +1.8] points**. That does not prove equivalence.

GPU compact task scores range from **1/12 Portuguese threshold policies** to **6/12
English intent and current status in either language**. Neither deployment matches
Jev in any of the fourteen compact task/language cells. Cells are small; none supports
claims about all Portuguese or all intent tasks.

A visible failure is Portuguese intent: all twelve compact cases become `cancel`,
including refund, access and other requests. English entailment and Portuguese
threshold cases also show strong preference for particular labels. On the original
suite, all five counterfactual policy pairs fail the both-correct criterion and keep
the same prediction after the relevant policy change. These are failures to follow
the supplied distinctions, not malformed JSON or missing responses.

## Probabilities and original policies

Compact Brier scores are **1.0761 GPU / 1.0737 CPU**, versus **0.0346 Jev** (lower
is better). GPU has **48 errors among 71 predictions with probability ≥0.9**;
CPU has **48 among 75**. A confidence threshold alone is not a safe rescue here.

The [original policy suite](../julia-comparison-v1/results.md) gives:

| Deployment | Original cases | All variants | Originals excluding three disputed families |
| --- | ---: | ---: | ---: |
| GPU | 50/130, 38.5% | 182/520, 35.0% | 49/127, 38.6% |
| CPU | 48/130, 36.9% | 183/520, 35.2% | 47/127, 37.0% |

Both miss all three frozen critical originals, including the two undisputed cases;
one of the three is an existing rubric ambiguity. This is not a production critical
recall estimate. Fair-random-outcome probes also remain poor: choice probability
MAE is **0.2183 GPU / 0.2133 CPU**, and Boolean/Noul MAE **0.2963 / 0.2652**.
Those probes evaluate known uncertainty separately from classification accuracy.

## Resource and size interpretation

Julia is the smallest tested checkpoint at nominal **144.3M parameters**, with
approximately **550.5 MiB FP32 weights**. GPU inference retains FP32 weights and
uses the runtime's native BF16 autocast; CPU uses FP32 with four threads. Container
limits are 40 GiB GPU / 8 GiB CPU; **limits are not measured peak consumption**.
We did not collect a comparable peak RAM/VRAM or energy trace, nor benchmark batching,
throughput, Bend, compilation, or other hardware. Both Julia containers were stopped
after completion, retaining their weights.

The primary size analysis counts Julia GPU once and excludes its CPU duplicate,
just as hosted/local Flash is counted once. Across fifteen known-size configurations,
**Spearman is 0.935**, and **Pearson(log10 size, accuracy) is 0.957**. The earlier
fourteen-configuration Spearman was 0.920. This strengthens the descriptive association
in our selected sample; shared backbones, training, interface and model selection
prevent treating it as a causal scaling law. Jev and OpenAI remain excluded because
verified sizes are unavailable.

## Reproduction and limits

The [protocol and deployment evidence](../../julia/README.md) were committed as
`7ebc8c9` before scored inference. Independent preflight verified pinned image,
weight/tokenizer hashes, actual wrapper bytes, choice/Noul operation and lossless
encoding of all 1,048 inputs on each deployment, including an overflow rejection
control. The runner checks provenance and non-truncation for every scored response.
No prompt, gold label or precision was selected using these results.

Run `benchmark/julia/score.sh`, then `python benchmark/julia/analyze.py` for offline
reproduction. [Paired device diagnostics](device-comparison.json) verify identical
wire-request hashes, complete single-attempt archives and exactly unchanged prior-model
summaries. Device and precision change together; CPU/GPU differences cannot be
attributed to BF16 alone. We have not independently reproduced the publisher's own
benchmark or determined why this checkpoint struggles with our request distribution.

These are AI-authored synthetic stress cases without independent human adjudication.
Narrow task-specific deployment deserves its own labeled evaluation. Perplexity was pending when this report was written. The later
[Perplexity comparison](../perplexity-comparison-v2/analysis.md) contains the current
twenty-configuration ranking. This report preserves the Julia run's dated scope.
