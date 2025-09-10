import numpy as np

def nearest_neighbor_algorithm(cities):
    if not cities:
        return []

    cities_with_index = list(enumerate(cities))
    path_indices = [cities_with_index.pop(0)]

    while cities_with_index:
        last_city = path_indices[-1][1]
        nearest_city_tuple = min(
            cities_with_index,
            key=lambda city: np.linalg.norm(np.array(last_city) - np.array(city[1]))
        )
        path_indices.append(nearest_city_tuple)
        cities_with_index.remove(nearest_city_tuple)

    path_indices.append(path_indices[0])

    return np.array([cities[index] for index, city in path_indices])