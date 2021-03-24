def calc_rain_water(h):
    result = 0
    stack = []
    for i in range(len(h)):
        if not stack or h[i] <= h[stack[-1]]:
            stack.append(i)
        else:
            while stack and h[i] > h[stack[-1]]:
                current_pos = stack.pop()
                if not stack:
                    break
                # h[stack[-1]] and h[i] are left and right borders for
                # column we just pop from the stack
                current_water_height = min(h[i], h[stack[-1]]) - h[current_pos]
                result += current_water_height * (i - stack[-1] - 1)
            stack.append(i)
    return result


# some test code
if __name__ == "__main__":
    test_h = [2, 5, 2, 3, 6, 9, 1, 3, 4, 6, 1]
    # should print 15
    print(calc_rain_water(test_h))

    test_h = [2, 4, 6, 8, 6, 4, 2]
    # should print 0
    print(calc_rain_water(test_h))

    test_h = [8, 6, 4, 2, 4, 6, 8]
    # should print 18
    print(calc_rain_water(test_h))