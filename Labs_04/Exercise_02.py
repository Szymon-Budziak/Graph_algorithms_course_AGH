"""
Dany jest graf przekątniowy G = (V,E). Zaimplementuj algorytm znajdujący rozmiar największej kliki w G.
"""
import os
from Additional_functions.dimacs import *


class Node:
    def __init__(self, idx):
        self.idx = idx
        self.out = set()
        self.RN = set()
        self.parent = None

    def connect_to(self, v):
        self.out.add(v)


def lex_BFS(G):
    visited = []
    vertices = [set(range(1, len(G)))]
    while len(visited) < len(G) - 1:
        u = vertices[-1].pop()
        visited.append(u)
        idx = 0
        while idx < len(vertices):
            i = 0
            neighbour = vertices[idx] & G[u].out
            not_neighbour = vertices[idx] - neighbour
            if len(neighbour) > 0:
                vertices.insert(idx + 1, neighbour)
                i += 1
            if len(not_neighbour) > 0:
                vertices.insert(idx + 1, not_neighbour)
                i += 1
            vertices.remove(vertices[idx])
            idx += i
        new_vertices = []
        intersection = set()
        for v in visited:
            new_vertices.append(v)
            intersection.add(v)
        G[u].RN = intersection & G[u].out
        found = False
        while len(new_vertices) > 0 and not found:
            if {new_vertices[-1]} & G[u].RN == set():
                new_vertices.pop(-1)
            else:
                found = True
        if found:
            G[u].parent = new_vertices[-1]
    return visited


def max_clique(file_path):
    V, L = loadWeightedGraph(file_path)
    G = [None] + [Node(i) for i in range(1, V + 1)]
    for (u, v, _) in L:
        G[u].connect_to(v)
        G[v].connect_to(u)
    visited = lex_BFS(G)
    result = 0
    for v in visited:
        result = max(result, len(G[v].RN) + 1)
    return result


directory = os.listdir("Graphs/maxclique")
for i in directory:
    file_path = "Graphs/maxclique/" + i
    result = max_clique(file_path)
    solution = int(readSolution(file_path))
    if result == solution:
        print(f"OK result {result} for {i}")
    else:
        print(f"WRONG result {result} for {i} answer is {solution}")
