
def find_numbers(a, k):
    '''
    Given an array aa and a number kk. An array is sorted in increasing order.
    Check if there are two elements xx and yy in the array such that they add up to kk.
    :param a: list, [1,2,8,10,11]
    :param k: int, 10
    :return: bool
    '''
    left, right = 0, len(a) - 1
    while left < right:
        if a[left] + a[right] == k:
            return True
        elif a[left] + a[right] < k:
            left += 1
        else:
            right -= 1
    return False


def is_palindrome(s):
    '''
    Given a string that contains lowercase characters a-z and whitespaces.
    Complete a function that checks if this string is a palindrome ignoring whitespaces.
    :param s: str, " mad am    "
    :return: bool, True
    '''
    left, right = 0, len(s) - 1
    while left < len(s) and right >= 0:
        if s[right] == ' ':
            right -= 1
            continue
        elif s[left] == ' ':
            left += 1
            continue
        if left < len(s) and right >= 0 and s[left] != s[right]:
            return False
        left += 1
        right -= 1
    return True


def find_unique(a):
    '''
    Given an array aa sorted in non-decreasing order. Find how many unique elements are there in this array.
    :param a: int, [1,2,2,2,3,3]
    :return: int, 3
    '''
    current_number_index = 0
    unique = 1
    for i in range(len(a)):
        if a[i] != a[current_number_index]:
            current_number_index = i
            unique += 1
    return unique


def moving_average(a, k):
    '''
    Given an array aa, a sliding window of size kk  is moving from the very left of the array to the very right.
    Each time the sliding window moves right by one position. For each sliding window position return average value of
    all numbers inside the sliding window.
    :param a: list, a=[1,2,3,4,8]
    :param k: int
    :return:
    '''
    sum = 0
    for i in range(k):
        sum += a[i]
    window_sum = [sum]
    left, right = 0, k - 1
    while right + 1 < len(a):
        window_sum.append(window_sum[len(window_sum) - 1] + a[right + 1] - a[left])
        right += 1
        left += 1
    return [x * 1.0 / k for x in window_sum]


if __name__ == '__main__':
    a = [0, 0, 10, 20, 30]
    print(find_numbers(a, 10))