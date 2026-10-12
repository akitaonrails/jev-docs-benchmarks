# vLLM Semantic Router Decision 3.0

Verified 12 October 2026 against the official Hugging Face repositories. The six
checkpoints are released and downloadable: d3, flash, mini, nano, lite and edge.
The user selected **only the flagship d3 and smallest d3-edge** for this benchmark.
The serving integration is documented on the development channel; availability of
the weights does not mean every integration is in a stable router release.

| Selected model | Published size label | Card's parameter total | Local runtime |
| --- | ---: | ---: | --- |
| d3 | 27B | 26.09B, including 0.46B vision encoder | Native BF16 with strict direct GPU loading |
| d3-edge | 0.6B | 0.59B, including 0.10B vision encoder | Native BF16 Transformers loading |

These Apache-2.0 checkpoints are Qwen-derived decision models. They score fixed
options without producing free-form answers. Native questions include choice,
Boolean/Noul and ordinal score. Text or JSON may be supplemented with images and
video. Our frozen suites evaluate text/JSON choice and Noul only; image/video and
ordinal capabilities are outside this comparison.

The official cards identify d3 as the flagship. Its published public Decision Index
0.3 score is 65.45 versus Edge's 28.82. These are publisher evaluations, with a
different dataset and scoring method from this repository. They motivate testing
the two extremes; they are not substituted into our ranking.

## Our measured result

Both selected models completed 1,048 valid requests each. D3 scores 99.4% compact
bilingual and 129/130 original policy cases, matching all Perplexity classification
labels. Edge scores 60.7% compact and 85/130 originals, at much lower memory and
latency. [Complete analysis](../benchmark/reports/decision3-comparison-v2/analysis.md).

## Homelab access

Both are installed on `192.168.0.90` in isolated Docker, alongside the earlier
benchmark services, and are loaded only for a run. d3 uses port 11450 and Edge
11451, both `POST /v1/systemone`; readiness is `GET /health`. The services have no
external API key or hosted token tariff. Electricity, hardware and operations
remain unmeasured and must not be described as free.

The local site cap is 8,192 tokens and rejects overflow. All frozen benchmark
requests independently encode to 146–728 tokens. Pinned snapshots and a full
manifest hash verification make these checks reproducible. Full d3 uses a strict
shard loader because the standard loading path spikes host memory. It preserves
native input formatting, weight dtypes, readout and temperature. ROCm uses reference
kernels; the publisher's MI325X speed claims do not predict this homelab's latency.

[Protocol, pins and reproduction](../benchmark/decision3/README.md),
[upstream manifests/configuration](../benchmark/decision3/upstream.json).

## Primary sources

- [Official collection](https://huggingface.co/collections/vllm-sr/decision-30)
- [d3 card and code](https://huggingface.co/vllm-sr/d3)
- [d3-edge card and code](https://huggingface.co/vllm-sr/d3-edge)
- [Publisher's Semantic Router project](https://github.com/vllm-project/semantic-router)
