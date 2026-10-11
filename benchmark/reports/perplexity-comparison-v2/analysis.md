# Perplexity Decider 1.1 27B: quality leader on the bilingual suite

Measured 11 October 2026 on the AMD gfx1151 homelab, using pinned BF16 weights and
the release's native SystemOne API. This is the Perplexity checkpoint, separate
from the previously tested Mapika `decider-4b`.

**1,048/1,048 scored responses were valid, one attempt each.** The comparison now
contains **20 v2 configurations (10,080 classifications)** and **18 v1 configurations
(9,792 responses)**. These are repeated evaluations of correlated cases, not
independent authored problems. The container is stopped and weights are retained.

## Business summary

**An open-weight model now has the highest measured bilingual accuracy in this
comparison.** Perplexity gets **167/168 compact cases (99.4%)**, versus Jev's
164/168 (97.6%) and hosted Clef's 161/168 (95.8%). It gets **501/504 overall**,
with the same English retrieval error across all three conditions and no PT-BR
errors. The lead over Jev is only three compact decisions; it is not proof of
superiority on unseen production traffic.

The resource tradeoff is substantial: **1,547/2,446 ms observed median/p95**,
approximately **49 GiB of BF16 weights** and additional runtime memory. This deployment
uses ROCm fallback kernels and a custom weight loader, so these timings do not
establish optimal speed on NVIDIA or another serving stack. Julia remains much
smaller and faster; its accuracy on these cases is far lower.

For private local policy classification with sufficient hardware, Perplexity is
now a strong candidate. For inexpensive hosted deployment, Jev retains the strongest
measured quality/list-price combination among the APIs tested. Local ownership,
latency, hardware contention and operations change that choice. A zero API fee
does not make local compute free.

## Rankings and input conditions

[Full twenty-configuration ranking](ranking.md) · [complete task/language tables](results.md).
Adjacent ordering is descriptive; use the paired intervals below.

| Configuration | Compact bilingual | All 504 | Observed median / p95 | Listed USD / 1,000 compact calls |
| --- | ---: | ---: | ---: | ---: |
| **Perplexity 27B local** | **99.4%** | **99.4%** | **1,547 / 2,446 ms** | Unmeasured local compute |
| Jev hosted | 97.6% | 98.2% | 255 / 304 ms | $0.01916 |
| Clef hosted | 95.8% | 96.4% | 302 / 683 ms | $0.06309 |
| OpenAI Decisions | 90.5% | 93.1% | 222 / 274 ms | $0.02331 |
| Jebadiah 4B v2 local | 90.5% | 86.5% | 205 / 485 ms | Unmeasured local compute |
| Kev 9B local | 88.1% | 87.3% | 561 / 883 ms | Unmeasured local compute |
| Clef-flash hosted | 87.5% | 87.1% | 394 / 804 ms | $0.00999 |
| Julia GPU | 31.5% | 31.3% | 12 / 25 ms | Unmeasured local compute |

Perplexity scores **83/84 English and 84/84 PT-BR in each condition**: compact,
worked examples and distractors. Portuguese exceeds English by one case, not a
basis for claiming Portuguese is generally stronger. The paired language-bootstrap
interval is **[0.0, +3.6] points** around the observed +1.2 points.

Across fourteen compact task/language cells, Perplexity exceeds Jev in **three**,
ties **eleven**, and loses **none**. The wins are English data handling, Portuguese
data handling and Portuguese retrieval, one case in each. Each cell has only twelve
families. Both models get all compact threshold-policy cases right. Perplexity's
success with missing values and exact boundaries here does not make deterministic
code unnecessary when rules can be implemented directly.

## The remaining retrieval error

All three misses are `retrieval-11-en-*`: the question asks which role is required
to approve; the passage says an approval notification is sent to managers. The
frozen rubric requires explicit support. A notification recipient does not establish
who must approve. Perplexity chooses **full answer** rather than **none**, with
probability **0.660 compact**, **0.660 examples**, and **0.724 distractors**. It
handles the Portuguese counterpart correctly.

The case illustrates an application boundary: routing a notification, authorizing
an action and identifying the required approver are distinct facts. A model can
supply a plausible association without the evidence required by the policy.

## Confidence and uncertainty

Compact multiclass Brier is **0.0124**, lower than Jev **0.0346**, Clef **0.0622**
and OpenAI **0.1262** on these cases. **161/168 compact predictions have probability
≥0.9, with zero errors in that subset**. That is 95.8% observed coverage on a small
synthetic suite, not a validated production confidence threshold. The known wrong
retrieval answer falls below 0.9. We did not tune a threshold or prompt to these results.

### Classification confidence is not general event probability

On twelve probes with explicitly known uniform-random probabilities, Perplexity's
**choice MAE is 0.1140** and **Boolean/Noul MAE is 0.3754**. The latter is a clear
weakness despite excellent classification accuracy. It returns **0.729** for an
event specified to have probability **1/4**, and **0.764** for one specified as
**1/6**. Neither event has been observed; there is no hidden outcome to predict.

| Model | Choice distribution MAE | Boolean/predicate MAE |
| --- | ---: | ---: |
| Perplexity 27B | 0.1140 | 0.3754 |
| Jev | 0.2629 | 0.0578 |
| Clef | 0.0731 | 0.3779 |
| OpenAI Decisions | 0.2048 | 0.0011 |
| Jebadiah 4B v2 | 0.1916 | 0.5634 |

Lower is better. OpenAI uses its native predicate primitive under the frozen
mapping. These small diagnostics do not establish calibration on production
traffic. They do show that a ranking by hard-label accuracy does not rank every
probability use case. Compute explicitly specified random-event probabilities in
ordinary code instead of substituting classifier confidence.

## Original policy suite

[All eighteen configurations](../perplexity-comparison-v1/results.md).

| Configuration | Originals / 130 | All variants / 520 |
| --- | ---: | ---: |
| **Perplexity 27B** | **129, 99.2%** | **516, 99.2%** |
| Jev | 125, 96.2% | 495, 95.2% |
| Clef | 123, 94.6% | 494, 95.0% |
| OpenAI Decisions | 121, 93.1% | 483, 92.9% |
| Jebadiah 4B v2 | 111, 85.4% | 436, 83.8% |

Perplexity changes its answer correctly in **all five policy-counterfactual pairs**.
It preserves the same semantic choice in every reordered, opaque-label and injected
variant: **130/130 agreement in each variant**, with no correct-to-wrong changes.
That is resistance to these fixed presentation attacks, not general prompt-injection
immunity. Observed v1 median/p95 latency is **1,297/1,793 ms**.

Its four scored errors are one family, `support_severity-07`, across four variants.
The record says production recovered except two tenants cannot export invoices.
The frozen gold is critical; Perplexity selects degraded. This family was flagged
as ambiguous in the existing errata before this run: the rubric does not resolve
whether this feature failure constitutes a multi-customer outage. Degraded is a
defensible reading. **No gold label was changed for Perplexity.**

Excluding the same three pre-existing disputed families for every model gives
Perplexity **127/127 originals and 508/508 variants**. The exclusions were identified
after the earliest benchmark inference, not preregistered at the project's beginning.
The frozen primary score remains 99.2%. Both undisputed critical originals—ongoing
production data loss and a multi-customer production outage—are classified correctly.
Two cases cannot establish production critical-ticket recall.

## Paired differences

Compact comparisons resample the **84 authored families**, keeping EN/PT-BR together:

| Perplexity minus | Difference | Family-bootstrap 95% interval |
| --- | ---: | ---: |
| Jev | +1.8 points | [0.0, +4.2] |
| Clef | +3.6 points | [+0.6, +7.1] |
| OpenAI Decisions | +8.9 points | [+3.6, +14.9] |
| Jebadiah 4B v2 | +8.9 points | [+4.2, +14.3] |

Intervals are exploratory and unadjusted for multiple comparisons. The Jev interval
includes zero, so its small observed deficit is not a settled general quality gap.
The larger measured gaps to OpenAI and Jebadiah are clearer on this suite. See the
[machine-readable comparisons](paired-family-comparisons.json).


## Cost, memory and deployment

The [pricing recheck](../../perplexity/pricing-recheck.md) confirms unchanged official
rates on 11 October: Jev $0.042/M input tokens, Clef $0.240/M, Flash $0.038/M and
OpenAI Decisions $0.100/M. Outputs have no listed fee for these tested endpoints.
The per-1,000 figures above use each provider's actual compact input usage; different
tokenizers and input envelopes make raw per-token rates insufficient. Free allowances
can change Cloudflare's incremental bill. These are list valuations, not invoices.

This addition makes **no hosted calls**. Perplexity's local API charge is **$0**,
while electricity, amortization, utilization and operations remain unmeasured. We
have not tested a hosted Perplexity service or priced one by analogy to this checkpoint.
[Snapshot](../../pricing/2026-10-11-perplexity.json).

A [point sample during scoring](../perplexity-runtime/scored-memory-sample.json)
recorded **20.95 GiB Docker memory usage** under a 24 GiB cap and **55.43 GiB total
system VRAM usage**. These are different counters; neither is an isolated model
peak. The GPU baseline before preflight was approximately 3.45 GiB; the native
health endpoint reports **48.63 GiB allocated by PyTorch** after v2. No energy,
saturation-throughput or concurrent-serving benchmark was performed.

The deployment preserves BF16, last-token pooling, the native noncausal full-attention
configuration and temperature **1.0087417621345625 applied once**. It uses Torch
2.9.1 ROCm rather than the release's CUDA Torch 2.14.0; Transformers remains 5.17.0.
Reference PyTorch linear-attention/convolution paths replace optional optimized
kernels. A strict loader copies all checkpoint tensors directly to GPU because the
standard loader exceeded the container's host-memory cap. We reviewed these changes
but did not run a paired CUDA/reference-loader equivalence experiment.

## Size versus quality

Adding Perplexity strengthens the descriptive association: across **sixteen
known-size configurations**, Spearman is **0.946** and Pearson(log10 size, accuracy)
**0.959**, compared with 0.935 / 0.957 before this addition. Count hosted/local Flash
once and Julia GPU/CPU once; exclude Jev and OpenAI, whose sizes are unverified.
Nominal sizes are labels, not exact tensor-count audits.

This is not a causal scaling law. Perplexity and Clef share a nominal 27B size but
differ in score, while Jebadiah 4B beats the tested 9B configurations on compact
cases. Families share backbones; training, precision, calibration and interface
also differ. See [full correlations](size-correlations.json) and the
[broader size analysis](../../../docs/size-vs-quality.md).

## Reproducibility and interpretation

The [protocol](../../perplexity/README.md) was committed as **`0d9c848` before scored
inference**. All 46 manifest files passed independent checksum verification. Both
native primitives passed smoke checks. All 1,048 requests encoded without dropping
input, within **141–723 tokens**, and the oversized-input negative control returned
HTTP 422. Image and command are pinned; health checks verify configuration before
and after each suite. Each successful scored token count must match the complete
preflight encoding for the exact request hash.

The native API has no truncation flag or per-response revision. Revision evidence
is in the pinned registry and before/after health sidecars. Raw records retain
that absence; the common
report counts missing flag telemetry. Losslessness is established by the separate
encoding evidence and pinned rejection behavior, not by inventing a response field.

The suites are AI-authored synthetic cases without independent human adjudication.
Translations and variants are correlated. The near-ceiling result means this v2
suite has limited ability to distinguish the strongest models. A useful next step
would be a separately frozen, human-reviewed holdout using actual application
policies and messier evidence. Our tests do not cover images, audio, long inputs near
the 8,192-token limit, many-option schemas, score primitives, or production throughput.
No additional suite was created or selected to change this ranking.

[Archive verification](verification.json) confirms complete, unique, single-attempt
records, matched encoding counts, verified response hashes and **exactly unchanged
metrics for every earlier entrant**. Reproduce with `benchmark/perplexity/score.sh`
and `python benchmark/perplexity/analyze.py`; no provider access is required.

The result supports the narrower conclusion that **a tested open checkpoint can
match or exceed commercial entrants on these supplied-rule cases**. It does not
show that every open model does so, that size alone explains the gain, or that
self-hosting has the lowest total cost.
