# Stellar Influences LLM Wiki Design

Date: 2026-04-21
Status: Draft approved in conversation, written for review before implementation

## Purpose

`Stellar Influences` should become a Karpathy-style LLM-maintained wiki for astrological combinations derived from curated source documents stored in `Stellar Influences Vault/`.

The wiki is the maintained knowledge layer between raw source documents and future queries. Raw sources remain immutable. The LLM updates the wiki, preserves provenance, flags contradictions, and compounds useful synthesis over time.

## Scope For V1

V1 is intentionally narrow.

- Ingest one source at a time.
- Process only explicit combination formulas stated by the source.
- Treat the wiki as a doctrine/combinations wiki only.
- Do not model natal, transit, direction, progression, or other application layers.
- Keep factor pages as first-class doctrine pages.
- In v1, populate factor pages only from explicit formula-derived material, not from standalone factor chapters.
- Preserve exact claim-level provenance with exact source page references.

## Approved Design Decisions

- Use a hybrid structure: canonical pages plus source-specific subentries.
- Use mixed doctrine boundaries:
  - Shared canonical track for known-planet midpoint structures.
  - Separate canonical track for Hamburg-only or transneptunian material.
- Normalize equivalent notation, but do not collapse distinct oriented meanings.
- Use claim-level evidence blocks with exact source pages.
- Make factors first-class wiki pages.
- Do not create source-native chapter pages.
- Use semi-supervised ingest:
  - The LLM writes updates directly.
  - Then it reports touched pages and decisions.
- Preserve conflicting claims side by side.
- Add contradiction notes and short reconciliation attempts where possible.
- Make factor pages full doctrine pages.
- Keep sourced material and LLM synthesis separate on factor pages.
- Build the page graph around factors, axes, activation pages, and triad hubs.
- Use readable filenames and full-name formulas rather than abbreviation codes.
- Give each source a minimal source page.
- Design the schema now to accommodate future Hamburg factors.
- Make the wiki Obsidian-friendly, not Obsidian-dependent.
- Use a shared comparative schema:
  - core meaning
  - psychology
  - body/health
  - social/relationship
  - events/manifestations
  - conflicts/notes
- Allow query answers to write back into canonical pages only as clearly labeled derived synthesis.
- Distinguish structural triad normalization from interpretive equivalence.

## Architecture

The repo has three conceptual layers:

1. Raw sources
   - Stored in `Stellar Influences Vault/`
   - Immutable
   - Read by the LLM, never edited by it
2. Wiki
   - Stored in `wiki/`
   - Markdown pages maintained by the LLM
   - Human-browseable in Obsidian or any editor
3. Schema and helper tooling
   - Stored in `AGENTS.md`, `wiki/_templates/`, and `tools/`
   - Defines page identity, workflow, validation, and maintenance rules

Recommended top-level layout:

```text
Stellar Influences Vault/
wiki/
tools/
AGENTS.md
```

Recommended wiki layout:

```text
wiki/
  _templates/
  factors/
  axes/
  activations/
  triads/
  sources/
  derived/
  index.md
  log.md
```

## Identity Model

The core design requirement is to separate structural normalization from doctrinal meaning.

### 1. Factor Identity

Examples:

- `Sun`
- `Moon`
- `Venus`
- `MC`

Factors are first-class doctrine pages.

### 2. Axis Identity

An axis is an unordered midpoint pair.

Example:

- `Sun/Moon`

`Sun/Moon` and `Moon/Sun` are the same axis.

### 3. Activation Identity

An activation page is an oriented formula and keeps its own meaning.

Examples:

- `Sun/Moon = Venus`
- `Sun/Venus = Moon`
- `Moon/Venus = Sun`

These three pages are distinct and must never be merged interpretively.

### 4. Triad-Set Identity

A triad hub is the unordered three-factor set.

Example:

- `{Sun, Moon, Venus}`

The triad hub exists for structural normalization, navigation, provenance rollup, and orientation mapping. It is not a merged interpretation page.

## Page Types

The wiki should contain these page types:

- `factor`
- `axis`
- `activation`
- `triad_hub`
- `source`
- `derived`

### Factor Page

Purpose:

- doctrine page for one factor
- gathers source-backed material and derived synthesis
- links into axes, activations, and sources

### Axis Page

Purpose:

- doctrine page for a bare midpoint axis such as `Sun/Moon`
- distinct from any activation page
- links to all activations that use the axis

### Activation Page

Purpose:

- doctrine page for one oriented formula such as `Sun/Moon = Venus`
- main canonical location for sourced claims about that specific formula

### Triad Hub Page

Purpose:

- structural hub for an unordered three-factor set
- lists all orientation siblings
- records source coverage and cross-orientation contradiction notes
- does not merge meaning

### Source Page

Purpose:

- minimal provenance hub for one document
- bibliographic metadata, scope notes, touched pages, ingest history

### Derived Page

Purpose:

- query-driven synthesis artifact
- may be linked from canonical pages
- may feed back into `Derived Synthesis` sections of canonical pages

## Naming And Slugs

Use readable slugs and full-name formulas.

Examples:

- `wiki/factors/sun.md`
- `wiki/axes/sun-moon.md`
- `wiki/activations/sun-moon-equals-venus.md`
- `wiki/triads/sun-moon-venus.md`
- `wiki/sources/reinhold-ebertin-the-combination-of-stellar-influences.md`

Rules:

- axis filenames normalize midpoint order only
- activation filenames preserve orientation
- triad filenames sort only at the unordered triad-set level
- aliases may capture notation variants
- aliases must not imply interpretive equivalence across different orientations

## Frontmatter Contracts

All pages should use YAML frontmatter.

Common fields:

```yaml
title:
page_type:
slug:
status:
framework_scope:
factors:
aliases:
source_pages:
updated_at:
```

### Activation Frontmatter

```yaml
title: Sun/Moon = Venus
page_type: activation
slug: sun-moon-equals-venus
normalized_formula: Sun/Moon = Venus
axis: Sun/Moon
activated_by: Venus
triad_set:
  - Sun
  - Moon
  - Venus
framework_scope: cosmobiology
aliases: []
source_pages: []
updated_at:
```

### Axis Frontmatter

```yaml
title: Sun/Moon
page_type: axis
slug: sun-moon
normalized_axis: Sun/Moon
factor_a: Sun
factor_b: Moon
related_activations: []
related_triad_hubs: []
framework_scope: cosmobiology
factors:
  - Sun
  - Moon
aliases: []
source_pages: []
updated_at:
```

### Triad Hub Frontmatter

```yaml
title: Sun Moon Venus
page_type: triad_hub
slug: sun-moon-venus
triad_set:
  - Sun
  - Moon
  - Venus
orientations:
  - Sun/Moon = Venus
  - Sun/Venus = Moon
  - Moon/Venus = Sun
framework_scope: mixed
factors:
  - Sun
  - Moon
  - Venus
aliases: []
source_pages: []
updated_at:
```

## Body Schema

### Activation Page Sections

Required sections:

1. `## Identity`
2. `## Source Entries`
3. `## Comparative Schema`
4. `## Contradictions`
5. `## Derived Synthesis`
6. `## Links`

Each source entry preserves source-native categories if they exist.

The comparative schema always uses these shared buckets:

- core meaning
- psychology
- body/health
- social/relationship
- events/manifestations
- conflicts/notes

### Axis Page Sections

Required sections:

1. `## Identity`
2. `## Source Entries`
3. `## Comparative Schema`
4. `## Related Activations`
5. `## Contradictions`
6. `## Derived Synthesis`
7. `## Links`

### Triad Hub Sections

Required sections:

1. `## Identity`
2. `## Orientation Map`
3. `## Source Coverage`
4. `## Contradictions Across Orientations`
5. `## Links`

The triad hub must never present a merged doctrinal interpretation for the whole set.

### Factor Page Sections

Required sections:

1. `## Identity`
2. `## Source Entries`
3. `## Comparative Schema`
4. `## Derived Synthesis`
5. `## Related Axes`
6. `## Related Activations`
7. `## Related Sources`
8. `## Open Questions`

### Source Page Sections

Required sections:

1. `## Bibliographic Metadata`
2. `## Scope Notes`
3. `## Factors Covered`
4. `## Axes Covered`
5. `## Activations Covered`
6. `## Ingestion History`

## Claim And Evidence Format

Claims should be atomic and auditable.

Recommended markdown pattern:

```md
- Claim: emotional harmony in partnership
  Source: [[reinhold-ebertin-the-combination-of-stellar-influences]]
  Pages: 78-79
  Evidence note: paraphrase of relationship and manifestation language
```

Optional short quotes may appear, but only as subordinate evidence support.

## Workflow

### Ingest

Ingest is semi-supervised and source-first.

Recommended sequence:

1. Read one source from `Stellar Influences Vault/`
2. Create or update its source page
3. Extract only explicit combination formulas for v1
4. Normalize each extracted item into:
   - activation page
   - linked axis page
   - linked triad hub page
   - affected factor pages
5. Preserve source-native categories inside the source subentry
6. Map claims into the shared comparative schema
7. Record contradictions explicitly
8. Update `wiki/index.md`
9. Append an ingest entry to `wiki/log.md`
10. Report touched pages and ambiguous decisions

### Query

Queries operate against the wiki first, not raw sources by default.

Recommended sequence:

1. Read `wiki/index.md`
2. Open relevant wiki pages
3. Synthesize an answer from the wiki
4. Preserve source-backed provenance in the answer
5. Optionally write valuable synthesis back into the wiki

### Write-Back

Write-back is allowed, but only with clear boundaries.

Canonical pages may be updated by queries in two ways:

- improve organization, linkage, contradiction notes, or comparison structure
- add clearly labeled `Derived Synthesis` grounded in existing wiki evidence

Canonical pages must not:

- insert unsourced doctrine into sourced sections
- collapse distinct activation orientations
- introduce natal, transit, direction, or progression layers into identity

### Contradiction Handling

When a conflict appears:

1. keep both claims
2. preserve exact provenance for both
3. add a contradiction note
4. add a short reconciliation attempt if the source basis permits
5. never silently overwrite older claims

Two contradiction classes matter:

- source disagreement
- orientation confusion

Orientation confusion is a domain-critical failure mode and must be treated explicitly.

### Lint

Linting should check for:

- orphan pages
- missing axis or triad links
- triad hubs missing orientation pages
- claims missing exact source pages
- contradictions missing notes
- bad aliases that imply false equivalence
- drift between frontmatter and links
- drift between actual pages and `wiki/index.md`

## Minimal Helper Tooling

V1 should stay lightweight. No database or server.

Recommended tools:

- `tools/normalize_identity.py`
  - normalize axis order
  - preserve activation orientation
  - generate canonical slugs
  - list orientation siblings for a triad-set
- `tools/rebuild_index.py`
  - rebuild `wiki/index.md` from frontmatter
- `tools/lint_wiki.py`
  - validate frontmatter by page type
  - validate linkage
  - catch duplicate or malformed identities

## Initial Implementation Slice

Do not scale the system before the identity model is proven.

First slice:

1. Create wiki folders, templates, and helper script stubs
2. Create one source page for Ebertin
3. Pilot only these pages:
   - `Sun/Moon`
   - `Sun/Moon = Venus`
   - `Sun/Venus = Moon`
   - `Moon/Venus = Sun`
   - triad hub for `Sun Moon Venus`
   - affected factor pages
4. Verify that:
   - the three orientations remain distinct
   - the triad hub links them cleanly
   - provenance is preserved at claim level
   - factor, axis, activation, and triad pages stay coherent
5. Only then ingest further material

## Acceptance Criteria

The design is working if:

- structural normalization does not collapse distinct doctrine
- every sourced claim is traceable to exact source pages
- activation pages remain orientation-specific
- triad hubs behave as structural hubs, not merged doctrine pages
- factor pages remain useful without replacing activation pages
- contradictions are explicit instead of silently flattened
- the wiki is editable by the LLM and browseable by a human without special infrastructure

## Not In Scope For V1

- full-book ingestion in one pass
- source-native chapter pages
- natal/transit/direction/progression modeling
- embeddings or vector infrastructure
- a database-backed ontology store
- aggressive automation before the pilot slice is validated
