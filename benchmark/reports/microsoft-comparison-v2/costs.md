# Microsoft and hosted workload costs

Rates checked 11 October 2026. Compact v2 uses the same 168 paired-language cases per model. Values exclude allowances, taxes and credit purchase fees. Local operating cost is unmeasured.

| Hosted model | Correct / 168 | Input tokens | USD / 1,000 calls | USD / 1,000 observed correct |
| --- | ---: | ---: | ---: | ---: |
| jev | 164 | 76623 | $0.01916 | $0.01962 |
| microsoft-decision-1 | 164 | 25789 | $0.00645 | $0.00660 |
| clef | 161 | 44161 | $0.06309 | $0.06583 |
| openai-decisions | 152 | 39169 | $0.02331 | $0.02577 |
| clef-flash | 147 | 44161 | $0.00999 | $0.01142 |

Cost per observed correct label does not include review or error damage, and does not mean correct answers can be identified in advance.

## This Microsoft execution

| Suite | Requests | Input tokens | OpenRouter reported USD |
| --- | ---: | ---: | ---: |
| v1 | 544 | 105269 | $0.004421298 |
| v2 | 504 | 159801 | $0.006711642 |

Scored total: **$0.011132940**. Including the separately observed smoke: **$0.011135376**.

Every scored usage.cost equals input_tokens × $0.042/M. This is reported successful-response usage, not a reconciliation of the full account invoice. Ten v2 HTTP 429 attempts preceded successful retries; the runner preserves their status and timing but no separate billing usage, so any failed-attempt charges are unverified. Earlier hosted figures are list-price valuations of their archived usage. Cloudflare free allowances can lower actual bills.

[Rate snapshot](../../pricing/2026-10-11-microsoft.json), [verification](verification.json), [OpenRouter price](https://openrouter.ai/microsoft/microsoft-decision-1).
