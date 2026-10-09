"""Host-side stdlib launcher. Reads only named exports, never executes secrets file."""
import os
from pathlib import Path
import shlex
import subprocess
import sys

allowed={'JEV_API_KEY','CLOUDFLARE_API_TOKEN','CLOUDFLARE_ACCOUNT_ID'}
env=os.environ.copy()
for line in (Path.home()/'.config/zsh/secrets').read_text().splitlines():
    stripped=line.strip()
    if not stripped.startswith('export '): continue
    name,sep,value=stripped[7:].partition('=')
    if sep and name in allowed:
        words=shlex.split(value,comments=True)
        if len(words)!=1: raise SystemExit('Expected literal credential export for '+name)
        env[name]=words[0]
root=Path(__file__).resolve().parents[2]
cmd=['docker','compose','-f',str(root/'benchmark/compose.yaml'),'--profile','hosted','run','--rm','-T','hosted',*sys.argv[1:]]
raise SystemExit(subprocess.call(cmd,env=env,cwd=root))
