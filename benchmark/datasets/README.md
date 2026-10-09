# Dataset v1

`scenarios.py` contains 130 authored examples and explicit fictional policies.
`build_dataset.py` expands them into `cases.jsonl`, whose SHA-256 is stored in
`manifest.json`. The fixture artifact was committed before the first inference call.

For each classification case:

- `request` is the only material sent to the model (plus its model selector).
- `gold` is the expected wire-format label; `semantic_gold` is its stable meaning.
- `semantic_map` allows opaque labels to be mapped back for scoring.
- `rationale` explains the authored answer under the policy.
- `family`, `domain`, and `variant` describe related cases for analysis.

For probability probes, `target` is an analytical probability, not a realized outcome.
A uniform choice among six outcomes has probability 1/6 for each. No invented future
observation is used as a gold answer.

The injected variant includes deliberately incorrect reviewer commentary. It is a
fixture attack, not a benchmark instruction. The trusted question explicitly tells
the evaluated model to ignore that commentary. Original option order is randomized
with a fixed seed; reverse order and opaque identifiers preserve the same meanings.

## Boundaries of the experiment

These cases measure applying a written rule to supplied facts. Many records explicitly
state which evidence is verified so that the expected answer is defensible. For
example, an email case can state that impersonation was independently verified. A
correct classification does NOT establish that the model could independently detect
impersonation from a real raw email. Likewise, "attached evidence is complete" is a
fact in a routing fixture, not an actual attachment the model is asked to analyze.

All policies are fictional operational definitions. Moderation, refund, lead scoring,
and approval examples are not legal or industry-standard requirements. Scope is
short English text; no tools, live websites, customer data, long documents, or images.

Golds are AI-authored with author review, not independently human-adjudicated. Three
ambiguous families found after inference began are disclosed in `errata.json`. They
remain in frozen primary scores and are excluded only in a separately labeled
sensitivity analysis. More sophisticated real-world cases may behave very differently.

There is no training split or prompt optimization against these cases. All are tests.
Once someone tunes to this suite, it becomes development data for that entrant.
