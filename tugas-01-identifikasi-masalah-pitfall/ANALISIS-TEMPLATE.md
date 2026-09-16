# Tugas 1 — Analisis Pitfall FoodGo

**Kelompok:** [nama kelompok]

| Nama | NIM | Kontribusi |
|---|---|---|
| Valen Jonathan Micelino Pasaribu | 10307240072 | Latency Zero |
| Muhammad Kafi Rijal | 10307240016 | [pitfall/bagian yang dikerjakan] |
| Yoga Perkasa Didik | 103072400106 | [pitfall/bagian yang dikerjakan] |

## Pitfall 1: Latency Zero — ditulis oleh Valen Jonathan Micelino Pasaribu

**Bukti di skenario:** "Tim menemukan bahwa kode mereka menulis asumsi seperti # network is always reliable, no need for retry"

**Kenapa ini keliru:** Karena komunikasi antar komponen dilakukan melalui jaringan sehingga selalu memiliki latency pada sistem terdistribusi. pada transaksi akan ada beberapa kondisi yang bisa membuat sebuah latency meningkat seperti, beban pada server yang meningkat, kondisi jaringan saat itu, dan  gangguan pada server. maka sistem yang menganggap komunikasi antar komponen akan berlangsung tanpa delay.

**Dampak ke FoodGo:** dampaknya adalah permintaan pada server akan terus menunggu karena tidak ada mekanisme timeout. dan ini akan berbahaya ketika server meminta banyak sekali permintaan, maka semakin banyak request yang tertahan dan menggunakan resource server seperti thread dan memory. ini juga berbahaya bagi server karena bisa overload dan crash.

**Solusi desain awal:** Menerapkan mekanisme timeout untuk setiap komunikasi antar service. dan jika suatu requast mengalami timeout maka requast akan diberentikan dan beban pada server bisa cepat dialokasikan ke request lainya. dan bagi request dihentikan dan sistem dapat menjalankan mekanisme penanganan kegagalan seperti retry.

**Trade-off:** trade off dari penggunaan timeout adalah ketika timeout terlalu cepat bisa saja transaksi yang masih diproses bisa di anggap gagal, sedangakan bila terlalu lama dapat menyebabkan resource tertahan ketika service bermasalah. maka diperlukan mekanisme tambahan seperti retry terbatas agar transaksi yang tidak bena benar gagal bisa mencoba kembali.

---

## Pitfall 2: Latency Zero — ditulis oleh Valen

(ulangi struktur di atas)

---

## Pitfall 3: [nama pitfall] — ditulis oleh [nama]

(ulangi struktur di atas)

---

## Kesimpulan Kelompok

[Ringkasan: jika FoodGo memperbaiki ketiga pitfall ini, apa arsitektur yang disarankan secara garis besar? Kaitkan dengan Tugas 2.]
