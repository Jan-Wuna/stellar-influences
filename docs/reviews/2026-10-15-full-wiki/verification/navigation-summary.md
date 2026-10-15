# Root navigation and template review

Reviewer: `/root/navigation_templates` (index full-read leaf: `/root/navigation_templates/index_reader`). Review date: 2026-10-15.

All four live root Markdown pages and all six templates were read completely. The four live pages remain unchanged at this handoff because the two generated pages await final root integration and the two historical files are protected records. All six templates changed. Two generators and one focused regression test also changed.

## Coverage and ledger state

| Surface | Full reads | Changed live files now | Unchanged live files now | Ledger |
| --- | ---: | ---: | ---: | --- |
| Root wiki pages | 4 | 0 | 4 | `ledgers/wiki-index.jsonl`, `ledgers/wiki-navigation.jsonl` |
| Templates, separate from live corpus | 6 | 6 | 0 | `ledgers/templates.jsonl` |

The index reader reviewed all 7,502 baseline lines and every displayed link, then confirmed that the live file matched the immutable baseline hash. The log was read in untruncated chunks 1-50, 51-100, 101-150, and 151-193. The query guide and dated lint report were each read in full. The six templates were each read before and after editing. All ten JSONL records parse and have `full_read: true`; each records a page-specific outcome and reason.

The index-only link check found 7,488 valid local links, no duplicate targets, and no label/path mismatches against the manifest. Its 7,487 canonical page listings remain unchanged in the read-only regenerated preview. This is an index check, not a claim that this reviewer read the linked pages.

## Prepared navigation changes

`tools/rebuild_index.py` now produces compact routes for exact formulas, shared pairs, recurring factors, orientation siblings, evidence/limits, and the mixed derived-note collection. Existing section headings and sorted canonical entries are retained. Triad, source, and derived sections receive short role explanations so a reader following a fragment link sees the scope. The manifest path becomes a clickable link.

`tools/query_manifest.py` now produces direct index routes, clickable synthesis/research titles using the existing relative-link helper, a passage-level evidence route, coverage qualifications, and an explanation of manifest roles and scores. Retrieval order remains activation, axis, factor, structural sibling lookup, explanatory synthesis, then supplemental evidence for a specific gap. Source counts and retrieval scores are not described as proof of independent corroboration or evidence quality.

An explicitly true `structural_only` frontmatter value is honored before ordinary canonical classification. The factor owner added it to the documented Chiron exception. The new focused test proves that the opt-in factor becomes `structural_only`, `answer_surface: false`, while an ordinary factor remains `canonical_answer`, `answer_surface: true`. No canonical factor names or activation orientations were changed. The read-only real-corpus preview reported 5,760 canonical answers and 1,619 structural pages, including Chiron.

## Template changes

All six templates retain their original frontmatter fields and section headings. The factor, axis, and activation templates retain a single `Derived Synthesis`, now with the anchor immediately adjacent to the heading. Their Identity sections link to the interpretation and source entries. The six Comparative Schema categories are explicit, and synthesis guidance requests compact connected prose grounded in identifiable local source subentries.

The remaining guidance covers exact orientation, unordered pair identity, standalone factor evidence and structural exceptions, genuine rather than assumed contradictions, source-native categories, exact passage references, sparse coverage, historical health/gender attribution, and the difference between repeated text and independent support. Triad guidance remains structural and prompts checked source-by-orientation coverage and base-axis routes. Source guidance distinguishes admitted scope and actual passage locators from missing bibliographic pagination. Derived-note guidance makes the question, evidence, reasoning, conclusion, inference, and limits explicit. Instructions remain visible author guidance, not hidden HTML comments or additional summaries.

## Verification completed

- The new routing test was run before implementation and failed because Chiron still received `canonical_answer`; it passed after the explicit flag check was added.
- A focused run of the existing index/manifest tests and all Chiron policy tests produced **10 passed, 1 failed, 1 deselected**. The existing failure is the exact-prose assertion at `tests/wiki/test_chiron_policy_surface.py:21`: another owner's revised Chiron note no longer contains `The present issue is source asymmetry, not contradiction.` The note owner/root was informed; this reviewer did not edit that note or weaken its test.
- The live-writing `test_rebuild_index_script_runs_from_repo_root` was deliberately deselected until root integration. The query-manifest CLI test writes only to its temporary fixture and passed.
- An in-memory real-corpus generator preview was exercised. Its entire generated guide and index introduction were inspected. Later small link/section-note adjustments were inspected in the actual diff; the final generated live delta remains an integration check.
- Automated baseline comparisons passed for all six templates' frontmatter and section-heading names; all three required anchor adjacencies and explicit six-category checks passed.
- SHA256 comparisons confirmed the historical `wiki/log.md` and `wiki/lint-report-2026-04-21.md` remain byte-identical to baseline.
- `git diff --check` passed for the owned generator, test, and template paths. All checks used `PYTHONDONTWRITEBYTECODE=1`, and pytest used `-p no:cacheprovider`.
- The programming audit reported only two pre-existing bare-`dict` return annotations in `query_manifest.py` (`_page_record` and `build_query_manifest`). Their signatures were not changed. The surgical assignment does not include an API/type migration. No new boundary, escape hatch, defensive layer, one-off helper, oversized module, parameter group, or logging path was introduced. Both generators retain their existing responsibility; the new regression checks observable retrieval roles rather than prompt prose.

## Final integration commands and remaining work

Run from the repository root after the parallel wiki edits settle:

```powershell
$env:PYTHONDONTWRITEBYTECODE='1'
& 'C:/pyMADMAX2/miniconda3/envs/deep11/python.exe' tools/rebuild_index.py
& 'C:/pyMADMAX2/miniconda3/envs/deep11/python.exe' tools/query_manifest.py
& 'C:/pyMADMAX2/miniconda3/envs/deep11/python.exe' tools/lint_wiki.py
```

Then review the generated `wiki/index.md`, `wiki/query-guide.md`, and `wiki/query-manifest.json` deltas, including all new fragment links, note links, source/triad/derived role explanations, Chiron's structural classification, and preserved canonical listings. Exercise the formula/pair/factor/sibling/evidence reader journeys in the final rendered surface. Run the previously deselected index CLI test once live regeneration is permitted. Update the index and guide ledger outcomes to `changed` only after those live files actually change, and record final delta/link verification. Historical log and lint report entries stay unchanged.

Outstanding at this handoff: final regeneration/delta review for two generated root pages; root coordination of the unrelated exact-prose Chiron note test; two existing generator type-annotation audit findings. No unresolved source or doctrine problem was introduced by this assignment, and no whole-corpus final structural or visual-QA result is claimed here.

## Changed paths owned by this assignment

- `tools/rebuild_index.py`
- `tools/query_manifest.py`
- `tests/wiki/test_chiron_policy_surface.py`
- `wiki/_templates/activation.md`
- `wiki/_templates/axis.md`
- `wiki/_templates/factor.md`
- `wiki/_templates/triad_hub.md`
- `wiki/_templates/source.md`
- `wiki/_templates/derived.md`
- `docs/reviews/2026-10-15-full-wiki/ledgers/wiki-index.jsonl`
- `docs/reviews/2026-10-15-full-wiki/ledgers/wiki-navigation.jsonl`
- `docs/reviews/2026-10-15-full-wiki/ledgers/templates.jsonl`
- `docs/reviews/2026-10-15-full-wiki/verification/navigation-summary.md`

The Chiron page metadata belongs to the factor reviewer, not this path list. No root wiki Markdown file or raw vault source was edited manually by this assignment.
