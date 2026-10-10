# v2 bilingual expansion results

84 authored families, paired translations, three correlated conditions. Compact is the primary language comparison. Task cells have only 12 families; numerical wins are exploratory.

| Model | Compact EN | Compact PT-BR | PT minus EN (paired bootstrap 95%) | Examples EN / PT | Distractors EN / PT |
| --- | ---: | ---: | --- | --- | --- |
| laya | 44.0% | 41.7% | -2.4% [-15.5%, +9.5%] | 36.9% / 35.7% | 39.3% / 36.9% |
| laya-typed | 50.0% | 35.7% | -14.3% [-27.4%, -2.4%] | 44.0% / 36.9% | 44.0% / 32.1% |
| clef-flash-local | 89.3% | 85.7% | -3.6% [-10.7%, +3.6%] | 90.5% / 84.5% | 88.1% / 84.5% |

## Compact tasks: en

| Task | laya | laya-typed | clef-flash-local |
| --- | ---: | ---: | ---: |
| sentiment | 33.3% | 41.7% | 100.0% |
| intent | 58.3% | 75.0% | 75.0% |
| entailment | 58.3% | 50.0% | 83.3% |
| retrieval | 41.7% | 50.0% | 91.7% |
| data_handling | 33.3% | 33.3% | 83.3% |
| current_status | 41.7% | 41.7% | 100.0% |
| threshold_policy | 41.7% | 58.3% | 91.7% |

## Compact tasks: pt-BR

| Task | laya | laya-typed | clef-flash-local |
| --- | ---: | ---: | ---: |
| sentiment | 33.3% | 25.0% | 100.0% |
| intent | 41.7% | 33.3% | 91.7% |
| entailment | 33.3% | 33.3% | 91.7% |
| retrieval | 41.7% | 25.0% | 75.0% |
| data_handling | 66.7% | 25.0% | 75.0% |
| current_status | 33.3% | 66.7% | 83.3% |
| threshold_policy | 41.7% | 41.7% | 83.3% |

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

## Latency and current hosted usage value

All 504 requests/model; conditions have different lengths. Local operating cost is unmeasured. Hosted values use the dated 10 October pricing snapshot, before any free allowance.

| Model | Valid / requests | Median / p95 | Input tokens | Listed usage USD |
| --- | ---: | ---: | ---: | ---: |
| laya | 504/504 | 41 / 78 ms | 147,319 | Unmeasured |
| laya-typed | 504/504 | 43 / 190 ms | 184,551 | Unmeasured |
| clef-flash-local | 504/504 | 618 / 935 ms | 213,111 | Unmeasured |
