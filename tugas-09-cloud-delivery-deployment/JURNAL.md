# Jurnal Proses — Tugas 9

## Diskusi deployment model
Deployment model yang dipilih kelompok kami adalah Hybrid Cloud, gabungan antara public dan private cloud <br>
Penjelasan per karakteristik NIST sebagai berikut : <br>
A. Resource pooling Data sensitif ditempatkan pada resource pool, private cloud, sehingga Negara memegang kendali penuh terhadap hypervisor, penyimpanan fisik, dan kunci enkripsi sesuai UU No. 27 Tahun 2022 tentang perlindungan data pribadi<br>
B. Rapid elasticity saat permintaan melonjak drastis, segmen public cloud melakukan auto-scaling secara instan tanpa memaksa pembelian hardware tambahan sementara<br>
C. Broad network access validasi layanan melalui berbagai jaringan tanpa harus menarik jalur fisik ke setiap titik<br>
D. On demand self service memproses node tambahan atau provisioning kuota API melalui portal mandiri saat ada kegiatan massal<br>
E. Measured service untuk pemanggilan API verifikasi dan mekanisme audit trail keamanan data<br>
- Opsi yang dipertimbangkan dan kenapa akhirnya memilih salah satu:
  - **Private Cloud Murni (Kurang cocok)**: Opsi ini sempat kami pertimbangkan karena dari sisi keamanan data paling ideal (semuanya 100% di bawah kendali negara). Tapi akhirnya kami tolak karena *rapid elasticity*-nya sangat buruk untuk menghadapi lonjakan musiman (seperti masa pemilu atau pendaftaran sekolah serentak). Jika memaksakan private cloud, pemerintah harus membeli banyak server fisik mahal yang sebagian besar waktunya bakal menganggur di hari biasa (*idle* dan boros anggaran). Selain itu, menghubungkan ribuan instansi luar (seperti perbankan untuk e-KYC) langsung ke jaringan data center internal negara memiliki risiko keamanan jaringan yang sangat tinggi.
  - **Public Cloud Murni (Ditolak)**: Ditolak secara mutlak karena melanggar UU No. 27 Tahun 2022 (UU PDP). Data kependudukan yang sangat sensitif (NIK dan biometrik) tidak boleh disimpan di server *multi-tenant* milik pihak ketiga/swasta yang tidak terkontrol penuh oleh negara.
  - **Hybrid Cloud (Dipilih)**: Merupakan solusi paling seimbang. Data sensitif dan proses inti tetap dikunci aman di Private Cloud milik negara, sementara kebutuhan skalabilitas dan gerbang akses untuk ribuan instansi luar ditangani secara elastis oleh Public Cloud.

## Diskusi service model per komponen
- Pada Database kami sepakat untuk wajib IaaS di private negara dikarenakan kita harus memiliki kontrol penuh pada data masyarakat sampai di level konfigurasi OS
- Untuk API Gateway, Cache itu kami memliki PaaS karena kita tidak perlu untuk mengurus Virtual Machine satu per satu
- Untuk Portal Layanan Warga & Dashboard petugas itu mengunakan SaaS karena pada user tidak perlu tahu konfigurasi server di belakangnya

## Diskusi risiko spesifik dan mitigasi
- **Risiko 1: Kebocoran data sensitif saat transit antara segmen Public dan Private (*Data in Transit*)**
  - *Penjelasan Masalah*: Karena menggunakan model hybrid, data harus berlalu-lalang antara gateway di public cloud dengan database inti di private cloud negara. Jika jalur koneksi ini disadap atau ada celah keamanan, data pribadi warga (seperti NIK dan biometrik) bisa terekspos.
  - *Mitigasi*:
    1. Menggunakan jalur koneksi privat khusus (*Dedicated Leased Line / Direct Connect*) yang diamankan dengan enkripsi VPN IPsec ganda (TLS 1.3), sehingga komunikasi data antar cloud tidak pernah melewati jalur internet umum.
    2. Menerapkan mekanisme *Tokenization* dan validasi *Zero-Knowledge*. Pihak luar (seperti bank yang melakukan KYC) tidak pernah menerima data mentah biometrik; segmen publik hanya mengirimkan hasil verifikasi sederhana berupa status `match: true/false` atau token terenkripsi.

- **Risiko 2: Efek lonjakan akses publik yang membobol kapasitas database internal (*Thundering Herd / Database Overload*)**
  - *Penjelasan Masalah*: Segmen public cloud bisa melakukan *auto-scaling* secara instan untuk menampung lonjakan ribuan instansi saat musim pemilu/sekolah. Namun kapasitas fisik server database di private cloud negara tetap terbatas. Jika jutaan request dari public cloud langsung ditembakkan serentak ke database internal, database utama negara bisa mengalami *choke*, macet, atau bahkan *down*.
  - *Mitigasi*:
    1. Memasang *Rate Limiting* dan *API Throttling* ketat di layer PaaS (API Gateway publik), sehingga tiap instansi memiliki batasan kuota akses per detik agar beban tetap terkendali.
    2. Menempatkan *Distributed Cache* (seperti Redis) di public segment untuk query verifikasi yang berulang, serta menggunakan *Message Queue* (seperti RabbitMQ/Kafka) untuk menampung request ke dalam antrean yang teratur sebelum diproses oleh database utama.

## Log Penggunaan AI (Level 2)

> Wajib diisi sesuai kebijakan Level 2 di [`../RUBRIK-UMUM.md`](../RUBRIK-UMUM.md). Tulis "Tidak memakai AI" pada baris pertama jika memang tidak dipakai. Hanya untuk brainstorming ide/outline — bukan untuk kode/analisis/teks akhir.

| Tanggal | Tool AI | Prompt yang diberikan | Ringkasan saran/ide AI | Bagaimana diolah jadi tulisan/kode sendiri |
|---|---|---|---|---|
| 10/22/2026 | ChatGPT | Bagaimana perbandingan arsitektur hybrid cloud untuk instansi pemerintah: apa komponen yang boleh di public edge dan apa yang wajib di private core? | Komponen yang wajib di private: database master, enkripsi kunci HSM, data identitas mentah. Komponen yang aman di public edge: API gateway, caching query non-sensitif, web portal publik, dan verifikasi zero-knowledge. | Kami jadikan acuan dalam membagi komponen sistem kependudukan menjadi 2 zona arsitektur pada README bagian 1 dan 2. |
| 10/22/2026 | ChatGPT | Apa contoh risiko spesifik arsitektur hybrid cloud jika dipakai sistem kependudukan selain risiko generik downtime? | Risiko kebocoran data saat transit antar cloud private dan edge, serta risiko database master private overload karena thundering herd query dari ribuan gateway publik jika tidak dipasang rate limiting/caching. | Kami elaborasi poin ini menjadi Bab 3 (Analisis Risiko & Mitigasi) dengan menambahkan solusi tokenization dan rate limiting per instansi. |
| 11/23/2026 | Antigravity (Gemini) | Diskusi pemilihan model deployment (apakah private cloud murni cocok?) serta perumusan 2 risiko spesifik hybrid cloud dan alasan penolakan private cloud murni dalam bahasa yang mudah dipahami. | Menjelaskan trade-off kedaulatan data vs rapid elasticity musiman pemilu, alasan penolakan private cloud murni (CapEx idle & keamanan akses luar), serta mitigasi data in-transit dan database overload. | Kami formulasikan menjadi poin perbandingan opsi alternatif yang ditolak dan analisis risiko mitigasi yang manusiawi di JURNAL.md. |
| 11/23/2026 | Antigravity (Gemini) | Kalau negara mampu untuk membangun banyak server demi menggunakan private cloud, kenapa nggak? | Menjelaskan bahwa kendala bukan sekadar mampu beli hardware (CapEx), tapi: (1) Inefisiensi anggaran karena server ribuan unit menganggur di luar musim pemilu/PPDB serta hardware usang (depresiasi 3–5 tahun); (2) Karakteristik *rapid elasticity* NIST tidak terpenuhi karena pengadaan fisik butuh birokrasi berbulan-bulan saat lonjakan darurat; (3) Melebarnya celah serangan (*attack surface*) karena data center private harus membuka koneksi langsung ke ribuan instansi luar tanpa ada bumper/tameng proteksi DDoS di edge publik. | Kami gunakan sebagai argumen penguat alasan penolakan Private Cloud murni serta bahan penyusunan skenario tandingan kelompok di README. |
