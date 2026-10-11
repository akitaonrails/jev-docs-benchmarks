# OpenAI Decisions benchmark protocol

Compare the native `POST https://api.openai.com/v1/decisions` endpoint, model
`gpt-6-luna`, with the existing frozen v1 and bilingual v2 suites. Entrant ID:
`openai-decisions`. No fine-tuning, threshold fitting, or gold-guided prompt tuning.

## Access and current status

The first independent access probe returned HTTP 429,
`insufficient_quota` / `credit_balance_exhausted`. The account was then funded;
the repeated independent probe returned HTTP 200 with valid choice and predicate
answers. Both are retained in [runtime evidence](../reports/openai-decisions-runtime/).
No scored calls had been made when this protocol was frozen. Codex subscription
access is separate from Platform API credentials and billing.

## Mapping fixed before inference

- Only `case.request` is read. IDs, golds, rationales and semantic maps stay local.
- String state becomes `input` unchanged; structured state is serialized as JSON.
- Choice instructions, option order, opaque IDs and descriptions are preserved.
  The named SystemOne question becomes one native `choice` question named `decision`.
- Noul maps to `predicate`. Its original instructions are followed by
  `\nCriteria: ` and the original criteria as JSON, retaining both event descriptions.
- Native probabilities are used for Brier/calibration and probability probes.
  The separate native `confidence` is archived but does not replace probabilities.
- Refusals and malformed answers count as failures, not abstention labels.
- One case per request, sequential requests, persistent HTTPS connection, seeded
  order, up to three attempts for transient errors as in the original hosted runner.
  Exhausted billing quota stops immediately. Partial runs cannot be archived as complete.
- No tools, retrieval, images, generated explanations or calls through Codex.
  Choice is used even for severity to preserve the original categorical scoring.

## Verification

The adapter tests cover both complete frozen datasets for evidence, rubric and
option preservation and exclusion of answer metadata. Response tests reject
missing/duplicate labels, invalid probabilities, wrong question names, wrong
answer types and refusals. An independent two-question smoke request checks
native choice/predicate access before any scored call. Archive hashes and request
hashes are checked by the existing scorers. Existing entrants are reused from
archives; they are not rerun or rescored with changed labels.

## Run in Docker

Use the existing `jev-benchmark-runner` image and export a funded `OPENAI_API_KEY`.
No host Python packages or local model installations are needed. The host shell
must have the key exported; no credential values belong in commands or reports.
From the repository root:

```sh
# Independent access/contract check; use a fresh output file after the failed probe.
benchmark/openai-decisions/run.sh smoke /results/openai-smoke-funded.json
benchmark/openai-decisions/run.sh v1 /results/openai-decisions-v1
benchmark/openai-decisions/run.sh v2 /results/openai-decisions-v2
# Only after both runs complete:
benchmark/openai-decisions/score.sh
```

The scoring command archives the standard result paths above and combines all
previous entrants into new `openai-comparison-v1` and `openai-comparison-v2`
reports. Earlier reports remain dated snapshots. Each scored run has a $5
conservative input reservation cap (bytes plus overhead, up to three attempts),
not a guaranteed billing ceiling. Actual listed cost is computed from returned
usage, with smoke and retried attempts reported separately.

## Sources and pricing

- [Official guide](https://developers.openai.com/api/docs/guides/decisions): public
  beta, native typed decisions, $0.10/M input tokens, no output charge. Regional
  and long-context adjustments are outside this short, global-endpoint protocol.
- [API schema](https://developers.openai.com/api/reference/resources/decisions/methods/create):
  native question/answer fields, per-option probabilities and refusals.
- [Authentication](https://learn.chatgpt.com/docs/auth): Platform API credentials
  and billing are distinct from ChatGPT/Codex subscription authentication.
- [Dated price snapshot](../pricing/2026-10-11.json).

The provider's “10x faster” statement compares against its Responses API. This
benchmark has no matched Responses run and cannot verify that claim.
