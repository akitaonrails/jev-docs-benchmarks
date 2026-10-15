"""Run INSIDE a CUDA image to recreate one cache without the original homelab."""
import argparse
import hashlib
import json
from pathlib import Path


def main():
    from huggingface_hub import snapshot_download
    p=argparse.ArgumentParser();p.add_argument('suffix');a=p.parse_args()
    root=Path('/models')
    evidence=json.loads((Path('/work/reports/cuda-runtime')/('weights-'+a.suffix+'.json')).read_text())
    snapshots={}
    for filename in evidence['files']:
        parts=Path(filename).parts
        repo=parts[2].removeprefix('models--').replace('--','/')
        revision=parts[4]
        snapshots[(repo,revision)]=None
    for repo,revision in sorted(snapshots):
        downloaded=snapshot_download(repo,revision=revision)
        if Path(downloaded).name!=revision:raise RuntimeError('Snapshot revision mismatch')
    refs_path=Path('/work/reports/cuda-runtime')/('refs-'+a.suffix+'.json')
    for name,revision in json.loads(refs_path.read_text()).items():
        destination=root/name
        destination.parent.mkdir(parents=True,exist_ok=True)
        destination.write_text(revision)
    for name,expected in evidence['files'].items():
        f=root/name
        h=hashlib.sha256()
        with f.open('rb') as handle:
            for chunk in iter(lambda:handle.read(8*1024*1024),b''):h.update(chunk)
        if h.hexdigest()!=expected:raise RuntimeError('File differs from measured snapshot: '+name)
    (root/'.transfer-complete').touch()
    print('Downloaded and verified',len(snapshots),'snapshots')

if __name__=='__main__':main()
