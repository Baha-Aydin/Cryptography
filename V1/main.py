import random
import string

def karakterleri_olustur():
    # Rastgele karakter seti oluştur
    return string.ascii_letters + string.digits + string.punctuation + " " + "ğüşöçİĞÜŞÖÇ"

def metni_sifrele(metin, anahtar, karakter_seti, info_file):
    # Şifreleme adımlarını kaydet
    sifrelenmis_metin = []
    for i, c in enumerate(metin):
        # Karakterin indeksini bul ve şifrele
        ascii_degeri = karakter_seti.index(c)
        xor_sonucu = (ascii_degeri + anahtar) % len(karakter_seti)
        sifrelenmis_metin.append(karakter_seti[xor_sonucu])
        
        # Adımı info.txt dosyasına kaydet
        adim_metni = f"Adım {i + 1}: '{c}' karakteri Unicode değeri: {ascii_degeri}, XOR Sonucu: {xor_sonucu}"
        with open(info_file, 'a', encoding='utf-8') as file:
            file.write(adim_metni + "\n")

    return ''.join(sifrelenmis_metin)

def karakterleri_bul(sifrelenmis_metin, anahtar, karakter_seti, info_file):
    # Şifrelenmiş metni orijinal karakterlere döndür
    orijinal_karakterler = []
    for i, c in enumerate(sifrelenmis_metin):
        ascii_degeri = karakter_seti.index(c)
        orijinal_ascii = (ascii_degeri - anahtar) % len(karakter_seti)
        orijinal_karakterler.append(karakter_seti[orijinal_ascii])
        
        # Adımı info.txt dosyasına kaydet
        adim_metni = f"Adım {i + 1}: '{c}' karakteri Unicode değeri: {ascii_degeri}, XOR Sonucu: {orijinal_ascii}"
        with open(info_file, 'a', encoding='utf-8') as file:
            file.write(adim_metni + "\n")

    return ''.join(orijinal_karakterler)

info_file = "info.txt"
karakter_seti = karakterleri_olustur()

while True:
    # Kullanıcıdan bit uzunluğunu seçmesini iste
    while True:
        bit_uzunlugu = input("Anahtarın bit uzunluğunu seçin (8, 16, 32): ")
        if bit_uzunlugu in ['8', '16', '32']:
            bit_uzunlugu = int(bit_uzunlugu)
            break
        else:
            print("Geçersiz değer. Lütfen 8, 16 veya 32 girin.")
            print("")

    # Bit uzunluğuna göre rastgele anahtar oluştur
    anahtar = random.getrandbits(bit_uzunlugu) % 256
    print(f"Kullanılan {bit_uzunlugu} bit anahtar: {anahtar}\n")

    # Kullanıcının şifrelenecek metni girmesini iste
    metin = input("Şifrelenecek metni girin: ")

    # Metni şifrele
    sifrelenmis_metin = metni_sifrele(metin, anahtar, karakter_seti, info_file)

    # Ekrana yazdır
    print(f"Bit seviyesinde şifrelenmiş metin: {sifrelenmis_metin}\n")

    # Şifrelenmiş metinden orijinal karakterleri bul
    orijinal_metin = karakterleri_bul(sifrelenmis_metin, anahtar, karakter_seti, info_file)

    # Ekrana yazdır
    print(f"Orijinal metin geri elde edildi: {orijinal_metin}\n")

    # Tüm adımları info.txt dosyasına kaydet
    with open(info_file, 'a', encoding='utf-8') as file:
        file.write(f"Kullanılan anahtar: {anahtar}\n")
        file.write(f"Şifrelenecek metin: {metin}\n")
        file.write(f"Şifrelenmiş metin: {sifrelenmis_metin}\n")
        file.write(f"Orijinal metin geri elde edildi: {orijinal_metin}\n")
        file.write("\n")  # Boşluk ekle

    # Yeni bir işlem yapmak isteyip istemediğini sor
    devam = input("Yeni bir işlem yapmak ister misiniz? (e/h): ").lower()
    if devam != 'e':
        break

input("Çıkmak için bir tuşa basın...")
