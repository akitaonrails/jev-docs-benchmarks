"""Standard-library hosted runner. Request allowlist prevents gold-label leakage."""
import argparse
from datetime import datetime, timezone
import hashlib
import http.client
import json
import math
import os
from pathlib import Path
import random
import ssl
import time

ROOT=Path(__file__).resolve().parents[1]
MODELS={'jev':('jev-1.13.0',0.042),'clef':('clef',0.24),'clef-flash':('clef-flash',0.09)}

# Local entrants remain distinct from hosted Clef-flash; no API price is assigned.
LOCAL_MODELS={'laya':('laya',None),'laya-typed':('laya-typed',None),'clef-flash-local':('clef-flash',None)}

def digest(obj):
    return hashlib.sha256(json.dumps(obj,sort_keys=True,ensure_ascii=False).encode()).hexdigest()

def load_cases(dataset=None):
    directory=Path(dataset) if dataset else ROOT/'datasets'
    path=directory/'cases.jsonl'
    manifest=json.loads((directory/'manifest.json').read_text())
    if hashlib.sha256(path.read_bytes()).hexdigest()!=manifest['sha256']:
        raise ValueError('Dataset differs from frozen manifest')
    rows=[json.loads(x) for x in path.read_text().splitlines()]
    if len({r['id'] for r in rows})!=len(rows): raise ValueError('Duplicate case IDs')
    return rows,manifest

def payload(case,model):
    # Never serialize the entire fixture. Gold, rationale and identifiers stay local.
    req=case['request']
    return {'state':req['state'],'questions':req['questions'],'model':{**MODELS,**LOCAL_MODELS}[model][0]}

def normalized(body, case):
    if not isinstance(body,dict): raise ValueError('Response is not an object')
    if 'success' in body:
        if not body['success']: raise ValueError('Provider reports failure')
        body=body['result']
    answer=body['answers']['decision']
    question=case['request']['questions']['decision']
    if question['type']=='noul':
        p=answer['noul']
        if isinstance(p,bool) or not isinstance(p,(int,float)) or not math.isfinite(p) or not 0<=p<=1:
            raise ValueError('Invalid Noul probability')
        return {'probability':p,'usage':body.get('usage',{}),'served_model':body.get('model')}
    probs=answer['probabilities']
    labels=list(question['criteria'])
    if set(probs)!=set(labels): raise ValueError('Probability labels mismatch')
    if any(isinstance(v,bool) or not isinstance(v,(int,float)) or not math.isfinite(v) or not 0<=v<=1 for v in probs.values()):
        raise ValueError('Invalid probability')
    total=sum(probs.values())
    # Published Jev values are rounded to 2 decimals; permit bounded rounding error.
    if abs(total-1)>0.0051*len(labels): raise ValueError('Probability sum outside rounding tolerance')
    choice=answer['choice']
    if choice not in probs: raise ValueError('Choice is not an allowed label')
    if probs[choice]+1e-8 < max(probs.values()): raise ValueError('Choice not a maximum-probability option')
    return {'choice':choice,'probabilities':{k:v/total for k,v in probs.items()},
        'raw_probability_sum':total,'usage':body.get('usage',{}),'served_model':body.get('model')}

def endpoint(model):
    if model=='jev': return 'api.typesafe.ai','/v1/systemone',os.environ['JEV_API_KEY']
    account=os.environ['CLOUDFLARE_ACCOUNT_ID']
    if len(account)!=32 or any(c not in '0123456789abcdef' for c in account.lower()): raise ValueError('Invalid account ID')
    return 'api.cloudflare.com',f'/client/v4/accounts/{account}/ai/run/@cf/cloudflare/{model}',os.environ['CLOUDFLARE_API_TOKEN']

def redact(value):
    text=json.dumps(value,ensure_ascii=False)
    for name in ('JEV_API_KEY','CLOUDFLARE_API_TOKEN','CLOUDFLARE_ACCOUNT_ID'):
        secret=os.environ.get(name)
        if secret: text=text.replace(secret,'[REDACTED]')
    return json.loads(text)

def run(args):
    rows,manifest=load_cases(getattr(args,'dataset',None))
    if args.limit: rows=rows[:args.limit]
    out=Path(args.output);out.mkdir(parents=True,exist_ok=True)
    result_path=out/'responses.jsonl'
    config={'dataset_sha256':manifest['sha256'],'models':args.models,'limit':args.limit,
        'seed':20261009,'max_attempts':3,'timeout_seconds':45,
        'dataset_directory':str(Path(args.dataset).resolve()) if getattr(args,'dataset',None) else str(ROOT/'datasets'),
        'estimated_cost_cap_usd':args.cost_cap,'runner_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
    config_path=out/'run.json'
    if config_path.exists():
        old=json.loads(config_path.read_text())
        if old['config']!=config: raise ValueError('Resume configuration mismatch; use a new output directory')
    else: config_path.write_text(json.dumps({'started_at':datetime.now(timezone.utc).isoformat(),'config':config},indent=2)+'\n')
    prior=[json.loads(x) for x in result_path.read_text().splitlines()] if result_path.exists() else []
    done={(r['model'],r['case_id']) for r in prior}
    reserved=sum(r['reserved_cost_usd'] for r in prior)
    tasks=[(m,c) for c in rows for m in args.models]
    random.Random(20261009).shuffle(tasks)
    connections={}
    stopped=set()
    for index,(model,case) in enumerate(tasks):
        if (model,case['id']) in done or model in stopped: continue
        req=payload(case,model);encoded=json.dumps(req,ensure_ascii=False).encode()
        # Bytes plus overhead is a conservative planning allowance, not a billing guarantee.
        reserve=(len(encoded)+4096)*MODELS[model][1]/1e6*3
        if reserved+reserve>args.cost_cap: raise SystemExit('Estimated input-cost cap reached before next call')
        reserved+=reserve
        host,path,key=endpoint(model)
        start=time.perf_counter();attempts=[];parsed=None;raw=None;error=None
        for attempt in range(3):
            try:
                conn=connections.get(model)
                if conn is None:
                    conn=http.client.HTTPSConnection(host,timeout=45,context=ssl.create_default_context());connections[model]=conn
                t=time.perf_counter()
                conn.request('POST',path,body=encoded,headers={'Authorization':'Bearer '+key,'Content-Type':'application/json','User-Agent':'jev-benchmark/1.0'})
                response=conn.getresponse();data=response.read();status=response.status
                try: raw=json.loads(data)
                except (ValueError,UnicodeDecodeError): raw={'non_json_body':data[:2000].decode(errors='replace')}
                attempts.append({'status':status,'seconds':time.perf_counter()-t})
                if status in (401,403,404,402):
                    error=f'HTTP {status}; provider stopped';stopped.add(model);break
                if status==429 or status>=500:
                    error=f'HTTP {status}'
                    if attempt<2:
                        retry=response.getheader('Retry-After','')
                        delay=min(30,float(retry)) if retry.replace('.','',1).isdigit() else 2**(attempt+1)
                        time.sleep(max(0,delay));continue
                    break
                if not 200<=status<300: error=f'HTTP {status}';break
                try: parsed=normalized(raw,case);error=None
                except (ValueError,KeyError,TypeError,ZeroDivisionError) as e: error='Invalid response: '+str(e)
                break
            except (OSError,http.client.HTTPException) as e:
                error=type(e).__name__
                attempts.append({'error':error,'seconds':time.perf_counter()-t})
                if model in connections: connections.pop(model).close()
                if attempt<2: time.sleep(2**(attempt+1))
        row={'case_id':case['id'],'model':model,'request_sha256':digest(req),
            'dataset_sha256':manifest['sha256'],'timestamp':datetime.now(timezone.utc).isoformat(),
            'latency_seconds':time.perf_counter()-start,'attempts':attempts,
            'reserved_cost_usd':reserve,'result':parsed,'error':error,'response':raw}
        with result_path.open('a') as f: f.write(json.dumps(redact(row),ensure_ascii=False)+'\n');f.flush()
        if error or (index+1)%30==0:
            print(f'{index+1}/{len(tasks)} {model}: '+(error or 'ok'),flush=True)
    for conn in connections.values(): conn.close()
    print('Finished. Responses:',result_path,'Stopped providers:',','.join(stopped) or 'none')

def main():
    p=argparse.ArgumentParser()
    p.add_argument('--models',nargs='+',choices=MODELS,default=list(MODELS))
    p.add_argument('--output',required=True)
    p.add_argument('--dataset',help='Frozen dataset directory; defaults to v1')
    p.add_argument('--limit',type=int,default=0)
    p.add_argument('--cost-cap',type=float,default=5)
    p.add_argument('--execute',action='store_true')
    args=p.parse_args()
    if not args.execute: p.error('Inference requires --execute')
    run(args)

if __name__=='__main__':main()
