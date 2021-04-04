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
    res = []
    s = pattern + '#' + text
    n = len(pattern)

    prefix = prefix_func(s)
    for i in range(n + 1, len(prefix)):
        if prefix[i] == n:
            res.append(i - 2 * n)

    return res


def KMPSearch(pat, txt):
    M = len(pat)
    N = len(txt)

    # create lps[] that will hold the longest prefix suffix
    # values for pattern
    lps = [0] * M
    j = 0  # index for pat[]

    # Preprocess the pattern (calculate lps[] array)
    computeLPSArray(pat, M, lps)
    print(lps)

    i = 0  # index for txt[]
    while i < N:
        if pat[j] == txt[i]:
            i += 1
            j += 1

        if j == M:
            print("Found pattern at index " + str(i - j))
            j = lps[j - 1]

        # mismatch after j matches
        elif i < N and pat[j] != txt[i]:
            # Do not match lps[0..lps[j-1]] characters,
            # they will match anyway
            if j != 0:
                j = lps[j - 1]
            else:
                i += 1


def computeLPSArray(pat, M, lps):
    len = 0  # length of the previous longest prefix suffix

    lps[0] = 0  # lps[0] is always 0
    i = 1

    # the loop calculates lps[i] for i = 1 to M-1
    while i < M:
        if pat[i] == pat[len]:
            len += 1
            lps[i] = len
            i += 1
        else:
            # This is tricky. Consider the example.
            # AAACAAAA and i = 7. The idea is similar
            # to search step.
            if len != 0:
                len = lps[len - 1]

                # Also, note that we do not increment i here
            else:
                lps[i] = 0
                i += 1


def cyclic_pattern(s):
    # https://stackoverflow.com/questions/6021274/finding-shortest-repeating-cycle-in-word
    nxt = [0]*len(s)
    for i in range(1, len(nxt)):
        k = nxt[i - 1]
        while True:
            if s[i] == s[k]:
                nxt[i] = k + 1
                break
            elif k == 0:
                nxt[i] = 0
                break
            else:
                k = nxt[k - 1]

    smallPieceLen = len(s) - nxt[-1]
    if len(s) % smallPieceLen != 0:
        return len(s)

    return smallPieceLen


if __name__ == '__main__':
    # txt = "ABABDABACDABABCABAB"
    # pat = "ABABCABAB"
    # txt = 'abracadabra'
    # pat = 'ab'
    # KMPSearch(pat, txt)
    #
    # print(kmp(txt, pat))
    cyclic_string = 'ddddddddddd'
    print(cyclic_pattern(cyclic_string))
