"""
Dany jest graf nieskierowany G = (V,E), funkcja c: E -> N dająca wagi krawędziom, oraz wyróżnione
wierzchołki s i t. Szukamy scieżki z s do t takiej, że najmniejsza waga krawędzi na tej ścieżce
jest jak największa. Należy zwrócić najmniejszą wagę krawędzi na znalezionej ścieżce.
(W praktyce ścieżki szukamy tylko koncepcyjnie.)
Implementacja z wykorzystaniem wyszukiwania binarnego i przegląd grafu metodami BFS/DFS.
"""
import os
from sys import setrecursionlimit
from dimacs import *

setrecursionlimit(20000)


def dfs(graph, visited, u, t, max_weight):
    if visited[u]:
        return False
    visited[u] = True
    if visited[t]:
        return True
    for v, weight in graph[u]:
        if weight >= max_weight and dfs(graph, visited, v, t, max_weight):
            return True
    return False


def binary_search(graph, L, l, r, s, t):
    while l <= r:
        mid = (l + r) // 2
        visited = [False] * len(graph)
        max_weight = L[mid][2]
        if dfs(graph, visited, s, t, max_weight):
            r = mid - 1
        else:
            l = mid + 1
    return l


def minimum_maximum_edge_weight_dfs(file_path):
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
    left = binary_search(graph, L, 0, len(L) - 1, s, t)
    return L[left][2]


directory = os.listdir("Graphs")
for i in directory:
    file_path = "Graphs/" + i
    result = minimum_maximum_edge_weight_dfs(file_path)
    if result == int(readSolution(file_path)):
        print(f"OK result {result} for {i}")
    else:
        print(f"WRONG result {result} for {i}")
