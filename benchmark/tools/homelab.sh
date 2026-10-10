#!/bin/sh
set -eu
bench_dir=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
exec docker run --rm --read-only --cap-drop ALL \
  --security-opt no-new-privileges:true --tmpfs /tmp \
  --user "$(id -u):$(id -g)" \
  -v "$bench_dir:/work:ro" -v "$bench_dir/results:/results" \
  jev-benchmark-runner /work/tools/homelab.py "$@"
