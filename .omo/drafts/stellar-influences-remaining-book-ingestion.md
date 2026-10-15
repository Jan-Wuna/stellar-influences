---
slug: stellar-influences-remaining-book-ingestion
status: execution-approved
intent: unclear
pending-action: execute .omo/plans/stellar-influences-remaining-book-ingestion.md
approach: Finish the Stellar Influences portion only: one remaining source per batch, source page first, canonical factor/axis/activation/triad pages second, lint after each accepted source, and explicit hold evidence for sources that cannot be mapped without schema or parser expansion.
---

# Draft: stellar-influences-remaining-book-ingestion

## Components (topology ledger)
| id | outcome (one line) | status | evidence path |
| --- | --- | --- | --- |
| C1 | Reconcile the 14 both_split/stellar_influences_first rows against live wiki/sources after commit ccfbfb72. | active | .omo/evidence/si-source-reconciliation.md |
| C2 | Ingest low-risk standalone factor/axis sources that have direct prose entries and no parser expansion. | active | .omo/evidence/si-low-risk-ingests.md |
| C3 | Decide and execute the explicit but abbreviation-driven Niggemann planetary-picture import without merging activation orientations. | active | .omo/evidence/si-niggemann-ingest.md |
| C4 | Decide and execute or hold reverse-lexicon sources Feist, Master-Lexicon, and Baker based on whether formula-keyword rows can be mapped without dumping full text. | active | .omo/evidence/si-reverse-lexicons.md |
| C5 | Rebuild query surfaces, lint, inspect representative factor/axis/activation/triad pages, and commit each verified batch. | active | .omo/evidence/si-final-verification.md |

## Open assumptions (announced defaults)
| assumption | adopted default | rationale | reversible? |
| --- | --- | --- | --- |
| Scope | Stellar Influences only; do not modify Stellar Craft. | User correction explicitly says continue the SI ingestion work. | Yes |
| Source ordering | Process one source at a time, with low-risk direct prose sources before parser-heavy sources. | AGENTS.md requires one-source ingest and source page first. | Yes |
| Existing coverage | Treat Witte/Rudolph/Lefeldt, Ebertin, McBroom, Munkasey, Banzhaf/Haebler, and Johndro as already ingested unless a later evidence pass finds a concrete missing entry. | Live source pages exist after commit ccfbfb72. | Yes |
| Reverse lexicons | Do not bulk-add every keyword row until a parser proves formula orientation, canonical factor mapping, duplicate handling, and compact page insertion. | Prevents full-text dump and orientation errors. | Yes |
| Schema holds | If a source primarily depends on signs, houses, degrees, timing, IC/DSC-only angles, minor bodies outside canon, or narrative cases, record hold evidence instead of forcing wiki entries. | Current SI page types are factor, axis, activation, triad_hub, source, derived. | Yes |

## Findings (cited)
- AGENTS.md: SI V1 scope allows explicit factor meanings, unordered axes, oriented activations, and triad hubs only; no signs/houses/degrees/timing layers.
- wiki/sources: live source inventory includes Witte/Rudolph/Lefeldt, Ebertin, McBroom, Munkasey, Carter, Falis, Hand, Sandbach, Udo Rudolph, Banzhaf/Haebler, and Johndro.
- W:/Stellar Craft/.omo/drafts/astro-book-phase2-analysis.csv: 14 rows have best_fit_destination of both_split or stellar_influences_first.
- Local PDF probes: Hall has factor-level planetary keyword tables on PDF pages 104-121; Harding/Harvey has a direct Sun/Moon midpoint chapter beginning on PDF page 61; Stein has direct Sun/Moon and ASC/MC midpoint descriptions beginning on PDF page 2; Niggemann has explicit planetary-picture table entries beginning around PDF page 26; Feist/Master-Lexicon/Baker expose reverse keyword-to-formula rows rather than formula-heading prose.

## Decisions (with rationale)
- Continue from committed baseline ccfbfb72 Ingest Banzhaf and Johndro source material.
- Implement low-risk direct prose sources first: Manly P. Hall, Harding/Harvey, then Zane B. Stein.
- Treat Aren Ober as a prove-or-hold source because sampled text is largely method, timing, and case narrative.
- Treat Hans Niggemann as an implementation source only after a worker builds an abbreviation map and sample parser evidence.
- Treat Feist, Uranian Master-Lexicon, and Baker as reverse-lexicon parser sources; do not hand-enter them.

## Scope IN
- W:/Stellar Influences/wiki/sources
- W:/Stellar Influences/wiki/factors
- W:/Stellar Influences/wiki/axes
- W:/Stellar Influences/wiki/activations
- W:/Stellar Influences/wiki/triads
- W:/Stellar Influences/wiki/index.md
- W:/Stellar Influences/wiki/query-guide.md
- W:/Stellar Influences/wiki/query-manifest.json
- .omo plan/evidence state for this start-work run.

## Scope OUT (Must NOT have)
- No Stellar Craft edits.
- No raw source collection edits.
- No new page types.
- No sign, house, degree, transit, progression, direction, timing, or broad method imports.
- No minor-body canon expansion.
- No merging activation orientations.
- No bulk full-text dumps from reverse lexicons.

## Open questions
- None for the next batch. Parser-heavy reverse lexicons may produce source-specific schema holds if they cannot be mapped safely.

## Approval gate
status: approved-by-start-work-bootstrap
