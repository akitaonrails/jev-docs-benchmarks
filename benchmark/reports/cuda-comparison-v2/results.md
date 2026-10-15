# v2 bilingual expansion results

84 authored families, paired translations, three correlated conditions. Compact is the primary language comparison. Task cells have only 12 families; numerical wins are exploratory.

| Model | Compact EN | Compact PT-BR | PT minus EN (paired bootstrap 95%) | Examples EN / PT | Distractors EN / PT |
| --- | ---: | ---: | --- | --- | --- |
| laya | 45.2% | 41.7% | -3.6% [-15.5%, +8.3%] | 38.1% / 35.7% | 39.3% / 35.7% |
| laya-typed | 47.6% | 35.7% | -11.9% [-25.0%, +0.0%] | 44.0% / 36.9% | 44.0% / 32.1% |
| clef-flash-local | 89.3% | 85.7% | -3.6% [-10.7%, +3.6%] | 90.5% / 84.5% | 88.1% / 85.7% |
| eikos-4b | 85.7% | 79.8% | -6.0% [-14.3%, +1.2%] | 79.8% / 81.0% | 84.5% / 79.8% |
| jebadiah-4b-v2 | 91.7% | 89.3% | -2.4% [-9.5%, +4.8%] | 90.5% / 85.7% | 86.9% / 75.0% |
| kev-0.8b | 64.3% | 59.5% | -4.8% [-16.7%, +7.1%] | 63.1% / 60.7% | 53.6% / 50.0% |
| kev-4b | 88.1% | 86.9% | -1.2% [-9.5%, +6.0%] | 84.5% / 81.0% | 78.6% / 70.2% |
| kev-9b | 91.7% | 84.5% | -7.1% [-13.1%, -1.2%] | 92.9% / 91.7% | 89.3% / 75.0% |
| simple-jev | 77.4% | 72.6% | -4.8% [-14.3%, +4.8%] | 81.0% / 82.1% | 77.4% / 65.5% |
| decider-4b | 89.3% | 85.7% | -3.6% [-10.7%, +3.6%] | 85.7% / 84.5% | 85.7% / 82.1% |
| laya-multilingual | 34.5% | 38.1% | +3.6% [-8.3%, +14.3%] | 31.0% / 36.9% | 26.2% / 34.5% |
| julia-1 | 36.9% | 25.0% | -11.9% [-23.8%, -1.2%] | 29.8% / 27.4% | 33.3% / 34.5% |
| d3-edge | 69.0% | 52.4% | -16.7% [-27.4%, -6.0%] | 52.4% / 47.6% | 65.5% / 50.0% |
| gliner2.5-decide | 54.8% | 50.0% | -4.8% [-15.5%, +6.0%] | 47.6% / 41.7% | 59.5% / 45.2% |
| gliner2.5-multi-decide | 32.1% | 35.7% | +3.6% [-6.0%, +13.1%] | 27.4% / 39.3% | 34.5% / 39.3% |

## Compact tasks: en

| Task | laya | laya-typed | clef-flash-local | eikos-4b | jebadiah-4b-v2 | kev-0.8b | kev-4b | kev-9b | simple-jev | decider-4b | laya-multilingual | julia-1 | d3-edge | gliner2.5-decide | gliner2.5-multi-decide |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| sentiment | 33.3% | 41.7% | 100.0% | 83.3% | 91.7% | 83.3% | 100.0% | 100.0% | 75.0% | 100.0% | 16.7% | 25.0% | 75.0% | 25.0% | 25.0% |
| intent | 58.3% | 75.0% | 75.0% | 100.0% | 100.0% | 58.3% | 91.7% | 91.7% | 91.7% | 100.0% | 41.7% | 50.0% | 66.7% | 75.0% | 33.3% |
| entailment | 66.7% | 50.0% | 83.3% | 91.7% | 100.0% | 83.3% | 91.7% | 91.7% | 75.0% | 75.0% | 33.3% | 33.3% | 83.3% | 50.0% | 33.3% |
| retrieval | 41.7% | 50.0% | 91.7% | 91.7% | 91.7% | 50.0% | 83.3% | 83.3% | 91.7% | 91.7% | 41.7% | 41.7% | 33.3% | 41.7% | 33.3% |
| data_handling | 33.3% | 33.3% | 83.3% | 75.0% | 83.3% | 66.7% | 75.0% | 91.7% | 66.7% | 75.0% | 33.3% | 33.3% | 75.0% | 58.3% | 41.7% |
| current_status | 41.7% | 33.3% | 100.0% | 91.7% | 100.0% | 58.3% | 100.0% | 100.0% | 91.7% | 100.0% | 50.0% | 50.0% | 66.7% | 83.3% | 41.7% |
| threshold_policy | 41.7% | 50.0% | 91.7% | 66.7% | 75.0% | 50.0% | 75.0% | 83.3% | 50.0% | 83.3% | 25.0% | 25.0% | 83.3% | 50.0% | 16.7% |

## Compact tasks: pt-BR

| Task | laya | laya-typed | clef-flash-local | eikos-4b | jebadiah-4b-v2 | kev-0.8b | kev-4b | kev-9b | simple-jev | decider-4b | laya-multilingual | julia-1 | d3-edge | gliner2.5-decide | gliner2.5-multi-decide |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| sentiment | 33.3% | 25.0% | 100.0% | 75.0% | 91.7% | 58.3% | 100.0% | 91.7% | 91.7% | 100.0% | 25.0% | 16.7% | 41.7% | 58.3% | 0.0% |
| intent | 41.7% | 33.3% | 91.7% | 91.7% | 100.0% | 75.0% | 83.3% | 75.0% | 91.7% | 83.3% | 50.0% | 25.0% | 33.3% | 58.3% | 50.0% |
| entailment | 33.3% | 33.3% | 91.7% | 91.7% | 91.7% | 83.3% | 100.0% | 91.7% | 58.3% | 83.3% | 41.7% | 16.7% | 75.0% | 33.3% | 41.7% |
| retrieval | 41.7% | 25.0% | 75.0% | 83.3% | 83.3% | 33.3% | 66.7% | 83.3% | 58.3% | 83.3% | 50.0% | 33.3% | 33.3% | 50.0% | 25.0% |
| data_handling | 66.7% | 25.0% | 75.0% | 83.3% | 91.7% | 58.3% | 83.3% | 75.0% | 58.3% | 83.3% | 25.0% | 25.0% | 66.7% | 50.0% | 50.0% |
| current_status | 33.3% | 66.7% | 83.3% | 75.0% | 91.7% | 50.0% | 91.7% | 91.7% | 91.7% | 91.7% | 41.7% | 50.0% | 50.0% | 66.7% | 50.0% |
| threshold_policy | 41.7% | 41.7% | 83.3% | 58.3% | 75.0% | 58.3% | 83.3% | 83.3% | 58.3% | 75.0% | 33.3% | 8.3% | 66.7% | 33.3% | 33.3% |

## Input truncation

| Model | Condition | Reported truncated / valid | Missing truncation telemetry |
| --- | --- | ---: | ---: |
| laya | compact | 0/168 | 0 |
| laya | examples | 0/168 | 0 |
| laya | distractors | 84/168 | 0 |
| laya-typed | compact | 0/168 | 0 |
| laya-typed | examples | 0/168 | 0 |
| laya-typed | distractors | 0/168 | 0 |
| clef-flash-local | compact | 0/168 | 168 |
| clef-flash-local | examples | 0/168 | 168 |
| clef-flash-local | distractors | 0/168 | 168 |
| eikos-4b | compact | 0/168 | 168 |
| eikos-4b | examples | 0/168 | 168 |
| eikos-4b | distractors | 0/168 | 168 |
| jebadiah-4b-v2 | compact | 0/168 | 168 |
| jebadiah-4b-v2 | examples | 0/168 | 168 |
| jebadiah-4b-v2 | distractors | 0/168 | 168 |
| kev-0.8b | compact | 0/168 | 168 |
| kev-0.8b | examples | 0/168 | 168 |
| kev-0.8b | distractors | 0/168 | 168 |
| kev-4b | compact | 0/168 | 168 |
| kev-4b | examples | 0/168 | 168 |
| kev-4b | distractors | 0/168 | 168 |
| kev-9b | compact | 0/168 | 168 |
| kev-9b | examples | 0/168 | 168 |
| kev-9b | distractors | 0/168 | 168 |
| simple-jev | compact | 0/168 | 168 |
| simple-jev | examples | 0/168 | 168 |
| simple-jev | distractors | 0/168 | 168 |
| decider-4b | compact | 0/168 | 168 |
| decider-4b | examples | 0/168 | 168 |
| decider-4b | distractors | 0/168 | 168 |
| laya-multilingual | compact | 0/168 | 0 |
| laya-multilingual | examples | 0/168 | 0 |
| laya-multilingual | distractors | 0/168 | 0 |
| julia-1 | compact | 0/168 | 0 |
| julia-1 | examples | 0/168 | 0 |
| julia-1 | distractors | 0/168 | 0 |
| d3-edge | compact | 0/168 | 168 |
| d3-edge | examples | 0/168 | 168 |
| d3-edge | distractors | 0/168 | 168 |
| gliner2.5-decide | compact | 0/168 | 168 |
| gliner2.5-decide | examples | 0/168 | 168 |
| gliner2.5-decide | distractors | 0/168 | 168 |
| gliner2.5-multi-decide | compact | 0/168 | 168 |
| gliner2.5-multi-decide | examples | 0/168 | 168 |
| gliner2.5-multi-decide | distractors | 0/168 | 168 |

## Latency and current hosted usage value

All 504 requests/model; conditions have different lengths. Local operating cost is unmeasured. Hosted values use the dated pricing snapshot in summary.json, before any free allowance.

| Model | Valid / requests | Median / p95 | Input tokens | Listed usage USD |
| --- | ---: | ---: | ---: | ---: |
| laya | 504/504 | 13 / 14 ms | 147,319 | Unmeasured |
| laya-typed | 504/504 | 14 / 16 ms | 184,551 | Unmeasured |
| clef-flash-local | 504/504 | 86 / 146 ms | 213,111 | Unmeasured |
| eikos-4b | 504/504 | 42 / 70 ms | 198,753 | Unmeasured |
| jebadiah-4b-v2 | 504/504 | 39 / 69 ms | 182,655 | Unmeasured |
| kev-0.8b | 504/504 | 49 / 58 ms | 153,783 | Unmeasured |
| kev-4b | 504/504 | 67 / 81 ms | 153,783 | Unmeasured |
| kev-9b | 504/504 | 69 / 106 ms | 153,783 | Unmeasured |
| simple-jev | 504/504 | 161 / 184 ms | 793,935 | Unmeasured |
| decider-4b | 504/504 | 91 / 115 ms | 160,479 | Unmeasured |
| laya-multilingual | 504/504 | 10 / 13 ms | 152,451 | Unmeasured |
| julia-1 | 504/504 | 7 / 8 ms | 147,483 | Unmeasured |
| d3-edge | 504/504 | 13 / 15 ms | 190,215 | Unmeasured |
| gliner2.5-decide | 504/504 | 20 / 40 ms | Unknown (504 responses lack usage) | Unmeasured |
| gliner2.5-multi-decide | 504/504 | 10 / 17 ms | Unknown (504 responses lack usage) | Unmeasured |
