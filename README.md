<div align="center">

# 🖧 MacTrix 2

### Modern synthetic MAC-address laboratory for Windows

**Generate • Validate • Import • Export • Test safely**

[![CI](https://github.com/Swir/MacTrix/actions/workflows/ci.yml/badge.svg)](https://github.com/Swir/MacTrix/actions/workflows/ci.yml)
![Python](https://img.shields.io/badge/Python-3.10--3.14-3776AB?logo=python&logoColor=white)
![Platform](https://img.shields.io/badge/Windows-10%20%7C%2011-0078D4?logo=windows11&logoColor=white)
![Version](https://img.shields.io/badge/version-2.0.0-2aa5ff)

</div>

---

## What changed in v2

MacTrix has been rebuilt from the old single-file Tkinter prototype into a small, tested Python package with a modern dark-blue desktop interface, safe address semantics, multilingual UI, persistent settings and an automated Windows release pipeline.

The application **does not change the MAC address of a network adapter**. It creates and validates synthetic values for development, QA, documentation, lab exercises and test datasets.

## Highlights

| Feature | MacTrix 2 |
|---|---|
| Standards-safe generation | Generated addresses are **locally administered + unicast** |
| Batch mode | 1 to 100,000 unique values per run |
| Synthetic profiles | Generic, Desktop, Mobile, Router and IoT namespaces |
| Custom prefix | Optional 3-byte prefix; local/unicast bits are normalized automatically |
| Formatting | `:` / `-` / no separator, upper or lower case |
| Import | TXT, CSV and JSON |
| Export | TXT, CSV and structured JSON |
| Validation | Accepts common MAC formats and normalizes them |
| Large batches | Full data kept for export; UI preview is capped for responsiveness |
| Languages | English, Polish and Norwegian with system-language detection |
| Settings | Language, profile, formatting and count are remembered |
| Diagnostics | Rotating local application log |
| Releases | Windows EXE + portable ZIP + SHA256 checksums |
| CI | Python 3.10, 3.11, 3.12, 3.13 and 3.14 + Windows smoke test |

## Synthetic profile prefixes

MacTrix uses private synthetic namespaces rather than pretending that generated values belong to real hardware vendors:

```text
Generic  02:00:00
Desktop  02:10:00
Mobile   02:20:00
Router   02:30:00
IoT      02:40:00
```

The first octet is always normalized so the generated address is locally administered and unicast. These prefixes are **not an IEEE OUI/vendor database**.

## Run from source

```bash
git clone https://github.com/Swir/MacTrix.git
cd MacTrix
python -m pip install -e ".[test]"
python run.py
```

Non-GUI self-test:

```bash
python -m mactrix --smoke-test
```

Run tests:

```bash
pytest
```

## Windows release

Tagged releases are built by GitHub Actions. A validated release contains:

```text
MacTrix.exe
MacTrix.exe.sha256
MacTrix-vX.Y.Z-Windows-x64.zip
MacTrix-vX.Y.Z-Windows-x64.zip.sha256
```

The packaged executable runs the same non-GUI smoke test before a release is published.

## Project layout

```text
MacTrix/
├─ assets/
│  └─ mactrix_icon.svg
├─ src/mactrix/
│  ├─ app.py
│  ├─ config.py
│  ├─ generator.py
│  ├─ i18n.py
│  ├─ logging_config.py
│  ├─ storage.py
│  └─ validation.py
├─ tests/
├─ tools/build_icon.py
├─ run.py
└─ pyproject.toml
```

## Data and privacy

MacTrix works locally. It does not need an online API, does not query vendor databases and does not transmit generated or imported address lists. User preferences and rotating logs are stored in the normal per-user application/configuration directory.

## Responsible use

Use MacTrix for your own development, testing, documentation and authorized lab environments. The project intentionally focuses on generation and validation of synthetic data; it does not include adapter spoofing, network impersonation or bypass functionality.

## Author

Developed by **Swir** — [github.com/Swir](https://github.com/Swir)

<div align="center">

**MacTrix 2 — clean test data without pretending to be real hardware.**

</div>
