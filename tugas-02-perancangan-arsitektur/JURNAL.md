# Jurnal Proses — Tugas 2

## [Tanggal]
- Opsi arsitektur yang dipertimbangkan:
  Kelompok kami memutuskan untuk menggunakan keduanya yakni Service-Oriented Architecture (SOA) atau Publish-Subscribe. 
- Kenapa akhirnya pilih [SOA/Pub-Sub]: pertama kami menggunakan SOA untuk memecah proses monolith yakni semua service berada pada satu runtutan/ satu aplikasi, ini bisa bermasalah jika salah satu service mengalami kendala yang akan berakibat service lainya juga berkendala sehingga ini kurang baik untuk implementasi pada FoodGo. lalu untuk pub-sub berfungsi untuk menangani kendala apabila ada service yang melakukan request ke service lain namun service yang di tuju sedang tidak tersedia sedangkan service yang melakukan request masih harus melakukan request ke service lain. dan ini menjadi masalah ketika mau ada pembaruan/deploy ulang salah satu service. kedua solusi tersebut bertujuan untuk, pertama memecah service dari yang tadinya monolith, sedangakan untuk pub-sub untuk menangani bagaimana service berkomunikasi tanpa terlalu bergantung satu sama lain.
- Revisi diagram (versi 1 → versi 2, apa yang berubah dan kenapa): ...

## Log Penggunaan AI (Level 2)

> Wajib diisi sesuai kebijakan Level 2 di [`../RUBRIK-UMUM.md`](../RUBRIK-UMUM.md). Tulis "Tidak memakai AI" pada baris pertama jika memang tidak dipakai. Hanya untuk brainstorming ide/outline — bukan untuk kode/analisis/teks akhir.

| Tanggal | Tool AI | Prompt yang diberikan | Ringkasan saran/ide AI | Bagaimana diolah jadi tulisan/kode sendiri |
|---|---|---|---|---|
| ... | ... | ... | ... | ... |
