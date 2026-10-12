import copy,sys,unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'tools'))
from next_contract import REGISTRY,request_for,verify_health,normalize_response
from hosted import load_cases
class Decision3Tests(unittest.TestCase):
 def test_native_inputs_and_runtime_guards(self):
  cases,_=load_cases()
  for model in ('d3','d3-edge'):
   for case in cases:self.assertEqual(request_for(case,model),dict(case['request'],model=model))
   health=REGISTRY[model]['expected_health'];verify_health(health,model)
   for key in health:
    bad=copy.deepcopy(health);bad.pop(key)
    with self.assertRaises(RuntimeError):verify_health(bad,model)
 def test_noul_is_not_choice_confidence(self):
  case={'request':{'state':'x','questions':{'decision':{'type':'noul','instructions':'True?'}}}}
  raw={'model':'d3','answers':{'decision':{'type':'noul','noul':.2,'confidence':.8}},'usage':{'input_tokens':10}}
  for model in ('d3','d3-edge'):self.assertEqual(normalize_response(raw,case,model)['probability'],.2)
