"""
Dany jest graf skierowany G = (V,E), funkcja c: E -> N dająca wagi krawędziom, oraz wyróżnione wieżchołki s i t.
Należy znaleźć maksymalny przepływ w grafie G pomiędzy s i t, tzn. funkcję f: E -> N spełniającą warunki definicji
przepływu, zapewniającą największą przepustowość. Do rozwiązania zadania należy wykorzystać algorytm Forda-Fulkersona,
porównując dwie strategie znajdowania ścieżek powiększających:
    - przy użyciu przeszukiwania metodą DFS,
    - przy użyciu przeszukiwania metodą BFS (algorytm Edmondsa-Karpa).
"""
import os
from Additional_functions.dimacs import *
from collections import deque
from math import inf
from sys import setrecursionlimit

setrecursionlimit(20000)


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
            graph[vertex2].append((vertex1, 0))
    for v in range(V):
        for (u, weight) in graph[v]:
            edges[(v, u)] = weight
    return graph, edges


# DFS method


def dfs_visit(graph, edges, source, visited, parent):
    visited[source] = True
    for (v, weight) in graph[source]:
        if not visited[v] and edges[(source, v)] != 0:
            parent[v] = source
            dfs_visit(graph, edges, v, visited, parent)


def dfs(graph, edges, s, t, parent):
    visited = [False] * len(graph)
    dfs_visit(graph, edges, s, visited, parent)
    return visited[t]


def ford_fulkerson_algorithm_dfs(file_path):
    V, L = loadDirectedWeightedGraph(file_path)
    s = 0
    t = V - 1
    graph, edges = create_graph_and_edges(V, L)
    parent = [None] * len(graph)
    max_flow = 0
    while dfs(graph, edges, s, t, parent):
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


# BFS method


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
    return visited[t]


def edmonds_karp_algorithm_bfs(file_path):
    V, L = loadDirectedWeightedGraph(file_path)
    s = 0
    t = V - 1
    graph, edges = create_graph_and_edges(V, L)
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


flow_directory = os.listdir("Graphs/flow")
for i in flow_directory:
    flow_file_path = "Graphs/flow/" + i
    flow_dfs_result = ford_fulkerson_algorithm_dfs(flow_file_path)
    solution = int(readSolution(flow_file_path))
    if flow_dfs_result == solution:
        print(f"OK result {flow_dfs_result} for {i} for dfs method")
    else:
        print(f"WRONG result {flow_dfs_result} for {i} answer is {solution}")
    flow_bfs_result = edmonds_karp_algorithm_bfs(flow_file_path)
    if flow_bfs_result == solution:
        print(f"OK result {flow_bfs_result} for {i} for bfs method")
    else:
        print(f"WRONG result {flow_bfs_result} for {i} answer is {solution} for bfs method")
