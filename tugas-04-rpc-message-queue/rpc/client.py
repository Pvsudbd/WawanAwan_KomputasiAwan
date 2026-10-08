"""
Tugas 4 - Jalur A: RPC Client (simulasi modul Pesanan)
Jalankan server.py di terminal lain terlebih dahulu.
"""

import xmlrpc.client
import time


def main():
    # TODO 1: buat ServerProxy ke http://localhost:8000
    proxy = xmlrpc.client.ServerProxy("http://localhost:8000")  # ganti dengan xmlrpc.client.ServerProxy(...)

    print("Memanggil cek_saldo('user1') ... menunggu respons sinkron")
    start = time.time()
    # TODO 2: panggil proxy.cek_saldo("user1") dan cetak hasilnya + waktu tempuh
    #         (buktikan client BENAR-BENAR menunggu sampai server membalas)
    saldo = proxy.cek_saldo("user1")
    print(f"Saldo user1: {saldo} (waktu tempuh: {time.time() - start:.4f} detik)")

    print("Memanggil proses_pembayaran('user1', 20000) ...")

    start_bayar = time.time()
    # TODO 3: panggil proxy.proses_pembayaran("user1", 20000) dan cetak hasilnya
    hasil_bayar = proxy.proses_pembayaran("user1", 20000)
    print(f"Hasil pembayaran: {hasil_bayar} (waktu tempuh: {time.time() - start_bayar:.4f} detik)")


if __name__ == "__main__":
    main()
