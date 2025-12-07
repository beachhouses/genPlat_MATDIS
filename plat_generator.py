import itertools
import os
import random
from datetime import datetime
import sys

# ===== Warna gradasi cokelat =====
RESET = "\033[0m"
BOLD = "\033[1m"
LIGHT_BROWN = "\033[38;5;180m"
DARK_BROWN = "\033[38;5;94m"
COPPER = "\033[38;5;136m"
GOLD = "\033[38;5;220m"
RED = "\033[91m"
GREEN = "\033[92m"

# ===== Validasi plat custom =====
def validate_plate(prefix, number, suffix):
    vowels = "AEIOU"
    if not (1 <= len(prefix) <= 3 and prefix.isalpha() and prefix.isupper()):
        return False, "Huruf awal harus 1–3 huruf besar (A–Z)."
    if not (number.isdigit() and 1 <= len(number) <= 4):
        return False, "Angka harus 1–4 digit."
    if number[0] == "0":
        return False, "Angka tidak boleh dimulai dengan 0."
    if int(number) % 2 != 0:
        return False, "Angka harus genap."
    if not (1 <= len(suffix) <= 2 and suffix.isalpha() and suffix.isupper()):
        return False, "Huruf akhir harus 1–2 huruf besar."
    if any(v in suffix for v in vowels):
        return False, "Huruf akhir tidak boleh mengandung huruf vokal."
    plate = f"{prefix} {number} {suffix}"
    if len(plate) > 10:
        return False, "Panjang total plat tidak boleh melebihi 10 karakter."
    return True, plate


# ===== Generator kombinasi random terbatas =====
def generate_license_plates(start_letter='B', max_combinations=50):
    consonants = [ch for ch in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ' if ch not in 'AEIOU']
    results = set()

    while len(results) < max_combinations:
        extra_letters_len = random.choice([0, 1, 2])
        extra_letters = ''.join(random.choices('ABCDEFGHIJKLMNOPQRSTUVWXYZ', k=extra_letters_len))
        prefix = (start_letter.upper() + extra_letters)[:3]

        num = random.randint(2, 9998)
        if num % 2 != 0:
            num += 1
        num_str = str(num)
        if num_str[0] == "0":
            continue

        suffix_len = random.choice([1, 2])
        suffix = ''.join(random.choices(consonants, k=suffix_len))

        plate = f"{prefix} {num_str} {suffix}"
        if len(plate) <= 10:
            results.add((prefix, num_str, suffix, plate))

    return list(results)


# ===== Tabel =====
def tampilkan_tabel(data, start_letter):
    os.makedirs("output", exist_ok=True)
    tanggal = datetime.now().strftime("%Y%m%d")
    filename = f"output/daftar_plat_valid_{start_letter}_{tanggal}.txt"

    print(f"\n{BOLD}{COPPER}╔══════════════════════════════════════════════════════════════════════╗")
    print(f"║           DAFTAR NOMOR PLAT KENDARAAN VALID                          ║")
    print(f"╚══════════════════════════════════════════════════════════════════════╝{RESET}")
    print(f"{LIGHT_BROWN}Huruf awal: {start_letter}{RESET}\n")

    garis = f"{DARK_BROWN}+{'-'*6}+{'-'*14}+{'-'*8}+{'-'*14}+{'-'*16}+{RESET}"
    header = f"{BOLD}{GOLD}| {'No.':<4} | {'Huruf Awal':<12} | {'Angka':<6} | {'Huruf Akhir':<12} | {'Kombinasi Plat':<12} |{RESET}"

    print(garis)
    print(header)
    print(garis)

    for i, (prefix, num, suffix, plate) in enumerate(data, start=1):
        print(f"{LIGHT_BROWN}| {i:<4} | {prefix:<12} | {num:<6} | {suffix:<12} | {plate:<12} |{RESET}")

    print(garis)
    print(f"\n{BOLD}{COPPER}Total kombinasi ditampilkan: {len(data)}{RESET}\n")

    with open(filename, "w", encoding="utf-8") as f:
        f.write("DAFTAR NOMOR PLAT KENDARAAN VALID\n")
        f.write(f"Huruf awal: {start_letter}\n\n")
        f.write("+------+--------------+--------+--------------+----------------+\n")
        f.write("| No.  | Huruf Awal   | Angka  | Huruf Akhir  | Kombinasi Plat |\n")
        f.write("+------+--------------+--------+--------------+----------------+\n")
        for i, (prefix, num, suffix, plate) in enumerate(data, start=1):
            f.write(f"| {i:<4} | {prefix:<12} | {num:<6} | {suffix:<12} | {plate:<14} |\n")
        f.write("+------+--------------+--------+--------------+----------------+\n")
        f.write(f"\nTotal kombinasi ditampilkan: {len(data)}\n")

    print(f"{LIGHT_BROWN} File hasil tersimpan di: {filename}{RESET}\n")


# ===== Main =====
if __name__ == "__main__":
    print(f"{COPPER}{BOLD}=== SISTEM NOMOR PLAT KENDARAAN ==={RESET}\n")
    mode = input("Apakah Anda ingin request plat khusus? (y/n): ").strip().lower()

    if mode == 'y':
        print(f"\n{GOLD}Masukkan detail plat yang ingin dicek validitasnya:{RESET}")
        prefix = input("Huruf awal (1–3 huruf besar): ").strip().upper()
        number = input("Angka (1–4 digit): ").strip()
        suffix = input("Huruf akhir (1–2 huruf besar): ").strip().upper()

        valid, result = validate_plate(prefix, number, suffix)
        if valid:
            print(f"\n{GREEN} Plat valid: {result}{RESET}\n")
        else:
            print(f"\n{RED} Plat tidak valid! Alasan: {result}{RESET}\n")

    else:
        huruf_awal = input("Masukkan huruf awal (default = B): ").strip().upper()
        if not huruf_awal:
            huruf_awal = 'B'

        # 🔍 Validasi huruf awal agar bukan angka / simbol
        if not huruf_awal.isalpha():
            print(f"\n{RED} ERROR: Huruf awal hanya boleh terdiri dari huruf A–Z (tidak boleh angka atau simbol).{RESET}")
            sys.exit(1)
        if len(huruf_awal) > 3:
            print(f"\n{RED} ERROR: Huruf awal maksimal 3 karakter huruf besar.{RESET}")
            sys.exit(1)

        try:
            jumlah = int(input("Masukkan jumlah maksimal kombinasi (default = 50): "))
        except ValueError:
            jumlah = 50

        if jumlah > 50:
            jumlah = 50  # batas kombinasi 50 maksimal

        plates = generate_license_plates(start_letter=huruf_awal, max_combinations=jumlah)
        tampilkan_tabel(plates, huruf_awal)