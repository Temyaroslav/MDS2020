import math

def double_factorial(n):
    if n <= 1:
        return 1
    return double_factorial(n - 2) * n

def exp(a, b):
    '''
    fn: exponent computation using recursion
    '''
    if b == 0:
        return 1
    if b % 2 == 0:
        return (exp(a, b // 2)) ** 2
    else:
        return a * exp(a, (b - 1) // 2) ** 2

def fibonacci(n):
    '''
    fn: Fibonacci numbers using recursion
    '''
    if n == 0 or n == 1:
        return 1
    return fibonacci(n - 1) + fibonacci(n - 2)

def factorial(n):
    '''
    fn: factorial computation using recursion
    '''
    if n == 1:
        return 1
    return n * factorial(n - 1)

def binom(n, k):
    '''
    fn: Newton binom using recursion
    '''
    if k == 0 or n == k:
        return 1
    return binom(n - 1, k) + binom(n - 1, k - 1)

def subsets2(elems):
    if not elems:
        return [ [] ]
    result = subsets2(elems[:-1])
    last = elems[-1]
    for i in range(len(result)):
        result.append(result[i] + [last])
    return result

def subsets(elems, k):
    if k == 0:
        return [[]]
    if len(elems) == 0:
        return []
        
    last = elems[-1]
    without_last = elems[:-1]
    result = subsets(without_last, k)
    with_last = subsets(without_last, k - 1)
    for s in with_last:
        result.append(s + [last])
    return result

def submessages(s):
    if len(s) == 0:
        return {''}
    last = s[-1]
    without_last = s[:-1]
    result = submessages(without_last)
    for m in list(result):
        result.add(m + last)
    return result

def take_to_space(mass, C):
    if len(mass) == 0:
        if C >= 0:
            return { tuple() }
        else:
            return set()
    without_last = take_to_space(mass[:-1], C)
    with_last = take_to_space(mass[:-1], C - mass[-1])
    result = without_last
    for s in with_last:
        result.add(tuple(s))
    return result

def passwords(n):
    if n == 0:
        return {""}
    prev = passwords(n - 1)
    result = set()
    for p in prev:
        result.add(p + 'A')
        result.add(p + 'B')
    return result

def slogan(words, L):
    if len(words) == 1 or len(words[-1]) == L:
        return len(words[-1]) == L
    last_word = words[-1]
    without_last_word = words[:-1]
    return slogan(without_last_word, L) or slogan(without_last_word, L - len(last_word) - 1)

def voc_to_list(vocabulary):
    """
    produces a list lengths such that lengths[i] is the number of
    words in length i in vocabulary
    """
    max_len = max([len(w) for w in vocabulary])
    lengths = [0] * (max_len + 1)
    for w in vocabulary:
        lengths[len(w)] += 1
    return lengths

def passwords(L, vocabulary):
    lengths = voc_to_list(vocabulary)
    k = len(lengths)
    tbl = [0] * (L + 1)
    for i in range(L + 1):
        if i < k:
            tbl[i] = lengths[i]
        for j in range(min(k, i)):
            tbl[i] += tbl[i - j - 1] * lengths[j]
    return tbl[L]

def num_boxes(n):
    tbl = [math.inf] * (n + 1)
    tbl[0] = 0
    last = [0] * (n + 1)
    for j in range(1, n + 1):
        i = 1
        while i**3 <= j:
            # if tbl[j] > 0:
            #     tbl[j] = tbl[j - i**3] + 1
            #     last[j] = i
            tbl[j] = min(tbl[j], tbl[j - i**3] + 1)
            last[j] = i
            i += 1
    cubes = []
    current = n
    while current > 0:
        cubes.append(last[current])
        current -= last[current]**3
    return tbl[-1], cubes[::-1]
    

if __name__ == '__main__':
    # print(exp(2, 10))
    # print(fibonacci(5))
    # print(factorial(4))
    # print(binom(6, 3))
    # print(subsets(list(range(10)), 4))
    # print(submessages('aba'))
    # print(take_to_space([1, 2, 3], 3))
    # print(passwords(2))
    # print(slogan(["modern", "cool", "abysmal"], 13))
    # print(passwords(5, ["hello", "oh"]))

    # should print (3, [1, 1, 2])
    # the order of boxes might be different
    print(num_boxes(237))
    
