from pathlib import Path
import re

root = Path(r'W:/Stellar Influences')
paths = sorted([p for p in root.glob('wiki/**/sun-*.md') if p.is_file()])

def clauses(text):
    text = ' '.join(text.replace('’', "'").replace('–', '-').replace('—', '-').split())
    parts = [p.strip(' .') for p in re.split(r'\.(?:\s+|$)', text)]
    return [p for p in parts if p]

def lc(s):
    return s[:1].lower() + s[1:] if s else s

def synth(page_type, entry):
    cs = clauses(entry)
    if not cs:
        return None
    if page_type == 'axis':
        if len(cs) == 1:
            return f'- This axis centers on {lc(cs[0])}.'
        if len(cs) == 2:
            return f'- This axis centers on {lc(cs[0])} and {lc(cs[1])}.'
        return f'- This axis centers on {lc(cs[0])}, {lc(cs[1])}, and {lc(cs[2])}.'
    if len(cs) == 1:
        return f'- This formula emphasizes {lc(cs[0])}.'
    return f'- This formula emphasizes {lc(cs[0])} and {lc(cs[1])}.'

patch = ['*** Begin Patch']
count = 0
for p in paths:
    text = p.read_text(encoding='utf-8')
    old = '- None yet beyond source structuring.'
    if old not in text:
        continue
    page_type = re.search(r'^page_type:\s*(.+)$', text, re.M).group(1).strip()
    m = re.search(r'#### (?:Witte|Sandbach) Entry\n\n(.+?)\n\n## Comparative Schema', text, re.S)
    if not m:
        m = re.search(r'#### Pair Summary\n\n(.+?)\n## Comparative Schema', text, re.S)
    if not m:
        continue
    new = synth(page_type, m.group(1).strip())
    if not new:
        continue
    rel = p.relative_to(root).as_posix()
    patch.append(f'*** Update File: {rel}')
    patch.append('@@')
    patch.append(f'-{old}')
    patch.append(f'+{new}')
    count += 1
patch.append('*** End Patch')
out = root / 'tmp_sun_synth.patch'
out.write_text('\n'.join(patch) + '\n', encoding='utf-8')
print(count)
print(out)
