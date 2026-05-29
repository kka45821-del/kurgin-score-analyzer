# Legacy Formula Versions

Put old formula variants here when available.

Recommended structure:

```text
legacy/
  old_v1/
    runner.py
    metadata.json
    notes.md
```

Each `runner.py` must expose:

```python
def calculate(engine_kwargs: dict) -> dict:
    ...
```

The output should follow current engine keys where possible:

```text
final_score
final_verdict
triple_score
structure_modifier
visual_check
critical_risk
structure_tags
diagnostics
breakdown
engine_version
```
