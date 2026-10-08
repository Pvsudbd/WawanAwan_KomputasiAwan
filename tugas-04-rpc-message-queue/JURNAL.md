# Jurnal Proses — Tugas 4

## Jalur yang dipilih
- [RPC / MQ / keduanya], alasan: Kami memilih keduanya untuk masing masing kasus. pertama yakni proses pembayaran perlu menggunakan rpc karena aksi pembayaran harus synchoronus. Proses pembayaran bersifat transaksional dan membutuhkan konsistensi data secara instan (real-time), jadi nantinya client akan menunggu validasi sistem lalu menampilkan notif dari status transaksi. sedangkan untuk kasus kedua yakni modul kurir/notifikasi bagus untuk menggunakan MQ/asynchronus karena ada kondisi dimana mungkin modul kurir bisa saja down/off(pokoknya berkendala) pesan akan masuk ke dalam antrian di rabbitMQ, sehingga ini membuat decoupling antar modul dan membuat modul pembayaran/pesanan tidak akan menunggu kurir dan bisa lanjut ke proses selanjutnya. 

## Kendala teknis
- Error saat setup (mis. koneksi RabbitMQ ditolak, port bentrok): ...

## Uji "pesan tidak hilang" (khusus Jalur B)
- **Langkah uji:** Matikan `consumer.py` → jalankan `publisher.py` (kirim 3 pesan) → nyalakan `consumer.py` lagi.
- **Hasil yang diamati:** 
  1. Pas `consumer.py` dimatikan dulu terus kita jalankan `publisher.py`, si publisher tetep bisa ngirim 3 pesan pembayaran tanpa ada error sama sekali:
     ![Publisher Kirim Pesan Saat Consumer Offline](bukti/MOM%20Asinkron%20-%20consumer%20offline.png)
  2. Terus pas dicek di dashboard RabbitMQ, 3 pesan itu ga hilang tapi ketahan dan numpuk di antrean `pembayaran_berhasil` dengan status **Ready: 3**:
     ![Dashboard RabbitMQ Pesan Menumpuk](bukti/rabbitmq%20-%20consumer%20offline.png)
  3. Nah, begitu `consumer.py` kita nyalain lagi, si consumer langsung otomatis nyedot dan memproses 3 pesan yang sempet nunggu tadi:
     ![Consumer Online Memproses Pesan](bukti/MOM%20Asinkron%20-%20consumer%20online.png)
     Pas dicheck lagi di dashboard RabbitMQ, jumlah antreannya langsung balik jadi 0 (**Ready: 0**). Ini ngebuktiin kalau pake Message Queue, pesan tetep aman dan ga bakal hilang walaupun aplikasinya sempet mati:
     ![Dashboard RabbitMQ Antrean Beres](bukti/rabbitmq%20-%20consumer%20online.png)
  
**Kesimpulan Uji Pengiriman Pesan:**
Percobaan ini membuktikan bahwa Message Queue punya sifat *asynchronous decoupling*. Artinya, modul pengirim dan modul penerima benar-benar independen, jadi pengirim tidak perlu menunggu penerima aktif, dan data transaksi dijamin aman tersimpan di RabbitMQ tanpa risiko hilang sedikit pun meskipun layanan penerima sedang mati.

## Log Penggunaan AI (Level 2)

> Wajib diisi sesuai kebijakan Level 2 di [`../RUBRIK-UMUM.md`](../RUBRIK-UMUM.md). Tulis "Tidak memakai AI" pada baris pertama jika memang tidak dipakai. Hanya untuk brainstorming ide/outline — bukan untuk kode/analisis/teks akhir.

| Tanggal | Tool AI | Prompt yang diberikan | Ringkasan saran/ide AI | Bagaimana diolah jadi tulisan/kode sendiri |
|---|---|---|---|---|
| ... | ... | ... | ... | ... |
