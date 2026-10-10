# Homelab v2 verification

Run completed **10 October 2026, 04:23:55–04:30:23 UTC**: 1,512 requests,
504 each for Laya, Laya-typed and local Clef-flash. All responses were valid,
with no retry or cold load. The client checked every selector, repository,
pinned revision and GPU parameter device before accepting the response.

- Dataset frozen in commit `f0ceb55` before inference; SHA-256
  `a89ae706767f5d7f79e4ea2898e39065e6e95d3d7fe3e5c71517514bceb7420a`.
- Recorded runner and shared adapter hashes match the source used for this run.
- [Run configuration](run.json) records the live health/model-discovery replies;
  all three models were already loaded on the AMD device.
- [Archive metadata](archive.json) hashes the uncompressed raw responses.
  The offline scorer verifies that hash, every request hash, the complete case
  set, unique records and the frozen dataset hash.
- [Client image ID](docker-image-id.txt) identifies the CPU runner container.
  The model server is the same deployment described in the
  [v1 environment capture](../homelab-v1/environment.md), using the
  [captured app](../homelab-v1/server-app.py) and pinned model snapshots.
- Sixteen offline tests passed, including bilingual gold/order parity, fixed
  dataset regeneration, example/test separation and payload metadata exclusion.

Input truncation is recorded in the [results](results.md), separately from
schema validity. A valid response does not imply the full input was retained.
No changes to model weights, prompts or gold answers were made after viewing outputs.
The newer [setup template](../../../docs/setup.md) was checked against this deployment;
it was not used to redeploy the running server.
