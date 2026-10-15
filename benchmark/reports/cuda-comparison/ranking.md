# CUDA technical ranking and cost-benefit interpretation

Ranked by compact bilingual accuracy, then total correct across the three v2 conditions. This is a ranking of the 15 configurations that fit the RTX 5090 at reference precision. Perplexity 27B and d3 flagship remain capacity exclusions, not low-scoring entries.

| Rank | Model | Compact /168 | All conditions /504 | CUDA median / p95 ms | ROCm / CUDA median ratio |
| ---: | --- | ---: | ---: | ---: | ---: |
| 1 | jebadiah-4b-v2 | 152 (90.5%) | 436 | 39.1 / 68.9 | 5.26× |
| 2 | kev-9b | 148 (88.1%) | 441 | 69.4 / 106.4 | 8.07× |
| 3 | clef-flash-local | 147 (87.5%) | 440 | 86.1 / 146.2 | 7.18× |
| 4 | decider-4b | 147 (87.5%) | 431 | 90.9 / 114.8 | 2.05× |
| 5 | kev-4b | 147 (87.5%) | 411 | 66.6 / 81.2 | 3.69× |
| 6 | eikos-4b | 139 (82.7%) | 412 | 42.3 / 69.6 | 5.54× |
| 7 | simple-jev | 126 (75.0%) | 383 | 160.6 / 184.1 | 8.41× |
| 8 | kev-0.8b | 104 (61.9%) | 295 | 48.6 / 57.6 | 1.78× |
| 9 | d3-edge | 102 (60.7%) | 283 | 12.6 / 15.1 | 3.60× |
| 10 | gliner2.5-decide | 88 (52.4%) | 251 | 20.1 / 40.2 | 10.32× |
| 11 | laya | 73 (43.5%) | 198 | 12.8 / 13.7 | 3.19× |
| 12 | laya-typed | 70 (41.7%) | 202 | 13.9 / 16.2 | 3.09× |
| 13 | laya-multilingual | 61 (36.3%) | 169 | 10.2 / 12.8 | 1.81× |
| 14 | gliner2.5-multi-decide | 57 (33.9%) | 175 | 10.4 / 17.5 | 6.03× |
| 15 | julia-1 | 52 (31.0%) | 157 | 7.3 / 8.1 | 1.70× |

## How to use the ranking

- **Jebadiah 4B v2:** first compact-task candidate on this GPU: 152/168 and 39 ms median. It falls to 136/168 on distractors, so its lead is conditional.
- **Kev 9B:** highest total v2 count among these CUDA entrants, 441/504, helped by 155/168 on the examples condition. Median is 69 ms; compact PT-BR is 71/84 versus Jebadiah’s 75/84.
- **Clef Flash local:** 440/504 overall, 146/168 on distractors, and the strongest original v1 policy score among these CUDA entrants, 118/130. Its median is 86 ms.
- **Small models:** Julia, Laya variants and D3 Edge are quicker in absolute time, but their lower scores on this difficult mix remain. Their size advantage can matter for narrow or constrained deployments; this GPU test does not establish mobile/CPU performance.

## Price and practical value

No hosted inference calls were made. CUDA electricity, whole-machine power, hardware amortization and operating effort were not priced. Therefore these results establish latency/quality tradeoffs, not a dollar-cost winner.

The [hosted comparison](../microsoft-comparison-v2/costs.md) still uses its dated 11 October rates and measured token usage. Microsoft remains that report’s paid workload-cost candidate; those services were not rerun or repriced here. CUDA speed improvements do not change that bill.

The homelab can hold the roughly 49 GiB BF16 27B models that scored 501/504. The 5090 cannot. A quantized, offloaded or multi-GPU version would need its own named configuration and new accuracy checks.

[Full paired tables](results.md) · [Analysis and limitations](../../../docs/cuda-rocm-comparison.md) · [Reproduction](../../cuda/README.md)
