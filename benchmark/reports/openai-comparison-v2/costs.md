# OpenAI Decisions cost reconciliation

Usage-based list-price valuation, not a verified invoice. The $20 account deposit is prepaid credit, not the cost of this test. Existing hosted results are reused without new requests.

| New run | Requests | Attempts | Input tokens | Known listed USD |
| --- | ---: | ---: | ---: | ---: |
| v1 | 544 | 544 | 151,230 | 0.015123 |
| v2 | 504 | 504 | 195,963 | 0.0195963 |
| Successful smoke (two questions) | 1 | 1 | 274 | 0.0000274 |

**Total known new usage: $0.0347467.** The initial unfunded probe returned no metered usage. Any prior retry attempts without usage are counted in costs.json; their charges cannot be reconstructed from a final response.

## Same compact bilingual cases

| Provider | Correct / 168 | Input tokens | USD per 1,000 classifications |
| --- | ---: | ---: | ---: |
| jev | 164/168 | 76,623 | 0.019156 |
| clef | 161/168 | 44,161 | 0.063087 |
| clef-flash | 147/168 | 44,161 | 0.009989 |
| openai-decisions | 152/168 | 39,169 | 0.023315 |

Rates: OpenAI Decisions $0.10/M input (verified 11 October UTC); Jev $0.042/M, Clef $0.24/M, Flash $0.038/M (10 October snapshot). All use zero output-token charges for these endpoints. Tokenizers and native request formats differ. Cloudflare free allowances, discounts, tax and local operating costs are excluded.

Sources: [OpenAI Decisions](https://developers.openai.com/api/docs/guides/decisions), [Jev](https://docs.typesafe.ai/models), [Clef](https://developers.cloudflare.com/workers-ai/models/clef/), [Flash](https://developers.cloudflare.com/workers-ai/models/clef-flash/).
