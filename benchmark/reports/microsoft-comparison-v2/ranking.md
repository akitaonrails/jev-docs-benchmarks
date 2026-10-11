# Expanded ranking and size analysis

Descriptive ordering on 168 compact bilingual cases per entrant. Adjacent ranks are not significance claims. GLiNER is a native-interface mapping track; probability metrics are unavailable. Sizes are nominal model/backbone labels, not exact parameter audits.

| Model | Nominal B | Compact EN / PT-BR | Combined compact | All 504 | v1 originals | Median / p95 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| pplx-decider-27b | 27 | 98.8% / 100.0% | 99.4% | 501/504 | 99.2% | 1547 / 2446 ms |
| jev | Unknown | 97.6% / 97.6% | 97.6% | 495/504 | 96.2% | 255 / 304 ms |
| microsoft-decision-1 | 9 | 95.2% / 100.0% | 97.6% | 493/504 | 95.4% | 422 / 551 ms |
| clef | 27 | 97.6% / 94.0% | 95.8% | 486/504 | 94.6% | 302 / 683 ms |
| jebadiah-4b-v2 | 4 | 91.7% / 89.3% | 90.5% | 436/504 | 85.4% | 205 / 485 ms |
| openai-decisions | Unknown | 90.5% / 90.5% | 90.5% | 469/504 | 93.1% | 222 / 274 ms |
| kev-9b | 9 | 92.9% / 83.3% | 88.1% | 440/504 | 87.7% | 561 / 883 ms |
| clef-flash | 9 | 91.7% / 83.3% | 87.5% | 439/504 | 90.8% | 394 / 804 ms |
| clef-flash-local | 9 | 89.3% / 85.7% | 87.5% | 439/504 | 90.8% | 618 / 935 ms |
| decider-4b | 4 | 89.3% / 85.7% | 87.5% | 430/504 | 86.9% | 186 / 480 ms |
| kev-4b | 4 | 88.1% / 86.9% | 87.5% | 411/504 | 82.3% | 246 / 469 ms |
| eikos-4b | 4 | 85.7% / 79.8% | 82.7% | 413/504 | 87.7% | 235 / 514 ms |
| simple-jev | 4 | 77.4% / 71.4% | 74.4% | 383/504 | 85.4% | 1349 / 1687 ms |
| kev-0.8b | 0.8 | 64.3% / 61.9% | 63.1% | 295/504 | 63.1% | 86 / 171 ms |
| gliner2.5-decide | 0.34 | 54.8% / 50.0% | 52.4% | 251/504 | Not run | 208 / 521 ms |
| laya | 0.421 | 44.0% / 41.7% | 42.9% | 197/504 | 43.8% | 41 / 78 ms |
| laya-typed | 0.421 | 50.0% / 35.7% | 42.9% | 204/504 | 43.8% | 43 / 190 ms |
| laya-multilingual | 0.322 | 35.7% / 38.1% | 36.9% | 170/504 | 43.8% | 19 / 45 ms |
| gliner2.5-multi-decide | 0.287 | 32.1% / 35.7% | 33.9% | 175/504 | Not run | 63 / 156 ms |
| julia-1 | 0.1443 | 38.1% / 25.0% | 31.5% | 158/504 | 38.5% | 12 / 25 ms |
| julia-1-cpu | 0.1443 | 38.1% / 25.0% | 31.5% | 158/504 | 36.9% | 71 / 197 ms |

## Size correlations

| Selection | n | Spearman | Pearson(log10 size, accuracy) |
| --- | ---: | ---: | ---: |
| Known-size entrants, deduplicated deployments | 17 | 0.943 | 0.960 |
| SystemOne only, deduplicated deployments | 15 | 0.928 | 0.959 |
| Kev size series | 3 | 1.000 | 0.951 |

### Kev size effects by input condition

| Model | Compact | Worked examples | Distractors | All 504 |
| --- | ---: | ---: | ---: | ---: |
| kev-0.8b | 63.1% | 60.7% | 51.8% | 58.5% |
| kev-4b | 87.5% | 82.7% | 74.4% | 81.5% |
| kev-9b | 88.1% | 92.3% | 81.5% | 87.3% |

Entrants without verified sizes (including Jev and OpenAI Decisions, when present) are excluded. Related checkpoints and shared backbones are dependent observations. These coefficients describe the tested configurations, not a causal scaling law or a random sample of available models. Nominal size bins ignore small head/adapter and exact-backbone differences.

## Task strengths against hosted Jev

Each cell has only 12 authored families. Counts describe exploratory task/language cells, not independent victories.

| Entrant | Cells above Jev | Tied with Jev | Below Jev |
| --- | ---: | ---: | ---: |
| pplx-decider-27b | 3 | 11 | 0 |
| microsoft-decision-1 | 3 | 10 | 1 |
| clef | 1 | 10 | 3 |
| jebadiah-4b-v2 | 0 | 6 | 8 |
| openai-decisions | 3 | 6 | 5 |
| kev-9b | 1 | 2 | 11 |
| clef-flash | 0 | 5 | 9 |
| clef-flash-local | 0 | 4 | 10 |
| decider-4b | 0 | 5 | 9 |
| kev-4b | 0 | 4 | 10 |
| eikos-4b | 0 | 2 | 12 |
| simple-jev | 0 | 1 | 13 |
| kev-0.8b | 0 | 0 | 14 |
| gliner2.5-decide | 0 | 0 | 14 |
| laya | 0 | 0 | 14 |
| laya-typed | 0 | 0 | 14 |
| laya-multilingual | 0 | 0 | 14 |
| gliner2.5-multi-decide | 0 | 0 | 14 |
| julia-1 | 0 | 0 | 14 |
| julia-1-cpu | 0 | 0 | 14 |

## Paired compact differences, clustered by authored family

English and Portuguese observations are kept together when bootstrapping the 84 families. Intervals are exploratory and not adjusted for multiple comparisons.

| Comparison | Difference (points) | Family bootstrap 95% (points) |
| --- | ---: | --- |
| pplx-decider-27b minus jev | +1.8 | [+0.0, +4.2] |
| microsoft-decision-1 minus jev | +0.0 | [-3.0, +3.0] |
| clef minus jev | -1.8 | [-5.4, +1.2] |
| jebadiah-4b-v2 minus jev | -7.1 | [-12.5, -2.4] |
| openai-decisions minus jev | -7.1 | [-13.1, -1.2] |
| kev-9b minus jev | -9.5 | [-16.1, -3.6] |
| clef-flash minus jev | -10.1 | [-16.1, -5.4] |
| clef-flash-local minus jev | -10.1 | [-16.1, -4.8] |
| decider-4b minus jev | -10.1 | [-16.7, -4.2] |
| kev-4b minus jev | -10.1 | [-16.1, -4.2] |
| eikos-4b minus jev | -14.9 | [-22.6, -7.7] |
| simple-jev minus jev | -23.2 | [-31.0, -15.5] |
| kev-0.8b minus jev | -34.5 | [-42.9, -26.2] |
| gliner2.5-decide minus jev | -45.2 | [-54.2, -36.9] |
| laya minus jev | -54.8 | [-63.7, -45.8] |
| laya-typed minus jev | -54.8 | [-63.1, -45.8] |
| laya-multilingual minus jev | -60.7 | [-69.0, -52.4] |
| gliner2.5-multi-decide minus jev | -63.7 | [-72.6, -54.8] |
| julia-1 minus jev | -66.1 | [-73.8, -57.7] |
| julia-1-cpu minus jev | -66.1 | [-74.4, -57.7] |
| kev-4b minus kev-0.8b | +24.4 | [+16.1, +33.3] |
| kev-9b minus kev-4b | +0.6 | [-6.5, +7.1] |
| openai-decisions minus clef | -5.4 | [-11.3, +0.6] |
| openai-decisions minus clef-flash | +3.0 | [-5.4, +10.7] |
| openai-decisions minus jebadiah-4b-v2 | +0.0 | [-6.5, +6.0] |
| pplx-decider-27b minus clef | +3.6 | [+0.6, +7.1] |
| pplx-decider-27b minus openai-decisions | +8.9 | [+3.6, +14.9] |
| pplx-decider-27b minus jebadiah-4b-v2 | +8.9 | [+4.2, +14.3] |
| microsoft-decision-1 minus pplx-decider-27b | -1.8 | [-4.2, +0.0] |
| microsoft-decision-1 minus clef | +1.8 | [-0.6, +4.8] |
| microsoft-decision-1 minus openai-decisions | +7.1 | [+2.4, +11.9] |
| microsoft-decision-1 minus clef-flash | +10.1 | [+4.7, +16.7] |
| microsoft-decision-1 minus kev-9b | +9.5 | [+4.8, +15.5] |
| julia-1-cpu minus julia-1 | +0.0 | [-1.8, +1.8] |
