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


def gui_smoke_test() -> int:
    import tkinter as tk

    from .app import MacTrixApp
    from .logging_config import configure_logging
    from .resources import apply_window_icon

    root = tk.Tk()
    root.withdraw()
    try:
        apply_window_icon(root)
        MacTrixApp(root, configure_logging())
        root.update_idletasks()
        root.update()
    finally:
        try:
            root.destroy()
        except tk.TclError:
            pass
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="MacTrix synthetic MAC address lab")
    parser.add_argument("--smoke-test", action="store_true", help="run a non-GUI packaged-app self test")
    parser.add_argument("--smoke-gui", action="store_true", help="construct and process the real GUI once, then exit")
    args = parser.parse_args()
    if args.smoke_test:
        return smoke_test()
    if args.smoke_gui:
        return gui_smoke_test()

    import tkinter as tk

    from .app import MacTrixApp
    from .logging_config import configure_logging
    from .resources import apply_window_icon

    root = tk.Tk()
    apply_window_icon(root)
    MacTrixApp(root, configure_logging())
    root.mainloop()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
