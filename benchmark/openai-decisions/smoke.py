"""One independent native request; no benchmark cases and no retries."""
import argparse
from datetime import datetime, timezone
import http.client
import json
from pathlib import Path
import ssl
import sys
import time
sys.path.insert(0, str(Path(__file__).resolve().parents[1]/'tools'))
from hosted import endpoint, redact
from openai_decisions import normalized

p=argparse.ArgumentParser();p.add_argument('--output',required=True);args=p.parse_args()
out=Path(args.output)
if out.exists():raise SystemExit('Use a fresh smoke output path')
request={'model':'gpt-6-luna','input':'The package contains exactly two red balls and no other objects.','questions':[
    {'name':'color','type':'choice','instructions':'What color are the balls?','choices':[{'value':'r','description':'Red'},{'value':'b','description':'Blue'}]},
    {'name':'red','type':'predicate','instructions':'At least one ball is red.'}]}
host,path,key=endpoint('openai-decisions')
conn=http.client.HTTPSConnection(host,timeout=45,context=ssl.create_default_context())
t=time.perf_counter();status=None;body=None;error=None
try:
    conn.request('POST',path,json.dumps(request).encode(),{'Authorization':'Bearer '+key,'Content-Type':'application/json'})
    response=conn.getresponse();status=response.status;data=response.read()
    try:body=json.loads(data)
    except (ValueError,UnicodeDecodeError):body={'non_json_body':data[:1000].decode(errors='replace')}
    if status!=200: error=f'HTTP {status}'
    else:
        answers=body['answers']
        if len(answers)!=2:raise ValueError('Expected two answers')
        for index,kind in enumerate(['choice','noul']):
            answer=dict(answers[index])
            if answer['name']!=['color','red'][index]:raise ValueError('Wrong question name/order')
            answer['name']='decision'
            normalized({**body,'answers':[answer]}, {'request':{'questions':{'decision':{'type':kind,'criteria':{'r':'Red','b':'Blue'}}}}})
except (OSError,http.client.HTTPException,ValueError,KeyError,TypeError) as exc:
    error=type(exc).__name__+': '+str(exc)
finally:conn.close()
record=redact({'timestamp':datetime.now(timezone.utc).isoformat(),'request':request,'status':status,
    'latency_seconds':time.perf_counter()-t,'response':body,'error':error})
out.parent.mkdir(parents=True,exist_ok=True);out.write_text(json.dumps(record,indent=2)+'\n')
print('Smoke:',error or 'valid choice and predicate responses', 'Saved:',out)
if error:raise SystemExit(1)
