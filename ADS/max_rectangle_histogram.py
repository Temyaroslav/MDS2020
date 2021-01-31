def refresh_max(height: list, pos: list, end: int, max: int):
    '''
    helper func to return max rectangle using height and position stacks
    :param height: list, stack with histogram columns height
    :param pos: list, stack with histogram columns positions
    :param end: int, end of rectangle
    :param max: int, current max
    :return: int, max
    '''
    cur_max = (end - pos[-1]) * height[-1]
    max = cur_max if cur_max > max else max
    height.pop()
    p = pos.pop()

    return max, p


def max_rect(a):
    max_ = -1
    height, pos = [], []
    for i in range(len(a)):
        if not height or a[i] > height[-1]:
            height.append(a[i])
            pos.append(i)
        else:
            while height and height[-1] >= a[i]:
                max_, p = refresh_max(height, pos, i, max_)
            height.append(a[i])
            pos.append(p)
    while height:
        max_, p = refresh_max(height, pos, len(a) - 1, max_)

    return max_


if __name__ == '__main__':
    a = [1, 5, 4, 0, 3, 5, 6, 2, 1, 3]
    print(max_rect(a))
