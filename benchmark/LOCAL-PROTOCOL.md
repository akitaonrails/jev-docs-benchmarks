# Homelab extension to frozen protocol v1

Authorized 10 October 2026. This extends [the hosted protocol](PROTOCOL.md) without
changing its dataset, labels, prompts, scoring or gold-ambiguity exclusions.

- Entrants: `laya`, `laya-typed`, `clef-flash-local`. Snapshot revisions are pinned in
  `models.json` and checked against discovery and every response. Local Clef-flash is
  distinct from the hosted alias; matching model names do not prove identical weights.
- Endpoint: the isolated ROCm service at `192.168.0.90:11436/v1/systemone`.
  Client runs in the existing CPU Docker container; workstation GPU is unused.
- One question/request, identical payload allowlist. All 544 cases per model, seeded
  sequential interleaving, one HTTP connection per request. No concurrency or throughput
  measurement. Models were already loaded by homelab smoke tests; this is a warm run.
- Six preliminary requests: first classification and first Noul probe per model.
  Smoke outputs are archived separately, excluded from main metrics; no tuning follows.
- No automatic retries. Timeout is 180 seconds. Transport/provenance failures stop;
  malformed model outputs remain failures. Resuming skips all persisted records,
  including errors, and requires matching dataset, request IDs, pins and runner hashes.
- Archive native responses including server metadata and usage. Validate the same
  probability bounds and rounding tolerance as hosted. Use option probabilities for
  calibration, never Laya's separate confidence/action signals.
- Report truncation flags, dropped state tokens and truncated question IDs. If reported,
  retain cases in primary metrics and distinguish contextual limits from classification
  failure; never rewrite inputs to hide truncation. Missing truncation telemetry is
  unknown, not proof of no truncation.
- Report client wall time and server-reported prediction time separately. Server timing
  is not independently instrumented GPU kernel time. LAN/AMD/PyTorch timings are not
  directly equivalent to WAN/cloud deployment timings. Other server workloads may run.
- API token price does not apply locally. Electricity, hardware amortization and
  operational cost are unmeasured, so local cost is unknown rather than zero.

Verification: payload allowlist and probability/provenance tests; six live smoke calls;
complete matrix with no duplicate IDs, dataset/request hashes validated by offline
scoring; all errors retained; archived usage inspected for truncation. The existing
hosted archives must rescore to the same numeric metrics after scorer generalization.
