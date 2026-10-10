# Broader tasks and paired English / Brazilian Portuguese

Run date: **10 October 2026**. Six entrants, **3,024 classifications**, all against
one frozen dataset. The 504 requests per model represent **84 authored scenario
families × two languages × three conditions**, not 504 independent samples.

[Complete tables](results.md) · [Machine-readable metrics](summary.json) ·
[Every wrong label](errors.jsonl) · [Protocol and fixtures](../../expansion-v2/README.md) ·
[Hosted archive](../hosted-v2/archive.json) · [Homelab archive](../homelab-v2/archive.json) ·
[Setup guide](../../../docs/setup.md).

## What this adds

V1 concentrated on short English operational policies. V2 adds sentiment, current
intent, entailment, retrieval relevance, fictional data-handling rules, incident
timelines and numerical thresholds. Each task has twelve cases. Every rubric,
option description, demonstration and record has a paired PT-BR version with the
same gold label and option order. Compact prompts are the primary comparison;
worked examples and longer distracting context are reported separately.

The seven tracks are balanced: uniform random choice and the per-task oracle
majority baseline both average **30.95%**. A “coin toss” is not the right baseline
for three- and four-label questions. An isolated cell close to chance does not
establish statistical equivalence to guessing.

These are AI-authored cases and translations, without independent human adjudication.
Some conventional-task fixtures are simpler than v1's adversarial variants. Comparing
v1 and v2 percentages as though difficulty were controlled would be misleading.
No model-specific prompt tuning, fine-tuning, or post-result changes to test golds
were performed. Dataset commit `f0ceb55` preceded inference.

## Primary result and technical ranking

| Technical tier in v2 | Entrant | Compact EN (84) | Compact PT-BR (84) | PT minus EN, percentage points |
| --- | --- | ---: | ---: | ---: |
| 1 | Jev | 82/84 — 97.6% | 82/84 — 97.6% | 0.0 |
| 1, close to Jev | Clef hosted | 82/84 — 97.6% | 79/84 — 94.0% | −3.6 |
| 2 | Clef-flash hosted | 77/84 — 91.7% | 70/84 — 83.3% | −8.3 |
| 2 | Clef-flash local | 75/84 — 89.3% | 72/84 — 85.7% | −3.6 |
| 3 | Laya | 37/84 — 44.0% | 35/84 — 41.7% | −2.4 |
| 3 | Laya-typed | 42/84 — 50.0% | 30/84 — 35.7% | −14.3 |

The Jev–Clef English difference is zero. Their PT-BR difference favors Jev by
3/84, but its paired bootstrap interval includes zero: Clef minus Jev is **−9.5
to +2.4 points**. This suite supports the same broad quality tiers as v1, with
Jev the numerical leader across languages; it does not establish a universal
Jev advantage over full Clef.

Hosted Flash's within-model PT-BR decline is **−8.3 points**, with a descriptive
paired interval of **−15.5 to −1.2**. Laya-typed's decline is **−14.3 points**
[−27.4, −2.4]. Intervals for the other four entrants include zero. These are
exploratory bootstrap intervals over 84 authored families, without correction
for the many comparisons, not population-level language guarantees.

Equal language accuracy also need not mean identical decisions. Jev got 80 pairs
right in both languages, two right only in English and two right only in PT-BR.
Laya-typed got 22 pairs right in both, 20 only in English and eight only in PT-BR.
All pairing counts and semantic agreement are in [summary.json](summary.json).

## Where open models match or win

Clef and Clef-flash are open-weight models. “Open versus commercial” would group
these incorrectly: Cloudflare also sells their hosted execution. We measured full
Clef only through its API and Flash both hosted and local.

- **Full Clef matched Jev's 82/84 English total.** In English data handling, Clef
  scored 12/12 versus Jev's 11/12; on numerical thresholds the ordering reversed.
- **Local Flash matched Jev's 12/12 sentiment score in both languages**, and its
  12/12 English incident-status score. It also matched Jev's 11/12 English
  retrieval score. These are useful candidate tasks for a workload-specific pilot.
- **Laya-typed matched local Flash on English intent, 9/12**, but hosted Flash
  scored 10/12 and Jev/full Clef 12/12. Base Laya matched hosted Flash's 8/12
  PT-BR data-handling score; that is a tie at a fairly weak accuracy.
- **Neither Laya checkpoint exceeded Jev or full Clef in any compact task/language
  cell.** Broader semantics and Portuguese did not reveal a strong untuned Laya
  substitute for those two models in this dataset.

These are all comparisons on cells of twelve families. One answer changes a cell
by 8.3 points. Read the complete fourteen task/language rows in [results.md](results.md)
and their paired intervals before interpreting a selected tie as equivalence.
No task here demonstrates that a local deployment is financially cheaper.

## Did worked examples help?

| Model | Compact EN / PT-BR | With examples EN / PT-BR |
| --- | ---: | ---: |
| Jev | 97.6% / 97.6% | 97.6% / 98.8% |
| Clef | 97.6% / 94.0% | 97.6% / 97.6% |
| Flash hosted | 91.7% / 83.3% | 91.7% / 84.5% |
| Flash local | 89.3% / 85.7% | 90.5% / 84.5% |
| Laya | 44.0% / 41.7% | 36.9% / 35.7% |
| Laya-typed | 50.0% / 35.7% | 44.0% / 36.9% |

One fixed example per class did not rescue Laya; several aggregate scores declined.
Neither Laya variant reported truncation in this condition. This tests a particular
shared demonstration format, not all possible prompting or supervised fine-tuning.
Examples should therefore be validated on held-out traffic instead of assumed to help.

## Longer context exposed a language-dependent limit

The distractor condition places ten irrelevant archive notes before the decisive
record. Base Laya reported truncation in **all 84 PT-BR distractor requests**, with
**30,992 state tokens dropped and 84 truncated questions**. It reported none in
English distractors or either compact/example condition. Laya-typed reported no
truncation in any condition. The other entrants did not expose truncation telemetry;
absence of a flag is not proof that no input was cut.

Base Laya scored 39.3% English / 36.9% PT-BR with distractors, Laya-typed 44.0% /
32.1%, local Flash 88.1% / 84.5%, hosted Flash 90.5% / 81.0%, Clef 95.2% / 96.4%,
and Jev 98.8% / 98.8%. Base Laya's PT-BR long-input result includes a confirmed
input-retention problem, so it cannot isolate language understanding. Its weak
compact results, and Laya-typed's decline, cannot be explained by that reported
truncation. Longer input also sometimes improved scores, so this single construction
does not establish a monotonic relation between length and accuracy.

## Hosted and local Flash no longer give identical labels

All **504 payload hashes match**, but choices agree on **485/504 (96.2%)**. There
are **19 differing labels**, listed in the summary. Both deployments nevertheless
score **439/504 overall**, a coincidence hiding different strengths and errors.
Their compact combined-language totals also tie at 147/168.

For example, local Flash gets 11/12 PT-BR intent cases right versus hosted Flash's
9/12, while hosted Flash gets 10/12 PT-BR retrieval cases right versus local's 9/12.
V1's exact 520-label agreement was a result on those inputs, not a guarantee of
future deployment equivalence. We cannot isolate the cause of v2 differences:
hosted alias weights, numerical precision, kernels, serving implementation and
hardware were not controlled. No selective retries were used to align outputs.

## Concrete failures and confidence

Jev incorrectly treats an English notification to managers as identifying the role
required to approve (`retrieval-11-en-compact`); the passage never supplies the
required permission. It also mistakes the PT-BR invoice ID `PASSWORD-523` for a
usable credential despite the record explicitly saying it cannot authenticate
anyone (`data_handling-09-pt-BR-compact`). These errors recur in the corresponding
example condition. Full Clef, for its part, misses the distinction between a false
AND-rule and missing evidence in `threshold_policy-07-en-compact`.

There were no wrong compact predictions at option probability ≥0.9 for any entrant,
but coverage differed greatly: Jev made 149/168 such predictions, full Clef 132,
hosted Flash 69, local Flash 79, base Laya two, and Laya-typed zero. That observation
does not certify a safe threshold: v1 already contained confident errors, and the
threshold was not validated on independent production data.

Brier scores, ten-bin ECE, macro-F1 and confusion tables are retained by task,
language and condition. Low ECE alone is not high accuracy: Laya-typed's compact
PT-BR ECE is about 0.046 despite only 35.7% correct. V2 contains no fresh mathematical
Choice/Noul uncertainty probes; those conclusions remain the separate v1 experiment.

## Price and cost-benefit ranking

Use the **168 compact requests** per model for the primary quality/cost comparison;
the longer conditions have different token budgets. Rates are the [10 October
snapshot](../../pricing/2026-10-10.json), based on official model and billing pages.
Outputs are free under those listed rates. Amounts below precede free allowances.

| Paid-workload decision order | Entrant | Compact correct / 168 | Compact list value | USD / 1,000 compact decisions |
| --- | --- | ---: | ---: | ---: |
| 1 when errors matter | Jev | 164 | $0.003218166 | $0.019156 |
| 2; first for API price | Clef-flash hosted | 147 | $0.001678118 | $0.009989 |
| 3 for paid API cost; competitive quality | Clef hosted | 161 | $0.010598640 | $0.063087 |
| Conditional on locality/control | Clef-flash local | 147 | Unmeasured local cost | Unmeasured |
| Last tier for this untuned workload | Laya / Laya-typed | 72 / 72 | Unmeasured local cost | Unmeasured |

Jev's premium over hosted Flash is **$0.001540048** for **17 fewer compact errors**,
or approximately **$0.000090591 per avoided error** (0.00906 US cents). As in v1,
even a tiny downstream error cost can outweigh the API saving in these fixtures.
This assumes equal error costs; actual business losses and review effort are unknown.
Full Clef costs more without a demonstrated overall quality improvement here, though
its task-specific successes or available free allowance can change the choice.

Portuguese also changes cost. For the 84 compact pairs, Jev reports **13.8% more
input tokens** for PT-BR, and both hosted Clef models **14.8% more**. These are
matched semantic inputs with different tokenizations, not longer or harder gold tasks.
Do not price a bilingual workload using only English average token counts.

Across **all 1,512 hosted v2 requests**, listed usage totals **$0.072358812**:
Jev $0.013113954, Clef $0.051146640, Flash $0.008098218. All token usage is present,
and there were no retries, failed calls or unpriced interrupted attempts in v2.
This is a usage valuation, not a verified invoice. Cloudflare's shared daily free
allowance and other account activity can reduce the bill; the earlier pricing audit
records the billing caveats. Local power, hardware and operations were not measured.

## Runtime and reproducibility

All six entrants produced 504 valid responses with one attempt per request. Hosted
execution ran **04:23:55–04:33:03 UTC**; the homelab ran **04:23:55–04:30:23 UTC**.
They ran concurrently on separate endpoints. Local requests were warm; the GPU
service image was rechecked and matches the [captured v1 image](../homelab-v1/server-image-id.txt).
Local median/p95 client latencies were 41/78 ms for Laya, 43/190 ms for Laya-typed,
and 618/935 ms for Flash. Hosted values were 255/304 ms Jev, 302/683 ms Clef and
394/804 ms Flash. These observed LAN/WAN deployment timings do not isolate hardware
speed, and no concurrency or sustained-throughput claim follows.

The archive hashes, request hashes and frozen dataset were checked offline. The
[setup guide](../../../docs/setup.md) reproduces the CPU client and documents the
AMD service, pinned downloads, private base-image dependency and untested RTX 5090
path. No workstation GPU was used.

## What remains untested

This is more diverse than v1, but still a small, synthetic text benchmark. It does
not test real Portuguese customer traffic, multilingual Laya, fine-tuned small
classifiers, images, code-switching, many-label schemas, concurrent throughput or
production review costs. Several top-model tasks hit the ceiling; merely adding
more similar sentiment examples is unlikely to locate their limits.

A useful next experiment would freeze independently reviewed, application-specific
cases and simple deterministic/embedding baselines, then evaluate a tuned small
model on a held-out split. That would answer whether a specialized local classifier
can win a real workload. The current experiment answers the narrower question:
**the tested stock models are easy to call, but their reliable task and language
coverage differs substantially.**

## Model size and intended deployment

The technical ranking above is an accuracy ranking for these fixtures. The tested Laya checkpoints are compact 421M encoders, and their measured warm local requests were substantially faster than local Flash. That tradeoff may be useful for narrower tasks or constrained local devices if quality requirements are met. CPU performance, peak memory and energy remain unmeasured. See [model size and deployment tradeoffs](../../../docs/model-tradeoffs.md) for the resource-aware interpretation, specialized-checkpoint caveats and next-round measurement plan.
