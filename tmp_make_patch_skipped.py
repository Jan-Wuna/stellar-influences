from pathlib import Path
import re

root = Path(r'W:/Stellar Influences')
skipped = [
    Path('wiki/activations/sun-admetos-equals-poseidon.md'),
    Path('wiki/activations/sun-admetos-equals-uranus.md'),
    Path('wiki/activations/sun-apollon-equals-neptune.md'),
    Path('wiki/activations/sun-apollon-equals-uranus.md'),
    Path('wiki/activations/sun-apollon-equals-venus.md'),
    Path('wiki/activations/sun-cupido-equals-admetos.md'),
    Path('wiki/activations/sun-cupido-equals-kronos.md'),
    Path('wiki/activations/sun-hades-equals-apollon.md'),
    Path('wiki/activations/sun-hades-equals-jupiter.md'),
    Path('wiki/activations/sun-hades-equals-neptune.md'),
    Path('wiki/activations/sun-hades-equals-pluto.md'),
    Path('wiki/activations/sun-hades-equals-uranus.md'),
    Path('wiki/activations/sun-kronos-equals-admetos.md'),
    Path('wiki/activations/sun-kronos-equals-apollon.md'),
    Path('wiki/activations/sun-kronos-equals-cupido.md'),
    Path('wiki/activations/sun-kronos-equals-jupiter.md'),
    Path('wiki/activations/sun-kronos-equals-neptune.md'),
    Path('wiki/activations/sun-poseidon-equals-saturn.md'),
    Path('wiki/activations/sun-vulcanus-equals-neptune.md'),
    Path('wiki/activations/sun-vulcanus-equals-uranus.md'),
    Path('wiki/activations/sun-zeus-equals-apollon.md'),
    Path('wiki/activations/sun-zeus-equals-cupido.md'),
    Path('wiki/activations/sun-zeus-equals-saturn.md'),
    Path('wiki/axes/sun-chiron.md'),
]

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
        take = cs[:3]
        if len(take) == 1:
            return f'- This axis centers on {lc(take[0])}.'
        if len(take) == 2:
            return f'- This axis centers on {lc(take[0])} and {lc(take[1])}.'
        return f'- This axis centers on {lc(take[0])}, {lc(take[1])}, and {lc(take[2])}.'
    take = cs[:2]
    if len(take) == 1:
        return f'- This formula emphasizes {lc(take[0])}.'
    return f'- This formula emphasizes {lc(take[0])} and {lc(take[1])}.'

patch = ['*** Begin Patch']
for rel in skipped:
    p = root / rel
    text = p.read_text(encoding='utf-8')
    page_type = re.search(r'^page_type:\s*(.+)$', text, re.M).group(1).strip()
    m = re.search(r'#### (?:Witte|Sandbach) Entry\n\n(.+?)\n## Comparative Schema', text, re.S)
    if not m:
        m = re.search(r'#### Pair Summary\n\n(.+?)\n## Comparative Schema', text, re.S)
    if not m:
        m = re.search(r'#### Principle\n\n(.+?)\n\n#### Process', text, re.S)
    if not m:
        raise SystemExit(f'No entry matched for {rel}')
    new = synth(page_type, m.group(1).strip())
    patch.append(f'*** Update File: {rel.as_posix()}')
    patch.append('@@')
    patch.append('-- None yet beyond source structuring.')
    patch.append(f'+{new}')
patch.append('*** End Patch')
out = root / 'tmp_sun_synth_skipped.patch'
out.write_text('\n'.join(patch) + '\n', encoding='utf-8')
print(out)
