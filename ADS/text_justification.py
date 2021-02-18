import math

def tj_cost(L, W):
    n = len(W)
    tbl = [math.inf] * (n + 1)
    split  = [0] * (n + 1)
    tbl[0] = 0
    for i in range(1, n + 1):
        length = -1
        for j in range(i - 1, -1, -1):
            length += 1 + len(W[j])
            if length > L:
                P = math.inf
            else:
                P = (L - length)**3 if i != n else 0
            if tbl[i] > tbl[j] + P:
                tbl[i] = tbl[j] + P
                split[i] = j
    return tbl[n]

def tj(L, W):
    n = len(W)
    tbl = [ math.inf ] * (n + 1)
    split  = [0] * (n + 1)
    tbl[0] = 0
    for i in range(1, n + 1):
        length = -1
        for j in range(i - 1, -1, -1):
            length += 1 + len(W[j])
            if length > L:
                P = math.inf
            else:
                P = (L - length)**3 if i != n else 0
            if tbl[i] > tbl[j] + P:
                tbl[i] = tbl[j] + P
                split[i] = j
    
    result = []
    last = n
    while last > 0:
        result.append(W[split[last] : last])
        last = split[last]
    result = result[::-1]

    s = str()
    for i in range(len(result) - 1):
        s += ' '.join(result[i]) + '\n'
    s += ' '.join(result[-1])
    return s


if __name__ == "__main__":
    W_example = ["jars", "jaws", "joke", "jury", "juxtaposition"]
    L_example = 15
    # should print 432
    # print(tj_cost(L_example, W_example))
    # should print:
    #jars jaws
    #joke jury
    #juxtaposition
    print(tj(L_example, W_example))
