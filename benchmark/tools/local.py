"""Explicit opt-in local inference worker; no model imports before approval flag.

Input JSONL: objects containing only `state` and `questions`.
Output JSONL: raw model responses. This is setup plumbing, not benchmark scoring.
"""
import argparse
import json
from pathlib import Path
import sys

parser = argparse.ArgumentParser()
parser.add_argument('model', choices=['laya', 'laya-typed', 'clef-flash'])
parser.add_argument('--allow-inference', action='store_true')
args = parser.parse_args()
if not args.allow_inference:
    parser.exit(2, 'Refusing model download/loading. GPU execution requires --allow-inference.\n')

import torch
from huggingface_hub import snapshot_download

if not torch.cuda.is_available():
    raise SystemExit('CUDA unavailable; refusing silent CPU fallback.')
config = json.loads(Path('/work/models.json').read_text())[args.model]
if args.model.startswith('laya'):
    import laya
    model = laya.load(config['repo'], revision=config['revision'], device='cuda', fast=False, compile=False)
    def predict(record):
        return model.predict(record['state'], record['questions'])
else:
    path = snapshot_download(config['repo'], revision=config['revision'])
    sys.path.insert(0, path)
    from joint_schema_model import load_release_model, systemone
    model, processor = load_release_model(path, device='cuda')
    def predict(record):
        return systemone(model, processor, dict(record, model='clef-flash'))

for line in sys.stdin:
    record = json.loads(line)
    if set(record) != {'state', 'questions'}:
        raise ValueError('Input must contain only state and questions; keep gold labels out of requests.')
    with torch.inference_mode():
        response = predict(record)
    print(json.dumps(response), flush=True)
