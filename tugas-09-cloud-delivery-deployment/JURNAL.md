# Jurnal Proses — Tugas 9

## Diskusi deployment model
- Opsi yang dipertimbangkan dan kenapa akhirnya memilih salah satu: ...

## Diskusi service model per komponen
- ...

## Log Penggunaan AI (Level 2)

> Wajib diisi sesuai kebijakan Level 2 di [`../RUBRIK-UMUM.md`](../RUBRIK-UMUM.md). Tulis "Tidak memakai AI" pada baris pertama jika memang tidak dipakai. Hanya untuk brainstorming ide/outline — bukan untuk kode/analisis/teks akhir.

| Tanggal | Tool AI | Prompt yang diberikan | Ringkasan saran/ide AI | Bagaimana diolah jadi tulisan/kode sendiri |
|---|---|---|---|---|
| 10/22/2026 | ChatGPT | Bagaimana perbandingan arsitektur hybrid cloud untuk instansi pemerintah: apa komponen yang boleh di public edge dan apa yang wajib di private core? | Komponen yang wajib di private: database master, enkripsi kunci HSM, data identitas mentah. Komponen yang aman di public edge: API gateway, caching query non-sensitif, web portal publik, dan verifikasi zero-knowledge. | Kami jadikan acuan dalam membagi komponen sistem kependudukan menjadi 2 zona arsitektur pada README bagian 1 dan 2. |
| 10/22/2026 | ChatGPT | Apa contoh risiko spesifik arsitektur hybrid cloud jika dipakai sistem kependudukan selain risiko generik downtime? | Risiko kebocoran data saat transit antar cloud private dan edge, serta risiko database master private overload karena thundering herd query dari ribuan gateway publik jika tidak dipasang rate limiting/caching. | Kami elaborasi poin ini menjadi Bab 3 (Analisis Risiko & Mitigasi) dengan menambahkan solusi tokenization dan rate limiting per instansi. |
