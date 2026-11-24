# Manajemen Servis Komputer

Aplikasi desktop Python Tkinter dengan database MySQL dan tema biru-putih.

## Fitur
- Login pengguna (akun admin awal dibuat otomatis)
- Dashboard ringkasan pelanggan, perangkat, servis, dan pembayaran
- CRUD dan pencarian data pelanggan, perangkat, teknisi, servis, pembayaran
- Ekspor data tiap menu ke Excel
- Laporan servis PDF
- Backup dan restore database melalui `mysqldump` dan `mysql`

## 1. Persiapan
1. Install Python 3.10 atau lebih baru.
2. Install MySQL Server atau XAMPP (MySQL/MariaDB).
3. Jalankan service MySQL.
4. Buka phpMyAdmin atau MySQL Workbench.
5. Import file `database/db_servis_komputer.sql`.

## 2. Atur koneksi database
Buka `config.py`, sesuaikan:
- host (biasanya localhost)
- port (biasanya 3306)
- user (sering root)
- password (sesuai password MySQL Anda)

## 3. Install library
Buka terminal di folder project, jalankan:

```bash
python -m venv .venv
.venv\\Scripts\\activate
pip install -r requirements.txt
```

Jika PowerShell menolak aktivasi, jalankan terminal CMD atau gunakan:
`.\.venv\Scripts\python.exe -m pip install -r requirements.txt`

## 4. Jalankan aplikasi
```bash
python main.py
```

Login pertama:
- Username: `admin`
- Password: `admin123`

Segera ubah password admin jika aplikasi digunakan sungguhan. Untuk tugas sekolah, akun default ini hanya untuk demonstrasi.

## 5. Urutan penggunaan
1. Tambahkan pelanggan.
2. Tambahkan perangkat dan pilih pelanggan.
3. Tambahkan teknisi.
4. Tambahkan servis, pilih perangkat dan teknisi.
5. Perbarui status servis dan biaya.
6. Tambahkan pembayaran dengan ID servis yang sesuai.
7. Ekspor Excel dari halaman data atau PDF dari menu samping.

## 6. Backup dan restore
Tombol backup/restore memanggil program command-line `mysqldump` dan `mysql`.
Pastikan folder `bin` MySQL sudah masuk ke PATH Windows. Pada XAMPP biasanya:
`C:\\xampp\\mysql\\bin`

## 7. Membuat file EXE
Setelah aplikasi berjalan baik:
```bash
pip install pyinstaller
pyinstaller --noconfirm --onefile --windowed --name ManajemenServisKomputer main.py
```
Hasil ada di folder `dist/ManajemenServisKomputer.exe`.
Komputer tujuan tetap harus memiliki MySQL dan database yang sudah dibuat.

## Catatan
- Aplikasi ini adalah fondasi proyek pembelajaran. Uji dengan data contoh terlebih dahulu.
- Login menggunakan hash SHA-256 sederhana untuk demonstrasi. Untuk penggunaan produksi, gunakan algoritma password hashing khusus seperti bcrypt/Argon2, mekanisme ganti password, dan pengaturan hak akses per menu.
- Hak akses role admin/petugas disimpan, tetapi pembatasan menu rinci belum diterapkan pada versi dasar ini.
- Backup/restore membutuhkan executable MySQL tersedia di PATH.