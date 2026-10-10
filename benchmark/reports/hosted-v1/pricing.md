# Pricing verification and test cost

Verified **9 October 2026**, in USD. **The main run plus smoke tests represent
$0.065970726 of successful usage at published token rates (about 6.60 US cents).
Actual account charges have not been verified.** Cloudflare's free allocation can
make its portion zero; Jev credits and two interrupted attempts remain unreconciled.

## Subsequent price observation: 10 October

Clef-flash now lists **$0.038/M input tokens**, versus the $0.09/M observed below.
The precise billing effective time is unknown. This document preserves the original
rate snapshot; it does not establish an invoice or today's cheapest provider.
See the [current cost-benefit ranking](../../../docs/cost-benefit-ranking.md) and
[updated rate snapshot](../../pricing/2026-10-10.json). Cloudflare's model pages now
explicitly confirm free output tokens for both Clef variants.

## Confirmed public rates (9 October snapshot)

| Service | Model requested | USD / million input tokens | Output treatment |
| --- | --- | ---: | --- |
| TypeSafe | `jev-1.13.0` | $0.042 | Explicitly free |
| Cloudflare | `@cf/cloudflare/clef` | $0.240 | Input-only published price; zero reported output tokens in this run |
| Cloudflare | `@cf/cloudflare/clef-flash` | $0.090 | Input-only published price; zero reported output tokens in this run |

TypeSafe lists $42 per **billion**, equivalent to $0.042 per million input tokens,
and explicitly makes output tokens free. Its state can be shared across multiple
questions, but our requests each contained one question. [TypeSafe model documentation](https://docs.typesafe.ai/models).
Cloudflare's model pages confirm the other two rates:
[Clef](https://developers.cloudflare.com/workers-ai/models/clef/),
[Clef-flash](https://developers.cloudflare.com/workers-ai/models/clef-flash/).

## Reconciliation from saved responses

Formula: reported successful input tokens × published USD per million / 1,000,000.
Digits below preserve arithmetic reproducibility; they do not imply invoice precision.
The 544 main requests per model include 520 classifications and 24 probability probes.

| Model | Main input tokens | Main list value | Smoke input tokens | Smoke list value | Combined list value |
| --- | ---: | ---: | ---: | ---: | ---: |
| Jev | 268,356 | $0.011270952 | 502 | $0.000021084 | $0.011292036 |
| Clef | 165,373 | $0.039689520 | 320 | $0.000076800 | $0.039766320 |
| Clef-flash | 165,373 | $0.014883570 | 320 | $0.000028800 | $0.014912370 |
| **Total** | | **$0.065844042** | | **$0.000126684** | **$0.065970726** |

Jev also reported 24,015 output tokens including smoke; their listed cost is zero.
All 1,635 successful logical requests supplied usage. There were 1,637 HTTP attempts.
Source archives: [main](responses.jsonl.gz), [smoke](../smoke-v1/responses.jsonl.gz).
[Machine-readable reconciliation](pricing.json) records their SHA-256 hashes, rates,
counts and UTC dates. Reproduce without network or GPU access:

```sh
benchmark/tools/offline.sh /work/tools/costs.py
```

## Cloudflare allowance and billing units

Cloudflare bills neurons: $0.011/1,000, with 10,000 free daily on Free and Paid
Workers plans, resetting at 00:00 UTC. Clef uses 21,818 neurons/million input tokens;
Clef-flash uses 8,182. These are rounded equivalents of the token prices.
[Official Workers AI pricing](https://developers.cloudflare.com/workers-ai/platform/pricing/).

Both models combined, including smoke, imply **4,970.79 neurons** on 9 October UTC.
The allowance is shared; do not assign 10,000 separately to each model.

- With no other Workers AI usage that day, this test's Cloudflare charge would be **$0**.
- With the allowance already exhausted on a paid plan, the estimated incremental
  charge would be **$0.05467869** for both models together.
- Partial remaining allowance gives an intermediate amount. Other account usage is unknown.

For other same-day usage O and benchmark usage B, estimated incremental paid-plan
neurons are `max(0, O+B-10000) - max(0, O-10000)`. This estimates an allocation of
cost to the test; it is not a dashboard measurement. No account billing export was read.

## Interrupted requests and other adjustments

Jev had two `RemoteDisconnected` attempts without usage, followed by successful retries:
`support_routing-02-reordered` and `request_routing-06-opaque`. Their billing status
is unknown. If both were processed once and each consumed the same input tokens as
its successful retry (498 and 514), the additional list value would be **$0.000042504**.
This is a conditional calculation, not an observed charge or a guaranteed bound.
Cloudflare required no retries.

No TypeSafe account-credit balance, negotiated discount, invoice, tax or currency
conversion was verified. The harness called the providers directly; it deployed no
Worker and used no AI Gateway. Existing subscriptions and local CPU/network costs
are outside this marginal API comparison. The runner's $5 reservation cap is a
conservative execution guard, not measured consumption or a charge.

## What comparison is justified?

At list price, Clef cost **3.52×** Jev for this main workload, and Clef-flash **1.32×**.
Comparing only per-token rates would suggest 5.71× and 2.14×, but Jev reported about
1.62× as many input tokens for the equivalent cases. Tokenization and provider request
representation affect the bill; a fixed number of words is not a fixed billed token count.
Jev had the lowest list-price usage valuation. Cloudflare can have the lowest cash
charge for this small test after its daily allowance. This replaces any unqualified
claim that Jev was “cheapest.”

For publication, say: **“Successful calls, including smoke tests, were valued at
$0.01129 for Jev, $0.03977 for Clef and $0.01491 for Clef-flash at published rates.
Cloudflare usage fits within one daily free allowance if unused by other workloads.
Actual invoiced charges and Jev's interrupted-attempt charges were not verified.”**

To confirm cash expense, reconcile the 9 October UTC Workers AI dashboard neuron
usage and remaining allowance with account billing, and obtain TypeSafe's usage/credit
ledger for the same period. Keep unrelated calls separate and resolve the two Jev
attempts. Only then replace the current `actual_invoice_verified: false` status.
