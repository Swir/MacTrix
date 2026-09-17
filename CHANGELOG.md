# Changelog

All notable changes to MacTrix are documented here.

## [2.0.0] - 2026-09-17

### Added
- Complete package-based architecture under `src/mactrix`.
- Modern dark-blue responsive Tkinter/ttk desktop UI.
- Standards-safe locally administered unicast MAC generation.
- Generic, Desktop, Mobile, Router and IoT synthetic profiles.
- Optional 3-byte custom prefix with automatic local/unicast normalization.
- Batch generation from 1 to 100,000 unique addresses.
- Colon, dash and compact output formatting plus case selection.
- TXT, CSV and JSON import/export.
- MAC normalization, validation and address-scope analysis.
- English, Polish and Norwegian UI with system-language detection.
- Persistent per-user settings and rotating application logs.
- Original MacTrix SVG application icon and Windows ICO build tool.
- Automated tests across Python 3.10-3.14 and Windows smoke testing.
- Automated Windows EXE, portable ZIP and SHA256 release workflow.
- Packaged-app smoke test before release publication.

### Changed
- Replaced the old vendor-like hard-coded prefixes with clearly synthetic local namespaces.
- Replaced the old `ttkthemes` dependency with a dependency-free runtime based on standard Tkinter/ttk.
- Large batches now keep all results for export while limiting the visible preview for UI responsiveness.

### Removed
- Removed the old single-file `base.py` prototype.

## Legacy

The original Windows archive was published in 2024 as `MacTrixWIN`.
