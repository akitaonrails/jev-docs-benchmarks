# What Jev is, what preceded it, and what is supported

Research snapshot: **3 October 2026**. Claims below distinguish TypeSafe's statements, direct observations published by experimenters, and our inferences. No Jev API calls or local benchmarks were run for this report. The newer open implementations are compared in [Jev alternatives](alternatives.md).

## Mechanics

Jev 1.13.0 accepts text state (a string or text-bearing JSON) plus typed questions through `POST /v1/systemone`. `Choice` returns an option and its distribution; `Score` returns an ordinal score and distribution; `Noul` returns a 0–1 probability for a proposition. Choice and Score also return a `confidence` statistic derived from the distribution; Noul does not. Questions can share one state in one request. The app still needs to define thresholds, actions, review paths, and any exact calculations. [Introduction](https://docs.typesafe.ai/introduction), [confidence](https://docs.typesafe.ai/confidence), [API primitives](https://docs.typesafe.ai/primitives).

Current published terms are $0.042 per million input tokens and no charge for output tokens, with 64,000 tokens across state and questions and 32,000 for the state plus the longest question. Input is text only; English is its strongest language. The model is shared across accounts and is not fine-tuned on each customer's data. Pin `jev-1.13.0` when tuning thresholds because `jev-latest` can move. [Model reference](https://docs.typesafe.ai/models).

Calling this a **classifier** is technically fair. More precisely, it is a *question-conditioned, multi-output decision model*: the categories and rubrics can change per request. A conventional fixed-label classifier may be much easier to validate for one recurring task. Jev's advantage, if established for that task, would be flexible questions, batching, serving economics, or probability quality.

The internal architecture, sampler, training data, and RLCD training procedure are not specified sufficiently in the launch material for an independent technical comparison. TypeSafe calls them new; this report treats that as a vendor claim. No conclusion about the unseen implementation follows from the public output interface. [Launch post](https://typesafe.ai/blog/introducing-system-one-models-and-jev).

## What could already be done?

| Capability | Existing route | What Jev packages |
| --- | --- | --- |
| Text into fixed labels | Supervised classifier, rules, or encoder model | Arbitrary request-specific labels and criteria without training a model for each task |
| New labels described at inference time | Zero-shot text classification, studied by 2019 and available through Hugging Face | Several typed questions over one state in one hosted call |
| Numerical confidence | Classifier probabilities and established calibration methods | Distributions in the standard response; claimed calibration must still be tested by domain |
| Schema-valid decisions from an LLM | Constrained decoding / structured outputs | A model intended to return decisions directly, without autoregressive answer generation |
| Open Jev-like service | Clef, Laya, or Kev weights behind a compatible endpoint | TypeSafe's managed API, model, and larger context than Laya |

Sources: [zero-shot classification research](https://arxiv.org/abs/1909.00161), [Hugging Face API](https://huggingface.co/docs/inference-providers/tasks/zero-shot-classification), [scikit-learn calibration](https://scikit-learn.org/1.8/modules/calibration.html), [OpenAI constrained outputs](https://openai.com/index/introducing-structured-outputs-in-the-api/), [Clef](https://huggingface.co/Cloudflare/clef), [Laya](https://github.com/NandhaKishorM/laya), [Arbiter](https://github.com/0xBakeer/arbiter).

Arbiter is a serving layer for Laya checkpoints, with a Jev-compatible endpoint; the [Fr3akaz0id fork](https://github.com/Fr3akaz0id/arbiter) adds an OpenAI-compatible approval endpoint. Compatibility establishes that clients can reuse the *contract*, not that model internals, calibration, or accuracy are equivalent. Laya's published results identify both strengths and weaknesses: its author reports better outcomes on some tasks and Jev ahead on large option sets and some distribution metrics. Its Jev figures come from third-party published tests using different prompts and samples, so its comparison table is indicative rather than controlled. Laya's local checkpoints also have much shorter default contexts than Jev. [Laya benchmarks and caveats](https://github.com/NandhaKishorM/laya).

Cloudflare's Clef release supplies evidence that was missing from Jev's launch: open weights and a described implementation using a frozen Qwen backbone, LoRA adapters, and a direct option-scoring head. It does not prove that TypeSafe uses the same architecture, but it shows that established components can reproduce the product abstraction and compete with Jev in a broad public suite. [Cloudflare launch](https://blog.cloudflare.com/clef-decision-models/), [detailed comparison](alternatives.md).

## Claims audit

| Claim | Evidence and interpretation |
| --- | --- |
| **193.6× faster / 444.6× cheaper** | TypeSafe's own selected workflow evaluations against LLMs. The company says these are on the high end of expected real-world gains. They are not comparisons with the best small classifier, local rules, or every cheap LLM. [Launch post](https://typesafe.ai/blog/introducing-system-one-models-and-jev), [eval design](https://evals.typesafe.ai/). |
| **Zero hallucinations** | TypeSafe says its 0% is *not empirical*: the schema guarantees an allowed output. It does not guarantee the chosen label is true. Constrained-output LLMs also separate schema validity from value correctness. [TypeSafe](https://typesafe.ai/blog/introducing-system-one-models-and-jev), [OpenAI](https://openai.com/index/introducing-structured-outputs-in-the-api/). |
| **Calibrated confidence** | A probability distribution and derived confidence are returned. Calibration is an empirical relationship between predictions and labeled outcomes; it must be measured for each domain and question format. TypeSafe itself recommends testing thresholds on one's own data. [Confidence docs](https://docs.typesafe.ai/confidence), [model jaggedness](https://docs.typesafe.ai/model-jaggedness/jev-1.13). |
| **Frontier-like accuracy** | TypeSafe's workflow reference is the average of GPT-6 Astra and Claude Fable 5.1 answers, not independently verified truth. It is evidence of agreement under that evaluation design. [Evaluation description](https://evals.typesafe.ai/). |
| **Better automation** | Plausible only for tasks reducible to narrow judgments and code-defined actions. TypeSafe advises decomposing complex questions and doing math, dates, and policy logic in code. [Introduction](https://docs.typesafe.ai/introduction), [limitations](https://docs.typesafe.ai/model-jaggedness/jev-1.13). |

## Independent measurements and limits

The [2,000-email phishing benchmark](https://github.com/anisselbd/jev-phishing-bench) reports Jev's direct verdict at **62.6% accuracy**, **239 ms median latency**, and **$0.038 per 1,000 emails**, versus Claude Haiku 4.5 at **81.3%**, **687 ms**, and **$0.462**. Its five-signal decomposition improved the resulting classifier substantially. Added controls found that a simple URL rule was already strong on the constructed dataset; the decomposed Jev result did not establish a universal quality lead over an equivalently decomposed LLM. These are the experimenter's reported results, not a replication here.

A separate [27-ticket test](https://github.com/WallerChen/jev-measured) found Jev tied one small chat model at 27/27, while two others scored 26/27. The sample is too small and narrow for a general accuracy ranking. It is useful evidence that a cheap chat model can be competitive on a particular typed classification task.

Paulo Câmara's article [“O aluno que marca a letra A”](paulo-camara-article.md) collects a wider set of early audits. Its strongest evidence shows that `Choice` can assign high probability to a preferred option when an outcome is unknowable, raw calibration degrades under ambiguity and domain change, and plausible untrusted context can redirect a decision. The separate annotation distinguishes those reproducible findings from the article's architecture, energy, neuroscience, and legal inferences.

TypeSafe's [jaggedness document](https://docs.typesafe.ai/model-jaggedness/jev-1.13) acknowledges literal interpretation, weak counting and numeric precision, date comparison errors, irrelevant-context degradation, adversarial steering, and inconsistency between equivalent-looking questions. These matter more than schema compliance when a model gates an action. A probability or confidence threshold cannot replace a labeled validation set and a review path.

## Conclusion

Jev is a credible implementation of a narrow, useful pattern. The product can make repeated semantic judgments cheaper and faster than asking a large chat model to generate text for each one. The underlying task, typed outputs, probabilities, and code-composed workflows are established. Clef, Laya, and Kev now make the category reproducible with open weights. The public evidence does not establish a general Jev accuracy lead, a fundamentally new task, or a safety guarantee. Evaluate it as a component for a specific measured decision, not as a general agent or reasoning upgrade.
