# Repository Cleanup Notes

Recommended repository policy:

## Keep

- source `.py` files
- `README*.md`
- `requirements*.txt`
- `assets/`
- `deployment/`
- test scripts

## Do not commit

- `__pycache__/`
- `*.pyc`
- local Excel outputs
- generated PDF outputs
- generated ZIP packages
- temporary supplier files with sensitive stock/pricing data

## Suggested .gitignore

Already included in this package.
