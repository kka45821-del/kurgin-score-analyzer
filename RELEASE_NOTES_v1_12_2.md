# KURGIN Score Analyzer v1.12.2 — Repository Sync + CI Gate

## Goal

Prepare the repository for production-grade development instead of ZIP-only versioning.

## Added

- GitHub Actions workflow:
  `.github/workflows/ci.yml`
- CI scripts:
  `scripts/ci_compile.py`
  `scripts/ci_repo_hygiene.py`
- Repository sync instructions.
- Release manifest.

## CI checks

- Python compile without pyc generation
- Core SDK smoke test
- API contract test
- Platform card endpoint test
- Formula regression smoke test
- Repository hygiene check

## Official formula

Official KURGIN Score is unchanged.
