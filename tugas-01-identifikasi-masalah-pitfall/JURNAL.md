# Jurnal Proses — Tugas 1

> Isi jurnal ini selama proses diskusi berlangsung, bukan ditulis ulang rapi di akhir. Tulis dengan gaya bebas — poin diskusi, kebuntuan, perubahan pikiran.

## 9/16/2026
- Peserta: 1. Muhammad Kafi Rijal (10307240016) 2. Valen Jhonatan Micelino Pasaribu (10307240072) 3. Yoga Perkasa Didik (103072400106)
- Poin diskusi: Mengidentifikasi 3 jenis pitfall utama yang ada pada kutipan
- Perbedaan pendapat (jika ada):

  1. Kami sempat memiliki perbedaan pendapat mengenai kutipan ketiga yang berbunyi  "Tim menemukan bahwa kode mereka menulis asumsi seperti # network is always reliable, no need for retry dan tidak ada timeout sama sekali pada pemanggilan antar service (modul pesanan memanggil modul pembayaran dan menunggu tanpa batas waktu).", dimana pitfalls ini sangatlah mirip dengan tipe "The network is reliable" (Kafi) dan "Latency is zero" (Valen), namun kemudian satu anggota lagi (Yoga) mengemukakan jika kutipan tersebut cukup mirip dengan "Transport cost is zero" karena pesan tersebut mengindikasikan tim developer yang tidak memikirkan tentang skenario Traffic tinggi. pad kesimpulan kasus pada perbincangan ini diputuskan dengan latency zero karena bagi valen 
  2. Pada kutipan "Saat trafik naik, satu server yang menangani semua modul (pesanan, pembayaran, notifikasi kurir) kewalahan karena semuanya berjalan di satu proses monolitik yang sama" yoga mengatakan bahwa itu merupakan bandwidth is infinite, sedangkan kafi mengatakan bahwa itu merupakan single point of failure, tetapi kita sepakat bahwa itu adalah point of failure

## [Tanggal diskusi 2]
- ...

## Review Silang
- Valen mengomentari analisis Kafi: penjelasaan trade off kurang jelas karena hanya menyebut biaya yang besar, padahal masih ada hal lain yang perlu dipertimbangkan seperti pada saat maintenace.

## Log Penggunaan AI (Level 2)

> Wajib diisi sesuai kebijakan Level 2 di [`../RUBRIK-UMUM.md`](../RUBRIK-UMUM.md). Tulis "Tidak memakai AI" pada baris pertama jika memang tidak dipakai. Hanya untuk brainstorming ide/outline — bukan untuk kode/analisis/teks akhir.

| Tanggal | Tool AI | Prompt yang diberikan | Ringkasan saran/ide AI | Bagaimana diolah jadi tulisan/kode sendiri |
|---|---|---|---|---|
| ... | ... | ... | ... | ... |
