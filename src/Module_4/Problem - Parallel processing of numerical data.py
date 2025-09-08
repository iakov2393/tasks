import json
import math
import multiprocessing
import random
import time
from concurrent.futures import ThreadPoolExecutor


def generate_data(n):
    return [random.randint(1, 1000) for _ in range(n)]




def process_number(number):
    if number < 2:
        return False
    for i in range(2, int(math.sqrt(number)) + 1):
        if number % i == 0:
            return False
    return True




def parallel_threads(data):
    with ThreadPoolExecutor() as executor:
        return list(executor.map(process_number, data))




def parallel_process_pool(data):
    with multiprocessing.Pool(processes=multiprocessing.cpu_count()) as pool:
        return pool.map(process_number, data)


def worker(input_queue, output_queue):
    while True:
        item = input_queue.get()
        if item is None:
            break
        output_queue.put(process_number(item))




def parallel_process_individual(data):
    input_queue = multiprocessing.Queue()
    output_queue = multiprocessing.Queue()
    num_processes = multiprocessing.cpu_count()
    processes = []

    for _ in range(num_processes):
        p = multiprocessing.Process(target=worker, args=(input_queue, output_queue))
        p.start()
        processes.append(p)

    for item in data:
        input_queue.put(item)

    for _ in range(num_processes):
        input_queue.put(None)

    results = []
    for _ in range(len(data)):
        results.append(output_queue.get())

    for p in processes:
        p.join()

    return results




def measure_time(func, *args):
    start = time.time()
    result = func(*args)
    end = time.time()
    return result, end - start




if __name__ == "__main__":
    N = 10000
    data = generate_data(N)

    print("Однопроцессная обработка... ")
    single_result, single_time = measure_time(list, map(process_number, data))
    print(f'Время: {single_time:.2f} сек')

    print("Параллельные потоки...")
    thread_result, thread_time = measure_time(parallel_threads, data)
    print(f'Время: {thread_time:.2f} сек')

    print("Пул процессов...")
    pool_result, pool_time = measure_time(parallel_process_pool, data)
    print(f'Время: {pool_time:.2f} сек')

    print("Отдельные процессы с очередью...")
    individual_result, individual_time = measure_time(parallel_process_individual, data)
    print(f'Время: {individual_time:.2f} сек')


    results_table = [
        ("Метод", "Время (сек)"),
        ("Однопроцессный", f"{single_time:.2f}"),
        ("ThreadPoolExecutor", f"{thread_time:.2f}"),
        ("multiprocessing.Pool", f"{pool_time:.2f}"),
        ("multiprocessing.Process", f"{individual_time:.2f}")
    ]

    col_with = max(len(str(word)) for row in results_table for word in row) + 2
    for row in results_table:
        print("".join(str(word).ljust(col_with) for word in row))

    with open("results.json", "w") as f:
        json.dump(single_result, f)

    print("\nРезультаты сохранены в файл results.json")
