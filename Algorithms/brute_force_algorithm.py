import numpy as np
from itertools import permutations

def brute_force_algorithm(cities):
    num_cities = len(cities)
    all_tours = permutations(range(num_cities))
    min_distance = float('inf')
    optimal_tour = None

    for tour in all_tours:
        distance = sum(np.linalg.norm(np.array(cities[tour[i]]) - np.array(cities[tour[(i + 1) 
                    % num_cities]])) for i in range(num_cities))
        
        if distance < min_distance:
            min_distance = distance
            optimal_tour = tour

    optimal_path = [cities[i] for i in optimal_tour]
    return np.array(optimal_path)