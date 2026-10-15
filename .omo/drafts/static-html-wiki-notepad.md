# Static HTML Wiki Notepad

## Skill Survey
- `omo:ulw-plan`: explicitly requested; used for exploration-first planning discipline. Its planner-only rule conflicts with the active ultrawork instruction to deliver the artifact in this turn, so implementation continues under the newer ultrawork directive.
- `omo:frontend`: required because the deliverable is a browser-facing static HTML wiki.
- `omo:programming`: required because the generator and tests are Python.
- `omo:visual-qa`: required after changing/building a browser UI.

## Tier
HEAVY. The work creates a new generated static web surface, package artifact, and generator/test path over 5,761 wiki pages.

## Assumptions
- "Planetary pictures" means oriented activation pages (`page_type: activation`, formulas like `Sun/Moon = Venus`).
- The portable zip must work after extraction without network access or server-side code.
- The generated site should focus navigation on factors, axes, and planetary pictures, while preserving internal context links where exported.
- Existing dirty worktree changes are unrelated and must not be reverted.

## Success Criteria
- SC1: Static export includes every factor, axis, and activation page from the wiki corpus.
- SC2: The export has a browsable index, page-type navigation, local search data, rewritten `.md` links, and no remote runtime dependencies.
- SC3: A portable zip is produced under `outputs/` and contains the generated HTML/CSS/JS assets.
- SC4: Focused pytest checks pass with `C:/pyMADMAX2/miniconda3/envs/deep11/python.exe`.
- SC5: Browser QA passes at 375px, 768px, and 1280px with captured screenshots.
- SC6: Review gate approves or all findings are fixed and resubmitted.

## Evidence Log
- Skill references read: ulw-plan `SKILL.md`, `references/full-workflow.md`, `references/intent-clear.md`; frontend `SKILL.md`, design README, design-system architecture, taste-skill, perfection README; programming `SKILL.md`, Python README, one-liners; visual-qa `SKILL.md`.
- Repo survey: 23 factor pages, 266 axis pages, 5,472 activation pages; 5,761 total primary pages.
- CodeGraph returned 0 flows, so direct file inspection is the source of truth.

## QA Scenarios
- RED: `C:/pyMADMAX2/miniconda3/envs/deep11/python.exe -m pytest tests/tools/test_export_static_wiki.py -q` must fail before generator implementation.
- GREEN: same focused pytest command must pass after implementation.
- Package: `C:/pyMADMAX2/miniconda3/envs/deep11/python.exe tools/export_static_wiki.py` must create `outputs/stellar-influences-static-wiki.zip`.
- Browser: open generated `outputs/static-wiki/index.html` through a local server or file URL; screenshot 375/768/1280; PASS if index shows counts/search/navigation and a sample activation page renders body content with local assets.

- RED 2026-06-23T06:45:43.9770782+00:00: C:/pyMADMAX2/miniconda3/envs/deep11/python.exe -m pytest tests/tools/test_export_static_wiki.py -q failed with ModuleNotFoundError for tools.export_static_wiki, as expected before implementation.
- GREEN: Focused exporter tests passed: `PYTHONDONTWRITEBYTECODE=1 C:/pyMADMAX2/miniconda3/envs/deep11/python.exe -m pytest tests/tools/test_export_static_wiki.py -q` -> 2 passed.
- EXPORT: `tools/export_static_wiki.py --wiki-root wiki --out-dir outputs/static-wiki --zip outputs/stellar-influences-static-wiki.zip` exported 5,761 primary pages and created `outputs/stellar-influences-static-wiki.zip`.
- PACKAGE CHECK: 5,765 HTML files generated; zip size 11M; required entries present; no `href="*.md` links found in `outputs/static-wiki`.
- GUARDRAILS: `tests/tools/test_export_static_wiki.py tests/tools/test_wiki_links.py tests/tools/test_normalize_identity.py tests/tools/test_lint_wiki.py -q` -> 22 passed.
- BROWSER POLICY: direct `file://` QA was blocked by Browser Use URL policy. Portability was verified by zip contents and relative links; browser rendering was verified through a local HTTP server serving the same `outputs/static-wiki` folder.
- BROWSER QA: `http://127.0.0.1:8765/index.html` passed viewport checks at 375, 768, and 1280 widths. Stats shown: 23 factors, 266 axes, 5472 planetary pictures. Search input present. Local assets only. No horizontal overflow.
- BROWSER QA: Search for `Sun/Moon = Venus` returned exactly `activations/sun-moon-equals-venus.html`; navigation loaded `Sun/Moon = Venus`; formula text present; no `.md` links; no horizontal overflow.
- SCREENSHOTS: `.codex_tmp/static-wiki-qa/http-index-375.png`, `.codex_tmp/static-wiki-qa/http-index-768.png`, `.codex_tmp/static-wiki-qa/http-index-1280.png`, `.codex_tmp/static-wiki-qa/http-activation-1280.png`.
- CLEANUP: local HTTP server PID 19908 terminated; port 8765 has no LISTENING socket remaining.
- REFACTOR: split oversized exporter after size check. Final pure line counts: `tools/export_static_wiki.py` 139, `tools/static_wiki_render.py` 172.
- POST-REFACTOR TESTS: `PYTHONDONTWRITEBYTECODE=1 C:/pyMADMAX2/miniconda3/envs/deep11/python.exe -m pytest tests/tools/test_export_static_wiki.py tests/tools/test_wiki_links.py tests/tools/test_normalize_identity.py tests/tools/test_lint_wiki.py -q` -> 22 passed.
- POST-REFACTOR EXPORT: regenerated 5,761 primary pages and `outputs/stellar-influences-static-wiki.zip`.
- FINAL PACKAGE CHECK: 5,765 HTML files; zip 11M with 5,769 entries; required entries present; no `href="*.md` links found.
- FINAL BROWSER QA: local HTTP render of regenerated output passed at 375/768/1280 with no horizontal overflow, local assets only, counts 23/266/5472, search to `Sun/Moon = Venus`, activation page formula present, no Markdown hrefs.
- FINAL SCREENSHOTS: `.codex_tmp/static-wiki-qa/final-index-375.png`, `.codex_tmp/static-wiki-qa/final-index-768.png`, `.codex_tmp/static-wiki-qa/final-index-1280.png`, `.codex_tmp/static-wiki-qa/final-activation-1280.png`.
- FINAL CLEANUP: QA server PID 9988 terminated; no LISTENING socket remains on port 8765.
- REVIEW FIX: Added `UnsafeExportPathError` guard so `build_static_wiki` refuses `out_dir` equal to wiki root, inside wiki root, or repository root before deleting an existing output directory.
- REVIEW FIX TEST: Added regression test proving output inside wiki root raises and leaves source wiki page intact.
- FINAL TESTS AFTER GUARD: `PYTHONDONTWRITEBYTECODE=1 C:/pyMADMAX2/miniconda3/envs/deep11/python.exe -m pytest tests/tools/test_export_static_wiki.py tests/tools/test_wiki_links.py tests/tools/test_normalize_identity.py tests/tools/test_lint_wiki.py -q` -> 23 passed.
- FINAL SIZE AFTER GUARD: exporter 159, renderer 172, export test 104 pure LOC.
- FINAL EXPORT AFTER GUARD: regenerated 5,761 primary pages and `outputs/stellar-influences-static-wiki.zip`.
- REVIEW FIX: Added `zip_path` validation before `_zip_dir` can unlink/truncate. Zip path now rejects wiki root, paths inside wiki root, repository root, output directory, and paths inside output directory.
- REVIEW FIX TEST: Added regression test proving a zip path aimed at an existing wiki page raises and leaves the page text unchanged.
- FINAL TESTS AFTER ZIP GUARD: `PYTHONDONTWRITEBYTECODE=1 C:/pyMADMAX2/miniconda3/envs/deep11/python.exe -m pytest tests/tools/test_export_static_wiki.py tests/tools/test_wiki_links.py tests/tools/test_normalize_identity.py tests/tools/test_lint_wiki.py -q` -> 24 passed.
- FINAL SIZE AFTER ZIP GUARD: exporter 171, renderer 172, export test 120 pure LOC.
- FINAL EXPORT AFTER ZIP GUARD: regenerated 5,761 primary pages and `outputs/stellar-influences-static-wiki.zip`.
