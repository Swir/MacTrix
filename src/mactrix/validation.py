from __future__ import annotations

import re

_HEX12 = re.compile(r"^[0-9A-Fa-f]{12}$")


def _hex12(value: str) -> str:
    cleaned = value.strip().replace(":", "").replace("-", "").replace(".", "")
    if not _HEX12.fullmatch(cleaned):
        raise ValueError("Invalid MAC address")
    return cleaned


def canonicalize(value: str, *, separator: str = ":", uppercase: bool = True) -> str:
    if separator not in {":", "-", ""}:
        raise ValueError("Unsupported separator")
    cleaned = _hex12(value)
    pairs = [cleaned[i : i + 2] for i in range(0, 12, 2)]
    result = separator.join(pairs)
    return result.upper() if uppercase else result.lower()


def is_valid(value: str) -> bool:
    try:
        _hex12(value)
    except (TypeError, AttributeError, ValueError):
        return False
    return True


def first_octet(value: str) -> int:
    return int(_hex12(value)[:2], 16)


def is_unicast(value: str) -> bool:
    return (first_octet(value) & 0x01) == 0


def is_locally_administered(value: str) -> bool:
    return (first_octet(value) & 0x02) == 0x02


def analyze(value: str) -> dict[str, bool | str]:
    canonical = canonicalize(value)
    return {
        "canonical": canonical,
        "valid": True,
        "unicast": is_unicast(canonical),
        "locally_administered": is_locally_administered(canonical),
    }
