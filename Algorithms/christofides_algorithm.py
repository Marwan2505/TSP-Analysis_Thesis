import numpy as np
import networkx as nx

def christofides_algorithm(cities):
    
    G = create_complete_graph(cities)
    
    mst = nx.minimum_spanning_tree(G, weight='weight')
    
    odd_degree_vertices = [v for v, d in mst.degree() if d % 2 == 1]
    
    subgraph = G.subgraph(odd_degree_vertices)
    matching = nx.algorithms.matching.min_weight_matching(subgraph)
    
    multigraph = nx.MultiGraph()
    multigraph.add_edges_from(mst.edges(data=True))
    multigraph.add_edges_from((u, v, G[u][v]) for u, v in matching)
    
    eulerian_circuit = list(nx.eulerian_circuit(multigraph))
    
    path = []
    visited = set()
    for u, v in eulerian_circuit:
        if u not in visited:
            path.append(u)
            visited.add(u)
    path.append(path[0])
    
    tsp_path_coords = [cities[i] for i in path]
    
    return tsp_path_coords

def create_complete_graph(cities):
        G = nx.Graph()
        num_cities = len(cities)
        for i in range(num_cities):
            for j in range(i+1, num_cities):
                distance = np.linalg.norm(np.array(cities[i]) - np.array(cities[j]))
                G.add_edge(i, j, weight=distance)
        return G