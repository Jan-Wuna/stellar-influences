# Shared editorial standard

Read `AGENTS.md`, `wiki/query-guide.md`, the manifest records for your assigned paths, and the applicable template before editing. Read each page completely, including frontmatter, source entries, all links, and all notes. Retrieve in bounded chunks with no truncated output. A script reading a file is not a substantive editorial review.

## Ownership and evidence

- Edit only your explicitly assigned wiki pages and your own ledger/report shard. You are not alone in the codebase. Preserve other changes; never reset, clean, stage, commit, or overwrite another reviewer's files.
- Use `apply_patch` for manual edits. Use `C:/pyMADMAX2/miniconda3/envs/deep11/python.exe` for every Python command. Prefer the Git Bash MCP for shell commands.
- Keep `Stellar Influences Vault/` unchanged. Begin with canonical evidence. Inspect companions, source catalogs, and raw passages only for a specific gap. Never repair a damaged source passage from astrological background knowledge.
- Preserve source entries verbatim unless a substantive repair has been checked against the actual source. Preserve exact references, source-native categories, quotes, minority claims, qualifications, and provenance. Record suspected OCR/translation problems explicitly and exclude damaged wording from confident synthesis.
- New synthesis must cite identifiable local source subentries, preferably Markdown links to their heading fragments. Supply the exact source reference when already known. Do not invent printed or PDF page numbers. A source passage locator and a missing bibliographic page number are distinct matters; record the latter as unresolved when genuinely absent.
- Repeated wording is not proof of independent corroboration. Historical medical/gender statements must remain attributed, never turned into diagnoses or universal facts.

## Canonical reading experience

- Keep existing section names and stable links. Use the existing `Derived Synthesis` as the single main explanation. Add a brief link to it in Identity before the long source entries (for example, `[Read the interpretation](#derived-synthesis)`), plus a source-entry link if useful. Do not create competing summaries.
- On factor, axis, and activation pages, put `<a id="derived-synthesis"></a>` immediately before `## Derived Synthesis`, with no blank line between them.
- Write connected, specific prose; explain what unifies the themes and what remains limited. Prefer one or two compact paragraphs over another keyword list. Keep useful uncommon meanings when sourced. Explain specialist terms locally when needed, using only a definition justified by the wiki or the formula's structure.
- Keep the six Comparative Schema categories: core meaning; psychology; body/health; social/relationship; events/manifestations; conflicts/notes. Replace storage-related filler with short evidence-grounded meaning. Distinguish an unrepresented category from a source asserting absence. For a sparse entry, say exactly what the entry does and does not establish; do not populate it from general doctrine.
- Remove empty editorial placeholders where permitted. Replace `None recorded yet` with an accurate, bounded assessment of the entries on the page. No unrecorded contradiction is proof of agreement. Differences of emphasis, conditional expressions, and different orientations are not contradictions.
- Source headings and local heading links provide traceability without repeating long bibliographies throughout the main prose. Do not remove supporting passages to make a page shorter.

## Page types

- Factor: explain the organizing themes and range supported by its own standalone evidence. Chiron is a documented structural exception; do not manufacture standalone doctrine.
- Axis: explain the shared pair theme. An unordered pair remains one identity. Keep activation-specific manifestations on their own pages.
- Activation: interpret the exact oriented formula. Make clear that the factor after `=` specifies the pair before it, within the actual entry's evidence. Do not infer an activation's meaning merely by combining generic factor meanings. Never borrow a sibling's wording or treat the three orientations as interchangeable.
- Triad hub: keep it structural. Improve the orientation map and coverage by checking the linked activation pages. Identify real source names, not `Michael` or `Udo`. Do not add a merged interpretation. Coverage lists must not imply completeness when they describe one source only. Add useful base-axis navigation if justified.
- Source catalog: clarify bibliography, source location, admitted scope, coverage, and limitations. Do not ingest additional source material.
- Derived note: make the question, evidence, reasoning, conclusion, and limits clear. Keep editorial inference distinct from sourced statements.
- Companion/research note: retain its existing role, quotation integrity, and research provenance; improve routes to the canonical answer pages.
- Navigation: help the reader choose formula, pair, factor, or structural lookup. Generated files are changed through their generators, not edited manually. Historical logs/reports may remain unchanged with a recorded reason.
- Templates: preserve required fields and section names. Make the standard explicit without putting template instructions into live prose.

## Ledger contract

Write JSONL at `docs/reviews/2026-10-15-full-wiki/ledgers/<your-assignment>.jsonl`, one complete object per page, using apply_patch. Required fields:

`path`, `reviewer`, `full_read` (true only after complete reading), `status` (`reviewed`), `outcome` (`changed` or `unchanged`), `problems` (array), `changes` (array), `verification` (array of actual checks), `unresolved` (array), `evidence` (array of local passages/sections used).

Each record must be page-specific. For unchanged pages, record the substantive reason in `changes` or `verification`. Record actual checks only; root will run whole-corpus structural checks later. Do not claim whole-corpus checks yourself. Record source problems specifically enough to locate them, including exact suspicious wording when helpful. Never mark a page reviewed after reading only a sample or a machine inventory.

After each batch, inspect your actual diff and revised prose against the source entries. Check orientation, references, and the immediately adjacent synthesis anchor. Report your count and unresolved problems to your supervisor. Do not spawn more agents unless your assignment explicitly authorizes delegation; leaf reviewers work inline.
