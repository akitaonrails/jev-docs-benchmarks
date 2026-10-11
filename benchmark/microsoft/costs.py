"""Derive comparable workload costs from stored usage; no network."""
from decimal import Decimal as D
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
folder=ROOT/'reports/microsoft-comparison-v2'
summary=json.loads((folder/'summary.json').read_text())
verification=json.loads((folder/'verification.json').read_text())
rows=[]
lines=['# Microsoft and hosted workload costs','','Rates checked 11 October 2026. Compact v2 uses the same 168 paired-language cases per model. Values exclude allowances, taxes and credit purchase fees. Local operating cost is unmeasured.','','| Hosted model | Correct / 168 | Input tokens | USD / 1,000 calls | USD / 1,000 observed correct |','| --- | ---: | ---: | ---: | ---: |']
for model,rate in summary['pricing']['input_usd_per_million'].items():
    groups=[summary['models'][model]['groups'][f'all/{l}/compact'] for l in ('en','pt-BR')]
    tokens=sum(g['input_tokens'] for g in groups);correct=sum(g['correct'] for g in groups)
    cost=D(tokens)*D(rate)/1_000_000
    rows.append({'model':model,'correct':correct,'input_tokens':tokens,'compact_cost_usd':str(cost),'per_1000_calls_usd':str(cost*1000/168),'per_1000_correct_usd':str(cost*1000/correct)})
for r in sorted(rows,key=lambda r:-r['correct']):
    lines.append(f"| {r['model']} | {r['correct']} | {r['input_tokens']} | ${D(r['per_1000_calls_usd']):.5f} | ${D(r['per_1000_correct_usd']):.5f} |")
lines+=['','Cost per observed correct label does not include review or error damage, and does not mean correct answers can be identified in advance.','','## This Microsoft execution','','| Suite | Requests | Input tokens | OpenRouter reported USD |','| --- | ---: | ---: | ---: |']
for v in ('v1','v2'):
    r=verification[v];lines.append(f"| {v} | {r['records']} | {r['input_tokens']} | ${r['reported_cost_usd']} |")
lines+=['',f"Scored total: **${verification['total_scored_cost_usd']}**. Including the separately observed smoke: **${verification['total_with_observed_smoke_usd']}**.",'','Every scored usage.cost equals input_tokens × $0.042/M. This is reported successful-response usage, not a reconciliation of the full account invoice. Ten v2 HTTP 429 attempts preceded successful retries; the runner preserves their status and timing but no separate billing usage, so any failed-attempt charges are unverified. Earlier hosted figures are list-price valuations of their archived usage. Cloudflare free allowances can lower actual bills.','', '[Rate snapshot](../../pricing/2026-10-11-microsoft.json), [verification](verification.json), [OpenRouter price](https://openrouter.ai/microsoft/microsoft-decision-1).']
((Path('/reports/microsoft-comparison-v2') if Path('/reports').is_dir() else folder)/'costs.json').write_text(json.dumps(rows,indent=2)+'\n')
((Path('/reports/microsoft-comparison-v2') if Path('/reports').is_dir() else folder)/'costs.md').write_text('\n'.join(lines)+'\n')
print('\n'.join(lines))
