import numpy as np
import math

def simulated_annealing_algorithm(cities, temp=10000, cooling_rate=0.001, temp_min=1):
    current_solution = np.arange(len(cities))
    np.random.shuffle(current_solution)
    
    distance_matrix = create_distance_matrix(cities)
    current_distance = calculate_total_distance(current_solution, distance_matrix)
    
    while temp > temp_min:
        new_solution = np.copy(current_solution)
        
        swap_first = np.random.randint(0, len(cities))
        swap_second = np.random.randint(0, len(cities))
        new_solution[swap_first], new_solution[swap_second] = new_solution[swap_second], new_solution[swap_first]
        new_distance = calculate_total_distance(new_solution, distance_matrix)
        
        if new_distance < current_distance:
            current_solution = np.copy(new_solution)
            current_distance = new_distance
        else:
            delta = new_distance - current_distance
            acceptance_probability = math.exp(-delta / temp)
            if np.random.random() < acceptance_probability:
                current_solution = np.copy(new_solution)
                current_distance = new_distance
        
        temp *= (1-cooling_rate)
    
    return [cities[i] for i in current_solution]


def calculate_total_distance(route, distance_matrix):
    num_cities = len(route)
    return sum([distance_matrix[route[i], route[(i+1) % num_cities]] for i in range(num_cities)])

def create_distance_matrix(cities):
    num_cities = len(cities)
    return np.array([[np.linalg.norm(np.array(cities[i]) - np.array(cities[j])) for j in range(num_cities)] for i in range(num_cities)])