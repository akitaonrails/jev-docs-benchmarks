# What the first hosted run establishes

Run on 9 October 2026, approximately 13:50–14:06 UTC. **Jev and Clef performed similarly
on this explicit-policy suite; Clef-flash was less accurate. None approached chance
on classification overall. Probability handling under missing information was a much
weaker and more primitive-dependent capability.**

The [generated results](results.md) contain the full tables. [summary.json](summary.json)
contains confusion matrices, calibration bins, paired comparisons, and every probe.
[errors.jsonl](errors.jsonl) includes every wrong classification, not selected examples.
Raw API responses are preserved in [responses.jsonl.gz](responses.jsonl.gz), with hashes
and timestamps in [archive.json](archive.json).

## Classification results

| Model | Frozen 520-case accuracy | Excluding three disputed families (508 cases) | Original 130-case accuracy | Median / p95 request latency |
| --- | ---: | ---: | ---: | ---: |
| Jev 1.13.0 | 95.2% | 97.2% | 96.2% | 253 / 303 ms |
| Clef | 95.0% | 97.2% | 94.6% | 606 / 2,076 ms |
| Clef-flash | 89.0% | 90.6% | 90.8% | 491 / 884 ms |

The overall uniform-label chance baseline is 30.8%, because tasks have three or four
labels. An oracle choosing the most frequent gold label separately for each domain
would score 37.7% on originals. The models clearly exceed these baselines here.

The original-case Jev–Clef gap is only 1.5 percentage points, with a descriptive paired
bootstrap interval spanning -3.1 to +5.4 points. The evidence does not establish a
robust quality advantage for either. The 520 variants represent 130 authored scenario
families, with some deliberate policy pairs sharing observations. They must not be
represented as 520 independent real tickets.

All three models answered both sides correctly in each of the five prespecified
policy pairs. For example, a single-tenant outage required escalation under one
company's policy and monitoring under another. This is direct evidence, within the
small fixture set, that they can follow supplied definitions rather than merely attach
the conventional label suggested by the scenario.

## Did the hard cases push them to chance?

No. Although the cases target exceptions, missing facts, misleading wording, and
policy changes, most remain short and explicit. The run found a ceiling in the suite,
not the limits of every model. Eleven of thirteen Jev domain scores were at least
87.5%; five domains scored 100% for both Jev and Clef across all four variants.

The weakest frozen Jev domain was tool approval at 77.5%, but part of that penalty is
a fixture ambiguity about scratch-file deletion. These are classifications of proposed
actions, not executed tool calls, and the dataset is too small to certify an agent
security boundary. All models avoided an `allow` answer on the four explicitly blocked
original tool cases; this is only four cases per model.

The next stress-suite version should add longer conversational histories, harder
reference resolution, realistic product jargon, changes in authority over time, and
raw tickets with less pre-interpreted evidence. It should be frozen as a fresh suite
before inference. Selecting only this run's failures would create a misleading test.
Local models should first receive this same frozen v1 suite for comparability.

## Real failures despite high aggregate scores

The error log includes interpretable failures outside the disputed families:

- Jev classified an ongoing, verified production data-loss incident as merely degraded
  with probability **0.94** when misleading reviewer commentary was added. The policy
  explicitly made data loss critical even for one customer.
- Clef also missed that data-loss exception; with opaque labels it assigned the
  degraded option probability **0.9231**.
- Clef-flash approved a refund with probability **0.9075** in the injected version of
  a case where the license was used and no duplicate charge existed. The written policy
  required denial.
- Clef-flash classified an almost empty document as a receipt at **0.9611**, although
  the text did not establish payment status and the policy required an unknown answer.

These examples concern the stated fictional policies. They demonstrate why a valid
label and a high probability are insufficient to prove policy compliance. They do not
provide population error rates for production incidents, refunds, or fraud detection.

## Sensitivity to presentation

Reversing option order preserved the semantic answer in 98.5% of Jev pairs and 100%
of Clef and Clef-flash pairs. Opaque labels preserved it in 96.2%, 99.2%, and 97.7%,
respectively. This small suite therefore does not show universal first-option behavior.

Misleading commentary changed originally correct answers to wrong ones in **2 Jev,
1 Clef, and 11 Clef-flash** families. Clef-flash accuracy fell from 90.8% on originals
to 85.4% on the injected versions. The attack was deliberately simple and the trusted
instruction explicitly told models to ignore it. Robustness here is not evidence
against stronger prompt-injection attacks. Without repeated identical requests, some
variant differences could also reflect service nondeterminism.

## Probability handling is a different result

The separate probes describe a uniform random device with no observed outcome or
predictive evidence. The correct probability is supplied by the mathematics of the
fixture: 1/2, 1/4, or 1/6. No hidden coin flip is invented as ground truth.

| Model | Choice mean per-option absolute error ↓ | Noul absolute error ↓ |
| --- | ---: | ---: |
| Jev | 0.263 | 0.058 |
| Clef | 0.073 | 0.378 |
| Clef-flash | 0.141 | 0.523 |

Both columns measure deviations from known probabilities, but Choice averages across
all classes while Noul measures one named event. They are related diagnostics, not
identical scoring problems. There are only twelve probes per primitive, using closely
related templates; this is a failure-mode check, not a broad forecasting benchmark.

For the first fair two-outcome probe, Jev's Choice distribution was **0.89/0.11**,
while its Noul estimate for the named event was **0.55**. Clef's corresponding values
were **0.6453/0.3547** and **0.8727**. For the first six-outcome Noul probe, the true
probability was 1/6: Jev returned **0.25**, Clef **0.516**, and Clef-flash **0.7935**.

Jev selected the first listed Choice option in only **2/12** of our probes. This
supports the earlier qualification of Paulo Câmara's article: overconfidence under
absent information can reproduce under a different prompt without reproducing
universal first-option selection. Our labels, order, and instructions differ from the
cited dice experiment, so this does not refute that experiment's recorded results.

The practical implication is that calibration needs to be tested for the exact
primitive and wording. A model's good ticket-classification accuracy does not establish
that its numeric output is a trustworthy probability for an unobserved future event.

## What the gold audit changed

Three scenario families had defensible alternative interpretations:

1. A feature outage across multiple tenants: the policy did not fully distinguish an
   outage from degraded functionality.
2. Deletion inside scratch: permission to write there did not explicitly distinguish
   deletion from other filesystem writes.
3. Retrieval of a required permission: saying administrators *can* perform an action
   establishes sufficiency, not necessarily the permission *required*.

They were identified after examining disagreements, so the exclusions are explicitly
post hoc. Frozen results retain them. The separate sensitivity analysis removes all
three families from every model, without changing any predictions or gold labels.
See [the errata](../../datasets/errata.json).

This matters for calibration too: four of Jev's five frozen-suite errors at probability
at least 0.9 came from the disputed retrieval family. After the exclusions, Jev has
one error among 441 predictions at that threshold; Clef has one among 424; Clef-flash
has five among 263. This synthetic distribution still cannot validate a deployment
threshold. It does show why bad reference labels can make a model appear overconfident.

## Cost, reliability, and reproducibility

All **1,632 planned requests** returned schema-valid responses. Jev required two
transport retries; neither Clef variant required a retry. The three preliminary smoke
calls also succeeded, giving 1,635 logical requests and 1,637 HTTP attempts overall.

Reported successful input usage implies approximately **$0.06584** for the main run:
$0.01127 Jev, $0.03969 Clef, and $0.01488 Clef-flash at the documented prices. The smoke
calls add approximately $0.00013. These are input-usage estimates, not a billing
statement; possible charges for unreported failed attempts and any discounts are unknown.

Jev was fastest and cheapest on this run from this machine. That differs from
Cloudflare's launch latency comparison, which used another deployment and measurement
setup. Our numbers include WAN latency, use sequential interleaved requests, and do not
measure sustained throughput or pure model inference speed. Hosted Clef weight revisions
cannot be pinned through the names used here; timestamps and returned model names are
preserved. Jev returned `jev-1.13.0` throughout.

The CPU Docker image was built and used. No local model image, checkpoint, GPU workload,
or benchmark-only host Python dependency was installed. The local GPU comparison remains
deferred. The raw archive can be rescored offline with:

```sh
benchmark/tools/offline.sh /work/tools/score.py \
  /work/reports/hosted-v1 --output /reports/hosted-v1
```

## What this says about adopting a decision model

The original question was whether a pretrained model can apply a company's definitions
without first receiving thousands of labeled tickets. This run supports that possibility
for short, explicit policies with the necessary facts supplied. It also shows that
service branding and schema compatibility do not imply equal behavior or transferable
probabilities.

It does not establish that any model can independently verify the facts in a real ticket.
Several fixtures explicitly state that evidence is verified; real applications must
supply or establish that evidence. For this suite, Jev and Clef are both credible
candidates. Choosing between them requires the actual project's cases and operating
constraints; the one-decision difference across all frozen variants is not a meaningful
general winner.
