# Microsoft Decision-1: original policy suite

11 October 2026. Same 544 frozen requests through OpenRouter/Azure: 520
classification variants and 24 separate uncertainty probes. All valid, one attempt
each. No input tuning. [Protocol](../../microsoft/README.md), [full comparison](results.md).

## Classification and robustness

Microsoft scores **124/130 originals (95.4%)** and **496/520 variants (95.4%)**.
Jev has 125/130 originals and Perplexity 129/130. With the same three disputed
families excluded for every entrant, Microsoft scores **123/127 originals** and
**492/508 variants**. No golds were changed after this run.

All five counterfactual rule pairs are correct. Reordered options and the tested
injected commentary each preserve all 130 original semantic predictions. Opaque
option names preserve 128/130; one correct answer becomes wrong and one wrong
answer becomes correct. These fixtures are not an exhaustive injection attack.

## What the errors mean

Six original failures:

| Case | Expected → predicted | Interpretation |
| --- | --- | --- |
| `support_severity-07` | critical → degraded | Existing ambiguity: invoice-export impairment in two tenants versus a production outage. |
| `retrieval_relevance-03` | answer → partial | Existing ambiguity: administrators can execute a command versus permission explicitly required. |
| `refund_policy-07` | deny → review | Known age of 30 days already excludes a refund; unknown usage cannot change eligibility. |
| `document_type-10` | invoice → unknown | Operative payment demand should dominate an explicitly quoted training example. |
| `incident_escalation-09` | investigate → escalate | One confirmed tenant down and the second unknown do not establish the two-tenant threshold. |
| `tool_approval-09` | review → block | Writing outside scratch needs review under the supplied rule; only specified actions are blocked. |

Both undisputed critical support originals are recognized; the third critical gold
is the disputed feature-outage case. All four explicitly blocked tool originals
avoid false allowance. These tiny counts do not establish production safety.

## Probability probes and latency

Choice uncertainty MAE is **0.1253**; Boolean/Noul MAE is **0.3690** across twelve
probes each. A fair binary event receives a Noul estimate of **0.8670** rather than
0.5; a one-in-four event receives **0.6792** rather than 0.25. A useful classifier
can therefore remain unsuitable as an unvalidated event-probability estimator.

Observed median/p95 end-to-end latency is **403/476 ms**. The run includes
OpenRouter and Azure routing; prior entrants were tested at other times and with
different deployments. This does not isolate model inference speed.

105,269 reported input tokens cost **$0.004421298**, exactly the sum of reported
usage costs at $0.042/M. [Combined costs](../microsoft-comparison-v2/costs.md),
[verification](../microsoft-comparison-v2/verification.json), [raw archive](../microsoft-v1/archive.json).
