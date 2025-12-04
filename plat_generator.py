import itertools
import os
from datetime import datetime

# ===== Warna gradasi cokelat =====
RESET = "\033[0m"
BOLD = "\033[1m"
LIGHT_BROWN = "\033[38;5;180m"
DARK_BROWN = "\033[38;5;94m"
COPPER = "\033[38;5;136m"
GOLD = "\033[38;5;220m"

def generate_license_plates(start_letter='B', max_combinations=50):
    consonants = [ch for ch in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ' if ch not in 'AEIOU']
    results = []

    # Huruf awal: 1–3 huruf, dimulai dari huruf tertentu
    for letters_len in range(0, 3):  # 0 artinya hanya huruf awal; 1–2 tambahan
        for letters in itertools.product('ABCDEFGHIJKLMNOPQRSTUVWXYZ', repeat=letters_len):
            prefix = start_letter.upper() + ''.join(letters)
            
            # Angka 1–4 digit (1–9999), tidak boleh dimulai 0, hanya genap
            for num in range(2, 10000, 2):
                num_str = str(num)
                if num_str[0] == '0':  
                    continue

                # Huruf akhir: 1–2 huruf, tanpa vokal
                for suffix_len in [1, 2]:
                    for suffix in itertools.product(consonants, repeat=suffix_len):
                        suffix_str = ''.join(suffix)
                        plate = f"{prefix} {num_str} {suffix_str}"
                        if len(plate) <= 10:
                            results.append((prefix, num_str, suffix_str, plate))
                            if len(results) >= max_combinations:
                                return results
    return results


def tampilkan_tabel(data, start_letter):
    os.makedirs("output", exist_ok=True)
    tanggal = datetime.now().strftime("%Y%m%d")
    filename = f"output/daftar_plat_valid_{start_letter}_{tanggal}.txt"

    # Header
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

    # Simpan ke file
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


# ===== Program utama =====
if __name__ == "__main__":
    huruf_awal = input("Masukkan huruf awal (default = B): ").strip().upper()
    if not huruf_awal:
        huruf_awal = 'B'

    try:
        jumlah = int(input("Masukkan jumlah maksimal kombinasi (default = 50): "))
    except ValueError:
        jumlah = 50

    plates = generate_license_plates(start_letter=huruf_awal, max_combinations=jumlah)
    tampilkan_tabel(plates, huruf_awal)