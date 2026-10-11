# OpenAI Decisions execution evidence

- `smoke.json`: initial independent request, rejected with exhausted API credit.
- `smoke-funded.json`: independent choice/predicate request after account funding;
  valid HTTP 200, 274 input tokens. Excluded from benchmark accuracy.
- `client.json`: Docker image identity and offline verification count.
- `completion.json`: scored counts, times, served alias, protocol freeze and usage.

Scored inference ran from 02:42:33 to 02:46:42 UTC on 11 October 2026, approximately
four minutes, sequentially within each suite (v2, then v1). All 1,048 requests
succeeded in one attempt. The client used no GPU or host-installed benchmark packages.
Earlier entrants were not queried again. Offline archive/request-hash checks and
regression comparisons preserved the previous v1/v2 accuracy, counts and Brier values.

[Protocol](../../openai-decisions/README.md) · [analysis](../openai-comparison-v2/analysis.md)
· [listed usage cost](../openai-comparison-v2/costs.md).
