# Static HTML Wiki Code Review

## Verdict
APPROVED

## Findings
No blocking findings and no unresolved low findings.

### CRITICAL
- None.

### HIGH
- None.

### MEDIUM
- None.

### LOW
- None.

## omo:programming Coverage
Skill-perspective check ran. I loaded `omo:programming`, its Python reference README, and the code-smell reference before judging Python strictness, maintainability, and test relevance.

- Destructive output deletion is guarded before `shutil.rmtree(out_dir)`: `tools/export_static_wiki.py:172` resolves `wiki_root`, `out_dir`, and `zip_path`; `tools/export_static_wiki.py:176` calls `_validate_output_dir()` before the delete at `tools/export_static_wiki.py:178`; `_validate_output_dir()` rejects the wiki root, paths inside the wiki root, and the repository root at `tools/export_static_wiki.py:68`.
- Destructive zip overwrite/truncation is guarded before `_zip_dir()`: `tools/export_static_wiki.py:177` calls `_validate_zip_path()` before `_zip_dir()` at `tools/export_static_wiki.py:196`; `_validate_zip_path()` rejects the wiki root, paths inside the wiki root, the repository root, the output directory, and paths inside the output directory at `tools/export_static_wiki.py:78`.
- Exporter dataclasses use `@dataclass(frozen=True, slots=True)` at `tools/export_static_wiki.py:30` and `tools/export_static_wiki.py:38`.
- Pure LOC stays under the 250-line ceiling: `tools/export_static_wiki.py` 171, `tools/static_wiki_render.py` 172, `tests/tools/test_export_static_wiki.py` 120.
- Scoped scans found no `Any`, `# type: ignore`, `pyright: ignore`, broad catches, bare catches, silent catches, or debug logging in the reviewed Python files. The only `print(...)` calls are CLI completion output.
- No parameter-bloat or unsafe over-abstraction issue was found in the scoped Python surface.
- The focused tests lock observable behavior through the public `build_static_wiki()` entry point: primary page inclusion and link rewriting at `tests/tools/test_export_static_wiki.py:17`, portable zip assets at `tests/tools/test_export_static_wiki.py:82`, unsafe output-dir rejection without deleting source pages at `tests/tools/test_export_static_wiki.py:107`, and unsafe zip-path rejection without overwriting a source page at `tests/tools/test_export_static_wiki.py:127`.

## omo:remove-ai-slops Coverage
Skill-perspective check ran. I loaded `omo:remove-ai-slops` and reviewed the explicit Python, test, CSS, JS, and design files for obvious comments, over-defensive code, excessive complexity, needless abstraction, boundary violations, dead code, duplication, performance-equivalent simplifications, missing tests, and oversized modules.

- Tests are not deletion-only, tautological, or implementation-constant mirrors. They create small wiki fixtures and assert observable export results: selected page types, template exclusion, rewritten `.html` links, portable local assets, and preservation of source pages when unsafe paths are rejected.
- `PAGE_LABELS` is not dead code in the current scope. It exists only in `tools/static_wiki_render.py` and is used by home and section rendering.
- No stale TODOs, commented-out code, broad exception swallowing, speculative abstraction, oversized module, or avoidable production parsing/normalization was found in scope.
- CSS and JS are purpose-bound and small. `tools/static_wiki_assets/site.js` has no console/debug leftovers and caps rendered search results at 30.
- The diff does not violate the remove-ai-slops perspective.

## Evidence Checked
- Reviewed current contents of:
  - `tools/export_static_wiki.py`
  - `tools/static_wiki_render.py`
  - `tools/static_wiki_assets/styles.css`
  - `tools/static_wiki_assets/site.js`
  - `tests/tools/test_export_static_wiki.py`
  - `DESIGN.md`
- Consulted `tools/wiki_pages.py`; `iter_wiki_pages()` skips `_templates`, which matches the export test fixture and primary-page-only goal.
- Worktree note: the scoped static-export files are currently untracked, so `git diff` did not provide a tracked patch for them. I reviewed the file contents directly.
- Ran focused tests with the required Python environment and bytecode disabled:
  - `PYTHONDONTWRITEBYTECODE=1 C:/pyMADMAX2/miniconda3/envs/deep11/python.exe -m pytest tests/tools/test_export_static_wiki.py tests/tools/test_wiki_links.py tests/tools/test_normalize_identity.py tests/tools/test_lint_wiki.py -q`
  - Result: `24 passed in 11.57s`.
- Ran a no-write AST syntax parse for `tools/export_static_wiki.py`, `tools/static_wiki_render.py`, and `tests/tools/test_export_static_wiki.py`: passed.
- Cross-checked generated artifacts:
  - `outputs/static-wiki/manifest.json`: `page_count` 5761, counts `factor=23`, `axis=266`, `activation=5472`.
  - Source directory counts match output page counts: 23 factor pages, 266 axis pages, 5472 activation pages.
  - `outputs/static-wiki`: 5765 HTML files.
  - `outputs/stellar-influences-static-wiki.zip`: 10,677,348 bytes, 5769 entries, 5765 HTML entries, 0 Markdown entries.
  - Required zip entries present: `index.html`, `manifest.json`, `assets/styles.css`, `assets/site.js`, `assets/search-data.js`, and `activations/sun-moon-equals-venus.html`.
  - `outputs/static-wiki/assets/search-data.js`: starts with `window.STELLAR_SEARCH_DATA = ` and includes `Sun/Moon = Venus`.
- Inspected `outputs/static-wiki/activations/sun-moon-equals-venus.html`: local assets only, `h1` and formula metadata present, factor/axis links rewritten to `.html`, orientation-specific activation content preserved, and excluded support pages marked unavailable.
- Scanned generated HTML for `.md` references: no hits.
- Scanned sampled generated HTML and static assets for external `http`, `https`, and `file:` asset links: no hits.

## Residual Risks
- I did not rerun the full export command in this read-only review because it would rewrite `outputs/static-wiki` and the zip; I cross-checked the current regenerated artifacts directly.
- I did not rerun browser visual QA or inspect screenshot artifacts because no browser-QA evidence path was supplied. The post-QA code changes under review are destructive-path guards, and the generated sample plus package checks did not show a rendering, link, asset, or portability regression.
- I did not rerun `py_compile` because it can write bytecode artifacts; the focused test imports and no-write AST parse passed.
- The renderer assumes the current canonical one-level primary page directories (`factors/`, `axes/`, `activations/`). That matches the current wiki structure and generated package.
