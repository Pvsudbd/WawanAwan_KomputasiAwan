# Jurnal Proses — Tugas 3

## Percobaan tanpa Lock
- Hasil `processed_count` yang didapat: [DENGAN LOCK] Total pesanan diproses: 100 (seharusnya 100)
- Kenapa bisa meleset (jelaskan mekanisme race condition dengan kata sendiri): ...

## Percobaan dengan Lock
- Hasil `processed_count` setelah perbaikan: [TANPA LOCK] Total pesanan diproses: 10 (seharusnya 100)
RACE CONDITION TERDETEKSI - lengkapi TODO 1 & TODO 2 dengan Lock!

--- DAFTAR THREAD YANG SALING TIMPA (LOST UPDATE) ---
Angka counter 1 ditimpa bersamaan oleh 10 thread: WorkerThread-5, WorkerThread-6, WorkerThread-4, WorkerThread-3, WorkerThread-7, WorkerThread-2, WorkerThread-10, WorkerThread-8, WorkerThread-1, WorkerThread-9
Angka counter 2 ditimpa bersamaan oleh 10 thread: WorkerThread-1, WorkerThread-8, WorkerThread-4, WorkerThread-9, WorkerThread-10, WorkerThread-3, WorkerThread-7, WorkerThread-2, WorkerThread-6, WorkerThread-5
Angka counter 3 ditimpa bersamaan oleh 10 thread: WorkerThread-3, WorkerThread-7, WorkerThread-1, WorkerThread-2, WorkerThread-5, WorkerThread-6, WorkerThread-4, WorkerThread-8, WorkerThread-10, WorkerThread-9
Angka counter 4 ditimpa bersamaan oleh 10 thread: WorkerThread-4, WorkerThread-1, WorkerThread-3, WorkerThread-2, WorkerThread-8, WorkerThread-6, WorkerThread-7, WorkerThread-10, WorkerThread-5, WorkerThread-9
Angka counter 5 ditimpa bersamaan oleh 10 thread: WorkerThread-6, WorkerThread-3, WorkerThread-7, WorkerThread-8, WorkerThread-4, WorkerThread-1, WorkerThread-2, WorkerThread-9, WorkerThread-10, WorkerThread-5
Angka counter 6 ditimpa bersamaan oleh 10 thread: WorkerThread-2, WorkerThread-6, WorkerThread-4, WorkerThread-8, WorkerThread-3, WorkerThread-10, WorkerThread-5, WorkerThread-9, WorkerThread-7, WorkerThread-1
Angka counter 7 ditimpa bersamaan oleh 10 thread: WorkerThread-4, WorkerThread-7, WorkerThread-8, WorkerThread-9, WorkerThread-10, WorkerThread-1, WorkerThread-3, WorkerThread-5, WorkerThread-6, WorkerThread-2
Angka counter 8 ditimpa bersamaan oleh 10 thread: WorkerThread-8, WorkerThread-3, WorkerThread-4, WorkerThread-6, WorkerThread-2, WorkerThread-5, WorkerThread-7, WorkerThread-10, WorkerThread-9, WorkerThread-1
Angka counter 9 ditimpa bersamaan oleh 10 thread: WorkerThread-6, WorkerThread-7, WorkerThread-3, WorkerThread-2, WorkerThread-10, WorkerThread-8, WorkerThread-9, WorkerThread-1, WorkerThread-5, WorkerThread-4
Angka counter 10 ditimpa bersamaan oleh 10 thread: WorkerThread-2, WorkerThread-6, WorkerThread-3, WorkerThread-7, WorkerThread-10, WorkerThread-5, WorkerThread-1, WorkerThread-4, WorkerThread-8, WorkerThread-9

## Kendala Docker
- Error yang ditemui saat `docker build`/`docker run` dan cara memperbaikinya: ...

## Log Penggunaan AI (Level 2)

> Wajib diisi sesuai kebijakan Level 2 di [`../RUBRIK-UMUM.md`](../RUBRIK-UMUM.md). Tulis "Tidak memakai AI" pada baris pertama jika memang tidak dipakai. Hanya untuk brainstorming ide/outline — bukan untuk kode/analisis/teks akhir.

| Tanggal | Tool AI | Prompt yang diberikan | Ringkasan saran/ide AI | Bagaimana diolah jadi tulisan/kode sendiri |
|---|---|---|---|---|
| ... | ... | ... | ... | ... |
