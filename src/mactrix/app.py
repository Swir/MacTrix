from __future__ import annotations

import logging
import threading
import tkinter as tk
from pathlib import Path
from tkinter import filedialog, messagebox, ttk

from .config import load_settings, save_settings
from .generator import MAX_BATCH, PROFILES, generate_many, resolve_prefix
from .i18n import detect_language, tr
from .storage import load_addresses, save_addresses
from .validation import analyze, canonicalize, is_valid

PREVIEW_LIMIT = 5000
LANGUAGE_LABELS = {"Auto": "auto", "English": "en", "Polski": "pl", "Norsk": "no"}
LANGUAGE_REVERSE = {value: key for key, value in LANGUAGE_LABELS.items()}
SEPARATORS = {":": ":", "-": "-", "None": ""}


class MacTrixApp:
    def __init__(self, root: tk.Tk, logger: logging.Logger | None = None) -> None:
        self.root = root
        self.logger = logger or logging.getLogger("mactrix")
        self.settings = load_settings()
        self.addresses: list[str] = []
        self.profile_label_to_key: dict[str, str] = {}

        configured_language = str(self.settings.get("language", "auto"))
        self.language = detect_language() if configured_language == "auto" else configured_language

        self.count_var = tk.StringVar(value=str(self.settings.get("count", 25)))
        self.profile_var = tk.StringVar()
        self.prefix_var = tk.StringVar()
        self.separator_var = tk.StringVar(value=str(self.settings.get("separator", ":")) or "None")
        self.uppercase_var = tk.BooleanVar(value=bool(self.settings.get("uppercase", True)))
        self.language_var = tk.StringVar(value=LANGUAGE_REVERSE.get(configured_language, "Auto"))
        self.status_var = tk.StringVar(value=tr(self.language, "status_ready"))

        self.root.title(tr(self.language, "title"))
        self.root.geometry("1080x720")
        self.root.minsize(860, 600)
        self.root.configure(bg="#07111f")
        self.root.protocol("WM_DELETE_WINDOW", self._on_close)

        self._configure_style()
        self._build_ui()
        self._refresh_profile_values(initial_key=str(self.settings.get("profile", "generic")))
        self._apply_language()

    def _configure_style(self) -> None:
        style = ttk.Style(self.root)
        try:
            style.theme_use("clam")
        except tk.TclError:
            pass
        style.configure("App.TFrame", background="#07111f")
        style.configure("Card.TFrame", background="#0d1d31", relief="flat")
        style.configure("Header.TLabel", background="#07111f", foreground="#eaf5ff", font=("Segoe UI Semibold", 24))
        style.configure("Sub.TLabel", background="#07111f", foreground="#82a8c9", font=("Segoe UI", 10))
        style.configure("Card.TLabel", background="#0d1d31", foreground="#cfe9ff", font=("Segoe UI", 10))
        style.configure("Hint.TLabel", background="#0d1d31", foreground="#6f97b8", font=("Segoe UI", 9))
        style.configure("Status.TLabel", background="#09182a", foreground="#9acfff", padding=(12, 8), font=("Segoe UI", 9))
        style.configure("Accent.TButton", font=("Segoe UI Semibold", 10), padding=(12, 8), background="#1479d6", foreground="white")
        style.map("Accent.TButton", background=[("active", "#299cff"), ("disabled", "#31475b")])
        style.configure("Ghost.TButton", font=("Segoe UI", 9), padding=(10, 7), background="#132a45", foreground="#d7edff")
        style.map("Ghost.TButton", background=[("active", "#1a3a60")])
        style.configure("TEntry", fieldbackground="#102640", foreground="#eaf5ff", insertcolor="#eaf5ff", padding=7)
        style.configure("TCombobox", fieldbackground="#102640", foreground="#eaf5ff", padding=5)
        style.configure("TSpinbox", fieldbackground="#102640", foreground="#eaf5ff", padding=5)
        style.configure("Treeview", background="#09182a", fieldbackground="#09182a", foreground="#d8eeff", rowheight=27, borderwidth=0)
        style.configure("Treeview.Heading", background="#102640", foreground="#a9d8ff", relief="flat", font=("Segoe UI Semibold", 9))
        style.map("Treeview", background=[("selected", "#165b91")], foreground=[("selected", "white")])
        style.configure("Horizontal.TProgressbar", background="#2aa5ff", troughcolor="#102640", borderwidth=0)

    def _build_ui(self) -> None:
        outer = ttk.Frame(self.root, style="App.TFrame", padding=(22, 18))
        outer.pack(fill="both", expand=True)
        outer.columnconfigure(0, weight=1)
        outer.rowconfigure(2, weight=1)

        header = ttk.Frame(outer, style="App.TFrame")
        header.grid(row=0, column=0, sticky="ew", pady=(0, 16))
        header.columnconfigure(0, weight=1)
        self.title_label = ttk.Label(header, style="Header.TLabel")
        self.title_label.grid(row=0, column=0, sticky="w")
        self.subtitle_label = ttk.Label(header, style="Sub.TLabel")
        self.subtitle_label.grid(row=1, column=0, sticky="w", pady=(3, 0))
        self.language_combo = ttk.Combobox(header, textvariable=self.language_var, values=list(LANGUAGE_LABELS), state="readonly", width=12)
        self.language_combo.grid(row=0, column=1, rowspan=2, sticky="e")
        self.language_combo.bind("<<ComboboxSelected>>", self._change_language)

        controls = ttk.Frame(outer, style="Card.TFrame", padding=16)
        controls.grid(row=1, column=0, sticky="ew", pady=(0, 14))
        for column in range(6):
            controls.columnconfigure(column, weight=1 if column in {0, 1, 2} else 0)

        self.count_label = ttk.Label(controls, style="Card.TLabel")
        self.count_label.grid(row=0, column=0, sticky="w")
        self.profile_label = ttk.Label(controls, style="Card.TLabel")
        self.profile_label.grid(row=0, column=1, sticky="w", padx=(12, 0))
        self.prefix_label = ttk.Label(controls, style="Card.TLabel")
        self.prefix_label.grid(row=0, column=2, sticky="w", padx=(12, 0))
        self.separator_label = ttk.Label(controls, style="Card.TLabel")
        self.separator_label.grid(row=0, column=3, sticky="w", padx=(12, 0))

        self.count_spin = ttk.Spinbox(controls, from_=1, to=MAX_BATCH, textvariable=self.count_var, width=12)
        self.count_spin.grid(row=1, column=0, sticky="ew", pady=(5, 0))
        self.profile_combo = ttk.Combobox(controls, textvariable=self.profile_var, state="readonly", width=18)
        self.profile_combo.grid(row=1, column=1, sticky="ew", padx=(12, 0), pady=(5, 0))
        self.prefix_entry = ttk.Entry(controls, textvariable=self.prefix_var, width=24)
        self.prefix_entry.grid(row=1, column=2, sticky="ew", padx=(12, 0), pady=(5, 0))
        self.separator_combo = ttk.Combobox(controls, textvariable=self.separator_var, values=list(SEPARATORS), state="readonly", width=8)
        self.separator_combo.grid(row=1, column=3, sticky="w", padx=(12, 0), pady=(5, 0))
        self.uppercase_check = ttk.Checkbutton(controls, variable=self.uppercase_var)
        self.uppercase_check.grid(row=1, column=4, padx=(12, 0), pady=(5, 0))
        self.generate_button = ttk.Button(controls, style="Accent.TButton", command=self._generate)
        self.generate_button.grid(row=1, column=5, padx=(12, 0), pady=(5, 0))

        self.about_label = ttk.Label(controls, style="Hint.TLabel", wraplength=1000)
        self.about_label.grid(row=2, column=0, columnspan=6, sticky="w", pady=(12, 0))
        self.progress = ttk.Progressbar(controls, mode="indeterminate")
        self.progress.grid(row=3, column=0, columnspan=6, sticky="ew", pady=(10, 0))

        body = ttk.Frame(outer, style="Card.TFrame", padding=12)
        body.grid(row=2, column=0, sticky="nsew")
        body.rowconfigure(0, weight=1)
        body.columnconfigure(0, weight=1)

        self.tree = ttk.Treeview(body, columns=("index", "mac", "scope"), show="headings", selectmode="extended")
        self.tree.heading("index", text="#")
        self.tree.heading("mac", text="MAC")
        self.tree.heading("scope", text="Type")
        self.tree.column("index", width=70, anchor="e", stretch=False)
        self.tree.column("mac", width=330, anchor="w")
        self.tree.column("scope", width=180, anchor="w")
        self.tree.grid(row=0, column=0, sticky="nsew")
        scrollbar = ttk.Scrollbar(body, orient="vertical", command=self.tree.yview)
        scrollbar.grid(row=0, column=1, sticky="ns")
        self.tree.configure(yscrollcommand=scrollbar.set)

        actions = ttk.Frame(outer, style="App.TFrame")
        actions.grid(row=3, column=0, sticky="ew", pady=(12, 0))
        self.load_button = ttk.Button(actions, style="Ghost.TButton", command=self._load)
        self.load_button.pack(side="left")
        self.save_button = ttk.Button(actions, style="Ghost.TButton", command=self._save)
        self.save_button.pack(side="left", padx=(8, 0))
        self.copy_button = ttk.Button(actions, style="Ghost.TButton", command=self._copy_selected)
        self.copy_button.pack(side="left", padx=(8, 0))
        self.copy_all_button = ttk.Button(actions, style="Ghost.TButton", command=self._copy_all)
        self.copy_all_button.pack(side="left", padx=(8, 0))
        self.sort_button = ttk.Button(actions, style="Ghost.TButton", command=self._sort)
        self.sort_button.pack(side="left", padx=(8, 0))
        self.dedupe_button = ttk.Button(actions, style="Ghost.TButton", command=self._dedupe)
        self.dedupe_button.pack(side="left", padx=(8, 0))
        self.clear_button = ttk.Button(actions, style="Ghost.TButton", command=self._clear)
        self.clear_button.pack(side="right")

        footer = ttk.Frame(outer, style="App.TFrame")
        footer.grid(row=4, column=0, sticky="ew", pady=(10, 0))
        footer.columnconfigure(0, weight=1)
        self.status_label = ttk.Label(footer, textvariable=self.status_var, style="Status.TLabel")
        self.status_label.grid(row=0, column=0, sticky="ew")
        ttk.Label(footer, text="MacTrix v2.0.0  •  by Swir  •  github.com/Swir", style="Sub.TLabel").grid(row=0, column=1, padx=(12, 0))

    def _apply_language(self) -> None:
        self.root.title(tr(self.language, "title"))
        self.title_label.configure(text=tr(self.language, "title"))
        self.subtitle_label.configure(text=tr(self.language, "subtitle"))
        self.count_label.configure(text=tr(self.language, "count"))
        self.profile_label.configure(text=tr(self.language, "profile"))
        self.prefix_label.configure(text=tr(self.language, "prefix"))
        self.separator_label.configure(text=tr(self.language, "separator"))
        self.uppercase_check.configure(text=tr(self.language, "uppercase"))
        self.generate_button.configure(text=tr(self.language, "generate"))
        self.load_button.configure(text=tr(self.language, "load"))
        self.save_button.configure(text=tr(self.language, "save"))
        self.copy_button.configure(text=tr(self.language, "copy"))
        self.copy_all_button.configure(text=tr(self.language, "copy_all"))
        self.sort_button.configure(text=tr(self.language, "sort"))
        self.dedupe_button.configure(text=tr(self.language, "dedupe"))
        self.clear_button.configure(text=tr(self.language, "clear"))
        self.about_label.configure(text=tr(self.language, "about"))
        self._refresh_profile_values(self._selected_profile_key())

    def _change_language(self, _event: object = None) -> None:
        selected = LANGUAGE_LABELS.get(self.language_var.get(), "auto")
        self.language = detect_language() if selected == "auto" else selected
        self._apply_language()
        self.status_var.set(tr(self.language, "status_ready"))

    def _refresh_profile_values(self, initial_key: str | None = None) -> None:
        key = initial_key or "generic"
        labels: list[str] = []
        mapping: dict[str, str] = {}
        for profile_key in PROFILES:
            label = tr(self.language, f"profile_{profile_key}")
            labels.append(label)
            mapping[label] = profile_key
        self.profile_label_to_key = mapping
        self.profile_combo.configure(values=labels)
        wanted = next((label for label, profile_key in mapping.items() if profile_key == key), labels[0])
        self.profile_var.set(wanted)

    def _selected_profile_key(self) -> str:
        return self.profile_label_to_key.get(self.profile_var.get(), "generic")

    def _format_options(self) -> tuple[str, bool]:
        return SEPARATORS.get(self.separator_var.get(), ":"), self.uppercase_var.get()

    def _generate(self) -> None:
        try:
            count = int(self.count_var.get())
            if not 1 <= count <= MAX_BATCH:
                raise ValueError
        except ValueError:
            messagebox.showerror(tr(self.language, "title"), tr(self.language, "invalid_count"), parent=self.root)
            return

        custom_prefix = self.prefix_var.get().strip() or None
        if custom_prefix:
            try:
                resolve_prefix(self._selected_profile_key(), custom_prefix)
            except ValueError:
                messagebox.showerror(tr(self.language, "title"), tr(self.language, "invalid_prefix"), parent=self.root)
                return

        separator, uppercase = self._format_options()
        profile = self._selected_profile_key()
        self.generate_button.state(["disabled"])
        self.progress.start(12)

        def worker() -> None:
            try:
                addresses = generate_many(
                    count,
                    profile,
                    custom_prefix=custom_prefix,
                    separator=separator,
                    uppercase=uppercase,
                )
            except Exception as exc:  # UI boundary
                self.logger.exception("Generation failed")
                self.root.after(0, lambda: self._generation_failed(str(exc)))
                return
            self.root.after(0, lambda: self._generation_finished(addresses))

        threading.Thread(target=worker, daemon=True).start()

    def _generation_failed(self, error: str) -> None:
        self.progress.stop()
        self.generate_button.state(["!disabled"])
        messagebox.showerror(tr(self.language, "title"), error, parent=self.root)

    def _generation_finished(self, addresses: list[str]) -> None:
        self.progress.stop()
        self.generate_button.state(["!disabled"])
        self.addresses = addresses
        self._populate()
        self.status_var.set(tr(self.language, "status_generated", count=len(addresses)))
        self.logger.info("Generated %d addresses", len(addresses))

    def _populate(self) -> None:
        self.tree.delete(*self.tree.get_children())
        for index, address in enumerate(self.addresses[:PREVIEW_LIMIT], start=1):
            try:
                info = analyze(address)
                scope = "local unicast" if info["locally_administered"] and info["unicast"] else "valid MAC"
            except ValueError:
                scope = "invalid"
            self.tree.insert("", "end", values=(index, address, scope))
        if len(self.addresses) > PREVIEW_LIMIT:
            self.status_var.set(f"{self.status_var.get()} • preview {PREVIEW_LIMIT}/{len(self.addresses)}")

    def _copy_selected(self) -> None:
        values = [self.tree.item(item, "values")[1] for item in self.tree.selection()]
        if values:
            self._copy(values)

    def _copy_all(self) -> None:
        if self.addresses:
            self._copy(self.addresses)

    def _copy(self, values: list[str]) -> None:
        self.root.clipboard_clear()
        self.root.clipboard_append("\n".join(values))
        self.status_var.set(f"{tr(self.language, 'copied')}: {len(values)}")

    def _load(self) -> None:
        path = filedialog.askopenfilename(
            parent=self.root,
            filetypes=[("Supported", "*.txt *.csv *.json"), ("Text", "*.txt"), ("CSV", "*.csv"), ("JSON", "*.json"), ("All", "*.*")],
        )
        if not path:
            return
        try:
            addresses, invalid = load_addresses(path)
            separator, uppercase = self._format_options()
            self.addresses = [canonicalize(address, separator=separator, uppercase=uppercase) for address in addresses]
            self._populate()
            self.status_var.set(tr(self.language, "status_loaded", count=len(self.addresses), invalid=invalid))
            self.logger.info("Imported %d addresses from %s; %d invalid", len(self.addresses), path, invalid)
        except Exception as exc:
            self.logger.exception("Import failed")
            messagebox.showerror(tr(self.language, "title"), tr(self.language, "file_error", error=exc), parent=self.root)

    def _save(self) -> None:
        if not self.addresses:
            messagebox.showinfo(tr(self.language, "title"), tr(self.language, "nothing"), parent=self.root)
            return
        path = filedialog.asksaveasfilename(
            parent=self.root,
            defaultextension=".txt",
            filetypes=[("Text", "*.txt"), ("CSV", "*.csv"), ("JSON", "*.json")],
        )
        if not path:
            return
        try:
            save_addresses(Path(path), self.addresses)
            self.status_var.set(tr(self.language, "status_saved", count=len(self.addresses)))
            self.logger.info("Exported %d addresses to %s", len(self.addresses), path)
        except Exception as exc:
            self.logger.exception("Export failed")
            messagebox.showerror(tr(self.language, "title"), tr(self.language, "file_error", error=exc), parent=self.root)

    def _sort(self) -> None:
        self.addresses.sort()
        self._populate()

    def _dedupe(self) -> None:
        self.addresses = list(dict.fromkeys(self.addresses))
        self._populate()

    def _clear(self) -> None:
        self.addresses.clear()
        self._populate()
        self.status_var.set(tr(self.language, "status_ready"))

    def _on_close(self) -> None:
        selected_language = LANGUAGE_LABELS.get(self.language_var.get(), "auto")
        separator, _ = self._format_options()
        settings = {
            "language": selected_language,
            "profile": self._selected_profile_key(),
            "separator": separator,
            "uppercase": self.uppercase_var.get(),
            "count": int(self.count_var.get()) if self.count_var.get().isdigit() else 25,
        }
        try:
            save_settings(settings)
        except OSError:
            self.logger.exception("Could not save settings")
        self.root.destroy()


def run() -> None:
    from .logging_config import configure_logging

    root = tk.Tk()
    MacTrixApp(root, configure_logging())
    root.mainloop()
