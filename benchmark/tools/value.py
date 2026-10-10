"""Value frozen classifications at dated prices; no network or inference."""
import gzip
import hashlib
import json
from decimal import Decimal as D
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def evaluate():
    cases = {c['id']: c for c in map(json.loads, (ROOT / 'datasets/cases.jsonl').read_text().splitlines())}
    prices = json.loads((ROOT / 'pricing/2026-10-10.json').read_text())
    historical = json.loads((ROOT / 'reports/hosted-v1/pricing.json').read_text())['input_usd_per_million']
    output = {'prices': prices, 'historical_input_usd_per_million': historical,
              'scope': '520 classification variants/model; smoke and probability probes excluded',
              'models': {}, 'source_archive_sha256': {}}
    for run in ('hosted-v1', 'homelab-v1'):
        raw = gzip.decompress((ROOT / 'reports' / run / 'responses.jsonl.gz').read_bytes())
        output['source_archive_sha256'][run] = hashlib.sha256(raw).hexdigest()
        rows = [json.loads(line) for line in raw.splitlines()]
        for model in sorted({r['model'] for r in rows}):
            selected = [r for r in rows if r['model'] == model and cases[r['case_id']]['kind'] == 'classification']
            assert len(selected) == 520 and all(r['result'] and not r['error'] for r in selected)
            inputs = sum(r['result']['usage']['input_tokens'] for r in selected)
            correct = sum(r['result']['choice'] == cases[r['case_id']]['gold'] for r in selected)
            entry = {'classifications': len(selected), 'correct': correct, 'input_tokens': inputs,
                     'historical_classification_list_usd': None, 'current_classification_list_usd': None,
                     'current_usd_per_1000_classifications': None, 'current_usd_per_1000_correct_labels': None}
            if model in prices['input_usd_per_million']:
                cost = D(inputs) * D(prices['input_usd_per_million'][model]) / 1_000_000
                entry.update(historical_classification_list_usd=D(inputs) * D(historical[model]) / 1_000_000,
                             current_classification_list_usd=cost,
                             current_usd_per_1000_classifications=cost * 1000 / len(selected),
                             current_usd_per_1000_correct_labels=cost * 1000 / correct)
            entry['server_classification_seconds'] = sum(D(str(r['response']['server']['predict_s'])) for r in selected) if run == 'homelab-v1' else None
            output['models'][model] = entry
    models = output['models']
    output['equal_error_cost_break_even_usd'] = {}
    for better in ('jev', 'clef'):
        extra_cost = models[better]['current_classification_list_usd'] - models['clef-flash']['current_classification_list_usd']
        fewer_errors = models[better]['correct'] - models['clef-flash']['correct']
        output['equal_error_cost_break_even_usd'][better + '_versus_flash'] = extra_cost / fewer_errors
    return output


if __name__ == '__main__':
    output = Path('/reports/comparison-v1') if Path('/reports').is_dir() else ROOT / 'reports/comparison-v1'
    result = evaluate()
    (output / 'classification-costs.json').write_text(json.dumps(result, default=str, indent=2) + '\n')
    print(json.dumps(result, default=str, indent=2))
