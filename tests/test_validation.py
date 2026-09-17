import pytest

from mactrix.validation import analyze, canonicalize, is_locally_administered, is_unicast, is_valid


@pytest.mark.parametrize(
    "value",
    ["02:10:00:AA:BB:CC", "02-10-00-aa-bb-cc", "021000AABBCC", "0210.00AA.BBCC"],
)
def test_supported_input_formats(value):
    assert is_valid(value)
    assert canonicalize(value) == "02:10:00:AA:BB:CC"


@pytest.mark.parametrize("value", ["", "GG:10:00:AA:BB:CC", "02:10:00:AA:BB", "02:10:00:AA:BB:CC:DD"])
def test_invalid_values(value):
    assert not is_valid(value)


def test_scope_flags():
    assert is_unicast("02:00:00:00:00:01")
    assert is_locally_administered("02:00:00:00:00:01")
    assert not is_unicast("03:00:00:00:00:01")


def test_analyze():
    result = analyze("02-10-00-aa-bb-cc")
    assert result == {
        "canonical": "02:10:00:AA:BB:CC",
        "valid": True,
        "unicast": True,
        "locally_administered": True,
    }
