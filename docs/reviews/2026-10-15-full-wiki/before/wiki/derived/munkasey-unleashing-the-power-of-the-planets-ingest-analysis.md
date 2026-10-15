---
title: "Michael Munkasey - Midpoints: Unleashing the Power of the Planets Ingest Analysis"
page_type: derived
slug: munkasey-unleashing-the-power-of-the-planets-ingest-analysis
status: source_grounded
framework_scope: comparative
source_pages: []
updated_at: 2026-04-22
---

## Purpose

Assess whether Michael Munkasey's *Midpoints: Unleashing the Power of the Planets* is a strong candidate for first-pass ingestion into the live wiki and identify the cleanest ingest boundary.

## Evidence Base

- Vault file: `Stellar Influences Vault/midpoints - Michael Munkasey - Unleashing the Power of the Planets.pdf`
- PDF metadata: `394` pages, embedded table of contents, and clean text extraction via `fitz`
- Structural explanation pages: printed pages `24`-`31`
- Factor keyword section: printed pages `42`-`54`
- Midpoint corpus: printed pages `55`-`366`

## Analysis

### Structural Fit

- The source is a strong ingest candidate.
- It uses a closed `13`-factor inventory already present in the live canonical corpus: `Sun`, `Moon`, `Mercury`, `Venus`, `Mars`, `Jupiter`, `Saturn`, `Uranus`, `Neptune`, `Pluto`, `Node`, `Asc`, and `MC`.
- It does not require new factor identities such as transneptunians, `Vernal Point`, or `Chiron`.
- The midpoint corpus is mechanically regular: `78` distinct pair headings, no missing headings, and an exact four-page cadence from PDF page `56` through PDF page `364`.

### What The Source Actually Provides

- Chapter 5 provides `13` standalone factor keyword pages, one for each factor in the source inventory.
- Each midpoint pair then occupies four pages:
- Page 1 gives axis-level material under recurring headings: `Basic Ideas`, `In Your Personal Life`, `In Your Relationships`, `With Body or Mind`, and `In Politics or Business`.
- Page 2 gives explicit activator meanings for the non-axis factors.
- Page 3 gives an uncategorized `CONCEPTS` phrase list for the pair.
- Page 4 gives two `With Itself` activations plus MWA-derived example lists of people and events.

### Canonical Coverage If Ingested

- Axis pages touched: `78`
- Activation pages touched: `1014`
- Distinct-factor activation pages among those: `858`
- Duplicate-factor activations such as `Sun/Moon = Sun`: `156`
- Distinct triad hubs implied by the corpus: `286`
- Factor pages touched: `13`

### Recommended First-Pass Boundary

- Ingest the `13` factor keyword pages into the canonical factor pages as source-native keyword blocks.
- Ingest midpoint page 1 into the canonical axis pages.
- Ingest midpoint page 2 into the canonical activation pages.
- Ingest the two `With Itself` entries at the top of midpoint page 4 into the canonical activation pages as duplicate-factor activations.
- Defer midpoint page 3 `CONCEPTS` lists in the first pass.
- Defer the MWA example lists on midpoint page 4 in the first pass.

### Why This Boundary Is The Cleanest

- Page 1 and page 2 map cleanly to the repo's current factor, axis, and activation model.
- The `With Itself` material is explicit oriented doctrine and fits the existing activation identity rules, even though those activations do not create triad hubs.
- The `CONCEPTS` pages are explicit source material, but they are large, uncategorized, and would materially bloat the canonical axis pages without fitting the current comparative schema cleanly.
- The MWA examples are not doctrine in the same sense as the midpoint definitions; they are ranked examples and would be better handled by a later evidence or exemplars layer if we choose to preserve them.

### Extraction Risk

- The PDF is text-extractable and does not look like a scan-rescue job.
- The recurring page headings are stable enough for scripted extraction.
- A light label-normalization pass is still needed. One confirmed example is `Merc` appearing where the surrounding corpus usually uses `Mer` on the `Venus/Saturn with Planets and Points` page.
- Ordinary line-wrap and hyphen cleanup will still be needed, but this source is much closer to the already-ingested midpoint corpora than to an OCR triage case.

### Framework Notes

- Munkasey explicitly acknowledges Ebertin and emulates the broad page format, so this source is midpoint-centric and COSI-adjacent.
- At the same time, the tone and topical spread are broader and more modern than strict Ebertin chapter taxonomy.
- If ingested, the safest framework label is probably `modern_astrology` unless we want a more specific midpoint or cosmobiology-adjacent scope label.

## Contradictions and Notes

- Munkasey's page-1 `Thesis` and `Anti` pairings should be preserved as source-native contrasts, not flattened into simple positive and negative doctrine.
- The source does not provide repeated-pair axes such as `Sun/Sun`; it provides distinct midpoint axes plus duplicate-factor activations like `Sun/Moon = Sun`.
- Because the live wiki already contains the full shared factor inventory, this source should deepen existing comparative pages rather than expand the ontology.

## Open Questions

- Should the eventual source page classify Munkasey as `modern_astrology`, or do we want a more specific midpoint-oriented framework scope?
- Do we want to preserve the page-3 `CONCEPTS` corpus anywhere in v1, or leave it out entirely until a better page type exists?
- Should the page-4 MWA examples be ignored, preserved only on the future source page, or modeled later as a separate evidence layer?
