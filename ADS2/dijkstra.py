from heapq import heappop, heappush


def dijkstra(start, graph):
    '''
    :param graph: adjacency list
    :param start:
    '''
    n = len(graph)
    dist = [float('inf')] * n
    heap = []
    visited = [False] * n

    heappush(heap, (0, start))
    dist[start] = 0

    while heap:
        d, v = heappop(heap)
        visited[v] = True

        if dist[v] < d:
            continue

        for u, cost in graph[v]:
            if not visited[u] and d + cost < dist[u]:
                dist[u] = d + cost
                heappush(heap, (dist[u], u))
    return dist


# Week 2 task 1
def dijkstra2(adj_matrix, v_from, v_to):
    n, graph = len(adj_matrix), adj_matrix
    dist = [float("inf")] * n
    heap = []
    visited = [False] * n

    heappush(heap, (0, v_from))
    dist[v_from] = 0

    while heap:
        d, v = heappop(heap)
        visited[v] = True

        if dist[v] < d:
            continue

        for u, cost in enumerate(adj_matrix[v]):
            if not visited[u] and d + cost < dist[u]:
                dist[u] = d + cost
                heappush(heap, (dist[u], u))

    return dist[v_to] if dist[v_to] != float('inf') else -1


def dijkstraPath(adj_matrix, v_from, v_to):
    n, graph = len(adj_matrix), adj_matrix
    heap, path = [], [[v_from] for _ in range(n)]

    dist = [float("inf")] * n
    visited = [False] * n

    heappush(heap, (0, v_from, [v_from]))
    dist[v_from] = 0

    while heap:
        d, v, p = heappop(heap)

        visited[v] = True

        if dist[v] < d:
            continue

        for u, cost in enumerate(adj_matrix[v]):
            if not visited[u] and d + cost < dist[u]:
                dist[u] = d + cost
                path[u] = p + [u]
                heappush(heap, (dist[u], u, path[u]))

    return -1 if dist[v_to] == float('inf') else path[v_to]


if __name__ == '__main__':
    adj_matrix = [[float('inf'), 5, 2],
                  [5, float('inf'), float('inf')],
                  [2, float('inf'), float('inf')]]
    # should print 2
    print(dijkstra2(adj_matrix, v_from=0, v_to=2))

    adj_matrix = [[0, 1], [4, 0]]
    print(dijkstraPath(adj_matrix, v_from=1, v_to=1))
