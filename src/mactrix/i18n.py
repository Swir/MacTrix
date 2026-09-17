from __future__ import annotations

import locale

SUPPORTED = {"en", "pl", "no"}

TRANSLATIONS: dict[str, dict[str, str]] = {
    "en": {
        "title": "MacTrix 2 — MAC Lab",
        "subtitle": "Generate standards-safe synthetic MAC addresses for tests and labs",
        "count": "Count",
        "profile": "Profile",
        "prefix": "Custom 3-byte prefix (optional)",
        "separator": "Separator",
        "uppercase": "Uppercase",
        "generate": "Generate",
        "copy": "Copy selected",
        "copy_all": "Copy all",
        "save": "Export",
        "load": "Import",
        "sort": "Sort",
        "dedupe": "Remove duplicates",
        "clear": "Clear",
        "status_ready": "Ready",
        "status_generated": "Generated {count} unique local-unicast addresses",
        "status_loaded": "Loaded {count} valid addresses; skipped {invalid} invalid rows",
        "status_saved": "Saved {count} addresses",
        "invalid_count": "Count must be an integer from 1 to 100000.",
        "invalid_prefix": "The custom prefix must contain exactly 3 hexadecimal bytes.",
        "nothing": "There are no addresses to export.",
        "copied": "Copied to clipboard",
        "profile_generic": "Generic",
        "profile_desktop": "Desktop",
        "profile_mobile": "Mobile",
        "profile_router": "Router",
        "profile_iot": "IoT",
        "about": "Generated addresses are synthetic, locally administered and unicast. Profiles do not represent vendor OUIs.",
        "file_error": "File operation failed: {error}",
    },
    "pl": {
        "title": "MacTrix 2 — Laboratorium MAC",
        "subtitle": "Generuj bezpieczne, syntetyczne adresy MAC do testów i laboratoriów",
        "count": "Liczba",
        "profile": "Profil",
        "prefix": "Własny prefiks 3-bajtowy (opcjonalnie)",
        "separator": "Separator",
        "uppercase": "Wielkie litery",
        "generate": "Generuj",
        "copy": "Kopiuj zaznaczone",
        "copy_all": "Kopiuj wszystko",
        "save": "Eksportuj",
        "load": "Importuj",
        "sort": "Sortuj",
        "dedupe": "Usuń duplikaty",
        "clear": "Wyczyść",
        "status_ready": "Gotowe",
        "status_generated": "Wygenerowano {count} unikalnych lokalnych adresów unicast",
        "status_loaded": "Wczytano {count} poprawnych adresów; pominięto {invalid} błędnych wierszy",
        "status_saved": "Zapisano {count} adresów",
        "invalid_count": "Liczba musi być całkowita od 1 do 100000.",
        "invalid_prefix": "Własny prefiks musi zawierać dokładnie 3 bajty szesnastkowe.",
        "nothing": "Brak adresów do eksportu.",
        "copied": "Skopiowano do schowka",
        "profile_generic": "Ogólny",
        "profile_desktop": "Komputer",
        "profile_mobile": "Telefon",
        "profile_router": "Router",
        "profile_iot": "IoT",
        "about": "Generowane adresy są syntetyczne, lokalnie administrowane i unicast. Profile nie udają prawdziwych prefiksów producentów.",
        "file_error": "Operacja na pliku nie powiodła się: {error}",
    },
    "no": {
        "title": "MacTrix 2 — MAC-lab",
        "subtitle": "Generer trygge, syntetiske MAC-adresser for test og lab",
        "count": "Antall",
        "profile": "Profil",
        "prefix": "Eget 3-byte prefiks (valgfritt)",
        "separator": "Skilletegn",
        "uppercase": "Store bokstaver",
        "generate": "Generer",
        "copy": "Kopier valgte",
        "copy_all": "Kopier alle",
        "save": "Eksporter",
        "load": "Importer",
        "sort": "Sorter",
        "dedupe": "Fjern duplikater",
        "clear": "Tøm",
        "status_ready": "Klar",
        "status_generated": "Genererte {count} unike lokale unicast-adresser",
        "status_loaded": "Lastet {count} gyldige adresser; hoppet over {invalid} ugyldige rader",
        "status_saved": "Lagret {count} adresser",
        "invalid_count": "Antall må være et heltall fra 1 til 100000.",
        "invalid_prefix": "Eget prefiks må inneholde nøyaktig 3 heksadesimale byte.",
        "nothing": "Det finnes ingen adresser å eksportere.",
        "copied": "Kopiert til utklippstavlen",
        "profile_generic": "Generell",
        "profile_desktop": "Datamaskin",
        "profile_mobile": "Mobil",
        "profile_router": "Ruter",
        "profile_iot": "IoT",
        "about": "Genererte adresser er syntetiske, lokalt administrerte og unicast. Profiler representerer ikke leverandør-OUI-er.",
        "file_error": "Filoperasjonen mislyktes: {error}",
    },
}


def detect_language() -> str:
    code = (locale.getlocale()[0] or "en").split("_")[0].lower()
    if code == "nb" or code == "nn":
        code = "no"
    return code if code in SUPPORTED else "en"


def tr(language: str, key: str, **values: object) -> str:
    table = TRANSLATIONS.get(language, TRANSLATIONS["en"])
    template = table.get(key, TRANSLATIONS["en"].get(key, key))
    return template.format(**values)
