# GitHub Sync Instructions — KURGIN Score Analyzer v1.12.2

Target repository:

```text
kka45821-del/kurgin-score-analyzer
```

## Important

The connected GitHub tool available in this session is read-only for repository contents.  
This package is prepared as a repo-ready sync package. Apply it locally via GitHub Desktop or CLI.

## Recommended sync method

1. Download this ZIP.
2. Extract it.
3. Open local repository folder:

```text
C:\Users\Karo\Documents\GitHub\kurgin-score-analyzer
```

4. Copy all extracted files into the repository root.
5. Replace existing files.
6. Make sure `.git/` stays untouched.
7. Run local smoke tests:

```bash
python -m pip install -r requirements-api.txt
set PYTHONDONTWRITEBYTECODE=1
python scripts/smoke_test_core.py
python scripts/contract_test_api.py
python scripts/smoke_test_platform_card.py
python scripts/ci_repo_hygiene.py
```

8. Commit:

```text
v1.12.2 repo sync ci gate
```

9. Push.

## Expected GitHub changes

Major folders/files:

```text
api/
kurgin_core/
platform_integration/
formula_versions/
formula_comparison/
api_contract/
deployment/
.github/workflows/ci.yml
Dockerfile
docker-compose.yml
requirements-api.txt
scripts/ci_compile.py
scripts/ci_repo_hygiene.py
```

## After push

GitHub Actions should run:

```text
KURGIN Score Analyzer CI
```
