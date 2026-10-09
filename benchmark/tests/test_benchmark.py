import copy
import json
from pathlib import Path
import sys
import unittest

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'tools'))
from build_dataset import generate
from hosted import normalized,payload

class BenchmarkTests(unittest.TestCase):
    def test_dataset_invariants(self):
        rows=generate()
        self.assertEqual(len(rows),544)
        self.assertEqual(len({r['id'] for r in rows}),544)
        families={}
        for r in rows:
            if r['kind']=='classification':
                self.assertIn(r['gold'],r['request']['questions']['decision']['criteria'])
                self.assertEqual(r['semantic_map'][r['gold']],r['semantic_gold'])
                families.setdefault(r['family'],[]).append(r)
        self.assertEqual(len(families),130)
        for group in families.values():
            self.assertEqual(len(group),4)
            self.assertEqual(len({r['semantic_gold'] for r in group}),1)
            original,reversed_,opaque,injected=group
            self.assertEqual(list(original['semantic_map']),list(reversed(reversed_['semantic_map'])))
            self.assertEqual(original['request']['state'],opaque['request']['state'])
            self.assertEqual(original['request']['state']['record'],injected['request']['state']['record'])

    def test_gold_never_serialized(self):
        r=generate()[0]
        r['gold']='LEAK_GOLD';r['rationale']='LEAK_RATIONALE'
        body=payload(r,'jev')
        self.assertEqual(set(body),{'state','questions','model'})
        self.assertNotIn('LEAK_',json.dumps(body))

    def test_response_validation_and_rounding(self):
        case=generate()[0];labels=list(case['request']['questions']['decision']['criteria'])
        body={'answers':{'decision':{'choice':labels[0],'probabilities':{k:0.25 for k in labels}}},'usage':{'input_tokens':10}}
        self.assertEqual(normalized(body,case)['choice'],labels[0])
        wrapped={'success':True,'result':body}
        self.assertEqual(normalized(wrapped,case)['usage']['input_tokens'],10)
        bad=copy.deepcopy(body);bad['answers']['decision']['probabilities'][labels[0]]=float('nan')
        with self.assertRaises(ValueError):normalized(bad,case)
        bad=copy.deepcopy(body);bad['answers']['decision']['choice']='not-a-label'
        with self.assertRaises(ValueError):normalized(bad,case)
        bad=copy.deepcopy(body);bad['answers']['decision']['probabilities'][labels[0]]=0.01
        with self.assertRaises(ValueError):normalized(bad,case)
        bad=copy.deepcopy(body);bad['answers']['decision']['probabilities']={labels[0]:0.1,labels[1]:0.4,labels[2]:0.25,labels[3]:0.25}
        with self.assertRaises(ValueError):normalized(bad,case)

if __name__=='__main__':unittest.main()
