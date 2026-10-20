#!/usr/bin/env python3
"""Mechanical submission checks; scientific content/fullness need human review."""
import re
import sys
from pathlib import Path
try:
    import fitz
except ImportError:
    sys.exit('Install checker dependency: python -m pip install -r requirements-dev.txt')

ROOT = Path(__file__).resolve().parents[1]
pdf_path = ROOT / 'build/main.pdf'
log_path = ROOT / 'build/main.log'
aux_path = ROOT / 'build/main.aux'
errors = []
if not all(p.exists() for p in [pdf_path, log_path, aux_path]):
    sys.exit('First run: python scripts/build.py')
log = log_path.read_text(encoding='utf-8', errors='replace')
aux = aux_path.read_text(encoding='utf-8', errors='replace')
if 'PREVIEW ONLY' in log:
    errors.append('Preview font is forbidden in a submission.')
counts = re.findall(r'KIB-ABSTRACT-LINES:\s*(\d+)', log)
if not counts or not 5 <= int(counts[-1]) <= 8:
    errors.append('Abstract must be one paragraph with 5--8 rendered lines.')
for pattern in [r'Overfull \\[hv]box', r'Missing character:', r'Citation .+ undefined',
                r'Reference .+ undefined', r'There were undefined references',
                r'Font shape .+ undefined', r'Rerun to get']:
    if re.search(pattern, log):
        errors.append('LaTeX log contains: ' + pattern)
if 'No hyphenation patterns were loaded' in log:
    errors.append('Install Russian hyphenation patterns (texlive-lang-cyrillic) and rebuild formats.')
source = '\n'.join(re.sub(r'(?m)(?<!\\)%.*$', '', p.read_text(encoding='utf-8'))
                   for p in (ROOT / 'content').glob('*.tex'))
for placeholder in ['И.О. ФАМИЛИЯ', 'Название доклада', 'Наименование организации',
                    'Здесь необходимо', 'Здесь следует', 'Этот проект содержит', '\\bibitem{sample}']:
    if placeholder in source:
        errors.append('Replace template content: ' + placeholder)
cited = []
for group in re.findall(r'\\citation\{([^}]+)\}', aux):
    for key in group.split(','):
        if key not in cited:
            cited.append(key)
listed = re.findall(r'\\bibcite\{([^}]+)\}', aux)
if cited != listed:
    errors.append('Bibliography must contain exactly cited sources in order of first citation.')
with fitz.open(pdf_path) as doc:
    if len(doc) != 2:
        errors.append(f'Expected exactly 2 pages; found {len(doc)}.')
    mm = 72 / 25.4
    for n, page in enumerate(doc, 1):
        if abs(page.rect.width - 148*mm) > .5 or abs(page.rect.height - 210*mm) > .5:
            errors.append(f'Page {n}: expected 148 x 210 mm.')
        for font in page.get_fonts(full=True):
            xref, ext, kind, name = font[:4]
            if xref and not doc.extract_font(xref)[3]:
                errors.append(f'Page {n}: font {name} is not embedded.')
        blocks = page.get_text('dict')['blocks']
        for block in blocks:
            if block.get('type') != 0:
                continue
            for line in block['lines']:
                for span in line['spans']:
                    text = span['text'].strip()
                    if not text:
                        continue
                    x0, y0, x1, y1 = span['bbox']
                    if x0 < 17*mm-1.5 or x1 > 130*mm+1.5 or y0 < 23*mm-1.5 or y1 > 185*mm+1.5:
                        errors.append(f'Page {n}: text outside margins: {text[:45]}')
                    # Formula fonts may differ; Russian letters must be Times New Roman.
                    if re.search('[А-Яа-яЁё]', text) and 'TimesNewRoman' not in span['font'].replace('-', '').replace(' ', ''):
                        errors.append(f'Page {n}: Cyrillic text is not Times New Roman ({span["font"]}).')
                    if span['color'] != 0:
                        errors.append(f'Page {n}: nonblack text: {text[:35]}')
        if n == 2:
            boxes = [b['bbox'] for b in blocks if b.get('type') == 0]
            if boxes:
                print(f'Last text on page 2 ends at {max(b[3] for b in boxes)/mm:.1f} mm; inspect page fullness manually.')
if errors:
    print('NOT READY FOR SUBMISSION:')
    for item in dict.fromkeys(errors):
        print(' -', item)
    sys.exit(1)
print('Mechanical checks passed. Manually verify page fullness, figures, content, bibliography and DOCX match.')
