"""
Dany jest graf nieskierowany G = (V,E). Graf G nazywamy grafem przekątniowych (chordal), jeśli nie istnieje w nim
żaden cykl długości większej niż 3, w którym żadne dwa wierzchołki nie są połączone krawędzią nie należącą do cyklu
(taki cykl nazywany jest czasem dziurą – graph hole).
Zaimplementuj algorytm sprawdzający, czy zadany graf G jest grafem przekątniowym. Należy wykorzystać w tym celu
algorytm LexBFS opisany w dalszej części konspektu, oraz następującą alternatywną definicję grafu przekątniowego:
G jest przekątniowy wtedy i tylko wtedy gdy można uszeregować jego wierzchołki w ciąg v[1], v[2], ..., v[n] taki,
że każdy wierzchołek v[i] wraz ze swoimi sąsiadami którzy występują w tym ciągu przed v[i] tworzą klikę (graf pełny).
Takie uporządkowanie wierzchołków nazywamy kolejnością idealnej eliminacji (perfect elimination ordering – PEO).
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


def check_lex_BFS(G, visited):
    for v in visited[1:]:
        if not G[v].RN - {G[v].parent} <= G[G[v].parent].RN:
            return False
    return True


def PEO(file_path):
    V, L = loadWeightedGraph(file_path)
    G = [None] + [Node(i) for i in range(1, V + 1)]
    for (u, v, _) in L:
        G[u].connect_to(v)
        G[v].connect_to(u)
    visited = lex_BFS(G)
    return check_lex_BFS(G, visited)


directory = os.listdir("Graphs/chordal")
for i in directory:
    file_path = "Graphs/chordal/" + i
    result = PEO(file_path)
    solution = True
    if int(readSolution(file_path)) == 0:
        solution = False
    if result == solution:
        print(f"OK result {result} for {i}")
    else:
        print(f"WRONG result {result} for {i} answer is {solution}")
