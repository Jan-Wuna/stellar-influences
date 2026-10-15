# Full-wiki review results

The editorial review and targeted source repairs are complete. Every live page and template has a substantive full-read outcome. The independent source gate passes all **5,331 source-section changes, 856 original flagged targets, and fifteen source catalogs**, with zero material repair holds. Genuine source limitations and the existing test-compatibility limits remain explicit below.

## Coverage

All 7,491 live Markdown pages and six templates have unique substantive full-read review records. The live inventory comprises 5,472 activations, 266 axes, 23 factors, 1,618 triad hubs, 93 derived pages including companions and research notes, 15 source catalogs, and four navigation/history pages. The generated manifest intentionally excludes the query guide; the review includes it.

Of the live pages, 7,489 changed and two remained unchanged: `wiki/log.md` preserves its historical entries, and `wiki/lint-report-2026-04-21.md` preserves a dated historical report. All six templates changed. There are zero unreviewed pages or templates. Existing records explain each outcome. Source-repair callbacks amend those records rather than creating additional reviews.

The final [consolidated ledger](page-review-ledger.jsonl) includes every record and its owning shard/line. [Counts](counts.json) record the generation time. **1,254 live pages retain a nonempty recorded source, coverage or interpretive limitation**; [the complete export](unresolved-pages.json) gives each exact path, note and evidence pointer. These are not silently treated as resolved source claims.

The initial working tree and HEAD are recorded in `baseline.json`. Its 6,036 protected-file hashes and all 7,497 exact original Markdown copies passed whole-corpus preservation checks; the latest final result is recorded in `verification/review-validation.json`. Raw vault files, unrelated initial changes, and historical log entries remain protected. No commit or push is part of this review.

## Representative changes

| Page | Before | After |
| --- | --- | --- |
| [Sun, original](before/wiki/factors/sun.md) → [revised](../../../wiki/factors/sun.md#derived-synthesis) | Three short synthesis bullets accumulated themes and liabilities, including burnout and brittle pride without passage links. | Two connected paragraphs explain life force, identity, purpose, supportive and dominating expressions, and role-based qualifications, with direct evidence links. The less obvious body, daily-life, day and annual-cycle meanings remain visible. |
| [Sun/Moon, original](before/wiki/axes/sun-moon.md) → [revised](../../../wiki/axes/sun-moon.md#derived-synthesis) | General integration and relationship keywords. | Explains how conscious aims and felt needs find a common focus, why the relationship also appears through partners and shared work, and how tension and differing gender frameworks affect the reading. |
| [Sun/Moon = Venus, original](before/wiki/activations/sun-moon-equals-venus.md) → [revised](../../../wiki/activations/sun-moon-equals-venus.md#derived-synthesis) | Claimed the clearest harmony-oriented expression among siblings. | Explains the exact activating role of Venus, traces affection, appreciation and art to this orientation's entries, and avoids an unsupported ranking of siblings. |
| [Sun/Venus = Moon](../../../wiki/activations/sun-venus-equals-moon.md#derived-synthesis) and [Moon/Venus = Sun](../../../wiki/activations/moon-venus-equals-sun.md#derived-synthesis) | Generalized nourishment, identity and purpose could blur the orientations. | The former explains felt nourishment and uneven expression of affection; the latter explains active care, shared feelings and artistic expression from its own passages. Each retains its distinct base pair and activating factor. |

The Comparative Schema retains all six shared categories while replacing storage descriptions with evidence-grounded meaning or specific evidence limits. Source-native categories and quotations remain accessible in Source Entries. Triad hubs stay structural; source catalogs now distinguish actual bibliographic evidence, corpus coverage and missing publication information.

## Verification and its limits

Every command used `C:/pyMADMAX2/miniconda3/envs/deep11/python.exe`. Generated navigation was rebuilt with `tools/rebuild_index.py` and `tools/query_manifest.py`; `tools/lint_wiki.py` passed. The review's additional whole-corpus validators check coverage, original-file preservation, identities, metadata, formulas, six schema categories, immediate synthesis anchors, links and fragments, manifest reconciliation and linked-page relationships. Their final receipts belong in `verification/`.

With that interpreter and `PYTHONUTF8=1 PYTHONDONTWRITEBYTECODE=1`, the maintenance and corpus commands are:

```text
tools/rebuild_index.py
tools/query_manifest.py
tools/lint_wiki.py
docs/reviews/2026-10-15-full-wiki/verification/validate_review.py
docs/reviews/2026-10-15-full-wiki/verification/validate_links_identity.py
```

`verification/review-validation.json` records every coverage/preservation check and the exact source-delta approval gate. `verification/links-identity-validation.json` records the link/identity checks when generated by its validator. `verification/source-repair-review-closure-progress.json` is the separate individual-target source-flag gate; a passing ledger count does not replace it.

Focused McBroom, manifest and index tests passed 15 checks. The narrowed structural-policy/manifest checks passed nine, and the corrected Sandbach coverage test passed. The earlier broad existing suite returned 716 passed and 43 failed. Failure triage identified 14 pre-existing failures, 28 stale content/policy expectations and one real source-count regression. The real count regression and two relevant structural-policy expectations were corrected and verified. The remaining 26 stale prose expectations and 14 pre-existing failures are documented, not reported as a passing full suite; see `verification/full-test-failure-triage.md` and `verification/structural-policy-test-compatibility.md`.

Rendered inspection is sampled CommonMark desktop inspection, separate from whole-corpus structural checks and full-page editorial review. The current selection contains **24 inspected views of 18 pages**, all checked against their current Markdown hashes. It covers every page type, long and sparse pages, disagreements, German quotations, source companions and research notes. Actual reader journeys find a formula, follow activation → axis → factor, compare three orientations, follow synthesis → source entry, and recognize limited evidence. Saved captures and independent observations are in `verification/rendered/` and `verification/reader-journeys-working.md`. Native Obsidian and narrow-screen rendering were not inspected.

## Retained source limitations

The ledger's `unresolved` field records source limitations as well as editorial follow-ups. A nonempty field does not establish a remaining repair defect. Genuine printed errors, physical occlusion, undefined terms, missing bibliographic leaves, incomplete source coverage and conflicting statements remain attributed and visible. They must not be silently reconstructed.

Specific examples include the obscured qualifiers in [Jupiter/Kronos = Venus](../../../wiki/activations/jupiter-kronos-equals-venus.md) (ABC printed p. 338 / PDF p. 168), Witte's unfinished [Jupiter/Saturn = Moon](../../../wiki/activations/jupiter-saturn-equals-moon.md) sentence, the printed “Sudden might luck” in [Jupiter/Uranus = Vulcanus](../../../wiki/activations/jupiter-uranus-equals-vulcanus.md), “Longing to be loneliness” in [Moon/Admetos = Venus](../../../wiki/activations/moon-admetos-equals-venus.md), and Sandbach's printed “when not is following” in [Sun/Chiron = Moon](../../../wiki/activations/sun-chiron-equals-moon.md). The [page-level unresolved export](unresolved-pages.json) provides every affected path and exact recorded limitation.

The source gate separately tracks all 856 original flagged targets. Every target has an independently accepted, passage-specific resolution; old locator-only approvals were not treated as verification of inherited wording. There are zero unreviewed source targets and zero unresolved material repair holds. Historical medical and gender claims remain attributed source statements and are not strengthened into diagnoses or universal claims.
