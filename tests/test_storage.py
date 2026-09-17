import json

import pytest

from mactrix.storage import load_addresses, save_addresses

ADDRESSES = ["02:10:00:AA:BB:CC", "02:10:00:11:22:33"]


@pytest.mark.parametrize("extension", [".txt", ".csv", ".json"])
def test_round_trip(tmp_path, extension):
    path = tmp_path / f"addresses{extension}"
    save_addresses(path, ADDRESSES)
    loaded, invalid = load_addresses(path)
    assert invalid == 0
    assert loaded == ADDRESSES


def test_invalid_rows_are_counted(tmp_path):
    path = tmp_path / "addresses.txt"
    path.write_text("02:10:00:AA:BB:CC\nnot-a-mac\n", encoding="utf-8")
    loaded, invalid = load_addresses(path)
    assert loaded == ["02:10:00:AA:BB:CC"]
    assert invalid == 1


def test_json_list_compatibility(tmp_path):
    path = tmp_path / "addresses.json"
    path.write_text(json.dumps(ADDRESSES), encoding="utf-8")
    loaded, invalid = load_addresses(path)
    assert loaded == ADDRESSES
    assert invalid == 0


def test_save_deduplicates(tmp_path):
    path = tmp_path / "addresses.txt"
    save_addresses(path, ADDRESSES + [ADDRESSES[0]])
    loaded, _ = load_addresses(path)
    assert loaded == ADDRESSES
