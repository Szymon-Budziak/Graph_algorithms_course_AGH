"""
Dany jest graf nieskierowany G = (V,E). Spójnością krawędziową grafu G nazywamy minimalną liczbę krawędzi, po
których usunięciu graf traci spójność. Przykładowo:
    - spójność krawędziowa drzewa = 1,
    - spójność krawędziowa cyklu = 2,
    - spójność krawędziowa n-kliki = n-1.
Opracuj i zaimplementuj algorytm obliczający spójność krawędziową zadanego grafu G, wykorzystując algorytm
Forda-Fulkersona oraz następujący fakt:
(Tw. Mengera) Minimalna ilość krawędzi które należy usunąć by zadane wierzchołki s, t znalazły się w różnych
komponentach spójnych jest równa ilości krawędziowo rozłącznych ścieżek pomiędzy s i t.
Wskazówka: jak można zinterpretować ilość krawędziowo rozłącznych ścieżek jako problem maksymalnego przepływu?
"""
import os
from Additional_functions.dimacs import *
from collections import deque
from math import inf
from copy import deepcopy


def create_graph_and_edges(V, L):
    graph = [[] for _ in range(V)]
    edges = {}
    for i in range(len(L)):
        vertex1, vertex2, weight = L[i]
        vertex1 -= 1
        vertex2 -= 1
        L[i] = (vertex1, vertex2, weight)
    for vertex1, vertex2, weight in L:
        graph[vertex1].append((vertex2, weight))
    for vertex1, vertex2, weight in L:
        if (vertex1, weight) not in graph[vertex2]:
            graph[vertex2].append((vertex1, 1))
    for v in range(V):
        for (u, weight) in graph[v]:
            edges[(v, u)] = weight
    return graph, edges


def bfs(graph, edges, s, t, parent):
    queue = deque()
    visited = [False] * len(graph)
    visited[s] = True
    queue.append(s)
    while len(queue) > 0:
        u = queue.popleft()
        for (v, weight) in graph[u]:
            if not visited[v] and edges[(u, v)] != 0:
                visited[v] = True
                parent[v] = u
                queue.append(v)
                if visited[t]:
                    return True
    return visited[t]


def edmonds_karp_algorithm(graph, edges, s, t):
    parent = [None] * len(graph)
    max_flow = 0
    while bfs(graph, edges, s, t, parent):
        current_flow = inf
        current = t
        while current != s:
            current_flow = min(current_flow, edges[(parent[current], current)])
            current = parent[current]
        max_flow += current_flow
        v = t
        while v != s:
            u = parent[v]
            edges[(u, v)] -= current_flow
            edges[(v, u)] += current_flow
            v = parent[v]
    return max_flow


def edge_consistency(file_path):
    V, L = loadDirectedWeightedGraph(file_path)
    s = 0
    graph, edges = create_graph_and_edges(V, L)
    min_result = inf
    for i in range(1, V):
        copied_graph = deepcopy(graph)
        copied_edges = deepcopy(edges)
        min_result = min(min_result, edmonds_karp_algorithm(copied_graph, copied_edges, s, i))
    return min_result


connectivity_directory = os.listdir("Graphs/connectivity")
for i in connectivity_directory:
    # 'grid100x100' takes too long so i skip it
    if i != 'grid100x100':
        connectivity_file_path = "Graphs/connectivity/" + i
        connectivity_edmonds_karp_result = edge_consistency(connectivity_file_path)
        solution = int(readSolution(connectivity_file_path))
        if connectivity_edmonds_karp_result == solution:
            print(f"OK result {connectivity_edmonds_karp_result} for {i}")
        else:
            print(f"WRONG result {connectivity_edmonds_karp_result} for {i} answer is {solution}")
