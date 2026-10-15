# DoneClaim: Markdown/prose corruption repair

## Changed files

- `wiki/axes/moon-jupiter.md`
- `wiki/axes/mars-jupiter.md`
- `wiki/axes/mars-uranus.md`
- `wiki/axes/sun-moon.md`
- `wiki/axes/sun-saturn.md`
- `wiki/axes/jupiter-neptune.md`
- `wiki/axes/mercury-asc.md`
- `wiki/axes/venus-node.md`

Generated query/index files were checked after rebuild; none changed in `git diff --name-only -- wiki`.

## Exact fixes

- Restored Carter prose from `ccfbfb72^` in `wiki/axes/moon-jupiter.md`:
  - before line 127: `...exaltation of`
  - after line 127: `...exaltation of Jupiter in Cancer.`
  - before line 139: `For some reason which I do not understand Moon Trine`
  - after line 139: `For some reason which I do not understand Moon Trine Jupiter in Air is common in the maps of violent criminals. Perhaps it aids the criminal to disguise his proclivities.`
- Restored Carter prose from `ccfbfb72^` in `wiki/axes/mars-jupiter.md`:
  - before line 143: `...The Sun was with`
  - after line 143: completed through `...the native did abandon monastic life, and married.`
- Restored Carter prose from `ccfbfb72^` in `wiki/axes/mars-uranus.md`:
  - before line 133: `...but with Sun and`
  - after line 133: completed through `...would probably have collapsed altogether.`
- Restored Carter prose from `ccfbfb72^` in `wiki/axes/sun-moon.md`:
  - before line 148: `...A child with the`
  - after line 148: completed through `...important though these are in their spheres.`
- Restored Carter prose from `ccfbfb72^` in `wiki/axes/sun-saturn.md`:
  - before line 151: `...In a case of the Sun Squared by`
  - after line 151: completed through `...bearing it in an idealistic spirit.`
- Repaired embedded schema headings:
  - `wiki/axes/jupiter-neptune.md`: before line 239 had `...Intoxication. ## Comparative Schema`; after lines 239-241 separate the bullet from column-zero `## Comparative Schema`.
  - `wiki/axes/mercury-asc.md`: before line 173 had `...contradiction. ## Comparative Schema`; after lines 173-175 separate the bullet from column-zero `## Comparative Schema`.
  - `wiki/axes/venus-node.md`: before line 171 had `...difficult to satisfy. ## Comparative Schema`; after lines 171-173 separate the bullet from column-zero `## Comparative Schema`.

## Verification

Scenario: wiki lint before generated rebuilds.
Invocation: `C:/pyMADMAX2/miniconda3/envs/deep11/python.exe tools/lint_wiki.py`
Binary observable: exit code 0; stdout `Lint passed`.
Captured artifact path: `.codex_tmp/evidence/repair-markdown-prose-corruption-20260620.md`.

Scenario: generated index rebuild.
Invocation: `C:/pyMADMAX2/miniconda3/envs/deep11/python.exe tools/rebuild_index.py`
Binary observable: exit code 0; no stdout.
Captured artifact path: `.codex_tmp/evidence/repair-markdown-prose-corruption-20260620.md`.

Scenario: generated query manifest rebuild.
Invocation: `C:/pyMADMAX2/miniconda3/envs/deep11/python.exe tools/query_manifest.py`
Binary observable: exit code 0; no stdout.
Captured artifact path: `.codex_tmp/evidence/repair-markdown-prose-corruption-20260620.md`.

Scenario: wiki lint after generated rebuilds.
Invocation: `C:/pyMADMAX2/miniconda3/envs/deep11/python.exe tools/lint_wiki.py`
Binary observable: exit code 0; stdout `Lint passed`.
Captured artifact path: `.codex_tmp/evidence/repair-markdown-prose-corruption-20260620.md`.

Scenario: repaired snippet inspection.
Invocation: PowerShell `Get-Content` line-window inspections on all eight changed files.
Binary observable: inspected lines show completed Carter prose at `moon-jupiter.md:127`, `moon-jupiter.md:139`, `mars-jupiter.md:143`, `mars-uranus.md:133`, `sun-moon.md:148`, `sun-saturn.md:151`, and column-zero schema headings at `jupiter-neptune.md:241`, `mercury-asc.md:175`, `venus-node.md:173`.
Captured artifact path: `.codex_tmp/evidence/repair-markdown-prose-corruption-20260620.md`.

Scenario: old corruption pattern check.
Invocation: `rg -n "exaltation of$|Moon Trine$|The Sun was with$|but with Sun and$|A child with the$|Sun Squared by$|## Comparative Schema" wiki/axes/moon-jupiter.md wiki/axes/mars-jupiter.md wiki/axes/mars-uranus.md wiki/axes/sun-moon.md wiki/axes/sun-saturn.md wiki/axes/jupiter-neptune.md wiki/axes/mercury-asc.md wiki/axes/venus-node.md`
Binary observable: exit code 0; output includes only column-zero `## Comparative Schema` matches at the eight axis pages, with no truncated-fragment matches.
Captured artifact path: `.codex_tmp/evidence/repair-markdown-prose-corruption-20260620.md`.

Scenario: changed wiki file surface.
Invocation: `git diff --name-only -- wiki`
Binary observable: exit code 0; output only the eight changed axis files listed above. Git emitted line-ending warnings for `jupiter-neptune.md`, `mercury-asc.md`, `sun-moon.md`, and `venus-node.md`.
Captured artifact path: `.codex_tmp/evidence/repair-markdown-prose-corruption-20260620.md`.

## Residual risk

- `apply_patch` failed twice with a Windows sandbox helper error before any file edit; the actual edits were made with exact .NET text replacements that failed if expected corrupted strings were absent.
- Git reports existing/autocrlf line-ending warnings for four edited files. No generated query/index files changed, and lint passed before and after rebuilds.