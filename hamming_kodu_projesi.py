import tkinter as tk
from tkinter import messagebox
import random

# Bellek depolama
bellek_depolama = {}

# Hamming Kodu Fonksiyonları (aşağıda tanımlandığı gibi)
def parite_bitleri_sayisini_hesapla(veri_bit_uzunlugu):
    r = 0
    while (2 ** r) < (veri_bit_uzunlugu + r + 1):
        r += 1
    return r

def hamming_kodu_olustur(veri_bitleri):
    m = len(veri_bitleri)
    r = parite_bitleri_sayisini_hesapla(m)
    toplam_uzunluk = m + r

    hamming_kodu = ['0'] * toplam_uzunluk

    # Veri bitlerini uygun konumlara yerleştir
    j = 0
    for i in range(1, toplam_uzunluk + 1):
        if (i & (i - 1)) == 0:
            continue
        hamming_kodu[i - 1] = veri_bitleri[j]
        j += 1

    # Parite bitlerini hesapla
    for i in range(r):
        parite_konumu = 2 ** i
        parite_toplami = 0
        for j in range(1, toplam_uzunluk + 1):
            if j & parite_konumu:
                parite_toplami += int(hamming_kodu[j - 1])
        hamming_kodu[parite_konumu - 1] = str(parite_toplami % 2)

    return ''.join(hamming_kodu)

def hata_olustur(hamming_kodu):
    hata_konumu = random.randint(0, len(hamming_kodu) - 1)
    hamming_kodu = list(hamming_kodu)
    hamming_kodu[hata_konumu] = '0' if hamming_kodu[hata_konumu] == '1' else '1'
    return ''.join(hamming_kodu), hata_konumu

def hatayi_tespit_et(hamming_kodu):
    n = len(hamming_kodu)
    r = parite_bitleri_sayisini_hesapla(n)
    hata_konumu = 0

    for i in range(r):
        parite_konumu = 2 ** i
        parite_toplami = 0
        for j in range(1, n + 1):
            if j & parite_konumu:
                parite_toplami += int(hamming_kodu[j - 1])
        if parite_toplami % 2 != 0:
            hata_konumu += parite_konumu

    return hata_konumu - 1 if hata_konumu != 0 else -1

def hatayi_duzelt(hamming_kodu, hata_konumu):
    if hata_konumu != -1:
        hamming_kodu = list(hamming_kodu)
        hamming_kodu[hata_konumu] = '0' if hamming_kodu[hata_konumu] == '1' else '1'
    return ''.join(hamming_kodu)

def rastgele_veri_olustur(bit_uzunlugu):
    return ''.join(random.choice('01') for _ in range(bit_uzunlugu))

def rastgele_veri_gui_olustur():
    bit_uzunlugu = int(bit_uzunlugu_var.get())
    rastgele_veri = rastgele_veri_olustur(bit_uzunlugu)
    veri_girisi.delete(0, tk.END)
    veri_girisi.insert(0, rastgele_veri)

def rastgele_hata_gui_olustur():
    veri = veri_girisi.get()
    if not veri:
        messagebox.showerror("Hata", "Bozulacak veri yok!")
        return
    bozuk_veri, hata_konumu = hata_olustur(veri)
    veri_girisi.delete(0, tk.END)
    veri_girisi.insert(0, bozuk_veri)
    hata_konumu_var.set(f"Hata konumu: {hata_konumu + 1}")

def kodu_olustur():
    veri = veri_girisi.get()
    if len(veri) not in [8, 16, 32]:
        messagebox.showerror("Hata", "Veri uzunluğu 8, 16 veya 32 bit olmalıdır.")
        return
    hamming_kodu = hamming_kodu_olustur(veri)
    hamming_kodu_var.set(hamming_kodu)
    hamming_kodu_etiketi.config(text=f"Hamming Kodu: {hamming_kodu}")

def bellege_kaydet():
    veri = veri_girisi.get()
    if len(veri) not in [8, 16, 32]:
        messagebox.showerror("Hata", "Veri uzunluğu 4, 8 veya 16 bit olmalıdır.")
        return
    hamming_kodu = hamming_kodu_olustur(veri)
    bellek_depolama[veri] = hamming_kodu
    hamming_kodu_etiketi.config(text=f"Belleğe Kaydedildi: {hamming_kodu}")

def hatayi_olustur():
    hamming_kodu = hamming_kodu_var.get()
    if not hamming_kodu:
        messagebox.showerror("Hata", "Bozulacak Hamming Kodu yok!")
        return
    bozuk_kod, hata_konumu = hata_olustur(hamming_kodu)
    bozuk_kod_var.set(bozuk_kod)
    hata_konumu_var.set(f"Hata konumu: {hata_konumu + 1}")
    bozuk_kod_etiketi.config(text=f"Bozuk Kod: {bozuk_kod}")
    hata_konumu_etiketi.config(text=f"Hata konumu: {hata_konumu + 1}")

def hatayi_tespit_ve_duzelt():
    bozuk_kod = bozuk_kod_var.get()
    if not bozuk_kod:
        messagebox.showerror("Hata", "Düzeltilecek bozuk kod yok!")
        return
    hata_konumu = hatayi_tespit_et(bozuk_kod)
    if hata_konumu == -1:
        duzeltilmis_kod_etiketi.config(text="Hata yok.")
    else:
        duzeltilmis_kod = hatayi_duzelt(bozuk_kod, hata_konumu)
        duzeltilmis_kod_var.set(duzeltilmis_kod)
        duzeltilmis_kod_etiketi.config(text=f"Düzeltilmiş Kod: {duzeltilmis_kod}")
        hata_konumu_etiketi.config(text=f"Hata düzeltilen konum: {hata_konumu + 1}")

def bellek_goster():
    bellek_icerik = "\n".join([f"{k}: {v}" for k, v in bellek_depolama.items()])
    messagebox.showinfo("Bellek Depolama", bellek_icerik)

# Ana uygulama penceresini ayarlama
root = tk.Tk()
root.title("Hamming Kodu Simülatörü")
root.configure(bg="#00897B")

# Değişkenler
veri_girisi = tk.Entry(root)
hamming_kodu_var = tk.StringVar()
bozuk_kod_var = tk.StringVar()
duzeltilmis_kod_var = tk.StringVar()
hata_konumu_var = tk.StringVar()
bit_uzunlugu_var = tk.StringVar(value="8")

# GUI Düzeni
header_frame = tk.Frame(root, bg="#00897B")
header_frame.pack(pady=10)

data_frame = tk.Frame(root, bg="#00897B")
data_frame.pack(pady=10)

bit_length_frame = tk.Frame(root, bg="#00897B")
bit_length_frame.pack(pady=10)

button_frame = tk.Frame(root, bg="#00897B")
button_frame.pack(pady=10)

result_frame = tk.Frame(root, bg="#00897B")
result_frame.pack(pady=10)

# Başlık
tk.Label(header_frame, text="Hamming Kodu Simülatörü", font=("Helvetica", 16, "bold"), bg="#00897B", fg="white").pack()

# Veri Girişi Bölümü
veri_girisi_etiketi = tk.Label(data_frame, text="Veri Bitlerini Girin:", bg="#00897B", fg="white")
veri_girisi_etiketi.pack(side=tk.LEFT, padx=5)
veri_girisi.pack( padx=5)

# Bit Uzunluğu ve Rastgele Veri Oluşturma
tk.Label(bit_length_frame, text="Bit Uzunluğu:", bg="#00897B", fg="white").pack(side=tk.LEFT, padx=5)
tk.Entry(bit_length_frame, textvariable=bit_uzunlugu_var).pack(side=tk.LEFT, padx=5)
tk.Button(bit_length_frame, text="Rastgele Veri Oluştur", command=rastgele_veri_gui_olustur).pack(side=tk.LEFT, padx=5)

# Düğme Bölümü
tk.Button(button_frame, text="Hamming Kodu Oluştur", command=kodu_olustur).pack(side=tk.LEFT, padx=5)
tk.Button(button_frame, text="Belleğe Kaydet", command=bellege_kaydet).pack(side=tk.LEFT, padx=5)
tk.Button(button_frame, text="Rastgele Hata Oluştur", command=rastgele_hata_gui_olustur).pack(side=tk.LEFT, padx=5)
tk.Button(button_frame, text="Hamming Kodunda Hata Oluştur", command=hatayi_olustur).pack(side=tk.LEFT, padx=5)
tk.Button(button_frame, text="Hatayı Tespit ve Düzelt", command=hatayi_tespit_ve_duzelt).pack(side=tk.LEFT, padx=5)
tk.Button(button_frame, text="Bellek Depolamayı Göster", command=bellek_goster).pack(side=tk.LEFT, padx=5)

# Sonuçları Gösterme Alanı
tk.Label(result_frame, text="Sonuçlar:", font=("Helvetica", 14, "bold"), bg="#00897B", fg="white").pack()
hamming_kodu_etiketi = tk.Label(result_frame, text="", font=("Helvetica", 12), bg="#00897B", fg="white")
hamming_kodu_etiketi.pack()
bozuk_kod_etiketi = tk.Label(result_frame, text="", font=("Helvetica", 12), bg="#00897B", fg="white")
bozuk_kod_etiketi.pack()
duzeltilmis_kod_etiketi = tk.Label(result_frame, text="", font=("Helvetica", 12), bg="#00897B", fg="white")
duzeltilmis_kod_etiketi.pack()
hata_konumu_etiketi = tk.Label(result_frame, text="", font=("Helvetica", 12), bg="#00897B", fg="white")
hata_konumu_etiketi.pack()

root.mainloop()

