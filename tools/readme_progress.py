from __future__ import annotations

import argparse
import re
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PROJECT = "MacTrix 2"
SCOPE = "product roadmap"
CARD = ROOT / "assets/readme/progress-card.svg"
MINI = ROOT / "assets/readme/progress-mini.svg"
README = ROOT / "README.md"
STATUS = ROOT / "STATUS.md"
LEGACY = re.compile(r"[█▓▒░]{4,}|\[(?:[#=]{4,}|-{8,})\]")


def card() -> str:
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="180" viewBox="0 0 1200 180" role="img" aria-labelledby="title desc">
<title id="title">{PROJECT} product progress</title>
<desc id="desc">Product progress is N/A because this repository has no authoritative measurable product roadmap.</desc>
<defs><linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop stop-color="#02050A"/><stop offset="1" stop-color="#07111C"/></linearGradient><linearGradient id="accent" x1="0" y1="0" x2="1" y2="0"><stop stop-color="#0088FF"/><stop offset="1" stop-color="#62E5FF"/></linearGradient><pattern id="grid" width="32" height="32" patternUnits="userSpaceOnUse"><path d="M32 0H0V32" fill="none" stroke="#62E5FF" stroke-opacity=".05"/></pattern></defs>
<rect x="1" y="1" width="1198" height="178" rx="22" fill="url(#bg)" stroke="#62E5FF" stroke-opacity=".24"/><rect x="1" y="1" width="1198" height="178" rx="22" fill="url(#grid)"/>
<text x="50" y="38" fill="#62E5FF" font-family="Segoe UI,Arial,sans-serif" font-size="15" font-weight="700" letter-spacing="3">SWIR PROGRESS</text><text x="50" y="72" fill="#F4FAFF" font-family="Segoe UI,Arial,sans-serif" font-size="27" font-weight="800">{PROJECT}</text><text x="50" y="99" fill="#8DA8B8" font-family="Segoe UI,Arial,sans-serif" font-size="14">Measured scope: {SCOPE}</text><text x="1110" y="72" text-anchor="end" fill="#F4FAFF" font-family="Segoe UI,Arial,sans-serif" font-size="32" font-weight="800">N/A</text><text x="1110" y="99" text-anchor="end" fill="#62E5FF" font-family="Segoe UI,Arial,sans-serif" font-size="13" font-weight="700">NO AUTHORITATIVE ROADMAP</text>
<rect x="50" y="118" width="1100" height="18" rx="9" fill="#08131F" stroke="#62E5FF" stroke-opacity=".18"/><path d="M70 127H1130" stroke="url(#accent)" stroke-width="2" stroke-dasharray="7 12" opacity=".28"/><text x="50" y="159" fill="#8DA8B8" font-family="Segoe UI,Arial,sans-serif" font-size="12">No completion percentage is inferred from release version, commits, tests, or documentation.</text>
</svg>
'''


def mini() -> str:
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="900" height="72" viewBox="0 0 900 72" role="img" aria-labelledby="title desc">
<title id="title">{PROJECT} compact product progress</title><desc id="desc">Product progress is N/A; no authoritative measurable roadmap exists.</desc>
<defs><linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop stop-color="#02050A"/><stop offset="1" stop-color="#07111C"/></linearGradient><linearGradient id="accent" x1="0" y1="0" x2="1" y2="0"><stop stop-color="#0088FF"/><stop offset="1" stop-color="#62E5FF"/></linearGradient></defs>
<rect x="1" y="1" width="898" height="70" rx="16" fill="url(#bg)" stroke="#62E5FF" stroke-opacity=".24"/><text x="24" y="29" fill="#F4FAFF" font-family="Segoe UI,Arial,sans-serif" font-size="16" font-weight="700">{PROJECT}</text><text x="24" y="50" fill="#8DA8B8" font-family="Segoe UI,Arial,sans-serif" font-size="12">Product roadmap</text><rect x="250" y="27" width="550" height="14" rx="7" fill="#08131F" stroke="#62E5FF" stroke-opacity=".16"/><path d="M268 34H782" stroke="url(#accent)" stroke-width="2" stroke-dasharray="6 11" opacity=".25"/><text x="862" y="43" text-anchor="end" fill="#62E5FF" font-family="Segoe UI,Arial,sans-serif" font-size="18" font-weight="800">N/A</text>
</svg>
'''


def validate_xml(text: str) -> None:
    ET.fromstring(text)


def check() -> int:
    expected = {CARD: card(), MINI: mini()}
    for path, text in expected.items():
        validate_xml(text)
        if not path.exists() or path.read_text(encoding="utf-8") != text:
            print(f"stale: {path.relative_to(ROOT)}", file=sys.stderr)
            return 1
    for path in (README, STATUS):
        data = path.read_text(encoding="utf-8")
        if LEGACY.search(data):
            print(f"legacy progress meter: {path.relative_to(ROOT)}", file=sys.stderr)
            return 1
    if "assets/readme/progress-card.svg" not in README.read_text(encoding="utf-8"):
        return 1
    if "assets/readme/progress-mini.svg" not in STATUS.read_text(encoding="utf-8"):
        return 1
    print("README progress assets are valid and synchronized (N/A product scope).")
    return 0


def write() -> None:
    CARD.parent.mkdir(parents=True, exist_ok=True)
    CARD.write_text(card(), encoding="utf-8")
    MINI.write_text(mini(), encoding="utf-8")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    if args.check:
        raise SystemExit(check())
    write()
    raise SystemExit(check())
