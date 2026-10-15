# manualQa

## surfaceEvidence

| scenario id | criterion reference | surface | exact invocation | verdict | artifactRefs |
|---|---|---|---|---|---|
| S1 | maintenance rebuild/index | repo command | `C:/pyMADMAX2/miniconda3/envs/deep11/python.exe tools/rebuild_index.py` | PASS | A1 |
| S2 | maintenance query surfaces | repo command | `C:/pyMADMAX2/miniconda3/envs/deep11/python.exe tools/query_manifest.py` | PASS | A1 |
| S3 | wiki lint | repo command | `C:/pyMADMAX2/miniconda3/envs/deep11/python.exe tools/lint_wiki.py` | PASS | A1 |
| S4 | sampled page type/orientation rules | sampled wiki reads | `Get-Content ...`, `rg ...`, `Select-String ...` against sampled pages | PASS | A2 |
| S5 | tracked wiki diff cleanliness | git status/diff | `git diff --name-only -- wiki/index.md wiki/query-guide.md wiki/query-manifest.json`; `git diff --name-status -- wiki` | PASS | A1 |

## adversarialCases

| scenario id | criterion reference | adversarial class | expected behavior | verdict | artifactRefs |
|---|---|---|---|---|---|
| A-1 | generated surfaces deterministic | stale generated query/index files | rebuild commands should exit 0 and leave no tracked generated diffs | PASS | A1 |
| A-2 | activation orientation safety | triad collapse risk | activation pages preserve `normalized_formula`, `axis`, and `activated_by`; triad hub lists orientations without merging meanings | PASS | A2 |
| A-3 | anchor contract | missing stable section anchor | canonical factor/axis/activation pages include `<a id="derived-synthesis"></a>` before `## Derived Synthesis` | PASS | A2 |

## artifactRefs

| id | kind | description | path |
|---|---|---|---|
| A1 | command transcript | Maintenance command results and git diff/status checks | `.omo/evidence/si-ingestion-qa/command-results.md` |
| A2 | sampled page evidence | Sampled page metadata, anchor, and orientation checks | `.omo/evidence/si-ingestion-qa/sampled-pages.md` |

