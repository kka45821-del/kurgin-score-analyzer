from __future__ import annotations

import os
from pathlib import Path


REQUIRED_IN_STAGING = [
    "KURGIN_API_ENV",
    "KURGIN_API_SECRET",
    "KURGIN_ALLOWED_ORIGINS",
]


def parse_env_file(path: Path):
    values = {}
    if not path.exists():
        return values
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        values[key.strip()] = value.strip()
    return values


def main():
    path = Path(".env.staging")
    values = parse_env_file(path)

    missing = [key for key in REQUIRED_IN_STAGING if not values.get(key)]
    weak = []
    secret = values.get("KURGIN_API_SECRET", "")
    if secret and len(secret) < 32:
        weak.append("KURGIN_API_SECRET should be at least 32 characters")

    if missing or weak:
        print("Staging env check failed")
        for item in missing:
            print("MISSING:", item)
        for item in weak:
            print("WEAK:", item)
        raise SystemExit(1)

    if values.get("KURGIN_API_ENV") != "staging":
        print("WARNING: KURGIN_API_ENV is not staging")

    print("Staging env check OK")


if __name__ == "__main__":
    main()
