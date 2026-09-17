from __future__ import annotations

import secrets
from dataclasses import dataclass

MAX_BATCH = 100_000


@dataclass(frozen=True)
class Profile:
    key: str
    prefix: tuple[int, int, int]


PROFILES: dict[str, Profile] = {
    "generic": Profile("generic", (0x02, 0x00, 0x00)),
    "desktop": Profile("desktop", (0x02, 0x10, 0x00)),
    "mobile": Profile("mobile", (0x02, 0x20, 0x00)),
    "router": Profile("router", (0x02, 0x30, 0x00)),
    "iot": Profile("iot", (0x02, 0x40, 0x00)),
}


def _parse_prefix(value: str) -> tuple[int, int, int]:
    cleaned = value.strip().replace("-", ":").replace(".", "")
    if ":" in cleaned:
        parts = cleaned.split(":")
    else:
        if len(cleaned) != 6:
            raise ValueError("Prefix must contain exactly 3 bytes")
        parts = [cleaned[i : i + 2] for i in range(0, 6, 2)]
    if len(parts) != 3:
        raise ValueError("Prefix must contain exactly 3 bytes")
    try:
        prefix = tuple(int(part, 16) for part in parts)
    except ValueError as exc:
        raise ValueError("Prefix contains non-hexadecimal characters") from exc
    if any(byte < 0 or byte > 255 for byte in prefix):
        raise ValueError("Prefix bytes must be in range 00-FF")
    first = (prefix[0] | 0x02) & 0xFE
    return first, prefix[1], prefix[2]


def resolve_prefix(profile: str = "generic", custom_prefix: str | None = None) -> tuple[int, int, int]:
    if custom_prefix:
        return _parse_prefix(custom_prefix)
    try:
        return PROFILES[profile].prefix
    except KeyError as exc:
        raise ValueError(f"Unknown profile: {profile}") from exc


def format_mac(raw: bytes | tuple[int, ...], separator: str = ":", uppercase: bool = True) -> str:
    if len(raw) != 6:
        raise ValueError("A MAC address must contain 6 bytes")
    if separator not in {":", "-", ""}:
        raise ValueError("Unsupported separator")
    value = separator.join(f"{byte:02x}" for byte in raw)
    return value.upper() if uppercase else value.lower()


def generate_one(
    profile: str = "generic",
    *,
    custom_prefix: str | None = None,
    separator: str = ":",
    uppercase: bool = True,
) -> str:
    prefix = resolve_prefix(profile, custom_prefix)
    suffix = secrets.token_bytes(3)
    return format_mac((*prefix, *suffix), separator=separator, uppercase=uppercase)


def generate_many(
    count: int,
    profile: str = "generic",
    *,
    custom_prefix: str | None = None,
    separator: str = ":",
    uppercase: bool = True,
) -> list[str]:
    if not isinstance(count, int):
        raise TypeError("count must be an integer")
    if count < 1 or count > MAX_BATCH:
        raise ValueError(f"count must be between 1 and {MAX_BATCH}")

    prefix = resolve_prefix(profile, custom_prefix)
    results: set[str] = set()
    while len(results) < count:
        suffix = secrets.token_bytes(3)
        results.add(format_mac((*prefix, *suffix), separator=separator, uppercase=uppercase))
    return list(results)
