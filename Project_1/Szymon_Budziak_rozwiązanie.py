from data import runtests
from math import inf
from queue import PriorityQueue, Queue


class Graph:
    def __init__(self, N, amount, paths):
        self.connections = [set() for _ in range(N + 1)]
        self.flow = dict()
        self.army_loss = dict()
        self.connections[0].add(1)
        self.army_loss[(0, 1)] = [0] * amount
        self.flow[(0, 1)] = 0
        self.flow[(1, 0)] = 0

        for (u, v), lost in paths:
            self.connections[u].add(v)
            self.connections[v].add(u)
            self.flow[(u, v)] = 0
            self.flow[(v, u)] = 0
            self.army_loss[(u, v)] = lost

    def __len__(self):
        return len(self.connections)


def residual_flow(graph, u, v):
    current_flow = graph.flow[(u, v)]
    current_loss = graph.army_loss.get((u, v), None)
    if current_flow == 0 and current_loss is not None:
        return len(current_loss) - current_flow, current_loss[0]
    elif 0 < current_flow < len(current_loss):
        return len(current_loss) - current_flow, current_loss[current_flow] - current_loss[current_flow - 1]
    elif current_flow < -1:
        current_loss = graph.army_loss[(v, u)]
        return -current_flow, current_loss[-current_flow - 2] - current_loss[-current_flow - 1]
    elif current_flow < 0:
        return -current_flow, -graph.army_loss[(v, u)][0]
    return None


def bellman_ford_relax(u, v, weight, distance, parent):
    if distance[v] > distance[u] + weight and parent[u] != v:
        distance[v] = distance[u] + weight
        parent[v] = u
        return True
    return False


def bellman_ford(graph, source):
    values = []
    for u in range(len(graph)):
        for v in graph.connections[u]:
            flow = residual_flow(graph, u, v)
            if flow is not None:
                values.append((u, v, flow[1]))
    distance = [inf] * len(graph)
    parent = [None] * len(graph)
    distance[source] = 0
    for i in range(len(graph) - 1):
        flag = False
        for u, v, weight in values:
            if bellman_ford_relax(u, v, weight, distance, parent):
                flag = True
        if not flag:
            return None
    for u, v, weight in values:
        if distance[v] > distance[u] + weight:
            parent[v] = u
            cycle = []
            v_copy = v
            for _ in range(len(graph)):
                v_copy = parent[v_copy]
            v = v_copy
            cycle.append(v)
            while v != v_copy or len(cycle) < 2:
                v = parent[v]
                cycle.append(v)
            cycle.reverse()
            return cycle
    return None


def dijkstra_relax(u, v, dist, distance, parent):
    if distance[v] > distance[u] + dist:
        distance[v] = distance[u] + dist
        parent[v] = u
        return True
    return False


def backtracking(t, parent):
    if parent[t] is None:
        return [t]
    return backtracking(parent[t], parent) + [t]


def dijkstra_algorithm(graph, s, t):
    queue = PriorityQueue()
    queue.put((0, s))
    parent = [None] * len(graph)
    distance = [inf] * len(graph)
    visited = [False] * len(graph)
    distance[s] = 0
    while not queue.empty():
        _, u = queue.get()
        for v in graph.connections[u]:
            flow = residual_flow(graph, u, v)
            if flow is not None and flow[1] >= 0:
                if not visited[v] and dijkstra_relax(u, v, flow[1], distance, parent):
                    queue.put((distance[v], v))
        visited[u] = True
    if distance[t] < inf:
        return backtracking(t, parent)
    return None


def bfs(graph, s, t):
    parent = [None] * len(graph)
    queue = Queue()
    visited = [False] * len(graph)
    visited[s] = True
    queue.put(s)
    while not queue.empty():
        u = queue.get()
        for v in graph.connections[u]:
            flow = residual_flow(graph, u, v)
            if flow is not None and flow[0] > 0 and not visited[v]:
                visited[v] = True
                parent[v] = u
                queue.put(v)
    if parent[t] is not None:
        return backtracking(t, parent)
    return None


def edmonds_karp(graph, s, t):
    max_flow = 0
    while True:
        bfs_path = bfs(graph, s, t)
        if bfs_path is not None:
            current_flow = inf
            idx = 0
            for u in bfs_path[1:]:
                current_flow = min(current_flow,
                                   len(graph.army_loss[(bfs_path[idx], u)]) - graph.flow[(bfs_path[idx], u)])
                idx += 1
        else:
            break
        idx = 0
        for u in bfs_path[1:]:
            graph.flow[(bfs_path[idx], u)] += current_flow
            graph.flow[(u, bfs_path[idx])] -= current_flow
            idx += 1
        max_flow += current_flow
    return max_flow


def negative_cycle(graph, cycle):
    cycle_cost = 0
    idx = 0
    for u in cycle[1:]:
        flow = residual_flow(graph, cycle[idx], u)
        if flow is not None:
            cycle_cost += flow[1]
            idx += 1
        else:
            return False
    return cycle_cost < 0


def min_cost_max_flow_algorithm(graph, s, t):
    while True:
        dijkstra_path = dijkstra_algorithm(graph, s, t)
        if dijkstra_path is not None:
            idx = 0
            for u in dijkstra_path[1:]:
                graph.flow[(dijkstra_path[idx], u)] += 1
                graph.flow[(u, dijkstra_path[idx])] -= 1
                idx += 1
        else:
            break
    edmonds_karp(graph, s, t)
    while True:
        current_cycle = bellman_ford(graph, t)
        if current_cycle is not None:
            while True:
                idx = 0
                for u in current_cycle[1:]:
                    graph.flow[(current_cycle[idx], u)] += 1
                    graph.flow[(u, current_cycle[idx])] -= 1
                    idx += 1
                if not negative_cycle(graph, current_cycle):
                    break
        else:
            break
    total_loss = 0
    for (u, v), flow in graph.flow.items():
        if flow > 0:
            total_loss += graph.army_loss[(u, v)][flow - 1]
    return total_loss


def army_march(N, amount, paths):
    graph = Graph(N, amount, paths)
    return min_cost_max_flow_algorithm(graph, 0, len(graph) - 1)


runtests(army_march)
