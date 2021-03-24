def find_max_same_color_block(a):
    block_start = 0
    max_block_start, max_block_end = 0, 0
    for i in range(len(a)):
        if a[block_start] != a[i]:
            if i - block_start > max_block_end - max_block_start:
                max_block_start = block_start
                max_block_end = i
            block_start = i
    return max_block_start, max_block_end


def lines(a):
    a.append(1111) # add ball of nonexistent color to handle border
    result = 0
    block_start, block_end = find_max_same_color_block(a)
    while block_end - block_start >= 3:
        result += block_end - block_start
        a = a[:block_start] + a[block_end:]
        block_start, block_end = find_max_same_color_block(a)
    return result


# some test code
if __name__ == "__main__":
    test_a = [2, 2, 1, 1, 1, 2, 1]
    # should print 6
    print(lines(test_a))

    test_a = [0, 0, 0, 0, 0]
    # should print 5
    print(lines(test_a))

    test_a = [2, 3, 1, 4]
    # should print 0
    print(lines(test_a))