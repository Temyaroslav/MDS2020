import time
import math
import random

# Reference solution using merge sort


def merge(a, b):
    i, j = 0, 0
    res = []
    while i < len(a) and j < len(b):
        if a[i] < b[j]:
            res.append(a[i])
            i += 1
        else:
            res.append(b[j])
            j += 1
    while i < len(a):
        res.append(a[i])
        i += 1
    while j < len(b):
        res.append(b[j])
        j += 1
    return res


def merge_sort(a):
    '''
    Merge sort algorithm from the lectures
    '''
    if len(a) <= 1:
        return a
    mid = len(a) // 2
    left = merge_sort(a[:mid])
    right = merge_sort(a[mid:])
    return merge(left, right)


def find_percentile_slow(a, b, p):
    '''
    Reference solution for the p-th percentile problem
    :param a: list, first sorted array
    :param b: list, second sorted array
    :param p: int, p-th percentile of a merged array
    :return: int, the p-th percentile of a merged array
    '''
    res = merge_sort(a + b)
    k = math.ceil(p / 100 * len(res))  # ordinal rank of the merged array
    if k == 0:
        return res[0]
    return res[k - 1]

# Main solution


def __find_percentile(a: list, len_a: int, b: list, len_b: int, k: int):
    '''
    Auxiliary method for finding the percentile
    :param a: list, first sorted array
    :param len_a: int, length of the first array
    :param b: list, second sorted array
    :param len_b: int, length of the second array
    :param k: int, the total length of both left partitions
    :return: int, the p-th percentile of a merged array
    '''

    start, end = max(0, k - len_b), min(len_a, k)

    while start <= end:
        split_a_idx = (start + end) // 2
        split_b_idx = k - split_a_idx

        # boundary case for the first array
        max_left_a = -math.inf if split_a_idx <= 0 else a[split_a_idx - 1]
        min_right_a = math.inf if split_a_idx >= len_a else a[split_a_idx]
        # boundary case for the second array
        max_left_b = -math.inf if split_b_idx <= 0 else b[split_b_idx - 1]
        min_right_b = math.inf if split_b_idx >= len_b else b[split_b_idx]

        if max_left_a <= min_right_b and max_left_b <= min_right_a:
            return max(max_left_a, max_left_b)
        elif max_left_a > min_right_b:
            end = split_a_idx - 1
        else:
            start = split_a_idx + 1

    return -1


def find_percentile(a: list, b: list, p: int):
    '''
    Main method for finding the percentile
    :param a: list, first sorted array
    :param b: list, second sorted array
    :param p: int, p-th percentile of a merged array
    :return: int, the p-th percentile of a merged array
    '''
    len_a = len(a)
    len_b = len(b)
    k = math.ceil(p / 100 * (len_a + len_b))  # ordinal rank of the merged array

    # Corner cases
    if len_a == len_b == 0:
        print('At least one of the arrays should be non-empty!')
        return -1
    elif k in {0, 1}:
        a_min_val = a[0] if len_a != 0 else math.inf
        b_min_val = b[0] if len_b != 0 else math.inf
        return min(a_min_val, b_min_val)
    elif len_a == 0 and len_b != 0:
        return b[k - 1]
    elif len_b == 0 and len_a != 0:
        return a[k - 1]
    elif len_a + len_b == k:
        return max(a[len_a - 1], b[len_b - 1])

    # as we want to get O(min(log n, log m)) complexity
    # we need to apply the binary search to the smaller array
    if len_a > len_b:
        res = __find_percentile(b, len_b, a, len_a, k)
    else:
        res = __find_percentile(a, len_a, b, len_b, k)

    return res

# Tests


def create_random_sorted_list(n: int, min_value: int = -1000000, max_value: int = 1000000):
    '''
    Auxiliary method to create random sorted arrays
    :param n: int, length of an array
    :param min_value: int, min possible value in the array
    :param max_value: int, max possible value in the array
    :return: list, sorted array
    '''
    res = []
    for i in range(n):
        value = random.randint(min_value, max_value)
        res.append(value)

    res.sort()

    return res


def test_find_percentile(a, b, p, correct_answer):
    res = find_percentile(a, b, p)
    error_msg = 'Test failed for:\nFirst array = {}\nSecond array = {}\nPercentile = {}\n' + \
                'Output: {}\nCorrect Output: {}'
    assert res == correct_answer, error_msg.format(a, b, p, res, correct_answer)


def run_unit_tests():
    # Unit test 1
    test_a, test_b, test_p = [], [-5, 0, 4, 6, 7], 20
    test_find_percentile(test_a, test_b, test_p, -5)
    # Unit test 2
    test_a, test_b, test_p = [-99, 20, 45, 68, 90], [], 95
    test_find_percentile(test_a, test_b, test_p, 90)
    # Unit test 3
    test_a, test_b, test_p = [1, 2, 3, 4], [5, 6, 7, 8], 50
    test_find_percentile(test_a, test_b, test_p, 4)
    # Unit test 4
    test_a, test_b, test_p = [1, 3, 5, 7], [2, 4, 6], 50
    test_find_percentile(test_a, test_b, test_p, 4)
    # Unit test 5
    test_a, test_b, test_p = [-10, -8, -7, -5], [-3, -2, -1], 90
    test_find_percentile(test_a, test_b, test_p, -1)
    # Unit test 6
    test_a, test_b, test_p = [-5, 10], [2, 4, 5], 30
    test_find_percentile(test_a, test_b, test_p, 2)
    # Unit test 7
    test_a, test_b, test_p = [-3, -2, 0, 2, 4, 4, 4, 6, 6, 7], [1, 2], 30
    test_find_percentile(test_a, test_b, test_p, 1)

    print('All unit tests passed.')
    print('=' * 25)

    return


def run_stress_test(max_test_size=1000, max_runs=100):
    random.seed(46)
    start = time.time()
    for a_test_size in range(1, max_test_size, 100):
        for b_test_size in range(0, max_test_size, 100):
            for test_p in [x for x in range(0, 110, 10)]:
                print(f'len_a = {a_test_size}, len_b = {b_test_size}, p = {test_p}')
                for _ in range(max_runs):
                    test_a, test_b = create_random_sorted_list(a_test_size), create_random_sorted_list(b_test_size)
                    test_find_percentile(test_a, test_b, test_p, find_percentile_slow(test_a, test_b, test_p))
    end = time.time()

    print('Stress test passed.')
    print('=' * 25)

    print('run_stress_test works {}s on the stress test'.format(round(end - start, 2)))

    return


# find_percentile works 0.0s on the max test
def run_max_test():
    random.seed(46)
    test_a, test_b = create_random_sorted_list(750000), create_random_sorted_list(1000000)
    test_p = 25
    start = time.time()
    print(f'Answer: {find_percentile(test_a, test_b, test_p)}')
    end = time.time()

    print('Max test passed.')
    print('=' * 25)

    print('find_percentile works {}s on the max test'.format(round(end - start, 2)))
    return


if __name__ == "__main__":
    run_unit_tests()

    run_max_test()

    # Uncomment to run the stress test
    # run_stress_test()

