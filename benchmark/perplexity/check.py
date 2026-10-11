"""Unscored native-interface and lossless-encoding checks, executed in Docker."""
import json
from pathlib import Path
import sys
import time
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'tools'))
from hosted import ROOT, load_cases, digest
from next_contract import request_for, normalize_response, verify_health
from next_wave import call

MODEL='pplx-decider-27b'
BASE='http://192.168.0.90:11449'
out=Path('/reports/perplexity-runtime')
for _ in range(120):
    try:
        status,health=call(BASE,'/healthz')
        if status==200 and health.get('status')=='ok':break
    except OSError:pass
    time.sleep(1)
else:raise RuntimeError('Service did not become ready')
verify_health(health,MODEL)
(out/'health.json').write_text(json.dumps(health,indent=2)+'\n')
smokes=[]
for kind,q in [('choice',{'type':'choice','instructions':'Route this request.','criteria':{'billing':'Payments and refunds','technical':'Software faults'}}),('noul',{'type':'noul','instructions':'Does the customer request a refund?','criteria':{'true':'The customer requests money back.','false':'The customer does not request money back.'}})]:
    case={'request':{'state':'Please refund the duplicate payment.','questions':{'decision':q}}}
    req=request_for(case,MODEL);status,body=call(BASE,'/v1/systemone',req)
    assert status==200,(status,body)
    result=normalize_response(body,case,MODEL)
    smokes.append({'request':req,'response':body,'result':result})
(out/'smoke.json').write_text(json.dumps(smokes,indent=2)+'\n')
records=[]
for version,directory in [('v1',ROOT/'datasets'),('v2',ROOT/'expansion-v2')]:
    cases,_=load_cases(directory)
    for c in cases:
        req=request_for(c,MODEL)
        status,body=call(BASE,'/v1/encoding',req)
        assert status==200,(version,c['id'],status,body)
        info=body['questions']['decision']
        assert info['ok'] and 0<info['input_tokens']<=8192,(c['id'],info)
        records.append({'version':version,'case_id':c['id'],'request_sha256':digest(req),**info})
negative={'request':{'state':'overflow '*13000,'questions':{'decision':{'type':'choice','instructions':'Select a label.','criteria':{'a':'A','b':'B'}}}}}
status,body=call(BASE,'/v1/systemone',request_for(negative,MODEL))
assert status==422 and 'no input was truncated' in str(body),(status,body)
(out/'encoding.json').write_text(json.dumps({'requests':len(records),'valid':len(records),'records':records,'overflow_negative_control':{'status':status,'response':body}},indent=2)+'\n')
print('Native choice/Noul valid;',len(records),'complete encodings; overflow rejected.',flush=True)
