"""Offline credential presence check. Never prints credential values."""
import os
import re

for name in ('JEV_API_KEY', 'CLOUDFLARE_API_TOKEN', 'CLOUDFLARE_ACCOUNT_ID'):
    value = os.environ.get(name, '')
    status = 'present (not authenticated)' if value else 'MISSING'
    if name == 'CLOUDFLARE_ACCOUNT_ID' and value and not re.fullmatch(r'[a-fA-F0-9]{32}', value):
        status = 'INVALID FORMAT (expected 32 hexadecimal characters)'
    print(f'{name}: {status}')
