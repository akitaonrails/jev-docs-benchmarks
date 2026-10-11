"""Stream SHA256 verification; execute inside the installed container before scoring."""
import hashlib
import json
import sys
from pathlib import Path
root=Path(sys.argv[1])
manifest=json.loads((root/'release-manifest.json').read_text())
verified=[]
for name,expected in manifest['files'].items():
    p=root/name
    h=hashlib.sha256()
    with p.open('rb') as handle:
        for block in iter(lambda:handle.read(8*1024*1024),b''):h.update(block)
    assert p.stat().st_size==expected['bytes'] and h.hexdigest()==expected['sha256'],name
    verified.append({'name':name,**expected})
print(json.dumps({'verified':len(verified),'files':verified},indent=2))
