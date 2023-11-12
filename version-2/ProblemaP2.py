import sys
from typing import Tuple
from collections import deque


def build_graph(keys: list[list[int]], k: int) -> Tuple[dict[int, list[int]], dict[int, list[int]]]:

    M = len(keys)
    N = len(keys[0])

    # Adjacency list
    # An edge 1 -> 2 means that boxes of key 2 are inside squares covered by boxes of key 1
    # I.e. key 1 must be used before key 2
    graph: dict[int, list[int]] = {i: set() for i in range(1, k + 1)}

    # For each key, which squares does it cover
    # The list contains the coordinates of the upper left and lower right corners
    areas: dict[int, list(int, int, int, int)] = {}

    # O(n^2)
    for i in range(M):
        for j in range(N):
            key = keys[i][j]
            if key not in areas:
                areas[key] = [i, j, i, j]
            else:
                areas[key] = [min(areas[key][0], i),
                              min(areas[key][1], j),
                              max(areas[key][2], i),
                              max(areas[key][3], j)]

    # O(n^2 * k)
    for i in range(M):
        for j in range(N):
            elem = keys[i][j]
            for key in areas:
                start_i, start_j, end_i, end_j = areas[key]
                if start_i <= i <= end_i and start_j <= j <= end_j and elem != key:
                    graph[key].add(elem)

    # The graph is built in O(n^2 * k)
    return graph, areas

def topological_sort(graph: dict[int, list[int]], start: int, used):
    """
    DFS-based iterative topological sort. 
    """

    seen = set()
    stack = [start]
    order = []

    while stack:
        v = stack[-1]
        if v not in seen:
            seen.add(v)
            if v in graph:
                stack.extend(graph[v])
        elif v not in used:
            stack.pop()
            order.append(v)
            used.add(v)
        else:
            stack.pop()

    return order  # return the topological order


def has_cycle(graph):
    # Inicializar un diccionario para rastrear el estado de visitado de cada nodo
    visit = {key: False for key in graph}
    # Inicializar un diccionario para rastrear el estado de recorrido de cada nodo durante DFS
    rec_stack = {key: False for key in graph}

    # Función DFS para verificar ciclos
    def dfs(node):
        visit[node] = True
        rec_stack[node] = True

        for neighbor in graph[node]:
            if not visit[neighbor]:
                if dfs(neighbor):
                    return True
            elif rec_stack[neighbor]:
                return True

        rec_stack[node] = False
        return False

    # Aplicar DFS a cada nodo no visitado
    for node in graph:
        if not visit[node]:
            if dfs(node):
                return True  # Se encontró un ciclo

    return False  # No hay ciclos en el grafo

def algorithm(keys: list[list[int]], k: int) -> list[str]:
    """
    Algorithm to solve the problem.
    """

    graph, areas = build_graph(keys, k)

    if has_cycle(graph):
        print("NO SE PUEDE")
        return
    
    finalorder = []
    used = set()
    sorted_keys = sorted(graph.keys(), key=lambda x: len(graph[x]), reverse=True)
    for key in sorted_keys:
        if key not in used:
            new_order = topological_sort(graph, key, used)
            finalorder.extend(new_order)
            for u in new_order:
                used.add(u)
            pass

    for p in range(len(finalorder)-1, -1, -1):
        key = finalorder[p]
        positions = areas[key]
        print(f"{key} {positions[0]+1} {positions[2]+1} {positions[1]+1} {positions[3]+1}")

def main():
    # python ProblemaP2.py < o.in > o.out
    # python ProblemaP2.py < alt.in > alt.out
    cases = int(sys.stdin.readline().strip())
    for _ in range(cases):
        m, n, k = map(int, sys.stdin.readline().strip().split())
        row = [list(map(int, sys.stdin.readline().strip().split())) for _ in range(m)]
        algorithm(row, k)

if __name__ == "__main__":
    main()