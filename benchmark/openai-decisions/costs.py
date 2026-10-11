"""Reconcile Decisions usage and compare hosted classification costs, offline."""
from decimal import Decimal as D
import gzip
import hashlib
import json
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]/'tools'))
from hosted import ROOT, load_cases

prices=json.loads((ROOT/'pricing/2026-10-11.json').read_text())
result={'pricing':prices,'actual_invoice_verified':False,'runs':{},'compact_v2':{}}
rate=D(prices['input_usd_per_million']['openai-decisions'])
for version in ['v1','v2']:
    folder=ROOT/f'reports/openai-decisions-{version}'
    raw=gzip.decompress((folder/'responses.jsonl.gz').read_bytes())
    assert hashlib.sha256(raw).hexdigest()==json.loads((folder/'archive.json').read_text())['raw_sha256']
    records=[json.loads(line) for line in raw.splitlines()]
    usages=[r['response'].get('usage',{}) for r in records if isinstance(r.get('response'),dict)]
    tokens=[u['input_tokens'] for u in usages if isinstance(u.get('input_tokens'),int) and not isinstance(u['input_tokens'],bool)]
    attempts=sum(len(r['attempts']) for r in records)
    result['runs'][version]={'requests':len(records),'http_attempts':attempts,
        'known_input_tokens':sum(tokens),'records_without_usage':len(records)-len(tokens),
        'prior_attempts_without_usage':attempts-len(records),
        'known_list_price_usd':str(D(sum(tokens))*rate/1_000_000),
        'raw_sha256':hashlib.sha256(raw).hexdigest()}
smoke=json.loads((ROOT/'reports/openai-decisions-runtime/smoke-funded.json').read_text())
assert smoke['status']==200 and not smoke['error']
result['successful_smoke']={'requests':1,'questions':2,'input_tokens':smoke['response']['usage']['input_tokens'],
    'list_price_usd':str(D(smoke['response']['usage']['input_tokens'])*rate/1_000_000)}
result['initial_access_probe']={'status':429,'error_code':'credit_balance_exhausted','reported_usage':None,
    'note':'Rejected before funding; no metered usage was returned.'}
result['new_known_list_price_usd']=str(sum(D(r['known_list_price_usd']) for r in result['runs'].values())+D(result['successful_smoke']['list_price_usd']))
cases={c['id']:c for c in load_cases(ROOT/'expansion-v2')[0] if c['condition']=='compact'}
for name in ['hosted-v2','openai-decisions-v2']:
    raw=gzip.decompress((ROOT/'reports'/name/'responses.jsonl.gz').read_bytes())
    for model in ['jev','clef','clef-flash','openai-decisions']:
        records=[r for r in map(json.loads,raw.splitlines()) if r['model']==model and r['case_id'] in cases]
        if not records:continue
        assert len(records)==168
        usages=[r['response'].get('usage') if model=='openai-decisions' else r['result']['usage'] if r['result'] else None for r in records]
        assert all(u is not None and 'input_tokens' in u for u in usages), 'Unknown compact token cost'
        tokens=sum(u['input_tokens'] for u in usages)
        correct=sum(bool(r['result']) and r['result']['choice']==cases[r['case_id']]['gold'] for r in records)
        cost=D(tokens)*D(prices['input_usd_per_million'][model])/1_000_000
        result['compact_v2'][model]={'n':168,'correct':correct,'input_tokens':tokens,'list_price_usd':str(cost),
            'usd_per_1000':str(cost*1000/168),'usd_per_1000_correct':str(cost*1000/correct) if correct else None}
output=Path('/reports/openai-comparison-v2')
output.mkdir(parents=True,exist_ok=True)
(output/'costs.json').write_text(json.dumps(result,indent=2)+'\n')
lines=['# OpenAI Decisions cost reconciliation','','Usage-based list-price valuation, not a verified invoice. The $20 account deposit is prepaid credit, not the cost of this test. Existing hosted results are reused without new requests.','',
       '| New run | Requests | Attempts | Input tokens | Known listed USD |','| --- | ---: | ---: | ---: | ---: |']
for name,r in result['runs'].items():
    lines.append(f"| {name} | {r['requests']} | {r['http_attempts']} | {r['known_input_tokens']:,} | {r['known_list_price_usd']} |")
r=result['successful_smoke']
lines += [f"| Successful smoke (two questions) | 1 | 1 | {r['input_tokens']} | {r['list_price_usd']} |",'',
          f"**Total known new usage: ${result['new_known_list_price_usd']}.** The initial unfunded probe returned no metered usage. Any prior retry attempts without usage are counted in costs.json; their charges cannot be reconstructed from a final response.",'',
          '## Same compact bilingual cases','', '| Provider | Correct / 168 | Input tokens | USD per 1,000 classifications |','| --- | ---: | ---: | ---: |']
for name,r in result['compact_v2'].items():
    lines.append(f"| {name} | {r['correct']}/168 | {r['input_tokens']:,} | {D(r['usd_per_1000']):.6f} |")
lines += ['', 'Rates: OpenAI Decisions $0.10/M input (verified 11 October UTC); Jev $0.042/M, Clef $0.24/M, Flash $0.038/M (10 October snapshot). All use zero output-token charges for these endpoints. Tokenizers and native request formats differ. Cloudflare free allowances, discounts, tax and local operating costs are excluded.', '',
          'Sources: [OpenAI Decisions](https://developers.openai.com/api/docs/guides/decisions), [Jev](https://docs.typesafe.ai/models), [Clef](https://developers.cloudflare.com/workers-ai/models/clef/), [Flash](https://developers.cloudflare.com/workers-ai/models/clef-flash/).', '']
(output/'costs.md').write_text('\n'.join(lines))
print(json.dumps(result,indent=2))
