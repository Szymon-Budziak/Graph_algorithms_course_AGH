"""
Proszę zaimplementować program obliczający spójność krawędziową grafu nieskierowanego G przy użyciu algorytmu
Stoera-Wagnera.

Problem znajdowania spójności krawędziowej sprowadza się do poszukiwania pary wierzchołków, pommiędzy którymi
maksymalny przepływ jest najmniejszy, stąd używając algorytmu przeznaczonego do tego problemu dostaniemy rozwiązanie
o mniejszej złożoności obliczeniowej (niż algorytm z Labs_02/Exercise_02.py).
"""
import os
from Additional_functions.dimacs import *
from queue import PriorityQueue
from math import inf


class Node:
    def __init__(self):
        self.edges = {}

    def add_edge(self, to, weight):
        self.edges[to] = self.edges.get(to, 0) + weight

    def del_edge(self, to):
        del self.edges[to]


def merge_vertices(graph, x, y):
    y_list = list(graph[y].edges.items())
    for vertex, weight in y_list:
        if vertex != x:
            graph[x].add_edge(vertex, weight)
            graph[vertex].add_edge(x, weight)
        graph[y].del_edge(vertex)
        graph[vertex].del_edge(y)


def minimum_cut_phase(graph, V):
    a = 1
    S = []
    queue = PriorityQueue()
    queue.put((0, a))
    visited = [False] * (V + 1)
    weights = [0] * (V + 1)
    while not queue.empty():
        v_weight, v = queue.get()
        if not visited[v]:
            S.append(v)
            visited[v] = True
            for u, u_weight in graph[v].edges.items():
                if not visited[u]:
                    weights[u] += u_weight
                    queue.put((-weights[u], u))
    s = S[-1]
    t = S[-2]
    result = 0
    for vertex, weight in graph[s].edges.items():
        result += weight
    merge_vertices(graph, t, s)
    return result


def stoer_wagner_algorithm(file_path):
    V, L = loadWeightedGraph(file_path)
    vertices = V
    graph = [Node() for _ in range(V + 1)]
    for vertex1, vertex2, weight in L:
        graph[vertex1].add_edge(vertex2, weight)
        graph[vertex2].add_edge(vertex1, weight)
    result = inf
    while vertices > 1:
        result = min(result, minimum_cut_phase(graph, V))
        vertices -= 1
    return result


directory = os.listdir("Graphs")
for i in directory:
    # 'grid100x100' takes too long so i skip it
    if i != "grid100x100":
        file_path = "Graphs/" + i
        result = stoer_wagner_algorithm(file_path)
        solution = int(readSolution(file_path))
        if result == solution:
            print(f"OK result {result} for {i}")
        else:
            print(f"WRONG result {result} for {i} answer is {solution}")
