import random
import os
import time
from multiprocessing import Pool

def generate_chunk(args):
    chunk_size, num_range = args
    return [str(random.randint(1, num_range)) for _ in range(chunk_size)]

# 1 wątek
def single_thread_file_generation(output_file, number_of_elements, num_range=100):
    print("Generowanie jednowątkowe...")
    start_time = time.time()
    with open(output_file, "w") as file:
        for _ in range(number_of_elements):
            file.write(f"{random.randint(1, num_range)},")
    end_time = time.time()
    print(f"Generowanie jednowątkowe zakończone w czasie: {end_time - start_time:.2f} sekund")

# wiele wątków
def multi_process_file_generation(output_file, number_of_elements, num_range=100):
    num_processes = os.cpu_count()
    chunk_size = number_of_elements // num_processes

    print(f"Generowanie wielowątkowe z {num_processes} procesami...")
    print(f"Chunk size: {chunk_size}")

    start_time = time.time()
    # Przygotowanie argumentów dla każdego procesu
    args = [(chunk_size, num_range) for _ in range(num_processes)]

    with Pool(processes=num_processes) as pool:
        results = pool.map(generate_chunk, args)

    # Zapis wyników do pliku
    with open(output_file, "w") as file:
        for chunk in results:
            file.write(",".join(chunk) + ",")
    end_time = time.time()
    print(f"Generowanie wielowątkowe zakończone w czasie: {end_time - start_time:.2f} sekund")

if __name__ == "__main__":
    number_of_elements = 100000000
    output_file = "lots_of_numbers.txt"
    num_range = 100

    single_thread_file_generation(output_file, number_of_elements, num_range)
    multi_process_file_generation(output_file, number_of_elements, num_range)
