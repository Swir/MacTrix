<div align="center">

<img src="assets/mactrix_icon.png" alt="MacTrix icon" width="140" />

# 🖧 MacTrix 2

### Modern synthetic MAC-address laboratory for Windows

**Generate • Validate • Import • Export • Test safely**

[![CI](https://github.com/Swir/MacTrix/actions/workflows/ci.yml/badge.svg)](https://github.com/Swir/MacTrix/actions/workflows/ci.yml)
![Python](https://img.shields.io/badge/Python-3.10--3.14-3776AB?logo=python&logoColor=white)
![Platform](https://img.shields.io/badge/Windows-10%20%7C%2011-0078D4?logo=windows11&logoColor=white)
![Version](https://img.shields.io/badge/version-2.1.0-2aa5ff)

</div>

---

## v2.1 regression audit

MacTrix 2.1 was checked against the original 2024 single-file Tkinter application. The classic user-facing workflow is preserved: choose a device/profile type, choose how many values to create, generate them, watch generation progress, load a list, save a list and sort the result. The modern version keeps those behaviors while retaining the safer package architecture introduced in v2.0.

The old generator showed a real percentage while producing values. v2.0 accidentally replaced that with an indeterminate animation; **v2.1 restores determinate 0–100% progress reporting**. The custom MacTrix icon is now also used by the running window, displayed here in README and bundled into the packaged executable.

The application **does not change the MAC address of a network adapter**. It creates and validates synthetic values for development, QA, documentation, lab exercises and test datasets.

## Classic-to-modern feature map

| Original MacTrix | MacTrix 2.1 |
|---|---|
| Number of MAC addresses | Preserved, expanded to 1–100,000 |
| Device type selector | Preserved as Generic/Desktop/Mobile/Router/IoT synthetic profiles |
| Generate button | Preserved |
| Generation progress | Preserved and restored as real 0–100% progress |
| Result list + scrollbar | Preserved with a responsive table and large-batch preview |
| Save to TXT/CSV | Preserved, plus JSON |
| Load TXT/CSV | Preserved, plus JSON and validation |
| Sort | Preserved |
| Duplicate warning | Improved: generation guarantees uniqueness; imported lists also have one-click dedupe |
| Footer / author credit | Preserved as `by Swir` |

The original hard-coded prefixes looked like vendor OUIs. Modern profiles intentionally use locally administered unicast namespaces so generated test data is clearly synthetic instead of pretending to belong to real hardware vendors.

## Highlights

| Feature | MacTrix 2.1 |
|---|---|
| Standards-safe generation | Generated addresses are **locally administered + unicast** |
| Batch mode | 1 to 100,000 unique values per run |
| Progress | Determinate 0–100% progress during generation |
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
| App icon | PNG at runtime/README + generated multi-size Windows ICO |
| Releases | Windows EXE + portable ZIP + SHA256 checksums |
| CI | Python 3.10–3.14 + real Windows GUI startup smoke test |

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

Real GUI startup smoke test:

```bash
python -m mactrix --smoke-gui
```

Run tests:

```bash
pytest
```

## Windows release

Tagged releases are built by GitHub Actions only after tests and both source/packaged GUI smoke checks succeed. A validated release contains:

```text
MacTrix.exe
MacTrix.exe.sha256
MacTrix-vX.Y.Z-Windows-x64.zip
MacTrix-vX.Y.Z-Windows-x64.zip.sha256
```

The packaged EXE bundles the runtime PNG icon and uses the generated ICO for Windows Explorer/taskbar metadata.

## Project layout

```text
MacTrix/
├─ assets/
│  ├─ mactrix_icon.svg
│  └─ mactrix_icon.png
├─ src/mactrix/
│  ├─ app.py
│  ├─ config.py
│  ├─ generator.py
│  ├─ i18n.py
│  ├─ logging_config.py
│  ├─ resources.py
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

**MacTrix 2.1 — classic workflow restored, modern safety retained.**

</div>
