import copy
import sys
import unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'tools'))
from next_contract import REGISTRY, normalize_response, request_for
from hosted import load_cases

class JuliaTests(unittest.TestCase):
    def test_same_wire_request_separate_verified_precision_tracks(self):
        case=load_cases()[0][0]
        self.assertEqual(request_for(case,'julia-1'),request_for(case,'julia-1-cpu'))
        labels=list(case['request']['questions']['decision']['criteria'])
        native={'answers':{'decision':{'choice':labels[0],'probabilities':dict(zip(labels,[.7,.1,.1,.1]))}},
                'usage':{'input_tokens':100,'state_truncated':False,'options_truncated':False},
                'server':{'repo':'SupersonicLabs/Julia-1',**REGISTRY['julia-1']['expected_server']}}
        saved=copy.deepcopy(native)
        result=normalize_response(native,case,'julia-1')
        self.assertEqual(native,saved)
        self.assertIs(result['usage']['truncated'],False)
        self.assertIn('a85b127',result['served_model'])
        with self.assertRaises(RuntimeError):normalize_response(native,case,'julia-1-cpu')
        for key in ['revision','device','precision','strict_encoding','head_length']:
            invalid=copy.deepcopy(native);invalid['server'][key]='wrong'
            with self.assertRaises(RuntimeError):normalize_response(invalid,case,'julia-1')
        for key in ['state_truncated','options_truncated']:
            invalid=copy.deepcopy(native);invalid['usage'][key]=True
            with self.assertRaises(RuntimeError):normalize_response(invalid,case,'julia-1')

if __name__=='__main__':unittest.main()
