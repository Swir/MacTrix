from __future__ import annotations

import json
import os
from pathlib import Path

DEFAULTS = {
    "language": "auto",
    "profile": "generic",
    "separator": ":",
    "uppercase": True,
    "count": 25,
}


def app_dir() -> Path:
    if os.name == "nt":
        root = Path(os.environ.get("LOCALAPPDATA", Path.home()))
        path = root / "MacTrix"
    else:
        root = Path(os.environ.get("XDG_CONFIG_HOME", Path.home() / ".config"))
        path = root / "mactrix"
    path.mkdir(parents=True, exist_ok=True)
    return path


def load_settings() -> dict[str, object]:
    path = app_dir() / "settings.json"
    if not path.exists():
        return dict(DEFAULTS)
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
        if not isinstance(payload, dict):
            return dict(DEFAULTS)
    except (OSError, json.JSONDecodeError):
        return dict(DEFAULTS)
    result = dict(DEFAULTS)
    result.update({key: payload[key] for key in DEFAULTS if key in payload})
    return result


def save_settings(settings: dict[str, object]) -> None:
    safe = {key: settings.get(key, value) for key, value in DEFAULTS.items()}
    (app_dir() / "settings.json").write_text(json.dumps(safe, indent=2), encoding="utf-8")
