import numpy as np

def ant_colony_algorithm(cities, num_ants=100, alpha=1.0, beta=2.0, evaporation_rate=0.5, iterations=100):
    num_cities = len(cities)
    distances = [[np.linalg.norm(np.array(cities[i]) - np.array(cities[j])) for j in range(num_cities)] for i in range(num_cities)]
    pheromone = [[1 / (num_cities ** 2) for _ in range(num_cities)] for _ in range(num_cities)]

    best_distance = float('inf')
    best_tour = None

    for iteration in range(iterations):
        ants = [Ant(alpha, beta, num_cities, distances) for _ in range(num_ants)]
        for ant in ants:
            city = np.random.randint(num_cities)
            while len(set(ant.tour)) < num_cities:
                city = ant.visit_city(city, pheromone)
            ant.distance += distances[ant.tour[-1]][ant.tour[0]]
            if ant.distance < best_distance:
                best_distance = ant.distance
                best_tour = ant.tour.copy()

        for i in range(num_cities):
            for j in range(num_cities):
                pheromone[i][j] *= (1 - evaporation_rate)
                for ant in ants:
                    if j in ant.tour and i in ant.tour:
                        i_index = ant.tour.index(i)
                        if ant.tour[(i_index + 1) % num_cities] == j:
                            pheromone[i][j] += 1.0 / ant.distance

    return np.array([cities[index] for index in best_tour]) if best_tour is not None else np.array([])
    
class Ant:

    def __init__(self, alpha, beta, num_cities, distances):
        self.alpha = alpha  #Pheromone importance
        self.beta = beta    #Distance priority
        self.num_cities = num_cities
        self.distances = distances
        self.tour = []      #The tour the ant takes
        self.distance = 0.0 #Total distance of the tour

    def visit_city(self, city, pheromone):
        if not self.tour:
            self.tour.append(city)
        unvisited = set(range(self.num_cities)) - set(self.tour)
        if not unvisited:
            return None
        probabilities = []
        for next_city in unvisited:
            prob = self.calculate_transition_probability(city, next_city, pheromone)
            probabilities.append((prob, next_city))
        probabilities.sort(reverse=True, key=lambda x: x[0])
        if probabilities:
            next_city = probabilities[0][1]
            self.tour.append(next_city)
            if len(self.tour) > 1:
                self.distance += self.distances[self.tour[-2]][next_city]
            return next_city
        return None

    def calculate_transition_probability(self, current_city, next_city, pheromone):
        tau = pheromone[current_city][next_city] ** self.alpha
        eta = (1.0 / self.distances[current_city][next_city]) ** self.beta
        return tau * eta
