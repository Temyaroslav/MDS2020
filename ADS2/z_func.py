def z_func(s):
    n = len(s)
    z = [0] * n

    l, r = 0, 0

    for i in range(1, n):
        if i <= r:
            z[i] = min(z[i - l], r - i + 1)

        while i + z[i] < n and s[z[i] + i] == s[z[i]]:
            z[i] += 1

        new_r = i + z[i] - 1
        if new_r > r:
            l, r = i, new_r

    return z


def match_z_func(text, pattern):
    n, m = len(text), len(pattern)
    special_symbol = "#"
    indices = []

    s = pattern + special_symbol + text
    z = z_func(s)

    for i in range(len(z)):
        if z[i] == m:
            indices.append(i - m - 1)

    return indices


if __name__ == '__main__':
    text = 'abracadabra'
    pattern = 'ab'

    print(match_z_func(text, pattern))
