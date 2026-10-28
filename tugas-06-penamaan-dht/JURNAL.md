# Jurnal Proses — Tugas 6

## Implementasi find_successor
- Kesalahan pertama yang ditemui (mis. lupa wrap-around di ring): 
  Pas awal nyoba bikin logika successor, kami mikir kalau pencarian linear biasa pake perulangan `node_id >= key_hash`. Masalahnya muncul pas ada hash kurir yang nilainya ternyata lebih besar dari seluruh ID node yang lagi aktif di ring. Contohnya kasus `kurir-005` yang punya hash 175, pas node jakarta-1 (id=177) keluar, node paling besar di ring tinggal node surabaya (id=136). Karena gak ada ID node yang lebih besar dari 175, perulangannya selesai gitu aja tanpa nemu node tujuan, ujung-ujungnya fungsi malah ngembaliin `None`. Selain itu di kode template awal (`chordlama.py`), fungsinya juga masih berupa `pass` sehingga semua lookup kurir sempat gagal/None semua.

  ![alt text](bukti/ChordLama.png)

- Cara memperbaikinya: 
  Kami menambahkan sebuah logika yang menerapkan sifat melingkar (wrap-around) sesuai konsep Chord ring. Jadi setelah daftar ID node diurutin (`sorted_nodes`), kita cari node pertama yang `>= key_hash`. Tapi kalau perulangannya tembus sampai akhir dan tetep gak nemu node yang lebih besar, kita gak balikin `None`, melainkan kita puter balik ke awal ring dengan ngembaliin node paling pertama yaitu `sorted_nodes[0]`. 
  
  Dengan perbaikan ini, hash yang ngelewatin ujung ring (kayak kurir-005 hash 175) otomatis muter balik dan ditampung sama node paling kecil yaitu node bandung (id=40). Pas di-run ulang, semua lookup kurir langsung sukses dapet IP aslinya secara akurat:

  ![alt text](bukti/ChordFix.png)

- Penelusuran manual langkah demi langkah lookup() menemukan successor:
  Sebagai contoh, kita telusuri alur kerja saat program mengeksekusi `lookup("kurir-001")`:
  1. **Hashing ID Kurir:** String `"kurir-001"` dihitung nilai hash-nya lewat `hash_id("kurir-001")` menggunakan SHA-1 modulo 256, menghasilkan nilai hash **50**.
  2. **Pemanggilan find_successor(50):** Fungsi `lookup()` memanggil `find_successor(50)` untuk menentukan node mana yang bertanggung jawab menampung data kurir ini.
  3. **Pengurutan Node di Ring:** Seluruh ID node yang aktif diambil dan diurutkan dari yang terkecil (`sorted_nodes`), sehingga urutannya adalah:
     - `node-bandung-1` (id = 40)
     - `node-jakarta-2` (id = 102)
     - `node-surabaya-1` (id = 136)
     - `node-jakarta-1` (id = 177)
     Urutan ring menjadi: `[40, 102, 136, 177]`.
  4. **Pengecekan Kondisi Successor:**
     - Iterasi 1: Cek node pertama yaitu **40**. Apakah $40 \ge 50$? Tidak, jadi lanjut ke node berikutnya.
     - Iterasi 2: Cek node kedua yaitu **102**. Apakah $102 \ge 50$? Ya, kondisi terpenuhi.
  5. **Hasil Successor:** Berdasarkan aturan Chord (node terkecil yang $\ge$ hash key), pencarian langsung berhenti dan mengembalikan ID **102** (`node-jakarta-2`).
  6. **Pengembalian IP:** Node 102 adalah penanggung jawab key 50, sehingga `lookup()` mengambil data dari `self.data[50]` dan mengembalikan alamat IP kurir tersebut yaitu **`192.168.1.10`**.

- Analisis Kecocokan DHT/Chord untuk Kasus FoodGo:
  1. **Kenapa Chord DHT Lebih Cocok dibanding Flat Naming dan DNS Konvensional:**
     Pada aplikasi FoodGo, mobilitas kurir sangat tinggi di mana mereka sering berpindah lokasi dan berganti jaringan (misalnya dari WiFi resto ke paket data 4G/5G), sehingga alamat IP kurir berubah sangat dinamis dalam hitungan menit. 
     - Kalau kita pakai **Flat Naming Terpusat** (misalnya satu server database pusat berisi tabel ID kurir -> IP), sistem bakal punya *Single Point of Failure (SPOF)*. Kalau server pusatnya down atau kena masalah jaringan, seluruh aplikasi pelanggan gak bisa melacak kurir manapun. Selain itu saat jam sibuk (peak hour), ribuan kurir yang update IP barengan bakal bikin server pusat bottleneck dan crash karena overload.
     - Kalau kita pakai **DNS Konvensional**, masalah terbesarnya ada di mekanisme *caching* dan *TTL (Time-To-Live)*. DNS dirancang untuk domain yang IP-nya relatif statis. Kalau IP kurir berubah cepat sedangkan cache di perangkat pelanggan atau ISP masih menyimpan IP lama (karena TTL belum habis), pelanggan bakal nyoba akses IP kurir yang udah basi (*cache staleness*). Sebaliknya, kalau TTL diset 0 detik biar selalu update, server DNS authoritative bakal dihujani jutaan request setiap detik (*lookup storm*) yang bikin sistem lambat.
     - **Chord DHT** menyelesaikan masalah ini dengan mendistribusikan pemetaan secara merata ke seluruh node ring (*consistent hashing*). Beban query dan update IP terbagi rata ke node-node (seperti node Jakarta, Bandung, Surabaya), tanpa ada server pusat tunggal. Update IP langsung diarahkan ke successor terkait, sehingga data yang dibaca pelanggan selalu data teranyar secara real-time.

  2. **Keunggulan dan Kelemahan Chord DHT:**
     - **Keunggulan:**
       - *Tanpa Titik Gagal Tunggal (Fault Tolerant):* Jika satu node mati (seperti di simulasi saat node Jakarta-1 keluar), sistem tidak tumbang karena tanggung jawab key otomatis dialihkan ke node successor berikutnya tanpa intervensi manual.
       - *Skalabilitas Tinggi:* Saat jumlah kurir bertambah pesat, kita cukup menambahkan node baru ke dalam ring (`join`), dan beban data akan otomatis terbagi ulang secara proporsional.
       - *Konsistensi Data Real-time:* Tidak ada latensi caching berjenjang seperti DNS, sehingga perubahan IP kurir langsung terbaca saat itu juga.
     - **Kelemahan:**
       - *Routing/Lookup Latency:* Pada jaringan nyata dengan jumlah node yang sangat besar, proses pencarian successor memerlukan beberapa kali lompatan pesan (*hop*) antar node ($O(\log N)$ pada Chord asli), yang bisa menambah sedikit jeda waktu koneksi dibanding langsung menembak satu IP server pusat.
       - *Overhead Perubahan Topologi (Churn):* Jika node-node server sering join dan leave secara tiba-tiba dalam frekuensi tinggi, lalu lintas jaringan akan disibukkan oleh proses migrasi data (*rebalancing key*) antar node.

  3. **Contoh Skenario Nyata di FoodGo:**
     - **Skenario 1 (Kurir Pindah Jaringan saat Antar Makanan):**
       Saat jam makan siang, `kurir-001` mengambil orderan di resto dan sempat terhubung ke WiFi resto (`192.168.1.10`). Begitu kurir jalan naik motor, koneksi langsung putus dan HP kurir beralih ke sinyal 4G dengan IP baru (`10.45.2.88`). Aplikasi kurir otomatis mengirim update IP ini ke DHT ring. Karena hash `kurir-001` adalah 50, pembaruan langsung disimpan di `node-jakarta-2` (id=102). Pelanggan yang sedang memantau pergerakan makanan di aplikasi bisa langsung mendapatkan IP `10.45.2.88` tanpa ada kendala *connection timeout* akibat memanggil IP lama.
     - **Skenario 2 (Server Regional Down / Maintenance):**
       Misalkan server regional `node-jakarta-1` (id=177) mengalami mati lampu mendadak atau gangguan jaringan. Jika memakai sistem terpusat, data kurir di area tersebut bakal hilang. Namun di Chord DHT, data `kurir-005` (hash 175) yang tadinya dipegang node 177 otomatis dialihkan ke successor barunya yaitu `node-bandung-1` (id=40) lewat mekanisme *wrap-around*. Pelanggan tetap bisa melakukan *lookup* dan melacak `kurir-005` dengan lancar tanpa terpengaruh matinya server Jakarta-1.

## Skenario join/leave
- Hasil sebelum & sesudah node baru bergabung:

<img width="623" height="98" alt="image" src="https://github.com/user-attachments/assets/4ff0cb1e-8c72-448b-90d2-d3bd583d8a84" />

Sebelum digabung. Ring baru berisi empat node, berurutan melingkar: node-bandung-1 (ID 40), node-jakarta-2 (102), node-surabaya-1 (136), dan node-jakarta-1   (177). Data kurir-012 punya hash 116, sehingga dipegang oleh node pertama yang ID-nya sama dengan atau lebih besar dari 116, yaitu node-surabaya-1 (136). Pada kondisi ini, lookup("kurir-012") mengembalikan IP 192.168.1.15.

Sesudah mereka gabung. node-medan-1 (ID 123, IP 10.0.0.5) masuk ke ring di antara node 102 dan 136, sehingga urutannya menjadi 40 → 102 → 123 → 136 → 177. Node 123 sekarang menjadi node terdekat yang ID-nya masih ≥ 116, jadi tanggung jawab atas kurir-012 bakal pindah dari node 136 ke node 123. Saat lookup("kurir-001") dan lookup("kurir-012") si eksekusi lagi, keduanya tetap mengembalikan IP yang benar, jadi gaka da data yang miss.

- Hasil sebelum & sesudah node keluar:

<img width="590" height="103" alt="image" src="https://github.com/user-attachments/assets/2cd9c06f-4b84-476e-a60a-8710168fce0c" />

Sebelum keluar. Ring berisi lima node dengan urutan 40 → 102 → 123 → 136 → 177. Data kurir-005 (hash 175) dipegang node jakarta-1 (177) dan alamat IP-nya 192.168.1.14.

Sesudah keluar. Node 177 dihapus, sehingga sisa ring menjadi 40 → 102 → 123 → 136. Sekarang tidak ada lagi node dengan ID ≥ 175, jadi pencarian kembali ke awal ring (wrap-around) dan kurir-005 pindah ke node bandung-1 (40). Hasil lookup setelah node keluar menunjukkan kurir-001, kurir-002, dan kurir-005 masih bisa diakses dengan IP yang tepat.

## Log Penggunaan AI (Level 2)

> Wajib diisi sesuai kebijakan Level 2 di [`../RUBRIK-UMUM.md`](../RUBRIK-UMUM.md). Tulis "Tidak memakai AI" pada baris pertama jika memang tidak dipakai. Hanya untuk brainstorming ide/outline — bukan untuk kode/analisis/teks akhir.

| Tanggal | Tool AI | Prompt yang diberikan | Ringkasan saran/ide AI | Bagaimana diolah jadi tulisan/kode sendiri |
|---|---|---|---|---|
| 10/8/2026 | ChatGPT | Apa perbedaan masalah cache staleness pada DNS dibanding lookup langsung di DHT Chord untuk IP dinamis? | DNS bergantung pada TTL; jika TTL lama maka IP kurir jadi stale (ketinggalan), jika TTL 0 maka Authoritative DNS server kebanjiran request (lookup storm). DHT mendistribusikan penyimpanan mapping langsung ke node successor sehingga update langsung terbaca tanpa stale cache. | Kami pakai ide ini untuk menyusun argumen perbandingan di README.md bagian 1, menjelaskan kenapa FoodGo lebih cocok memakai DHT Chord daripada DNS atau tabel pusat. |
| 10/8/2026 | ChatGPT | Bagaimana logika perpindahan data (rebalancing) saat node baru join di antara dua node pada Chord? | Node baru N mengambil alih key dari successor lamanya untuk key yang nilainya <= N dan > predecessor N. Sisanya tetap di node lama. | Kami implementasikan ke dalam loop di method `join()` dan `leave()` di `chord_simulation.py` untuk mendeteksi key mana yang berpindah dan mencatat log perpindahannya. |
