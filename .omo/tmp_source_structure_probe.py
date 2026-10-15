from __future__ import annotations
from pathlib import Path
import re
import fitz

ROOT = Path(r'W:/books references etc/!master list astro')
FILES = [
'harmonics - Michael Harding Charles Harvey - Working with astrology_harmonics, midpoints and Astro_Carto_Graphy.pdf',
'midpoints - Aren Ober - Midpoint Interpretation.pdf',
'midpoints - Hans Niggemann - Rules for planetary pictures.pdf',
"midpoints - Zane B Stein The Quadrant Midpoints The Chart's Backbone.pdf",
'planetary expression - Michael Feist - Lexicon for Planetary Pictures.pdf',
'planetary expressions - D.M. Baker - Colloquialism.pdf',
'planetary expressions - Uranian Astrology - Master-Lexicon v2_1.pdf',
'varia - Manly P Hall - Astrological Keywords.pdf',
]
patterns = [
    re.compile(r'\bSun\s*/\s*Moon\b', re.I),
    re.compile(r'\bSun\s*[-+]\s*Moon\b', re.I),
    re.compile(r'\bSun\s*/\s*Moon\s*=\s*Venus\b', re.I),
    re.compile(r'\bMoon\s*/\s*Venus\s*=\s*Sun\b', re.I),
    re.compile(r'\bSUN\s*/\s*MOON\b'),
    re.compile(r'\bSUN\s*[-+]\s*MOON\b'),
]
for filename in FILES:
    path = ROOT / filename
    print('\n###', filename)
    if not path.exists():
        print('MISSING')
        continue
    try:
        doc = fitz.open(path)
    except Exception as exc:
        print('OPEN_ERROR', type(exc).__name__, exc)
        continue
    print('pages', len(doc))
    pages = [1, min(2, len(doc)), min(3, len(doc)), max(1, len(doc)//2), len(doc)]
    seen = set()
    for pno in pages:
        if pno in seen: continue
        seen.add(pno)
        text = doc[pno-1].get_text('text')
        clean = re.sub(r'\s+', ' ', text).strip()
        print('sample', pno, 'chars', len(clean), clean[:350].encode('ascii','replace').decode())
    hits = []
    max_pages = min(len(doc), 80 if 'Master-Lexicon' not in filename else 25)
    for i in range(max_pages):
        text = doc[i].get_text('text')
        if any(p.search(text) for p in patterns):
            clean = re.sub(r'\s+', ' ', text).strip()
            hits.append((i+1, clean[:500].encode('ascii','replace').decode()))
            if len(hits) >= 3: break
    print('pattern_hits', hits)
