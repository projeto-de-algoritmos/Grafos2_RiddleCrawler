import random
import heapq

def randomWeightedGraph(num_nodes, num_edges, min_weight, max_weight):
    if num_edges > num_nodes * (num_nodes - 1) / 2:
        raise ValueError("Too many edges for the given number of nodes.")

    # Cria um grafo vazio feito de um dictionary de dictionaries
    graph = {node: {} for node in range(num_nodes)}

    # Gera um valor aleatório para as arestas
    while num_edges > 0:
        node1, node2 = random.sample(range(num_nodes), 2)

        # Impede a criação de aresta entre 0 e 14
        if node1 == 0 and node2 == 14 or node1 == 14 and node2 == 0:
            continue
        
        if node2 not in graph[node1]:
            weight = random.randint(min_weight, max_weight)
            graph[node1][node2] = weight
            graph[node2][node1] = weight
            num_edges = num_edges - 1

    return graph

def dijkstra(graph, start_node, end_node):
    # Create a dictionary to store the shortest distances from the start node
    distances = {node: float('inf') for node in graph}
    distances[start_node] = 0

    # Create a priority queue to store nodes and their tentative distances
    priority_queue = [(0, start_node)]

    # Create a dictionary to store the previous node in the shortest path
    previous_nodes = {}

    while priority_queue:
        current_distance, current_node = heapq.heappop(priority_queue)

        if current_node == end_node:
            break

        if current_distance > distances[current_node]:
            continue

        for neighbor, weight in graph[current_node].items():
            distance = current_distance + weight

            if distance < distances[neighbor]:
                distances[neighbor] = distance
                previous_nodes[neighbor] = current_node
                heapq.heappush(priority_queue, (distance, neighbor))

    path = []
    while end_node is not None:
        path.insert(0, end_node)
        end_node = previous_nodes.get(end_node, None)

    return path, distances

# Testing the graphs functions
'''
if __name__ == "__main__":
    num_nodes = 15
    num_edges = num_nodes + int(num_nodes / 2)
    min_weight = 10
    max_weight = 17
    start_node = 0
    end_node = 14
    
    shortest_path = [14]

    # Loop to create a graph that has a path between 0 and 14
    while(shortest_path == [14]):
        random_graph = randomWeightedGraph(num_nodes, num_edges, min_weight, max_weight)
        shortest_path, shortest_distance = dijkstra(random_graph, start_node, end_node)
    
    # Print the edges and their weights
    for node1, edges in random_graph.items():
        for node2, weight in edges.items():
            print(f"Edge ({node1}, {node2}) has weight {weight}")

    print(f"Nodes: {num_nodes} Edges: {num_edges}")
    print(f"Shortest path from {start_node} to {end_node}: {shortest_path}")
    print(f"Shortest distance from {start_node} to {end_node}: {shortest_distance}")
'''
        