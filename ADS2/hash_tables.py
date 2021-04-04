def _isAnagram(s):
    freq = {}
    for char in s:
        freq[char] = freq.get(char, 0) + 1
    return freq


def isAnagram(string1, string2):
    freq1 = _isAnagram(string1)
    freq2 = _isAnagram(string2)

    return freq1 == freq2


def longestNonRepeating(text):
    n = len(text)
    longest = 0

    last_idx = {}
    start_idx = 0

    for i in range(n):
        if text[i] in last_idx:
            start_idx = max(start_idx, last_idx[text[i]] + 1)

        longest = max(longest, i - start_idx + 1)

        last_idx[text[i]] = i

    return longest


def arrayIntersection(array1, array2):
    return list(set(array1) & set(array2))


if __name__ == '__main__':
    # string1 = 'baa'
    # string2 = 'aab'
    #
    # # True
    # print(isAnagram(string1, string2))

    # text = 'baa'
    # # Should print 2
    # print(longestNonRepeating(text))

    array1 = [1, 2, 3]
    array2 = [2, 4, 5]
    print(arrayIntersection(array1, array2))