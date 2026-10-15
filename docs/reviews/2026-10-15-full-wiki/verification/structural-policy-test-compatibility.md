# Narrow structural-policy test compatibility

Only two functions changed: `test_chiron_factor_page_is_explicitly_source_bounded_and_non_doctrinal` and `test_seeded_jupiter_mc_additional_activation_cluster_has_real_derived_synthesis`.

The Chiron factor test now requires its sole Sandbach scope, explicit absence of ingested standalone doctrine, and live `structural_only` / `answer_surface: false` routing. The Jupiter/MC test requires that same routing for the source-empty Chiron orientation and preserves canonical-answer requirements for all nine other formulas.

Before: both named tests failed (2 failed in 23.72s). After: the complete Chiron-policy module, the named Jupiter/MC test and `tests/tools/test_query_manifest.py` passed (9 passed in 44.95s). LSP reported no errors for either changed file. The JSON companion records the exact command, original hashes/diff, final hashes and full results.

All other functions in both files are unchanged. The other 41 initially failing tests' files and both protected user-owned test sources retain their prior hashes. Existing dirty imports/fixture tests were preserved.

No full-suite green result is claimed. The 24 source/capitalization pins and 2 other editorial pins remain 26 legacy prose-compatibility limitations. The 14 initial-snapshot failed functions remain outside this change. The source-catalog owner separately fixed the count mismatch and reported its focused test passing.

