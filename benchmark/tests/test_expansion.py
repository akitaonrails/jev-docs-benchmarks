import hashlib
import importlib.util
import json
from pathlib import Path
import sys
import unittest
from collections import Counter, defaultdict

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'tools'))
sys.path.insert(0,str(ROOT/'expansion-v2'))
from build import generate
from scenarios_v2 import TRACKS
from hosted import payload, load_cases
from score_v2 import paired

class ExpansionTests(unittest.TestCase):
    def test_frozen_bilingual_pairs_and_balance(self):
        rows,manifest=load_cases(ROOT/'expansion-v2')
        self.assertEqual(rows,generate())
        self.assertEqual(len(rows),504)
        groups=defaultdict(list)
        for case in rows:groups[(case['family'],case['condition'])].append(case)
        self.assertEqual(len(groups),252)
        for a,b in groups.values():
            self.assertEqual({a['language'],b['language']},{'en','pt-BR'})
            self.assertEqual(a['gold'],b['gold'])
            self.assertEqual(a['semantic_map'],b['semantic_map'])
            self.assertEqual(list(a['request']['questions']['decision']['criteria']),list(b['request']['questions']['decision']['criteria']))
        for name,t in TRACKS.items():
            counts=Counter(c[2] for c in t['cases'])
            self.assertEqual(len(set(counts.values())),1,name)
            for col in (0,1):
                self.assertFalse({c[col] for c in t['cases']} & {c[col] for c in t['examples']})

    def test_wire_allowlist_and_pair_arithmetic(self):
        case=generate()[0];case['gold']='HIDDEN_GOLD'
        self.assertNotIn('HIDDEN_GOLD',json.dumps(payload(case,'jev')))
        result=paired([1,1,0,0],[1,0,1,0])
        self.assertEqual(result['accuracy_b_minus_a'],0)
        self.assertEqual([result[k] for k in ['both_correct','a_only_correct','b_only_correct','both_wrong']],[1]*4)
