# Microsoft Decision-1: tied hosted compact quality, lowest measured API cost

11 October 2026. **1,048 new valid responses**, using the same frozen v1 and v2
inputs. The comparison now contains **21 bilingual configurations (10,584 v2
classifications)** and **19 original-policy configurations (10,336 responses)**.
Prior models' metrics are unchanged. [Verification](verification.json),
[protocol](../../microsoft/README.md), [full ranking](ranking.md), [task tables](results.md).

## Technical ranking

Compact inputs are the primary v2 comparison; longer conditions stay separate.
Equal scores are ties, not alphabetical performance differences.

| Entrant | Compact / 168 | English / 84 | PT-BR / 84 | All 504 | Median / p95 |
| --- | ---: | ---: | ---: | ---: | ---: |
| Perplexity Decider 27B, local | 167 (99.4%) | 83 | 84 | 501 | 1,547 / 2,446 ms |
| Jev | 164 (97.6%) | 82 | 82 | 495 | 255 / 304 ms |
| **Microsoft Decision-1** | **164 (97.6%)** | **80** | **84** | **493** | **422 / 551 ms** |
| Clef | 161 (95.8%) | 82 | 79 | 486 | 302 / 683 ms |
| OpenAI Decisions | 152 (90.5%) | 76 | 76 | 469 | 222 / 274 ms |
| Jebadiah 4B v2, local | 152 (90.5%) | 77 | 75 | 436 | 205 / 485 ms |
| Kev 9B, local | 148 (88.1%) | 78 | 70 | 440 | 561 / 883 ms |
| Clef-flash, hosted | 147 (87.5%) | 77 | 70 | 439 | 394 / 804 ms |

Microsoft versus Jev is **0.0 points, family-bootstrap 95% interval [-3.0, +3.0]**.
Microsoft versus Perplexity is -1.8 points [-4.2, 0.0]; versus Clef +1.8
[-0.6, +4.8]. These do not establish general superiority or equivalence. Its larger
observed advantages over OpenAI (+7.1 points) and Flash (+10.1) have exploratory
intervals excluding zero. Intervals cluster paired languages by 84 authored
families and are not corrected for multiple comparisons. [Exact comparisons](paired-family-comparisons.json).

## Language, examples and concrete weaknesses

| Condition | English / 84 | PT-BR / 84 | Combined / 168 |
| --- | ---: | ---: | ---: |
| Compact | 80 | 84 | 164 |
| Worked examples | 82 | 83 | 165 |
| Distractors | 82 | 82 | 164 |

PT-BR compact is four decisions better than English, +4.8 points with paired
95% interval [+1.2, +9.5]. This applies to these translations; it does not prove
Portuguese is generally the model's stronger language. Longer contexts introduce
Portuguese mistakes even though all compact Portuguese cases pass.

All four compact errors occur in English:

- `threshold_policy-07`: for an AND rule, the known false delay condition already
  establishes no escalation. The model unnecessarily requires the missing error rate.
- `threshold_policy-09`: a count of either 3 or 4 cannot establish “above 3”; it escalates.
- `threshold_policy-12`: an interval of 8–12 cannot establish “at least 10”; it escalates.
- `retrieval-11`: notification recipients do not establish who is required to approve;
  it labels the passage partial. With examples and distractors it upgrades this to
  full, still incorrectly, reaching 96.7% probability with distractors.

Microsoft exceeds Jev in three of fourteen compact task/language cells (English
and Portuguese data handling, Portuguese retrieval), ties ten and trails English
threshold policy. Each cell has only twelve authored cases. General semantic tasks
are strong; supplied Boolean logic and unknown measurements still expose failures.

Worked examples improve the aggregate by only one answer. They also introduce a
Portuguese sentiment error with 99.5% probability. Distractors produce a Portuguese
threshold error with 99.4% probability. Added context is not a dependable repair.

## Probabilities and original policy suite

Compact Brier score is **0.03076**. All **160/168 compact predictions at probability
≥0.9 are correct** here, but the longer conditions contain confidently wrong
answers. This observed coverage/error tradeoff is not a production calibration
claim, and a threshold chosen after seeing results needs independent validation.

The v1 known-random-event probes remain weak: choice MAE **0.1253**, Boolean/Noul
MAE **0.3690**. For a fair binary event, a Noul response is 0.867 instead of 0.5.
OpenAI's predicate result remains much stronger on these specific probes. Good
classification probabilities on deterministic fixtures do not establish general
probabilistic reasoning.

V1 scores **124/130 originals**, **496/520 variants**, or **123/127 originals**
after the existing common ambiguity exclusions. All five policy-change pairs pass.
Option reordering and the tested injection preserve all original predictions;
opaque labels change two. See [v1 error analysis](../microsoft-comparison-v1/analysis.md).

## Price and cost-benefit recommendation

| Hosted entrant | Compact accuracy | USD / 1,000 compact calls |
| --- | ---: | ---: |
| **Microsoft Decision-1** | **97.6%** | **$0.00645** |
| Jev | 97.6% | $0.01916 |
| Clef | 95.8% | $0.06309 |
| OpenAI Decisions | 90.5% | $0.02331 |
| Clef-flash | 87.5% | $0.00999 |

**Microsoft becomes the first paid hosted candidate to evaluate for this input
mix**, tying Jev's compact count at about **66% lower reported workload cost** and
costing about **35% less than Flash**. Its nominal price is the same as Jev's
$0.042/M; it reports only 25,789 compact input tokens against Jev's 76,623. The
observed usage difference explains the savings; we cannot infer each vendor's
internal token accounting. This is not a guarantee for arbitrary input lengths.

**Jev is the second candidate when latency or the specific missed policies matter**:
it is faster here, gets two more labels right across all v2 conditions and one
more v1 original. Microsoft and Jev have different errors; a tied aggregate is
not interchangeability. Perplexity remains the best local quality point estimate,
with much higher memory and latency, and no measured dollar cost. Jebadiah remains
a smaller local compromise. Cloudflare's available allowance can make hosted
Clef attractive at zero incremental inference charge. OpenAI retains lower observed
latency and stronger Boolean uncertainty probes. These qualifications prevent a
single universal dollar/quality ranking.

Successful scored usage totals **$0.011132940**; with the separately observed
smoke, **$0.011135376**. All successful usage costs exactly match the published
rate. Ten v2 requests encounter HTTP 429 once and succeed on retry: **514 attempts
for 504 results**, with no final failures. Retry waiting is included in latency.
The archive preserves attempt status/timing, but not separate failed-attempt usage;
any associated charge is unverified. Taxes, credit purchase fees and the full
account bill are not reconciled. [Detailed cost arithmetic](costs.md).

## Model size and limits of the conclusion

Microsoft's nominal Qwen3.5-9B backbone scores above nominal 27B Clef in this
compact sample, and above the other tested 9B models. Size therefore cannot
explain the ordering alone. Across seventeen known-size entrants after removing
duplicate Flash/Julia deployments, Spearman is **0.943** and Pearson(log10 size)
**0.960**. Related models and selected tasks make this descriptive, not causal.
Jev and OpenAI have unknown verified sizes and remain excluded.

The model is hosted through OpenRouter/Azure; no local weights or installation are
part of this run. Returned version is `microsoft/microsoft-decision-1-20261009`.
Hosted identifiers do not pin immutable weights. Responses lack truncation
telemetry. Timings include network/provider routing and are not concurrent matched
hardware tests. Synthetic cases, small task cells, correlated variants and existing
v1 gold ambiguities limit generalization. No measured project workload or deployment
benefit follows solely from these scores.
