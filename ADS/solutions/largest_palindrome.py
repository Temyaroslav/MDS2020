def largest_palindrome(s):
    max_start, max_end = 0, 0
    for center in range(len(s)):
        # odd palindromes
        size = 0
        while center - size - 1 >= 0 and center + size + 1 < len(s) and s[center + size + 1] == s[center - size - 1]:
            size += 1
        if 2 * size + 1 > max_end - max_start + 1:
            max_start = center - size
            max_end = center + size

        # even palindromes
        size = -1
        while center - size - 2 >= 0 and center + size + 1 < len(s) and s[center + size + 1] == s[center - size - 2]:
            size += 1
        if 2 * size + 2 > max_end - max_start + 1:
            max_start = center - size - 1
            max_end = center + size
    return s[max_start: max_end + 1]


# some test code
if __name__ == "__main__":
    test_s = 'ABBCB'
    # should print BCB
    print(largest_palindrome(test_s))

    test_s = 'ABACABAD'
    # should print ABACABA
    print(largest_palindrome(test_s))

    test_s = 'ABCDE'
    # should print A
    print(largest_palindrome(test_s))