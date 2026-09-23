# Jurnal Proses — Tugas 2

## [Tanggal]
- Opsi arsitektur yang dipertimbangkan:
  Kelompok kami memutuskan untuk menggunakan keduanya yakni Service-Oriented Architecture (SOA) atau Publish-Subscribe. 
- Kenapa akhirnya pilih [SOA/Pub-Sub]: pertama kami menggunakan SOA untuk memecah proses monolith yakni semua service berada pada satu runtutan/ satu aplikasi, ini bisa bermasalah jika salah satu service mengalami kendala yang akan berakibat service lainya juga berkendala sehingga ini kurang baik untuk implementasi pada FoodGo. lalu untuk pub-sub berfungsi untuk menangani kendala apabila ada service yang melakukan request ke service lain namun service yang di tuju sedang tidak tersedia sedangkan service yang melakukan request masih harus melakukan request ke service lain. dan ini menjadi masalah ketika mau ada pembaruan/deploy ulang salah satu service. kedua solusi tersebut bertujuan untuk, pertama memecah service dari yang tadinya monolith, sedangakan untuk pub-sub untuk menangani bagaimana service berkomunikasi tanpa terlalu bergantung satu sama lain.
- Revisi:
- Alur Skenario: Pelanggan --> Service Pesanan --> Service Pembayaran --> Message Broker --> Service Notifikasi Kurir & Service Katalog Resto
  
  * Tahap 1: Pelanggan membuat pesanan
  * Interaksi: Pelanggan --> Service Pesanan
  * Jenis Komunikasi: Sinkron
  * Penjelasan: Pelanggan mengirimkan pesanan baru ke sistem, service pesanan menerima dan memvalidasi pesanan tersebut\n

  * Tahap 2: Pemrosesan pembayaran
  * Interaksi: Service Pesanan --> Service Pembayaran
  * Jenis Komunikasi: Sinkron
  * Penjelasan: Service pesanan memanggil service pembayaran untuk memproses pembayaran transaksi, komunikasi dilakukan
  * secara sinkron karena pesanan memerlukan konfirmasi langsung mengenai status pembayaran sebelum diproses lebih lanjut

  * Tahap 3: Publikasi event pesanan dibuat
  * Interaksi: Service Pembayaran --> Message Broker
  * Jenis Komunikasi: Asinkron
  * Penjelasan: Setelah pembayaran selesai

  * Tahap 4: Distribusi event ke subcriber
  * Interaksi: Message Broker --> Service Notifikasi Kuris & Service Katalog Resto
  * Jenis Komunikasi: Asinkron
  * Penjelasan: Message broker meneruskan event secara independen ke modul modul yang berlangganan:
      service notifikasi kurir: Menerima event untuk mulai mencari driver terdekat dan mengirimkan notifikasi penugasan pesanan,
      service katalog resto: Menerima event untuk meneruskan pesanan ke pihak restoran

## Log Penggunaan AI (Level 2)

> Wajib diisi sesuai kebijakan Level 2 di [`../RUBRIK-UMUM.md`](../RUBRIK-UMUM.md). Tulis "Tidak memakai AI" pada baris pertama jika memang tidak dipakai. Hanya untuk brainstorming ide/outline — bukan untuk kode/analisis/teks akhir.

| Tanggal | Tool AI | Prompt yang diberikan | Ringkasan saran/ide AI | Bagaimana diolah jadi tulisan/kode sendiri |
|---|---|---|---|---|
| ... | ... | ... | ... | ... |
