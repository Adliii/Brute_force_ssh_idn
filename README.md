# Brute_force_ssh_idn
tugas bootcamp idn

---

# SSH Hybrid Brute Force Script

---

Ini adalah skrip Python yang dirancang untuk melakukan serangan brute force terhadap server SSH. Skrip ini mengimplementasikan pendekatan hibrida: pertama, ia akan mencoba kata sandi dari **daftar yang disediakan (dictionary attack)**. Jika upaya tersebut gagal, skrip akan secara otomatis beralih ke mode **pure brute force**, mencoba setiap kombinasi karakter yang memungkinkan hingga kata sandi ditemukan atau proses dihentikan secara manual.

## Fitur

* **Dictionary Attack:** Menggunakan daftar kata sandi yang Anda berikan untuk mencoba kredensial dengan cepat.
* **Pure Brute Force:** Jika dictionary attack gagal, skrip akan beralih untuk menghasilkan dan mencoba setiap kombinasi karakter yang mungkin.
* **Dukungan Karakter Luas:** Pure brute force mencakup huruf kecil, huruf besar, angka, dan semua simbol tanda baca (`string.punctuation`).
* **Tanpa Batas Panjang (Pure Brute Force):** Mode pure brute force akan terus berjalan, meningkatkan panjang kata sandi yang dicoba tanpa henti, sampai berhasil atau dihentikan oleh pengguna.
* **Penanganan Error Dasar:** Mencakup penanganan untuk kesalahan koneksi SSH dan timeout.
* **Port Kustom:** Mendukung penentuan port SSH selain port default 22.

## Persyaratan

* Python 3.x
* Library `paramiko`

## Instalasi

1.  **Clone repositori ini:**
    ```bash
    git clone https://github.com/YourUsername/your-repo-name.git
    cd Brute_force_ssh_idn
    ```

2.  **Instal library yang dibutuhkan:**
    ```bash
    pip install paramiko
    ```

## Penggunaan

1.  **Buat file daftar kata sandi (opsional):**
    Anda dapat membuat file teks (misalnya, `passwords.txt`) yang berisi daftar kata sandi yang ingin Anda coba di tahap dictionary attack. Setiap kata sandi harus berada di baris terpisah. Jika Anda tidak menyediakan file ini, skrip akan langsung memulai tahap pure brute force.

    Contoh `passwords.txt`:
    ```
    rahasia123
    admin123
    Password!
    qwerty
    ```

2.  **Jalankan skrip:**
    ```bash
    python Brute_force_ssh_idn.py
    ```

3.  **Ikuti prompt:**
    Skrip akan meminta Anda untuk memasukkan informasi berikut:
    * **Hostname atau IP server SSH target:** Alamat IP atau nama host server yang ingin Anda serang.
    * **Port SSH target (default: 22):** Port SSH server. Tekan Enter untuk menggunakan default (22).
    * **Username SSH target:** Nama pengguna yang akan Anda coba untuk login.
    * **Path ke file daftar kata sandi (kosongkan jika tidak ingin dictionary attack):** Masukkan path ke file `passwords.txt` Anda, atau kosongkan jika Anda ingin langsung ke brute force murni.

4.  **Menghentikan Skrip:**
    Jika skrip berada dalam mode pure brute force dan Anda ingin menghentikannya, cukup tekan **`Ctrl+C`** di terminal.

## Cara Kerja

Skrip ini beroperasi dalam dua fase:

### Fase 1: Dictionary Attack

Skrip akan terlebih dahulu mencoba login menggunakan setiap kata sandi yang ada dalam file daftar kata sandi yang Anda sediakan. Ini adalah metode yang relatif cepat dan sering kali berhasil jika kata sandi target umum atau sudah bocor.

### Fase 2: Pure Brute Force

Jika dictionary attack tidak menemukan kata sandi yang cocok, skrip akan beralih ke mode pure brute force. Dalam mode ini, skrip akan secara sistematis menghasilkan dan mencoba setiap kemungkinan kombinasi karakter (huruf kecil, huruf besar, angka, dan simbol) untuk panjang kata sandi tertentu. Kemudian, ia akan meningkatkan panjang kata sandi dan mengulangi proses tersebut tanpa batas hingga menemukan kata sandi atau dihentikan secara manual.
