from __future__ import annotations

import argparse
import tempfile
from pathlib import Path

from .generator import generate_many
from .storage import load_addresses, save_addresses
from .validation import is_locally_administered, is_unicast, is_valid


def smoke_test() -> int:
    generated = generate_many(32, "desktop")
    if len(generated) != 32 or len(set(generated)) != 32:
        return 2
    if not all(is_valid(value) and is_unicast(value) and is_locally_administered(value) for value in generated):
        return 3
    with tempfile.TemporaryDirectory() as directory:
        target = Path(directory) / "smoke.json"
        save_addresses(target, generated)
        loaded, invalid = load_addresses(target)
        if invalid != 0 or set(loaded) != set(generated):
            return 4
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="MacTrix synthetic MAC address lab")
    parser.add_argument("--smoke-test", action="store_true", help="run a non-GUI packaged-app self test")
    args = parser.parse_args()
    if args.smoke_test:
        return smoke_test()

    from .app import run

    run()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
