# Stellar Influences Repo Instructions

## Purpose

This repo is a markdown-first LLM wiki for astrological combinations derived from curated source documents stored in `Stellar Influences Vault/`.

## Working Rules

- Use `C:/pyMADMAX2/miniconda3/envs/deep11/python.exe` for Python commands.
- Treat `Stellar Influences Vault/` as immutable raw source storage.
- Keep the wiki Obsidian-friendly, but do not depend on Obsidian-specific plugins.
- Use `apply_patch` for manual file edits.

## V1 Scope

- Ingest one source at a time.
- Ingest explicit combination formulas stated by a source.
- Ingest standalone factor chapters into factor pages when the source provides them.
- Do not model natal, transit, direction, progression, or timing layers.

## Page Types

- `factor`
- `axis`
- `activation`
- `triad_hub`
- `source`
- `derived`

## Identity Rules

- Factors are first-class doctrine pages.
- Axes are unordered midpoint pairs.
  - `Sun/Moon` and `Moon/Sun` are the same axis.
- Activations are oriented formulas.
  - `Sun/Moon = Venus`
  - `Sun/Venus = Moon`
  - `Moon/Venus = Sun`
  These are distinct pages and must never be merged interpretively.
- Triad hubs normalize unordered three-factor sets only.
  - They are structural hubs, not merged doctrine pages.
- Keep full-name factor identities canonical in filenames, titles, and normalized formulas.
- Astronomicon tokens are display-only helpers and must never replace canonical page identity.
  - Moon through Pluto: `R S T Q U V W X Y Z`
  - Node: `g`
  - TNPs Cupido through Poseidon: `¡ ¢ £ ¤ ¥ ¦ § ¨`

## Canonical Structure

- `wiki/factors/`
- `wiki/axes/`
- `wiki/activations/`
- `wiki/triads/`
- `wiki/sources/`
- `wiki/derived/`
- `wiki/_templates/`
- `wiki/index.md`
- `wiki/log.md`

## Ingest Rules

- Create or update a minimal source page first.
- Preserve source-native categories inside each source subentry.
- Map claims into the shared comparative schema:
  - core meaning
  - psychology
  - body/health
  - social/relationship
  - events/manifestations
  - conflicts/notes
- Preserve exact source page references for every sourced claim.
- Keep conflicting claims side by side.
- Add contradiction notes instead of silently flattening differences.

## Query And Write-Back Rules

- Query the wiki first, not raw sources by default.
- Canonical pages may gain clearly labeled `Derived Synthesis` grounded in existing wiki evidence.
- Do not insert unsourced doctrine into sourced sections.
- Do not use aliases to collapse different activation orientations.

## Maintenance Rules

- `tools/rebuild_index.py` rebuilds `wiki/index.md`.
- `tools/lint_wiki.py` validates frontmatter and orientation-safe identity rules.
- Ignore `wiki/_templates/` when treating markdown files as live pages.
