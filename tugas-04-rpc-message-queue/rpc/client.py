"""
Tugas 4 - Jalur A: RPC Client (simulasi modul Pesanan)
Jalankan server.py di terminal lain terlebih dahulu.
"""

import xmlrpc.client
import time


def main():
    proxy = xmlrpc.client.ServerProxy("http://localhost:8000")

    print("Memanggil cek_saldo('user1') ... menunggu respons sinkron")
    start = time.time()
    # TODO 2: panggil proxy.cek_saldo("user1") dan cetak hasilnya + waktu tempuh
    #         (buktikan client BENAR-BENAR menunggu sampai server membalas)

    saldo = proxy.cek_saldo("user1")
    print(f"Saldo user1: {saldo} (waktu tempuh: {time.time() - start:.4f} detik)")

    print("Memanggil proses_pembayaran('user1', 20000) ...")
    # TODO 3: panggil proxy.proses_pembayaran("user1", 20000) dan cetak hasilnya

    saldo_baru = proxy.proses_pembayaran("user1", 20000)
    print(f"Saldo user1 setelah transaksi: {saldo_baru}")

if __name__ == "__main__":
    main()
