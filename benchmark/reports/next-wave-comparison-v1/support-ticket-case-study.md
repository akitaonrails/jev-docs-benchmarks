# Support severity: a concrete failure hidden by the average

The user's original example was company support tickets with company-specific
severity rules. The frozen v1 fixture `support_severity-04-original` demonstrates
why a supplied rubric still needs validation.

**Policy:** ongoing production data loss is critical. A production outage affecting
multiple customers is also critical. A single-customer outage below those criteria
is degraded.

**Record:** engineers confirm ongoing permanent loss of production records for
one customer. The expected answer is **critical**: the data-loss condition applies
independently of customer count.

| Observed answer | Tested configurations |
| --- | --- |
| Critical, as expected | Jev, hosted/local Clef-flash, Laya-typed, Simple-Jev, Laya multilingual |
| Degraded | Full hosted Clef, base Laya, Eikos 4B, Jebadiah 4B v2, Mapika Decider 4B, Kev 4B, Kev 9B |
| Unknown | Kev 0.8B |

This is a single synthetic case, not a production failure-rate estimate. It shows
that **a 27B model can miss a policy exception that some smaller configurations
handle**, and that aggregate accuracy alone does not establish reliable handling of
the errors a business cares about. The observations are consistent with several
models over-weighting the single-customer cue, but their internal reasoning is not
observable from these labels.

The other unambiguous critical original, `support_severity-02-original`, describes
three production tenants unable to check out even though the customer says there
is no rush. Base Laya answers degraded, Kev 0.8B/4B answer unknown, and multilingual
Laya answers routine. All other tested SystemOne configurations answer critical.

There are only **two undisputed critical originals**. A third authored critical
case, `support_severity-07`, was already flagged in the shared
[errata](../../datasets/errata.json) because impairment versus outage is ambiguous.
The report's primary three-case critical-miss count includes it; do not present
that count without this qualification. GLiNER did not run this suite.

## Practical implication

When impact facts are structured and trustworthy, encode exact severity rules in
code. If a model is needed to interpret free text, evaluate extraction of those
facts and the final routing separately, preserve missing information, and measure
critical under-triage explicitly. Decomposing extraction from deterministic rules
is a proposed workflow to test; this benchmark did not measure that intervention.

Source evidence: [frozen v1 cases](../../datasets/cases.jsonl),
[full expanded results](results.md), [new native response archives](../next-wave-v1/),
[original hosted archive](../hosted-v1/), and [original local archive](../homelab-v1/).
