"""Frozen next-wave wire mappings; no access to gold labels or semantic maps."""
import json
import math
from pathlib import Path

REGISTRY = json.loads((Path(__file__).resolve().parents[1] / 'next-wave/models.json').read_text())


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
