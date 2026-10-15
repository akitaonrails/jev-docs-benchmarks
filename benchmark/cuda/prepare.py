"""Freeze the CUDA deployment registry from the original ROCm selectors/commands."""
import json
from runtime import require_local_docker
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
GROUPS = {
 'qwen': {'eikos-4b':'eikos4b', 'jebadiah-4b-v2':'jebadiah4b', 'kev-0.8b':'kev', 'kev-4b':'kev', 'kev-9b':'kev'},
 'encoders': {'laya':'hf', 'laya-typed':'hf', 'laya-multilingual':'layaml', 'gliner2.5-decide':'gliner', 'gliner2.5-multi-decide':'gliner'},
 'simple': {'simple-jev':'simplejev'}, 'clef': {'clef-flash-local':'hf'}, 'decider': {'decider-4b':'decider'}, 'julia': {'julia-1':'julia1'}, 'd3': {'d3-edge':'d3_edge'}}

def main():
    require_local_docker()
    original = json.loads((ROOT/'next-wave/models.json').read_text())
    output = {}
    for group, models in GROUPS.items():
        image = json.loads(subprocess.check_output(['docker','image','inspect','jev-cuda-'+group]))[0]['Id']
        for name, volume in models.items():
            config = original.get(name, {'selector': name.replace('-local',''), 'interface':'systemone',
                'command':['uvicorn','app:app','--host','0.0.0.0','--port','8000']}).copy()
            config.update(image=image, container_name='jev-cuda-'+name, base_url='http://127.0.0.1:11500',
                          volume='jev_cuda_'+volume, port=11500, backend='cuda', group=group)
            if group in ('encoders','julia','d3'):
                config['working_dir']='/opt/'+{'encoders':'encoders','julia':'julia','d3':'d3'}[group]
            if name in ('laya','laya-typed','clef-flash-local'):
                config['working_dir']='/opt/systemone'
            if name.startswith('kev-'):
                config['command']=['env','KEV_CUDA_GRAPHS=0','KEV_FUSED=0']+config['command']
            if name=='eikos-4b':
                config['working_dir']=config['command'][1].split('=',1)[1]
            output[name]=config
    (ROOT/'cuda/models.json').write_text(json.dumps(output,indent=2)+'\n')
    inventory=ROOT/'results/cuda-resources.json'
    if inventory.exists():
        resources=json.loads(inventory.read_text())
        existing=subprocess.check_output(['docker','volume','ls','--format','{{.Name}}'],text=True).splitlines()
        resources['volumes']=sorted({c['volume'] for c in output.values()} & set(existing))
        inventory.write_text(json.dumps(resources,indent=2)+'\n')

if __name__=='__main__':main()
