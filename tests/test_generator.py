import pytest

from mactrix.generator import MAX_BATCH, PROFILES, format_mac, generate_many, generate_one, resolve_prefix
from mactrix.validation import is_locally_administered, is_unicast, is_valid


def test_generate_one_is_valid_local_unicast():
    value = generate_one("generic")
    assert is_valid(value)
    assert is_unicast(value)
    assert is_locally_administered(value)


@pytest.mark.parametrize("profile", list(PROFILES))
def test_profiles_generate_expected_prefix(profile):
    value = generate_one(profile)
    expected = ":".join(f"{byte:02X}" for byte in PROFILES[profile].prefix)
    assert value.startswith(expected + ":")


def test_custom_prefix_forces_local_unicast_bits():
    assert resolve_prefix("generic", "01:AA:bb") == (0x02, 0xAA, 0xBB)


def test_generate_many_is_unique():
    values = generate_many(500, "desktop")
    assert len(values) == len(set(values)) == 500


def test_generate_many_reports_progress_to_completion():
    events: list[tuple[int, int]] = []
    values = generate_many(250, "mobile", progress=lambda done, total: events.append((done, total)))
    assert len(values) == 250
    assert events
    assert events[-1] == (250, 250)
    assert all(0 < done <= total == 250 for done, total in events)
    assert [done for done, _ in events] == sorted(done for done, _ in events)


def test_format_options():
    raw = (0x02, 0x10, 0x00, 0xAA, 0xBB, 0xCC)
    assert format_mac(raw, separator="-") == "02-10-00-AA-BB-CC"
    assert format_mac(raw, separator="", uppercase=False) == "021000aabbcc"


@pytest.mark.parametrize("count", [0, -1, MAX_BATCH + 1])
def test_invalid_batch_count(count):
    with pytest.raises(ValueError):
        generate_many(count)


def test_invalid_profile():
    with pytest.raises(ValueError):
        generate_one("missing")
