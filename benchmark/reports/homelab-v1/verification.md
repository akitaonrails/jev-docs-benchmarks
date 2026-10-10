# Verification record

Completed 10 October 2026 by the benchmark agent.

| Claim | Evidence | Limit |
| --- | --- | --- |
| Same benchmark inputs | Frozen manifest verified; scorer recomputes every dataset/request hash; hosted/local Clef-flash payload hashes match for all 544 cases | Model-internal processing differs |
| No gold leakage in client payload | Payload allowlist tests; only state, questions and model serialized | Does not independently validate authored golds |
| Correct local checkpoint selection | Discovery plus per-response repo/revision/selector checks; serving source and image captured | Metadata is server-reported; no new full-weight hashing during timed run |
| Complete, valid run | 1,632 unique main records, six smoke records; all schema-valid; no retries/missing/errors | One main observation per fixture/model |
| Honest probability scoring | Shared hosted normalizer, raw responses retained; vendor confidence/action fields not substituted | Vendor rounding retained then normalized under the frozen tolerance |
| No hidden local price assumption | Local cost is null; test verifies no hosted price applied | Electricity/ownership costs unmeasured |
| Truncation visible | Native usage preserved; test verifies truncation/drop aggregation and unknown-field handling | Clef-flash omits telemetry |
| Existing hosted numbers preserved | Original hosted archive rescored and recursively compared with saved metrics at 1e-12 numeric tolerance; no changes | No new hosted calls |
| Reproducible artifacts | Gzip raw-content SHA-256 verified; unique IDs/counts checked; comparison generated offline | Narrative is an interpretation of the saved data |

All 14 offline unit tests passed in the CPU runner with networking disabled. Report
links resolve and `git diff --check` passed. All six smoke normalized results matched
their main-run counterparts. This is a limited repeat check, not proof of determinism.

The runtime image is existing Docker infrastructure. No benchmark-only packages were
installed on the workstation and no workstation GPU was allocated. The homelab's
already running service remains managed by its own project.
