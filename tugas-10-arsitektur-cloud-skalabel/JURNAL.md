# Jurnal Proses — Tugas 10

## Setup Nginx & multi-instance
- Kendala saat konfigurasi upstream:
  - Saat kami mengonfigurasi `upstream` di Nginx, kami harus mendefinisikan nama service backend (`app1:8000`, `app2:8000`, `app3:8000`) agar terhubung dalam satu network Docker Compose. Kami juga memastikan mapping port luar 8080 di Nginx diteruskan ke port 8000 di masing-masing backend.
  
- **Eksperimen Failover (Simulasi Instance Dimatikan)**:
  - Ketika `app2` kami matikan secara sengaja menggunakan perintah `docker compose stop app2`, kami langsung menjalankan `load_test.py` untuk mengamati bagaimana reaksi Nginx.
  - **Hasil yang kami dapatkan**: Dari 300 request, `app3` menangani 141 request, `app1` menangani 139 request, dan muncul **20 request ERROR** dengan durasi total yang membengkak menjadi **16.06 detik**.
  - **Analisis kami**: Setelah kami telusuri, Nginx open-source ternyata menggunakan mekanisme *passive health check*. Artinya, Nginx tidak mengecek status server secara proaktif, melainkan baru tahu `app2` mati saat mencoba mengirim request ke sana dan mengalami kegagalan (*connection refused/timeout*). Sebanyak 20 request awal itulah yang gagal. Namun begitu Nginx menyadari `app2` tidak merespons (mencapai batas `max_fails`), Nginx langsung menandai `app2` sebagai *unhealthy* dan secara otomatis mengalihkan sisa request berikutnya hanya ke `app1` dan `app3` tanpa membuat seluruh sistem tumbang.
  - Bukti screenshot failover kami: [`bukti/Failover.png`](bukti/Failover.png)

## Hasil Load Test Horizontal (3 instance)
- Distribusi request per instance:
  - Pada pengujian awal dengan 3 instance aktif (`app1`, `app2`, `app3`), kami mengirim 300 request konkuren dengan concurrency 30 thread.
  - Kami melihat beban terbagi rata secara otomatis dengan algoritma default *Round-Robin*, di mana tiap instance menangani porsi yang seimbang sekitar **~100 request per instance** tanpa ada error sama sekali.
  - Bukti pengujian awal kami: [`bukti/BuktiCurl.png`](bukti/BuktiCurl.png) dan [`bukti/DockComp.png`](bukti/DockComp.png)

## Hasil Setelah Scale-up (4 instance)
- Distribusi request per instance:
  - Kami kemudian melakukan simulasi *horizontal scale-up* secara manual dengan menambahkan service `app4` di `docker-compose.yml` dan mendaftarkan `server app4:8000;` ke blok `upstream` di `nginx/nginx.conf`.
  - Setelah cluster kami build dan restart ulang, kami jalankan load test 300 request lagi dan mendapatkan hasil yang sangat presisi:
    - `app1`: 75 request
    - `app2`: 75 request
    - `app3`: 75 request
    - `app4`: 75 request
  - Seluruh 300 request berhasil kami selesaikan dalam waktu **3.81 detik** dengan tingkat kegagalan 0% (semua request sukses). Beban terbagi rata tepat 25% untuk masing-masing dari 4 instance.
  - Bukti scale-up 4 instance kami: [`bukti/H_Scaleup.png`](bukti/H_Scaleup.png)

## Hasil Vertical Scaling (1 instance besar)
- Latensi/kegagalan dibanding horizontal:
  - Untuk perbandingan, kami mematikan cluster 4 instance dan menjalankan **1 instance besar saja** langsung di port 8080 menggunakan batas resource CPU dan RAM lebih tinggi (`docker run -d --name app_vertical -p 8080:8000 --cpus=2 --memory=1g -e INSTANCE_ID=app_single_vertical ...`).
  - **Hasil yang kami amati**: Seluruh 300 request ditangani oleh satu instance (`app_single_vertical: 300 request`) dan selesai dalam waktu **1.92 detik** tanpa error.
  - **Hasil diskusi dan perbandingan kelompok kami**:
    - **Dari segi latensi lokal**: Di pengujian skala kecil laptop kami, 1 instance besar memang terasa sedikit lebih cepat (1.92 detik vs 3.81 detik) karena request langsung masuk ke aplikasi tanpa harus melewati proses *proxy passing* dari Nginx.
    - **Dari segi ketahanan (kasus TicketGo)**: Walaupun cepat di beban rendah, kelompok kami menyimpulkan bahwa 1 instance besar sangat berbahaya karena memiliki **Single Point of Failure (SPOF)**. Kalau ada lonjakan 1 juta user mendadak seperti di kasus TicketGo dan server kehabisan CPU/RAM, satu-satunya server itu akan langsung mati dan layanan lumpuh total. Berbeda dengan Horizontal Scaling yang kami uji di atas, sistem punya sifat *fault tolerance*, meskipun satu server mati, Load Balancer tetap bisa membagi beban ke server lain yang masih hidup.
  - Bukti pengujian vertical scaling kami: [`bukti/Vert_scaling.png`](bukti/Vert_scaling.png)

## Keterbatasan Simulasi vs Auto-Scaling Cloud Nyata
- **Keterbatasan Simulasi:**
  - Masih serba manual: menambah instance harus mengedit `docker-compose.yml` dan `nginx.conf` lalu restart container.
  - Tidak sanggup merespons lonjakan mendadak karena server keburu tumbang sebelum admin sempat melakukan scaling manual.
  - Tidak ada mekanisme scale-down otomatis saat sepi, sehingga berisiko memboroskan biaya/resource.
- **Komponen agar Menjadi Otomatis (seperti Cloud Asli):**
  1. *Metric Collector* (misal CloudWatch / Prometheus): memantau CPU, RAM, dan request per detik secara real-time.
  2. *Auto-Scaler Controller & Scaling Policy* (misal AWS ASG / Kubernetes HPA): otomatis memicu penambahan/pengurangan instance berdasarkan ambang batas (*threshold*).
  3. *Dynamic Discovery & Health Check*: mendaftarkan IP instance baru ke Load Balancer secara otomatis dan memastikan server sehat (`HTTP 200`) sebelum dialiri trafik.
  4. *Connection Draining*: memberi jeda waktu agar request yang sedang diproses selesai terlebih dahulu sebelum instance dimatikan saat scale-down.

## Log Penggunaan AI (Level 2)

> Wajib diisi sesuai kebijakan Level 2 di [`../RUBRIK-UMUM.md`](../RUBRIK-UMUM.md). Tulis "Tidak memakai AI" pada baris pertama jika memang tidak dipakai. Hanya untuk brainstorming ide/outline — bukan untuk kode/analisis/teks akhir.

| Tanggal | Tool AI | Prompt yang diberikan | Ringkasan saran/ide AI | Bagaimana diolah jadi tulisan/kode sendiri |
|---|---|---|---|---|
| 11/23/2026 | Antigravity (Gemini) | Bagaimana urutan eksekusi simulasi arsitektur cloud skalabel dan cara menguji failover serta scale-up manual 4 instance? | Memberikan panduan tahapan uji container, penjelasan fenomena passive health check Nginx yang menghasilkan 20 error saat failover, dan perbandingan konsep SPOF vertical vs fault tolerance horizontal. | Data metrik riil dari pengujian diolah dan dicatat ke dalam poin-poin jurnal proses serta menjadi dasar perbandingan arsitektur di README. |
