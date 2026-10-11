"""Run a single pinned next-wave endpoint; lifecycle stays in run-next-wave.sh."""
import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import random
import time
from urllib.error import HTTPError
from urllib.request import Request, urlopen

from hosted import ROOT, digest, load_cases, normalized
from next_contract import REGISTRY, request_for, normalize_response, verify_health


def call(base, route, request=None):
    data = None if request is None else json.dumps(request, ensure_ascii=False).encode()
    try:
        with urlopen(Request(base + route, data=data, headers={'Content-Type': 'application/json'}), timeout=180) as response:
            return response.status, json.load(response)
    except HTTPError as e:
        raw = e.read().decode(errors='replace')
        try:
            raw = json.loads(raw)
        except ValueError:
            pass
        return e.code, raw


def run(args):
    config = REGISTRY[args.model]
    base = f'http://192.168.0.90:{config["port"]}'
    route = '/v1/classify' if config['interface'] == 'gliner' else '/v1/systemone'
    out = Path(args.output)
    out.mkdir(parents=True, exist_ok=True)
    rows, manifest = load_cases(args.dataset)
    if args.limit:
        rows = rows[:args.limit]
    provenance = json.loads((out/'container.json').read_text())
    if provenance['image'] != config['image'] or provenance['command'] != config['command']:
        raise ValueError('Container image/command differs from frozen registry')
    if provenance['running_benchmark_containers'] != ['dm-' + args.model]:
        raise ValueError('Expected exactly one active benchmark model')
    settings = {'models': [args.model], 'limit': args.limit, 'dataset_sha256': manifest['sha256'],
                'dataset_directory': str(Path(args.dataset).resolve()), 'registry': config,
                'runner_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                'contract_sha256': hashlib.sha256((ROOT/'tools/next_contract.py').read_bytes()).hexdigest(),
                'shared_runner_sha256': hashlib.sha256((ROOT/'tools/hosted.py').read_bytes()).hexdigest(),
                'max_attempts': 1, 'seed': 20261010, 'probability_semantics': 'native-label-confidence-only' if config['interface']=='gliner' else 'native-distribution'}
    meta = out/'run.json'
    if meta.exists():
        if json.loads(meta.read_text())['config'] != settings:
            raise ValueError('Resume configuration mismatch')
    else:
        meta.write_text(json.dumps({'started_at': datetime.now(timezone.utc).isoformat(), 'config': settings,
                                   'provenance': provenance}, indent=2)+'\n')
    # Independent readiness/warm-up ticket, never counted as a benchmark response.
    smoke = {'request': {'state': 'Please refund the duplicate payment.', 'questions': {'decision': {
        'type': 'choice', 'instructions': 'Route to the responsible department.',
        'criteria': {'billing': 'Payments and refunds', 'technical': 'Software faults'}}}}}
    for attempt in range(90):
        try:
            status, raw = call(base, route, request_for(smoke, args.model))
            if status == 503:
                time.sleep(2)
                continue
            if status != 200:
                raise ValueError(f'Warm-up HTTP {status}: {raw}')
            normalize_response(raw, smoke, args.model)
            (out/'warmup.json').write_text(json.dumps(raw, indent=2)+'\n')
            break
        except OSError:
            time.sleep(2)
    else:
        raise RuntimeError('Service did not become ready')
    if config.get('expected_health'):
        status, health = call(base, '/healthz')
        if status != 200:
            raise RuntimeError('Health provenance unavailable')
        verify_health(health, args.model)
        (out/'health-before.json').write_text(json.dumps(health, indent=2)+'\n')
    encodings = {}
    if config.get('encoding_evidence'):
        evidence = json.loads((ROOT/config['encoding_evidence']).read_text())
        encodings = {r['request_sha256']: r['input_tokens'] for r in evidence['records']}
        if any(digest(request_for(c, args.model)) not in encodings for c in rows):
            raise RuntimeError('Missing lossless-encoding evidence')
    path = out/'responses.jsonl'
    prior = [json.loads(line) for line in path.read_text().splitlines()] if path.exists() else []
    done = {r['case_id'] for r in prior}
    tasks = list(rows)
    random.Random(20261010).shuffle(tasks)
    for index, case in enumerate(tasks):
        if case['id'] in done:
            continue
        req = request_for(case, args.model)
        started = time.perf_counter()
        raw = parsed = error = None
        status = None
        try:
            status, raw = call(base, route, req)
            if status != 200:
                raise ValueError(f'HTTP {status}')
            parsed = normalize_response(raw, case, args.model)
            if encodings and parsed['usage'].get('input_tokens') != encodings[digest(req)]:
                raise RuntimeError('Scored token usage differs from verified complete encoding')
        except (ValueError, KeyError, TypeError, OSError) as exc:
            error = f'{type(exc).__name__}: {exc}'
        elapsed = time.perf_counter()-started
        record = {'model': args.model, 'case_id': case['id'], 'dataset_sha256': manifest['sha256'],
                  'request_sha256': digest(req), 'timestamp': datetime.now(timezone.utc).isoformat(),
                  'latency_seconds': elapsed, 'attempts': [{'status': status, 'seconds': elapsed}],
                  'response': raw, 'result': parsed, 'error': error}
        with path.open('a') as handle:
            handle.write(json.dumps(record, ensure_ascii=False)+'\n')
        if error or (index+1) % 50 == 0:
            print(f'{args.model} {index+1}/{len(tasks)} {error or "ok"}', flush=True)
        if status is None or status >= 500:
            raise RuntimeError('Infrastructure failure; partial response retained')
    if config.get('expected_health'):
        status, health = call(base, '/healthz')
        if status != 200:
            raise RuntimeError('Final health provenance unavailable')
        verify_health(health, args.model)
        (out/'health-after.json').write_text(json.dumps(health, indent=2)+'\n')
    print(args.model, 'complete', len(tasks), flush=True)


if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('--model', required=True, choices=REGISTRY)
    p.add_argument('--dataset', required=True)
    p.add_argument('--output', required=True)
    p.add_argument('--limit', type=int, default=0)
    p.add_argument('--execute', action='store_true')
    a = p.parse_args()
    if not a.execute:
        p.error('Requires --execute')
    run(a)
