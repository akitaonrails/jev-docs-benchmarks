# Business summary: should I care about Jev?

## Perplexity update: 11 October 2026

The [twenty-configuration comparison](../benchmark/reports/perplexity-comparison-v2/analysis.md)
now has an open-weight quality leader: **Perplexity Decider 1.1 27B**, at **99.4%
compact bilingual accuracy**, versus Jev 97.6% and Clef 95.8%. It scores **501/504**
overall and all PT-BR cases correctly. The lead over Jev is three compact decisions;
this is an observed ranking on a small synthetic suite, not general superiority.

It requires about 49 GiB of BF16 weights plus working memory. The tested ROCm
configuration measures **1,547/2,446 ms median/p95**, with fallback kernels and a
custom loader disclosed. Consider it for local quality when memory and latency
permit. Jebadiah 4B remains a smaller, faster candidate at 90.5% compact; Julia
is much smaller and faster but scores 31.5%. No local dollar cost was measured.

Jev retains the best measured hosted quality/list-price combination; Flash remains
the cheapest tested hosted option by compact usage. [Official prices were rechecked](../benchmark/perplexity/pricing-recheck.md)
and are unchanged.

On original policies, Perplexity scores **129/130**, or **127/127** after the same
pre-existing ambiguity exclusions applied to every model. Its Boolean uncertainty
MAE is **0.3754**, however: classification strength does not imply reliable event
probabilities. The compact lead over Jev has a family-bootstrap interval including
zero. Earlier sections below preserve their historical scope.

**Decision:** No portfolio-wide integration. A typed-decision model is worth a small experiment only where a project repeatedly asks a narrow question and can use a bounded answer immediately. FrankClaw's model routing and ai-memory's candidate ranking are the clearest candidates. Neither is presently a demonstrated bottleneck or a proven improvement.

Jev is TypeSafe AI's hosted, text-only decision model. A request supplies a state and several questions; each returns a choice, ordinal score, or yes/no probability. Application code owns the policy and action. It can answer several questions over the same state without generating a prose response. This is useful for classification, ranking, and routing, especially at high volume. It cannot write a summary, inspect an image directly, prove a claim, or enforce a security boundary. [Product documentation](https://docs.typesafe.ai/introduction), [model limits](https://docs.typesafe.ai/models).

The task is established. Earlier zero-shot classifiers accepted arbitrary candidate labels; classifiers have long returned probabilities; constrained-output LLMs can guarantee schema-conforming values. The potentially valuable product work is a convenient API, parallel typed questions over shared state, and low advertised price and latency. TypeSafe claims a new architecture and training method, but has not published enough detail to establish their technical novelty independently. [2019 zero-shot classification paper](https://arxiv.org/abs/1909.00161), [Hugging Face zero-shot API](https://huggingface.co/docs/inference-providers/tasks/zero-shot-classification), [OpenAI Structured Outputs](https://openai.com/index/introducing-structured-outputs-in-the-api/), [TypeSafe launch](https://typesafe.ai/blog/introducing-system-one-models-and-jev).

The **193.6× faster / 444.6× cheaper** headline describes selected TypeSafe workflows against LLM baselines. TypeSafe says these are likely near the high end of real-world gains. Its **zero hallucinations** number measures guaranteed output shape, not whether the selected answer is correct. Its workflow reference answers average two other models rather than human-verified ground truth. These facts support a useful speed claim on certain comparisons, not universal superiority. [Launch methodology](https://typesafe.ai/blog/introducing-system-one-models-and-jev), [workflow evals](https://evals.typesafe.ai/).

Cloudflare's October 2026 release of **Clef** makes the category easier to judge. Clef and Clef-flash offer a Jev-compatible API, Apache-2.0 weights, disclosed Qwen-based architectures, and image input. Cloudflare reports stronger results than Jev on many tasks in its internal run of the open Decision Index, while Jev still wins some tasks and had the lowest listed hosted input price at our original snapshot. **Laya** covers the small local end: its 322M–421M encoders are inexpensive and fine-tunable, but its own documentation says the base models are weak zero-shot decision engines. See the [full alternatives comparison](alternatives.md).

Independent evidence is mixed. On one 2,000-email phishing dataset, Jev's direct verdict was faster and cheaper but less accurate than Claude Haiku 4.5 (62.6% versus 81.3%). Asking for several specific signals improved the workflow, yet a simple rule was already strong on that dataset. This is a task-specific result, not a general rank of the models. [Reproducible phishing study and controls](https://github.com/anisselbd/jev-phishing-bench).

**Business rule:** buy or build a decision service when the cost of repeated judgments is visible, its error rate is acceptable on your own labels, and it improves the complete workflow against a simple baseline. Use Jev for cheap managed text decisions, consider Clef when vision or its broader published performance matters, and consider fine-tuned Laya when local control matters. The project review found a few candidate decisions, but no README demonstrates that this threshold has been reached. See [project fit](use-cases.md).


## Measured follow-up: 10 October 2026

Our [frozen hosted/local benchmark](../benchmark/reports/comparison-v1/analysis.md)
now provides direct evidence: Jev and hosted Clef scored about 95% across the synthetic
classification variants, hosted and local Clef-flash about 89%, and both stock Laya
checkpoints 38.5%. Local Clef-flash matched all 520 hosted classification labels.
Laya was fast (38 ms median on the AMD homelab) but unreliable on the explicit policies,
particularly with misleading reviewer commentary. A common API does not make these
checkpoints interchangeable. These are untuned synthetic-suite results, not production
error rates; the detailed report includes original-only scores, disputed-gold sensitivity,
uncertainty probes and environment differences.


## Cost-benefit decision: current prices

The [technical and cost-benefit ranking](cost-benefit-ranking.md) rechecks prices on
10 October. Clef-flash now costs $0.038/M input tokens, down from the $0.09/M recorded
in our earlier audit. For 1,000 classifications matching this suite's length mix,
current list values are about **$0.01172 Flash, $0.02093 Jev, $0.07401 Clef**.
Jev is the preferred paid default when errors matter; Flash wins pure API cost;
full Clef is attractive within Cloudflare's available daily free allowance. Local
Flash preserves measured classification behavior, but local operating costs are
unmeasured. Stock Laya's weak accuracy makes its low latency insufficient here.


## Broader bilingual follow-up

The [v2 experiment](../benchmark/reports/comparison-v2/analysis.md) adds seven tasks
and paired English/PT-BR cases. Jev scored 97.6% compact accuracy in both languages;
full Clef matched English and scored 94.0% in PT-BR. Local Flash matched Jev on a few
specific tasks, but both Flash deployments were weaker overall. Stock Laya remained
far behind, and worked examples did not consistently help. Base Laya also truncated
all long PT-BR inputs. These small synthetic task cells guide further evaluation;
they do not establish production accuracy. The broader evidence preserves the
cost-benefit recommendation above while showing that language and deployment can
change individual decisions.

## Expanded open-model follow-up

Ten additional local configurations now have [measured results](../benchmark/reports/next-wave-comparison-v2/analysis.md).
Jev and hosted Clef remain the leading quality group on the difficult bilingual
cases. Jebadiah 4B v2 is the strongest local compact candidate by point estimate;
Kev 9B benefits more from examples and distractors. Some local models match Jev
on particular small task cells, and Kev 9B wins one English data-handling cell.
Those cells do not establish general superiority.

Size correlates with score, but both workload and training matter. The stock-Qwen
Simple-Jev configuration trails the stronger decision models on v2 while matching
Jebadiah on v1 originals. Multilingual Laya is fast but remains weak on this
supplied-rule workload. This broadens the candidate shortlist; it does not create
a portfolio-wide need for a classifier or establish local dollar savings.

## OpenAI Decisions follow-up

The [new native API comparison](../benchmark/reports/openai-comparison-v2/analysis.md)
places OpenAI at **90.5% compact bilingual accuracy**, tied with local Jebadiah 4B,
below Jev (97.6%) and Clef (95.8%). It is stronger with examples and distractors,
reaching 93.1% overall, and has the lowest observed hosted median latency (222 ms).
Its measured compact list cost is $0.02331/1,000 calls, versus Jev's $0.01916.
The current quality/price recommendation remains Jev; an OpenAI integration may
still be useful for specific tasks. Exact thresholds and Boolean conditions remain
visible failure modes. Subscription access to Codex does not fund these API calls.

[Julia-1 GPU/CPU results](../benchmark/reports/julia-comparison-v2/analysis.md) add
two completed deployments of the 144.3M model: both score 31.5% compact, close to
the 31.0% random baseline. GPU median latency is 12 ms; four-thread CPU is 71 ms.
Speed and small storage do not offset these policy errors. The quality/price
recommendations above remain unchanged; local compute cost is unmeasured.
