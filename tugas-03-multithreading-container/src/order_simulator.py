"""
Tugas 3 - Simulasi Pesanan Masuk dengan Multithreading

Skeleton ini sengaja belum lengkap. Isi bagian bertanda TODO.
Jangan mengubah nama fungsi (dipakai untuk pengecekan otomatis oleh asisten).
"""

import threading
import random
import time
import logging

# Konfigurasi format log yang bagus (menampilkan waktu, nama thread, dan pesan)
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s | %(threadName)-10s | %(message)s',
    datefmt='%H:%M:%S'
)

NUM_ORDERS = 100        # jumlah pesanan simulasi yang masuk
NUM_WORKERS = 10        # jumlah thread pekerja

# Counter bersama untuk menghitung total pesanan yang berhasil diproses.
# Sengaja rawan race condition jika diakses tanpa proteksi.
processed_count = 0

# Tambahan: Untuk melacak dan mencetak thread mana yang saling timpa (hanya untuk log)
tracker_lock = threading.Lock()
write_tracker = {}

# TODO 1: Buat objek Lock di sini untuk melindungi `processed_count`.
# lock = threading.Lock()


def process_order(order_id: int) -> None:
    """Proses satu pesanan. Dipanggil oleh tiap thread pekerja."""
    global processed_count, write_tracker

    # Simulasikan kerja nyata (mis. validasi, hitung total harga)
    time.sleep(random.uniform(0.001, 0.01))

    # TODO 2: Tambahkan increment `processed_count` DI SINI.
    # Langkah 1: jalankan dulu tanpa lock (increment biasa: processed_count += 1)
    #            dan buktikan hasil akhirnya sering salah (< NUM_ORDERS).
    # Langkah 2: bungkus increment dengan `with lock:` dan buktikan hasilnya
    #            selalu tepat NUM_ORDERS. Simpan bukti kedua kondisi ini
    #            di JURNAL.md / folder bukti/.
    
    # VERSI TANPA LOCK (Untuk memicu Race Condition)
    current = processed_count
    
    time.sleep(0.0001)
    
    processed_count = current + 1
    
    # Catat thread mana yang merubah angka menjadi ini
    thread_name = threading.current_thread().name
    with tracker_lock:
        if processed_count not in write_tracker:
            write_tracker[processed_count] = []
        write_tracker[processed_count].append(thread_name)


def worker(order_ids: list) -> None:
    """Satu thread pekerja memproses sekumpulan order_id."""
    for order_id in order_ids:
        process_order(order_id)


def main() -> None:
    order_ids = list(range(1, NUM_ORDERS + 1))

    # TODO 3: Bagi `order_ids` menjadi NUM_WORKERS bagian, buat satu
    # threading.Thread per bagian yang menjalankan `worker(...)`,
    # start semua thread, lalu join semua thread sebelum lanjut.
    threads = []
    
    chunk_size = len(order_ids) // NUM_WORKERS
    for i in range(NUM_WORKERS):
        start_idx = i * chunk_size
        end_idx = start_idx + chunk_size if i < NUM_WORKERS - 1 else len(order_ids)
        worker_orders = order_ids[start_idx:end_idx]
        
        t = threading.Thread(target=worker, args=(worker_orders,))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    print(f"\nTotal pesanan diproses: {processed_count} (seharusnya {NUM_ORDERS})")
    if processed_count != NUM_ORDERS:
        print("RACE CONDITION TERDETEKSI - lengkapi TODO 1 & TODO 2 dengan Lock!\n")
        print("--- DAFTAR THREAD YANG SALING TIMPA ---")
        for val, threads_list in sorted(write_tracker.items()):
            if len(threads_list) > 1:
                print(f"Angka {val} ditimpa bersamaan oleh {len(threads_list)} thread: {', '.join(threads_list)}")


if __name__ == "__main__":
    main()
