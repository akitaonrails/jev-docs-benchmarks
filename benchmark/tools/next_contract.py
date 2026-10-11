"""Frozen next-wave wire mappings; no access to gold labels or semantic maps."""
import json
import math
from pathlib import Path

REGISTRY = json.loads((Path(__file__).resolve().parents[1] / 'next-wave/models.json').read_text())


def verify_health(health, model):
    for key, value in REGISTRY[model].get('expected_health', {}).items():
        if key not in health or type(health[key]) is not type(value) or health[key] != value:
            raise RuntimeError(f'Server health provenance mismatch: {key}')


def request_for(case, model):
    config = REGISTRY[model]
    req = case['request']
    if config['interface'] == 'systemone':
        return {'state': req['state'], 'questions': req['questions'], 'model': config['selector']}
    q = req['questions']['decision']
    if q['type'] != 'choice':
        raise ValueError('GLiNER does not expose native Noul probabilities')
    if not isinstance(req['state'], str):
        raise ValueError('GLiNER track requires a text state')
    return {'text': req['state'], 'tasks': {'decision': {
        'labels': q['criteria'], 'prompt': q['instructions'], 'multi_label': False}},
        'include_confidence': True}


def normalize_gliner(body, case):
    answer = body['result']['decision']
    if not isinstance(answer, dict):
        raise ValueError('Unexpected GLiNER classification shape')
    label = answer['label']
    confidence = answer['confidence']
    if label not in case['request']['questions']['decision']['criteria']:
        raise ValueError('GLiNER label outside allowed options')
    if isinstance(confidence, bool) or not isinstance(confidence, (int, float)) or not math.isfinite(confidence) or not 0 <= confidence <= 1:
        raise ValueError('Invalid GLiNER confidence')
    return {'choice': label, 'native_confidence': confidence, 'probabilities': None,
            'usage': {}, 'served_model': body.get('server', {}).get('repo')}


def normalize_response(body, case, model):
    from hosted import normalized
    config = REGISTRY[model]
    if config['interface'] == 'gliner':
        return normalize_gliner(body, case)
    expected = config.get('expected_server')
    if expected:
        server = body.get('server', {})
        for key, value in expected.items():
            actual = server.get(key)
            if key not in server or type(actual) is not type(value) or actual != value:
                raise RuntimeError(f'Server provenance mismatch: {key}')
        usage = dict(body['usage'])
        if usage.get('state_truncated') is not False or usage.get('options_truncated') is not False:
            raise RuntimeError('Strict Julia encoding not confirmed lossless')
        # Normalize explicit native telemetry for the common scoring schema.
        usage['truncated'] = False
        body = {**body, 'usage': usage,
                'model': body.get('model') or f"{server['repo']}@{server['revision']}"}
    return normalized(body, case)
