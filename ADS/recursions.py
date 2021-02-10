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

if __name__ == '__main__':
    # print(exp(2, 10))
    # print(fibonacci(5))
    # print(factorial(4))
    # print(binom(6, 3))
    # print(subsets(list(range(10)), 4))
    # print(submessages('aba'))
    print(take_to_space([1, 2, 3], 3))
    # print(passwords(2))
    # print(slogan(["modern", "cool", "abysmal"], 13))
    
