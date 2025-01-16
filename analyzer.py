import time
from statistics import mean, median, variance
from multiprocessing import Pool
import os

def load_data(file_path):
    with open(file_path, "r") as file:
        numbers = list(map(int, file.read().split(",")))
    return numbers

# Funkcje dla wielu
def calculate_mean_chunk(chunk):
    return mean(chunk)
def calculate_median_chunk(chunk):
    return median(chunk)
def calculate_variance_chunk(chunk):
    return variance(chunk)

# Podział na chunki
def split_data(numbers, chunks):
    chunk_size = len(numbers) // chunks
    return [numbers[i:i + chunk_size] for i in range(0, len(numbers), chunk_size)]

# 1 wątek
def single_thread_calculations(numbers):
    start = time.time()
    avg = mean(numbers)
    med = median(numbers)
    var = variance(numbers)
    end = time.time()
    return avg, med, var, end - start

# wiele wątków
def multi_process_calculations(numbers):
    num_processes = os.cpu_count()  # Liczba procesów = liczba rdzeni
    chunks = split_data(numbers, num_processes)

    start = time.time()
    with Pool(processes=num_processes) as pool:
        means = pool.map(calculate_mean_chunk, chunks)
        medians = pool.map(calculate_median_chunk, chunks)
        variances = pool.map(calculate_variance_chunk, chunks)

    # łączenie wyników
    total_mean = sum(means) / len(means)
    total_median = median(medians)  # Przybliżona mediana
    total_variance = sum(variances) / len(variances)

    end = time.time()
    return total_mean, total_median, total_variance, end - start

def main():
    file_path = "lots_of_numbers.txt"
    print("Wczytywanie danych...")
    numbers = load_data(file_path)
    print(f"Załadowano {len(numbers)} liczb.\n")

    print("Obliczenia wieloprocesowe z podziałem na chunki...")
    avg, med, var, time_taken = multi_process_calculations(numbers)
    print(f"Średnia: {avg}, Mediana: {med}, Wariancja: {var}")
    print(f"Czas wykonania: {time_taken:.2f} sekund\n")

    print("Obliczenia jednowątkowe...")
    avg, med, var, time_taken = single_thread_calculations(numbers)
    print(f"Średnia: {avg}, Mediana: {med}, Wariancja: {var}")
    print(f"Czas wykonania: {time_taken:.2f} sekund\n")

if __name__ == "__main__":
    main()