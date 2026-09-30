
"""
Tugas 3 - Simulasi Pesanan Masuk dengan Multithreading

Skeleton ini sengaja belum lengkap. Isi bagian bertanda TODO.

Jangan mengubah nama fungsi (dipakai untuk pengecekan otomatis oleh asisten).
"""

import threading
import random
import time
import logging

# Konfigurasi format log yang bagus
# Menampilkan waktu, nama thread, dan pesan
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

# Untuk melacak dan mencetak thread mana yang saling timpa
tracker_lock = threading.Lock()
write_tracker = {}

# TODO 1: Buat objek Lock di sini untuk melindungi processed_count.
lock = threading.Lock()

# Barrier digunakan untuk memastikan semua worker sudah membaca
# processed_count sebelum melakukan penulisan.
barrier = threading.Barrier(NUM_WORKERS)


def process_order(order_id: int) -> None:
    """Proses satu pesanan. Dipanggil oleh tiap thread pekerja."""
    global processed_count, write_tracker

    # Simulasikan kerja nyata
    # Thread lain tetap dapat berjalan selama proses ini berlangsung.
    time.sleep(random.uniform(0.001, 0.01))

    # TODO 2: Tambahkan increment processed_count DI SINI.
    #
    # VERSI TANPA LOCK:
    # Setiap thread membaca nilai yang sama terlebih dahulu.
    current = processed_count

    # Menunggu sampai seluruh worker sudah membaca nilai counter.
    # Dengan begitu, race condition lebih mudah terlihat tanpa
    # menggunakan time.sleep untuk memancing race condition.
    barrier.wait()

    # Semua thread kemudian menulis hasilnya.
    processed_count = current + 1

    # Catat thread mana yang mengubah angka menjadi nilai tersebut.
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

    # TODO 3: Bagi order_ids menjadi NUM_WORKERS bagian,
    # buat satu threading.Thread per bagian yang menjalankan
    # worker(...), start semua thread, lalu join semua thread.
    threads = []

    chunk_size = len(order_ids) // NUM_WORKERS

    for i in range(NUM_WORKERS):
        start_idx = i * chunk_size

        end_idx = (
            start_idx + chunk_size
            if i < NUM_WORKERS - 1
            else len(order_ids)
        )

        worker_orders = order_ids[start_idx:end_idx]

        t = threading.Thread(
            target=worker,
            args=(worker_orders,)
        )

        threads.append(t)
        t.start()

    # Tunggu semua thread selesai.
    for t in threads:
        t.join()

    print(
        f"\nTotal pesanan diproses: "
        f"{processed_count} (seharusnya {NUM_ORDERS})"
    )

    if processed_count != NUM_ORDERS:
        print(
            "RACE CONDITION TERDETEKSI - "
            "lengkapi TODO 1 & TODO 2 dengan Lock!\n"
        )

        print("--- DAFTAR THREAD YANG SALING TIMPA ---")

        for val, threads_list in sorted(write_tracker.items()):
            if len(threads_list) > 1:
                print(
                    f"Angka {val} ditimpa bersamaan oleh "
                    f"{len(threads_list)} thread: "
                    f"{', '.join(threads_list)}"
                )


if __name__ == "__main__":
    main()

