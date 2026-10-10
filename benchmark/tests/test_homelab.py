import copy
import json
from pathlib import Path
import sys
import unittest
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'tools'))
from hosted import payload, normalized, load_cases, digest
from score import score
from homelab import validate_server

class HomelabTests(unittest.TestCase):
    def test_local_payload_and_native_probability(self):
        cases, _ = load_cases()
        case = copy.deepcopy(cases[0])
        case['gold'] = 'DO_NOT_SEND'
        request = payload(case, 'clef-flash-local')
        self.assertEqual(request['model'], 'clef-flash')
        self.assertEqual(set(request), {'model', 'state', 'questions'})
        self.assertNotIn('DO_NOT_SEND', json.dumps(request))
        labels = list(request['questions']['decision']['criteria'])
        probs = {k: 1 / len(labels) for k in labels}
        body = {'answers': {'decision': {'choice': labels[0], 'probabilities': probs,
                                         'confidence': 0.99}},
                'usage': {'truncated': True, 'state_tokens_dropped': 12}, 'server': {'cold': False}}
        answer = normalized(body, case)
        self.assertEqual(answer['probabilities'], probs)
        self.assertTrue(answer['usage']['truncated'])

    def test_provenance_mismatch_fails(self):
        pins = {'clef-flash': {'repo': 'Cloudflare/clef-flash', 'revision': 'pinned'}}
        body = {'server': dict(pins['clef-flash'], selector='clef-flash', device='cuda:0')}
        validate_server(body, 'clef-flash-local', pins)
        body['server']['revision'] = 'different'
        with self.assertRaises(ValueError):
            validate_server(body, 'clef-flash-local', pins)

    def test_local_scoring_has_no_hosted_price_and_records_truncation(self):
        cases, manifest = load_cases()
        case = cases[0]
        labels = list(case['request']['questions']['decision']['criteria'])
        record = {'model': 'clef-flash-local', 'case_id': case['id'],
                  'dataset_sha256': manifest['sha256'],
                  'request_sha256': digest(payload(case, 'clef-flash-local')),
                  'result': {'choice': labels[0], 'probabilities': {k: 1/len(labels) for k in labels},
                             'usage': {'input_tokens': 100, 'truncated': True, 'state_tokens_dropped': 7},
                             'served_model': 'clef-flash'},
                  'response': {'server': {'cold': False, 'predict_s': 0.2, 'revision': 'pin'}},
                  'latency_seconds': 0.3, 'attempts': [{'status': 200}], 'error': None}
        report = score(cases, manifest, [record], ['clef-flash-local'])['models']['clef-flash-local']
        self.assertIsNone(report['operations']['estimated_reported_usage_cost_usd'])
        self.assertEqual(report['operations']['missing'], 543)
        self.assertEqual(report['operations']['local']['truncation_reported_count'], 1)
        self.assertEqual(report['operations']['local']['state_tokens_dropped'], 7)
        self.assertEqual(report['operations']['local']['server_prediction_median_seconds'], 0.2)
