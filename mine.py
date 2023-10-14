import pyxel
import random
import heapq

# Steve class é o personagem para chegar até o diamante com uma vida estabelecida
class Steve:
    def __init__(self, x, y, life):
        self.x = x
        self.y = y
        # w = width e h = height eu acho
        self.w = 8
        self.h = 8
        self.life = life #atributo de vida
    
    def draw(self):

        pyxel.blt(self.x, self.y, 0, 16, 0, self.w, self.h)
        pyxel.text(self.x, self.y - 10, "Vida: " + str(self.life), 7)

# Define a classe Maze, que gera o labirinto e inclui lógica de Dijkstra
class Maze:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.graph = self.randomWeightedGraph(6, 10, 1, 20)
        self.steve = Steve(16, 16, 100)

    def randomWeightedGraph(self, num_nodes, num_edges, min_weight, max_weight):
        if num_edges > num_nodes * (num_nodes - 1) / 2:
            raise ValueError("Too many edges for the given number of nodes.")

        # Cria um grafo vazio feito de um dictionary de dictionaries
        graph = {node: {} for node in range(num_nodes)}

        # Gera um valor aleatório para as arestas
        while num_edges > 0:
            node1, node2 = random.sample(range(num_nodes), 2)

            if node2 not in graph[node1]:
                weight = random.randint(min_weight, max_weight)
                graph[node1][node2] = weight
                graph[node2][node1] = weight
                num_edges = num_edges - 1

        return graph

    def dijkstra(self, start, goal):
        distances = {node: float('inf') for node in self.graph}
        distances[start] = 0
        priority_queue = [(0, start)]
        previous_nodes = {}

        while priority_queue:
            current_distance, current_node = heapq.heappop(priority_queue)

            if current_node == goal:
                break

            if current_distance > distances[current_node]:
                continue

            for neighbor, weight in self.graph[current_node].items():
                distance = current_distance + weight

                if distance < distances[neighbor]:
                    distances[neighbor] = distance
                    previous_nodes[neighbor] = current_node
                    heapq.heappush(priority_queue, (distance, neighbor))

        path = []
        while goal is not None:
            path.insert(0, goal)
            goal = previous_nodes.get(goal, None)

        return path, distances

    def move_steve(self, target_node):
        # Implementação da lógica de movimento de Steve baseada no algoritmo de Dijkstra
        pass

    def draw(self):
        # Renderize o labirinto aqui
        for y in range(self.height):
            for x in range(self.width):
                pyxel.rect(x * 8, y * 8, 8, 8, 7)  # Isso representa uma célula do labirinto


# Define a classe App com a estrutura que você forneceu
class App:
    def __init__(self):
        pyxel.init(160, 120, title="Minecraft", fps=60)
        pyxel.load("assets/PYXEL_RESOURCE_FILE.pyxres")
        self.maze = Maze(20, 15)
        pyxel.run(self.update, self.draw)

    def update(self):
        # Atualize a lógica do jogo, incluindo o movimento de Steve
        target_node = 4  # Defina o nó de destino desejado
        self.maze.move_steve(target_node)

    def draw(self):
        pyxel.cls(0)
        self.maze.draw()
        self.maze.steve.draw()
        pyxel.text(10, 10, "Vida de Steve: " + str(self.maze.steve.life), 7)

# Início do Jogo
App()