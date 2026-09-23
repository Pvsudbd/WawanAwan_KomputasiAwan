# Jurnal Proses — Tugas 2

## [Tanggal]
- Opsi arsitektur yang dipertimbangkan:
  Kelompok kami memutuskan untuk menggunakan keduanya yakni Service-Oriented Architecture (SOA) atau Publish-Subscribe. 
- Kenapa akhirnya pilih [SOA/Pub-Sub]: pertama kami menggunakan SOA untuk memecah proses monolith yakni semua service berada pada satu runtutan/ satu aplikasi, ini bisa bermasalah jika salah satu service mengalami kendala yang akan berakibat service lainya juga berkendala sehingga ini kurang baik untuk implementasi pada FoodGo. lalu untuk pub-sub berfungsi untuk menangani kendala apabila ada service yang melakukan request ke service lain namun service yang di tuju sedang tidak tersedia sedangkan service yang melakukan request masih harus melakukan request ke service lain. dan ini menjadi masalah ketika mau ada pembaruan/deploy ulang salah satu service. kedua solusi tersebut bertujuan untuk, pertama memecah service dari yang tadinya monolith, sedangakan untuk pub-sub untuk menangani bagaimana service berkomunikasi tanpa terlalu bergantung satu sama lain.
- Revisi:
- Alur Skenario: Pelanggan --> Service Pesanan --> Service Pembayaran
                                               |-> Message Broker --> Service Notifikasi Kurir & Service Katalog Resto
  
  * Tahap 1: Pelanggan membuat pesanan
  * Interaksi: Pelanggan --> Service Pesanan
  * Jenis Komunikasi: Sinkron
  * Penjelasan: Pelanggan mengirimkan pesanan baru ke sistem, service pesanan menerima dan memvalidasi pesanan tersebut

  * Tahap 2: Pemrosesan pembayaran
  * Interaksi: Service Pesanan --> Service Pembayaran
  * Jenis Komunikasi: Sinkron
  * Penjelasan: Service pesanan memanggil service pembayaran untuk memproses pembayaran transaksi, komunikasi dilakukan
  * secara sinkron karena pesanan memerlukan konfirmasi langsung mengenai status pembayaran sebelum diproses lebih lanjut

  * Tahap 3: Publikasi event pesanan dibuat
  * Interaksi: Service Pembayaran --> Message Broker
  * Jenis Komunikasi: Asinkron
  * Penjelasan: Setelah pembayaran selesai, service pesanan akan membuat event untuk message broker

  * Tahap 4: Distribusi event ke subcriber
  * Interaksi: Message Broker --> Service Notifikasi Kuris & Service Katalog Resto
  * Jenis Komunikasi: Asinkron
  * Penjelasan: Message broker meneruskan event secara independen ke modul modul yang berlangganan:
      service notifikasi kurir: Menerima event untuk mulai mencari driver terdekat dan mengirimkan notifikasi penugasan pesanan,
      service katalog resto: Menerima event untuk meneruskan pesanan ke pihak restoran

- Nomer 4

Kalau dari yang kami pahami dari Tugas Pertama, “Server menangani 4 modul secara bersamaan”, ini berarti menandakan bahwa 4 modul (Pesanan, Pembayaran, Notifikasi, dan Katalog Resto) masih berjalan dalam satu aplikasi monolitik. Jadi, kalau ada salah satu modul yang mengalami gangguan atau perlu diperbarui, modul lainnya juga berpotensi ikut terdampak karena masih berada dalam satu aplikasi dan server yang sama.

Nah, di cara kami yang baru, kami membuat agar modul Pesanan dan Pembayaran dibuat sebagai service dengan pendekatan SOA (Service-Oriented Architecture) yang nantinya akan mengurangi ketergantungan antar-modul dalam satu aplikasi. Dengan dibuat sebagai service, masing-masing modul dapat berjalan dan dikembangkan secara lebih independen. Jadi, ketika salah satu service mengalami gangguan atau perlu diperbarui, service lainnya tidak harus ikut dihentikan atau diperbarui.

Untuk modul seperti Notifikasi Kurir dan Katalog Resto, kami menggunakan konsep Publish-Subscribe (Pub-Sub). Jika setiap modul harus berkomunikasi secara langsung dengan modul lainnya (contoh, SOA), jumlah hubungan komunikasi dapat meningkat secara kuadratik, yaitu mendekati O(n²), seiring bertambahnya jumlah modul. Sebaliknya, dengan Pub-Sub, setiap modul cukup berkomunikasi dengan message broker, sehingga jumlah hubungan langsung antara modul dan perantara dapat bertambah secara linear, yaitu O(n). Broker kemudian meneruskan event kepada modul-modul yang telah berlangganan. Dengan demikian, Pub-Sub dapat mengurangi jumlah ketergantungan langsung antar-modul dan membuat komunikasi lebih fleksibel.
## Log Penggunaan AI (Level 2)

> Wajib diisi sesuai kebijakan Level 2 di [`../RUBRIK-UMUM.md`](../RUBRIK-UMUM.md). Tulis "Tidak memakai AI" pada baris pertama jika memang tidak dipakai. Hanya untuk brainstorming ide/outline — bukan untuk kode/analisis/teks akhir.

| Tanggal | Tool AI | Prompt yang diberikan | Ringkasan saran/ide AI | Bagaimana diolah jadi tulisan/kode sendiri |
|---|---|---|---|---|
| ... | ... | ... | ... | ... |
