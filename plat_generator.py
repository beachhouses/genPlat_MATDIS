import itertools
import os
import random
import time
from datetime import datetime
import sys

# ===== Warna terminal =====
RESET = "\033[0m"
BOLD = "\033[1m"
DIM = "\033[2m"
LIGHT_BROWN = "\033[38;5;180m"
DARK_BROWN = "\033[38;5;94m"
COPPER = "\033[38;5;136m"
GOLD = "\033[38;5;220m"
RED = "\033[91m"
GREEN = "\033[92m"
CYAN = "\033[96m"
GRAY = "\033[90m"

def typewriter(text, delay=0.02, color=None):
    if color is None:
        color = ""
    print(color, end="", flush=True)
    for ch in text:
        print(ch, end="", flush=True)
        time.sleep(delay)
    print(RESET)

def fade_clear():
    for i in range(3):
        print(f"{GRAY}Menghapus tampilan lama{'.' * (i+1)}{RESET}", end="\r")
        time.sleep(0.3)
    os.system('cls' if os.name == 'nt' else 'clear')

def validating_anim():
    for frame in ["⚙️ Validating.", "⚙️ Validating..", "⚙️ Validating..."]:
        print(f"\r{COPPER}{frame}{RESET}", end="", flush=True)
        time.sleep(0.25)
    print("\r", end="")

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


# ===== Generator kombinasi random =====
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


# ===== Efek loading =====
def loading_bar(text="Menyiapkan data", length=30, delay=0.05):
    print(f"\n{GOLD}{text}...", end="", flush=True)
    time.sleep(0.3)
    print()
    for i in range(length + 1):
        filled = int((i / length) * 30)
        bar = f"{COPPER}█" * filled + f"{DARK_BROWN}░" * (30 - filled)
        percent = int((i / length) * 100)
        print(f"\r{BOLD}{GOLD}⏳ [{bar}{RESET}{BOLD}{GOLD}] {percent:3d}%{RESET}", end="", flush=True)
        time.sleep(delay)
    print(f"\n{GREEN}✅ Data berhasil dimuat!{RESET}\n")
    time.sleep(0.5)


# ===== Banner tampilan awal =====
def banner():
    fade_clear()
    print(f"{COPPER}{BOLD}")
    print("╔════════════════════════════════════════════════════════╗")
    print("║               SISTEM NOMOR PLAT KENDARAAN              ║")
    print("╚════════════════════════════════════════════════════════╝")
    print(f"{RESET}{GRAY}Tugas Kelompok Matdis | Oleh Kelompok 2 | Versi 2.3.1{RESET}\n")
    typewriter("Selamat datang di sistem validasi plat kendaraan berbasis CLI.", 0.015, GOLD)
    time.sleep(0.4)


# ===== Tabel tampilan =====
def tampilkan_tabel(data, start_letter):
    loading_bar("Menampilkan tabel kombinasi plat")

    os.makedirs("output", exist_ok=True)
    tanggal = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"output/daftar_plat_valid_{start_letter}_{tanggal}.txt"

    print(f"{GOLD}╔══════════════════════════════════════════════════════════════════════╗")
    print(f"║                 DAFTAR PLAT NOMOR VALID                              ║")
    print(f"╚══════════════════════════════════════════════════════════════════════╝{RESET}\n")

    garis = f"{COPPER}+{'-'*6}+{'-'*14}+{'-'*8}+{'-'*14}+{'-'*16}+{RESET}"
    header = (
        f"{GOLD}| {'No.':<4} "
        f"| {COPPER}{'Huruf Awal':<12} "
        f"| {DARK_BROWN}{'Angka':<6} "
        f"| {COPPER}{'Huruf Akhir':<12} "
        f"| {GOLD}{'Kombinasi Plat':<12} |{RESET}"
    )

    print(garis)
    print(header)
    print(garis)

    color_cycle = [LIGHT_BROWN, COPPER, DARK_BROWN, GOLD]
    for i, (prefix, num, suffix, plate) in enumerate(data, start=1):
        col = color_cycle[i % len(color_cycle)]
        print(
            f"{col}| {i:<4} "
            f"| {prefix:<12} "
            f"| {num:<6} "
            f"| {suffix:<12} "
            f"| {BOLD}{GOLD}{plate:<12}{RESET} {GOLD}|{RESET}"
        )
        time.sleep(0.02)

        print(garis)
    angka_list = [int(num) for _, num, _, _ in data]
    print(f"\n{COPPER}📊 Statistik:")
    print(f"{GOLD}- Angka terkecil: {min(angka_list)}")
    print(f"{GOLD}- Angka terbesar: {max(angka_list)}")

    print(f"\n{BOLD}{COPPER}Total kombinasi ditampilkan: {len(data)}{RESET}")
    print(f"{DIM}{GRAY}File tersimpan di: {filename}{RESET}\n")

    # ===== Simpan ke file txt =====
    with open(filename, "w", encoding="utf-8") as f:
        f.write("DAFTAR PLAT NOMOR VALID\n")
        f.write(f"Dibuat pada: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write("=" * 60 + "\n")
        f.write(f"{'No.':<5}{'Huruf Awal':<12}{'Angka':<8}{'Huruf Akhir':<14}{'Kombinasi Plat':<15}\n")
        f.write("-" * 60 + "\n")
        for i, (prefix, num, suffix, plate) in enumerate(data, start=1):
            f.write(f"{i:<5}{prefix:<12}{num:<8}{suffix:<14}{plate:<15}\n")
        f.write("-" * 60 + "\n")
        f.write(f"Total kombinasi: {len(data)}\n")
        f.write(f"Angka terkecil: {min(angka_list)} | ")
        f.write(f"Angka terbesar: {max(angka_list)} | ")
        f.write(f"Rata-rata angka: {sum(angka_list)/len(angka_list):.2f}\n")

    print(f"{GREEN}💾 Data berhasil disimpan ke file!{RESET}\n")

# ===== Menu Riwayat =====
def tampilkan_riwayat():
    os.makedirs("output", exist_ok=True)
    files = sorted(os.listdir("output"), reverse=True)
    if not files:
        print(f"{RED}Belum ada file output yang tersimpan.{RESET}\n")
        return
    print(f"\n{COPPER}📁 Riwayat File Output:{RESET}")
    for i, file in enumerate(files, start=1):
        print(f"{GOLD}{i:>2}. {file}{RESET}")
    print()


# ===== Menu Utama =====
def main_menu():
    while True:
        banner()
        print(f"{COPPER}{BOLD}╔════════════════════════════════════╗")
        print(f"║             MENU UTAMA             ║")
        print(f"╠════════════════════════════════════╣")
        print(f"║ {GOLD}1{RESET}{COPPER}. Generate Plat Otomatis          ║")
        print(f"║ {GOLD}2{RESET}{COPPER}. Cek Validitas Plat Manual       ║")
        print(f"║ {GOLD}3{RESET}{COPPER}. Lihat Riwayat File Output       ║")
        print(f"║ {GOLD}4{RESET}{COPPER}. Keluar dari Program             ║")
        print(f"╚════════════════════════════════════╝{RESET}\n")

        pilihan = input(f"{GOLD}Pilih menu (1/2/3/4): {RESET}").strip()

        if pilihan == "1":
            while True:
                huruf_awal = input(f"{CYAN}Masukkan huruf awal (default = B): {RESET}").strip().upper()
                if not huruf_awal:
                    huruf_awal = 'B'

                if not huruf_awal.isalpha():
                    validating_anim()
                    print(f"{RED}\n⛔ ERROR: Huruf awal hanya boleh huruf A–Z.{RESET}")
                    time.sleep(1)
                    continue

                while True:
                    jumlah_input = input(f"{CYAN}Masukkan jumlah kombinasi (1–50): {RESET}").strip()
                    if not jumlah_input.isdigit():
                        validating_anim()
                        print(f"{RED}\n⛔ ERROR: Masukkan hanya angka (1–50)!{RESET}")
                        time.sleep(1)
                        continue
                    jumlah = int(jumlah_input)
                    if jumlah < 1 or jumlah > 50:
                        validating_anim()
                        print(f"{RED}\n⛔ ERROR: Nilai harus antara 1 sampai 50.{RESET}")
                        time.sleep(1)
                        continue
                    break

                start_time = time.time()
                loading_bar("Menghasilkan kombinasi plat")
                plates = generate_license_plates(start_letter=huruf_awal, max_combinations=jumlah)
                tampilkan_tabel(plates, huruf_awal)
                exec_time = time.time() - start_time
                print(f"{DIM}{GRAY}Waktu eksekusi: {exec_time:.2f} detik{RESET}\n")

                ulang = input(f"{GOLD}Ingin generate lagi dengan huruf awal berbeda? (y/n): {RESET}").strip().lower()
                if ulang != 'y':
                    break

            input(f"{DIM}Tekan ENTER untuk kembali ke menu utama...{RESET}")

        elif pilihan == "2":
            print(f"\n{COPPER}Masukkan detail plat untuk dicek validitasnya:{RESET}")
            prefix = input(" Huruf awal (1–3 huruf besar): ").strip().upper()
            number = input(" Angka (1–4 digit): ").strip()
            suffix = input(" Huruf akhir (1–2 huruf besar): ").strip().upper()

            loading_bar("Mengecek validitas")
            valid, result = validate_plate(prefix, number, suffix)
            if valid:
                print(f"{GREEN}✅ Plat valid: {result}{RESET}\n")
            else:
                print(f"{RED}❌ Plat tidak valid! Alasan: {result}{RESET}\n")

            input(f"{DIM}Tekan ENTER untuk kembali ke menu utama...{RESET}")

        elif pilihan == "3":
            tampilkan_riwayat()
            input(f"{DIM}Tekan ENTER untuk kembali ke menu utama...{RESET}")

        elif pilihan == "4":
            typewriter("Terima kasih telah menggunakan sistem ini.", 0.015, COPPER)
            print(f"{GRAY} Kelompok 2 - Matdis 2025 | All rights reserved.{RESET}\n")
            break
        else:
            validating_anim()
            print(f"{RED}\n⚠ Pilihan tidak valid! Silakan masukkan 1, 2, 3, atau 4.{RESET}")
            time.sleep(1.5)


# ===== Main =====
if __name__ == "__main__":
    main_menu()