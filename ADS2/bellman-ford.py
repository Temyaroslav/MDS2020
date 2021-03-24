def bellman_ford(start, n, edges):
    # Using edge list as a graph representation
    dist = [float('inf')] * n
    dist[start] = 0

    for _ in range(1, n):
        for v_from, v_to, cost in edges:
            dist[v_to] = min(dist[v_to], dist[v_from] + cost)

    return dist

# Week 2 task 1
def BellmanFord(weight_matrix, v_from):
    n, graph = len(weight_matrix), weight_matrix
    dist = [float("inf")] * n
    dist[v_from] = 0

    # for n - 1 number of edges
    for _ in range(1, n):
        for v_from in range(len(weight_matrix)):
            for v_to, cost in enumerate(weight_matrix[v_from]):
                dist[v_to] = min(dist[v_to], dist[v_from] + cost)

    return dist

# Week 2 task 2
def hasNegativeCycle(weight_matrix):
    n = len(weight_matrix)
    dist = [float("inf")] * n
    dist[0] = 0

    # for n - 1 number of edges
    for _ in range(1, n):
        for v_from in range(len(weight_matrix)):
            for v_to, cost in enumerate(weight_matrix[v_from]):
                dist[v_to] = min(dist[v_to], dist[v_from] + cost)

    for v_from in range(len(weight_matrix)):
        for v_to, cost in enumerate(weight_matrix[v_from]):
            if dist[v_from] != float('inf') and dist[v_from] + cost < dist[v_to]:
                return True

    return False


if __name__ == '__main__':
    weight_matrix = [[float('inf'), 5, 2],
                     [5, float('inf'), float('inf')],
                     [2, float('inf'), float('inf')]]
    # should print [0, 5, 2]
    print(BellmanFord(weight_matrix, v_from=0))

    weight_matrix = [[float('inf'), 5, 2],
                     [5, float('inf'), -10],
                     [2, -10, float('inf')]]
    # should print True
    print(hasNegativeCycle(weight_matrix))

