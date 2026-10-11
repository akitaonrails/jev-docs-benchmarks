import copy
import sys
import unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'tools'))
from next_contract import REGISTRY, request_for, normalize_response, verify_health

class PerplexityTests(unittest.TestCase):
    def test_native_choice_and_noul_preserve_probabilities(self):
        case={'request':{'state':'Example','questions':{'decision':{'type':'choice','instructions':'Policy','criteria':{'b':'B','a':'A'}}}},'gold':'never sent'}
        req=request_for(case,'pplx-decider-27b')
        self.assertEqual(req,dict(case['request'],model='pplx-decider-v1.1-27b'))
        body={'model':'autojev-qwen3.8-27b','answers':{'decision':{'type':'choice','choice':'b','confidence':.8,'probabilities':{'b':.8,'a':.2}}},'usage':{'input_tokens':100,'output_tokens':0}}
        original=copy.deepcopy(body)
        self.assertEqual(normalize_response(body,case,'pplx-decider-27b')['probabilities'],{'b':.8,'a':.2})
        self.assertEqual(body,original)
        case['request']['questions']['decision']={'type':'noul','instructions':'True?','criteria':{'true':'Yes','false':'No'}}
        body['answers']['decision']={'type':'noul','noul':.3}
        self.assertAlmostEqual(normalize_response(body,case,'pplx-decider-27b')['probability'],.3)

    def test_health_requires_exact_frozen_runtime(self):
        health=REGISTRY['pplx-decider-27b']['expected_health']
        verify_health(health,'pplx-decider-27b')
        for key in health:
            bad=dict(health);bad.pop(key)
            with self.assertRaises(RuntimeError):verify_health(bad,'pplx-decider-27b')
            bad=dict(health);bad[key]='wrong'
            with self.assertRaises(RuntimeError):verify_health(bad,'pplx-decider-27b')
