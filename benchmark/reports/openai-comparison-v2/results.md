# v2 bilingual expansion results

84 authored families, paired translations, three correlated conditions. Compact is the primary language comparison. Task cells have only 12 families; numerical wins are exploratory.

| Model | Compact EN | Compact PT-BR | PT minus EN (paired bootstrap 95%) | Examples EN / PT | Distractors EN / PT |
| --- | ---: | ---: | --- | --- | --- |
| jev | 97.6% | 97.6% | +0.0% [-4.8%, +4.8%] | 97.6% / 98.8% | 98.8% / 98.8% |
| clef | 97.6% | 94.0% | -3.6% [-7.2%, +0.0%] | 97.6% / 97.6% | 95.2% / 96.4% |
| clef-flash | 91.7% | 83.3% | -8.3% [-15.5%, -1.2%] | 91.7% / 84.5% | 90.5% / 81.0% |
| laya | 44.0% | 41.7% | -2.4% [-15.5%, +9.5%] | 36.9% / 35.7% | 39.3% / 36.9% |
| laya-typed | 50.0% | 35.7% | -14.3% [-27.4%, -2.4%] | 44.0% / 36.9% | 44.0% / 32.1% |
| clef-flash-local | 89.3% | 85.7% | -3.6% [-10.7%, +3.6%] | 90.5% / 84.5% | 88.1% / 84.5% |
| openai-decisions | 90.5% | 90.5% | +0.0% [-6.0%, +6.0%] | 91.7% / 95.2% | 95.2% / 95.2% |
| decider-4b | 89.3% | 85.7% | -3.6% [-10.7%, +3.6%] | 86.9% / 83.3% | 84.5% / 82.1% |
| eikos-4b | 85.7% | 79.8% | -6.0% [-14.3%, +1.2%] | 81.0% / 81.0% | 84.5% / 79.8% |
| gliner2.5-decide | 54.8% | 50.0% | -4.8% [-15.5%, +6.0%] | 47.6% / 41.7% | 59.5% / 45.2% |
| gliner2.5-multi-decide | 32.1% | 35.7% | +3.6% [-6.0%, +13.1%] | 27.4% / 39.3% | 34.5% / 39.3% |
| jebadiah-4b-v2 | 91.7% | 89.3% | -2.4% [-9.5%, +4.8%] | 90.5% / 85.7% | 85.7% / 76.2% |
| kev-0.8b | 64.3% | 61.9% | -2.4% [-14.3%, +9.5%] | 63.1% / 58.3% | 53.6% / 50.0% |
| kev-4b | 88.1% | 86.9% | -1.2% [-9.5%, +6.0%] | 84.5% / 81.0% | 78.6% / 70.2% |
| kev-9b | 92.9% | 83.3% | -9.5% [-16.7%, -3.6%] | 92.9% / 91.7% | 88.1% / 75.0% |
| laya-multilingual | 35.7% | 38.1% | +2.4% [-9.5%, +13.1%] | 31.0% / 38.1% | 26.2% / 33.3% |
| simple-jev | 77.4% | 71.4% | -6.0% [-15.5%, +3.6%] | 81.0% / 81.0% | 78.6% / 66.7% |

## Compact tasks: en

| Task | jev | clef | clef-flash | laya | laya-typed | clef-flash-local | openai-decisions | decider-4b | eikos-4b | gliner2.5-decide | gliner2.5-multi-decide | jebadiah-4b-v2 | kev-0.8b | kev-4b | kev-9b | laya-multilingual | simple-jev |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| sentiment | 100.0% | 100.0% | 100.0% | 33.3% | 41.7% | 100.0% | 75.0% | 100.0% | 83.3% | 25.0% | 25.0% | 91.7% | 83.3% | 100.0% | 100.0% | 16.7% | 75.0% |
| intent | 100.0% | 100.0% | 83.3% | 58.3% | 75.0% | 75.0% | 100.0% | 100.0% | 100.0% | 75.0% | 33.3% | 100.0% | 58.3% | 91.7% | 91.7% | 41.7% | 91.7% |
| entailment | 100.0% | 100.0% | 83.3% | 58.3% | 50.0% | 83.3% | 100.0% | 75.0% | 91.7% | 50.0% | 33.3% | 100.0% | 83.3% | 91.7% | 91.7% | 41.7% | 75.0% |
| retrieval | 91.7% | 91.7% | 91.7% | 41.7% | 50.0% | 91.7% | 100.0% | 91.7% | 91.7% | 41.7% | 33.3% | 91.7% | 50.0% | 83.3% | 83.3% | 41.7% | 91.7% |
| data_handling | 91.7% | 100.0% | 91.7% | 33.3% | 33.3% | 83.3% | 100.0% | 75.0% | 75.0% | 58.3% | 41.7% | 83.3% | 66.7% | 75.0% | 100.0% | 33.3% | 66.7% |
| current_status | 100.0% | 100.0% | 100.0% | 41.7% | 41.7% | 100.0% | 91.7% | 100.0% | 91.7% | 83.3% | 41.7% | 100.0% | 58.3% | 100.0% | 100.0% | 50.0% | 91.7% |
| threshold_policy | 100.0% | 91.7% | 91.7% | 41.7% | 58.3% | 91.7% | 66.7% | 83.3% | 66.7% | 50.0% | 16.7% | 75.0% | 50.0% | 75.0% | 83.3% | 25.0% | 50.0% |

## Compact tasks: pt-BR

| Task | jev | clef | clef-flash | laya | laya-typed | clef-flash-local | openai-decisions | decider-4b | eikos-4b | gliner2.5-decide | gliner2.5-multi-decide | jebadiah-4b-v2 | kev-0.8b | kev-4b | kev-9b | laya-multilingual | simple-jev |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| sentiment | 100.0% | 100.0% | 100.0% | 33.3% | 25.0% | 100.0% | 83.3% | 100.0% | 75.0% | 58.3% | 0.0% | 91.7% | 58.3% | 100.0% | 91.7% | 25.0% | 83.3% |
| intent | 100.0% | 91.7% | 75.0% | 41.7% | 33.3% | 91.7% | 100.0% | 83.3% | 91.7% | 58.3% | 50.0% | 100.0% | 75.0% | 83.3% | 75.0% | 50.0% | 91.7% |
| entailment | 100.0% | 100.0% | 91.7% | 33.3% | 33.3% | 91.7% | 100.0% | 83.3% | 91.7% | 33.3% | 41.7% | 91.7% | 83.3% | 100.0% | 91.7% | 41.7% | 58.3% |
| retrieval | 91.7% | 91.7% | 83.3% | 41.7% | 25.0% | 75.0% | 91.7% | 83.3% | 83.3% | 50.0% | 25.0% | 83.3% | 33.3% | 66.7% | 75.0% | 50.0% | 58.3% |
| data_handling | 91.7% | 91.7% | 66.7% | 66.7% | 25.0% | 75.0% | 100.0% | 83.3% | 83.3% | 50.0% | 50.0% | 91.7% | 58.3% | 83.3% | 75.0% | 25.0% | 58.3% |
| current_status | 100.0% | 100.0% | 83.3% | 33.3% | 66.7% | 83.3% | 100.0% | 91.7% | 75.0% | 66.7% | 50.0% | 91.7% | 58.3% | 91.7% | 91.7% | 41.7% | 91.7% |
| threshold_policy | 100.0% | 83.3% | 83.3% | 41.7% | 41.7% | 83.3% | 58.3% | 75.0% | 58.3% | 33.3% | 33.3% | 75.0% | 66.7% | 83.3% | 83.3% | 33.3% | 58.3% |

## Input truncation

| Model | Condition | Reported truncated / valid | Missing truncation telemetry |
| --- | --- | ---: | ---: |
| jev | compact | 0/168 | 168 |
| jev | examples | 0/168 | 168 |
| jev | distractors | 0/168 | 168 |
| clef | compact | 0/168 | 168 |
| clef | examples | 0/168 | 168 |
| clef | distractors | 0/168 | 168 |
| clef-flash | compact | 0/168 | 168 |
| clef-flash | examples | 0/168 | 168 |
| clef-flash | distractors | 0/168 | 168 |
| laya | compact | 0/168 | 0 |
| laya | examples | 0/168 | 0 |
| laya | distractors | 84/168 | 0 |
| laya-typed | compact | 0/168 | 0 |
| laya-typed | examples | 0/168 | 0 |
| laya-typed | distractors | 0/168 | 0 |
| clef-flash-local | compact | 0/168 | 168 |
| clef-flash-local | examples | 0/168 | 168 |
| clef-flash-local | distractors | 0/168 | 168 |
| openai-decisions | compact | 0/168 | 168 |
| openai-decisions | examples | 0/168 | 168 |
| openai-decisions | distractors | 0/168 | 168 |
| decider-4b | compact | 0/168 | 168 |
| decider-4b | examples | 0/168 | 168 |
| decider-4b | distractors | 0/168 | 168 |
| eikos-4b | compact | 0/168 | 168 |
| eikos-4b | examples | 0/168 | 168 |
| eikos-4b | distractors | 0/168 | 168 |
| gliner2.5-decide | compact | 0/168 | 168 |
| gliner2.5-decide | examples | 0/168 | 168 |
| gliner2.5-decide | distractors | 0/168 | 168 |
| gliner2.5-multi-decide | compact | 0/168 | 168 |
| gliner2.5-multi-decide | examples | 0/168 | 168 |
| gliner2.5-multi-decide | distractors | 0/168 | 168 |
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
| laya-multilingual | compact | 0/168 | 0 |
| laya-multilingual | examples | 0/168 | 0 |
| laya-multilingual | distractors | 0/168 | 0 |
| simple-jev | compact | 0/168 | 168 |
| simple-jev | examples | 0/168 | 168 |
| simple-jev | distractors | 0/168 | 168 |

## Latency and current hosted usage value

All 504 requests/model; conditions have different lengths. Local operating cost is unmeasured. Hosted values use the dated pricing snapshot in summary.json, before any free allowance.

| Model | Valid / requests | Median / p95 | Input tokens | Listed usage USD |
| --- | ---: | ---: | ---: | ---: |
| jev | 504/504 | 255 / 304 ms | 312,237 | 0.013113954 |
| clef | 504/504 | 302 / 683 ms | 213,111 | 0.05114664 |
| clef-flash | 504/504 | 394 / 804 ms | 213,111 | 0.008098218 |
| laya | 504/504 | 41 / 78 ms | 147,319 | Unmeasured |
| laya-typed | 504/504 | 43 / 190 ms | 184,551 | Unmeasured |
| clef-flash-local | 504/504 | 618 / 935 ms | 213,111 | Unmeasured |
| openai-decisions | 504/504 | 222 / 274 ms | 195,963 | 0.0195963 |
| decider-4b | 504/504 | 186 / 480 ms | 160,479 | Unmeasured |
| eikos-4b | 504/504 | 235 / 514 ms | 198,753 | Unmeasured |
| gliner2.5-decide | 504/504 | 208 / 521 ms | Unknown (504 responses lack usage) | Unmeasured |
| gliner2.5-multi-decide | 504/504 | 63 / 156 ms | Unknown (504 responses lack usage) | Unmeasured |
| jebadiah-4b-v2 | 504/504 | 205 / 485 ms | 182,655 | Unmeasured |
| kev-0.8b | 504/504 | 86 / 171 ms | 153,783 | Unmeasured |
| kev-4b | 504/504 | 246 / 469 ms | 153,783 | Unmeasured |
| kev-9b | 504/504 | 561 / 883 ms | 153,783 | Unmeasured |
| laya-multilingual | 504/504 | 19 / 45 ms | 152,451 | Unmeasured |
| simple-jev | 504/504 | 1349 / 1687 ms | 793,935 | Unmeasured |
