from mactrix.__main__ import smoke_test
from mactrix.i18n import TRANSLATIONS, tr


def test_smoke_test():
    assert smoke_test() == 0


def test_translation_keys_match():
    baseline = set(TRANSLATIONS["en"])
    assert set(TRANSLATIONS["pl"]) == baseline
    assert set(TRANSLATIONS["no"]) == baseline


def test_translation_fallback():
    assert tr("missing", "generate") == "Generate"
