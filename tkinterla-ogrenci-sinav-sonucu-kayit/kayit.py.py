import tkinter as tk
from tkinter import ttk
import os

class BilgiApp(tk.Tk):
    def __init__(self):
        super().__init__()
        
        self.title("Kayıt Formu")
        self.geometry("600x400")

        tk.Label(self, text="Adınız:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        tk.Label(self, text="Soyadınız:").grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
        tk.Label(self, text="Yaşınız:").grid(row=2, column=0, sticky=tk.W, padx=5, pady=5)
        tk.Label(self, text="Cinsiyetiniz:").grid(row=3, column=0, sticky=tk.W, padx=5, pady=5)
        tk.Label(self, text="Vize:").grid(row=4, column=0, sticky=tk.W, padx=5, pady=5)
        tk.Label(self, text="Final:").grid(row=5, column=0, sticky=tk.W, padx=5, pady=5)
        tk.Label(self, text="Sonuç:").grid(row=6, column=0, sticky=tk.W, padx=5, pady=5)

        self.edtAd = tk.Entry(self)
        self.edtAd.grid(row=0, column=1, padx=5, pady=5)
        
        self.edtSoyad = tk.Entry(self)
        self.edtSoyad.grid(row=1, column=1, padx=5, pady=5)
        
        self.spnYas = tk.Spinbox(self, from_=0, to=200, width=5)
        self.spnYas.grid(row=2, column=1, padx=5, pady=5)
        
        self.cmbCinsiyet = ttk.Combobox(self, values=["Erkek", "Kadın"], state="readonly")
        self.cmbCinsiyet.current(0)
        self.cmbCinsiyet.grid(row=3, column=1, padx=5, pady=5)
        
        self.edtVize = tk.Entry(self)
        self.edtVize.grid(row=4, column=1, padx=5, pady=5)
        
        self.edtFinal = tk.Entry(self)
        self.edtFinal.grid(row=5, column=1, padx=5, pady=5)

        self.lblSonuc = tk.Label(self, text="", font=("Arial", 12))
        self.lblSonuc.grid(row=6, column=1, sticky=tk.W, padx=5, pady=5)

        self.btnOnceki = tk.Button(self, text="Önceki", command=self.btnOncekiTikla, width=20, height=1)
        self.btnOnceki.grid(row=7, column=1, pady=5)

        self.btnSonraki = tk.Button(self, text="Sonraki", command=self.btnSonrakiTikla, width=20, height=1)
        self.btnSonraki.grid(row=8, column=1, pady=5)

        self.btnYeni = tk.Button(self, text="Yeni", command=self.btnYeniTikla, width=20, height=1)
        self.btnYeni.grid(row=9, column=1, pady=5)

        self.btnKaydet = tk.Button(self, text="Kaydet", command=self.btnKaydetTikla, width=20, height=1)
        self.btnKaydet.grid(row=10, column=1, pady=5)

        self.btnSil = tk.Button(self, text="Sil", command=self.btnSilTikla, width=20, height=1)
        self.btnSil.grid(row=11, column=1, pady=5)

        self.dosyaPath = "veriler1.txt"
        self.aktifSatir = 0
        self.dosyayiOku()
        self.kayitGoster()

    def dosyayiOku(self):
        if not os.path.exists(self.dosyaPath):
            open(self.dosyaPath, "w").close()
        with open(self.dosyaPath, "r", encoding="utf-8") as dosya:
            self.tumSatirlar = dosya.readlines()
        self.satirSayisi = len(self.tumSatirlar)
        self.kayitModu = 'g' if self.satirSayisi > 0 else 'y'
        
    def dosyayaYaz(self):
        with open(self.dosyaPath, "w", encoding="utf-8") as dosya:
            dosya.writelines(self.tumSatirlar)

    def btnOncekiTikla(self):
        if self.aktifSatir > 0:
            self.aktifSatir -= 1
            self.kayitGoster()

    def btnSonrakiTikla(self):
        if self.aktifSatir < self.satirSayisi - 1:
            self.aktifSatir += 1
            self.kayitGoster()

    def btnYeniTikla(self):
        self.edtAd.delete(0, tk.END)
        self.edtSoyad.delete(0, tk.END)
        self.spnYas.delete(0, tk.END)
        self.spnYas.insert(0, 20)
        self.cmbCinsiyet.current(0)
        self.edtVize.delete(0, tk.END)
        self.edtFinal.delete(0, tk.END)
        self.lblSonuc.config(text="", fg="black")
        self.kayitModu = 'y'

    def btnKaydetTikla(self):
        vize = int(self.edtVize.get().strip()) if self.edtVize.get().strip().isdigit() else 0
        final = int(self.edtFinal.get().strip()) if self.edtFinal.get().strip().isdigit() else 0
        sonuc = "G" if (vize + final) / 2 >= 50 else "K"
        renk = "green" if sonuc == "G" else "red"
        self.lblSonuc.config(text=sonuc, fg=renk)
        satir = f"{self.edtAd.get().strip():20}|{self.edtSoyad.get().strip():20}|{self.spnYas.get():3}|{self.cmbCinsiyet.get():5}|{vize:3}|{final:3}|{sonuc}\n"
        if self.kayitModu == 'g':
            self.tumSatirlar[self.aktifSatir] = satir
        else:
            self.tumSatirlar.append(satir)
            self.kayitModu = 'g'
            self.aktifSatir = self.satirSayisi
        self.dosyayaYaz()
        self.dosyayiOku()

    def kayitGoster(self):
        if self.satirSayisi > 0:
            satir = self.tumSatirlar[self.aktifSatir]
            kayit = satir.strip().split('|')
            self.edtAd.delete(0, tk.END)
            self.edtAd.insert(0, kayit[0].strip())
            self.edtSoyad.delete(0, tk.END)
            self.edtSoyad.insert(0, kayit[1].strip())
            self.spnYas.delete(0, tk.END)
            self.spnYas.insert(0, kayit[2].strip())
            self.cmbCinsiyet.set(kayit[3].strip())
            self.edtVize.delete(0, tk.END)
            self.edtVize.insert(0, kayit[4].strip())
            self.edtFinal.delete(0, tk.END)
            self.edtFinal.insert(0, kayit[5].strip())
            sonuc = kayit[6].strip()
            renk = "green" if sonuc == "G" else "red"
            self.lblSonuc.config(text=sonuc, fg=renk)
        else:
            self.btnYeniTikla()

    def btnSilTikla(self):
        if self.satirSayisi > 0:
            self.tumSatirlar.pop(self.aktifSatir)
            self.dosyayaYaz()
            self.dosyayiOku()
            self.aktifSatir = 0
            self.kayitGoster()

if __name__ == "__main__":
    app = BilgiApp()
    app.mainloop()
