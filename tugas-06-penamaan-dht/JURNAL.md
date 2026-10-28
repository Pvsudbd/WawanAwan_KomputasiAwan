# Jurnal Proses — Tugas 6

## Implementasi find_successor
- Kesalahan pertama yang ditemui (mis. lupa wrap-around di ring): ...
- Cara memperbaikinya: ...

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
