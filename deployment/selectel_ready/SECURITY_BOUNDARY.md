# Formula Security Boundary

## Public frontend

Should receive only:

- KURGIN Score result
- public class
- tags
- interpretation
- PDF/report output

Should not receive:

- internal coefficients
- formula implementation
- supplier files
- private diagnostics for non-professional users

## Backend

Can call:

```python
from kurgin_core import analyze_stone, analyze_dataframe
```

or HTTP Formula API.

## API key

Set:

```text
KURGIN_API_SECRET
```

and require:

```text
X-KURGIN-API-Key
```

## Recommended production model

```text
KURGIN Platform backend
  -> private Formula API
  -> closed formula code
```
