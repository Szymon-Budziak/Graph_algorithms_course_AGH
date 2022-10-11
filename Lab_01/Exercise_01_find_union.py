"""
Dany jest graf nieskierowany G = (V,E), funkcja c: E -> N dająca wagi krawędziom, oraz wyróżnione
wierzchołki s i t. Szukamy scieżki z s do t takiej, że najmniejsza waga krawędzi na tej ścieżce
jest jak największa. Należy zwrócić najmniejszą wagę krawędzi na znalezionej ścieżce.
(W praktyce ścieżki szukamy tylko koncepcyjnie.)
Implementacja z wykorzystaniem struktury find-union.
"""
import os
from Additional_functions.dimacs import *
from math import inf


class Node:
    def __init__(self, value):
        self.value = value
        self.rank = 0
        self.parent = self


def find(x):
    if x != x.parent:
        x.parent = find(x.parent)
    return x.parent


def union(x, y):
    x = find(x)
    y = find(y)
    if x == y:
        return
    if x.rank > y.rank:
        y.parent = x
    else:
        x.parent = y
        if x.rank == y.rank:
            y.rank += 1


def make_set(v):
    return Node(v)


def minimum_maximum_edge_weight_find_union(file_path):
    V, L = loadWeightedGraph(file_path)
    L.sort(key=lambda x: x[2], reverse=True)
    vertices = [make_set(j) for j in range(V)]
    s = 1
    t = 2
    result = inf
    for vertex1, vertex2, weight in L:
        union(vertices[vertex1 - 1], vertices[vertex2 - 1])
        result = min(result, weight)
        if find(vertices[s - 1]) == find(vertices[t - 1]):
            return result


directory = os.listdir("Graphs")
for i in directory:
    file_path = "Graphs/" + i
    result = minimum_maximum_edge_weight_find_union(file_path)
    if result == int(readSolution(file_path)):
        print(f"OK result {result} for {i}")
    else:
        print(f"WRONG result {result} for {i}")
