# Decision 3.0: flagship matches the local leader; Edge trades accuracy for size

12 October 2026. **2,096 new valid responses, one attempt each, no errors or input loss.**
The comparison now has 23 bilingual configurations (11,592 v2 classifications) and
21 policy configurations (11,424 responses). All previous model metrics are unchanged.
Both services are stopped. [Verification](verification.json), [ranking](ranking.md),
[task/language tables](results.md).

The user selected the flagship **d3** and smallest **d3-edge**.
Both use pinned native BF16 models on the AMD homelab. No intermediate variants,
image/video tests, CPU tests or hosted inference calls were added.
[Protocol](../../decision3/README.md), [availability](../../../docs/decision3-availability.md).

## Bilingual classification

| Model | Compact EN / 84 | Compact PT-BR / 84 | Compact total / 168 | Examples / 168 | Distractors / 168 | All / 504 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| d3 | 83 | 84 | 167 (99.4%) | 167 | 167 | 501 |
| Perplexity Decider 27B | 83 | 84 | 167 (99.4%) | 167 | 167 | 501 |
| d3-edge | 57 | 45 | 102 (60.7%) | 86 | 99 | 287 |

**d3 and Perplexity agree on every one of the 504 labels.** Both miss only the
English `retrieval-11` family in all three conditions: a passage saying approval
notifications go to managers does not establish which role is required to approve.
Both select full relevance, where the supplied rule requires none. Portuguese
versions pass. Identical labels do not imply identical probabilities, weights or
training, and this suite cannot distinguish their classification quality.

Microsoft and Jev each remain at 164/168 compact. The three-answer lead of either
large local model is small and does not establish general superiority. Related
Qwen-derived models and repeated translations/conditions are dependent observations.

Edge is above the suite's 31.0% uniform-random baseline and above the tested tiny
Laya/Julia point estimates, but its errors remain substantial. Compact task totals
are 19/24 entailment, 18/24 threshold policy, 16/24 data handling, 14/24 sentiment,
14/24 current status, 12/24 intent and 9/24 retrieval. These small cells describe
this untuned workload; they do not establish a reliable production specialization.
Its compact PT-BR result trails English by twelve cases. Worked examples reduce
the combined count from 102 to 86; more context does not reliably compensate for
capacity or training differences.

## Timing, probabilities and the original policy suite

| Entrant | v2 median / p95 | v1 originals / 130 | All v1 variants / 520 | Compact Brier | Compact probability ≥0.9: errors / selected |
| --- | ---: | ---: | ---: | ---: | ---: |
| d3 | 1,420 / 2,135 ms | 129 | 516 | 0.01375 | 0 / 158 |
| Perplexity 27B | 1,547 / 2,446 ms | 129 | 516 | 0.01241 | 0 / 161 |
| d3-edge | 45 / 102 ms | 85 | 347 | 0.55034 | 14 / 68 |

The large models also agree on all 520 v1 classification labels: **1,024 identical
labels across both suites**. This ceiling limits the benchmark's ability to choose
between them; their probability outputs differ. A lower observed d3 median is not
a controlled speed win: the runs occurred at different times and neither is an
optimized hardware comparison. Startup and warmup are excluded.

D3's sole v1 failure family is the existing disputed `support_severity-07` case,
about invoice-export impairment versus a production outage. After the same three
pre-existing family exclusions, it scores 127/127 originals and 508/508 variants.
All five policy-change pairs pass, and all original semantic labels survive
reordering, opaque names and the tested injection. Edge passes only three policy
pairs and misses a clear multi-tenant checkout outage. [Detailed v1 analysis](../decision3-comparison-v1/analysis.md).

High-confidence Edge predictions still contain **20.6% errors** in this compact
sample. D3's zero observed errors above 0.9 is limited to 158 predictions on these
fixtures and does not validate a production threshold.

| Model | Choice uncertainty MAE | Boolean/Noul uncertainty MAE |
| --- | ---: | ---: |
| d3 | 0.0979 | 0.4061 |
| Perplexity 27B | 0.1140 | 0.3754 |
| d3-edge | 0.2847 | 0.2659 |

There are twelve probes per primitive. D3 gives **0.7469** to an event explicitly
having probability **1/6**; Edge gives **0.0531** to a fair binary event. Edge's lower
Boolean MAE does not make its estimates reliable. Classification quality, choice
uncertainty and Boolean event probabilities must be evaluated separately.

## Paired comparisons and model size

D3 minus Perplexity is 0.0 points with a [0.0, 0.0] family-bootstrap interval because
their labels match here; this is not proof of population equivalence. D3 minus
Microsoft is +1.8 points [0.0, +4.2]. D3 minus Edge is +38.7 points [+29.8, +47.6].
Edge versus Kev 0.8B is -2.4 points [-9.5, +5.4], so that small observed ordering is
uncertain. Intervals cluster English/PT-BR by authored family and are exploratory,
without multiple-comparison correction. [Exact comparisons](paired-family-comparisons.json).

Edge's compact PT-BR minus English difference is -14.3 points, paired interval
[-26.2, -2.4]. D3's is +1.2 points [0.0, +3.6]. These results concern these paired
translations, not universal language rankings.

Across **19 known-size configurations** after excluding duplicate Flash/Julia
deployments, Spearman is **0.958**, Pearson(log10 size, compact accuracy) **0.958**.
Unknown-size Jev/OpenAI are excluded. The association remains strong but confounded
by training, architecture and model selection. Two endpoints do not isolate a
causal size effect or establish the best intermediate checkpoint.

## Deployment and price interpretation

Both models retain their vision weights during this text-only test. Published size
labels are 27B and 0.6B; the cards give 26.09B and 0.59B total parameters. Measured
GPU tensor allocation is roughly 48.7 GiB for d3 versus 1.24 GiB for Edge. A sampled
Edge container used 2.21 GiB host memory; a d3 sample used 21.78 GiB. System GPU
usage includes unrelated baseline allocations and allocator reservations, so these
numbers are not interchangeable or isolated peak-memory measurements. The full
model's warmup approached the 64 GiB GPU limit.

The native model uses BF16 weights and FP32 readout with temperature 1.0. Full d3
uses a strict shard-at-a-time GPU loader to avoid host-memory spikes. The loaded
image launcher matches the captured source; all snapshot manifest hashes were
independently verified. ROCm reference kernels are used. The original publisher's
MI325X latency claims are not directly comparable to this deployment.

No new hosted inference was performed. The dated 11 October hosted-price snapshot
and previous usage valuations remain applicable to those archived calls; local
hardware, electricity and operations are **unmeasured**, not $0. Microsoft remains
the leading paid hosted cost-benefit candidate on this input mix: $0.00645 per
1,000 compact calls, versus Jev $0.01916. That hosted ordering is unaffected by
adding local models without measured dollar costs.

Edge's small memory footprint may matter on a constrained device, but this run
used the same GPU as d3. It establishes neither CPU performance nor that its 60.7%
compact accuracy is sufficient for a particular application. The two endpoints of
a family also cannot identify its best intermediate size; those were intentionally
not tested.

## Evidence and limitations

Every model sees the same frozen 544-request v1 and 504-request v2 suites. Golds,
policies, translations and options are unchanged; there was no output-driven tuning.
All 2,096 inputs independently encode to 146–728 tokens, and scored usage must
match those complete encodings. The 8,192-token site cap rejects oversized input.
Image digests, native runtime checks and model revisions are recorded. Scoring and
comparison are offline; prior entrants' metrics must remain exactly unchanged.

Synthetic AI-authored scenarios, limited task cells, correlated variants and existing
v1 gold ambiguities constrain generalization. Calibration on deterministic labels
and known-random probability probes answer different questions. Classification
accuracy alone cannot validate a confidence threshold or a production workflow.
