# Hosted v2 verification and usage value

Completed **10 October 2026, 04:23:55–04:33:03 UTC**. Jev, Clef and Clef-flash each
returned 504 valid responses: **1,512 total**, one attempt each, no provider stop,
retry, invalid result, or interrupted attempt. Jev reported `jev-1.13.0`; Cloudflare
reported its service aliases. Hosted aliases do not pin immutable weights.

The frozen dataset was committed as `f0ceb55` before inference. Its SHA-256 is
`a89ae706767f5d7f79e4ea2898e39065e6e95d3d7fe3e5c71517514bceb7420a`.
The recorded runner hash matches the committed inference source. The offline scorer
verified the uncompressed [response archive](responses.jsonl.gz) hash, every request
hash, the full unique case set, and the dataset hash. See [archive.json](archive.json),
[run.json](run.json), and [client image ID](docker-image-id.txt).

The [combined report](../comparison-v2/analysis.md) contains the findings and ranking;
[summary.json](../comparison-v2/summary.json) retains per-language/condition usage.
Using the [10 October official-rate snapshot](../../pricing/2026-10-10.json):

| Model | Reported input tokens | USD / million input | Listed usage value |
| --- | ---: | ---: | ---: |
| Jev | 312,237 | $0.042 | $0.013113954 |
| Clef | 213,111 | $0.24 | $0.051146640 |
| Clef-flash | 213,111 | $0.038 | $0.008098218 |
| **Total** | | | **$0.072358812** |

Outputs are free at these published rates. Usage is present for every request. These
are pre-allowance values, not verified charges. Cloudflare's shared 10,000-neuron
daily allowance and other account activity affect billing. The earlier dated
[pricing audit](../hosted-v1/pricing.md) explains those uncertainties; the current
snapshot records the subsequently observed Flash price reduction. The runner's
conservative cap uses the original higher Flash rate and is not the valuation.
No billing-dashboard or invoice reconciliation was performed.
