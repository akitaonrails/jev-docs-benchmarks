# RTX 5090 CUDA versus gfx1151 ROCm

Same pinned checkpoint and request per pair. End-to-end serial warm-request latency; different GPU, CPU, network and runtime builds. Ratios are deployment comparisons, not an isolated backend effect.

| Model | Compact CUDA / ROCm | All v2 CUDA / ROCm | Changed v2 labels | CUDA median / p95 ms | ROCm median / p95 ms | Median ratio ROCm / CUDA |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| eikos-4b | 139/168 / 139/168 | 412/504 / 413/504 | 2 | 42.1 / 69.2 | 234.6 / 514.5 | 5.58× |
| jebadiah-4b-v2 | 152/168 / 152/168 | 436/504 / 436/504 | 3 | 39.1 / 68.7 | 205.4 / 485.1 | 5.25× |
| laya | 73/168 / 72/168 | 198/504 / 197/504 | 6 | 13.4 / 14.9 | 40.7 / 78.1 | 3.05× |
| laya-typed | 70/168 / 72/168 | 202/504 / 204/504 | 6 | 13.7 / 15.7 | 43.1 / 190.2 | 3.14× |
| julia-1 | 52/168 / 53/168 | 157/504 / 158/504 | 12 | 8.0 / 9.5 | 12.4 / 25.1 | 1.55× |
| d3-edge | 102/168 / 102/168 | 283/504 / 287/504 | 8 | 13.3 / 16.2 | 45.4 / 101.9 | 3.41× |
