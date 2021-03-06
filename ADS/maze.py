import math

def can_escape(maze, i=0, j=0):
    # (i, j) is the starting position
    # maze[x][y] = 0 <=> (x, y) cell is empty
    # maze[x][y] = 1 <=> (x, y) cell contains a wall
    n = len(maze)
    m = len(maze[0])
    if i == n - 1 and j == m - 1:
        return 1
    maze[i][j] = 1
    result = False
    for a, b in [(i - 1, j), (i, j - 1), (i + 1, j), (i, j + 1)]:
        if 0 <= a < n and 0 <= b < m and maze[a][b] == 0:
            result = result or can_escape(maze, a, b)
    maze[i][j] = 0
    return result

def fastest_escape_length(maze, i=0, j=0):
    n = len(maze)
    m = len(maze[0])
    if i == n - 1 and j == m - 1:
        return 1
    maze[i][j] = 1
    result = math.inf
    for a, b in [(i - 1, j), (i, j - 1), (i + 1, j), (i, j + 1)]:
        if 0 <= a < n and 0 <= b < m and maze[a][b] == 0:
            result = min(result, fastest_escape_length(maze, a, b) + 1)
    maze[i][j] = 0
    return result

def fastest_escapes(maze, i=0, j=0):
    n = len(maze)
    m = len(maze[0])
    if i == n - 1 and j == m - 1:
        return [[(i, j)]]
    maze[i][j] = 1
    result = []
    for a, b in [(i - 1, j), (i, j - 1), (i + 1, j), (i, j + 1)]:
        if 0 <= a < n and 0 <= b < m and maze[a][b] == 0:
            result += fastest_escapes(maze, a, b)
            if result:
                for x in result:
                    if (i, j) not in x:
                        x.insert(0, (i, j))
    maze[i][j] = 0
    if i == 0 and j == 0 and result:
        min_path = min([len(x) for x in result])
        result = list(filter(lambda x: len(x) == min_path, result))
    return result


def weighted_escape_length(maze, w, i=0, j=0):
    n = len(maze)
    m = len(maze[0])
    if i == n - 1 and j == m - 1:
        return 1
    w_here = w if maze[i][j] == 1 else 1
    maze[i][j] = -1 if maze[i][j] == 0 else -2
    result = math.inf
    for a, b in [(i - 1, j), (i, j - 1), (i + 1, j), (i, j + 1)]:
        if 0 <= a < n and 0 <= b < m and maze[a][b] not in [-1, -2]:
            result = min(result, weighted_escape_length(maze, w, a, b) + w_here)
    maze[i][j] = 0 if maze[i][j] == -1 else 1
    return result


def weighted_escapes(maze, w, i=0, j=0):
    n = len(maze)
    m = len(maze[0])
    if i == n - 1 and j == m - 1:
        return [[(i, j)]]
    maze[i][j] = -1 if maze[i][j] == 0 else -2
    result = []
    for a, b in [(i - 1, j), (i, j - 1), (i + 1, j), (i, j + 1)]:
        if 0 <= a < n and 0 <= b < m and maze[a][b] not in [-1, -2]:
            result += weighted_escapes(maze, w, a, b)
            if result:
                for x in result:
                    if (i, j) not in x:
                        x.insert(0, (i, j))
    maze[i][j] = 0 if maze[i][j] == -1 else 1
    if i == 0 and j == 0 and result:
        res = []
        min_path = math.inf
        for path in result:
            path_len = 0
            for cell in path:
                path_len += 1 if maze[cell[0]][cell[1]] == 0 else w
            if path_len < min_path:
                res = [path]
                min_path = path_len
            elif path_len == min_path:
                res.append(path)
        result = res
    return result


# some test.py code
if __name__ == "__main__":
    test_a = [
        [0, 0, 0],
        [1, 1, 0],
        [1, 1, 0]
    ]
    # should print 5  
    # print(fastest_escape_length(test_a))
    # should print 2
    # print(weighted_escape_length(test_a, 0))
    test_b = [
        [0, 0, 0],
        [1, 1, 1],
        [0, 0, 0]
    ]
    test_c = [
        [0, 0, 0],
        [1, 0, 0],
        [1, 1, 0]
    ]
    # should print inf
    # print(fastest_escape_length(test_b))
    # should print 5
    # print(weighted_escape_length(test_b, 1))
    # # should print 6
    # print(weighted_escape_length(test_b, 2))

    # should print [[(0, 0), (0, 1), (0, 2), (1, 2), (2, 2)]]
    # print(fastest_escapes(test_a))
    # should print []
    # print(fastest_escapes(test_b))
    #  [ [(0, 0), (0, 1), (0, 2), (1, 2), (2, 2)], [(0, 0), (0, 1), (1, 1), (1, 2), (2, 2)] 
    # print(fastest_escapes(test_c))
    # should print [5, 5, 5, 5, 5, 5]
    # print(list(map( len, fastest_escapes([[0 for _ in range(3)] for _ in range(3)]))))

    # should print [[(0, 0), (1, 0), (1, 1), (1, 2), (2, 2)]]
    # print(weighted_escapes(test_b, 0))
    # sould print [ [(0, 0), (1, 0), (2, 0), (2, 1), (2, 2)] ]
    # print(weighted_escapes(test_c, 0))
    # should print [[(0, 0), (1, 0), (2, 0), (2, 1), (2, 2)], [(0, 0), (0, 1), (1, 1), (2, 1), (2, 2)], [(0, 0), (0, 1), (0, 2), (1, 2), (2, 2)]]
    # the order of the paths within the list might be different
    print(weighted_escapes(test_b, 2))
