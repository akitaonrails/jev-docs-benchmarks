"""Build locked environments in a dedicated LOCAL builder whose cache can be removed."""
import json
from pathlib import Path
import subprocess
from runtime import require_local_docker

ROOT=Path(__file__).resolve().parents[1]
FAMILIES=('qwen','encoders','decider','julia','d3','clef','simple')
BUILDER='jev-cuda-benchmark'


def main():
    require_local_docker()
    tags=subprocess.check_output(['docker','image','ls','--format','{{.Repository}}'],text=True).splitlines()
    if any('jev-cuda-'+f in tags for f in FAMILIES):
        raise RuntimeError('CUDA benchmark tags already exist; reuse or clean them before rebuilding')
    if subprocess.run(['docker','buildx','inspect',BUILDER],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL).returncode==0:
        raise RuntimeError('Dedicated builder already exists; inspect/clean the previous run')
    manifest=ROOT/'results/cuda-resources.json'
    inventory={'builder_name':BUILDER,'images':{},'volumes':[],'build_cache_ids':[]}
    manifest.parent.mkdir(exist_ok=True)
    manifest.write_text(json.dumps(inventory,indent=2)+'\n')
    subprocess.run(['docker','buildx','create','--name',BUILDER,'--driver','docker-container','default'],check=True)
    for family in FAMILIES:
        tag='jev-cuda-'+family
        subprocess.run(['docker','buildx','build','--builder',BUILDER,'--load','--build-arg','FAMILY='+family,'-f',str(ROOT/'cuda/Dockerfile.locked'),'-t',tag,str(ROOT)],check=True)
        inventory['images'][tag]=json.loads(subprocess.check_output(['docker','image','inspect',tag]))[0]['Id']
        manifest.write_text(json.dumps(inventory,indent=2)+'\n')

if __name__=='__main__':main()
