import math

def neighbours(i, j):
    return [(i - 1, j), (i, j - 1), (i + 1, j), (i, j + 1)]

def fastest_escape_length(maze, i=0, j=0):
    n = len(maze)
    m = len(maze[0])
    if i == n - 1 and j == m - 1:
        return 1
    maze[i][j] = 1
    result = math.inf
    for x, y in neighbours(i, j):
        if 0 <= x < n and 0 <= y < m and maze[x][y] == 0:
            result = min(result, fastest_escape_length(maze, x, y) + 1)
    maze[i][j] = 0
    return result

def fastest_escapes(maze, i=0, j=0):
    n = len(maze)
    m = len(maze[0])
    if i == n - 1 and j == m - 1:
        return [[(i, j)]]
    maze[i][j] = 1
    escapes = []
    min_len = math.inf
    for x, y in neighbours(i, j):
        if 0 <= x < n and 0 <= y < m and maze[x][y] == 0:
            escapes_xy = fastest_escapes(maze, x, y)
            if escapes_xy:
                escape_xy_len = len(escapes_xy[0])
                if escape_xy_len + 1 < min_len:
                    escapes = []
                if escape_xy_len + 1 <= min_len:
                    for esc in escapes_xy:
                        escapes.append([(i, j)] + esc)
                    min_len = escape_xy_len + 1
    maze[i][j] = 0
    return escapes

def weighted_escape_length(maze, w, i=0, j=0):
    n = len(maze)
    m = len(maze[0])
    if i == n - 1 and j == m - 1:
        return 1
    cur_cell = maze[i][j]
    maze[i][j] = 2
    result = math.inf
    step_cost = 1 if cur_cell == 0 else w
    for x, y in neighbours(i, j):
        if 0 <= x < n and 0 <= y < m and maze[x][y] != 2:
            result = min(result, weighted_escape_length(maze, w, x, y) + step_cost)
    maze[i][j] = cur_cell
    return result

def weighted_escapes(maze, w, i=0, j=0):
    n = len(maze)
    m = len(maze[0])
    if i == n - 1 and j == m - 1:
        return [[(i, j)]]
    cur_cell = maze[i][j]
    maze[i][j] = 2
    escapes = []
    min_len = math.inf
    for x, y in neighbours(i, j):
        step_cost = 1 if maze[i][j] == 0 else w
        if 0 <= x < n and 0 <= y < m and maze[x][y] != 2:
            escapes_xy = weighted_escapes(maze, w, x, y)
            if escapes_xy:
                escape_xy_len = sum([1 if maze[c][d] == 0 else w for c, d in escapes_xy[0]])
                if escape_xy_len + step_cost < min_len:
                    escapes = []
                if escape_xy_len + step_cost <= min_len:
                    for esc in escapes_xy:
                        escapes.append([(i, j)] + esc)
                    min_len = escape_xy_len + step_cost
    maze[i][j] = cur_cell
    return escapes



if __name__ == "__main__":
    lucky = [
        [0, 0, 0],
        [1, 1, 0],
        [1, 1, 0]
    ]
    print(fastest_escape_length(lucky))
    print(weighted_escape_length(lucky, 0))
    unlucky = [
        [0, 0, 0],
        [1, 1, 1],
        [0, 0, 0]
    ]
    print(fastest_escape_length(unlucky))
    print(weighted_escape_length(unlucky, 1))
    print(weighted_escape_length(unlucky, 2))

    print(fastest_escapes(lucky))
    print(fastest_escapes(unlucky))
    print(list(map(len, fastest_escapes([[0 for _ in range(3)] for _ in range(3)]))))

    print(weighted_escapes(unlucky, 0))
    print(weighted_escapes(unlucky, 2))