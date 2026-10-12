# Decision 3.0 on the original policy suite

12 October 2026. Each model completes 544 valid, single-attempt responses:
520 classification variants and 24 separate probability probes. All complete input
encodings match reported usage. [Full results](results.md),
[verification](../decision3-comparison-v2/verification.json),
[inspectable original/compact errors](../decision3-comparison-v2/selected-errors.json).

| Model | Originals | All variants | Originals after common exclusions | Variants after common exclusions | Median / p95 |
| --- | ---: | ---: | ---: | ---: | ---: |
| d3 | 129/130 (99.2%) | 516/520 (99.2%) | 127/127 | 508/508 | 1,336 / 1,399 ms |
| d3-edge | 85/130 (65.4%) | 347/520 (66.7%) | 85/127 | 345/508 | 28 / 34 ms |

## Flagship: same classification labels as Perplexity

All 520 d3 labels match Perplexity's existing run. The only failed family is
`support_severity-07`: two tenants cannot export invoices after a recovered outage.
The gold says critical; d3 says degraded. This case was already listed in the common
errata because feature impairment versus a production outage is ambiguous. No gold
was changed for this run. The two undisputed critical originals are both recognized.

D3 passes all five counterfactual policy-change pairs. Every original semantic label
survives reordered options, opaque labels and the tested injected commentary. This
is limited robustness evidence from these fixtures, not comprehensive attack resistance.

## Edge: errors relevant to actual support routing

Edge labels the verified inability of three production tenants to check out as
unknown, missing a clear critical case (`support_severity-02`). It also mistakes a
staging-only cosmetic problem for production degradation when the customer calls
it critical. Those errors matter more for a support workflow than schema validity.

It passes three of five policy-change pairs. Semantic agreement with originals is
122/130 after option reordering, 117/130 with opaque names, and 113/130 with injected
commentary. Respectively 3, 2 and 5 originally correct answers become wrong. Some
wrong answers also become correct, so aggregate changes alone hide instability.

## Separate uncertainty probes

D3's choice MAE is 0.0979 and Boolean/Noul MAE 0.4061; Edge's are 0.2847 and 0.2659.
A one-in-six Boolean event receives 0.7469 from d3. Edge assigns 0.0531 to a fair
binary event. There are only twelve probes per primitive, but these are concrete
failures of the known probabilities. High classification accuracy does not justify
using these outputs as unvalidated event probabilities.

[Combined bilingual, resource and cost analysis](../decision3-comparison-v2/analysis.md).
