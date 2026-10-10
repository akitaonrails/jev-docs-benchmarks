# Decision benchmark v1 results

Synthetic, explicit-policy stress suite. 130 authored scenario families, four variants each (520 classifications), plus 24 probability probes per model. Variants are correlated. No independent human labeling or production-generalization claim.

| Model | Originals | All variants | Original 95% bootstrap interval | Valid/planned | Median / p95 wall seconds | List-price usage value |
| --- | ---: | ---: | --- | --- | --- | ---: |
| jev | 96.2% | 95.2% | 92.3%–99.2% | 544/544 | 0.253 / 0.303 | $0.01127 |
| clef | 94.6% | 95.0% | 90.0%–98.5% | 544/544 | 0.606 / 2.076 | $0.03969 |
| clef-flash | 90.8% | 89.0% | 85.4%–95.4% | 544/544 | 0.491 / 0.884 | $0.01488 |
| laya | 43.8% | 38.5% | 35.4%–52.3% | 544/544 | 0.038 / 0.041 | Unmeasured local compute |
| laya-typed | 43.8% | 38.5% | 35.4%–52.3% | 544/544 | 0.038 / 0.041 | Unmeasured local compute |
| clef-flash-local | 90.8% | 89.0% | 85.4%–95.4% | 544/544 | 0.595 / 0.652 | Unmeasured local compute |

Missing/invalid responses count wrong in accuracy. Probability metrics use valid responses only. Latency includes network and retries. Hosted cost is successful reported input usage × published rate, before free allowances, not an invoice; smoke-test calls are separate. Local compute cost is unmeasured.

Three rubric ambiguities were flagged after inference began. Frozen scores above retain them; the separate sensitivity analysis removes all three families for every model. See `datasets/errata.json`.

Original-case baselines: uniform_random: 30.8%, always_first: 19.2%, per_domain_oracle_majority: 37.7%. The majority baseline uses gold label frequencies and is an oracle diagnostic.

## Per-use-case accuracy (all four variants)

| Use case | jev | clef | clef-flash | laya | laya-typed | clef-flash-local |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| support_severity | 85.0% | 82.5% | 75.0% | 20.0% | 32.5% | 75.0% |
| support_routing | 100.0% | 100.0% | 90.0% | 45.0% | 57.5% | 90.0% |
| refund_policy | 97.5% | 90.0% | 80.0% | 37.5% | 37.5% | 80.0% |
| incident_escalation | 100.0% | 100.0% | 90.0% | 37.5% | 25.0% | 90.0% |
| tool_approval | 77.5% | 90.0% | 82.5% | 25.0% | 20.0% | 82.5% |
| email_fraud | 100.0% | 100.0% | 90.0% | 37.5% | 35.0% | 90.0% |
| document_type | 100.0% | 92.5% | 80.0% | 45.0% | 65.0% | 80.0% |
| evidence_support | 100.0% | 100.0% | 100.0% | 50.0% | 40.0% | 100.0% |
| retrieval_relevance | 90.0% | 90.0% | 90.0% | 40.0% | 30.0% | 90.0% |
| moderation | 100.0% | 100.0% | 87.5% | 42.5% | 40.0% | 87.5% |
| request_routing | 87.5% | 100.0% | 100.0% | 62.5% | 62.5% | 100.0% |
| lead_qualification | 100.0% | 97.5% | 92.5% | 30.0% | 27.5% | 92.5% |
| forecast_triage | 100.0% | 92.5% | 100.0% | 27.5% | 27.5% | 100.0% |

## Sensitivity excluding disputed golds

| Model | Remaining originals (127) | Remaining variants (508) |
| --- | ---: | ---: |
| jev | 97.6% | 97.2% |
| clef | 96.9% | 97.2% |
| clef-flash | 92.1% | 90.6% |
| laya | 44.1% | 38.6% |
| laya-typed | 44.1% | 38.6% |
| clef-flash-local | 92.1% | 90.6% |

## Accuracy by presentation

| Model | Original | Reordered | Opaque labels | Injected commentary |
| --- | ---: | ---: | ---: | ---: |
| jev | 96.2% | 94.6% | 93.8% | 96.2% |
| clef | 94.6% | 94.6% | 95.4% | 95.4% |
| clef-flash | 90.8% | 90.8% | 89.2% | 85.4% |
| laya | 43.8% | 43.1% | 47.7% | 19.2% |
| laya-typed | 43.8% | 46.9% | 48.5% | 14.6% |
| clef-flash-local | 90.8% | 90.8% | 89.2% | 85.4% |

## Calibration and uncertainty

| Model | Brier ↓ | ECE ↓ | ≥0.9 error rate / coverage | Choice probability MAE ↓ | Noul probability MAE ↓ |
| --- | ---: | ---: | --- | ---: | ---: |
| jev | 0.079 | 0.020 | 1.1% / 85.6% | 0.263 | 0.058 |
| clef | 0.081 | 0.034 | 1.2% / 82.3% | 0.073 | 0.378 |
| clef-flash | 0.180 | 0.036 | 2.3% / 50.8% | 0.141 | 0.523 |
| laya | 0.761 | 0.210 | 60.7% / 5.4% | 0.211 | 0.435 |
| laya-typed | 0.687 | 0.114 | N/A / 0.0% | 0.072 | 0.190 |
| clef-flash-local | 0.181 | 0.039 | 2.3% / 50.2% | 0.142 | 0.522 |

These are synthetic-suite calibration diagnostics, not production calibration guarantees. Choice probes score distance to the uniform distribution; Noul probes score the single event probability. Vendor confidence fields are not used.

## Paired original-case accuracy differences

- jev minus clef: +1.5 percentage points; bootstrap 95% interval [-3.1, +5.4].
- jev minus clef-flash: +5.4 percentage points; bootstrap 95% interval [+0.8, +10.8].
- jev minus laya: +52.3 percentage points; bootstrap 95% interval [+43.1, +61.5].
- jev minus laya-typed: +52.3 percentage points; bootstrap 95% interval [+43.1, +61.5].
- jev minus clef-flash-local: +5.4 percentage points; bootstrap 95% interval [+0.8, +10.8].
- clef minus clef-flash: +3.8 percentage points; bootstrap 95% interval [-1.5, +9.2].
- clef minus laya: +50.8 percentage points; bootstrap 95% interval [+42.3, +60.0].
- clef minus laya-typed: +50.8 percentage points; bootstrap 95% interval [+42.3, +60.0].
- clef minus clef-flash-local: +3.8 percentage points; bootstrap 95% interval [-1.5, +9.2].
- clef-flash minus laya: +46.9 percentage points; bootstrap 95% interval [+37.7, +56.2].
- clef-flash minus laya-typed: +46.9 percentage points; bootstrap 95% interval [+37.7, +56.2].
- clef-flash minus clef-flash-local: +0.0 percentage points; bootstrap 95% interval [+0.0, +0.0].
- laya minus laya-typed: +0.0 percentage points; bootstrap 95% interval [-8.5, +8.5].
- laya minus clef-flash-local: -46.9 percentage points; bootstrap 95% interval [-56.2, -37.7].
- laya-typed minus clef-flash-local: -46.9 percentage points; bootstrap 95% interval [-56.2, -37.7].

See `summary.json` for confusion matrices, reliability bins, abstention, policy pairs, invariance, probability-probe outputs, and operations details. See `errors.jsonl` for every incorrect or missing classification. Dataset was frozen before inference; do not select only difficult-looking results.
