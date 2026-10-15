---
title: Wiki Lint Report 2026-04-21
page_type: maintenance_report
slug: lint-report-2026-04-21
report_date: 2026-04-21
---

# Wiki Health Check

Date: `2026-04-21`

## Commands Run

- `C:/pyMADMAX2/miniconda3/envs/deep11/python.exe tools/rebuild_index.py`
- `C:/pyMADMAX2/miniconda3/envs/deep11/python.exe tools/lint_wiki.py`
- Custom checks for internal relative links, frontmatter presence, page inventory, and shared-factor source coverage

## Findings

- 🔵 `tools/rebuild_index.py` completed successfully and refreshed `wiki/index.md`.
- 🔵 `tools/lint_wiki.py` passed with no activation required-field failures and no alias-orientation collapses.
- 🔵 Internal relative-link check found `0` broken Markdown links across `wiki/**/*.md`.
- 🔵 Inventory snapshot: `6906` markdown files total. `5` template files under `wiki/_templates/` are excluded from live-page linting. Live/special files scanned: `6901`.
- 🔵 Live/special page counts: `22` factor pages, `253` axis pages, `5082` activation pages, `1540` triad hubs, `2` source pages, and `2` special untyped pages (`wiki/index.md`, `wiki/log.md`).
- 🟡 `wiki/derived/` has no live derived articles yet. The comparative synthesis layer exists structurally but is empty in practice.
- 🟡 The current lint workflow is narrow. `tools/lint_wiki.py` only enforces required fields for `activation` pages plus orientation-safe alias rules. `factor`, `axis`, `triad_hub`, and `source` pages are parseable, but they are not schema-validated by the current linter.
- 🟡 The corpus overlap between Witte and Ebertin is not yet surfaced on first-class factor pages. There are `13` shared factors (`Sun`, `Moon`, `Mercury`, `Venus`, `Mars`, `Jupiter`, `Saturn`, `Uranus`, `Neptune`, `Pluto`, `Node`, `Asc`, `MC`), and `0` of those factor pages currently list both sources in frontmatter. All `13` shared factor pages currently point only to Ebertin at the factor-page level.

## Suggested Articles

- 🔵 `wiki/derived/shared-factors-witte-vs-ebertin.md`
  Compare the `13` shared factor chapters side by side and record convergences, divergences, and contradiction notes without collapsing framework boundaries.
- 🔵 `wiki/derived/orientation-matters-sun-moon-venus.md`
  Use the fully populated `Sun/Moon = Venus`, `Sun/Venus = Moon`, and `Moon/Venus = Sun` triad to explain why activation orientations stay distinct and how triad hubs should be read.
- 🔵 `wiki/derived/corpus-coverage-witte-vs-ebertin.md`
  Document why Witte yields the full `22`-factor combinatorial grid while Ebertin is a smaller explicit subset, so readers can distinguish source-driven absences from ingest mistakes.

## Overall Status

- 🔵 No failing lint checks were found in the current AGENTS.md maintenance workflow.
- 🟡 The main gaps are comparative synthesis coverage and limited schema enforcement outside activation pages.
