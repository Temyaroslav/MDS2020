import math

def edistance(A, B):
    n = len(A)
    m = len(B)
    D = [[0 for _ in range(m + 1)] for _ in range(n + 1)]
    for i in range(n + 1):
        for j in range(m + 1):
            if i == 0:
                D[i][j] = j
            elif j == 0:
                D[i][j] = i
            elif A[i - 1] == B[j - 1]:
                D[i][j] = D[i - 1][j - 1]
            else:
                D[i][j] = 1 + min(
                    D[i - 1][j],
                    D[i][j - 1],
                    D[i - 1][j - 1]
                )  # delete A[i - 1] or B[j - 1] or substitute A[i - 1] for B[j - 1]
    return D[n][m]

def weighted_edistance(A, B, wdel, wins, wsub):
    n = len(A)
    m = len(B)
    D = [[0 for _ in range(m + 1)] for _ in range(n + 1)]
    for i in range(n + 1):
        for j in range(m + 1):
            if i == 0:
                D[i][j] = j * wins
            elif j == 0:
                D[i][j] = i * wdel
            elif A[i - 1] == B[j - 1]:
                D[i][j] = D[i - 1][j - 1]
            else:
                D[i][j] = min(
                    D[i - 1][j] + wdel,
                    D[i][j - 1] + wins,
                    D[i - 1][j - 1] + wsub
                )
    return D[n][m]

def edistance_substring(A, B):
    n = len(A)
    m = len(B)
    D = [[0 for _ in range(m + 1)] for _ in range(n + 1)]
    for i in range(n + 1):
        for j in range(m + 1):
            if i == 0:
                D[i][j] = j
            elif j == 0:
                D[i][j] = 0
            elif A[i - 1] == B[j - 1]:
                D[i][j] = D[i - 1][j - 1]
            else:
                D[i][j] = 1 + min(
                    D[i - 1][j],
                    D[i][j - 1],
                    D[i - 1][j - 1]
                )  # delete A[i - 1] or B[j - 1] or substitute A[i - 1] for B[j - 1]
    return D[n][m]

if __name__ == "__main__":
    # should print 3
    # print(edistance('good', 'baad'))
    # should print 7
    print(weighted_edistance("good", "bad", 1, 2, 5))
