# OpenAI Decisions on the original policy suite

Completed 11 October 2026 UTC / 10 October São Paulo. **544 valid responses,
544 attempts, no API/schema failures**: 520 classifications plus 24 separate
probability probes. The alias returned was `gpt-6-luna`; no immutable server
checkpoint identifier was available. Original competitors are reused from archives.

| Hosted configuration | Original cases | All variants | Excluding disputed originals |
| --- | ---: | ---: | ---: |
| Jev | 125/130, 96.2% | 495/520, 95.2% | 124/127, 97.6% |
| Clef | 123/130, 94.6% | 494/520, 95.0% | 123/127, 96.9% |
| OpenAI Decisions | 121/130, 93.1% | 483/520, 92.9% | 120/127, 94.5% |
| Clef-flash | 118/130, 90.8% | 463/520, 89.0% | 117/127, 92.1% |

All five prespecified policy-counterfactual pairs are correct for OpenAI. However,
option reordering, opaque labels and injected commentary each cause two originally
correct cases to become wrong. Identical aggregate totals do not establish
presentation invariance.

OpenAI misses the undisputed single-customer ongoing-production-data-loss ticket:
it chooses degraded instead of the required critical. It gets the other undisputed
critical original right. The third critical-labeled original belongs to the existing
errata, so do not infer a production critical-miss rate from the three-case aggregate.

Probability probes expose a primitive-specific difference. Native predicates
closely preserve 1/2, 1/4 and 1/6 event uncertainty (MAE 0.00111); native choices
remain biased (per-option MAE 0.20481), selecting the first option in 11/12 probes.
These probes have no hidden outcome to guess and are scored separately from accuracy.

The v1 OpenAI usage value is **$0.015123**, excluding the separate smoke test;
median/p95 client latency is **234/274 ms**. Prices are usage valuations, not invoices.
The generated [results](results.md) preserve historical runner rates for the earlier
providers (including Flash's old $0.09/M). Use the [dated current cost comparison](../openai-comparison-v2/costs.md)
for current listed rates; do not mistake old runner rates for current pricing.

See the [complete analysis](../openai-comparison-v2/analysis.md) for bilingual
results, ranking, practical cost/benefit, uncertainty and limitations. The
[summary](summary.json) and [error list](errors.jsonl) preserve all 15 entrants.
