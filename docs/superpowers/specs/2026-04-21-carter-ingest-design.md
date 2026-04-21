# Carter Ingest Design

Date: 2026-04-21
Status: Approved in conversation, written for review before implementation

## Purpose

Define the safest way to ingest Charles Carter's *The Astrological Aspects* into the current Stellar Influences wiki without introducing a new page namespace and without pretending Carter states midpoint activations.

## Decision

Collapse Carter into the existing `wiki/axes/` pages only.

This is an intentional semantic compromise. Carter's source is aspect-based rather than midpoint-based, but the user prefers to keep the existing page structure instead of extending the schema. To keep that compromise bounded:

- Carter content will live only in canonical axis pages.
- Carter content will not create or modify activation pages.
- Carter content will not create or modify triad hubs.
- Carter content will not drive factor-page doctrine in the first pass.

## Rejected Approaches

### 1. New Carter-Specific Aspect Schema

Rejected because the user explicitly prefers collapse into existing pages.

This would be the cleanest doctrinal model, but it would add new page types and expand the schema beyond the requested direction.

### 2. Reusing Activation Pages

Rejected because Carter does not state oriented formulas like `Sun/Moon = Venus`.

Putting Carter into activation pages would create false precision and would misrepresent the source.

### 3. Freeform Carter Blob Per Axis

Rejected because it would make the source hard to lint, compare, and query later.

The Carter entry needs stable substructure for:

- Harmonious Aspects
- The Conjunction
- Inharmonious Aspects
- example lists

## Carter Source Model

The source is built around unordered planetary pairs. Each pair chapter contains:

1. pair-level introductory framing
2. `THE HARMONIOUS ASPECTS`
3. `THE CONJUNCTION`
4. `THE INHARMONIOUS ASPECTS`
5. `EXAMPLES FOR <PAIR>`
   with family-grouped example lists

This means Carter maps cleanly to unordered pair identity, which is why axis pages are the least-wrong collapse target.

## Approved Ingest Shape

Each affected axis page will gain a Carter source entry under `## Source Entries`.

Recommended body shape:

```md
### Charles Carter - The Astrological Aspects

- Source heading: `Aspects of the Sun and Moon`
- Source starting page: `5`

#### Harmonious Aspects

...

#### The Conjunction

...

#### Inharmonious Aspects

...

#### Examples

- Harmonious: ...
- The Conjunction: ...
- Inharmonious: ...
```

This preserves Carter's actual doctrinal units without pretending they are separate canonical pages.

## Comparative Positioning Inside Axis Pages

Axis pages already contain midpoint-derived material from Witte, Ebertin, and Falis.

Carter should be appended as another source entry, but the comparative summary must acknowledge the doctrinal mismatch explicitly.

Required note in Carter-touched axis pages:

- Carter's source entry is aspect-based and is intentionally collapsed into the canonical pair page for practical repo reasons.
- Carter's three aspect families must remain visibly separate inside the source entry.
- Carter material must not be flattened into midpoint wording in the `Comparative Schema`.

## Source Page Design

Create one minimal source page:

- `wiki/sources/charles-carter-the-astrological-aspects.md`

It should state:

- bibliographic metadata
- that the source covers 36 unordered planetary pairs
- that each pair is divided into three aspect families
- that this ingest is intentionally collapsed into canonical axis pages
- that the source does not produce activation pages

## Parser Design

Add a Carter parser module, likely:

- `tools/carter_source.py`

It should emit a pair-level model such as:

```python
@dataclass(frozen=True)
class CarterAxisBlock:
    factor_a: str
    factor_b: str
    page: int
    heading: str
    harmonious_text: str
    conjunction_text: str
    inharmonious_text: str
    harmonious_examples: list[str]
    conjunction_examples: list[str]
    inharmonious_examples: list[str]
```

Parsing responsibilities:

- detect the 36 pair headings from the table of contents and body
- normalize `&` and `AND` forms into canonical factor names
- extract the three family sections
- extract example lines by family
- preserve exact printed page numbers

## Rendering Design

Add a Carter ingest script, likely:

- `tools/ingest_carter.py`

It should:

1. parse Carter pair blocks
2. open existing axis pages
3. preserve current source entries
4. append or replace the Carter source entry idempotently
5. add Carter to `source_pages`
6. set `framework_scope: comparative` on touched axis pages if not already comparative
7. write the Carter source page
8. rebuild `wiki/index.md`
9. append `wiki/log.md`

The ingest must be rerunnable without duplicating Carter entries.

## Page Scope Rules

### Axis Pages

Touched by Carter ingest.

### Activation Pages

Untouched by Carter ingest.

### Triad Hubs

Untouched by Carter ingest.

### Factor Pages

Untouched in the first Carter pass.

Reason:

- Carter offers pair doctrine, not standalone factor chapters.
- Pulling aspect-pair doctrine into factors is a second-order design question and should not be mixed into the initial ingest.

## Comparative Schema Handling

Do not try to algorithmically merge Carter's family texts into the existing comparative bullets.

For the first Carter pass, the `## Comparative Schema` section on touched axis pages should stay conservative:

- note that midpoint and aspect doctrines are both present on the page
- note that Carter's entry is aspect-family structured
- avoid synthesized claims that erase the difference

## Pilot Strategy

Do not ingest all 36 pairs first.

Pilot only:

- `Sun/Moon`

The pilot should prove:

- Carter text can be parsed cleanly
- exact page references are preserved
- family boundaries survive rendering
- rerunning the ingest is idempotent
- existing Witte/Falis/Ebertin content is not damaged

Only after the pilot passes should the remaining 35 Carter pair chapters be ingested.

## Tests

Add focused parser tests:

- `tests/tools/test_carter_source.py`

Minimum parser checks:

- `Sun/Moon` extracts all three family bodies
- `Moon/Mercury` extracts family-grouped examples
- pair normalization handles both `AND` and `&`

Add focused wiki ingest tests:

- `tests/wiki/test_carter_axis_ingest.py`

Minimum ingest checks:

- Carter source page exists
- `wiki/axes/sun-moon.md` includes Carter entry and all three family headings
- Carter does not add `source_pages` to any activation page
- rerender leaves exactly one Carter source entry per touched axis page

## Risks

### 1. Doctrinal Mixing

Axis pages will now combine midpoint-pair doctrine and aspect-pair doctrine.

This is accepted by user preference, but must be made explicit in the page wording.

### 2. Section Parsing Drift

Carter is OCR-cleaner than Falis, but parser logic still needs to respect:

- long running prose
- section headers
- example blocks
- printed page numbering

### 3. Overreach Into Factor Pages

This should be explicitly avoided in the first pass.

## Success Criteria

The Carter ingest design is successful if:

- Carter is represented only on axis pages and the Carter source page
- the three aspect families remain visibly distinct
- no activation pages are changed by Carter ingest
- no new page types are introduced
- source page references remain exact
- rerunning the ingest is idempotent
- `pytest`, `tools/lint_wiki.py`, and `tools/rebuild_index.py` pass

## Next Step

After review of this spec, write an implementation plan for:

1. Carter parser pilot on `Sun/Moon`
2. Carter axis-page merge logic
3. pilot verification
4. expansion from pilot to full 36-pair ingest
