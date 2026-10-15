# SI Ingestion QA Command Results

Repo: `W:\Stellar Influences`
Python: `C:/pyMADMAX2/miniconda3/envs/deep11/python.exe`
Range reviewed: `ccfbfb72^..HEAD`

## Maintenance Commands

### rebuild_index

Invocation:

```powershell
C:/pyMADMAX2/miniconda3/envs/deep11/python.exe tools/rebuild_index.py
```

Result: exit `0`, stdout empty.

### query_manifest

Invocation:

```powershell
C:/pyMADMAX2/miniconda3/envs/deep11/python.exe tools/query_manifest.py
```

Result: exit `0`, stdout empty.

### lint_wiki

Invocation:

```powershell
C:/pyMADMAX2/miniconda3/envs/deep11/python.exe tools/lint_wiki.py
```

Result: exit `0`.

Output:

```text
Lint passed
```

## Git Checks

Invocation:

```powershell
git diff --name-only -- wiki/index.md wiki/query-guide.md wiki/query-manifest.json
```

Result: exit `0`, stdout empty. The rebuild commands produced no tracked diffs in the generated query/index files.

Invocation:

```powershell
git status --short -- wiki
```

Result: exit `0`.

Output:

```text
?? wiki/.obsidian/
```

Invocation:

```powershell
git diff --name-status -- wiki
```

Result: exit `0`, stdout empty. No tracked wiki diffs after the maintenance commands.

Invocation:

```powershell
git diff --check -- wiki/index.md wiki/query-guide.md wiki/query-manifest.json
```

Result: exit `0`, stdout empty.

