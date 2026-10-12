# 🎙️ SKRIP PRESENTASI FINAL LENGKAP: EEPIS AUTO VIP DEALERSHIP v2.0
### Kelompok 3 — 1 D4 IT C (Teknik Informatika PENS)
**Anggota Presenter:** Mustofa Barakbah (3125600065) & Reza Ali Muhammad (3125600061)  
**File Presentasi:** `d:\PraktikumOOP\EepisAutoGUI\EEPIS_Auto_VIP_Dealership_v2.pptx`

---

## 📌 PANDUAN PEMBAGIAN DAN TIPS PANGGUNG
1. **Durasi Total:** 10 – 12 Menit (termasuk demonstrasi aplikasi).
2. **Postur:** Berdiri tegap, tatap mata dosen penguji secara bergantian, jangan membaca teks slide secara monoton melainkan ceritakan alur logikanya.
3. **Kata Kunci Penilaian Dosen:** *Separation of Concerns*, *Dynamic Dispatch*, *Data Hiding / Encapsulation*, *Robustness via Custom Exception*, *JavaFX Canvas 60 FPS*.

---

### 🎬 SLIDE 1: COVER & IDENTITAS PROYEK
*(Tampilan: Slide Cover bernuansa Obsidian Dark Tech dengan logo EEPIS MOTORS)*

> **[Presenter 1 - Mustofa]:**  
> *"Selamat pagi/siang Bapak/Ibu Dosen Penguji yang kami hormati, serta rekan-rekan sekalian.*  
>  
> *Perkenalkan, saya Mustofa Barakbah bersama rekan saya Reza Ali Muhammad dari Kelompok 3, kelas 1 D4 IT C. Hari ini, kami sangat bangga mempersembahkan Final Project Pemrograman Berorientasi Objek kami yang berjudul: **Sistem EEPIS Auto VIP Dealership versi 2.0**.*  
>  
> *Aplikasi ini bukan sekadar simulasi katalog konvensional, melainkan sebuah platform Enterprise terpadu berbasis JavaFX yang memadukan manajemen dealer mobil mewah, wealth management portofolio aset, kalkulasi pajak otomatis, dan simulasi interaktif **Test Drive 2D Canvas 60 FPS**. Seluruh ekosistem ini dibangun dengan menerapkan 4 Pilar OOP secara murni, kokoh, dan berstandar industri."*

---

### 🎬 SLIDE 2: OVERVIEW & ARSITEKTUR SISTEM
*(Tampilan: 7 Modul Interaktif, KPI MVC, dan Latar Belakang Masalah)*

> **[Presenter 1 - Mustofa]:**  
> *"Bapak/Ibu sekalian, proyek ini dilatarbelakangi oleh keterbatasan sistem dealer tradisional yang umumnya hanya bersifat pasif tanpa validasi kelayakan finansial pelanggan secara dinamis, tanpa transparansi audit pajak, dan tanpa pengalaman menguji kendaraan secara nyata.*  
>  
> *EEPIS Auto 2.0 menjawab tantangan tersebut dengan menghadirkan **7 Modul Interaktif dalam satu kendali terpusat**: mulai dari Katalog Showroom dengan Java Stream API, Dasbor Portofolio Aset, Pusat Servis Resmi, Kalkulasi Pajak PPN 11%, Trade-In mobil bekas, Log Riwayat Finansial, hingga VIP Lounge.*  
>  
> *Arsitektur sistem dibangun di atas pola desain **Model-View-Controller (MVC)**. Model menangani logika bisnis murni, View didefinisikan secara bersih lewat berkas deklaratif FXML dan CSS modern, serta Controller mengorkestrasi event aplikasi tanpa saling tumpang tindih (*Separation of Concerns*)."*

---

### 🎬 SLIDE 3: PILAR OOP 1 — ABSTRACTION & INHERITANCE
*(Tampilan: Diagram Hierarki User-Customer & Vehicle serta Bedah Kode Java)*

> **[Presenter 2 - Reza]:**  
> *"Memasuki bedah konsep OOP, pilar pertama yang kami terapkan adalah **Abstraction** dan **Inheritance**.*  
>  
> *Kami mendefinisikan kelas `User`, `Customer`, dan `Vehicle` sebagai **Abstract Class**. Tujuannya adalah mencegah pembuatan objek (*instantiation*) yang belum konkret secara bisnis. Kita tidak bisa sekadar membuat 'objek kendaraan' tanpa tahu apakah itu mobil listrik atau mobil bensin.*  
>  
> *Dari abstract class tersebut, kami membangun dua cabang hierarki inheritance:*  
> *1. **Hierarki Pelanggan:** `User` mewariskan sifat identitas dasar ke `Customer`, yang kemudian dispesialisasikan menjadi tiga tier VIP: `RegularCustomer`, `SilverCustomer` (diskon 5%), dan `GoldCustomer` (diskon 8% plus cashback saldo).*  
> *2. **Hierarki Kendaraan:** Abstract class `Vehicle` diturunkan ke `ElectricCar` yang memiliki atribut kapasitas baterai kWh dan jarak tempuh, serta `GasCar` yang memiliki kapasitas mesin cc dan jenis transmisi.*  
> *Pewarisan ini memastikan struktur kode sangat rapi, modular, dan dapat dikembangkan di masa depan tanpa menduplikasi kode dasar."*

---

### 🎬 SLIDE 4: PILAR OOP 2 — POLYMORPHISM (DYNAMIC DISPATCH)
*(Tampilan: Overriding testDrive(), calculateDiscount(), applyBonus(), dan Cuplikan Kode)*

> **[Presenter 2 - Reza]:**  
> *"Pilar kedua adalah **Polymorphism** melalui mekanisme **Dynamic Method Dispatch**.*  
>  
> *Keunggulan utama polimorfisme adalah kemampuan memanggil nama method yang sama pada tipe objek induk `Vehicle` atau `Customer`, namun Java secara otomatis mengeksekusi perilaku unik milik subclass terkait saat runtime.*  
>  
> *Sebagai contoh nyata pada kode kami:*  
> *- Ketika pengguna menekan tombol Test Drive pada `GasCar`, method `testDrive()` mengembalikan suara mesin 3000cc yang menderu kencang.*  
> *- Sebaliknya pada `ElectricCar`, method yang sama menghasilkan karakteristik motor listrik yang instan dan senyap.*  
>  
> *Hal serupa berlaku pada method `calculateDiscount()` dan `applyBonus()`. Controller tidak membutuhkan percabangan `if-else` yang rumit untuk mengecek tipe pelanggan. Cukup memanggil `currentUser.applyBonus()`, dan kelas `GoldCustomer` secara otomatis memotong saldo dengan diskon 8% serta memberikan cashback 2% ke rekening pelanggan."*

---

### 🎬 SLIDE 5: PILAR OOP 3 — ENCAPSULATION & DATA INTEGRITY
*(Tampilan: Proteksi bankBalance, Alur Validasi buyVehicle(), dan Cuplikan Kode)*

> **[Presenter 1 - Mustofa]:**  
> *"Pilar ketiga yang menjadi fondasi keamanan finansial sistem kami adalah **Encapsulation**.*  
>  
> *Variabel kritis seperti `bankBalance` pada pelanggan dan `stock` pada kendaraan disembunyikan menggunakan modifier akses `protected/private`. Atribut ini tidak boleh diakses atau diubah langsung dari luar kelas.*  
>  
> *Perhatikan cuplikan method `buyVehicle()` pada layar. Method ini bertindak sebagai gerbang integritas data yang menjalankan validasi atomik:*  
> *1. Pertama, memvalidasi ketersediaan stok fisik.*  
> *2. Kedua, menghitung diskon tier polimorfis dan menambahkan beban PPN 11%.*  
> *3. Ketiga, memverifikasi kecukupan dana pelanggan. Jika saldo kurang, sistem langsung menolak transaksi.*  
> *4. Dan keempat, jika seluruh syarat terpenuhi, saldo dipotong secara internal, stok dikurangi, unit ditambahkan ke koleksi `garage`, dan faktur transaksi resmi diterbitkan.*  
>  
> *Melalui enkapsulasi, mustahil terjadi saldo bernilai negatif atau pembelian kendaraan saat stok kosong."*

---

### 🎬 SLIDE 6: PILAR OOP 4 — INTERFACE & CUSTOM EXCEPTION
*(Tampilan: Kontrak ITaxable, Kelas DealershipException, dan Blok Try-Catch GUI)*

> **[Presenter 1 - Mustofa]:**  
> *"Pilar keempat adalah implementasi **Interface ITaxable** dan **Custom Exception Handling** untuk menjamin ketahanan program (*robustness*).*  
>  
> *Kami mendefinisikan interface `ITaxable` sebagai kontrak wajib perpajakan. Melalui interface ini, seluruh kelas turunan `Vehicle` diwajibkan mengimplementasikan method `calculateTax()` yang menghitung tarif PPN 11% secara standar nasional.*  
>  
> *Untuk menangani kondisi darurat, kami membangun kelas khusus `DealershipException` turunan langsung dari `java.lang.Exception`. Jika pelanggan mencoba membeli mobil yang stoknya habis atau saldo rekeningnya tidak mencukupi, logika bisnis akan melempar (*throw*) exception ini.*  
>  
> *Di lapisan Controller, exception ditangkap dengan blok `try-catch` secara elegan. Alih-alih membuat program berhenti tiba-tiba (*crash*), sistem menangkap pesan kesalahan tersebut dan menampilkannya dalam bentuk notifikasi **Toast Merah** yang anggun di layar antarmuka pengguna."*

---

### 🎬 SLIDE 7: INOVASI UTAMA — TEST DRIVE 2D CANVAS GAME
*(Tampilan: Screenshot Gameplay Racing 3 Jalur & Mekanisme Fisika)*

> **[Presenter 2 - Reza]:**  
> *"Salah satu terobosan paling inovatif dalam EEPIS Auto 2.0 adalah pembaruan total modul **Test Drive** menjadi **Simulasi 2D Mini Game Interaktif (60 FPS)**.*  
>  
> *Sebelumnya, test drive hanya menampilkan dialog teks. Kini, kami membangun game engine mandiri berbasis JavaFX `Canvas` dan `AnimationTimer` dengan mekanisme:*  
> *- **Full Geometric Rendering:** Seluruh bodi mobil, lampu depan/belakang, roda, dan partikel digambar langsung menggunakan `GraphicsContext` sehingga 100% bebas dari glitch rendering font/emoji.*  
> *- **Fisika Berbeda (EV vs Gas):** Mobil listrik memiliki torsi instan dengan akselerasi awal lebih gesit dan efek glow neon biru. Sedangkan mobil bensin memiliki akselerasi bertahap, suara raungan, dan efek asap knalpot.*  
> *- **Gameplay & Reward Nyata:** Pemain mengendalikan mobil di jalan raya 3 lajur dengan tombol panah atau [A]/[D], menghindari kendaraan rintangan (3 nyawa), dan mengumpulkan koin emas yang memberikan reward nyata berupa saldo tambahan ke rekening pelanggan."*

---

### 🎬 SLIDE 8: DEMONSTRASI SHOWROOM & HASIL TEST DRIVE
*(Tampilan: Screenshot Katalog Showroom & Modal Skor Test Drive)*

> **[Presenter 2 - Reza]:**  
> *"Pada slide ini, Bapak/Ibu dapat melihat implementasi antarmuka hasil dari kode tersebut.*  
>  
> *Di sisi kiri adalah **Katalog Showroom Modern**. Kami memanfaatkan Java Stream API untuk melakukan penyaringan data secara real-time saat pengguna mengetikkan kata kunci atau memilih filter harga dan tipe EV/Bensin. Kartu mobil menampilkan status stok, harga, serta estimasi diskon dan PPN.*  
>  
> *Di sisi kanan adalah **Modal Hasil Test Drive**. Setelah simulasi selesai, sistem menampilkan skor jarak tempuh, gelar peringkat pengemudi (Master Driver, Advanced, atau Beginner), serta mencetak kalimat output polimorfis dari method `testDrive()` mobil yang bersangkutan."*

---

### 🎬 SLIDE 9: DEMONSTRASI DASBOR PORTOFOLIO & GARASI
*(Tampilan: Screenshot Dasbor Portofolio, BarChart Nilai Aset, & Sertifikat Garasi)*

> **[Presenter 1 - Mustofa]:**  
> *"Slide ini memperlihatkan modul kebanggaan kami: **Dasbor Portofolio Aset (Wealth Management)**.*  
>  
> *Di bagian atas, sistem merangkum total unit, nilai aset portofolio, dan beban pajak garasi.  
> Di bawahnya, grafik **BarChart JavaFX** berhasil diperbaiki secara sempurna: garis batang aset kini muncul dengan warna gradasi zamrud yang elegan, menampilkan perbandingan nilai aset per unit mobil secara proporsional dalam jutaan rupiah.*  
>  
> *Di sebelah kanan grafik, **Sertifikat Kepemilikan Garasi** menampilkan sertifikat digital kendaraan dengan nomor registrasi kepemilikan unik (#01, #02), rincian spesifikasi, dan stempel verifikasi lunas."*

---

### 🎬 SLIDE 10: DEMONSTRASI SERVIS, PAJAK & TRADE-IN
*(Tampilan: Screenshot Servis Center Berkala & Faktur Pembelian Terformat)*

> **[Presenter 2 - Reza]:**  
> *"Berikut adalah modul operasional purna jual kami:*  
> *- **Pusat Servis Berkala:** Pelanggan dapat memilih unit di garasi untuk diservis dengan biaya standar Rp 2.500.000. Transaksi ini memotong saldo terenkapsulasi secara aman dan dicatat di histori log.*  
> *- **Kalkulasi Pajak & Asuransi:** Menghitung akumulasi beban PPN 11% yang harus dibayarkan ke negara berdasarkan seluruh unit aktif di garasi.*  
> *- **Faktur Transaksi:** Pada gambar kanan, faktur digital mencatat rincian harga OTR, potongan diskon tier pelanggan, pajak PPN, sisa saldo akhir, serta bonus VIP seperti asuransi all-risk dan cashback tunai."*

---

### 🎬 SLIDE 11: UML CLASS DIAGRAM & PEMETAAN SISTEM
*(Tampilan: Diagram UML 3 Kolom: Hierarki Customer, Controller, dan Hierarki Vehicle)*

> **[Presenter 1 - Mustofa]:**  
> *"Sebagai kesimpulan arsitektur perangkat lunak secara menyeluruh, mari kita perhatikan **UML Class Diagram** di layar.*  
>  
> *- **Kolom Kiri (Inheritance Customer):** Menunjukkan superclass `User` yang diturunkan ke `Customer`, lalu dispesialisasikan ke `RegularCustomer`, `SilverCustomer`, dan `GoldCustomer`.*  
> *- **Kolom Kanan (Realization & Inheritance Vehicle):** Menunjukkan interface `ITaxable` yang direalisasikan oleh abstract class `Vehicle`, kemudian diturunkan ke `GasCar` dan `ElectricCar`.*  
> *- **Kolom Tengah (PrimaryController sebagai Aggregate Root):** Menunjukkan relasi **Agregasi** di mana Controller mengelola sesi `Customer` aktif dan koleksi showroom `Vehicle`. Serta relasi agregasi antara `Customer` dengan `Vehicle` melalui atribut garasi `List<Vehicle>`.*  
>  
> *Struktur ini membuktikan bahwa hubungan antar kelas dirancang secara terencana, konsisten, dan mematuhi kaidah Object-Oriented Design standar industri."*

---

### 🎬 SLIDE 12: KESIMPULAN & PENUTUP
*(Tampilan: 5 Poin Keunggulan Utama & Penutup Sesi Tanya Jawab)*

> **[Presenter 1 - Mustofa]:**  
> *"Bapak/Ibu Dosen Penguji yang kami hormati, pengembangan EEPIS Auto VIP Dealership v2.0 membuktikan bahwa penerapan 4 pilar OOP secara utuh menghasilkan aplikasi yang:*  
> *1. **Modular & Scalable:** Mudah ditambah tier pelanggan atau tipe mobil baru tanpa mengubah kode yang sudah ada.*  
> *2. **Aman & Terintegritas:** Saldo dan inventaris terlindungi lewat Enkapsulasi.*  
> *3. **Fleksibel:** Polimorfisme dan Interface menyatukan kalkulasi pajak dan test drive.*  
> *4. **Robust:** Custom Exception menjamin aplikasi tidak pernah mengalami crash.*  
> *5. **Engaging:** Tampilan bertaraf Enterprise dengan Simulasi 2D Game 60 FPS.*  
>  
> *Demikian presentasi dari Kelompok 3. Terima kasih yang sebesar-besarnya atas perhatian dan waktu Bapak/Ibu Dosen. Waktu dan tempat kami persilakan untuk sesi tanya jawab."*

---
*(Presenter membungkuk memberi hormat secara profesional)*
