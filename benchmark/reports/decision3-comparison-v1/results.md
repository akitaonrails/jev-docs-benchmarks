# Decision benchmark v1 results

Synthetic, explicit-policy stress suite. 130 authored scenario families, four variants each (520 classifications), plus 24 probability probes per model. Variants are correlated. No independent human labeling or production-generalization claim.

| Model | Originals | All variants | Original 95% bootstrap interval | Valid/planned | Median / p95 wall seconds | Runner list-price usage value |
| --- | ---: | ---: | --- | --- | --- | ---: |
| jev | 96.2% | 95.2% | 92.3%–99.2% | 544/544 | 0.253 / 0.303 | $0.01127 |
| clef | 94.6% | 95.0% | 90.0%–98.5% | 544/544 | 0.606 / 2.076 | $0.03969 |
| clef-flash | 90.8% | 89.0% | 85.4%–95.4% | 544/544 | 0.491 / 0.884 | $0.01488 |
| laya | 43.8% | 38.5% | 35.4%–52.3% | 544/544 | 0.038 / 0.041 | Unmeasured local compute |
| laya-typed | 43.8% | 38.5% | 35.4%–52.3% | 544/544 | 0.038 / 0.041 | Unmeasured local compute |
| clef-flash-local | 90.8% | 89.0% | 85.4%–95.4% | 544/544 | 0.595 / 0.652 | Unmeasured local compute |
| openai-decisions | 93.1% | 92.9% | 88.5%–96.9% | 544/544 | 0.234 / 0.274 | $0.01512 |
| microsoft-decision-1 | 95.4% | 95.4% | 91.5%–98.5% | 544/544 | 0.403 / 0.476 | $0.00442 |
| eikos-4b | 87.7% | 86.9% | 81.5%–93.1% | 544/544 | 0.190 / 0.211 | Unmeasured local compute |
| jebadiah-4b-v2 | 85.4% | 83.8% | 79.2%–91.5% | 544/544 | 0.151 / 0.188 | Unmeasured local compute |
| decider-4b | 86.9% | 86.0% | 80.8%–92.3% | 544/544 | 0.184 / 0.189 | Unmeasured local compute |
| kev-0.8b | 63.1% | 63.3% | 54.6%–70.8% | 544/544 | 0.080 / 0.100 | Unmeasured local compute |
| kev-4b | 82.3% | 82.7% | 75.4%–88.5% | 544/544 | 0.240 / 0.279 | Unmeasured local compute |
| kev-9b | 87.7% | 85.6% | 81.5%–93.1% | 544/544 | 0.462 / 0.500 | Unmeasured local compute |
| simple-jev | 85.4% | 82.7% | 79.2%–91.5% | 544/544 | 1.182 / 1.322 | Unmeasured local compute |
| laya-multilingual | 43.8% | 39.4% | 35.4%–52.3% | 544/544 | 0.017 / 0.019 | Unmeasured local compute |
| julia-1 | 38.5% | 35.0% | 30.8%–46.9% | 544/544 | 0.011 / 0.024 | Unmeasured local compute |
| julia-1-cpu | 36.9% | 35.2% | 29.2%–45.4% | 544/544 | 0.059 / 0.076 | Unmeasured local compute |
| pplx-decider-27b | 99.2% | 99.2% | 97.7%–100.0% | 544/544 | 1.297 / 1.793 | Unmeasured local compute |
| d3 | 99.2% | 99.2% | 97.7%–100.0% | 544/544 | 1.336 / 1.399 | Unmeasured local compute |
| d3-edge | 65.4% | 66.7% | 56.9%–73.8% | 544/544 | 0.028 / 0.034 | Unmeasured local compute |

Missing/invalid responses count wrong in accuracy. Probability metrics use valid responses only. Latency includes network and retries. Hosted cost is successful reported input usage × published rate, before free allowances, not an invoice; smoke-test calls are separate. Local compute cost is unmeasured.

Three rubric ambiguities were flagged after inference began. Frozen scores above retain them; the separate sensitivity analysis removes all three families for every model. See `datasets/errata.json`.

Original-case baselines: uniform_random: 30.8%, always_first: 19.2%, per_domain_oracle_majority: 37.7%. The majority baseline uses gold label frequencies and is an oracle diagnostic.

## Per-use-case accuracy (all four variants)

| Use case | jev | clef | clef-flash | laya | laya-typed | clef-flash-local | openai-decisions | microsoft-decision-1 | eikos-4b | jebadiah-4b-v2 | decider-4b | kev-0.8b | kev-4b | kev-9b | simple-jev | laya-multilingual | julia-1 | julia-1-cpu | pplx-decider-27b | d3 | d3-edge |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| support_severity | 85.0% | 82.5% | 75.0% | 20.0% | 32.5% | 75.0% | 75.0% | 90.0% | 72.5% | 75.0% | 85.0% | 32.5% | 60.0% | 67.5% | 90.0% | 30.0% | 35.0% | 35.0% | 90.0% | 90.0% | 60.0% |
| support_routing | 100.0% | 100.0% | 90.0% | 45.0% | 57.5% | 90.0% | 100.0% | 100.0% | 87.5% | 92.5% | 97.5% | 67.5% | 97.5% | 90.0% | 95.0% | 52.5% | 25.0% | 27.5% | 100.0% | 100.0% | 72.5% |
| refund_policy | 97.5% | 90.0% | 80.0% | 37.5% | 37.5% | 80.0% | 92.5% | 90.0% | 57.5% | 55.0% | 82.5% | 37.5% | 40.0% | 60.0% | 45.0% | 40.0% | 35.0% | 37.5% | 100.0% | 100.0% | 27.5% |
| incident_escalation | 100.0% | 100.0% | 90.0% | 37.5% | 25.0% | 90.0% | 100.0% | 90.0% | 90.0% | 80.0% | 95.0% | 77.5% | 100.0% | 100.0% | 100.0% | 30.0% | 37.5% | 37.5% | 100.0% | 100.0% | 60.0% |
| tool_approval | 77.5% | 90.0% | 82.5% | 25.0% | 20.0% | 82.5% | 80.0% | 90.0% | 72.5% | 57.5% | 57.5% | 40.0% | 57.5% | 72.5% | 52.5% | 22.5% | 40.0% | 42.5% | 100.0% | 100.0% | 45.0% |
| email_fraud | 100.0% | 100.0% | 90.0% | 37.5% | 35.0% | 90.0% | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 97.5% | 97.5% | 100.0% | 90.0% | 25.0% | 30.0% | 25.0% | 100.0% | 100.0% | 90.0% |
| document_type | 100.0% | 92.5% | 80.0% | 45.0% | 65.0% | 80.0% | 100.0% | 92.5% | 100.0% | 95.0% | 87.5% | 65.0% | 82.5% | 82.5% | 97.5% | 40.0% | 47.5% | 47.5% | 100.0% | 100.0% | 62.5% |
| evidence_support | 100.0% | 100.0% | 100.0% | 50.0% | 40.0% | 100.0% | 100.0% | 100.0% | 90.0% | 80.0% | 70.0% | 65.0% | 95.0% | 90.0% | 87.5% | 47.5% | 30.0% | 30.0% | 100.0% | 100.0% | 92.5% |
| retrieval_relevance | 90.0% | 90.0% | 90.0% | 40.0% | 30.0% | 90.0% | 90.0% | 90.0% | 90.0% | 80.0% | 90.0% | 57.5% | 90.0% | 90.0% | 77.5% | 37.5% | 32.5% | 32.5% | 100.0% | 100.0% | 60.0% |
| moderation | 100.0% | 100.0% | 87.5% | 42.5% | 40.0% | 87.5% | 100.0% | 100.0% | 80.0% | 87.5% | 75.0% | 55.0% | 75.0% | 70.0% | 75.0% | 42.5% | 35.0% | 30.0% | 100.0% | 100.0% | 65.0% |
| request_routing | 87.5% | 100.0% | 100.0% | 62.5% | 62.5% | 100.0% | 80.0% | 97.5% | 100.0% | 100.0% | 90.0% | 100.0% | 100.0% | 100.0% | 100.0% | 52.5% | 35.0% | 37.5% | 100.0% | 100.0% | 85.0% |
| lead_qualification | 100.0% | 97.5% | 92.5% | 30.0% | 27.5% | 92.5% | 90.0% | 100.0% | 100.0% | 90.0% | 90.0% | 75.0% | 90.0% | 92.5% | 80.0% | 57.5% | 35.0% | 37.5% | 100.0% | 100.0% | 57.5% |
| forecast_triage | 100.0% | 92.5% | 100.0% | 27.5% | 27.5% | 100.0% | 100.0% | 100.0% | 90.0% | 97.5% | 97.5% | 52.5% | 90.0% | 97.5% | 85.0% | 35.0% | 37.5% | 37.5% | 100.0% | 100.0% | 90.0% |

## Sensitivity excluding disputed golds

| Model | Remaining originals (127) | Remaining variants (508) |
| --- | ---: | ---: |
| jev | 97.6% | 97.2% |
| clef | 96.9% | 97.2% |
| clef-flash | 92.1% | 90.6% |
| laya | 44.1% | 38.6% |
| laya-typed | 44.1% | 38.6% |
| clef-flash-local | 92.1% | 90.6% |
| openai-decisions | 94.5% | 94.9% |
| microsoft-decision-1 | 96.9% | 96.9% |
| eikos-4b | 89.8% | 89.0% |
| jebadiah-4b-v2 | 87.4% | 85.8% |
| decider-4b | 89.0% | 87.6% |
| kev-0.8b | 64.6% | 64.8% |
| kev-4b | 84.3% | 84.6% |
| kev-9b | 89.8% | 87.6% |
| simple-jev | 85.8% | 83.7% |
| laya-multilingual | 44.1% | 39.6% |
| julia-1 | 38.6% | 34.8% |
| julia-1-cpu | 37.0% | 35.0% |
| pplx-decider-27b | 100.0% | 100.0% |
| d3 | 100.0% | 100.0% |
| d3-edge | 66.9% | 67.9% |

## Accuracy by presentation

| Model | Original | Reordered | Opaque labels | Injected commentary |
| --- | ---: | ---: | ---: | ---: |
| jev | 96.2% | 94.6% | 93.8% | 96.2% |
| clef | 94.6% | 94.6% | 95.4% | 95.4% |
| clef-flash | 90.8% | 90.8% | 89.2% | 85.4% |
| laya | 43.8% | 43.1% | 47.7% | 19.2% |
| laya-typed | 43.8% | 46.9% | 48.5% | 14.6% |
| clef-flash-local | 90.8% | 90.8% | 89.2% | 85.4% |
| openai-decisions | 93.1% | 93.1% | 92.3% | 93.1% |
| microsoft-decision-1 | 95.4% | 95.4% | 95.4% | 95.4% |
| eikos-4b | 87.7% | 88.5% | 86.2% | 85.4% |
| jebadiah-4b-v2 | 85.4% | 86.2% | 84.6% | 79.2% |
| decider-4b | 86.9% | 86.9% | 84.6% | 85.4% |
| kev-0.8b | 63.1% | 66.9% | 66.9% | 56.2% |
| kev-4b | 82.3% | 83.8% | 82.3% | 82.3% |
| kev-9b | 87.7% | 83.8% | 87.7% | 83.1% |
| simple-jev | 85.4% | 85.4% | 83.8% | 76.2% |
| laya-multilingual | 43.8% | 40.0% | 50.8% | 23.1% |
| julia-1 | 38.5% | 30.0% | 38.5% | 33.1% |
| julia-1-cpu | 36.9% | 31.5% | 36.9% | 35.4% |
| pplx-decider-27b | 99.2% | 99.2% | 99.2% | 99.2% |
| d3 | 99.2% | 99.2% | 99.2% | 99.2% |
| d3-edge | 65.4% | 66.2% | 69.2% | 66.2% |

## Calibration and uncertainty

| Model | Brier ↓ | ECE ↓ | ≥0.9 error rate / coverage | Choice probability MAE ↓ | Noul probability MAE ↓ |
| --- | ---: | ---: | --- | ---: | ---: |
| jev | 0.079 | 0.020 | 1.1% / 85.6% | 0.263 | 0.058 |
| clef | 0.081 | 0.034 | 1.2% / 82.3% | 0.073 | 0.378 |
| clef-flash | 0.180 | 0.036 | 2.3% / 50.8% | 0.141 | 0.523 |
| laya | 0.761 | 0.210 | 60.7% / 5.4% | 0.211 | 0.435 |
| laya-typed | 0.687 | 0.114 | N/A / 0.0% | 0.072 | 0.190 |
| clef-flash-local | 0.181 | 0.039 | 2.3% / 50.2% | 0.142 | 0.522 |
| openai-decisions | 0.113 | 0.009 | 2.4% / 79.4% | 0.205 | 0.001 |
| microsoft-decision-1 | 0.082 | 0.035 | 3.0% / 96.3% | 0.125 | 0.369 |
| eikos-4b | 0.201 | 0.042 | 3.2% / 41.9% | 0.213 | 0.554 |
| jebadiah-4b-v2 | 0.263 | 0.086 | 2.2% / 17.5% | 0.192 | 0.563 |
| decider-4b | 0.199 | 0.025 | 3.5% / 65.2% | 0.172 | 0.185 |
| kev-0.8b | 0.510 | 0.093 | 0.0% / 1.2% | 0.121 | 0.300 |
| kev-4b | 0.256 | 0.061 | 1.6% / 35.0% | 0.093 | 0.633 |
| kev-9b | 0.217 | 0.034 | 3.6% / 53.7% | 0.051 | 0.381 |
| simple-jev | 0.253 | 0.069 | 6.9% / 70.0% | 0.247 | 0.200 |
| laya-multilingual | 0.897 | 0.355 | 59.4% / 34.6% | 0.180 | 0.270 |
| julia-1 | 1.071 | 0.485 | 65.9% / 50.2% | 0.218 | 0.296 |
| julia-1-cpu | 1.064 | 0.468 | 64.5% / 49.8% | 0.213 | 0.265 |
| pplx-decider-27b | 0.017 | 0.010 | 0.8% / 95.2% | 0.114 | 0.375 |
| d3 | 0.012 | 0.015 | 0.0% / 93.8% | 0.098 | 0.406 |
| d3-edge | 0.470 | 0.160 | 13.3% / 49.2% | 0.285 | 0.266 |

These are synthetic-suite calibration diagnostics, not production calibration guarantees. Choice probes score distance to the uniform distribution; Noul probes score the single event probability. Vendor confidence fields are not used.

## Paired original-case accuracy differences

- jev minus clef: +1.5 percentage points; bootstrap 95% interval [-3.1, +5.4].
- jev minus clef-flash: +5.4 percentage points; bootstrap 95% interval [+0.8, +10.8].
- jev minus laya: +52.3 percentage points; bootstrap 95% interval [+43.1, +61.5].
- jev minus laya-typed: +52.3 percentage points; bootstrap 95% interval [+43.1, +61.5].
- jev minus clef-flash-local: +5.4 percentage points; bootstrap 95% interval [+0.8, +10.8].
- jev minus openai-decisions: +3.1 percentage points; bootstrap 95% interval [-0.8, +6.9].
- jev minus microsoft-decision-1: +0.8 percentage points; bootstrap 95% interval [-3.1, +4.6].
- jev minus eikos-4b: +8.5 percentage points; bootstrap 95% interval [+3.8, +13.8].
- jev minus jebadiah-4b-v2: +10.8 percentage points; bootstrap 95% interval [+4.6, +16.9].
- jev minus decider-4b: +9.2 percentage points; bootstrap 95% interval [+4.6, +14.6].
- jev minus kev-0.8b: +33.1 percentage points; bootstrap 95% interval [+24.6, +41.5].
- jev minus kev-4b: +13.8 percentage points; bootstrap 95% interval [+7.7, +20.8].
- jev minus kev-9b: +8.5 percentage points; bootstrap 95% interval [+3.8, +13.8].
- jev minus simple-jev: +10.8 percentage points; bootstrap 95% interval [+4.6, +17.7].
- jev minus laya-multilingual: +52.3 percentage points; bootstrap 95% interval [+43.1, +60.8].
- jev minus julia-1: +57.7 percentage points; bootstrap 95% interval [+47.7, +66.2].
- jev minus julia-1-cpu: +59.2 percentage points; bootstrap 95% interval [+49.2, +67.7].
- jev minus pplx-decider-27b: -3.1 percentage points; bootstrap 95% interval [-6.9, +0.0].
- jev minus d3: -3.1 percentage points; bootstrap 95% interval [-6.9, +0.0].
- jev minus d3-edge: +30.8 percentage points; bootstrap 95% interval [+22.3, +38.5].
- clef minus clef-flash: +3.8 percentage points; bootstrap 95% interval [-1.5, +9.2].
- clef minus laya: +50.8 percentage points; bootstrap 95% interval [+42.3, +60.0].
- clef minus laya-typed: +50.8 percentage points; bootstrap 95% interval [+42.3, +60.0].
- clef minus clef-flash-local: +3.8 percentage points; bootstrap 95% interval [-1.5, +9.2].
- clef minus openai-decisions: +1.5 percentage points; bootstrap 95% interval [-3.1, +6.2].
- clef minus microsoft-decision-1: -0.8 percentage points; bootstrap 95% interval [-5.4, +3.8].
- clef minus eikos-4b: +6.9 percentage points; bootstrap 95% interval [+2.3, +12.3].
- clef minus jebadiah-4b-v2: +9.2 percentage points; bootstrap 95% interval [+3.8, +15.4].
- clef minus decider-4b: +7.7 percentage points; bootstrap 95% interval [+3.1, +13.1].
- clef minus kev-0.8b: +31.5 percentage points; bootstrap 95% interval [+23.1, +40.0].
- clef minus kev-4b: +12.3 percentage points; bootstrap 95% interval [+6.2, +18.5].
- clef minus kev-9b: +6.9 percentage points; bootstrap 95% interval [+2.3, +12.3].
- clef minus simple-jev: +9.2 percentage points; bootstrap 95% interval [+2.3, +16.2].
- clef minus laya-multilingual: +50.8 percentage points; bootstrap 95% interval [+41.5, +60.0].
- clef minus julia-1: +56.2 percentage points; bootstrap 95% interval [+46.9, +64.6].
- clef minus julia-1-cpu: +57.7 percentage points; bootstrap 95% interval [+48.5, +66.2].
- clef minus pplx-decider-27b: -4.6 percentage points; bootstrap 95% interval [-8.5, -1.5].
- clef minus d3: -4.6 percentage points; bootstrap 95% interval [-8.5, -1.5].
- clef minus d3-edge: +29.2 percentage points; bootstrap 95% interval [+20.8, +37.7].
- clef-flash minus laya: +46.9 percentage points; bootstrap 95% interval [+37.7, +56.2].
- clef-flash minus laya-typed: +46.9 percentage points; bootstrap 95% interval [+37.7, +56.2].
- clef-flash minus clef-flash-local: +0.0 percentage points; bootstrap 95% interval [+0.0, +0.0].
- clef-flash minus openai-decisions: -2.3 percentage points; bootstrap 95% interval [-7.7, +3.1].
- clef-flash minus microsoft-decision-1: -4.6 percentage points; bootstrap 95% interval [-10.0, -0.8].
- clef-flash minus eikos-4b: +3.1 percentage points; bootstrap 95% interval [-2.3, +8.5].
- clef-flash minus jebadiah-4b-v2: +5.4 percentage points; bootstrap 95% interval [-0.8, +11.5].
- clef-flash minus decider-4b: +3.8 percentage points; bootstrap 95% interval [-2.3, +10.0].
- clef-flash minus kev-0.8b: +27.7 percentage points; bootstrap 95% interval [+18.5, +36.9].
- clef-flash minus kev-4b: +8.5 percentage points; bootstrap 95% interval [+3.1, +14.6].
- clef-flash minus kev-9b: +3.1 percentage points; bootstrap 95% interval [-2.3, +8.5].
- clef-flash minus simple-jev: +5.4 percentage points; bootstrap 95% interval [-1.5, +13.1].
- clef-flash minus laya-multilingual: +46.9 percentage points; bootstrap 95% interval [+37.7, +56.9].
- clef-flash minus julia-1: +52.3 percentage points; bootstrap 95% interval [+42.3, +61.5].
- clef-flash minus julia-1-cpu: +53.8 percentage points; bootstrap 95% interval [+43.8, +63.1].
- clef-flash minus pplx-decider-27b: -8.5 percentage points; bootstrap 95% interval [-13.8, -3.8].
- clef-flash minus d3: -8.5 percentage points; bootstrap 95% interval [-13.8, -3.8].
- clef-flash minus d3-edge: +25.4 percentage points; bootstrap 95% interval [+16.9, +33.8].
- laya minus laya-typed: +0.0 percentage points; bootstrap 95% interval [-8.5, +8.5].
- laya minus clef-flash-local: -46.9 percentage points; bootstrap 95% interval [-56.2, -37.7].
- laya minus openai-decisions: -49.2 percentage points; bootstrap 95% interval [-59.2, -39.2].
- laya minus microsoft-decision-1: -51.5 percentage points; bootstrap 95% interval [-60.8, -42.3].
- laya minus eikos-4b: -43.8 percentage points; bootstrap 95% interval [-53.1, -33.8].
- laya minus jebadiah-4b-v2: -41.5 percentage points; bootstrap 95% interval [-52.3, -30.8].
- laya minus decider-4b: -43.1 percentage points; bootstrap 95% interval [-53.1, -33.1].
- laya minus kev-0.8b: -19.2 percentage points; bootstrap 95% interval [-30.0, -8.5].
- laya minus kev-4b: -38.5 percentage points; bootstrap 95% interval [-49.2, -27.7].
- laya minus kev-9b: -43.8 percentage points; bootstrap 95% interval [-53.8, -33.8].
- laya minus simple-jev: -41.5 percentage points; bootstrap 95% interval [-52.3, -31.5].
- laya minus laya-multilingual: +0.0 percentage points; bootstrap 95% interval [-8.5, +8.5].
- laya minus julia-1: +5.4 percentage points; bootstrap 95% interval [-6.2, +16.2].
- laya minus julia-1-cpu: +6.9 percentage points; bootstrap 95% interval [-4.6, +17.7].
- laya minus pplx-decider-27b: -55.4 percentage points; bootstrap 95% interval [-63.8, -46.9].
- laya minus d3: -55.4 percentage points; bootstrap 95% interval [-63.8, -46.9].
- laya minus d3-edge: -21.5 percentage points; bootstrap 95% interval [-31.5, -10.8].
- laya-typed minus clef-flash-local: -46.9 percentage points; bootstrap 95% interval [-56.2, -37.7].
- laya-typed minus openai-decisions: -49.2 percentage points; bootstrap 95% interval [-59.2, -39.2].
- laya-typed minus microsoft-decision-1: -51.5 percentage points; bootstrap 95% interval [-60.8, -42.3].
- laya-typed minus eikos-4b: -43.8 percentage points; bootstrap 95% interval [-53.8, -33.8].
- laya-typed minus jebadiah-4b-v2: -41.5 percentage points; bootstrap 95% interval [-50.8, -32.3].
- laya-typed minus decider-4b: -43.1 percentage points; bootstrap 95% interval [-53.8, -33.1].
- laya-typed minus kev-0.8b: -19.2 percentage points; bootstrap 95% interval [-30.0, -8.5].
- laya-typed minus kev-4b: -38.5 percentage points; bootstrap 95% interval [-48.5, -29.2].
- laya-typed minus kev-9b: -43.8 percentage points; bootstrap 95% interval [-53.8, -33.8].
- laya-typed minus simple-jev: -41.5 percentage points; bootstrap 95% interval [-50.8, -32.3].
- laya-typed minus laya-multilingual: +0.0 percentage points; bootstrap 95% interval [-9.2, +10.0].
- laya-typed minus julia-1: +5.4 percentage points; bootstrap 95% interval [-6.2, +16.9].
- laya-typed minus julia-1-cpu: +6.9 percentage points; bootstrap 95% interval [-4.6, +18.5].
- laya-typed minus pplx-decider-27b: -55.4 percentage points; bootstrap 95% interval [-63.8, -46.9].
- laya-typed minus d3: -55.4 percentage points; bootstrap 95% interval [-63.8, -46.9].
- laya-typed minus d3-edge: -21.5 percentage points; bootstrap 95% interval [-31.5, -11.5].
- clef-flash-local minus openai-decisions: -2.3 percentage points; bootstrap 95% interval [-7.7, +3.1].
- clef-flash-local minus microsoft-decision-1: -4.6 percentage points; bootstrap 95% interval [-10.0, -0.8].
- clef-flash-local minus eikos-4b: +3.1 percentage points; bootstrap 95% interval [-2.3, +8.5].
- clef-flash-local minus jebadiah-4b-v2: +5.4 percentage points; bootstrap 95% interval [-0.8, +11.5].
- clef-flash-local minus decider-4b: +3.8 percentage points; bootstrap 95% interval [-2.3, +10.0].
- clef-flash-local minus kev-0.8b: +27.7 percentage points; bootstrap 95% interval [+18.5, +36.9].
- clef-flash-local minus kev-4b: +8.5 percentage points; bootstrap 95% interval [+3.1, +14.6].
- clef-flash-local minus kev-9b: +3.1 percentage points; bootstrap 95% interval [-2.3, +8.5].
- clef-flash-local minus simple-jev: +5.4 percentage points; bootstrap 95% interval [-1.5, +13.1].
- clef-flash-local minus laya-multilingual: +46.9 percentage points; bootstrap 95% interval [+37.7, +56.9].
- clef-flash-local minus julia-1: +52.3 percentage points; bootstrap 95% interval [+42.3, +61.5].
- clef-flash-local minus julia-1-cpu: +53.8 percentage points; bootstrap 95% interval [+43.8, +63.1].
- clef-flash-local minus pplx-decider-27b: -8.5 percentage points; bootstrap 95% interval [-13.8, -3.8].
- clef-flash-local minus d3: -8.5 percentage points; bootstrap 95% interval [-13.8, -3.8].
- clef-flash-local minus d3-edge: +25.4 percentage points; bootstrap 95% interval [+16.9, +33.8].
- openai-decisions minus microsoft-decision-1: -2.3 percentage points; bootstrap 95% interval [-6.2, +1.5].
- openai-decisions minus eikos-4b: +5.4 percentage points; bootstrap 95% interval [+0.0, +10.8].
- openai-decisions minus jebadiah-4b-v2: +7.7 percentage points; bootstrap 95% interval [+1.5, +14.6].
- openai-decisions minus decider-4b: +6.2 percentage points; bootstrap 95% interval [+0.8, +12.3].
- openai-decisions minus kev-0.8b: +30.0 percentage points; bootstrap 95% interval [+21.5, +39.2].
- openai-decisions minus kev-4b: +10.8 percentage points; bootstrap 95% interval [+4.6, +17.7].
- openai-decisions minus kev-9b: +5.4 percentage points; bootstrap 95% interval [+0.0, +10.8].
- openai-decisions minus simple-jev: +7.7 percentage points; bootstrap 95% interval [+1.5, +14.6].
- openai-decisions minus laya-multilingual: +49.2 percentage points; bootstrap 95% interval [+40.0, +58.5].
- openai-decisions minus julia-1: +54.6 percentage points; bootstrap 95% interval [+44.6, +63.8].
- openai-decisions minus julia-1-cpu: +56.2 percentage points; bootstrap 95% interval [+46.2, +65.4].
- openai-decisions minus pplx-decider-27b: -6.2 percentage points; bootstrap 95% interval [-10.8, -2.3].
- openai-decisions minus d3: -6.2 percentage points; bootstrap 95% interval [-10.8, -2.3].
- openai-decisions minus d3-edge: +27.7 percentage points; bootstrap 95% interval [+20.0, +36.2].
- microsoft-decision-1 minus eikos-4b: +7.7 percentage points; bootstrap 95% interval [+3.1, +13.1].
- microsoft-decision-1 minus jebadiah-4b-v2: +10.0 percentage points; bootstrap 95% interval [+3.8, +16.2].
- microsoft-decision-1 minus decider-4b: +8.5 percentage points; bootstrap 95% interval [+3.1, +14.6].
- microsoft-decision-1 minus kev-0.8b: +32.3 percentage points; bootstrap 95% interval [+23.8, +40.8].
- microsoft-decision-1 minus kev-4b: +13.1 percentage points; bootstrap 95% interval [+6.9, +20.0].
- microsoft-decision-1 minus kev-9b: +7.7 percentage points; bootstrap 95% interval [+2.3, +13.8].
- microsoft-decision-1 minus simple-jev: +10.0 percentage points; bootstrap 95% interval [+3.1, +16.9].
- microsoft-decision-1 minus laya-multilingual: +51.5 percentage points; bootstrap 95% interval [+42.3, +60.8].
- microsoft-decision-1 minus julia-1: +56.9 percentage points; bootstrap 95% interval [+46.9, +66.2].
- microsoft-decision-1 minus julia-1-cpu: +58.5 percentage points; bootstrap 95% interval [+48.5, +67.7].
- microsoft-decision-1 minus pplx-decider-27b: -3.8 percentage points; bootstrap 95% interval [-7.7, -0.8].
- microsoft-decision-1 minus d3: -3.8 percentage points; bootstrap 95% interval [-7.7, -0.8].
- microsoft-decision-1 minus d3-edge: +30.0 percentage points; bootstrap 95% interval [+21.5, +38.5].
- eikos-4b minus jebadiah-4b-v2: +2.3 percentage points; bootstrap 95% interval [-3.1, +7.7].
- eikos-4b minus decider-4b: +0.8 percentage points; bootstrap 95% interval [-4.6, +6.2].
- eikos-4b minus kev-0.8b: +24.6 percentage points; bootstrap 95% interval [+16.9, +33.1].
- eikos-4b minus kev-4b: +5.4 percentage points; bootstrap 95% interval [+0.0, +10.8].
- eikos-4b minus kev-9b: +0.0 percentage points; bootstrap 95% interval [-4.6, +4.6].
- eikos-4b minus simple-jev: +2.3 percentage points; bootstrap 95% interval [-5.4, +10.0].
- eikos-4b minus laya-multilingual: +43.8 percentage points; bootstrap 95% interval [+33.8, +53.8].
- eikos-4b minus julia-1: +49.2 percentage points; bootstrap 95% interval [+39.2, +58.5].
- eikos-4b minus julia-1-cpu: +50.8 percentage points; bootstrap 95% interval [+40.0, +60.0].
- eikos-4b minus pplx-decider-27b: -11.5 percentage points; bootstrap 95% interval [-17.7, -6.2].
- eikos-4b minus d3: -11.5 percentage points; bootstrap 95% interval [-17.7, -6.2].
- eikos-4b minus d3-edge: +22.3 percentage points; bootstrap 95% interval [+14.6, +30.0].
- jebadiah-4b-v2 minus decider-4b: -1.5 percentage points; bootstrap 95% interval [-7.7, +4.6].
- jebadiah-4b-v2 minus kev-0.8b: +22.3 percentage points; bootstrap 95% interval [+13.8, +30.8].
- jebadiah-4b-v2 minus kev-4b: +3.1 percentage points; bootstrap 95% interval [-3.1, +9.2].
- jebadiah-4b-v2 minus kev-9b: -2.3 percentage points; bootstrap 95% interval [-8.5, +3.1].
- jebadiah-4b-v2 minus simple-jev: +0.0 percentage points; bootstrap 95% interval [-6.9, +6.9].
- jebadiah-4b-v2 minus laya-multilingual: +41.5 percentage points; bootstrap 95% interval [+31.5, +51.5].
- jebadiah-4b-v2 minus julia-1: +46.9 percentage points; bootstrap 95% interval [+36.2, +56.9].
- jebadiah-4b-v2 minus julia-1-cpu: +48.5 percentage points; bootstrap 95% interval [+36.9, +58.5].
- jebadiah-4b-v2 minus pplx-decider-27b: -13.8 percentage points; bootstrap 95% interval [-20.0, -8.5].
- jebadiah-4b-v2 minus d3: -13.8 percentage points; bootstrap 95% interval [-20.0, -8.5].
- jebadiah-4b-v2 minus d3-edge: +20.0 percentage points; bootstrap 95% interval [+11.5, +29.2].
- decider-4b minus kev-0.8b: +23.8 percentage points; bootstrap 95% interval [+15.4, +32.3].
- decider-4b minus kev-4b: +4.6 percentage points; bootstrap 95% interval [-2.3, +11.5].
- decider-4b minus kev-9b: -0.8 percentage points; bootstrap 95% interval [-5.4, +3.8].
- decider-4b minus simple-jev: +1.5 percentage points; bootstrap 95% interval [-6.9, +9.2].
- decider-4b minus laya-multilingual: +43.1 percentage points; bootstrap 95% interval [+33.8, +52.3].
- decider-4b minus julia-1: +48.5 percentage points; bootstrap 95% interval [+38.5, +58.5].
- decider-4b minus julia-1-cpu: +50.0 percentage points; bootstrap 95% interval [+40.0, +60.0].
- decider-4b minus pplx-decider-27b: -12.3 percentage points; bootstrap 95% interval [-18.5, -6.9].
- decider-4b minus d3: -12.3 percentage points; bootstrap 95% interval [-18.5, -6.9].
- decider-4b minus d3-edge: +21.5 percentage points; bootstrap 95% interval [+12.3, +30.8].
- kev-0.8b minus kev-4b: -19.2 percentage points; bootstrap 95% interval [-27.7, -10.8].
- kev-0.8b minus kev-9b: -24.6 percentage points; bootstrap 95% interval [-33.8, -16.2].
- kev-0.8b minus simple-jev: -22.3 percentage points; bootstrap 95% interval [-31.5, -12.3].
- kev-0.8b minus laya-multilingual: +19.2 percentage points; bootstrap 95% interval [+7.7, +30.8].
- kev-0.8b minus julia-1: +24.6 percentage points; bootstrap 95% interval [+13.1, +36.2].
- kev-0.8b minus julia-1-cpu: +26.2 percentage points; bootstrap 95% interval [+14.6, +36.9].
- kev-0.8b minus pplx-decider-27b: -36.2 percentage points; bootstrap 95% interval [-44.6, -28.4].
- kev-0.8b minus d3: -36.2 percentage points; bootstrap 95% interval [-44.6, -28.4].
- kev-0.8b minus d3-edge: -2.3 percentage points; bootstrap 95% interval [-12.3, +7.7].
- kev-4b minus kev-9b: -5.4 percentage points; bootstrap 95% interval [-11.5, +0.0].
- kev-4b minus simple-jev: -3.1 percentage points; bootstrap 95% interval [-9.2, +3.8].
- kev-4b minus laya-multilingual: +38.5 percentage points; bootstrap 95% interval [+28.5, +48.5].
- kev-4b minus julia-1: +43.8 percentage points; bootstrap 95% interval [+33.1, +53.9].
- kev-4b minus julia-1-cpu: +45.4 percentage points; bootstrap 95% interval [+34.6, +55.4].
- kev-4b minus pplx-decider-27b: -16.9 percentage points; bootstrap 95% interval [-23.8, -10.8].
- kev-4b minus d3: -16.9 percentage points; bootstrap 95% interval [-23.8, -10.8].
- kev-4b minus d3-edge: +16.9 percentage points; bootstrap 95% interval [+10.0, +24.6].
- kev-9b minus simple-jev: +2.3 percentage points; bootstrap 95% interval [-4.6, +10.0].
- kev-9b minus laya-multilingual: +43.8 percentage points; bootstrap 95% interval [+34.6, +53.1].
- kev-9b minus julia-1: +49.2 percentage points; bootstrap 95% interval [+39.2, +58.5].
- kev-9b minus julia-1-cpu: +50.8 percentage points; bootstrap 95% interval [+40.8, +60.8].
- kev-9b minus pplx-decider-27b: -11.5 percentage points; bootstrap 95% interval [-16.9, -6.2].
- kev-9b minus d3: -11.5 percentage points; bootstrap 95% interval [-16.9, -6.2].
- kev-9b minus d3-edge: +22.3 percentage points; bootstrap 95% interval [+13.8, +30.8].
- simple-jev minus laya-multilingual: +41.5 percentage points; bootstrap 95% interval [+31.5, +51.5].
- simple-jev minus julia-1: +46.9 percentage points; bootstrap 95% interval [+36.2, +56.9].
- simple-jev minus julia-1-cpu: +48.5 percentage points; bootstrap 95% interval [+37.7, +58.5].
- simple-jev minus pplx-decider-27b: -13.8 percentage points; bootstrap 95% interval [-20.0, -7.7].
- simple-jev minus d3: -13.8 percentage points; bootstrap 95% interval [-20.0, -7.7].
- simple-jev minus d3-edge: +20.0 percentage points; bootstrap 95% interval [+11.5, +28.5].
- laya-multilingual minus julia-1: +5.4 percentage points; bootstrap 95% interval [-5.4, +16.9].
- laya-multilingual minus julia-1-cpu: +6.9 percentage points; bootstrap 95% interval [-3.9, +17.7].
- laya-multilingual minus pplx-decider-27b: -55.4 percentage points; bootstrap 95% interval [-63.8, -47.7].
- laya-multilingual minus d3: -55.4 percentage points; bootstrap 95% interval [-63.8, -47.7].
- laya-multilingual minus d3-edge: -21.5 percentage points; bootstrap 95% interval [-30.8, -11.5].
- julia-1 minus julia-1-cpu: +1.5 percentage points; bootstrap 95% interval [+0.0, +3.8].
- julia-1 minus pplx-decider-27b: -60.8 percentage points; bootstrap 95% interval [-68.5, -52.3].
- julia-1 minus d3: -60.8 percentage points; bootstrap 95% interval [-68.5, -52.3].
- julia-1 minus d3-edge: -26.9 percentage points; bootstrap 95% interval [-37.7, -15.4].
- julia-1-cpu minus pplx-decider-27b: -62.3 percentage points; bootstrap 95% interval [-70.0, -53.8].
- julia-1-cpu minus d3: -62.3 percentage points; bootstrap 95% interval [-70.0, -53.8].
- julia-1-cpu minus d3-edge: -28.5 percentage points; bootstrap 95% interval [-39.2, -16.9].
- pplx-decider-27b minus d3: +0.0 percentage points; bootstrap 95% interval [+0.0, +0.0].
- pplx-decider-27b minus d3-edge: +33.8 percentage points; bootstrap 95% interval [+26.1, +41.6].
- d3 minus d3-edge: +33.8 percentage points; bootstrap 95% interval [+26.1, +41.6].

See `summary.json` for confusion matrices, reliability bins, abstention, policy pairs, invariance, probability-probe outputs, and operations details. See `errors.jsonl` for every incorrect or missing classification. Dataset was frozen before inference; do not select only difficult-looking results.
