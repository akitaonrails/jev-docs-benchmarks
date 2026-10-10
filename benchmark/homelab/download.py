"""Download pinned public snapshots; never imports model code or touches a GPU."""
import json
from pathlib import Path
from huggingface_hub import snapshot_download

pins = json.loads(Path('/bench/models.json').read_text())
for name, spec in pins.items():
    path = snapshot_download(spec['repo'], revision=spec['revision'])
    if Path(path).name != spec['revision']:
        raise RuntimeError('Unexpected snapshot revision')
    print(json.dumps({'selector': name, 'repo': spec['repo'], 'revision': spec['revision'], 'snapshot': path}), flush=True)
