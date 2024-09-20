import random
import os

# 256-bit kaydırma ve XOR işlemi
def bit_manipulasyonu_256(metin_bloku, anahtar_bloku, info_file):
    sifrelenmis_blok = []
    
    # Her karakteri anahtar ile XOR işlemi uygula ve kaydır
    for i, c in enumerate(metin_bloku):
        # Unicode karakteri (her karakteri 16-bit olarak alıyoruz)
        unicode_degeri = ord(c)
        
        # XOR işlemi anahtarın ilgili kısmı ile
        xor_karakter = unicode_degeri ^ ord(anahtar_bloku[i % len(anahtar_bloku)])
        
        # 256 bitlik kaydırma: Hem sola hem sağa kaydırma
        bit_kaydirma = ((xor_karakter << (i + 1)) | (xor_karakter >> (16 - (i + 1)))) & 0xFFFF
        
        # Şifrelenmiş karakteri ekle
        sifrelenmis_blok.append(chr(bit_kaydirma))

        # Adımı info.txt dosyasına kaydet
        adim_metni = f"Adım {i + 1}: '{c}' karakteri Unicode değeri: {unicode_degeri}, XOR Sonucu: {xor_karakter}, Kaydırma Sonucu: {bit_kaydirma}"
        with open(info_file, 'a', encoding='utf-8') as file:
            file.write(adim_metni + "\n")
    
    return ''.join(sifrelenmis_blok)

# Bit manipülasyonunu geri alma işlemi (256-bit çözümleme)
def bit_manipulasyonunu_geri_al_256(sifrelenmis_blok, anahtar_bloku,info_file):
    desifrelenmis_blok = []
    
    # Her karakteri anahtar ile XOR işlemini geri al ve kaydırmayı tersine çevir
    for i, c in enumerate(sifrelenmis_blok):
        unicode_degeri = ord(c)
        
        # Kaydırmayı geri al
        geri_kaydirma = ((unicode_degeri >> (i + 1)) | (unicode_degeri << (16 - (i + 1)))) & 0xFFFF
        
        # XOR işlemini geri alma
        xor_karakter = geri_kaydirma ^ ord(anahtar_bloku[i % len(anahtar_bloku)])
        
        # Orijinal karakteri ekle
        desifrelenmis_blok.append(chr(xor_karakter))

        # Adımı info.txt dosyasına kaydet
        adim_metni = f"Adım {i + 1}: '{c}' karakteri Unicode değeri: {unicode_degeri}, Geri Kaydırma Sonucu: {geri_kaydirma}, XOR Sonucu: {xor_karakter}"
        with open(info_file, 'a', encoding='utf-8') as file:
            file.write(adim_metni + "\n")
    
    return ''.join(desifrelenmis_blok)

# Metni şifreleme işlemi (256-bit)
def metni_sifrele_256(metin, anahtar,info_file):
    # Metni 256 bitlik bloklara bölelim (her blok 16 karakter)
    blok_boyutu = 16
    sifrelenmis_metin = ''
    
    # Her blok için şifreleme
    for i in range(0, len(metin), blok_boyutu):
        metin_bloku = metin[i:i + blok_boyutu]
        sifrelenmis_metin += bit_manipulasyonu_256(metin_bloku, anahtar,info_file)
    
    return sifrelenmis_metin

# Metni şifre çözme işlemi (256-bit)
def metni_desifrele_256(sifrelenmis_metin, anahtar,info_file):
    # 256 bitlik bloklara ayır
    blok_boyutu = 16
    desifrelenmis_metin = ''
    
    # Her blok için çözme
    for i in range(0, len(sifrelenmis_metin), blok_boyutu):
        sifrelenmis_blok = sifrelenmis_metin[i:i + blok_boyutu]
        desifrelenmis_metin += bit_manipulasyonunu_geri_al_256(sifrelenmis_blok, anahtar,info_file)
    
    return desifrelenmis_metin

# Rastgele 256-bit anahtar oluşturma (16 karakter = 128 bit, 32 karakter = 256 bit)
def rastgele_anahtar_olustur(uzunluk=32):
    karakter_seti = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*()-_=+[]{}|;:",.<>?/`~'
    return ''.join(random.choice(karakter_seti) for _ in range(uzunluk))

# Kullanım
info_file = "info.txt"
while True:
    metin = input("Şifrelenecek metni girin (Çıkmak için 'exit' yazın): ")
    if metin.lower() == 'exit' or metin.lower() == 'çıkış':
        break

    anahtar = rastgele_anahtar_olustur(32)  # 256-bit uzunluğunda bir anahtar
    
    # Metni şifrele
    sifrelenmis_metin = metni_sifrele_256(metin, anahtar, info_file)
    print(f"Şifrelenmiş metin: {sifrelenmis_metin}")
    with open(info_file, 'a', encoding='utf-8') as file:
        file.write(f"Şifrelenmiş metin: {sifrelenmis_metin}\n")

    # Şifreyi çöz
    desifrelenmis_metin = metni_desifrele_256(sifrelenmis_metin, anahtar, info_file)
    print(f"Desifrelenmiş metin: {desifrelenmis_metin}")
    with open(info_file, 'a', encoding='utf-8') as file:
        file.write(f"Desifrelenmiş metin: {desifrelenmis_metin}\n")