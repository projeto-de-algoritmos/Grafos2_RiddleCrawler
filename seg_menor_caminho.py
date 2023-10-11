import networkx as nx
import random


def gerador_grafo_aleatorio(n, p):
	"""
	Gera um grafo aleatório com n nós e probabilidade p de existência
	de cada aresta, com pesos aleatórios nas arestas
	"""
	G = nx.erdos_renyi_graph(n, p)

	# Atribuindo pesos aleatórios às arestas
	for u, v in G.edges():
		weight = random.uniform(0.1, 1.0) #Peso aleatório no intervalo [0.1, 1.0]
		G[u][v]['weight'] = weight

	return G	

# Chame a função para gerar um grafo aleatório ponderado
grafo_ponderado = gerador_grafo_aleatorio(10, 0.3)
