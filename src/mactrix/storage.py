from __future__ import annotations

import csv
import json
from pathlib import Path

from .validation import canonicalize, is_valid


def _clean(addresses: list[str]) -> list[str]:
    result: list[str] = []
    seen: set[str] = set()
    for value in addresses:
        if not is_valid(value):
            continue
        canonical = canonicalize(value)
        if canonical not in seen:
            result.append(canonical)
            seen.add(canonical)
    return result


def save_addresses(path: str | Path, addresses: list[str]) -> Path:
    target = Path(path)
    cleaned = _clean(addresses)
    suffix = target.suffix.lower()

    if suffix == ".json":
        target.write_text(
            json.dumps({"format": "mactrix-2", "addresses": cleaned}, indent=2),
            encoding="utf-8",
        )
    elif suffix == ".csv":
        with target.open("w", encoding="utf-8", newline="") as handle:
            writer = csv.writer(handle)
            writer.writerow(["mac_address"])
            writer.writerows([[address] for address in cleaned])
    else:
        target.write_text("\n".join(cleaned) + ("\n" if cleaned else ""), encoding="utf-8")
    return target


def load_addresses(path: str | Path) -> tuple[list[str], int]:
    source = Path(path)
    suffix = source.suffix.lower()
    raw: list[str]

    if suffix == ".json":
        payload = json.loads(source.read_text(encoding="utf-8"))
        if isinstance(payload, dict):
            values = payload.get("addresses", [])
        elif isinstance(payload, list):
            values = payload
        else:
            raise ValueError("Unsupported JSON structure")
        raw = [str(value) for value in values]
    elif suffix == ".csv":
        with source.open("r", encoding="utf-8-sig", newline="") as handle:
            rows = list(csv.reader(handle))
        raw = []
        for row in rows:
            if not row:
                continue
            value = row[0].strip()
            if value.lower() in {"mac", "mac_address", "address"}:
                continue
            raw.append(value)
    else:
        raw = [line.strip() for line in source.read_text(encoding="utf-8-sig").splitlines() if line.strip()]

    valid = _clean(raw)
    invalid_count = sum(1 for value in raw if not is_valid(value))
    return valid, invalid_count
