---
title: "Vault Source Coverage Audit"
page_type: derived
slug: vault-source-coverage-audit
status: source_grounded
framework_scope: comparative
factors: []
aliases: []
source_pages: []
updated_at: 2026-05-06
---

## Purpose

Classify vault PDFs that are present in `Stellar Influences Vault/` but not represented by a source catalog page in `wiki/sources/`.

## Method

- Compared vault PDF filenames against source catalog pages.
- Read PDF metadata, table of contents where available, and first extracted pages.
- Classified each uncataloged PDF as `in-scope`, `out-of-scope`, or `future schema needed` for the current wiki model.

## Non-Catalog PDF Classifications

| Vault PDF | Classification | Reason |
| --- | --- | --- |
| `houses - Michael Munkasey - The Astrological Thesaurus Book.pdf` | future schema needed | House keyword material is potentially useful, but the current canonical page types do not model houses, house systems, quadrants, or house-topic keyword indexes. Do not ingest into factor, axis, or activation pages. |
| `Keywords for Astrology Hajo Banzhaf and Anna Haebler 2024.pdf` | future schema needed | The source is a broad keyword encyclopedia covering planets, signs, houses, aspects, and interpretive levels. Factor keyword excerpts may become useful later, but the source is not midpoint- or formula-native and needs a controlled factor-keyword policy before ingest. |
| `Martha Lang-Wescott - Orders of Light.pdf` | future schema needed | The source contains planets, angles, transneptunians, asteroids, and order/aspect methodology. Some factor material may overlap with the wiki inventory, but asteroids and order technique need a separate schema and scope decision before ingest. |

## Cataloged Vault PDFs

- `Book_2000_Charles Carter_The Astrological Aspects.pdf`
- `Book_2007_Don Mcbroom_Midpoints.pdf`
- `Book_2012_Michelle Falis_AstroFix_Planet Combinations- Astrological Brainstorms_kindle.pdf`
- `Book_2015_John Sandbach_Midpoints_A Kabbalistic Compendium of Meanings for Astrological Midpoints.pdf`
- `midpoints - Michael Munkasey - Unleashing the Power of the Planets.pdf`
- `planetary expressions - Alfred Witte, Ludwig Rudolph & Hermann Lefeldt - Rules for Planetary Pictures 2020.pdf`
- `planetary expressions - Reinhold Ebertin - The Combination Of Stellar Influences.pdf`
- `planetary expressions - Robert Hand - Horoscope Symbols.pdf`
- `Udo-Rudolph_ABC-fur-Planetenbilder.pdf`

## Recommendations

- Do not ingest any non-catalog PDF directly into canonical pages yet.
- If house material becomes a priority, define a house methodology or house keyword page type first.
- If broad keyword dictionaries become a priority, define a factor-keyword companion layer so generic keywords do not dilute source-specific midpoint doctrine.
- If Lang-Wescott becomes a priority, decide whether the wiki will model asteroids and order/aspect methodology, or only extract overlapping factor chapters.

## Links

- [Query Guide](../query-guide.md)
- [Don McBroom - Midpoints](../sources/don-mcbroom-midpoints.md)
