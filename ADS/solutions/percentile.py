import math


def find_percentile(a, b, p=50):
    if len(a) < len(b):
        a, b = b, a
    n, m = len(a), len(b)
    k = int(math.ceil(float(n + m) * (p / 100.0)))
    if m == 0:
        return a[k - 1]
    left = max(0, k - m)
    right = min(n, k)
    while left <= right:
        i = (left + right) // 2
        j = k - i
        if (i > 0 and j < m and a[i - 1] > b[j]):
            right = i - 1
        elif (j > 0 and i < n and b[j - 1] > a[i]):
            left = i + 1
        else:
            break
    if i == 0:
        mid = b[j - 1]
    elif j == 0:
        mid = a[i - 1]
    else:
        mid = max(a[i - 1], b[j - 1])
    return mid


# some test code
if __name__ == "__main__":
    test_a, test_b, test_p = [1, 2, 7, 8, 10], [6, 12], 50
    # should print 7
    print(find_percentile(test_a, test_b, test_p))

    test_a, test_b, test_p = [1, 2, 7, 8], [6, 12], 50
    # should print 6
    print(find_percentile(test_a, test_b, test_p))

    test_a, test_b, test_p = [15, 20, 35, 40, 50], [], 30
    # should print 20
    print(find_percentile(test_a, test_b, test_p))

    test_a, test_b, test_p = [15, 20], [25, 40, 50], 40
    # should print 20
    print(find_percentile(test_a, test_b, test_p))
