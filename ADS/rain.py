def calc_rain_water(h):
    size = 100000
    left, right = [0] * size, [0] * size
    water = 0

    left[0] = h[0]
    for i in range(1, len(h)):
        left[i] = max(left[i - 1], h[i])

    right[len(h) - 1] = h[len(h) - 1]
    for i in range(len(h) - 2, -1, -1):
        right[i] = max(right[i + 1], h[i])

    for i in range(len(h)):
        water += min(left[i], right[i]) - h[i]

    return water


# some test.py code
if __name__ == "__main__":
    test_h = [2, 5, 2, 3, 6, 9, 1, 3, 4, 6, 1]
    # should print 15
    print(calc_rain_water(test_h))

    test_h = [2, 4, 6, 8, 6, 4, 2]
    # should print 0
    print(calc_rain_water(test_h))

    test_h = [8, 6, 4, 2, 4, 6, 8]
    # should print 18
    print(calc_rain_water(test_h))