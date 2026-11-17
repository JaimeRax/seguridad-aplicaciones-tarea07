#!/usr/bin/env python3
"""Quality Gate SAST: falla ante hallazgos ERROR, HIGH o CRITICAL."""
import json
import sys
from pathlib import Path

if len(sys.argv) != 2:
    print('Uso: python scripts/gate_semgrep.py <semgrep-results.json>', file=sys.stderr)
    sys.exit(2)
p = Path(sys.argv[1])
if not p.is_file():
    print(f'ERROR: no existe reporte Semgrep: {p}', file=sys.stderr)
    sys.exit(2)
try:
    data = json.loads(p.read_text(encoding='utf-8'))
    results = data['results']
    if not isinstance(results, list):
        raise ValueError('results no es lista')
except (ValueError, KeyError, TypeError) as exc:
    print(f'ERROR: reporte Semgrep ilegible: {exc}', file=sys.stderr)
    sys.exit(2)
levels = {'ERROR', 'HIGH', 'CRITICAL'}
blocking = [r for r in results if str(r.get('extra', {}).get('severity', '')).upper() in levels]
print(f'Hallazgos Semgrep: {len(results)}; bloqueantes: {len(blocking)}')
for r in blocking:
    print(f"BLOQUEANTE: {r.get('check_id')} en {r.get('path')}:{r.get('start',{}).get('line','?')}")
if blocking:
    print('QUALITY GATE SAST: FAILED')
    sys.exit(1)
print('QUALITY GATE SAST: SUCCESS')
