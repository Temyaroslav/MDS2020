def prefix_func(s):
    n = len(s)
    prefix = [0] * n

    for i in range(1, n):
        x = prefix[i - 1]

        while x > 0 and s[i] != s[x]:
            x = prefix[x - 1]

        if s[i] == s[x]:
            prefix[i] = x + 1

    return prefix


def kmp(text, pattern):
    s = pattern + '#' + text
    n = len(pattern)

    prefix = prefix_func(s)
    for i in range(n + 1, len(prefix)):
        if prefix[i] == n:
            return i - 2 * n