# Tugas 1 — Analisis Pitfall FoodGo

**Kelompok:** Wawan Awan

| Nama | NIM | Kontribusi |
|---|---|---|
| Valen Jonathan Micelino Pasaribu | 10307240072 | Latency Zero |
| Muhammad Kafi Rijal | 10307240016 | Single Point of Failure |
| Yoga Perkasa Didik | 103072400106 | [pitfall/bagian yang dikerjakan] |

## Pitfall 1: Latency Zero — ditulis oleh Valen Jonathan Micelino Pasaribu

**Bukti di skenario:** "Tim menemukan bahwa kode mereka menulis asumsi seperti # network is always reliable, no need for retry"

**Kenapa ini keliru:** Karena komunikasi antar komponen dilakukan melalui jaringan sehingga selalu memiliki latency pada sistem terdistribusi. pada transaksi akan ada beberapa kondisi yang bisa membuat sebuah latency meningkat seperti, beban pada server yang meningkat, kondisi jaringan saat itu, dan  gangguan pada server. maka sistem yang menganggap komunikasi antar komponen akan berlangsung tanpa delay.

**Dampak ke FoodGo:** dampaknya adalah permintaan pada server akan terus menunggu karena tidak ada mekanisme timeout. dan ini akan berbahaya ketika server meminta banyak sekali permintaan, maka semakin banyak request yang tertahan dan menggunakan resource server seperti thread dan memory. ini juga berbahaya bagi server karena bisa overload dan crash.

**Solusi desain awal:** Menerapkan mekanisme timeout untuk setiap komunikasi antar service. dan jika suatu requast mengalami timeout maka requast akan diberentikan dan beban pada server bisa cepat dialokasikan ke request lainya. dan bagi request dihentikan dan sistem dapat menjalankan mekanisme penanganan kegagalan seperti retry.

**Trade-off:** trade off dari penggunaan timeout adalah ketika timeout terlalu cepat bisa saja transaksi yang masih diproses bisa di anggap gagal, sedangakan bila terlalu lama dapat menyebabkan resource tertahan ketika service bermasalah. maka diperlukan mekanisme tambahan seperti retry terbatas agar transaksi yang tidak bena benar gagal bisa mencoba kembali.

---

## Pitfall 2: Single Point of Failure — ditulis oleh Muhammad Kafi Rijal

**Bukti di skenario:** Saat trafik naik, satu server yang menangani semua modul (pesanan, pembayaran, notifikasi kurir) kewalahan karena semuanya berjalan di satu proses monolitik yang sama.

**Kenapa ini keliru:** Karena semua modul (pesanan, pembayaran, notigikasi kurir) di tangani oleh satu server dan dalam satu proses yang sama

**Dampak ke FoodGo:** Ketika trafik sedang tinggi membuat proses menjadi sangat lambat dan ada beberapa permintaan yang timeout

**Solusi desain awal:** Mengubah yang awalnya centralized menjadi distributed

**Trade-off:** Biaya yang lebih besar

---

## Pitfall 3: Transport cost is zero — ditulis oleh Yoga Perkasa Didik

**Bukti di skenario:** 

1. Saat trafik naik, satu server yang menangani semua modul (pesanan, pembayaran, notifikasi kurir) kewalahan karena semuanya berjalan di satu proses monolitik yang sama.

2. Tim menemukan bahwa kode mereka menulis asumsi seperti # network is always reliable, no need for retry dan tidak ada timeout sama sekali pada pemanggilan antar service (modul pesanan memanggil modul pembayaran dan menunggu tanpa batas waktu).

**Kenapa ini keliru:** 

Pada kutipan pertama, semua proses seperti pesanan, pembayaran, dan notifikasi kurir di handle oleh satu server (monolitik) yang sama. Dampaknya adalah, ketika terjadi lonjakan trafik, server akan mengalami kewalahan karena resource CPU dan memory yang harus di bagi untuk menghandle tiga proses tersebut, yang kemungkinan akan menyebabkan sistem menjadi lambat atau munkin RTO (Request Time Out).

Untuk kutpan kedua, walaupun beberapa kata sangan cocok dengan point "The network is reliable", saya menyimpulkan jika pesan "network is always reliable, no need for retry", menunjukan bagaimana tim developer tidak memikirkan skenario yang terjadi pada traffic tinggi saat banyak proses datang. Tentunya biaya dari setiap proses tidaklah murah dan kurang cocok untuk sistem yang monolitik, kecuali jika tim developer sudah melakukan optimasi, scaling, atau perhitungan cost.

**Dampak ke FoodGo:** 

Dampak yang paling terasa dapat dilihat dari beberapa kata seperti 
1. Aplikasi jadi sangat lambat, beberapa permintaan timeout.
2. Server backend kadang crash total dan perlu di-restart manual.

Karena semua proses berjalan dalam sistem monolitik, maka ketika sistem mengalami lonjakan trafik, server akan mengalami kewalahan karena resource CPU dan memory yang harus di bagi untuk menghandle tiga proses tersebut, yang kemungkinan akan menyebabkan sistem menjadi lambat atau munkin RTO (Request Time Out). Selain itu, ketika sistem mengalami kegagalan, sistem akan mengalami crash total.

**Solusi desain awal:** 

Solusi sendiri sebenernya cukup beragam, tergantung dari budget yang ada di FoodGo. Kalau dari saya, hal paling pertama yang bisa diperbaiki adalah Topologi dari sistem FoodGo itu sendiri. Kalau dilihat dari kutuipan yang saya cantumkan, saya beranggapan jika sistem monolitik FoodGo, lebih tepatnya spek server, masih belum memumpuni untuk menampung lonjakan trafik dari tiga proses. Jadi, saran yang bisa saya beri adalah antara melakukan scaling baik vertical scaling (meningkatkan spesifikasi server) atau Horizontal Scaling (menambah jumlah server).

 Pastinya yang lebih murah dikit menggunakan vertical scalling, maka FoodGo dapat meningkatkan spesifikasi server yang saat ini digunakan, seperti menambah kapasitas RAM, CPU, atau resource lainnya. Dengan begitu, satu server yang menangani proses pesanan, pembayaran, dan notifikasi dapat memiliki kapasitas yang lebih besar untuk menangani lonjakan trafik. Pendekatan ini relatif lebih sederhana karena tidak perlu mengubah arsitektur sistem secara besar-besaran, tetapi tetap memiliki batas karena kemampuan peningkatan spesifikasi pada satu server juga terbatas.


**Trade-off:**

Keunggulan yang didapat adalah pemrosesan request yang menjadi lebih cepat dibandingkan sebelumnya.

Namun untuk resiko, tentunya biaya untuk melakukan upgrade baik horizontal maupun vertical tidaklah murah. Kalaupun pihak tim lebih memilih vertical scalling dan masih menggunakan monolitik, masih belum ada jaminan jika masalah lonjakan traffic dapat diselesaikan.

## Kesimpulan Kelompok

[Ringkasan: jika FoodGo memperbaiki ketiga pitfall ini, apa arsitektur yang disarankan secara garis besar? Kaitkan dengan Tugas 2.]
