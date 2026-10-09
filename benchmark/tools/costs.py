"""Reconcile archived successful usage at prices verified on 2026-10-09; no network."""
import gzip
import hashlib
import json
from decimal import Decimal as D
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RATES = {'jev': D('0.042'), 'clef': D('0.24'), 'clef-flash': D('0.09')}
NEURONS = {'clef': D('21818'), 'clef-flash': D('8182')}


def reconcile():
    result = {'verified_on': '2026-10-09', 'currency': 'USD',
              'actual_invoice_verified': False,
              'input_usd_per_million': RATES, 'neurons_per_million_input': NEURONS,
              'sources': ['https://docs.typesafe.ai/models',
                          'https://developers.cloudflare.com/workers-ai/models/clef/',
                          'https://developers.cloudflare.com/workers-ai/models/clef-flash/',
                          'https://developers.cloudflare.com/workers-ai/platform/pricing/'],
              'runs': {}}
    for run in ('hosted-v1', 'smoke-v1'):
        archive = ROOT / 'reports' / run / 'responses.jsonl.gz'
        data = archive.read_bytes()
        rows = [json.loads(line) for line in gzip.decompress(data).splitlines()]
        models = {}
        for model, rate in RATES.items():
            selected = [r for r in rows if r['model'] == model]
            # Fail closed: missing usage must never silently become zero cost.
            assert selected and all(r['result'] and not r['error'] for r in selected)
            inputs = sum(r['result']['usage']['input_tokens'] for r in selected)
            outputs = sum(r['result']['usage']['output_tokens'] for r in selected)
            assert model == 'jev' or outputs == 0
            models[model] = {'requests': len(selected), 'input_tokens': inputs,
                             'output_tokens': outputs,
                             'http_attempts': sum(len(r['attempts']) for r in selected),
                             'list_price_usd': D(inputs) * rate / 1_000_000}
        result['runs'][run] = {'archive_sha256': hashlib.sha256(data).hexdigest(),
                               'utc_dates': sorted({r['timestamp'][:10] for r in rows}),
                               'models': models}
    combined = {}
    for model, rate in RATES.items():
        totals = {key: sum(run['models'][model][key] for run in result['runs'].values())
                  for key in ('requests', 'input_tokens', 'output_tokens', 'http_attempts', 'list_price_usd')}
        if model in NEURONS:
            totals['estimated_neurons'] = D(totals['input_tokens']) * NEURONS[model] / 1_000_000
        combined[model] = totals
    result['combined'] = combined
    result['total_list_price_usd'] = sum(r['list_price_usd'] for r in combined.values())
    result['cloudflare'] = {'estimated_neurons': sum(combined[m]['estimated_neurons'] for m in NEURONS),
                            'daily_free_neurons': 10000, 'usd_per_1000_neurons': D('0.011'),
                            'other_account_usage': 'unknown'}
    return result


if __name__ == '__main__':
    output = ROOT / 'reports' / 'hosted-v1' / 'pricing.json'
    # Docker mounts reports writable at /reports.
    if Path('/reports/hosted-v1').is_dir():
        output = Path('/reports/hosted-v1/pricing.json')
    output.write_text(json.dumps(reconcile(), default=str, indent=2) + '\n')
    print(output)
