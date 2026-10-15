# Stellar Influences Remaining Book Ingestion Report

Date: 2026-06-20

## Sources Ingested

- Hajo Banzhaf and Anna Haebler, *Keywords for Astrology*: source page, 11 factor pages, and 70 axis pages. Committed in `ccfbfb72`.
- L. Edward Johndro, *Astrological Dictionary*: source page and 10 planetary factor pages. Committed in `ccfbfb72`.
- Manly P. Hall, *Astrological Keywords*: source page and 9 factor pages. Committed in `67f2a445`.
- Michael Harding and Charles Harvey, *Working with Astrology*: source page and `Sun/Moon` axis entry only. Committed in `91f68967`.
- Zane B. Stein, *The Quadrant Midpoints*: source page plus `Sun/Moon` and `Asc/MC` axis entries only. Committed in `b76b40ff`.
- Aren Ober, *Midpoint Interpretation Simplified*: source page, `Jupiter/Uranus` and `Sun/Jupiter` axis entries, and 14 oriented activation entries from explicit chapter 8 examples. Committed in `7fabdb01`.

## Sources Held or Skipped

- Hans Niggemann, *Rules for Planetary Pictures*: held. Sample manifest failed reliability gates: OCR-broken headings, unknown tokens, row-order conflicts, missing/extra rows, and body text parsed as activation rows.
- Michael Feist, *Lexicon for Planetary Pictures*: held. Parser found 37,711 current-schema rows, but all duplicated existing Witte-backed activation pages and 1,299 formula-like rows remained OCR/token rejects.
- Uranian Astrology, *Master-Lexicon v2_1*: held. Manifest showed 6,506 parsed rows, 17,830 rejects, 6,402 Witte duplicate rows, and severe OCR/glyph corruption.
- D.M. Baker, *Colloquialism*: held. Manifests showed 0 decoded current-schema rows, 755 formula-like rejects, 741 unknown glyphs, and 720 sign/house/aspect contamination hits.

## Pages Changed

- New accepted source pages: `hajo-banzhaf-anna-haebler-keywords-for-astrology.md`, `l-edward-johndro-astrological-dictionary.md`, `manly-p-hall-astrological-keywords.md`, `michael-harding-charles-harvey-working-with-astrology.md`, `zane-b-stein-the-quadrant-midpoints.md`, `aren-ober-midpoint-interpretation.md`.
- Canonical factors updated by accepted factor sources: Sun, Moon, Mercury, Venus, Mars, Jupiter, Saturn, Uranus, Neptune, Pluto, Node as applicable by source.
- Canonical axes updated by accepted sources include `Sun/Moon`, `Asc/MC`, `Jupiter/Uranus`, `Sun/Jupiter`, plus Banzhaf axis coverage from the earlier committed batch.
- Canonical activations updated by Ober: `Jupiter/Uranus = Sun/Moon/Mercury/Venus/Mars/Node` and `Sun/Jupiter = Moon/Mercury/Venus/Mars/Saturn/Uranus/Neptune/Pluto`.
- Rebuilt generated surfaces: `wiki/index.md`, `wiki/query-guide.md`, `wiki/query-manifest.json`. Committed in `c3604b71`.

## Verification

- Per accepted source batch: `C:/pyMADMAX2/miniconda3/envs/deep11/python.exe -B tools/lint_wiki.py` passed.
- Final rebuild commands passed:
  - `C:/pyMADMAX2/miniconda3/envs/deep11/python.exe -B tools/rebuild_index.py`
  - `C:/pyMADMAX2/miniconda3/envs/deep11/python.exe -B tools/query_manifest.py`
  - `C:/pyMADMAX2/miniconda3/envs/deep11/python.exe -B tools/lint_wiki.py` -> `Lint passed`
- Representative page inspection covered `wiki/factors/sun.md`, `wiki/factors/moon.md`, `wiki/axes/sun-moon.md`, `wiki/axes/asc-mc.md`, `wiki/axes/jupiter-uranus.md`, `wiki/activations/venus-vulcanus-equals-jupiter.md`, `wiki/activations/jupiter-uranus-equals-sun.md`, `wiki/activations/sun-jupiter-equals-moon.md`, and `wiki/triads/sun-jupiter-uranus.md`.
- Final `git status --short -- wiki` is clean except pre-existing/untracked `wiki/.obsidian/`.

## Unresolved Decisions

- Minor-body and angle canon expansion remains out of scope: IC/DSC, DSC/MC, ASC/IC, Eris, and similar material were held.
- Hans/Master-Lexicon need more reliable OCR or page-image-assisted parsers before any import.
- Feist may be useful only as a reverse-index/source-companion artifact, not as canonical doctrine, unless duplicate handling policy changes.
- Baker requires a verified glyph-font mapping and a model for colloquial/glyph references before current-schema import is safe.