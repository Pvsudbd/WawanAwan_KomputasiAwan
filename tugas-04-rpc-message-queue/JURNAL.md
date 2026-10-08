# Jurnal Proses — Tugas 4

## Jalur yang dipilih
- [RPC / MQ / keduanya], alasan: Kami memilih keduanya untuk masing masing kasus. pertama yakni proses pembayaran perlu menggunakan rpc karena aksi pembayaran harus synchoronus. Proses pembayaran bersifat transaksional dan membutuhkan konsistensi data secara instan (real-time), jadi nantinya client akan menunggu validasi sistem lalu menampilkan notif dari status transaksi. sedangkan untuk kasus kedua yakni modul kurir/notifikasi bagus untuk menggunakan MQ/asynchronus karena ada kondisi dimana mungkin modul kurir bisa saja down/off(pokoknya berkendala) pesan akan masuk ke dalam antrian di rabbitMQ, sehingga ini membuat decoupling antar modul dan membuat modul pembayaran/pesanan tidak akan menunggu kurir dan bisa lanjut ke proses selanjutnya. 

## Kendala teknis
- Error saat setup (mis. koneksi RabbitMQ ditolak, port bentrok): ...

## Uji "pesan tidak hilang" (khusus Jalur B)
- Langkah uji: matikan consumer → jalankan publisher → nyalakan consumer
- Hasil yang diamati: ...

## Log Penggunaan AI (Level 2)

> Wajib diisi sesuai kebijakan Level 2 di [`../RUBRIK-UMUM.md`](../RUBRIK-UMUM.md). Tulis "Tidak memakai AI" pada baris pertama jika memang tidak dipakai. Hanya untuk brainstorming ide/outline — bukan untuk kode/analisis/teks akhir.

| Tanggal | Tool AI | Prompt yang diberikan | Ringkasan saran/ide AI | Bagaimana diolah jadi tulisan/kode sendiri |
|---|---|---|---|---|
| ... | ... | ... | ... | ... |
