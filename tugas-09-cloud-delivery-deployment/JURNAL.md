# Jurnal Proses — Tugas 9

## Diskusi deployment model
Deployment model yang dipilih kelompok kami adalah Hybrid Cloud, gabungan antara public dan private cloud <br>
Penjelasan per karakteristik NIST sebagai berikut : <br>
A. Resource pooling Data sensitif ditempatkan pada resource pool, private cloud, sehingga Negara memegang kendali penuh terhadap hypervisor, penyimpanan fisik, dan kunci enkripsi sesuai UU No. 27 Tahun 2022 tentang perlindungan data pribadi<br>
B. Rapid elasticity saat permintaan melonjak drastis, segmen public cloud melakukan auto-scaling secara instan tanpa memaksa pembelian hardware tambahan sementara<br>
C. Broad network access validasi layanan melalui berbagai jaringan tanpa harus menarik jalur fisik ke setiap titik<br>
D. On demand self service memproses node tambahan atau provisioning kuota API melalui portal mandiri saat ada kegiatan massal<br>
E. Measured service untuk pemanggilan API verifikasi dan mekanisme audit trail keamanan data<br>
- Opsi yang dipertimbangkan dan kenapa akhirnya memilih salah satu: ...

## Diskusi service model per komponen
- ...

## Log Penggunaan AI (Level 2)

> Wajib diisi sesuai kebijakan Level 2 di [`../RUBRIK-UMUM.md`](../RUBRIK-UMUM.md). Tulis "Tidak memakai AI" pada baris pertama jika memang tidak dipakai. Hanya untuk brainstorming ide/outline — bukan untuk kode/analisis/teks akhir.

| Tanggal | Tool AI | Prompt yang diberikan | Ringkasan saran/ide AI | Bagaimana diolah jadi tulisan/kode sendiri |
|---|---|---|---|---|
| 10/22/2026 | ChatGPT | Bagaimana perbandingan arsitektur hybrid cloud untuk instansi pemerintah: apa komponen yang boleh di public edge dan apa yang wajib di private core? | Komponen yang wajib di private: database master, enkripsi kunci HSM, data identitas mentah. Komponen yang aman di public edge: API gateway, caching query non-sensitif, web portal publik, dan verifikasi zero-knowledge. | Kami jadikan acuan dalam membagi komponen sistem kependudukan menjadi 2 zona arsitektur pada README bagian 1 dan 2. |
| 10/22/2026 | ChatGPT | Apa contoh risiko spesifik arsitektur hybrid cloud jika dipakai sistem kependudukan selain risiko generik downtime? | Risiko kebocoran data saat transit antar cloud private dan edge, serta risiko database master private overload karena thundering herd query dari ribuan gateway publik jika tidak dipasang rate limiting/caching. | Kami elaborasi poin ini menjadi Bab 3 (Analisis Risiko & Mitigasi) dengan menambahkan solusi tokenization dan rate limiting per instansi. |
