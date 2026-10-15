# RTX 5090 CUDA versus gfx1151 ROCm

Same pinned checkpoint and request per pair. End-to-end serial warm-request latency; different GPU, CPU, network and runtime builds. Ratios are deployment comparisons, not an isolated backend effect.

| Model | Compact CUDA / ROCm | All v2 CUDA / ROCm | Changed v2 labels | CUDA median / p95 ms | ROCm median / p95 ms | Median ratio ROCm / CUDA |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| eikos-4b | 139/168 / 139/168 | 412/504 / 413/504 | 2 | 42.3 / 69.6 | 234.6 / 514.5 | 5.54× |
| jebadiah-4b-v2 | 152/168 / 152/168 | 436/504 / 436/504 | 3 | 39.1 / 68.9 | 205.4 / 485.1 | 5.26× |
| kev-0.8b | 104/168 / 106/168 | 295/504 / 295/504 | 6 | 48.6 / 57.6 | 86.5 / 171.2 | 1.78× |
| kev-4b | 147/168 / 147/168 | 411/504 / 411/504 | 2 | 66.6 / 81.2 | 246.1 / 468.8 | 3.69× |
| kev-9b | 148/168 / 148/168 | 441/504 / 440/504 | 3 | 69.4 / 106.4 | 560.6 / 883.0 | 8.07× |
| laya | 73/168 / 72/168 | 198/504 / 197/504 | 6 | 12.8 / 13.7 | 40.7 / 78.1 | 3.19× |
| laya-typed | 70/168 / 72/168 | 202/504 / 204/504 | 6 | 13.9 / 16.2 | 43.1 / 190.2 | 3.09× |
| laya-multilingual | 61/168 / 62/168 | 169/504 / 170/504 | 6 | 10.2 / 12.8 | 18.5 / 44.9 | 1.81× |
| gliner2.5-decide | 88/168 / 88/168 | 251/504 / 251/504 | 0 | 20.1 / 40.2 | 208.0 / 521.5 | 10.32× |
| gliner2.5-multi-decide | 57/168 / 57/168 | 175/504 / 175/504 | 0 | 10.4 / 17.5 | 63.0 / 156.3 | 6.03× |
| simple-jev | 126/168 / 125/168 | 383/504 / 383/504 | 11 | 160.6 / 184.1 | 1349.5 / 1687.7 | 8.41× |
| clef-flash-local | 147/168 / 147/168 | 440/504 / 439/504 | 1 | 86.1 / 146.2 | 618.1 / 934.6 | 7.18× |
| decider-4b | 147/168 / 147/168 | 431/504 / 430/504 | 3 | 90.9 / 114.8 | 186.3 / 480.1 | 2.05× |
| julia-1 | 52/168 / 53/168 | 157/504 / 158/504 | 12 | 7.3 / 8.1 | 12.4 / 25.1 | 1.70× |
| d3-edge | 102/168 / 102/168 | 283/504 / 287/504 | 8 | 12.6 / 15.1 | 45.4 / 101.9 | 3.60× |

## Language and prompt conditions

Counts are CUDA / ROCm. EN and PT-BR columns use the 84 compact cases per language; examples/distractors each contain 168 cases.

| Model | EN | PT-BR | Examples | Distractors |
| --- | ---: | ---: | ---: | ---: |
| eikos-4b | 72 / 72 | 67 / 67 | 135 / 136 | 138 / 138 |
| jebadiah-4b-v2 | 77 / 77 | 75 / 75 | 148 / 148 | 136 / 136 |
| kev-0.8b | 54 / 54 | 50 / 52 | 104 / 102 | 87 / 87 |
| kev-4b | 74 / 74 | 73 / 73 | 139 / 139 | 125 / 125 |
| kev-9b | 77 / 78 | 71 / 70 | 155 / 155 | 138 / 137 |
| laya | 38 / 37 | 35 / 35 | 62 / 61 | 63 / 64 |
| laya-typed | 40 / 42 | 30 / 30 | 68 / 68 | 64 / 64 |
| laya-multilingual | 29 / 30 | 32 / 32 | 57 / 58 | 51 / 50 |
| gliner2.5-decide | 46 / 46 | 42 / 42 | 75 / 75 | 88 / 88 |
| gliner2.5-multi-decide | 27 / 27 | 30 / 30 | 56 / 56 | 62 / 62 |
| simple-jev | 65 / 65 | 61 / 60 | 137 / 136 | 120 / 122 |
| clef-flash-local | 75 / 75 | 72 / 72 | 147 / 147 | 146 / 145 |
| decider-4b | 75 / 75 | 72 / 72 | 143 / 143 | 141 / 140 |
| julia-1 | 31 / 32 | 21 / 21 | 48 / 48 | 57 / 57 |
| d3-edge | 58 / 57 | 44 / 45 | 84 / 86 | 97 / 99 |

## Original policy suite and uncertainty

Counts and Noul MAE are CUDA / ROCm. Noul probes have stated event-probability targets; lower MAE is better.

| Model | Original /130 | All variants /520 | Changed labels | Choice probe MAE | Noul probe MAE |
| --- | ---: | ---: | ---: | ---: | ---: |
| eikos-4b | 114 / 114 | 450 / 452 | 2 | 0.213 / 0.213 | 0.552 / 0.554 |
| jebadiah-4b-v2 | 111 / 111 | 436 / 436 | 0 | 0.192 / 0.192 | 0.565 / 0.563 |
| kev-0.8b | 81 / 82 | 327 / 329 | 2 | 0.120 / 0.121 | 0.302 / 0.300 |
| kev-4b | 107 / 107 | 430 / 430 | 0 | 0.093 / 0.093 | 0.633 / 0.633 |
| kev-9b | 114 / 114 | 446 / 445 | 1 | 0.050 / 0.051 | 0.380 / 0.381 |
| laya | 59 / 57 | 204 / 200 | 5 | 0.212 / 0.211 | 0.435 / 0.435 |
| laya-typed | 58 / 57 | 201 / 200 | 7 | 0.072 / 0.072 | 0.189 / 0.190 |
| laya-multilingual | 57 / 57 | 205 / 205 | 3 | 0.182 / 0.180 | 0.267 / 0.270 |
| simple-jev | 112 / 111 | 432 / 430 | 2 | 0.248 / 0.247 | 0.207 / 0.200 |
| clef-flash-local | 118 / 118 | 463 / 463 | 2 | 0.143 / 0.142 | 0.522 / 0.522 |
| decider-4b | 113 / 113 | 448 / 447 | 3 | 0.173 / 0.172 | 0.187 / 0.185 |
| julia-1 | 49 / 50 | 184 / 182 | 14 | 0.217 / 0.218 | 0.297 / 0.296 |
| d3-edge | 84 / 85 | 347 / 347 | 6 | 0.286 / 0.285 | 0.266 / 0.266 |

## Probability output differences

Absolute changes per option across the 504 v2 cases; these are output differences, not calibration scores. GLiNER supplies native confidence, not a distribution.

| Model | Mean absolute difference | Maximum absolute difference |
| --- | ---: | ---: |
| eikos-4b | 0.003885 | 0.087718 |
| jebadiah-4b-v2 | 0.002210 | 0.061783 |
| kev-0.8b | 0.002779 | 0.022540 |
| kev-4b | 0.002344 | 0.026600 |
| kev-9b | 0.002473 | 0.059600 |
| laya | 0.003380 | 0.055100 |
| laya-typed | 0.001568 | 0.014900 |
| laya-multilingual | 0.003518 | 0.037355 |
| simple-jev | 0.007272 | 0.114274 |
| clef-flash-local | 0.001937 | 0.042100 |
| decider-4b | 0.002135 | 0.047400 |
| julia-1 | 0.013639 | 0.261031 |
| d3-edge | 0.003407 | 0.048349 |

All request hashes are checked before pairing. See `paired.json` for changed case IDs, available token-usage comparisons and setup-run repeat agreement. Missing usage telemetry is not evidence of lossless encoding. Existing model-specific truncation is retained and reported by the standard scorers.

The 27B d3 and Perplexity checkpoints do not fit this 32 GiB GPU at reference BF16 precision. Hosted-only models and the Julia CPU configuration are outside this paired GPU track. Local operating cost remains unmeasured.
