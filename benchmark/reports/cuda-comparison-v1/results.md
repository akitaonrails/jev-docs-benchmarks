# Decision benchmark v1 results

Synthetic, explicit-policy stress suite. 130 authored scenario families, four variants each (520 classifications), plus 24 probability probes per model. Variants are correlated. No independent human labeling or production-generalization claim.

| Model | Originals | All variants | Original 95% bootstrap interval | Valid/planned | Median / p95 wall seconds | Runner list-price usage value |
| --- | ---: | ---: | --- | --- | --- | ---: |
| laya | 45.4% | 39.2% | 36.9%–53.8% | 544/544 | 0.013 / 0.014 | Unmeasured local compute |
| laya-typed | 44.6% | 38.7% | 36.2%–53.1% | 544/544 | 0.017 / 0.019 | Unmeasured local compute |
| clef-flash-local | 90.8% | 89.0% | 85.4%–95.4% | 544/544 | 0.083 / 0.088 | Unmeasured local compute |
| eikos-4b | 87.7% | 86.5% | 81.5%–93.1% | 544/544 | 0.041 / 0.052 | Unmeasured local compute |
| jebadiah-4b-v2 | 85.4% | 83.8% | 79.2%–91.5% | 544/544 | 0.036 / 0.047 | Unmeasured local compute |
| kev-0.8b | 62.3% | 62.9% | 53.8%–70.8% | 544/544 | 0.049 / 0.054 | Unmeasured local compute |
| kev-4b | 82.3% | 82.7% | 75.4%–88.5% | 544/544 | 0.064 / 0.071 | Unmeasured local compute |
| kev-9b | 87.7% | 85.8% | 81.5%–93.1% | 544/544 | 0.067 / 0.070 | Unmeasured local compute |
| simple-jev | 86.2% | 83.1% | 80.0%–92.3% | 544/544 | 0.153 / 0.164 | Unmeasured local compute |
| decider-4b | 86.9% | 86.2% | 80.8%–92.3% | 544/544 | 0.084 / 0.087 | Unmeasured local compute |
| laya-multilingual | 43.8% | 39.4% | 35.4%–52.3% | 544/544 | 0.010 / 0.012 | Unmeasured local compute |
| julia-1 | 37.7% | 35.4% | 30.0%–46.2% | 544/544 | 0.007 / 0.008 | Unmeasured local compute |
| d3-edge | 64.6% | 66.7% | 56.2%–73.1% | 544/544 | 0.012 / 0.014 | Unmeasured local compute |

Missing/invalid responses count wrong in accuracy. Probability metrics use valid responses only. Latency includes network and retries. Hosted cost is successful reported input usage × published rate, before free allowances, not an invoice; smoke-test calls are separate. Local compute cost is unmeasured.

Three rubric ambiguities were flagged after inference began. Frozen scores above retain them; the separate sensitivity analysis removes all three families for every model. See `datasets/errata.json`.

Original-case baselines: uniform_random: 30.8%, always_first: 19.2%, per_domain_oracle_majority: 37.7%. The majority baseline uses gold label frequencies and is an oracle diagnostic.

## Per-use-case accuracy (all four variants)

| Use case | laya | laya-typed | clef-flash-local | eikos-4b | jebadiah-4b-v2 | kev-0.8b | kev-4b | kev-9b | simple-jev | decider-4b | laya-multilingual | julia-1 | d3-edge |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| support_severity | 20.0% | 32.5% | 75.0% | 72.5% | 75.0% | 32.5% | 60.0% | 67.5% | 90.0% | 85.0% | 30.0% | 35.0% | 60.0% |
| support_routing | 45.0% | 55.0% | 90.0% | 87.5% | 92.5% | 67.5% | 97.5% | 90.0% | 95.0% | 97.5% | 52.5% | 25.0% | 72.5% |
| refund_policy | 37.5% | 37.5% | 80.0% | 55.0% | 55.0% | 37.5% | 40.0% | 60.0% | 45.0% | 85.0% | 40.0% | 35.0% | 27.5% |
| incident_escalation | 37.5% | 25.0% | 90.0% | 90.0% | 80.0% | 77.5% | 100.0% | 100.0% | 100.0% | 95.0% | 30.0% | 40.0% | 60.0% |
| tool_approval | 25.0% | 22.5% | 82.5% | 70.0% | 57.5% | 40.0% | 57.5% | 72.5% | 52.5% | 57.5% | 22.5% | 42.5% | 50.0% |
| email_fraud | 37.5% | 32.5% | 90.0% | 100.0% | 100.0% | 97.5% | 97.5% | 100.0% | 92.5% | 100.0% | 25.0% | 27.5% | 90.0% |
| document_type | 45.0% | 67.5% | 80.0% | 100.0% | 95.0% | 65.0% | 82.5% | 82.5% | 97.5% | 87.5% | 40.0% | 52.5% | 60.0% |
| evidence_support | 50.0% | 40.0% | 100.0% | 90.0% | 80.0% | 62.5% | 95.0% | 90.0% | 87.5% | 72.5% | 47.5% | 30.0% | 90.0% |
| retrieval_relevance | 40.0% | 30.0% | 90.0% | 90.0% | 80.0% | 57.5% | 90.0% | 90.0% | 80.0% | 90.0% | 37.5% | 32.5% | 60.0% |
| moderation | 42.5% | 40.0% | 87.5% | 80.0% | 87.5% | 55.0% | 75.0% | 72.5% | 75.0% | 72.5% | 42.5% | 30.0% | 65.0% |
| request_routing | 67.5% | 62.5% | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 100.0% | 90.0% | 52.5% | 35.0% | 85.0% |
| lead_qualification | 30.0% | 27.5% | 92.5% | 100.0% | 90.0% | 75.0% | 90.0% | 92.5% | 80.0% | 90.0% | 57.5% | 37.5% | 57.5% |
| forecast_triage | 32.5% | 30.0% | 100.0% | 90.0% | 97.5% | 50.0% | 90.0% | 97.5% | 85.0% | 97.5% | 35.0% | 37.5% | 90.0% |

## Sensitivity excluding disputed golds

| Model | Remaining originals (127) | Remaining variants (508) |
| --- | ---: | ---: |
| laya | 45.7% | 39.4% |
| laya-typed | 44.9% | 38.8% |
| clef-flash-local | 92.1% | 90.6% |
| eikos-4b | 89.8% | 88.6% |
| jebadiah-4b-v2 | 87.4% | 85.8% |
| kev-0.8b | 63.8% | 64.4% |
| kev-4b | 84.3% | 84.6% |
| kev-9b | 89.8% | 87.8% |
| simple-jev | 85.8% | 83.9% |
| decider-4b | 89.0% | 87.8% |
| laya-multilingual | 44.1% | 39.6% |
| julia-1 | 37.8% | 35.2% |
| d3-edge | 66.1% | 67.9% |

## Accuracy by presentation

| Model | Original | Reordered | Opaque labels | Injected commentary |
| --- | ---: | ---: | ---: | ---: |
| laya | 45.4% | 43.1% | 47.7% | 20.8% |
| laya-typed | 44.6% | 46.9% | 48.5% | 14.6% |
| clef-flash-local | 90.8% | 90.8% | 89.2% | 85.4% |
| eikos-4b | 87.7% | 88.5% | 86.2% | 83.8% |
| jebadiah-4b-v2 | 85.4% | 86.2% | 84.6% | 79.2% |
| kev-0.8b | 62.3% | 66.9% | 66.2% | 56.2% |
| kev-4b | 82.3% | 83.8% | 82.3% | 82.3% |
| kev-9b | 87.7% | 83.8% | 88.5% | 83.1% |
| simple-jev | 86.2% | 85.4% | 83.8% | 76.9% |
| decider-4b | 86.9% | 86.9% | 84.6% | 86.2% |
| laya-multilingual | 43.8% | 40.0% | 50.0% | 23.8% |
| julia-1 | 37.7% | 30.8% | 37.7% | 35.4% |
| d3-edge | 64.6% | 67.7% | 68.5% | 66.2% |

## Calibration and uncertainty

| Model | Brier ↓ | ECE ↓ | ≥0.9 error rate / coverage | Choice probability MAE ↓ | Noul probability MAE ↓ |
| --- | ---: | ---: | --- | ---: | ---: |
| laya | 0.761 | 0.207 | 60.7% / 5.4% | 0.212 | 0.435 |
| laya-typed | 0.688 | 0.128 | N/A / 0.0% | 0.072 | 0.189 |
| clef-flash-local | 0.181 | 0.037 | 2.3% / 50.0% | 0.143 | 0.522 |
| eikos-4b | 0.203 | 0.049 | 3.2% / 42.1% | 0.213 | 0.552 |
| jebadiah-4b-v2 | 0.262 | 0.087 | 2.2% / 17.5% | 0.192 | 0.565 |
| kev-0.8b | 0.510 | 0.100 | 0.0% / 1.2% | 0.120 | 0.302 |
| kev-4b | 0.256 | 0.063 | 1.7% / 34.8% | 0.093 | 0.633 |
| kev-9b | 0.217 | 0.034 | 3.2% / 53.7% | 0.050 | 0.380 |
| simple-jev | 0.251 | 0.065 | 6.6% / 69.6% | 0.248 | 0.207 |
| decider-4b | 0.198 | 0.026 | 3.5% / 65.4% | 0.173 | 0.187 |
| laya-multilingual | 0.897 | 0.355 | 60.1% / 34.2% | 0.182 | 0.267 |
| julia-1 | 1.065 | 0.477 | 64.2% / 51.0% | 0.217 | 0.297 |
| d3-edge | 0.471 | 0.159 | 13.5% / 50.0% | 0.286 | 0.266 |

These are synthetic-suite calibration diagnostics, not production calibration guarantees. Choice probes score distance to the uniform distribution; Noul probes score the single event probability. Vendor confidence fields are not used.

## Paired original-case accuracy differences

- laya minus laya-typed: +0.8 percentage points; bootstrap 95% interval [-7.7, +9.2].
- laya minus clef-flash-local: -45.4 percentage points; bootstrap 95% interval [-55.4, -36.2].
- laya minus eikos-4b: -42.3 percentage points; bootstrap 95% interval [-52.3, -32.3].
- laya minus jebadiah-4b-v2: -40.0 percentage points; bootstrap 95% interval [-50.8, -29.2].
- laya minus kev-0.8b: -16.9 percentage points; bootstrap 95% interval [-27.7, -5.4].
- laya minus kev-4b: -36.9 percentage points; bootstrap 95% interval [-47.7, -26.2].
- laya minus kev-9b: -42.3 percentage points; bootstrap 95% interval [-52.3, -32.3].
- laya minus simple-jev: -40.8 percentage points; bootstrap 95% interval [-51.5, -30.8].
- laya minus decider-4b: -41.5 percentage points; bootstrap 95% interval [-52.3, -31.5].
- laya minus laya-multilingual: +1.5 percentage points; bootstrap 95% interval [-6.9, +10.0].
- laya minus julia-1: +7.7 percentage points; bootstrap 95% interval [-3.1, +18.5].
- laya minus d3-edge: -19.2 percentage points; bootstrap 95% interval [-30.0, -7.7].
- laya-typed minus clef-flash-local: -46.2 percentage points; bootstrap 95% interval [-55.4, -36.9].
- laya-typed minus eikos-4b: -43.1 percentage points; bootstrap 95% interval [-53.1, -33.1].
- laya-typed minus jebadiah-4b-v2: -40.8 percentage points; bootstrap 95% interval [-50.8, -31.5].
- laya-typed minus kev-0.8b: -17.7 percentage points; bootstrap 95% interval [-28.5, -6.9].
- laya-typed minus kev-4b: -37.7 percentage points; bootstrap 95% interval [-47.7, -27.7].
- laya-typed minus kev-9b: -43.1 percentage points; bootstrap 95% interval [-53.1, -33.1].
- laya-typed minus simple-jev: -41.5 percentage points; bootstrap 95% interval [-51.5, -32.3].
- laya-typed minus decider-4b: -42.3 percentage points; bootstrap 95% interval [-52.3, -32.3].
- laya-typed minus laya-multilingual: +0.8 percentage points; bootstrap 95% interval [-9.2, +10.8].
- laya-typed minus julia-1: +6.9 percentage points; bootstrap 95% interval [-4.6, +18.5].
- laya-typed minus d3-edge: -20.0 percentage points; bootstrap 95% interval [-30.8, -9.2].
- clef-flash-local minus eikos-4b: +3.1 percentage points; bootstrap 95% interval [-2.3, +8.5].
- clef-flash-local minus jebadiah-4b-v2: +5.4 percentage points; bootstrap 95% interval [-0.8, +11.5].
- clef-flash-local minus kev-0.8b: +28.5 percentage points; bootstrap 95% interval [+19.2, +37.7].
- clef-flash-local minus kev-4b: +8.5 percentage points; bootstrap 95% interval [+3.1, +14.6].
- clef-flash-local minus kev-9b: +3.1 percentage points; bootstrap 95% interval [-2.3, +8.5].
- clef-flash-local minus simple-jev: +4.6 percentage points; bootstrap 95% interval [-3.1, +12.3].
- clef-flash-local minus decider-4b: +3.8 percentage points; bootstrap 95% interval [-2.3, +10.0].
- clef-flash-local minus laya-multilingual: +46.9 percentage points; bootstrap 95% interval [+37.7, +56.9].
- clef-flash-local minus julia-1: +53.1 percentage points; bootstrap 95% interval [+42.3, +62.3].
- clef-flash-local minus d3-edge: +26.2 percentage points; bootstrap 95% interval [+17.7, +34.6].
- eikos-4b minus jebadiah-4b-v2: +2.3 percentage points; bootstrap 95% interval [-3.1, +7.7].
- eikos-4b minus kev-0.8b: +25.4 percentage points; bootstrap 95% interval [+17.7, +33.8].
- eikos-4b minus kev-4b: +5.4 percentage points; bootstrap 95% interval [+0.0, +10.8].
- eikos-4b minus kev-9b: +0.0 percentage points; bootstrap 95% interval [-4.6, +4.6].
- eikos-4b minus simple-jev: +1.5 percentage points; bootstrap 95% interval [-6.2, +9.2].
- eikos-4b minus decider-4b: +0.8 percentage points; bootstrap 95% interval [-5.4, +6.9].
- eikos-4b minus laya-multilingual: +43.8 percentage points; bootstrap 95% interval [+33.8, +53.8].
- eikos-4b minus julia-1: +50.0 percentage points; bootstrap 95% interval [+40.0, +59.2].
- eikos-4b minus d3-edge: +23.1 percentage points; bootstrap 95% interval [+14.6, +30.8].
- jebadiah-4b-v2 minus kev-0.8b: +23.1 percentage points; bootstrap 95% interval [+14.6, +32.3].
- jebadiah-4b-v2 minus kev-4b: +3.1 percentage points; bootstrap 95% interval [-3.1, +9.2].
- jebadiah-4b-v2 minus kev-9b: -2.3 percentage points; bootstrap 95% interval [-8.5, +3.1].
- jebadiah-4b-v2 minus simple-jev: -0.8 percentage points; bootstrap 95% interval [-7.7, +6.2].
- jebadiah-4b-v2 minus decider-4b: -1.5 percentage points; bootstrap 95% interval [-7.7, +3.8].
- jebadiah-4b-v2 minus laya-multilingual: +41.5 percentage points; bootstrap 95% interval [+31.5, +51.5].
- jebadiah-4b-v2 minus julia-1: +47.7 percentage points; bootstrap 95% interval [+36.2, +57.7].
- jebadiah-4b-v2 minus d3-edge: +20.8 percentage points; bootstrap 95% interval [+12.3, +30.0].
- kev-0.8b minus kev-4b: -20.0 percentage points; bootstrap 95% interval [-28.5, -11.5].
- kev-0.8b minus kev-9b: -25.4 percentage points; bootstrap 95% interval [-34.6, -16.9].
- kev-0.8b minus simple-jev: -23.8 percentage points; bootstrap 95% interval [-33.1, -14.6].
- kev-0.8b minus decider-4b: -24.6 percentage points; bootstrap 95% interval [-33.1, -16.2].
- kev-0.8b minus laya-multilingual: +18.5 percentage points; bootstrap 95% interval [+6.9, +30.0].
- kev-0.8b minus julia-1: +24.6 percentage points; bootstrap 95% interval [+13.1, +36.2].
- kev-0.8b minus d3-edge: -2.3 percentage points; bootstrap 95% interval [-11.6, +6.9].
- kev-4b minus kev-9b: -5.4 percentage points; bootstrap 95% interval [-11.5, +0.0].
- kev-4b minus simple-jev: -3.8 percentage points; bootstrap 95% interval [-10.8, +3.1].
- kev-4b minus decider-4b: -4.6 percentage points; bootstrap 95% interval [-10.8, +1.5].
- kev-4b minus laya-multilingual: +38.5 percentage points; bootstrap 95% interval [+28.5, +48.5].
- kev-4b minus julia-1: +44.6 percentage points; bootstrap 95% interval [+33.8, +54.6].
- kev-4b minus d3-edge: +17.7 percentage points; bootstrap 95% interval [+10.0, +25.4].
- kev-9b minus simple-jev: +1.5 percentage points; bootstrap 95% interval [-6.2, +9.2].
- kev-9b minus decider-4b: +0.8 percentage points; bootstrap 95% interval [-4.6, +5.4].
- kev-9b minus laya-multilingual: +43.8 percentage points; bootstrap 95% interval [+34.6, +53.1].
- kev-9b minus julia-1: +50.0 percentage points; bootstrap 95% interval [+39.2, +60.0].
- kev-9b minus d3-edge: +23.1 percentage points; bootstrap 95% interval [+14.6, +31.5].
- simple-jev minus decider-4b: -0.8 percentage points; bootstrap 95% interval [-8.5, +6.9].
- simple-jev minus laya-multilingual: +42.3 percentage points; bootstrap 95% interval [+32.3, +52.3].
- simple-jev minus julia-1: +48.5 percentage points; bootstrap 95% interval [+37.7, +58.5].
- simple-jev minus d3-edge: +21.5 percentage points; bootstrap 95% interval [+13.1, +30.0].
- decider-4b minus laya-multilingual: +43.1 percentage points; bootstrap 95% interval [+33.1, +53.1].
- decider-4b minus julia-1: +49.2 percentage points; bootstrap 95% interval [+39.2, +59.2].
- decider-4b minus d3-edge: +22.3 percentage points; bootstrap 95% interval [+13.1, +31.5].
- laya-multilingual minus julia-1: +6.2 percentage points; bootstrap 95% interval [-5.4, +16.9].
- laya-multilingual minus d3-edge: -20.8 percentage points; bootstrap 95% interval [-30.8, -10.8].
- julia-1 minus d3-edge: -26.9 percentage points; bootstrap 95% interval [-38.5, -14.6].

See `summary.json` for confusion matrices, reliability bins, abstention, policy pairs, invariance, probability-probe outputs, and operations details. See `errors.jsonl` for every incorrect or missing classification. Dataset was frozen before inference; do not select only difficult-looking results.
