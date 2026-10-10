"""Capture native API contracts using an independent, unscored smoke ticket."""
import json
import sys
import time
from pathlib import Path
from urllib.request import Request, urlopen
from urllib.error import HTTPError

model, port = sys.argv[1:]
base = 'http://192.168.0.90:' + port
out = Path('/results/next-wave-smoke') / model
out.mkdir(parents=True, exist_ok=True)
for attempt in range(90):
    try:
        with urlopen(base + '/v1/models', timeout=5) as r:
            discovery = json.load(r)
        break
    except HTTPError as e:
        if e.code == 404:
            discovery = {'discovery_status': 404, 'note': 'Native runtime has no /v1/models; provenance captured through container command and image.'}
            break
        time.sleep(2)
    except OSError:
        time.sleep(2)
else:
    raise SystemExit('Service did not become ready')
(out / 'models.json').write_text(json.dumps(discovery, indent=2))
question = {'type': 'choice', 'instructions': 'Route this support request to the responsible department.',
            'criteria': {'billing': 'Payments and refunds', 'shipping': 'Delivery and tracking', 'technical': 'Software problems'}}
state = 'I was charged twice. Please refund the duplicate payment.'
request = {'model': model, 'state': state, 'questions': {'decision': question}}
route = '/v1/systemone'
if model.startswith('gliner'):
    route = '/v1/classify'
    request = {'text': state, 'tasks': {'decision': {'labels': question['criteria'], 'prompt': question['instructions'], 'multi_label': False}}, 'include_confidence': True}
for i in range(2):
    t = time.perf_counter()
    for ready_attempt in range(90):
        try:
            with urlopen(Request(base + route, data=json.dumps(request).encode(), headers={'Content-Type': 'application/json'}), timeout=180) as r:
                response = json.load(r)
                status = r.status
            break
        except HTTPError as e:
            status = e.code
            response = e.read().decode()
            if status != 503:
                break
            time.sleep(2)
    result = {'request': request, 'status': status, 'response': response, 'seconds': time.perf_counter()-t}
    (out / f'smoke-{i}.json').write_text(json.dumps(result, indent=2))
    print(model, i, json.dumps(result), flush=True)
