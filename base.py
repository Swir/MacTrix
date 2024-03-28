import random
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from ttkthemes import ThemedTk

class MACGenerator:
    def __init__(self):
        self.window = ThemedTk(theme="radiance")
        self.window.title("Generator adresów MAC")
        self.window.resizable(False, False)

        self.style = ttk.Style()
        self.style.theme_use("clam")  

        self.device_types = {
            "Komputer": "00:1A:79",
            "Telefon": "00:1A:BC",
            "Router": "00:1A:dE",
            "Inne": "00:1A:EF"
        }

        # Ustawienie stylu ramki bez obramowania
        self.style.configure("Background.TFrame", background="#0074D9", borderwidth=0)

        self.create_widgets()

    def create_widgets(self):
        self.frame = ttk.Frame(self.window, padding="20", style="Background.TFrame")
        self.frame.grid(row=0, column=0, padx=20, pady=20)

        self.num_addresses_label = ttk.Label(self.frame, text="Liczba adresów MAC:")
        self.num_addresses_label.grid(row=0, column=0, pady=10)

        self.num_addresses_entry = ttk.Entry(self.frame)
        self.num_addresses_entry.grid(row=0, column=1, pady=10)

        self.device_type_label = ttk.Label(self.frame, text="Typ urządzenia:")
        self.device_type_label.grid(row=1, column=0, pady=10)

        self.device_type_combobox = ttk.Combobox(self.frame, values=list(self.device_types.keys()))
        self.device_type_combobox.grid(row=1, column=1, pady=10)

        self.generate_mac_button = ttk.Button(self.frame, text="Generuj adresy MAC", command=self.generate_mac_button_click)
        self.generate_mac_button.grid(row=2, column=0, columnspan=2, pady=20)

        self.progress_bar = ttk.Progressbar(self.frame, orient="horizontal", mode="determinate", length=200)
        self.progress_bar.grid(row=3, column=0, columnspan=2, pady=10)

        self.progress_label = ttk.Label(self.frame, text="Generowanie...")
        self.progress_label.grid(row=4, column=0, columnspan=2, pady=10)

        self.mac_listbox = tk.Listbox(self.frame, width=40, height=10, font=("Courier New", 11))
        self.mac_listbox.grid(row=5, column=0, columnspan=2, pady=10)

        self.scrollbar = ttk.Scrollbar(self.frame, orient="vertical", command=self.mac_listbox.yview)
        self.scrollbar.grid(row=5, column=2, pady=10, sticky="ns")
        self.mac_listbox.configure(yscrollcommand=self.scrollbar.set)

        self.save_button = ttk.Button(self.frame, text="Zapisz do pliku", command=self.save_button_click)
        self.save_button.grid(row=6, column=0, columnspan=2, pady=10)

        self.load_button = ttk.Button(self.frame, text="Wczytaj z pliku", command=self.load_button_click)
        self.load_button.grid(row=7, column=0, columnspan=2, pady=10)

        self.sort_button = ttk.Button(self.frame, text="Sortuj", command=self.sort_button_click)
        self.sort_button.grid(row=8, column=0, columnspan=2, pady=10)

        footer_frame = ttk.Frame(self.window)
        footer_frame.grid(row=1, column=0, pady=10)
        self.footer_label = ttk.Label(footer_frame, text="Mac Generator By Swir Swirtvtram", font=("Arial", 8))
        self.footer_label.pack()

        # Konfiguracja stylu przycisków
        self.style.configure("TButton", background="#001f3f", foreground="white", font=("Helvetica", 12))
        self.style.map("TButton", background=[('active', '#39CCCC')])

        # Konfiguracja stylu etykiet
        self.style.configure("TLabel", background="#0074D9", foreground="white", font=("Helvetica", 12))

        # Konfiguracja stylu pola wprowadzania tekstu
        self.style.configure("TEntry", fieldbackground="#ffffff", foreground="black", font=("Helvetica", 12))

        # Konfiguracja stylu paska postępu
        self.style.map("TProgressbar", background=[('active', '#FFDC00')])

    def generate_mac_address(self, device_type):
        prefix = self.device_types[device_type]
        mac = [int(x, 16) for x in prefix.split(":")]
        mac += [random.randint(0x00, 0xff) for _ in range(3)]
        mac_address = ':'.join(['{:02X}'.format(x) for x in mac])
        return mac_address

    def generate_mac_addresses(self, num_addresses, device_type):
        mac_addresses = []
        for i in range(num_addresses):
            progress = (i + 1) * 100 / num_addresses
            self.progress_bar["value"] = progress
            self.progress_label.config(text="Generowanie: {:.1f}%".format(progress))
            mac_address = self.generate_mac_address(device_type)
            mac_addresses.append(mac_address)
            self.window.update_idletasks()
        self.progress_bar["value"] = 0
        self.progress_label.config(text="Generowanie zakończone!")
        return mac_addresses

    def generate_mac_button_click(self):
        try:
            num_addresses = int(self.num_addresses_entry.get())
            device_type = self.device_type_combobox.get()

            if num_addresses <= 0:
                raise ValueError("Liczba adresów MAC musi być większa od zera.")

            if device_type not in self.device_types:
                raise ValueError("Wybrano nieprawidłowy typ urządzenia.")

            self.mac_listbox.delete(0, tk.END)
            self.save_button.config(state=tk.DISABLED)
            self.progress_label.config(text="Generowanie...")
            self.progress_bar["value"] = 0
            self.progress_bar.start()

            mac_addresses = self.generate_mac_addresses(num_addresses, device_type)

            self.progress_bar.stop()

            for mac_address in mac_addresses:
                self.mac_listbox.insert(tk.END, mac_address)

            self.save_button.config(state=tk.NORMAL)

            if len(set(mac_addresses)) != len(mac_addresses):
                messagebox.showwarning("Uwaga", "Wygenerowane adresy MAC zawierają powtórzenia.")

        except ValueError as e:
            messagebox.showerror("Błąd", str(e))

    def save_button_click(self):
        try:
            file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Plik tekstowy", "*.txt"), ("Plik CSV", "*.csv")])

            if not file_path:
                return

            with open(file_path, "w") as file:
                for i in range(self.mac_listbox.size()):
                    file.write(self.mac_listbox.get(i) + "\n")

            messagebox.showinfo("Sukces", "Adresy MAC zostały zapisane do pliku: " + file_path)

        except Exception as e:
            messagebox.showerror("Błąd", "Wystąpił błąd podczas zapisywania do pliku.")

    def load_button_click(self):
        try:
            file_path = filedialog.askopenfilename(filetypes=[("Plik tekstowy", "*.txt"), ("Plik CSV", "*.csv")])

            if not file_path:
                return

            with open(file_path, "r") as file:
                mac_addresses = file.read().splitlines()

            self.mac_listbox.delete(0, tk.END)

            for mac_address in mac_addresses:
                self.mac_listbox.insert(tk.END, mac_address)

            self.save_button.config(state=tk.NORMAL)

        except Exception as e:
            messagebox.showerror("Błąd", "Wystąpił błąd podczas wczytywania pliku.")

    def sort_button_click(self):
        mac_addresses = list(self.mac_listbox.get(0, tk.END))
        mac_addresses.sort()
        self.mac_listbox.delete(0, tk.END)
        for mac_address in mac_addresses:
            self.mac_listbox.insert(tk.END, mac_address)

    def run(self):
        self.window.mainloop()

if __name__ == "__main__":
    mac_generator = MACGenerator()
    mac_generator.run()
