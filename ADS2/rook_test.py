def dfs(current_rook, remaining_rooks):
    for rook in remaining_rooks:
        if rook != current_rook:
            if current_rook[0] == rook[0] or current_rook[1] == rook[1]:
                r = dfs(rook, [x for x in remaining_rooks if x != current_rook])
                # print(r)
                if len(r) < len(remaining_rooks):
                    remaining_rooks = r
    return remaining_rooks


def minRooksLeft(board_size, coordinates):
    # each entry in coordinates array looks like this:
    # (x, y) - coordinates of the rook
    n = len(coordinates)
    rooks_left = board_size ** 2

    # start point
    for i in range(n):
        start_rook = coordinates[i]
        result = dfs(start_rook, coordinates)
        rooks_left = min(rooks_left, len(result))

    return rooks_left


if __name__ == '__main__':
    coordinates = [(0, 0), (0, 3), (3, 0)]
    print(minRooksLeft(4, coordinates))