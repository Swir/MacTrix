from __future__ import annotations

import sys
from pathlib import Path
import tkinter as tk


def asset_path(name: str) -> Path:
    """Resolve an asset both from source checkout and from a PyInstaller bundle."""
    bundle_root = getattr(sys, "_MEIPASS", None)
    if bundle_root:
        return Path(bundle_root) / "assets" / name
    return Path(__file__).resolve().parents[2] / "assets" / name


def apply_window_icon(root: tk.Tk) -> None:
    """Apply the MacTrix PNG icon when available without breaking startup."""
    path = asset_path("mactrix_icon.png")
    if not path.exists():
        return
    try:
        icon = tk.PhotoImage(file=str(path))
        root.iconphoto(True, icon)
        # Tk only keeps a Tcl-side reference on some platforms; retain Python ref too.
        root._mactrix_icon = icon  # type: ignore[attr-defined]
    except tk.TclError:
        # Icon failure must never prevent the application from starting.
        return
