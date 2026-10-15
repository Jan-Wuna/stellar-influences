# Full-test failure triage

Observed 2026-10-15T14:42:00.584983+00:00. Original receipt: **43 failed, 716 passed in193.16s**. This is a read-only diagnosis; no wiki, ledger or test edits were made.

Fourteen tests already fail against the initial wiki snapshot. Of the29 newly failing tests,24 pin ABC wording that has since been corrected or rephrased with raw support,3 pin superseded editorial sentences,1 expects a source-empty Chiron placeholder to remain a canonical answer, and1 exposes a real Sandbach catalog-count mismatch.

The valid coverage test must remain: Sandbach claims1092 attributed activation pages, while the evaluated live corpus has1088. The four removed attributions are Mercury/Asc=Node, Moon/Asc=Mercury, Moon/Asc=Node and Venus/Neptune=Moon. This was routed to the parent/source-catalog owner.

## Method and limits

- Evaluated all266 assertions/loop iterations for these43 tests against each snapshot using in-memory assertion instrumentation. No test file or cache was written. The original pytest receipt remains the full-run evidence.
- Baseline means current test assertions/current loaders evaluated against `before/wiki`; this does not claim a historical replay of old test or tool code.
- Inspected every failing function/helper, current and baseline content, exact failed assertion and review record. Read original ABC PDF text for all24 source-literal failures; personally viewed full source scans37,118,126,232 for Neptune/Pluto boundaries, and Hand109 for widest/Aries Point. Other visual checks are explicitly attributed to existing review records.
- Three hypotheses were tested: stale source pins, new contract violations, and initial-snapshot failures. All three occur. No failing assertion here demonstrates a changed formula identity or merged orientation.
- Protected test sources `tests/tools/test_export_static_wiki.py` and `tests/tools/test_local_query_core.py` still match their baseline SHA256 values. The JSON companion records hashes, all masked failures, source deltas and proof references.

## Fix boundaries

Keep the14 baseline failures outside current-delta implementation unless the parent explicitly authorizes separate maintenance. Two of those tests also contain newly failing masked assertions: Hand's Vernal Point test now correctly says widest and discloses the source-native Aries Point name, and Moon/Asc=Mercury now removes unsupported Sandbach attribution. These are justified deltas, not reasons to restore old source defects.

Jupiter/MC=Chiron is source-empty both before and after review. Its new `structural_only:true` flag correctly changes manifest routing; the seeded synthesis test must respect that exception. Neptune/Node=Chiron has the same source-empty character but lacks the flag, an inherited policy gap routed to the parent. The parent confirmed narrow structural metadata fixes for that page and Uranus/Asc=Chiron. A missing paragraph from one source does not make an otherwise source-bearing page structural.

Do not recover green tests by restoring Pluto clauses to Neptune entries, undoing raw glyph repairs, deleting legitimate labeled German quotations, or removing source/native identity protections. Test updates below are proposals only and require a parent-assigned implementation scope.

## Exhaustive matrix

| # | Test and assertion lines | Snapshot result | Classification | Evidence/consequence |
|---|---|---|---|---|
| 1 | [test_carter_axis_ingest.py:22](../../../../tests/wiki/test_carter_axis_ingest.py) `test_carter_source_page_exists` | pass → FAIL | stale_editorial_pin | Carter is still placed on canonical unordered axes and explicitly kept separate from midpoint/activation doctrine. The new scope note states the same routing more accurately; 'collapsed into' was removed. |
| 2 | [test_carter_axis_ingest.py:29](../../../../tests/wiki/test_carter_axis_ingest.py) `test_sun_moon_axis_includes_carter_family_headings` | FAIL → FAIL | pre_existing | The baseline already has 12 sources, whereas this test requires an exact 9-source list. The same list and Carter subentry survive; every other assertion passes. |
| 3 | [test_carter_axis_ingest.py:51](../../../../tests/wiki/test_carter_axis_ingest.py) `test_mercury_venus_axis_includes_carter_nonstandard_examples` | FAIL → FAIL | pre_existing | The baseline already includes Banzhaf/Haebler as a ninth source beyond the 8-source expected list. Metadata is unchanged and Carter's examples remain. |
| 4 | [test_chiron_policy_surface.py:11, 12, 13](../../../../tests/wiki/test_chiron_policy_surface.py) `test_chiron_factor_page_is_explicitly_source_bounded_and_non_doctrinal` | pass → FAIL | stale_editorial_pin | The exact three policy sentences were consolidated, but current Identity, schema and synthesis still explicitly restrict Chiron to Sandbach formula lookup with no standalone chapter or doctrine. structural_only:true improves machine routing. |
| 5 | [test_comparative_factors.py:26](../../../../tests/wiki/test_comparative_factors.py) `test_shared_factor_pages_reference_both_sources` | FAIL → FAIL | pre_existing | Eleven of thirteen factors already had additional admitted sources in the snapshot; exact 5-source equality failed then and now. Asc and MC satisfy the list. Required source names and framework notes pass for all thirteen. |
| 6 | [test_ebertin_full_ingest.py:50](../../../../tests/wiki/test_ebertin_full_ingest.py) `test_live_triad_page_includes_ebertin_source_coverage` | FAIL → FAIL | pre_existing | The baseline hub already omitted the pinned Ebertin page-81 string. Current hub links Ebertin's exact local entry on every orientation and retains source attribution; the test's coverage guarantee is met through links, without inventing a printed locator. |
| 7 | [test_ebertin_full_ingest.py:71](../../../../tests/wiki/test_ebertin_full_ingest.py) `test_ebertin_unresolved_review_page_exists` | pass → FAIL | stale_editorial_pin | The machine-readable queue still has unresolved_entries:[] and the derived note states that no activator-decoding block is recorded, while distinguishing OCR and completeness limits. Only the old unqualified sentence is absent. |
| 8 | [test_falis_axis_ingest.py:28](../../../../tests/wiki/test_falis_axis_ingest.py) `test_sun_moon_axis_includes_falis_entry` | FAIL → FAIL | pre_existing | The snapshot already has 12 sources rather than the pinned 9. The Falis section and Strong parental influence sentence still pass. |
| 9 | [test_hand_axis_ingest.py:33, 45](../../../../tests/wiki/test_hand_axis_ingest.py) `test_sun_moon_axis_includes_hand_entry` | FAIL → FAIL | pre_existing | Both the 9-source equality and exact title-case Source heading were already false in the baseline. Current Hand paragraph and title remain; source-heading metadata differs among independently labeled sources. |
| 10 | [test_hand_axis_ingest.py:55](../../../../tests/wiki/test_hand_axis_ingest.py) `test_vernal_point_sun_axis_becomes_comparative_with_hand_entry` | FAIL → FAIL | pre_existing | Only the exact '- Source heading: Sun/Aries' pin fails, in both snapshots. Comparative metadata, source list, Hand section and its public-contact passage pass. |
| 11 | [test_hand_axis_ingest.py:72](../../../../tests/wiki/test_hand_axis_ingest.py) `test_node_asc_axis_includes_hand_entry` | FAIL → FAIL | pre_existing | Only the exact Nodes/Ascendant heading pin fails in both snapshots; source attribution, framework, Hand title and personal-connections passage pass. |
| 12 | [test_hand_axis_ingest.py:86, 94](../../../../tests/wiki/test_hand_axis_ingest.py) `test_sun_factor_includes_hand_entry` | FAIL → FAIL | pre_existing | The snapshot already has Banzhaf/Haebler, Johndro and Hall beyond the pinned five sources, and lacks the exact The Sun source-heading line. Hand's chapter and energy-of-Being quotation survive. |
| 13 | [test_hand_axis_ingest.py:110](../../../../tests/wiki/test_hand_axis_ingest.py) `test_asc_factor_includes_hand_shared_entry` | FAIL → FAIL | pre_existing | The exact The Ascendant and Midheaven source-heading metadata line was absent before review and remains absent; Hand's shared factor paragraph and environment exchange survive. |
| 14 | [test_hand_axis_ingest.py:121, 122, 123](../../../../tests/wiki/test_hand_axis_ingest.py) `test_vernal_point_factor_becomes_comparative_with_hand_entry` | FAIL → FAIL | pre_existing_with_justified_source_delta | The missing heading pin already failed. Additional current failures are justified: Hand PDF109 prints widest, not oddest, and Aries Point is now disclosed as the source-native name while canonical title/slug/alias remain Vernal Point/VP. |
| 15 | [test_sandbach_ingest.py:46](../../../../tests/wiki/test_sandbach_ingest.py) `test_sun_moon_axis_includes_sandbach_entry` | FAIL → FAIL | pre_existing | The initial 12-source metadata fails the pinned 9-source list. Sandbach title, Principle, Process and both quoted meanings pass. |
| 16 | [test_sandbach_ingest.py:101, 102](../../../../tests/wiki/test_sandbach_ingest.py) `test_missing_sandbach_activation_creates_structural_placeholder_page` | FAIL → FAIL | pre_existing_policy_gap | Both exact omission sentences were absent before review. Current page documents a full actual PDF111–112 chapter check and still supplies no Chiron doctrine. It lacks structural_only:true, so the retrieval builder still treats the placeholder as a canonical answer; that inherited metadata gap is separate from this assertion failure. |
| 17 | [test_sandbach_ingest.py:109, 110, 111](../../../../tests/wiki/test_sandbach_ingest.py) `test_existing_witte_activation_can_absorb_sandbach_extraction_gap_note` | FAIL → FAIL | pre_existing_with_justified_source_delta | Both Sandbach section/omission prose pins already failed. New source-list failure follows removal of unsupported Sandbach attribution after full Moon/Ascendant PDF39–40 check; the page explicitly documents that no Mercury activation exists there. |
| 18 | [test_seeded_relationship_synthesis.py:4700, 4702](../../../../tests/wiki/test_seeded_relationship_synthesis.py) `test_seeded_jupiter_mc_additional_activation_cluster_has_real_derived_synthesis` | pass → FAIL | stale_structural_policy | Only Jupiter/MC=Chiron now fails canonical_answer/answer_surface=true. It is source-empty both before and after; structural_only:true correctly changes routing under query_manifest.py. Other nine formulas and the existing deferred-synthesis condition pass. |
| 19 | [test_source_page_coverage_claims.py:49](../../../../tests/wiki/test_source_page_coverage_claims.py) `test_source_page_coverage_claims_match_live_source_attribution` | pass → FAIL | actual_catalog_regression | Baseline passes every source claim. Current evaluation finds one mismatch: Sandbach claims1092 activation pages, live attribution1088. Four unsupported Sandbach attributions were removed during source review. The consistency assertion is valid. |
| 20 | [test_udo_rudolph_activation_repairs_batch_eight.py:54, 55](../../../../tests/wiki/test_udo_rudolph_activation_repairs_batch_eight.py) `test_asc_zeus_equals_vernal_point_uses_reviewed_abc_activation_translation` | pass → FAIL | stale_verified_source_pin | Umwelt/Umfeld refers to surroundings here; it does not require ecological environmental goals. Current text retains all seven clauses and limits Partner-Führung agency. |
| 21 | [test_udo_rudolph_activation_repairs_batch_five.py:55](../../../../tests/wiki/test_udo_rudolph_activation_repairs_batch_five.py) `test_saturn_mc_equals_neptune_uses_reviewed_abc_activation_translation` | pass → FAIL | stale_verified_source_pin | The required developmental-tasks phrase belongs to the following Pluto row. The current eight-clause Neptune translation restores future problems and excludes absorbed Pluto material. |
| 22 | [test_udo_rudolph_activation_repairs_batch_fourteen.py:38, 39](../../../../tests/wiki/test_udo_rudolph_activation_repairs_batch_fourteen.py) `test_moon_mars_equals_sun_uses_reviewed_abc_activation_translation` | pass → FAIL | stale_verified_source_pin | The man's efforts toward a woman and productive members of a people are faithful renderings; tests pin the older awkward English. All seven actual clauses remain. |
| 23 | [test_udo_rudolph_activation_repairs_batch_nine.py:54](../../../../tests/wiki/test_udo_rudolph_activation_repairs_batch_nine.py) `test_sun_mercury_equals_neptune_uses_reviewed_abc_activation_translation` | pass → FAIL | stale_verified_source_pin | The failing first phrase differs only by initial capitalization. Additional source-verified changes remove absorbed Pluto developmental clauses and translate Personen-Verkehr in der Luft as passenger traffic. |
| 24 | [test_udo_rudolph_activation_repairs_batch_nineteen.py:54](../../../../tests/wiki/test_udo_rudolph_activation_repairs_batch_nineteen.py) `test_node_vulcanus_equals_sun_uses_reviewed_abc_activation_translation` | pass → FAIL | stale_verified_source_pin | Failure is only Encounter versus encounter. The source-verified violent-person clause remains and must not be softened to powerful. |
| 25 | [test_udo_rudolph_activation_repairs_batch_nineteen.py:62, 63](../../../../tests/wiki/test_udo_rudolph_activation_repairs_batch_nineteen.py) `test_node_poseidon_equals_neptune_uses_reviewed_abc_activation_translation` | pass → FAIL | stale_verified_source_pin | Current mental-or-spiritual wording preserves geistig's range. The test's spiritual-development phrase is from the following Pluto row; current Neptune restores metaphysics and foreign cultures. |
| 26 | [test_udo_rudolph_activation_repairs_batch_sixteen.py:54, 55](../../../../tests/wiki/test_udo_rudolph_activation_repairs_batch_sixteen.py) `test_moon_kronos_equals_mars_uses_reviewed_abc_activation_translation` | pass → FAIL | stale_verified_source_pin | Current woman's-will syntax and priority treatment are faithful English alternatives. The source-native German is now explicit; eight source clauses remain. |
| 27 | [test_udo_rudolph_activation_repairs_batch_thirteen.py:62](../../../../tests/wiki/test_udo_rudolph_activation_repairs_batch_thirteen.py) `test_moon_mars_equals_mc_uses_reviewed_abc_activation_translation` | pass → FAIL | stale_verified_source_pin | Feelingful actions of the soul is a defensible rendering of the same phrase; all ten first-person clauses are retained. |
| 28 | [test_udo_rudolph_activation_repairs_batch_thirty_four.py:37](../../../../tests/wiki/test_udo_rudolph_activation_repairs_batch_thirty_four.py) `test_vulcanus_poseidon_equals_pluto_uses_reviewed_abc_activation_translation` | pass → FAIL | stale_verified_source_pin | Unfolding spiritual energies retains the old unfold-spiritual-energies meaning. Current text also restores the three complete initial Pluto clauses omitted in baseline. |
| 29 | [test_udo_rudolph_activation_repairs_batch_thirty_one.py:38](../../../../tests/wiki/test_udo_rudolph_activation_repairs_batch_thirty_one.py) `test_cupido_admetos_equals_jupiter_uses_reviewed_abc_activation_translation` | pass → FAIL | stale_verified_source_pin | Failure is only Blocked versus blocked. Current source repair restores a separate shared-law-consolidation clause omitted before. |
| 30 | [test_udo_rudolph_activation_repairs_batch_thirty_one.py:46](../../../../tests/wiki/test_udo_rudolph_activation_repairs_batch_thirty_one.py) `test_cupido_vulcanus_equals_mc_uses_reviewed_abc_activation_translation` | pass → FAIL | stale_verified_source_pin | Current translation distinguishes seelisch (soul/inner life) from separately printed psychisch (psychic), and repairs ich bin stark. Shared psychic influence is no longer the exact chosen English. |
| 31 | [test_udo_rudolph_activation_repairs_batch_thirty_one.py:54, 55](../../../../tests/wiki/test_udo_rudolph_activation_repairs_batch_thirty_one.py) `test_hades_admetos_equals_moon_uses_reviewed_abc_activation_translation` | pass → FAIL | stale_verified_source_pin | The first failure is capitalization; immersion versus deepening is an equally direct rendering of Vertiefung here. All seven clauses remain, with health claims attributed elsewhere on page. |
| 32 | [test_udo_rudolph_activation_repairs_batch_thirty_three.py:38](../../../../tests/wiki/test_udo_rudolph_activation_repairs_batch_thirty_three.py) `test_kronos_poseidon_equals_uranus_uses_reviewed_abc_activation_translation` | pass → FAIL | stale_verified_source_pin | Intellectual impulses is within geistig's mental/spiritual range and retains the same authority, cultural-reform and idea clauses. No orientation changed. |
| 33 | [test_udo_rudolph_activation_repairs_batch_thirty_three.py:46, 47](../../../../tests/wiki/test_udo_rudolph_activation_repairs_batch_thirty_three.py) `test_kronos_poseidon_equals_neptune_uses_reviewed_abc_activation_translation` | pass → FAIL | stale_verified_source_pin | Particularly versus especially and intellectual versus spiritual are faithful choices. More materially, current text ends at metaphysical truth and removes the next Pluto row's three developmental clauses. |
| 34 | [test_udo_rudolph_activation_repairs_batch_thirty_two.py:62](../../../../tests/wiki/test_udo_rudolph_activation_repairs_batch_thirty_two.py) `test_kronos_apollon_equals_vulcanus_uses_reviewed_abc_activation_translation` | pass → FAIL | stale_verified_source_pin | Special successes of power expresses the same German compound more naturally; important increase of power still passes. Full eight-clause row remains. |
| 35 | [test_udo_rudolph_activation_repairs_batch_three.py:46](../../../../tests/wiki/test_udo_rudolph_activation_repairs_batch_three.py) `test_vernal_point_neptune_equals_mc_uses_reviewed_abc_activation_translation` | pass → FAIL | stale_verified_source_pin | The failed phrase differs only by initial capitalization. Current unknown-public-sphere and inner-fine-sensitivity translations also match the German rather than implying spiritual doctrine. |
| 36 | [test_udo_rudolph_activation_repairs_batch_twelve.py:46, 47](../../../../tests/wiki/test_udo_rudolph_activation_repairs_batch_twelve.py) `test_sun_apollon_equals_vulcanus_uses_reviewed_abc_activation_translation` | pass → FAIL | stale_verified_source_pin | Current text distinguishes Gewalt force from Macht power. The second pin is changed possessive syntax (a person's growing power), not lost content. |
| 37 | [test_udo_rudolph_activation_repairs_batch_twelve.py:54, 55](../../../../tests/wiki/test_udo_rudolph_activation_repairs_batch_twelve.py) `test_sun_admetos_equals_mc_uses_reviewed_abc_activation_translation` | pass → FAIL | stale_verified_source_pin | The first failure is capitalization. Inner depth and inwardly blocked/established/oppressed render seelisch without imposing an occult meaning; all eight clauses remain. |
| 38 | [test_udo_rudolph_activation_repairs_batch_twenty_five.py:38, 39](../../../../tests/wiki/test_udo_rudolph_activation_repairs_batch_twenty_five.py) `test_jupiter_zeus_equals_asc_uses_reviewed_abc_activation_translation` | pass → FAIL | stale_verified_source_pin | Successful pursuit of goals at a place and a partner's accomplishments retain the same meanings in a grammatical translation; all eight clauses remain. |
| 39 | [test_udo_rudolph_activation_repairs_batch_twenty_one.py:46, 47](../../../../tests/wiki/test_udo_rudolph_activation_repairs_batch_twenty_one.py) `test_mercury_cupido_equals_neptune_uses_reviewed_abc_activation_translation` | pass → FAIL | stale_verified_source_pin | Foreign-language community differs only in hyphenation/capitalization. The test's evolutionary-conversations clause belongs to the following Pluto row; current Neptune retains its complete seven clauses. |
| 40 | [test_udo_rudolph_activation_repairs_batch_twenty_six.py:46](../../../../tests/wiki/test_udo_rudolph_activation_repairs_batch_twenty_six.py) `test_saturn_apollon_equals_uranus_uses_reviewed_abc_activation_translation` | pass → FAIL | stale_verified_source_pin | Only initial capitalization breaks the first assertion. Complete technical-science/reform/new-duty row is unchanged in meaning. |
| 41 | [test_udo_rudolph_activation_repairs_batch_twenty_three.py:63](../../../../tests/wiki/test_udo_rudolph_activation_repairs_batch_twenty_three.py) `test_mars_admetos_equals_pluto_uses_reviewed_abc_activation_translation` | pass → FAIL | stale_verified_source_pin | Growing depression impulses is the same compound meaning as growing impulses of depression. Current text also restores perseverance, blocked development and consolidation of will lost in baseline. |
| 42 | [test_udo_rudolph_priority_translation_repairs.py:39](../../../../tests/wiki/test_udo_rudolph_priority_translation_repairs.py) `test_neptune_factor_uses_reviewed_abc_keyword_translation` | pass → FAIL | stale_verified_source_pin | The English translation still contains the required unknown/lack-of-clarity/uncertainty phrase. Failure is the negative assertion banning a legitimate labeled German quotation, now added with the scan-confirmed missing tail. |
| 43 | [test_udo_rudolph_priority_translation_repairs.py:46](../../../../tests/wiki/test_udo_rudolph_priority_translation_repairs.py) `test_sun_mc_axis_uses_reviewed_abc_pair_summary` | pass → FAIL | stale_verified_source_pin | Ich is first-person I; current I during the day is more exact than the pinned self in the day. Other eleven-part source meanings remain. |

## Per-test assertion and fix record

### 1. tests/wiki/test_carter_axis_ingest.py::test_carter_source_page_exists

Current failed assertions:

- Line 22: `'collapsed into canonical axis pages' in page.body`

Proposed target: `tests/wiki/test_carter_axis_ingest.py`. Assert source type/scope, axis-only placement and preserved aspect families in the Scope Notes block; do not restore wording that suggests aspect doctrine was merged.

Scope: current_delta_candidate_only_after_parent_assignment.

### 2. tests/wiki/test_carter_axis_ingest.py::test_sun_moon_axis_includes_carter_family_headings

Current failed assertions:

- Line 29: `page.meta['source_pages'] == [WITTE_SLUG, UDO_RUDOLPH_SLUG, EBERTIN_SLUG, FALIS_SLUG, CARTER_SLUG, SANDBACH_SLUG, HAND_SLUG, MCBROOM_SLUG, MUNKASEY_SLUG]`

Proposed target: `tests/wiki/test_carter_axis_ingest.py`. Check required Carter attribution and entry families as a subset, and separately check source metadata against actual source sections.

Scope: pre_existing_failure_outside_current_delta; do not mass-update this test. Any newly introduced masked assertion is distinguished in interpretation..

Review record: `docs/reviews/2026-10-15-full-wiki/ledgers/axes-022.jsonl:1`.

### 3. tests/wiki/test_carter_axis_ingest.py::test_mercury_venus_axis_includes_carter_nonstandard_examples

Current failed assertions:

- Line 51: `page.meta['source_pages'] == [WITTE_SLUG, UDO_RUDOLPH_SLUG, EBERTIN_SLUG, FALIS_SLUG, CARTER_SLUG, SANDBACH_SLUG, HAND_SLUG, MUNKASEY_SLUG]`

Proposed target: `tests/wiki/test_carter_axis_ingest.py`. Replace obsolete exhaustive metadata equality with required attribution plus entry-specific Carter checks.

Scope: pre_existing_failure_outside_current_delta; do not mass-update this test. Any newly introduced masked assertion is distinguished in interpretation..

Review record: `docs/reviews/2026-10-15-full-wiki/ledgers/axes-012.jsonl:2`.

### 4. tests/wiki/test_chiron_policy_surface.py::test_chiron_factor_page_is_explicitly_source_bounded_and_non_doctrinal

Current failed assertions:

- Line 11: `"This page is source-bounded to Sandbach's modern midpoint corpus." in page.body`
- Line 12: `'Do not read it as a comparative factor doctrine page.' in page.body`
- Line 13: `'This factor page should not be used as standalone `Chiron` doctrine.' in page.body`

Proposed target: `tests/wiki/test_chiron_policy_surface.py`. Keep the non-doctrinal contract; verify explicit structural metadata, Sandbach-only source scope and the current standalone-evidence boundary instead of three sentences.

Scope: current_delta_candidate_only_after_parent_assignment.

Review record: `docs/reviews/2026-10-15-full-wiki/ledgers/factors-001.jsonl:4`.

### 5. tests/wiki/test_comparative_factors.py::test_shared_factor_pages_reference_both_sources

Current failed assertions:

- Line 26: `page.meta['source_pages'] == ['alfred-witte-ludwig-rudolph-hermann-lefeldt-rules-for-planetary-pictures', 'udo-rudolph-abc-fur-planetenbilder', 'reinhold-ebertin-the-combination-of-stellar-influences', 'robert-hand-horoscope-symbols', 'michael-munkasey-midpoints-unleashing-the-power-of-the-planets']`

Proposed target: `tests/wiki/test_comparative_factors.py`. Require the original five source slugs as a subset and independently reconcile all metadata slugs to source subentries.

Scope: pre_existing_failure_outside_current_delta; do not mass-update this test. Any newly introduced masked assertion is distinguished in interpretation..

Review record: `docs/reviews/2026-10-15-full-wiki/ledgers/factors-004.jsonl:2`.

### 6. tests/wiki/test_ebertin_full_ingest.py::test_live_triad_page_includes_ebertin_source_coverage

Current failed assertions:

- Line 50: `f'`Sun/Mercury = Venus`: {EBERTIN_TITLE}, page `81`' in triad.body`

Proposed target: `tests/wiki/test_ebertin_full_ingest.py`. Check Ebertin metadata plus formula-specific links to the three canonical #ebertin-entry surfaces; exact locators belong on those source-bearing pages.

Scope: pre_existing_failure_outside_current_delta; do not mass-update this test. Any newly introduced masked assertion is distinguished in interpretation..

Review record: `docs/reviews/2026-10-15-full-wiki/ledgers/triads-016.jsonl:63`.

### 7. tests/wiki/test_ebertin_full_ingest.py::test_ebertin_unresolved_review_page_exists

Current failed assertions:

- Line 71: `'No unresolved Ebertin activation entries are currently blocked.' in review.body`

Proposed target: `tests/wiki/test_ebertin_full_ingest.py`. Assert derived type, linked empty machine-readable queue and bounded decoding status; retain limitations on OCR/source completeness.

Scope: current_delta_candidate_only_after_parent_assignment.

Review record: `docs/reviews/2026-10-15-full-wiki/ledgers/derived-001.jsonl:4`.

### 8. tests/wiki/test_falis_axis_ingest.py::test_sun_moon_axis_includes_falis_entry

Current failed assertions:

- Line 28: `page.meta['source_pages'] == ['alfred-witte-ludwig-rudolph-hermann-lefeldt-rules-for-planetary-pictures', UDO_RUDOLPH_SLUG, EBERTIN_SLUG, FALIS_SLUG, CARTER_SLUG, SANDBACH_SLUG, HAND_SLUG, MCBROOM_SLUG, MUNKASEY_SLUG]`

Proposed target: `tests/wiki/test_falis_axis_ingest.py`. Require Falis membership and its local section; permit other admitted sources.

Scope: pre_existing_failure_outside_current_delta; do not mass-update this test. Any newly introduced masked assertion is distinguished in interpretation..

Review record: `docs/reviews/2026-10-15-full-wiki/ledgers/axes-022.jsonl:1`.

### 9. tests/wiki/test_hand_axis_ingest.py::test_sun_moon_axis_includes_hand_entry

Current failed assertions:

- Line 33: `page.meta['source_pages'] == [WITTE_SLUG, UDO_RUDOLPH_SLUG, EBERTIN_SLUG, FALIS_SLUG, CARTER_SLUG, SANDBACH_SLUG, HAND_SLUG, MCBROOM_SLUG, MUNKASEY_SLUG]`
- Line 45: `'- Source heading: `Sun/Moon`' in page.body`

Proposed target: `tests/wiki/test_hand_axis_ingest.py`. Check Hand attribution and its section directly. Verify a native heading only against actual Hand source evidence; do not demand another source's heading format.

Scope: pre_existing_failure_outside_current_delta; do not mass-update this test. Any newly introduced masked assertion is distinguished in interpretation..

Review record: `docs/reviews/2026-10-15-full-wiki/ledgers/axes-022.jsonl:1`.

### 10. tests/wiki/test_hand_axis_ingest.py::test_vernal_point_sun_axis_becomes_comparative_with_hand_entry

Current failed assertions:

- Line 55: `'- Source heading: `Sun/Aries`' in page.body`

Proposed target: `tests/wiki/test_hand_axis_ingest.py`. Keep comparative/source/meaning checks; locate the native heading with raw evidence before adding any heading-specific assertion.

Scope: pre_existing_failure_outside_current_delta; do not mass-update this test. Any newly introduced masked assertion is distinguished in interpretation..

Review record: `docs/reviews/2026-10-15-full-wiki/ledgers/axes-028.jsonl:10`.

### 11. tests/wiki/test_hand_axis_ingest.py::test_node_asc_axis_includes_hand_entry

Current failed assertions:

- Line 72: `'- Source heading: `Nodes/Ascendant`' in page.body`

Proposed target: `tests/wiki/test_hand_axis_ingest.py`. Test Hand section coverage without manufacturing a source heading.

Scope: pre_existing_failure_outside_current_delta; do not mass-update this test. Any newly introduced masked assertion is distinguished in interpretation..

Review record: `docs/reviews/2026-10-15-full-wiki/ledgers/axes-016.jsonl:9`.

### 12. tests/wiki/test_hand_axis_ingest.py::test_sun_factor_includes_hand_entry

Current failed assertions:

- Line 86: `page.meta['source_pages'] == [WITTE_SLUG, UDO_RUDOLPH_SLUG, EBERTIN_SLUG, HAND_SLUG, MUNKASEY_SLUG]`
- Line 94: `'- Source heading: `The Sun`' in page.body`

Proposed target: `tests/wiki/test_hand_axis_ingest.py`. Use required attribution membership and Hand-local evidence, retaining source-list consistency checks.

Scope: pre_existing_failure_outside_current_delta; do not mass-update this test. Any newly introduced masked assertion is distinguished in interpretation..

Review record: `docs/reviews/2026-10-15-full-wiki/ledgers/factors-006.jsonl:1`.

### 13. tests/wiki/test_hand_axis_ingest.py::test_asc_factor_includes_hand_shared_entry

Current failed assertions:

- Line 110: `'- Source heading: `The Ascendant and Midheaven`' in page.body`

Proposed target: `tests/wiki/test_hand_axis_ingest.py`. Keep the shared-section semantic and metadata contract; native heading assertions require verified heading evidence.

Scope: pre_existing_failure_outside_current_delta; do not mass-update this test. Any newly introduced masked assertion is distinguished in interpretation..

Review record: `docs/reviews/2026-10-15-full-wiki/ledgers/factors-001.jsonl:3`.

### 14. tests/wiki/test_hand_axis_ingest.py::test_vernal_point_factor_becomes_comparative_with_hand_entry

Current failed assertions:

- Line 121: `'- Source heading: `The Vernal Point`' in page.body`
- Line 122: `'most impersonal but also the oddest social contacts' in page.body`
- Line 123: `'Aries Point' not in page.body`

Proposed target: `tests/wiki/test_hand_axis_ingest.py`. Assert canonical identity separately from allowed source-native terminology. Replace oddest with the scan-confirmed widest social range, scoped to Hand's entry.

Scope: pre_existing_failure_outside_current_delta; do not mass-update this test. Any newly introduced masked assertion is distinguished in interpretation..

Review record: `docs/reviews/2026-10-15-full-wiki/ledgers/factors-006.jsonl:4`.

### 15. tests/wiki/test_sandbach_ingest.py::test_sun_moon_axis_includes_sandbach_entry

Current failed assertions:

- Line 46: `page.meta['source_pages'] == [WITTE_SLUG, UDO_RUDOLPH_SLUG, EBERTIN_SLUG, FALIS_SLUG, CARTER_SLUG, SANDBACH_SLUG, HAND_SLUG, MCBROOM_SLUG, MUNKASEY_SLUG]`

Proposed target: `tests/wiki/test_sandbach_ingest.py`. Require Sandbach source membership and both native categories, allowing other admitted sources.

Scope: pre_existing_failure_outside_current_delta; do not mass-update this test. Any newly introduced masked assertion is distinguished in interpretation..

Review record: `docs/reviews/2026-10-15-full-wiki/ledgers/axes-022.jsonl:1`.

### 16. tests/wiki/test_sandbach_ingest.py::test_missing_sandbach_activation_creates_structural_placeholder_page

Current failed assertions:

- Line 101: `"Sandbach's visible source page omits a text-bearing `Chiron` activator entry" in page.body`
- Line 102: `'this page is parked as Sandbach-only' in page.body`

Proposed target: `tests/wiki/test_sandbach_ingest.py`. Update the omission test to assert exact orientation and source-empty scope; route explicit structural metadata to the canonical owner, then assert structural_only/answer_surface=false.

Scope: pre_existing_failure_outside_current_delta; do not mass-update this test. Any newly introduced masked assertion is distinguished in interpretation..

Review record: `docs/reviews/2026-10-15-full-wiki/ledgers/activations-052.jsonl:51`.

### 17. tests/wiki/test_sandbach_ingest.py::test_existing_witte_activation_can_absorb_sandbach_extraction_gap_note

Current failed assertions:

- Line 109: `page.meta['source_pages'] == [WITTE_SLUG, UDO_RUDOLPH_SLUG, SANDBACH_SLUG, MUNKASEY_SLUG]`
- Line 110: `'### John Sandbach - Midpoints: A Kabbalistic Compendium of Meanings for Astrological Midpoints' in page.body`
- Line 111: `"Sandbach's visible source page omits a text-bearing entry for this activator" in page.body`

Proposed target: `tests/wiki/test_sandbach_ingest.py`. Test the three actual source entries and a bounded omission-provenance note. Reconcile catalog count rather than re-add Sandbach as a source-bearing claim.

Scope: pre_existing_failure_outside_current_delta; do not mass-update this test. Any newly introduced masked assertion is distinguished in interpretation..

Review record: `docs/reviews/2026-10-15-full-wiki/ledgers/activations-042.jsonl:4`.

### 18. tests/wiki/test_seeded_relationship_synthesis.py::test_seeded_jupiter_mc_additional_activation_cluster_has_real_derived_synthesis

Current failed assertions:

- Line 4700: `record['retrieval_role'] == 'canonical_answer'`
- Line 4702: `record['answer_surface'] is True`

Proposed target: `tests/wiki/test_seeded_relationship_synthesis.py`. Use the existing deferred/structural policy for source-empty Chiron records: require structural_only and answer_surface=false; retain canonical-answer/real-synthesis requirements on the nine source-bearing formulas.

Scope: current_delta_candidate_only_after_parent_assignment.

### 19. tests/wiki/test_source_page_coverage_claims.py::test_source_page_coverage_claims_match_live_source_attribution

Current failed assertions:

- Line 49: `claimed == live_counts[page_type]` — john-sandbach-midpoints-a-kabbalistic-compendium-of-meanings-for-astrological-midpoints claims 1092 activation pages, but live source attribution is 1088

Proposed target: `wiki/sources/john-sandbach-midpoints-a-kabbalistic-compendium-of-meanings-for-astrological-midpoints.md`. Source-catalog owner must reconcile the count to verified live attribution and clarify structural omission slots. Preserve this dynamic test unchanged.

Scope: current_delta_candidate_only_after_parent_assignment.

### 20. tests/wiki/test_udo_rudolph_activation_repairs_batch_eight.py::test_asc_zeus_equals_vernal_point_uses_reviewed_abc_activation_translation

Current failed assertions:

- Line 54: `'fire in the environment of public life' in page.body`
- Line 55: `'public environmental goals' in page.body`

Raw support: ABC printed 126, one-based PDF 62: Feuer im Umfeld des öffentlichen Lebens; öffentliche Umwelt-Ziele. Original PDF text read; existing review record supplies prior visual verification. Source terms normalize OCR spelling and are not a diplomatic transcription.

Proposed target: `tests/wiki/test_udo_rudolph_activation_repairs_batch_eight.py`. Retain public fire/surroundings and public-goal clauses with case-insensitive bounded checks; preserve rejection of old mixed OCR.

Scope: current_delta_candidate_only_after_parent_assignment.

Review record: `docs/reviews/2026-10-15-full-wiki/ledgers/activations-007.jsonl:17`.

### 21. tests/wiki/test_udo_rudolph_activation_repairs_batch_five.py::test_saturn_mc_equals_neptune_uses_reviewed_abc_activation_translation

Current failed assertions:

- Line 55: `'my developmental tasks' in page.body`

Raw support: ABC printed 77, one-based PDF 37: Neptune: meine zukünftigen Probleme. Pluto begins: Entfaltung der Seele als Aufgabe, meine Entwicklungs-Aufgaben. Original PDF text read plus existing full facsimile personally viewed for glyph boundary; no new scan files written

Proposed target: `tests/wiki/test_udo_rudolph_activation_repairs_batch_five.py`. Pin the Neptune terminal future-problems clause and absence of developmental tasks within #abc-entry; retain old-soul wording and mixed-OCR exclusion.

Scope: current_delta_candidate_only_after_parent_assignment.

Review record: `docs/reviews/2026-10-15-full-wiki/ledgers/activations-066.jsonl:44`.

### 22. tests/wiki/test_udo_rudolph_activation_repairs_batch_fourteen.py::test_moon_mars_equals_sun_uses_reviewed_abc_activation_translation

Current failed assertions:

- Line 38: `'efforts of the man for the woman' in page.body`
- Line 39: `'creative people of a people' in page.body`

Raw support: ABC printed 180, one-based PDF 89: Bemühungen des Mannes um die Frau; schaffende Menschen eines Volkes. Original PDF text read; existing review record supplies prior visual verification. Source terms normalize OCR spelling and are not a diplomatic transcription.

Proposed target: `tests/wiki/test_udo_rudolph_activation_repairs_batch_fourteen.py`. Check man's efforts toward a woman and productive members, scoped to this Sun row, retaining the corrupt-OCR exclusion.

Scope: current_delta_candidate_only_after_parent_assignment.

Review record: `docs/reviews/2026-10-15-full-wiki/ledgers/activations-044.jsonl:17`.

### 23. tests/wiki/test_udo_rudolph_activation_repairs_batch_nine.py::test_sun_mercury_equals_neptune_uses_reviewed_abc_activation_translation

Current failed assertions:

- Line 54: `'reports about subtle bodies' in page.body`

Raw support: ABC printed 143, one-based PDF 70: Berichte über feinstoffliche Körper ... Verfeinerung der Körper-Sprache; Pluto begins Entfaltung junger Menschen. Original PDF text read; existing review record supplies prior visual verification. Source terms normalize OCR spelling and are not a diplomatic transcription.

Proposed target: `tests/wiki/test_udo_rudolph_activation_repairs_batch_nine.py`. Case-fold the unchanged subtle-bodies meaning; add the verified Neptune row boundary instead of retaining Pluto clauses.

Scope: current_delta_candidate_only_after_parent_assignment.

Review record: `docs/reviews/2026-10-15-full-wiki/ledgers/activations-074.jsonl:14`.

### 24. tests/wiki/test_udo_rudolph_activation_repairs_batch_nineteen.py::test_node_vulcanus_equals_sun_uses_reviewed_abc_activation_translation

Current failed assertions:

- Line 54: `'encounter with human power' in page.body`

Raw support: ABC printed 236, one-based PDF 117: Begegnung mit menschlicher Macht ... Verbindung zu einer gewalttätigen Person. Original PDF text read; existing review record supplies prior visual verification. Source terms normalize OCR spelling and are not a diplomatic transcription.

Proposed target: `tests/wiki/test_udo_rudolph_activation_repairs_batch_nineteen.py`. Case-fold the encounter pin, retain connection to a violent person and mixed-OCR exclusion.

Scope: current_delta_candidate_only_after_parent_assignment.

Review record: `docs/reviews/2026-10-15-full-wiki/ledgers/activations-058.jsonl:35`.

### 25. tests/wiki/test_udo_rudolph_activation_repairs_batch_nineteen.py::test_node_poseidon_equals_neptune_uses_reviewed_abc_activation_translation

Current failed assertions:

- Line 62: `'disappointment in a spiritual connection' in page.body`
- Line 63: `'spiritual development in a connection' in page.body`

Raw support: ABC printed 239, one-based PDF 118: Enttäuschung in einer geistigen Verbindung ... Verbindung zu fremden Kulturen; Pluto: geistige Entwicklung in einer Verbindung. Original PDF text read plus existing full facsimile personally viewed for glyph boundary; no new scan files written

Proposed target: `tests/wiki/test_udo_rudolph_activation_repairs_batch_nineteen.py`. Require disappointment/sensitivity, metaphysical clarity and foreign cultures within Neptune; reject the Pluto development clause in this source entry.

Scope: current_delta_candidate_only_after_parent_assignment.

Review record: `docs/reviews/2026-10-15-full-wiki/ledgers/activations-058.jsonl:11`.

### 26. tests/wiki/test_udo_rudolph_activation_repairs_batch_sixteen.py::test_moon_kronos_equals_mars_uses_reviewed_abc_activation_translation

Current failed assertions:

- Line 54: `'authority of the will of a woman' in page.body`
- Line 55: `'preferential treatment of the woman' in page.body`

Raw support: ABC printed 198, one-based PDF 98: Autorität des Willens einer Frau ... vorrangige Behandlung der Frau. Original PDF text read; existing review record supplies prior visual verification. Source terms normalize OCR spelling and are not a diplomatic transcription.

Proposed target: `tests/wiki/test_udo_rudolph_activation_repairs_batch_sixteen.py`. Assert authority of a woman's will and priority treatment without requiring the old sentence form.

Scope: current_delta_candidate_only_after_parent_assignment.

Review record: `docs/reviews/2026-10-15-full-wiki/ledgers/activations-043.jsonl:41`.

### 27. tests/wiki/test_udo_rudolph_activation_repairs_batch_thirteen.py::test_moon_mars_equals_mc_uses_reviewed_abc_activation_translation

Current failed assertions:

- Line 62: `'soulful emotional actions' in page.body`

Raw support: ABC printed 180, one-based PDF 89: Beseelte Gefühls-Handlungen ... Wille meines Volkes. Original PDF text read; existing review record supplies prior visual verification. Source terms normalize OCR spelling and are not a diplomatic transcription.

Proposed target: `tests/wiki/test_udo_rudolph_activation_repairs_batch_thirteen.py`. Use bounded soul/feeling/action checks and retain will-of-my-people and corrupt-OCR rejection.

Scope: current_delta_candidate_only_after_parent_assignment.

Review record: `docs/reviews/2026-10-15-full-wiki/ledgers/activations-044.jsonl:9`.

### 28. tests/wiki/test_udo_rudolph_activation_repairs_batch_thirty_four.py::test_vulcanus_poseidon_equals_pluto_uses_reviewed_abc_activation_translation

Current failed assertions:

- Line 37: `'unfold spiritual energies' in page.body`

Raw support: ABC printed 479, one-based PDF 238: Entfaltung geistiger Gewalt ... geistige Energien entfalten ... wachsender kultureller Einfluß. Original PDF text read; existing review record supplies prior visual verification. Source terms normalize OCR spelling and are not a diplomatic transcription.

Proposed target: `tests/wiki/test_udo_rudolph_activation_repairs_batch_thirty_four.py`. Accept the grammatical unfolding wording while asserting restored force/ideas/development clauses and growing cultural influence.

Scope: current_delta_candidate_only_after_parent_assignment.

Review record: `docs/reviews/2026-10-15-full-wiki/ledgers/activations-100.jsonl:27`.

### 29. tests/wiki/test_udo_rudolph_activation_repairs_batch_thirty_one.py::test_cupido_admetos_equals_jupiter_uses_reviewed_abc_activation_translation

Current failed assertions:

- Line 38: `'blocked financial community' in page.body`

Raw support: ABC printed 432, one-based PDF 215: Blockierte Finanz-Gemeinschaft ... Gemeinschafts-Recht festigen ... gemeinsamer Erfolg durch Ausdauer. Original PDF text read; existing review record supplies prior visual verification. Source terms normalize OCR spelling and are not a diplomatic transcription.

Proposed target: `tests/wiki/test_udo_rudolph_activation_repairs_batch_thirty_one.py`. Case-fold the financial-community pin; preserve success-through-endurance and add the scan-confirmed community-law clause.

Scope: current_delta_candidate_only_after_parent_assignment.

Review record: `docs/reviews/2026-10-15-full-wiki/ledgers/activations-008.jsonl:41`.

### 30. tests/wiki/test_udo_rudolph_activation_repairs_batch_thirty_one.py::test_cupido_vulcanus_equals_mc_uses_reviewed_abc_activation_translation

Current failed assertions:

- Line 46: `'shared psychic influence' in page.body`

Raw support: ABC printed 434, one-based PDF 216: Gemeinsamer seelischer Einfluß ... psychische Energie einer Gemeinschaft ... seelische Kraft einer Gemeinschaft. Original PDF text read; existing review record supplies prior visual verification. Source terms normalize OCR spelling and are not a diplomatic transcription.

Proposed target: `tests/wiki/test_udo_rudolph_activation_repairs_batch_thirty_one.py`. Test shared influence of the soul/inner life separately from psychic energy; retain all seven clauses and OCR exclusion.

Scope: current_delta_candidate_only_after_parent_assignment.

Review record: `docs/reviews/2026-10-15-full-wiki/ledgers/activations-010.jsonl:54`.

### 31. tests/wiki/test_udo_rudolph_activation_repairs_batch_thirty_one.py::test_hades_admetos_equals_moon_uses_reviewed_abc_activation_translation

Current failed assertions:

- Line 54: `'lack of endurance of a woman' in page.body`
- Line 55: `'deepening into the past of a people' in page.body`

Raw support: ABC printed 444, one-based PDF 221: Ausdauer-Mangel einer Frau ... Vertiefung in die Vergangenheit eines Volkes. Original PDF text read; existing review record supplies prior visual verification. Source terms normalize OCR spelling and are not a diplomatic transcription.

Proposed target: `tests/wiki/test_udo_rudolph_activation_repairs_batch_thirty_one.py`. Case-fold the endurance clause and accept immersion in the people's past; retain full-row coverage and OCR exclusion.

Scope: current_delta_candidate_only_after_parent_assignment.

Review record: `docs/reviews/2026-10-15-full-wiki/ledgers/activations-011.jsonl:15`.

### 32. tests/wiki/test_udo_rudolph_activation_repairs_batch_thirty_three.py::test_kronos_poseidon_equals_uranus_uses_reviewed_abc_activation_translation

Current failed assertions:

- Line 38: `'spiritual impulses of authority' in page.body`

Raw support: ABC printed 467, one-based PDF 232: Geistige Impulse der Obrigkeit ... selbständige Kultur-Reform. Original PDF text read plus existing full facsimile personally viewed for glyph boundary; no new scan files written

Proposed target: `tests/wiki/test_udo_rudolph_activation_repairs_batch_thirty_three.py`. Accept intellectual/mental-spiritual wording while requiring authority and independent cultural reform in the Uranus row.

Scope: current_delta_candidate_only_after_parent_assignment.

Review record: `docs/reviews/2026-10-15-full-wiki/ledgers/activations-022.jsonl:14`.

### 33. tests/wiki/test_udo_rudolph_activation_repairs_batch_thirty_three.py::test_kronos_poseidon_equals_neptune_uses_reviewed_abc_activation_translation

Current failed assertions:

- Line 46: `'especially clear water' in page.body`
- Line 47: `'sensitivity of a spiritual authority' in page.body`

Raw support: ABC printed 467, one-based PDF 232: Besonders klares Wasser ... Sensibilität einer geistigen Obrigkeit ... wichtige Wahrheit der Metaphysik; Pluto: Dominante Ideen entwickeln. Original PDF text read plus existing full facsimile personally viewed for glyph boundary; no new scan files written

Proposed target: `tests/wiki/test_udo_rudolph_activation_repairs_batch_thirty_three.py`. Require clear water, sensitive intellectual authority and metaphysical truth; reject absorbed Pluto development within this Neptune entry.

Scope: current_delta_candidate_only_after_parent_assignment.

Review record: `docs/reviews/2026-10-15-full-wiki/ledgers/activations-022.jsonl:9`.

### 34. tests/wiki/test_udo_rudolph_activation_repairs_batch_thirty_two.py::test_kronos_apollon_equals_vulcanus_uses_reviewed_abc_activation_translation

Current failed assertions:

- Line 62: `'special power successes' in page.body`

Raw support: ABC printed 461, one-based PDF 229: Autoritäts-Einfluß der Wissenschaft, besondere Macht-Erfolge ... wichtige Macht-Zunahme. Original PDF text read; existing review record supplies prior visual verification. Source terms normalize OCR spelling and are not a diplomatic transcription.

Proposed target: `tests/wiki/test_udo_rudolph_activation_repairs_batch_thirty_two.py`. Check special power successes via a source-grounded semantic phrase, preserving knowledge/state influence and increased power.

Scope: current_delta_candidate_only_after_parent_assignment.

Review record: `docs/reviews/2026-10-15-full-wiki/ledgers/activations-021.jsonl:28`.

### 35. tests/wiki/test_udo_rudolph_activation_repairs_batch_three.py::test_vernal_point_neptune_equals_mc_uses_reviewed_abc_activation_translation

Current failed assertions:

- Line 46: `'my disappointments in public life' in page.body`

Raw support: ABC printed 40, one-based PDF 19: Meine Enttäuschungen im öffentlichen Leben ... seelisches Feingefühl in der Öffentlichkeit. Original PDF text read; existing review record supplies prior visual verification. Source terms normalize OCR spelling and are not a diplomatic transcription.

Proposed target: `tests/wiki/test_udo_rudolph_activation_repairs_batch_three.py`. Case-fold the disappointments pin; retain public uncertainty and mixed-OCR rejection, with correct inner-sensitivity meaning.

Scope: current_delta_candidate_only_after_parent_assignment.

Review record: `docs/reviews/2026-10-15-full-wiki/ledgers/activations-096.jsonl:21`.

### 36. tests/wiki/test_udo_rudolph_activation_repairs_batch_twelve.py::test_sun_apollon_equals_vulcanus_uses_reviewed_abc_activation_translation

Current failed assertions:

- Line 46: `'expansion of masculine power' in page.body`
- Line 47: `'growing power of a person' in page.body`

Raw support: ABC printed 167, one-based PDF 82: Ausdehnung der männlichen Gewalt ... Gewalt vieler Menschen ... zunehmende Macht eines Menschen. Original PDF text read; existing review record supplies prior visual verification. Source terms normalize OCR spelling and are not a diplomatic transcription.

Proposed target: `tests/wiki/test_udo_rudolph_activation_repairs_batch_twelve.py`. Require expansion of masculine force and growing personal power; preserve the source's force/power distinction rather than restore a flattened translation.

Scope: current_delta_candidate_only_after_parent_assignment.

Review record: `docs/reviews/2026-10-15-full-wiki/ledgers/activations-070.jsonl:50`.

### 37. tests/wiki/test_udo_rudolph_activation_repairs_batch_twelve.py::test_sun_admetos_equals_mc_uses_reviewed_abc_activation_translation

Current failed assertions:

- Line 54: `'my bodily circulation' in page.body`
- Line 55: `'soulful depth of a person' in page.body`

Raw support: ABC printed 168, one-based PDF 83: Mein Körper-Kreislauf ... seelischer Tiefgang eines Menschen. Original PDF text read; existing review record supplies prior visual verification. Source terms normalize OCR spelling and are not a diplomatic transcription.

Proposed target: `tests/wiki/test_udo_rudolph_activation_repairs_batch_twelve.py`. Case-fold bodily circulation and verify inner depth, retaining corrupt-OCR rejection and the three distinct inward states.

Scope: current_delta_candidate_only_after_parent_assignment.

Review record: `docs/reviews/2026-10-15-full-wiki/ledgers/activations-070.jsonl:19`.

### 38. tests/wiki/test_udo_rudolph_activation_repairs_batch_twenty_five.py::test_jupiter_zeus_equals_asc_uses_reviewed_abc_activation_translation

Current failed assertions:

- Line 38: `'successful striving toward goals of a place' in page.body`
- Line 39: `'performance successes of the partner' in page.body`

Raw support: ABC printed 336, one-based PDF 167: Erfolgreiches Zielstreben eines Ortes ... Leistungs-Erfolge des Partners. Original PDF text read; existing review record supplies prior visual verification. Source terms normalize OCR spelling and are not a diplomatic transcription.

Proposed target: `tests/wiki/test_udo_rudolph_activation_repairs_batch_twenty_five.py`. Assert local successful goal pursuit and partner accomplishments within the ABC row, retaining the old-OCR exclusion.

Scope: current_delta_candidate_only_after_parent_assignment.

Review record: `docs/reviews/2026-10-15-full-wiki/ledgers/activations-020.jsonl:30`.

### 39. tests/wiki/test_udo_rudolph_activation_repairs_batch_twenty_one.py::test_mercury_cupido_equals_neptune_uses_reviewed_abc_activation_translation

Current failed assertions:

- Line 46: `'foreign language community' in page.body`
- Line 47: `'evolutionary conversations in the community' in page.body`

Raw support: ABC printed 255, one-based PDF 126: Fremde Sprach-Gemeinschaft ... gemeinsame Zukunft der Jugend; Pluto: Entfaltung einer jungen Gemeinschaft, Evolutions-Gespräche in der Gemeinschaft. Original PDF text read plus existing full facsimile personally viewed for glyph boundary; no new scan files written

Proposed target: `tests/wiki/test_udo_rudolph_activation_repairs_batch_twenty_one.py`. Require the foreign-language community, future communities/art/youth; reject Pluto's evolutionary conversations within this Neptune entry.

Scope: current_delta_candidate_only_after_parent_assignment.

Review record: `docs/reviews/2026-10-15-full-wiki/ledgers/activations-034.jsonl:37`.

### 40. tests/wiki/test_udo_rudolph_activation_repairs_batch_twenty_six.py::test_saturn_apollon_equals_uranus_uses_reviewed_abc_activation_translation

Current failed assertions:

- Line 46: `'tasks of technical science' in page.body`

Raw support: ABC printed 363, one-based PDF 180: Aufgaben der technischen Wissenschaft ... Zunahme neuer Pflichten. Original PDF text read; existing review record supplies prior visual verification. Source terms normalize OCR spelling and are not a diplomatic transcription.

Proposed target: `tests/wiki/test_udo_rudolph_activation_repairs_batch_twenty_six.py`. Case-fold the technical-science phrase and retain new duties plus corrupt-OCR exclusion.

Scope: current_delta_candidate_only_after_parent_assignment.

Review record: `docs/reviews/2026-10-15-full-wiki/ledgers/activations-064.jsonl:37`.

### 41. tests/wiki/test_udo_rudolph_activation_repairs_batch_twenty_three.py::test_mars_admetos_equals_pluto_uses_reviewed_abc_activation_translation

Current failed assertions:

- Line 63: `'growing impulses of depression' in page.body`

Raw support: ABC printed 319, one-based PDF 158: Ausdauer in der Arbeit entwickeln ... wachsende Depressions-Impulse. Original PDF text read; existing review record supplies prior visual verification. Source terms normalize OCR spelling and are not a diplomatic transcription.

Proposed target: `tests/wiki/test_udo_rudolph_activation_repairs_batch_twenty_three.py`. Assert the same growing-depression motif with full seven-clause row coverage, retaining thorough work changes and corrupt-OCR rejection.

Scope: current_delta_candidate_only_after_parent_assignment.

Review record: `docs/reviews/2026-10-15-full-wiki/ledgers/activations-022.jsonl:50`.

### 42. tests/wiki/test_udo_rudolph_priority_translation_repairs.py::test_neptune_factor_uses_reviewed_abc_keyword_translation

Current failed assertions:

- Line 39: `'Unklarheit, Unsicherheit' not in page.body`

Raw support: ABC printed 17, one-based PDF 7: Unbekanntes, Unklarheit, Unsicherheit ... Gestaltloses, Verneinung. Original PDF text read; existing review record supplies prior visual verification. Source terms normalize OCR spelling and are not a diplomatic transcription.

Proposed target: `tests/wiki/test_udo_rudolph_priority_translation_repairs.py`. Assert English translation inside its labeled translation and allow explicitly labeled German source quotation; continue rejecting mixed-language OCR in English prose.

Scope: current_delta_candidate_only_after_parent_assignment.

Review record: `docs/reviews/2026-10-15-full-wiki/ledgers/factors-004.jsonl:2`.

### 43. tests/wiki/test_udo_rudolph_priority_translation_repairs.py::test_sun_mc_axis_uses_reviewed_abc_pair_summary

Current failed assertions:

- Line 46: `'self in the day' in page.body`

Raw support: ABC printed 62–63, one-based PDF 30: Beseelter Mensch, ich am Tage ... Zentrum der Seele. Original PDF text read; existing review record supplies prior visual verification. Source terms normalize OCR spelling and are not a diplomatic transcription.

Proposed target: `tests/wiki/test_udo_rudolph_priority_translation_repairs.py`. Require the first-person daytime meaning and center of the soul, with mixed-OCR exclusions unchanged.

Scope: current_delta_candidate_only_after_parent_assignment.

Review record: `docs/reviews/2026-10-15-full-wiki/ledgers/axes-021.jsonl:6`.


