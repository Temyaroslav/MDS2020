def order(c):
    return ord(c) - ord('a') + 1


def rabin_karp(text, pattern):
    n, m = len(text), len(pattern)
    p, q = 31, 10**9 + 7

    p_pow = 1
    for i in range(m - 1):
        p_pow = (p_pow * p) % q

    pattern_hash = 0
    window_hash = 0
    for i in range(m):
        pattern_hash = (pattern_hash * p + order(pattern[i])) % q
        window_hash = (window_hash * p + order(text[i])) % q

    for i in range(n - m + 1):
        if pattern_hash == window_hash:
            match = True
            for j in range(m):
                if pattern[j] != text[i + j]:
                    match = False
                    break
            if match:
                yield i
        if i < n - m:
            window_hash = (window_hash - order(text[i]) * p_pow) % q
            window_hash = (window_hash * p + order(text[i + m])) % q
            window_hash = (window_hash + q) % q


if __name__ == '__main__':
    print(list(rabin_karp('ernfebrhsegiuehg', 'hse')))