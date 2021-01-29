def largest_palindrome2(s):
    '''
    O(n^3) solution of finding the largest palindrome
    '''
    max_length = 0
    max_start_idx, max_end_idx = 0, 0
    for i in range(len(s)):
        for j in range(i, len(s)):
            sub_s = s[i:j+1]
            is_palindrome = True
            l, r = 0, len(sub_s) - 1
            while l < len(sub_s) and r >= 0:
                if l < len(sub_s) and r >= 0 and sub_s[l] != sub_s[r]:
                    is_palindrome = False
                    break
                l += 1
                r -= 1
            if is_palindrome:
                length = j - i + 1
                if length > max_length:
                    max_length = length
                    max_start_idx = i
                    max_end_idx = j

    return s[max_start_idx:max_end_idx + 1]


def largest_palindrome(s):
    '''
    O(n^2) solution of finding the largest palindrome
    '''
    max_length = 0
    max_start_idx, max_end_idx = 0, 0
    start, length = 0, len(s)
    for center in range(1, length):
        # even palindrome
        l = center - 1
        r = center
        while l >= 0 and r < length and s[l] == s[r]:
            if r - l + 1 > max_length:
                max_start_idx = l
                max_end_idx = r
                max_length = r - l + 1
            l -= 1
            r += 1
        # odd palindrome
        l = center - 1
        r = center + 1
        while l >= 0 and r < length and s[l] == s[r]:
            if r - l + 1 > max_length:
                max_start_idx = l
                max_end_idx = r
                max_length = r - l + 1
            l -= 1
            r += 1

    return s[max_start_idx:max_end_idx + 1]


# some test code
if __name__ == "__main__":
    test_s = 'ABBCB'
    # should print BCB
    print(largest_palindrome(test_s))

    # test_s = 'ABACABAD'
    # # should print ABACABA
    # print(largest_palindrome(test_s))
    #
    # test_s = 'forgeeksskeegfor'
    # # should print A
    # print(largest_palindrome(test_s))

