# Jev and open decision-model benchmarks

**Measure how reliably decision models apply supplied rules, how their probabilities
behave, and what those decisions cost.** Compare TypeSafe Jev, Microsoft Decision-1 and OpenAI Decisions with hosted and local
Clef/Clef-flash, Laya, Kev, Eikos, Jebadiah, Mapika Decider, Simple-Jev and GLiNER,
using frozen inputs, inspectable expected answers, raw
response archives, and reproducible scoring.

The goal is to find **where each model works, where it fails, and whether its quality,
latency and operating cost justify using it** for classification, support routing,
retrieval and similar tasks. Schema-valid JSON is not evidence that a decision is correct.

This repository combines source-based research with our own synthetic experiments.
It is not an official vendor benchmark, a production accuracy guarantee, or a demonstration
that one model is universally best. See [methodology and limitations](#methodology-and-limitations).

## Start here

- **Latest results:** [Microsoft/OpenRouter comparison](benchmark/reports/microsoft-comparison-v2/analysis.md),
  [21-configuration ranking](benchmark/reports/microsoft-comparison-v2/ranking.md),
  [task/language tables](benchmark/reports/microsoft-comparison-v2/results.md), and
  [actual reported usage and price comparison](benchmark/reports/microsoft-comparison-v2/costs.md).
- **Latest hosted setup:** [Microsoft access and reproduction](benchmark/microsoft/README.md).
- **Previous quality leader addition:** [Perplexity 27B comparison](benchmark/reports/perplexity-comparison-v2/analysis.md).
- **Previous local expansion:** [16-configuration analysis](benchmark/reports/next-wave-comparison-v2/analysis.md).
- **Local deployment:** [Perplexity runtime and setup](benchmark/perplexity/README.md).
- **First six models:** [initial English / PT-BR analysis](benchmark/reports/comparison-v2/analysis.md).
- **Original policy suite:** [hosted versus local analysis](benchmark/reports/comparison-v1/analysis.md)
  and [complete six-model tables](benchmark/reports/comparison-v1/results.md).
- **Which is worth using?** [Technical and cost-benefit ranking](docs/cost-benefit-ranking.md).
- **Run it yourself:** [setup and reproduction guide](docs/setup.md), including the actual
  AMD homelab runtime and its custom base-image dependency.
- **Research:** [business summary](docs/business-summary.md), [mechanics and prior art](docs/research.md),
  [alternatives](docs/alternatives.md), [use cases](docs/use-cases.md),
  [Paulo Câmara article analysis](docs/paulo-camara-article.md).
- **Open-model coverage:** [researched shortlist](docs/next-models.md) and
  [next-wave protocol and reproduction](benchmark/next-wave/README.md).
- **Broader coverage:** [paired English / PT-BR expansion](benchmark/expansion-v2/README.md).

## Microsoft Decision-1: tied hosted quality, lowest measured API cost

**1,048 new valid responses.** Microsoft ties Jev at **97.6% compact bilingual
accuracy**, behind local Perplexity's **99.4%**. It scores **80/84 English**, **84/84
PT-BR**, **493/504 across all conditions**, and **124/130 original policy cases**.

| Entrant | Compact bilingual | USD / 1,000 compact calls |
| --- | ---: | ---: |
| Perplexity Decider 27B, local | 99.4% | Local cost unmeasured |
| **Microsoft Decision-1, OpenRouter** | **97.6%** | **$0.00645** |
| Jev | 97.6% | $0.01916 |
| Clef | 95.8% | $0.06309 |
| OpenAI Decisions | 90.5% | $0.02331 |
| Jebadiah 4B v2, local | 90.5% | Local cost unmeasured |
| Clef-flash | 87.5% | $0.00999 |

Microsoft becomes the first paid hosted candidate to evaluate for this workload:
about **66% cheaper than Jev** by reported compact usage. Jev remains faster
(255/304 ms median/p95 versus 422/551) and slightly stronger across all conditions.
The compact tie does not imply identical errors. Microsoft still mishandles some
threshold rules and known-random probability probes. Perplexity retains the highest
local quality point estimate; small model resource constraints remain relevant.

Successful usage including the smoke totals **$0.011135376**. Ten v2 HTTP 429
attempts recover on retry; any separate retry charge and account fees are unverified.
Cloudflare allowances and unmeasured local costs qualify the price comparison.
[Analysis](benchmark/reports/microsoft-comparison-v2/analysis.md),
[costs](benchmark/reports/microsoft-comparison-v2/costs.md),
[setup](benchmark/microsoft/README.md).

**The following sections retain the results and recommendations of earlier stages.**

## Perplexity Decider 1.1 27B: an open model leads this suite

**99.4% compact bilingual accuracy (167/168)** and **501/504 overall**. Perplexity
scores every PT-BR case correctly and misses one English retrieval family across
all three conditions. It also scores **129/130 original policy cases**, rising to
127/127 after the same existing disputed-family exclusions used for every model. Jev scores 97.6% compact; Clef 95.8%; OpenAI and Jebadiah 90.5%.
The small observed lead over Jev does not establish general superiority.

This local BF16 deployment needs roughly 49 GiB of weights plus runtime memory,
and measures **1,547/2,446 ms median/p95** on AMD ROCm with fallback kernels.
It is the strongest measured local quality candidate here; Jev remains the leading
hosted quality/list-price choice. Local total cost is unmeasured. Its Boolean
probabilities still fail known-random-outcome probes, so high classification
accuracy does not establish general probability reliability.
[Full analysis and limitations](benchmark/reports/perplexity-comparison-v2/analysis.md),
[reproduction](benchmark/perplexity/README.md).

## Julia-1: GPU and CPU results

**2,096 new scored requests, all valid and untruncated.** At this earlier stage the comparison had
19 bilingual configurations and 17 original-policy configurations. Julia's 144.3M
checkpoint scores **31.5% compact bilingual accuracy** on both GPU and CPU, close
to the suite's **31.0% uniform-random baseline**. GPU median/p95 is **12/25 ms**;
four-thread CPU is **71/197 ms**. Low resource requirements and speed are useful,
but these results do not support autonomous difficult policy decisions.

Before the Perplexity addition, Jev (**97.6%**) and Clef (**95.8%**) led, followed by the OpenAI/Jebadiah
compact tie (**90.5%**). No new hosted charges; local compute cost is unmeasured.
[Analysis, cost-benefit and limitations](benchmark/reports/julia-comparison-v2/analysis.md),
[reproduction protocol](benchmark/julia/README.md).

## OpenAI Decisions: native API comparison

**1,048 new scored requests, all valid, no retries.** At this earlier stage the comparison contained
17 bilingual configurations and 15 original-policy configurations. OpenAI uses
`gpt-6-luna` through the native Decisions endpoint, with the same frozen rules,
option descriptions and evidence. The new usage cost is **$0.03475**, including
the successful independent smoke test; the $20 account deposit is prepaid credit.

| Model | Compact EN + PT-BR | All three v2 conditions | Listed USD / 1,000 compact calls |
| --- | ---: | ---: | ---: |
| Jev | 97.6% | 98.2% | $0.01916 |
| Clef | 95.8% | 96.4% | $0.06309 |
| **OpenAI Decisions** | **90.5%** | **93.1%** | **$0.02331** |
| Jebadiah 4B v2, local | 90.5% | 86.5% | Local cost unmeasured |
| Clef-flash, hosted | 87.5% | 87.1% | $0.00999 |

OpenAI has the lowest observed hosted v2 median/p95 latency (**222/274 ms**), but
the timed runs occurred on different dates. Jev retains the stronger measured
quality/price balance. OpenAI's predicate probabilities preserve known random-event
uncertainty well, while its choice probabilities remain biased on those probes.
Exact-threshold rules and the critical data-loss support ticket still expose errors.

[Full analysis and limitations](benchmark/reports/openai-comparison-v2/analysis.md),
[v1 policy tables](benchmark/reports/openai-comparison-v1/results.md),
[native adapter and reproduction](benchmark/openai-decisions/README.md).

## Earlier expansion: ten additional local configurations

**9,392 new scored responses, all valid, zero retries.** Together with the first
runs, that stage contained 16 bilingual configurations and 14 policy-suite
configurations. The new inference ran sequentially on the AMD homelab in about
55 minutes; all benchmark containers are stopped afterward.

The observations in this table describe that earlier sixteen-configuration stage.

| Configuration | Compact bilingual accuracy | Main observation |
| --- | ---: | --- |
| Jev | 97.6% | Highest point estimate; full hosted Clef is close at 95.8%. |
| Jebadiah 4B v2 | 90.5% | Highest tested local compact point estimate. |
| Kev 9B | 88.1% | Larger gains with examples/distractors than compact inputs. |
| Mapika Decider 4B / Kev 4B / Flash deployments | 87.5% each | Equal aggregate counts conceal different task/language errors. |
| Simple-Jev with stock Qwen 4B | 74.4% | Fixed prompt/readout baseline; matches Jebadiah on v1 originals but trails on v2. |
| Laya multilingual | 36.9% | Fastest observed local median, about 19 ms; weak on these supplied-rule cases. |

The [full sixteen-row ranking](benchmark/reports/next-wave-comparison-v2/ranking.md)
also includes Eikos, Kev 0.8B, the original Laya checkpoints and both GLiNER models.
GLiNER is a native classification mapping track, without fabricated probability metrics.

Size correlates strongly with compact score in the tested known-size sample
(Spearman **0.920**), but the Kev series is more informative: **63.1% → 87.5% → 88.1%**
at 0.8B/4B/9B. The last step is uncertain on compact inputs and more useful with
examples or distractors. See [size analysis](docs/size-vs-quality.md).

The new wave adds **no hosted inference charges**; local operating cost remains
unmeasured. [Analysis and cost-benefit recommendations](benchmark/reports/next-wave-comparison-v2/analysis.md),
[concrete support-ticket failure](benchmark/reports/next-wave-comparison-v1/support-ticket-case-study.md),
and [reproduction protocol](benchmark/next-wave/README.md).

## Initial v2: first six entrants, English / PT-BR

Seven tasks, 84 new scenarios, paired languages and three conditions: **3,024 new
classifications across six entrants**, all valid, with no retries. Compact inputs
are the primary comparison; examples and longer distractors are reported separately.

| Entrant | Compact English | Compact PT-BR |
| --- | ---: | ---: |
| Jev | 97.6% | 97.6% |
| Clef hosted | 97.6% | 94.0% |
| Clef-flash hosted | 91.7% | 83.3% |
| Clef-flash local | 89.3% | 85.7% |
| Laya | 44.0% | 41.7% |
| Laya-typed | 50.0% | 35.7% |

Full Clef matched Jev's English total. Local Flash matched Jev on sentiment in both
languages and English incident status, but task cells contain only twelve scenarios.
Neither Laya checkpoint beat Jev or full Clef in any compact task/language cell.
Examples did not consistently help. Base Laya truncated every long PT-BR input,
so that stress result cannot isolate language understanding.

Hosted/local Flash now disagree on **19/504 labels** despite equal overall accuracy;
v1's exact agreement does not generalize. The new hosted run's list-price usage is
**$0.07236 before allowances**, with local operating cost unmeasured. Read the
[analysis and scoped cost-benefit ranking](benchmark/reports/comparison-v2/analysis.md)
for paired uncertainty, concrete errors, language token costs and limitations.

## Initial v1: first six entrants, explicit policies

13 tasks × 10 original scenarios × four presentations = **520 classifications/model**,
plus **24 separate uncertainty probes/model**. Hosted runs were recorded 9 October 2026;
AMD homelab runs on 10 October. All six entrants completed 544 valid responses each.

| Entrant | Originals / all variants | Median client latency | Deployment |
| --- | ---: | ---: | --- |
| Jev 1.13.0 | 96.2% / 95.2% | 253 ms | TypeSafe API |
| Clef | 94.6% / 95.0% | 606 ms | Cloudflare Workers AI |
| Clef-flash | 90.8% / 89.0% | 491 ms | Cloudflare Workers AI |
| Laya | 43.8% / 38.5% | 38 ms | Pinned snapshot, AMD ROCm |
| Laya-typed | 43.8% / 38.5% | 38 ms | Pinned snapshot, AMD ROCm |
| Clef-flash local | 90.8% / 89.0% | 595 ms | Pinned snapshot, AMD ROCm |

Jev and full Clef are effectively tied in classification quality on this small suite.
Local Clef-flash matched all 520 hosted classification labels, though probabilities
varied slightly. Laya's fastest latency came with much weaker policy-following here.
The local main run took about six minutes with already-loaded models; downloads and
cold starts are excluded. LAN and WAN timings are not controlled hardware comparisons.

These results **do not establish that small open models are weak on every task**.
All entrants received an untuned explicit-policy track. The separate bilingual
expansion tests ordinary semantics, worked examples and distracting context.
Clef is itself open-weight: open/proprietary and local/hosted are separate comparisons.

## Pricing is dated, not an invoice

Rates rechecked **11 October 2026**: Jev $0.042/M input tokens, Clef $0.24/M,
Clef-flash **$0.038/M**, Microsoft/OpenRouter **$0.042/M**, OpenAI Decisions **$0.10/M**. Flash's earlier observed rate was $0.09/M; the dated original
valuation is retained. For v1's classification-only input mix, current list values per
1,000 decisions are approximately **$0.02093 Jev, $0.07401 Clef, $0.01172 Flash**.
[Sources, arithmetic and error-cost trade-offs](docs/cost-benefit-ranking.md).

Cloudflare's available daily free allowance can make small runs free. Actual billing
was not verified. Local electricity, hardware and operations were not measured and
are never labeled $0. A cheaper API response is not necessarily a cheaper workflow
if a wrong label creates review work or damage.

## Offline quick start

Requires Git and Docker; no API credentials or GPU needed to inspect/recompute results.

```sh
git clone https://github.com/akitaonrails/jev-docs-benchmarks.git
cd jev-docs-benchmarks
docker build -t jev-benchmark-runner -f benchmark/docker/Dockerfile.runner benchmark
benchmark/tools/offline.sh -m unittest discover -s /work/tests
benchmark/tools/offline.sh /work/tools/compare.py \
  /work/reports/hosted-v1 /work/reports/homelab-v1 --output /reports/comparison-recomputed
benchmark/tools/offline.sh /work/tools/score_v2.py \
  /work/reports/hosted-v2 /work/reports/homelab-v2 --output /reports/comparison-v2-recomputed
```

`offline.sh` disables network access. To run new inference, configure credentials or
the model server and follow [setup.md](docs/setup.md). Inference requires an explicit
`--execute`. All benchmark dependencies stay in containers; the client uses no GPU.

## Experiments and evidence

| Experiment | Dataset/protocol | Evidence/status |
| --- | --- | --- |
| v1 hosted | [Frozen protocol](benchmark/PROTOCOL.md), [cases](benchmark/datasets/cases.jsonl) | [Archive](benchmark/reports/hosted-v1/archive.json), [analysis](benchmark/reports/hosted-v1/analysis.md) |
| v1 local | [Local extension](benchmark/LOCAL-PROTOCOL.md), same v1 cases | [Archive](benchmark/reports/homelab-v1/archive.json), [environment](benchmark/reports/homelab-v1/environment.md), [verification](benchmark/reports/homelab-v1/verification.md) |
| v2 EN / PT-BR | [Protocol](benchmark/expansion-v2/README.md), [504 cases/model](benchmark/expansion-v2/cases.jsonl) | [Analysis](benchmark/reports/comparison-v2/analysis.md), [tables](benchmark/reports/comparison-v2/results.md), [hosted archive](benchmark/reports/hosted-v2/archive.json), [local archive](benchmark/reports/homelab-v2/archive.json) |

The v2 expansion contains 84 new semantic scenarios, paired EN/PT-BR versions,
and compact/example-guided/distractor conditions. Report by task, language and condition;
never interpret translations as independent examples or mix v2 into the v1 headline.
The installed Laya checkpoints are not its separate multilingual checkpoint.

## Methodology and limitations

- Cases, policies and translations are AI-authored and inspectable. There is no
  independent human adjudication or claim that their distribution represents customer traffic.
- Four v1 variants are correlated views of 130 originals. V2 language/condition variants
  are also correlated. Bootstrap intervals are descriptive within these authored families.
- Three v1 gold ambiguities are disclosed in [errata](benchmark/datasets/errata.json).
  Primary scores retain them; sensitivity scores exclude the same families for everyone.
- Test golds and rationales are excluded by the request allowlist. Raw outputs, usage,
  model IDs, dataset/request hashes and failures are preserved. Every model sees the
  same task inputs; no output-driven prompt tuning was performed.
- Choice probabilities and Noul estimates are evaluated separately from classification.
  Vendor confidence fields do not replace option probabilities in calibration metrics.
- Local snapshot revisions are pinned. Hosted aliases are not immutable weight versions.
  Latency includes real deployment overhead; no high-concurrency throughput claim is made.
- No fine-tuning, vision, audio, live customer data, or workstation RTX 5090 test is included.
  Models do not execute the tool actions described in fixtures.

## Repository layout

```text
docs/                         Research, interpretation, pricing and setup
benchmark/datasets/           Frozen v1 cases, source policies and errata
benchmark/expansion-v2/        Paired EN/PT-BR source cases and frozen manifest
benchmark/tools/              Stdlib runners, validators, scoring and valuation
benchmark/tests/              Offline correctness checks
benchmark/docker/             Client and deferred workstation image recipes
benchmark/homelab/             Original ROCm service and pinned downloader
benchmark/next-wave/           New service snapshots, adapters and lifecycle protocol
benchmark/reports/            Published metrics, raw gzip responses and provenance
benchmark/results/            Ignored working outputs from new runs
```

For model licenses and upstream implementations, follow the source links in
[alternatives](docs/alternatives.md). Check current provider rates and terms before
new runs; snapshots in this repository document what was observed at the stated dates.
