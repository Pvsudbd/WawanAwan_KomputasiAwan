# Jurnal Proses — Tugas 6

## Implementasi find_successor
- Kesalahan pertama yang ditemui (mis. lupa wrap-around di ring): 
  Pas awal nyoba bikin logika successor, kami mikir kalau pencarian linear biasa pake perulangan `node_id >= key_hash`. Masalahnya muncul pas ada hash kurir yang nilainya ternyata lebih besar dari seluruh ID node yang lagi aktif di ring. Contohnya kasus `kurir-005` yang punya hash 175, pas node jakarta-1 (id=177) keluar, node paling besar di ring tinggal node surabaya (id=136). Karena gak ada ID node yang lebih besar dari 175, perulangannya selesai gitu aja tanpa nemu node tujuan, ujung-ujungnya fungsi malah ngembaliin `None`. Selain itu di kode template awal (`chordlama.py`), fungsinya juga masih berupa `pass` sehingga semua lookup kurir sempat gagal/None semua.

  ![alt text](bukti/ChordLama.png)

- Cara memperbaikinya: 
  Kami menambahkan sebuah logika yang menerapkan sifat melingkar (wrap-around) sesuai konsep Chord ring. Jadi setelah daftar ID node diurutin (`sorted_nodes`), kita cari node pertama yang `>= key_hash`. Tapi kalau perulangannya tembus sampai akhir dan tetep gak nemu node yang lebih besar, kita gak balikin `None`, melainkan kita puter balik ke awal ring dengan ngembaliin node paling pertama yaitu `sorted_nodes[0]`. 
  
  Dengan perbaikan ini, hash yang ngelewatin ujung ring (kayak kurir-005 hash 175) otomatis muter balik dan ditampung sama node paling kecil yaitu node bandung (id=40). Pas di-run ulang, semua lookup kurir langsung sukses dapet IP aslinya secara akurat:

  ![alt text](bukti/ChordFix.png)

## Skenario join/leave
- Hasil sebelum & sesudah node baru bergabung: ...
- Hasil sebelum & sesudah node keluar: ...

## Log Penggunaan AI (Level 2)

> Wajib diisi sesuai kebijakan Level 2 di [`../RUBRIK-UMUM.md`](../RUBRIK-UMUM.md). Tulis "Tidak memakai AI" pada baris pertama jika memang tidak dipakai. Hanya untuk brainstorming ide/outline — bukan untuk kode/analisis/teks akhir.

| Tanggal | Tool AI | Prompt yang diberikan | Ringkasan saran/ide AI | Bagaimana diolah jadi tulisan/kode sendiri |
|---|---|---|---|---|
| ... | ... | ... | ... | ... |
