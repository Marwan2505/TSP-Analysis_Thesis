import numpy as np

def genetic_algorithm(cities, pop_size=500, elite_size=50, mutation_rate=0.01, generations=10000):
    distance_matrix = create_distance_matrix(cities)
    population = initialize_population(pop_size, len(cities))
    progress = []

    for _ in range(generations):
        population = evolve(population, elite_size, mutation_rate, distance_matrix)
        progress.append(rank_routes(population, distance_matrix)[0][1])
    
    best_route_index = rank_routes(population, distance_matrix)[0][0]
    best_route = population[best_route_index]
    
    return np.array([cities[i] for i in best_route])

def create_distance_matrix(cities):
    num_cities = len(cities)
    return np.array([[np.linalg.norm(np.array(cities[i]) - np.array(cities[j])) for j in range(num_cities)] for i in range(num_cities)])

def initialize_population(size, num_cities):
    return [np.random.permutation(num_cities) for _ in range(size)]

def evolve(population, elite_size, mutation_rate, distance_matrix):
    pop_ranked = rank_routes(population, distance_matrix)
    selection_results = selection(pop_ranked, elite_size)
    matingPool = mating_pool(population, selection_results)
    children = matingPool[:elite_size] 
    
    for i in range(len(matingPool) - elite_size):
        child = breed(matingPool[i], matingPool[len(matingPool) - i - 1])
        children.append(mutate(child, mutation_rate))
    
    return children

def rank_routes(population, distance_matrix):
    fitness_results = {}
    for i in range(len(population)):
        fitness_results[i] = calculate_route_length(population[i], distance_matrix)
    return sorted(fitness_results.items(), key=lambda x: x[1], reverse=False)

def selection(pop_ranked, elite_size):
    selection_results = []
    for i in range(elite_size):
        selection_results.append(pop_ranked[i][0])
    return selection_results

def mating_pool(population, selection_results):
    pool = [population[i] for i in selection_results]
    return pool

def breed(parent1, parent2):
    gene_a = int(np.random.random() * len(parent1))
    gene_b = int(np.random.random() * len(parent1))
    
    start_gene = min(gene_a, gene_b)
    end_gene = max(gene_a, gene_b)

    child_p1 = []
    child_p1.extend(parent1[start_gene:end_gene])
    child_p2 = [item for item in parent2 if item not in child_p1]

    child = child_p1 + child_p2
    return np.array(child)

def mutate(individual, mutation_rate):
    for swapped in range(len(individual)):
        if(np.random.random() < mutation_rate):
            swap_with = int(np.random.random() * len(individual))
            
            individual[swapped], individual[swap_with] = individual[swap_with], individual[swapped]
    return individual

def calculate_route_length(route, distance_matrix):
    return sum([distance_matrix[route[i], route[(i + 1) % len(route)]] for i in range(len(route))])