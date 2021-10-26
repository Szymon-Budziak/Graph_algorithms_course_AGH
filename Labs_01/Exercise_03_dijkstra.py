"""
Dany jest graf nieskierowany G = (V,E), funkcja c: E -> N dająca wagi krawędziom, oraz wyróżnione
wierzchołki s i t. Szukamy scieżki z s do t takiej, że najmniejsza waga krawędzi na tej ścieżce
jest jak największa. Należy zwrócić najmniejszą wagę krawędzi na znalezionej ścieżce.
(W praktyce ścieżki szukamy tylko koncepcyjnie.)
Implementacja z wykorzystaniem algorytmu a’la Dijkstra.
"""
import os
from dimacs import *
from queue import PriorityQueue
from math import inf


def dijkstra(graph, s, t):
    distance = [-inf] * len(graph)
    distance[s] = inf
    queue = PriorityQueue()
    queue.put((-distance[s], s))
    while not queue.empty():
        dist, u = queue.get()
        dist = -dist
        for v, weight in graph[u]:
            if distance[v] < min(weight, dist):
                distance[v] = min(weight, dist)
                queue.put((-distance[v], v))
    return distance[t]


def minimum_maximum_edge_weight_dijkstra(file_path):
    V, L = loadWeightedGraph(file_path)
    L.sort(key=lambda x: x[2], reverse=True)
    graph = [[] for _ in range(V)]
    for vertex1, vertex2, weight in L:
        vertex1 -= 1
        vertex2 -= 1
        graph[vertex1].append((vertex2, weight))
        graph[vertex2].append((vertex1, weight))
    s = 0
    t = 1
    return dijkstra(graph, s, t)


directory = os.listdir("Graphs")
for i in directory:
    file_path = "Graphs/" + i
    result = minimum_maximum_edge_weight_dijkstra(file_path)
    if result == int(readSolution(file_path)):
        print(f"OK result {result} for {i}")
    else:
        print(f"WRONG result {result} for {i}")
