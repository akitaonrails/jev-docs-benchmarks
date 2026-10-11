# Pricing recheck: 11 October 2026

Official rates remain unchanged from the previous snapshot:

| Service | USD / million input tokens | Output fee | Primary source |
| --- | ---: | ---: | --- |
| Jev | 0.042 | 0 | [TypeSafe](https://docs.typesafe.ai/models) |
| Clef | 0.240 | 0 | [Cloudflare Clef](https://developers.cloudflare.com/workers-ai/models/clef/) |
| Clef-flash | 0.038 | 0 | [Cloudflare Flash](https://developers.cloudflare.com/workers-ai/models/clef-flash/) |
| OpenAI Decisions | 0.100 | 0 | [OpenAI guide](https://developers.openai.com/api/docs/guides/decisions) |

Cloudflare still lists 21,818 / 3,455 neurons per million input tokens for
Clef / Flash, 10,000 daily free neurons and $0.011 per 1,000 neurons above the
allowance. [Billing source](https://developers.cloudflare.com/workers-ai/platform/pricing/).
OpenAI figures cover our short text global requests; regional and long-context
multipliers are outside this suite.

The [new snapshot](../pricing/2026-10-11-perplexity.json) preserves the earlier files.
Combined scoring revalues the same archived usage at these unchanged rates. No
hosted API calls are needed to add Perplexity's local results. Electricity, hardware,
operations and utilization are unmeasured, so local dollar totals remain unknown.
This is neither an invoice audit nor a test of a hosted Perplexity service.
