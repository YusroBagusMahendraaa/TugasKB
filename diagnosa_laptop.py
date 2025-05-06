import tkinter as tk
from tkinter import messagebox

# Basis gejala dan aturan pakar
GEJALA = [
    ("Kipas berbunyi tidak normal", "kipas_berbunyi"),
    ("Laptop cepat panas", "cepat_panas"),
    ("Sering blue screen", "blue_screen"),
    ("Laptop lambat walau spesifikasi bagus", "lambat"),
    ("Suara aneh dari harddisk", "suara_hdd"),
    ("File sering korup", "file_korup"),
    ("Baterai tidak mengisi", "baterai"),
    ("Laptop mati saat charger dicabut", "mati_charger"),
    ("Tampilan bergaris", "garis"),
    ("Layar berkedip", "berkedip")
]

# Basis aturan kerusakan
ATURAN = {
    "Kipas Rusak": {"kipas_berbunyi", "cepat_panas"},
    "RAM Bermasalah": {"blue_screen", "lambat"},
    "Harddisk Rusak": {"suara_hdd", "file_korup"},
    "Battery Rusak": {"baterai", "mati_charger"},
    "LCD Bermasalah": {"garis", "berkedip"}
}

class PakarApp:
    def __init__(self, master):
        self.master = master
        master.title("Sistem Pakar Deteksi Kerusakan Laptop")

        self.label = tk.Label(master, text="Selamat datang di sistem pakar deteksi kerusakan laptop!", font=("Arial", 12))
        self.label.pack(pady=10)

        self.start_button = tk.Button(master, text="Mulai Diagnosa", command=self.start_diagnosis)
        self.start_button.pack(pady=5)

        self.reset_button = tk.Button(master, text="Reset", command=self.reset, state=tk.DISABLED)
        self.reset_button.pack(pady=5)

        self.gejala_index = 0
        self.jawaban = set()

    def start_diagnosis(self):
        self.start_button.config(state=tk.DISABLED)
        self.reset_button.config(state=tk.NORMAL)
        self.tanya_gejala()

    def tanya_gejala(self):
        if self.gejala_index >= len(GEJALA):
            self.tampilkan_diagnosa()
            return

        teks, kode = GEJALA[self.gejala_index]
        response = messagebox.askyesno("Pertanyaan", f"Apakah {teks}?")
        if response:
            self.jawaban.add(kode)

        self.gejala_index += 1
        self.tanya_gejala()

    def tampilkan_diagnosa(self):
        for kerusakan, syarat in ATURAN.items():
            if syarat.issubset(self.jawaban):
                messagebox.showinfo("Hasil Diagnosa", f"Kerusakan terdeteksi: {kerusakan}")
                return
        messagebox.showinfo("Hasil Diagnosa", "Maaf, kerusakan tidak dapat dikenali.")

    def reset(self):
        self.gejala_index = 0
        self.jawaban.clear()
        self.start_button.config(state=tk.NORMAL)
        self.reset_button.config(state=tk.DISABLED)
        messagebox.showinfo("Reset", "Sistem telah di-reset.")

# Jalankan aplikasi
if __name__ == "__main__":
    root = tk.Tk()
    app = PakarApp(root)
    root.mainloop()
