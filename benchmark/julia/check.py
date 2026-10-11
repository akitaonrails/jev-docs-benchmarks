"""Independent readiness, native API and strict-encoding checks; no scored inference."""
import argparse
import json
from pathlib import Path
import sys
import time
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'tools'))
from hosted import ROOT, load_cases
from next_contract import REGISTRY, request_for, normalize_response
from next_wave import call

p=argparse.ArgumentParser();p.add_argument('--model',required=True,choices=['julia-1','julia-1-cpu']);p.add_argument('--output',required=True);a=p.parse_args()
base=f'http://192.168.0.90:{REGISTRY[a.model]["port"]}'
out=Path(a.output);out.mkdir(parents=True,exist_ok=True)
for attempt in range(60):
    try:
        status,health=call(base,'/healthz')
        if status==200 and health.get('ready'):break
    except OSError:pass
    time.sleep(1)
else:raise RuntimeError('Julia did not become ready')
for k,v in REGISTRY[a.model]['expected_server'].items():
    assert health.get(k)==v,(k,health.get(k),v)
(out/'health.json').write_text(json.dumps(health,indent=2)+'\n')
smokes=[]
for kind,q in [('choice',{'type':'choice','instructions':'Route this request.','criteria':{'billing':'Payments and refunds','technical':'Software faults'}}),('noul',{'type':'noul','instructions':'Does the customer request a refund?','criteria':{'true':'The customer requests money back.','false':'The customer does not request money back.'}})]:
    case={'request':{'state':'Please refund the duplicate payment.','questions':{'decision':q}}}
    req=request_for(case,a.model);status,body=call(base,'/v1/systemone',req)
    assert status==200,(status,body)
    normalized=normalize_response(body,case,a.model)
    smokes.append({'kind':kind,'request':req,'response':body,'result':normalized})
(out/'smoke.json').write_text(json.dumps(smokes,indent=2)+'\n')
encodings=[]
for version,directory in [('v1',ROOT/'datasets'),('v2',ROOT/'expansion-v2')]:
    cases,_=load_cases(directory)
    for c in cases:
        status,body=call(base,'/v1/encoding',request_for(c,a.model))
        assert status==200,(version,c['id'],status,body)
        info=body['questions']['decision']
        assert info['ok'],(version,c['id'],info)
        encodings.append({'version':version,'case_id':c['id'],**info})
negative={'request':{'state':'Test','questions':{'decision':{'type':'choice','instructions':'Select a label.','criteria':{'a':'word '*80,'b':'Short'}}}}}
status,body=call(base,'/v1/encoding',request_for(negative,a.model))
assert status==400 or (status==200 and body['questions']['decision']['ok'] is False),(status,body)
(out/'encoding.json').write_text(json.dumps({'requests':len(encodings),'valid':len(encodings),'records':encodings,'overflow_negative_control':{'status':status,'response':body}},indent=2)+'\n')
print(a.model, 'native choice/noul valid;',len(encodings),'strict encodings valid; overflow rejected',flush=True)
