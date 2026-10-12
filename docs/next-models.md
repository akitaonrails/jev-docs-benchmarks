# Further open models to benchmark

**12 October update:** Decision 3.0 is released. Only the user-selected flagship
d3 and smallest d3-edge were installed and tested; the four intermediate sizes
were excluded. [Availability](decision3-availability.md),
[results](../benchmark/reports/decision3-comparison-v2/analysis.md).

Checked **10 October 2026** against upstream repositories, model cards, GitHub/Hub
metadata and the live Decision Index. This is a test shortlist, not a measured
ranking on our fixtures. No new model was downloaded, installed or run for this review.

**Subsequent setup:** the homelab agent installed ten configurations after this review.
See the [installation handoff](homelab-installation-report.md) and
[frozen next-wave protocol](../benchmark/next-wave/README.md). Julia CPU/GPU and
Perplexity 27B have since been added. Microsoft Decision-1 is also available through OpenRouter; see [access](microsoft-availability.md) and the [latest measured comparison](../benchmark/reports/decision3-comparison-v2/analysis.md).
Other heavy-model candidates remain assessments.

## Initial homelab deployment

The benchmark added **one Docker container**, `decision-models-systemone`, using
`decision-models-systemone:local`, exposing `192.168.0.90:11436`. Its FastAPI/PyTorch
ROCm process serves three pinned checkpoints: Laya, Laya-typed and Clef-flash. Their
weights live in the persistent Docker volume `decision_models_hf`.

Ollama (`:11434`) and llama-swap (`:11435`) were pre-existing, separate services. Our
benchmark calls the custom SystemOne service, not either of those servers. The
client also runs in disposable Docker containers on the workstation and uses no GPU.

The checked-in [serving source](../benchmark/homelab/app.py) matches the captured
server implementation. Models load lazily on their first request and remain in the
process's `_loaded` dictionary. There is **no individual unload endpoint, automatic
idle eviction, or maximum-resident-model policy**. Live `/healthz` inspection during
this review showed all three loaded.

On the server, existing container lifecycle commands are:

```sh
# Release all benchmark models and their process memory; retain weights on disk.
docker stop decision-models-systemone
# Start an empty server; the next request loads only its requested model.
docker start decision-models-systemone
```

Stopping/restarting this container affects all three benchmark models. It does not
stop Ollama or llama-swap. These commands are instructions; this review did not stop,
restart or unload the running service. See [setup](setup.md) for its owning Compose file.

For the next round, one model process/container at a time is the simplest reliable
way to release memory between entrants. A per-model unload API could be added, but
it does not exist today. Process exit gives a clearer cleanup boundary than merely
clearing a Python variable or allocator cache.

## Our existing coverage is narrow

The six benchmark entrants are **five checkpoint/service identities across three
families**: Jev, Clef, Clef-flash, Laya, and Laya-typed. Hosted and local Flash are
two deployments of the same named model family. Our results therefore do not rank
the entire open ecosystem.

The live [Decision Index](https://huggingface.co/spaces/multimodalart/jev-decision-index)
data inspected here contains **116 model configurations plus a separate Jev reference**.
Those include sizes, revisions, stock-model readouts and serving modes, not 116
independent architectures. Its current Full score mixes public and private evaluation;
it is not raw accuracy and is not comparable to our percent-correct tables.
[Methodology](https://github.com/apolinario/decision-index),
[board data](https://huggingface.co/spaces/multimodalart/jev-decision-index/resolve/main/data/index.json).

## Requested candidates: GLiDE, Eikos, Surogate, Decider, PPLX, Simple-Jev, Jebadiah

| Name | Verified artifact / category | Priority for our benchmark |
| --- | --- | --- |
| **GLiDE** | Fastino hosted decision model with optional additional reasoning; a downloadable checkpoint was not found. | Hosted extension once credentials, current price and thinking mode are recorded. |
| **Eikos** | MIT decision fine-tunes, 4B and 27B; trained in English and Portuguese. | **High: Eikos-4B** directly addresses our bilingual supplied-rule cases. |
| **Surogate** | The serving/training engine; **Rune 26B-A4B v3** is its decision checkpoint. | Heavy-model phase, with runtime/format checks first. |
| **Decider** | Here, **Mapika Decider**, distinct from Strands and Perplexity; a family including a 4B release. | **High: Mapika/decider-4b v2.1**. |
| **PPLX** | **Perplexity pplx-decider-v1.1-27b**, Apache-2.0 weights. | **Installed** on ROCm; [protocol and status](perplexity-decider-availability.md). |
| **Simple-Jev** | Featherless's open inference server over an existing compatible model; no new classifier head is required. | **High as a baseline**, with one fixed Qwen checkpoint and prompt policy. |
| **Jebadiah** | Frontier Infra's Apache-2.0 4B/9B v2 and 27B decision models. | **High: 4B v2**, then 9B v2 to test scaling. |

**Eikos:** upstream explicitly documents EN/PT training and a consistency objective
across translations. It specializes in applying supplied financial/trading rules;
that motivates testing transfer to our other domains rather than assuming general
expertise. It offers native serving plus FP8/INT4 variants. Start with the BF16 4B
reference; an NVIDIA quantization build is not proof of AMD support. Sources:
[model card](https://huggingface.co/caiovicentino1/Eikos-4B),
[code and license scope](https://github.com/caiovicentino/eikos).

**Jebadiah:** the canonical spelling is Jebadiah, at `getainode/jebadiah` and
`frontier-infra` on the Hub. The 4B v2 uses the Qwen3.5 chat checkpoint, whereas
v1 used the base model. English training and a 20-choice HTTP cap are disclosed.
Its public JevBench results are interesting but cannot establish Portuguese transfer.
[Repository](https://github.com/getainode/jebadiah),
[4B v2 card](https://huggingface.co/frontier-infra/jebadiah-4b-v2).

**Simple-Jev:** this is exactly the baseline needed to test whether specialized
training buys anything beyond scoring an ordinary LLM's permitted answer tokens.
Name an entrant as `Simple-Jev + checkpoint + prompt policy`, since the server alone
has no classification accuracy. Pin its format; its defaults can select a different
policy by model size. Noul is derived from rating-token scores, which must be disclosed
when comparing uncertainty primitives. [Upstream README](https://github.com/featherless-ai/simple-jev).

**Surogate Rune:** its current `surogate/rune-26b-a4b-GGUF` repository name is
misleading: the card says v3 contains **BF16 safetensors, 51.6 GB**, and no v3 GGUF
build. The old GGUF version remains in history. Roughly 4B active parameters does
not mean only 4B weights must be resident. The recommended Surogate wheels target
CUDA 13/NVIDIA; a Transformers path is documented, but ROCm parity is untested here.
Hub metadata reports gated access. Use separate thinking-off/on configurations;
the latter performs additional inference. [Rune card](https://huggingface.co/surogate/rune-26b-a4b-GGUF),
[Surogate hardware requirements](https://github.com/invergent-ai/surogate).

**GLiDE:** Fastino's launch provides an API at `api.fastino.ai/v1/systemone` and
model ID `fastino/glide`. Its launch benchmark includes adaptive reasoning; the
current board row we inspected is explicitly *no-thinking*. Those are different
configurations and potentially different latency/cost budgets. The board lists open
weights as forthcoming, and an unauthenticated query of Fastino's Hub models for
GLiDE returned none. This establishes no verified download path, not proof that
weights can never become available. [Official launch](https://fastino.ai/blog/introducing-glide-the-first-thinking-decision-model).

## Other practical, informative additions

| Candidate | Size / license reported upstream | What it would tell us | Integration considerations |
| --- | --- | --- | --- |
| **Laya multilingual** | 322M, Apache-2.0 | The missing direct test of Laya's intended non-English checkpoint. Highest priority for PT-BR fairness. | Existing Laya runtime, but pin its own weights; test the multilingual checkpoint directly, with Router as a separate configuration. |
| **GLiNER2.5-Decide and multi-Decide** | 340M English / 287M multilingual, Apache-2.0 | Whether another small encoder family does better on intent, sentiment and operational classification. | Its native classification API differs; preserve rubric/label descriptions and report any unsupported primitives or unavailable probabilities. |
| **Kev-4B and Kev-9B** | 4B / 9B, Apache-2.0 | A useful middle ground between small encoders and Flash's 9B implementation; also enables a size comparison. | SystemOne-compatible server; use versioned Kev 1.0 releases and exact base/adapter/runtime pins. ROCm needs a smoke test. |
| **Strands Decider 2B, hobson-v21** | Qwen3.5-2B base plus adapter/head, Apache-2.0 | A compact decoder-backed alternative for routing and supplied rules. | Native SystemOne serving. Pin v21 rather than accidentally mixing it with v19 results. |
| **Mapika Decider-4B v2.1** | 4.2B, Apache-2.0 | Another training recipe at roughly Kev-4B's size, with detailed published failure analysis. | Use a runtime that honors its per-primitive calibration temperatures; older clients produce different probabilities. |
| **Von 1.3 / von-1.2 weights** | 395M, Apache-2.0 | Another small encoder and a useful test of option wording and definitions. | 1.3 adds inference chains over the same weights. Report chain mode separately from a single-pass baseline. |
| **CLM-v0.1-8B** | Frozen Qwen3-8B plus projection heads, Apache-2.0 | A genuinely different state/action embedding approach, particularly relevant to routing and candidate ranking. | Requires the correct last-token-pooled encoder and head; caching changes latency and must be disclosed. |
| **Bespoke-Nimble-9B, Apache release** | 9B base plus adapter, Apache-2.0 weights | A contrastive-data/token-readout alternative at Flash's size. | Pin the release and prompt builder. Current Apache release uses T=1.0; the old calibration must not be reused. |

### Primary sources and release caveats

- [Laya multilingual model card](https://huggingface.co/convaiinnovations/laya-multilingual):
  default 1,024-token limit, configurable to 8,192. A higher configured limit is not
  a measured guarantee of long-context accuracy. Our previous two checkpoints were
  English/typed variants, so their PT-BR results do not evaluate this one.
- [GLiNER English card](https://huggingface.co/fastino/GLiNER2.5-Decide),
  [multilingual card](https://huggingface.co/fastino/GLiNER2.5-multi-Decide): the
  publisher's main comparative suite is English. Calling a model multilingual does
  not establish PT-BR accuracy. Native label classification and our explicit policy
  tasks should both be represented.
- [Kev repository](https://github.com/jaredpalmer/kev): also offers 0.8B and 27B.
  The smaller versions share a recipe, making 4B/9B a useful family
  comparison. The published 65k accepted context is distinct from the shorter
  validated context of some releases. `pip install kev` refers to an unrelated
  package; installation must follow this project's source instructions inside Docker.
- [Strands v21 card](https://huggingface.co/StrandsAgents/strands-decider-2B-hobson-v21):
  upstream explicitly reports weak question sensitivity and difficulty with long,
  multi-step inputs. Those are good reasons to test our policy pairs. Its reported
  public JevBench result is 176/231, not our benchmark's expected performance.
- [Mapika 4B card](https://huggingface.co/Mapika/decider-4b): v2.1 makes trade-offs
  between hard decisions, calibration and sampled actions. This is useful evidence
  against assuming a later version improves every task.
- [Von repository](https://github.com/wfzyx/von): supports CPU, CUDA, ROCm and MPS
  paths upstream. Its quoted speed claims use different hardware/protocols and do
  not predict latency on our homelab.
- [CLM card](https://huggingface.co/Contrastive-LM/CLM-v0.1-8B): its strongest verifier
  headlines use fine-tuned heads, not the generic checkpoint. We should first test
  the generic release and keep training experiments separate.
- [Nimble Apache model card](https://huggingface.co/bespokelabs/Bespoke-Nimble-9B)
  documents its 8,192-token limit and separate base download. The code repository's
  GitHub metadata reports no detected license; model licensing does not establish
  the license of every serving file. Use and record the licensed release artifacts.

## Second round: stronger but much heavier candidates

**Perplexity `pplx-decider-v1.1-27b`** is a particularly relevant quality challenger.
Its native checkpoint uses a separate decision head and noncausal full-attention
behavior, so an ordinary causal chat loader does not reproduce it. The card calls
for roughly 49 GiB for weights plus working memory. Hub metadata returned
`private=false`, `gated=false` during inspection, despite stale private-repository
wording in its instructions. Anonymous weight access is now confirmed. A native-API ROCm deployment now passes smoke and full input-encoding checks;
see [installation and compatibility details](perplexity-decider-availability.md). [Model card](https://huggingface.co/perplexity-ai/pplx-decider-v1.1-27b).

**Kev-27B** and **full local Clef-27B** are also relevant. We already measured full
Clef through Cloudflare, but have not compared its local deployment. These belong
in a dedicated capacity check, not alongside every resident 9B model.
[Kev family](https://github.com/jaredpalmer/kev),
[Clef weights](https://huggingface.co/Cloudflare/clef).

Several earlier benchmark containers have a **40 GiB host-memory limit**, separate
from the GPU-addressable budget. Perplexity uses a **24 GiB host cap** and a strict
direct-to-GPU loader after the standard loader exceeded that cap. See its
[deployment evidence](../benchmark/perplexity/README.md). Weight loading and
inference must fit both applicable limits. The homelab
also shares physical memory with other services. “64 GiB GPU-addressable” must not
be interpreted as 64 GiB of free, dedicated VRAM. Fit, peak memory, quantization and
hardware availability need to be measured before scheduling 27B runs. A quantized model is a separately reported
configuration.

## Candidates to distinguish from permissive open-source releases

- **Bespoke-Nimble-9B-v3** is a newer, stronger-looking candidate in published
  benchmarks, but its weights are **CC BY-NC 4.0**, unlike the Apache release above.
  It belongs in a separately marked research-only shortlist, not the same commercial
  adoption category. [v3 card](https://huggingface.co/bespokelabs/Bespoke-Nimble-9B-v3).
- **Torchcast Decision 27B** is another high-scoring board entrant whose current
  Hub metadata lists **CC BY-NC 4.0**. Its size also puts it in the heavy-model group.
  [Model card](https://huggingface.co/torchcast-ai/torchcast-decision-27b).
- **Fastino GLiDE** appears on the board, but that snapshot says its open weights
  are coming soon and supplies no weights repository. A hosted result is not a
  downloadable open release. Keep it on a watchlist, separate from GLiNER2.5-Decide.
- **Arbiter and deployment wrappers** should be recorded as runtimes, not counted
  as additional learned models when they serve the same checkpoint.

## Popularity and independent benchmark evidence

GitHub API observations on 10 October: Laya **32,087** stars, Kev **8,881**, GLiNER2
**2,351**, Nimble **2,150**, Mapika Decider **1,119**, Von **877**, Surogate **853**,
Simple-Jev **598**, Eikos **41**, and Jebadiah **5**. These are repository-level interest signals,
not checkpoint quality or usage counts. GLiNER2's total also covers its extraction
library. Sources: the repositories' public `/repos/{owner}/{repo}` GitHub API records.

For one dated external comparison, the inspected Decision Index 0.3.1 Full scores
were Perplexity v1.1 **62.75**, Jev **60.11**, Kev-27B **58.78**, Nimble-v3 **54.67**,
Clef **53.08**, Flash **47.61**, Kev-9B **43.27**, and Kev-4B **39.50**. These are
maintainer-reported composite scores, not measurements we reran, and the board groups
small gaps. They justify testing more candidates; they do not replace our evaluation.

In particular, our small policy suite favoring Jev does not establish that Jev beats
all open models. The broader board has at least one open-weight candidate above it.
Conversely, popular small encoders can remain weak on broad explicit-policy tasks.

## Original proposed experiment and subsequent status

Start with **Eikos-4B, Jebadiah-4B-v2, Mapika Decider-4B, Kev-4B, Simple-Jev over a
fixed Qwen-4B, Laya multilingual, and the English/multilingual GLiNER2.5-Decide pair**.
These eight configurations include the specifically requested families, a stock-model
readout baseline, and the missing multilingual encoders. Then add Kev/Jebadiah 9B,
Strands v21, Von, CLM and the Apache Nimble release. PPLX has since been installed for testing. Rune, Kev-27B and local full Clef
still require separate memory/runtime checks.
Treat GLiDE as an additional hosted competitor until downloadable weights are verified.

Use the frozen v1/v2 fixtures unchanged first. Add a separately frozen representation
track comparing meaningful labels with opaque IDs, plus matched rule changes. The
[labels-versus-definitions study](https://arxiv.org/abs/2610.02586) reports large
format dependence in several models. Our opaque v2 IDs deliberately isolate supplied
criteria, but do not exhaust the models' intended native classification workflows.
All entrants should receive the same added conditions; do not tune prompts on test
answers or mix the new scores into the old headline.

Preserve native probability semantics. A classifier's independent label scores are
not automatically a normalized Choice distribution, and a wrapper must not invent
Noul probabilities. Report unsupported outputs and evaluate accuracy separately when
probability metrics cannot be compared. Include a stock local LLM and a conventional
classifier/reranker baseline to test whether specialized training adds value.

Deployment would remain containerized, with pinned model/code/base revisions, a
reviewed adapter per family, explicit model lifecycle, and cold versus warm timing.
The initial eight configurations plus Kev 0.8B/9B have now been installed and
benchmarked. See the [completed expanded analysis](../benchmark/reports/next-wave-comparison-v2/analysis.md).
The additional representation track, Jebadiah 9B, Strands, Von, CLM, Nimble and
heavy-model/GLiDE extensions remain future work.
