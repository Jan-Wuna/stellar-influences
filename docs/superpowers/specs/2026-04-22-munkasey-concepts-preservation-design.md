# Munkasey Concepts Preservation Design

Date: 2026-04-22
Status: Approved in conversation, written for review before implementation

## Purpose

Define the cleanest way to preserve Michael Munkasey's page-3 `CONCEPTS` material from *Midpoints: Unleashing the Power of the Planets* without polluting the canonical axis pages or pretending that phrase-cloud material is equivalent to formal midpoint doctrine.

## Decision

Preserve Munkasey's page-3 `CONCEPTS` as one source-grounded companion page per axis under `wiki/derived/`, and link to that companion page from the corresponding canonical axis page.

This is an intentional separation of doctrine from lexical-image material.

- Canonical doctrine remains on factor, axis, and activation pages.
- Munkasey's page-3 phrase lists are preserved, but they do not enter the comparative schema directly.
- MWA example tables from page 4 are dropped entirely.

## Rejected Approaches

### 1. Inline `CONCEPTS` On Canonical Axis Pages

Rejected because it would blur the boundary between formal source doctrine and Munkasey's image-prompt phrase lists.

The axis pages already carry comparative source entries and a shared schema. Appending 80-100 additional phrase fragments to each touched axis page would bloat the page and make the source look more doctrinally structured than it is.

### 2. One Giant Munkasey Concepts Appendix

Rejected because it would preserve the material but make it hard to navigate, hard to compare, and awkward to discover from the canonical pages.

The concepts are pair-specific. They should stay one click away from the axis they belong to.

### 3. New Page Type Such As `source_artifact`

Rejected for the first pass because the current `derived` page type is already sufficient.

Adding a new page type would expand linting, templates, and tooling for little immediate gain. These concept pages are source-grounded companion artifacts, and `derived` can hold that role if the page body explicitly states the boundary.

### 4. Preserve The MWA Example Tables

Rejected because the user explicitly wants them dropped.

This includes:

- `STRONG`
- `WEAK`
- `EVENTS`
- per-activator example rows on page 4

## Munkasey Source Model

Each midpoint block in Munkasey spans four pages:

1. axis-level prose with thematic sections
2. activator meanings for third factors
3. `CONCEPTS` phrase list
4. `With Itself` activations plus MWA example tables

This design splits those four pages as follows:

- page 1 -> canonical axis page
- page 2 -> canonical activation pages
- page 3 -> per-axis companion concept page in `wiki/derived/`
- top of page 4 -> canonical duplicate-factor activation pages
- remainder of page 4 -> discarded

## Approved Preservation Shape

### Companion Concepts Pages

Create one page per axis in `wiki/derived/`.

Path pattern:

- `wiki/derived/munkasey-<axis-slug>-concepts.md`

Examples:

- `wiki/derived/munkasey-sun-moon-concepts.md`
- `wiki/derived/munkasey-venus-saturn-concepts.md`

Title pattern:

- `Michael Munkasey - <Axis> Concepts`

Slug pattern:

- `munkasey-<axis-slug>-concepts`

These pages are not comparative doctrine pages. They are source-grounded companion sheets for lexical and imagistic material.

### Frontmatter Contract

Use the existing `derived` page type:

```yaml
---
title: "Michael Munkasey - Sun/Moon Concepts"
page_type: derived
slug: munkasey-sun-moon-concepts
status: source_grounded
framework_scope: modern_astrology
source_pages:
  - michael-munkasey-midpoints-unleashing-the-power-of-the-planets
updated_at: 2026-04-22
---
```

Notes:

- `framework_scope` should follow the eventual Munkasey source-page scope.
- `source_pages` should point at the future Munkasey source page once that page exists.

### Body Contract

Each concepts page should use this body structure:

```md
## Purpose

Preserve Munkasey's page-3 concept phrases for `Sun/Moon` as source-native image material.

## Evidence Base

- [Sun/Moon](../axes/sun-moon.md)
- [Michael Munkasey - Midpoints: Unleashing the Power of the Planets](../sources/michael-munkasey-midpoints-unleashing-the-power-of-the-planets.md)
- Source concept page: `57`

## Source Concepts

- Arrogant Approval
- Emotional Pretension
- Flowery Imagination

## Notes On Use

- These phrases are preserved as source-native concept prompts, not as comparative doctrine.
- They are kept off the canonical axis page's comparative schema to avoid conflating image phrases with formal delineation.
```

Rules:

- Preserve the phrases as a flat list in source order.
- Do not rewrite them into schema buckets.
- Do not summarize them into a new doctrinal paragraph.
- Do not create contradiction logic around them.
- Do not add `Derived Synthesis` unless explicitly asked later.

## Canonical Axis Page Integration

Axis pages should not absorb the phrase lists themselves.

Instead, the Munkasey axis source block should gain a short companion link immediately after the formal source prose.

Recommended shape:

```md
#### Munkasey Concepts Companion

- [Michael Munkasey - Sun/Moon Concepts](../derived/munkasey-sun-moon-concepts.md)
```

This gives the concepts page strong discoverability without making the axis page unreadable.

## Activation Page Scope

Activation pages are unchanged by this design except for the already-approved Munkasey ingest boundary:

- page-2 activations belong on activation pages
- page-4 `With Itself` entries belong on duplicate-factor activation pages

The page-3 `CONCEPTS` material does not belong on activation pages.

## Source Page Scope

The future Munkasey source page should state explicitly that:

- the source contributes factor pages, axis prose, activation prose, and separate concept companion pages
- the page-3 `CONCEPTS` corpus is preserved in `wiki/derived/`
- the page-4 MWA example tables were intentionally omitted

This keeps the omission explicit rather than silent.

## Parser Design

Add Munkasey parsing support in a dedicated source module, likely:

- `tools/munkasey_source.py`

It should emit a pair-level structure rich enough to support all retained layers:

```python
@dataclass(frozen=True)
class MunkaseyAxisBlock:
    factor_a: str
    factor_b: str
    axis_page: int
    activations_page: int
    concepts_page: int
    with_itself_page: int
    basic_ideas: str
    personal_thesis: str
    personal_anti: str
    relationship_thesis: str
    relationship_anti: str
    body_mind: str
    politics_business_thesis: str
    politics_business_anti: str
    activations: dict[str, str]
    concepts: tuple[str, ...]
    with_itself: dict[str, str]
```

Parsing responsibilities for the concepts layer:

- detect the page-3 heading such as `SUN/MOON CONCEPTS`
- collect the phrase lines in order
- strip blank lines and page-number noise
- preserve exact printed page number for provenance

The parser should not attempt semantic clustering of the phrases.

## Rendering Design

Add an ingest script, likely:

- `tools/ingest_munkasey.py`

For the concepts layer specifically, it should:

1. parse each axis block
2. render one `wiki/derived/munkasey-<axis>-concepts.md` page per axis
3. insert or replace the companion link in the canonical axis page idempotently
4. avoid touching activation pages with any concepts material
5. avoid writing any MWA table data
6. rebuild `wiki/index.md`
7. append `wiki/log.md`

The ingest must be rerunnable without duplicating companion links or derived pages.

## Index And Discoverability

Because these pages live in `wiki/derived/`, they will naturally appear under the generated `## Derived Pages` section in `wiki/index.md`.

This is acceptable.

The primary discovery path, however, should be from the canonical axis page, not from the global derived index.

## Tests

Add focused parser tests:

- `tests/tools/test_munkasey_source.py`

Minimum parser checks:

- `Sun/Moon` concepts page extracts a non-empty ordered phrase list
- `Venus/Saturn` concepts page extracts the expected heading and phrase count
- page-number provenance for the concepts page is preserved

Add focused ingest tests:

- `tests/wiki/test_munkasey_concepts_ingest.py`

Minimum ingest checks:

- a concepts companion page is created for `Sun/Moon`
- `wiki/axes/sun-moon.md` contains exactly one concepts companion link
- the concepts phrases render as a flat ordered list
- no MWA example-table text is rendered to any wiki page
- rerunning the ingest is idempotent

## Risks

### 1. Derived-Page Semantics

`derived` currently means query-driven synthesis in some parts of the repo.

This design reuses `derived` as a source-grounded companion container. That is acceptable for now, but the page body must be explicit that these are preserved source artifacts rather than synthesized doctrine.

### 2. Axis-Page Link Drift

If the companion-link placement is not standardized, reruns could create duplicate or differently placed links.

The renderer should own one exact insertion point inside the Munkasey source block.

### 3. Phrase-Line Parsing

The `CONCEPTS` pages are visually simple, but extraction still needs to guard against:

- accidental heading capture
- line-wrap artifacts
- page footer contamination

The parser should stay conservative and fail loudly if a concepts page does not match the expected shape.

## Non-Goals

This design does not:

- preserve MWA example tables
- model the examples as evidence pages
- create a new page type
- promote `CONCEPTS` into comparative schema bullets
- derive activation doctrine from page-3 phrase material

## Implementation Sequence

1. Create `tools/munkasey_source.py`
2. Implement concepts-page parsing and provenance capture
3. Implement derived companion-page rendering
4. Implement canonical axis-page companion-link insertion
5. Ensure MWA example tables are ignored by the ingest
6. Add focused parser and ingest tests
7. Rebuild `wiki/index.md`
8. Run `tools/lint_wiki.py`
