# Local run completed

On 10 October 2026, the AMD homelab completed all 544 requests for each of Laya,
Laya-typed and pinned Clef-flash: **1,632 valid responses, no errors or retries**.
Six separate [smoke responses](../homelab-smoke-v1/responses.jsonl.gz) also passed.

- [Full hosted-versus-local analysis](../comparison-v1/analysis.md)
- [Local metrics](results.md) and [machine-readable summary](summary.json)
- [All classification errors](errors.jsonl)
- [Raw native responses](responses.jsonl.gz) and [archive hashes](archive.json)
- [Actual server environment and implementation](environment.md)
- [Verification record](verification.md)
- [Local execution protocol](../../LOCAL-PROTOCOL.md)

Both Laya variants scored 38.5% across 520 classification variants; local Clef-flash
scored 89.0% and matched every hosted Clef-flash classification label. See the full
analysis for original-only results, chance baselines, policy failures, uncertainty
probes, truncation reporting, timing and cost limitations.
