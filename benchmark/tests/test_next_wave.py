import copy
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]/'tools'))
from hosted import load_cases, normalized, payload, ROOT
from next_contract import REGISTRY, request_for, normalize_gliner
from score import class_metrics


class NextWaveTests(unittest.TestCase):
    def setUp(self):
        self.case = load_cases(ROOT/'expansion-v2')[0][0]

    def test_gold_and_rationale_cannot_change_request(self):
        changed = copy.deepcopy(self.case)
        changed.update(gold='SECRET', semantic_gold='SECRET', semantic_map={'SECRET':'SECRET'}, rationale='SECRET')
        for model in REGISTRY:
            self.assertEqual(request_for(self.case, model), request_for(changed, model))
            self.assertEqual(payload(self.case, model), request_for(self.case, model))

    def test_gliner_preserves_rubric_descriptions_and_state(self):
        r = request_for(self.case, 'gliner2.5-decide')
        q = self.case['request']['questions']['decision']
        self.assertEqual(r['text'], self.case['request']['state'])
        self.assertEqual(r['tasks']['decision']['labels'], q['criteria'])
        self.assertEqual(r['tasks']['decision']['prompt'], q['instructions'])

    def test_native_confidence_is_not_distribution(self):
        body = {'result': {'decision': {'label':self.case['gold'], 'confidence':.7}}}
        result = normalize_gliner(body, self.case)
        m = class_metrics([self.case], {self.case['id']:{'result':result}})
        self.assertEqual(m['accuracy'], 1)
        self.assertEqual(m['valid'], 1)
        self.assertEqual(m['probability_distributions'], 0)
        self.assertIsNone(m['brier_valid_only'])
        self.assertIsNone(m['ece_valid_only'])
        for confidence in [float('nan'), float('inf'), True, -.1, 1.1]:
            body['result']['decision']['confidence'] = confidence
            with self.assertRaises(ValueError):
                normalize_gliner(body, self.case)

    def test_systemone_bad_distribution_rejected(self):
        labels = self.case['request']['questions']['decision']['criteria']
        body = {'answers':{'decision':{'choice':self.case['gold'], 'probabilities':dict.fromkeys(labels,.8)}}}
        with self.assertRaises(ValueError):
            normalized(body, self.case)


if __name__ == '__main__':
    unittest.main()
