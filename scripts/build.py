#!/usr/bin/env python3
"""Portable XeLaTeX build; no shell, make, Perl or latexmk required."""
import argparse
from pathlib import Path
import shutil
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--preview', action='store_true', help='DejaVu Serif preview, NOT for submission')
parser.add_argument('--check', action='store_true', help='Run strict submission checks after build')
args = parser.parse_args()
if args.preview and args.check:
    parser.error('--preview cannot be combined with --check')
if not shutil.which('xelatex'):
    sys.exit('XeLaTeX not found. Install TeX Live / MacTeX / MiKTeX, then reopen your terminal.')
out = ROOT / 'build'
out.mkdir(exist_ok=True)
name = 'preview' if args.preview else 'main'
for run in range(1, 4):
    print(f'XeLaTeX pass {run}/3: {name}.tex', flush=True)
    result = subprocess.run(['xelatex', '-no-shell-escape', '-interaction=nonstopmode',
                             '-halt-on-error', '-file-line-error', '-output-directory=build',
                             name + '.tex'], cwd=ROOT, stdout=subprocess.PIPE,
                            stderr=subprocess.STDOUT, encoding='utf-8', errors='replace')
    if result.returncode:
        print(result.stdout[-10000:])
        sys.exit(result.returncode)
print('Built:', out / (name + '.pdf'))
log = (out / (name + '.log')).read_text(encoding='utf-8', errors='replace')
for line in log.splitlines():
    if any(s in line for s in ['KIB-ABSTRACT-LINES:', 'Warning', 'Overfull', 'Missing character']):
        print(line)
if args.preview:
    print('PREVIEW ONLY: wrong font for KIB. Rebuild main.tex with Times New Roman before submission.')
if args.check:
    sys.exit(subprocess.call([sys.executable, str(ROOT / 'scripts/check.py')], cwd=ROOT))
