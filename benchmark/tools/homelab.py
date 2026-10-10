"""Run frozen cases against the isolated homelab SystemOne service (no credentials)."""
import argparse
from datetime import datetime, timezone
import hashlib
import http.client
import json
from pathlib import Path
import random
import time
from urllib.parse import urlsplit
from urllib.request import urlopen

from hosted import ROOT, LOCAL_MODELS, digest, load_cases, normalized, payload


def validate_server(body, model, pins):
    metadata = body['server']
    expected = pins[LOCAL_MODELS[model][0]]
    if any(metadata.get(k) != expected[k] for k in ('repo', 'revision')):
        raise ValueError('Checkpoint provenance mismatch')
    if metadata.get('selector') != LOCAL_MODELS[model][0]:
        raise ValueError('Selector mismatch')
    if not str(metadata.get('device', '')).startswith('cuda'):
        raise ValueError('GPU device not reported')


def run(args):
    rows, manifest = load_cases(getattr(args, 'dataset', None))
    if args.smoke:
        rows = [rows[0], next((c for c in rows if c['kind'] == 'probability' and c['variant'] == 'noul'), rows[1])]
    url = urlsplit(args.base_url)
    if url.scheme != 'http' or url.hostname != '192.168.0.90' or url.port != 11436 or url.path not in ('', '/'):
        raise ValueError('This adapter only permits the configured homelab service')
    pins = json.loads((ROOT / 'models.json').read_text())
    environment = {}
    for route in ('healthz', 'v1/models'):
        with urlopen(args.base_url.rstrip('/') + '/' + route, timeout=10) as response:
            environment[route] = json.load(response)
    for model in args.models:
        selector = LOCAL_MODELS[model][0]
        if any(environment['v1/models'][selector].get(k) != pins[selector][k] for k in ('repo', 'revision')):
            raise ValueError('Model discovery disagrees with pinned snapshots')
    if not environment['healthz']['cuda_available']:
        raise ValueError('GPU unavailable')
    output = Path(args.output)
    output.mkdir(parents=True, exist_ok=True)
    config = {'dataset_sha256': manifest['sha256'], 'models': args.models,
              'limit': len(rows) if args.smoke else 0, 'case_ids': [c['id'] for c in rows],
              'seed': 20261009, 'max_attempts': 1, 'timeout_seconds': 180,
              'base_url': args.base_url, 'pins': pins,
              'dataset_directory': str(Path(args.dataset).resolve()) if getattr(args, 'dataset', None) else str(ROOT / 'datasets'),
              'runner_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
              'shared_runner_sha256': hashlib.sha256((ROOT / 'tools/hosted.py').read_bytes()).hexdigest()}
    meta = output / 'run.json'
    if meta.exists():
        if json.loads(meta.read_text())['config'] != config:
            raise ValueError('Resume configuration mismatch')
    else:
        meta.write_text(json.dumps({'started_at': datetime.now(timezone.utc).isoformat(),
                                   'config': config, 'environment': environment}, indent=2) + '\n')
    path = output / 'responses.jsonl'
    prior = [json.loads(line) for line in path.read_text().splitlines()] if path.exists() else []
    done = {(r['model'], r['case_id']) for r in prior}
    tasks = [(model, case) for case in rows for model in args.models]
    random.Random(20261009).shuffle(tasks)
    for index, (model, case) in enumerate(tasks):
        if (model, case['id']) in done:
            continue
        request = payload(case, model)
        start = time.perf_counter()
        raw = parsed = error = None
        attempts = []
        conn = http.client.HTTPConnection(url.hostname, url.port, timeout=180)
        try:
            conn.request('POST', '/v1/systemone', body=json.dumps(request, ensure_ascii=False).encode(),
                         headers={'Content-Type': 'application/json'})
            response = conn.getresponse()
            data = response.read()
            attempts.append({'status': response.status, 'seconds': time.perf_counter() - start})
            raw = json.loads(data)
            if response.status != 200:
                raise ValueError(f'HTTP {response.status}')
            validate_server(raw, model, pins)
            parsed = normalized(raw, case)
        except (ValueError, KeyError, TypeError, ZeroDivisionError, OSError, http.client.HTTPException) as exc:
            error = f'{type(exc).__name__}: {exc}'
            if not attempts:
                attempts.append({'error': type(exc).__name__, 'seconds': time.perf_counter() - start})
        finally:
            conn.close()
        record = {'model': model, 'case_id': case['id'], 'request_sha256': digest(request),
                  'dataset_sha256': manifest['sha256'], 'timestamp': datetime.now(timezone.utc).isoformat(),
                  'latency_seconds': time.perf_counter() - start, 'attempts': attempts,
                  'result': parsed, 'error': error, 'response': raw}
        with path.open('a') as handle:
            handle.write(json.dumps(record, ensure_ascii=False) + '\n')
            handle.flush()
        if error or (index + 1) % 60 == 0 or args.smoke:
            print(f'{index + 1}/{len(tasks)} {model} {case["id"]}: {error or "ok"}', flush=True)
        # Invalid schema is scored as failure; infrastructure/provenance failure stops the run.
        if error and (raw is None or not isinstance(raw, dict) or 'server' not in raw
                      or any(word in error for word in ('mismatch', 'GPU device'))):
            raise SystemExit('Stopped after infrastructure/provenance failure; inspect preserved response')
    print('Completed', len(tasks), 'planned requests', flush=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--base-url', default='http://192.168.0.90:11436')
    parser.add_argument('--models', nargs='+', choices=LOCAL_MODELS, default=list(LOCAL_MODELS))
    parser.add_argument('--output', required=True)
    parser.add_argument('--dataset', help='Frozen dataset directory; defaults to v1')
    parser.add_argument('--smoke', action='store_true')
    parser.add_argument('--execute', action='store_true')
    args = parser.parse_args()
    if not args.execute:
        parser.error('Inference requires --execute')
    run(args)
