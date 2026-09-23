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

- Nomer 4. Analisis tertulis: kenapa gaya ini mengatasi masalah coupling dari Tugas 1, dan apa trade-off-nya (mis. Pub-Sub menambah kompleksitas debugging karena alur tidak linear).

Kalau dari yang kami pahami dari Tugas Pertama, “Server menangani 4 modul secara bersamaan”, ini berarti menandakan bahwa 4 modul (Pesanan, Pembayaran, Notifikasi, dan Katalog Resto) masih berjalan dalam satu aplikasi monolitik. Jadi, kalau ada salah satu modul yang mengalami gangguan atau perlu diperbarui, modul lainnya juga berpotensi ikut terdampak karena masih berada dalam satu aplikasi dan server yang sama.

Nah, di cara kami yang baru, kami membuat agar modul Pesanan dan Pembayaran dibuat sebagai service dengan pendekatan SOA (Service-Oriented Architecture) yang nantinya akan mengurangi ketergantungan antar-modul dalam satu aplikasi. Dengan dibuat sebagai service, masing-masing modul dapat berjalan dan dikembangkan secara lebih independen. Jadi, ketika salah satu service mengalami gangguan atau perlu diperbarui, service lainnya tidak harus ikut dihentikan atau diperbarui.

Untuk modul seperti Notifikasi Kurir dan Katalog Resto, kami menggunakan konsep Publish-Subscribe (Pub-Sub). Jika setiap modul harus berkomunikasi secara langsung dengan modul lainnya (contoh, SOA), jumlah hubungan komunikasi dapat meningkat secara kuadratik, yaitu mendekati O(n²), seiring bertambahnya jumlah modul. Sebaliknya, dengan Pub-Sub, setiap modul cukup berkomunikasi dengan message broker, sehingga jumlah hubungan langsung antara modul dan perantara dapat bertambah secara linear, yaitu O(n). Broker kemudian meneruskan event kepada modul-modul yang telah berlangganan. Dengan demikian, Pub-Sub dapat mengurangi jumlah ketergantungan langsung antar-modul dan membuat komunikasi lebih fleksibel.

Trade Off : Kalau dari kasus tugas 1, pub sub bisa ngebantu nanganin lonjakan request karena bisa menggunakan tipe Pub Sub asyncronus (menampung event dan subscriber bisa ngeproses sesuai kapasitas) jadi beban masih bisa diantrikan. Tapi penggunaanya bisa ngebuat debugging jadi lebih sulit karena sistem komunikasinya asyncronus, jadi perlu effort buat ngelacak event gagal di modul.
## Log Penggunaan AI (Level 2)

> Wajib diisi sesuai kebijakan Level 2 di [`../RUBRIK-UMUM.md`](../RUBRIK-UMUM.md). Tulis "Tidak memakai AI" pada baris pertama jika memang tidak dipakai. Hanya untuk brainstorming ide/outline — bukan untuk kode/analisis/teks akhir.

| Tanggal | Tool AI | Prompt yang diberikan | Ringkasan saran/ide AI | Bagaimana diolah jadi tulisan/kode sendiri |
|---|---|---|---|---|
| 9/23/2026 | ChatGPT | Kalau semisal Pub-Sub di beri lonjakan traffic, katakanlah 10.000, apakah dia bakal lebih murah daripada SOA? | SOA + komunikasi sinkron: request bisa membuat service harus menunggu response. Kalau 10.000 request datang bersamaan, service yang dituju bisa menjadi bottleneck.Pub-Sub + asynchronous: producer cukup mengirim event ke broker, lalu bisa lanjut. Broker dapat menampung/buffering event dan subscriber memprosesnya sesuai kapasitas.Jadi Pub-Sub bisa lebih tahan terhadap burst traffic karena beban pemrosesan dapat diantrikan.Tapi broker sendiri juga punya batas kapasitas. Jadi bukan berarti 10.000 request otomatis lebih murah atau lebih cepat. | Kalau dari kasus tugas 1, pub sub bisa ngebantu nanganin lonjakan request karena bisa menggunakan tipe Pub Sub asyncronus (menampung event dan subscriber bisa ngeproses sesuai kapasitas) jadi beban masih bisa diantrikan. Tapi penggunaanya bisa ngebuat debugging jadi lebih sulit karena sistem komunikasinya asyncronus, jadi perlu effort buat ngelacak event gagal di modul. |
