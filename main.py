import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
import math
import time
from Algorithms.nearest_neighbor import nearest_neighbor_algorithm
from Algorithms.ant_colony_algorithm import ant_colony_algorithm
from Algorithms.simulated_annealing_algorithm import simulated_annealing_algorithm
from Algorithms.genetic_algorithm import genetic_algorithm
#from Algorithms.held_karp_algorithm import held_karp_algorithm
from Algorithms.brute_force_algorithm import brute_force_algorithm
from Algorithms.christofides_algorithm import christofides_algorithm
from Algorithms.marwan_algorithm import marwan_algorithm

def plot_result(path, elapsed_time=None, total_distance=None):
    if path.size == 0:
        print("No path to plot.")
        return
    if not np.array_equal(path[0], path[-1]):
        path = np.vstack([path, path[0]])

    normalized_path = normalize_coordinates(path)
    plt.figure(figsize=(10, 6))
    xs, ys = zip(*normalized_path)
    plt.plot(xs, ys, 'o-', label='Path')
    plt.scatter(xs[0], ys[0], c='red', label='Start')
    plt.title("Resulting Path (Normalized)")
    plt.xlabel("X Coordinate (Normalized)")
    plt.ylabel("Y Coordinate (Normalized)")
    if elapsed_time is not None and total_distance is not None:
        plt.suptitle(f"Total Distance: {total_distance:.2f}, Time: {elapsed_time:.3f} seconds", fontsize=10, y=0.95)
    plt.legend()
    plt.show()

def main():
    file_path = input("Enter the path to the cities file: ")
    try:
        global cities
        cities = load_cities_from_file(file_path)
        if not cities:
            print("No cities loaded, please check your file.")
            return
    except FileNotFoundError:
        print(f"File not found: {file_path}")
        return

    start_from_last = input("Start from the first or last set of coordinates? (f/l): ").lower().strip() == 'l'
    if start_from_last:
        cities = [cities[-1]] + cities[:-1]

    algorithms = {
        '1': ("Nearest Neighbor Algorithm", nearest_neighbor_algorithm),
        '2': ("Christofides' Algorithm", christofides_algorithm),
        '3': ("Ant Colony Algorithm", ant_colony_algorithm),
        '4': ("Simulated Annealing Algorithm", simulated_annealing_algorithm),
        '5': ("Genetic Algorithm", genetic_algorithm),
        '6': ("Brute Force Algorithm", brute_force_algorithm),
        '7': ("Marwan Algorithm", marwan_algorithm),
        '8': ("Random Path Algorithm", random_path_algorithm)
    }

    while True:
        print("\nSelect an algorithm:")
        for key, (name, _) in algorithms.items():
            print(f"{key}. {name}")
        print("0. Exit")

        choice = input("Enter your choice: ")
        if choice == '0':
            break

        _, algorithm = algorithms.get(choice, (None, None))
        if algorithm:
            start_time = time.time()
            path = algorithm(cities)
            end_time = time.time()

            path = np.array(path)
            if path.size > 0:
                if start_from_last:
                    start_index = np.where((path == cities[0]).all(axis=1))[0][0]
                    path = np.roll(path, -start_index, axis=0)

                total_distance = calculate_total_distance_main(path)
                print(f"Total distance: {total_distance:.2f}")

            elapsed_time = end_time - start_time
            print(f"Execution time: {elapsed_time:.3f} seconds")
            plot_result(path, elapsed_time=elapsed_time, total_distance=total_distance)
            save_path_to_file(path)

def load_cities_from_file(filepath):
    cities = []
    with open(filepath, 'r') as file:
        for line in file:
            parts = line.strip().split(',')
            if len(parts) == 2:
                try:
                    x, y = float(parts[0]), float(parts[1])
                    cities.append((x, y))
                except ValueError as e:
                    print(f"Error parsing line '{line.strip()}': {e}")
    return cities

def normalize_coordinates(cities):
    xs, ys = zip(*cities)
    min_x, max_x = min(xs), max(xs)
    min_y, max_y = min(ys), max(ys)
    range_x = max_x - min_x
    range_y = max_y - min_y

    normalized_cities = [((x - min_x) / range_x, (y - min_y) / range_y) for x, y in cities]
    return normalized_cities

def calculate_total_distance_main(path):
    total_distance = 0
    if len(path) > 1:
        for i in range(len(path) - 1):
            total_distance += np.linalg.norm(np.array(path[i]) - np.array(path[i + 1]))
        total_distance += np.linalg.norm(np.array(path[-1]) - np.array(path[0]))
    return total_distance

def save_path_to_file(path, file_name="Results.txt"):
    if len(path) > 1 and not np.array_equal(path[0], path[-1]):
        path = np.vstack([path, path[0]])

    with open(file_name, 'w') as f:
        for point in path:
            f.write(f"{point[0]}, {point[1]}\n")
    print(f"Path saved to {file_name}")

def random_path_algorithm(cities):
    num_cities = len(cities)
    path_indices = np.random.permutation(num_cities)
    path = np.array(cities)[path_indices]
    return path

if __name__ == "__main__":
    main()


