import math


def tj_cost(L, W):
    n = len(W)
    min_penalty = [math.inf] * (n + 1)
    min_penalty[0] = 0

    # Filling the same lookup table as in the lecture
    for i in range(1, n + 1):
        length = -1
        for j in range(i - 1, -1, -1):
            length += 1 + len(W[j])
            if length > L:
                penalty = math.inf
            else:
                penalty = (L - length) ** 3
            min_penalty[i] = min(min_penalty[i], min_penalty[j] + penalty)

    # Considering possible options for the last line (the penalty-free one)
    len_last = len(W[-1])
    best = min_penalty[-2]
    cur_word_index = len(W) - 1
    while len_last <= L and cur_word_index > 0:
        best = min(best, min_penalty[cur_word_index])
        cur_word_index -= 1
        len_last += len(W[cur_word_index]) + 1

    return best


def tj(L, W):
    n = len(W)
    min_penalty = [math.inf] * (n + 1)
    min_penalty[0] = 0
    split = [0] * (n + 1)
    # Filling the lookup table and the split array as in the lecture
    for i in range(1, n + 1):
        length = -1
        for j in range(i - 1, -1, -1):
            length += 1 + len(W[j])
            if length > L:
                penalty = math.inf
            else:
                penalty = (L - length) ** 3
            if min_penalty[i] > min_penalty[j] + penalty:
                min_penalty[i] = min_penalty[j] + penalty
                split[i] = j

    # Composing the last (penalty-free) line
    len_last = len(W[-1])
    best = min_penalty[-2]
    cur_word_index = len(W) - 1
    best_last_first_word = len(W) - 1
    while len_last <= L and cur_word_index > 0:
        if best > min_penalty[cur_word_index]:
            best = min_penalty[cur_word_index]
            best_last_first_word = cur_word_index
        cur_word_index -= 1
        len_last += len(W[cur_word_index]) + 1
    result = " ".join(W[best_last_first_word:])

    # Composing the remaining lines
    cur_word_index = best_last_first_word
    while cur_word_index > 0:
        result = " ".join(W[split[cur_word_index]: cur_word_index]) + "\n" + result
        cur_word_index = split[cur_word_index]

    return result


if __name__ == "__main__":
    W_example = ["jars", "jaws", "joke", "jury", "juxtaposition"]
    L_example = 15
    print(tj_cost(L_example, W_example))
    print(tj(L_example, W_example))