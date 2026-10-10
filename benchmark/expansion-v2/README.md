# v2: paired English / Brazilian Portuguese expansion

**Scope:** 84 new authored scenarios × two languages × three conditions = **504
classification requests per entrant**, 3,024 across the six existing entrants.
This is a separate experiment from v1. It must not be averaged into the v1 headline.

The purpose is to identify task/condition-specific strengths and language differences,
including opportunities for open models to match hosted proprietary models. There is
no requirement that any particular model win. Clef/Clef-flash are themselves open-weight
models; hosted versus local is a separate axis from open versus proprietary.

## What v1 missed

V1 tested short English records with explicit operational rules and adversarial
variants. It gave evidence about those policies, but little about ordinary semantic
classification, Portuguese, worked examples, distracting context or fine-tuning.
More v1 paraphrases would not resolve those gaps. V2 adds:

| Task | Main difficulty |
| --- | --- |
| Sentiment | Writer versus quotation, negation, sarcasm, mixed aspects |
| Current intent | Withdrawn requests, competing actions, hypothetical requests |
| Entailment | Quantifiers, implication direction, missing facts, temporal order |
| Retrieval relevance | All/some/none of the requested information; lexical distractors |
| Data handling | Fictional secrets versus mentions/redaction/revocation; rule priority |
| Current incident status | Timeline order, verified versus unverified, conflicts |
| Threshold policy | Inclusive bounds, units, intervals, AND/OR with missing values |

There are 12 originals per task. The native EN and PT-BR versions preserve the rule,
expected answer and option order. All task instructions, criteria, examples and records
are translated; opaque `c0` etc. wire IDs remain identical to avoid English label names
confounding the comparison. Portuguese uses natural Brazilian phrasing and decimal
commas where appropriate. It is not independently human-adjudicated translation.

## Conditions

- **compact:** short target record and rubric, no demonstrations.
- **examples:** same record/rubric plus one distinct worked example per class. No
  training or weight changes. Demonstrations are fixed before inference and shared
  across entrants; they do not disclose the current test answer.
- **distractors:** same rubric, with ten irrelevant archive sentences before the target.
  This deliberately increases context length and places decisive information last.
  It is a context stress condition, not an attempt to make small models look equivalent
  when their input is silently cut. Truncation and missing telemetry must be reported.

The gold follows only the stated rubric. Examples include an invented privacy policy,
not legal advice or real personal data. All credential-like strings are fictional.
Every request is generated from `request` alone; no gold, rationale or case ID is sent.

## Evaluation fixed before inference

Report each model by **task × language × condition**. Do not bury a small-model win in
one overall mean, or label a numerical tie proof of equivalence. Keep compact results
as the primary language comparison; demonstrations and context stress are separate.

For each EN/PT pair report both-correct, EN-only correct, PT-only correct, both-wrong,
and semantic prediction agreement. Compute the paired accuracy difference PT minus EN
with a descriptive bootstrap over authored families. Do the same task pairing across
models. Only 12 families/task means wide uncertainty; clearly label exploratory wins.

Also report per-condition accuracy, per-task majority and uniform baselines, Brier/ECE,
wall median/p95, input usage, dated hosted price valuation, dropped tokens, truncation
flags and missing telemetry. Charge estimates must use each provider's reported tokens;
Portuguese can change token consumption. Local compute cost is unmeasured.

Use the existing six entrants and pinned local snapshots. These Laya checkpoints are
English and typed-decisions variants; they do not represent the separate multilingual
checkpoint. No new checkpoints, fine-tuning, images, batching or throughput experiment
is included. Those would need separate protocols and configuration-specific results.

Freeze `cases.jsonl` and its SHA-256 in Git before inference. Retain all failures and
raw native outputs. No prompt editing or favorable-case selection after viewing outputs.
Validation checks bilingual gold/order parity, example/test separation, unique IDs,
expected counts, baseline balance, request allowlist and frozen hash. All content is
synthetic and some within-task cases are related; translations/conditions are not new
independent observations.
