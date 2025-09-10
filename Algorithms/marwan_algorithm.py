import numpy as np

def create_distance_matrix(cities):
    num_cities = len(cities)
    distance_matrix = np.array([[np.linalg.norm(np.array(cities[i]) - np.array(cities[j])) 
                                 for j in range(num_cities)] for i in range(num_cities)])
    return distance_matrix

def marwan_algorithm(cities):
    n = len(cities)
    dist_matrix = create_distance_matrix(cities)
    path_indices = [0]
    unvisited = set(range(n)) - set(path_indices)
    
    while unvisited:
        last = path_indices[-1]
        nearest_dist = np.inf
        nearest_city_index = None
        for city_index in unvisited:
            if dist_matrix[last, city_index] < nearest_dist:
                nearest_dist = dist_matrix[last, city_index]
                nearest_city_index = city_index
        
        #Dynamic evaluation for insertion
        best_insertion_cost = np.inf
        best_position = 0
        for i in range(len(path_indices)):
            next_i = (i + 1) % len(path_indices)
            insertion_cost = dist_matrix[path_indices[i], nearest_city_index] + dist_matrix[nearest_city_index, path_indices[next_i]] - dist_matrix[path_indices[i], path_indices[next_i]]
            
            #Penalty
            average_length = sum([dist_matrix[path_indices[j], path_indices[(j + 1) % len(path_indices)]] for j in range(len(path_indices))]) / len(path_indices)
            penalty = abs(dist_matrix[path_indices[i], nearest_city_index] - average_length) + abs(dist_matrix[nearest_city_index, path_indices[next_i]] - average_length)
            
            total_cost = insertion_cost + penalty
            
            if total_cost < best_insertion_cost:
                best_insertion_cost = total_cost
                nearest_city_index = city_index
                best_position = i + 1
        
        path_indices.insert(best_position, nearest_city_index)
        unvisited.remove(nearest_city_index)
    
    return np.array([cities[index] for index in path_indices])