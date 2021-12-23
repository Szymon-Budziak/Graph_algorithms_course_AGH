from data import runtests


def my_solve(V, k, edges):
    print("Ilosc wierzcholkow: {}, krawedzi: {}".format(V, len(edges)))
    print("Ilosc oddzialow: {}".format(k))
    for (a, b), losses in edges:
        # ...
        pass
    return 0


runtests(my_solve)
