import math

def edistance(A, B):
    edist = [[math.inf for _ in range(len(B) + 1)] for _ in range(len(A) + 1)]
    for i in range(len(B) + 1):
        edist[0][i] = i
    for j in range(len(A) + 1):
        edist[i][0] = i
    for i in range(1, len(A) + 1):
        for j in range(1, len(B) + 1):
            if A[i - 1] == B[j - 1]:
                # substitution
                edist[i][j] = edist[i - 1][j - 1]
            else:
                edist[i][j] = 1 + min(
                    edist[i - 1][j], # deletion
                    edist[i][j - 1], # insertion
                    edist[i - 1][j - 1] # substitution
                )
    return edist[-1][-1]

def weighted_edistance(A, B, wdel, wins, wsub):
    edist = [[math.inf for _ in range(len(B) + 1)] for _ in range(len(A) + 1)]
    for i in range(len(B) + 1):
        edist[0][i] = i * wins
    for j in range(len(A) + 1):
        edist[i][0] = i * wdel
    for i in range(1, len(A) + 1):
        for j in range(1, len(B) + 1):
            if A[i - 1] == B[j - 1]:
                edist[i][j] = edist[i - 1][j - 1]
            else:
                edist[i][j] = min(
                    edist[i - 1][j] + wdel,
                    edist[i][j - 1] + wins,
                    edist[i - 1][j - 1] + wsub
                )
    return edist[-1][-1]

def edistance_substring(A, B):
    # Filling the lookup table in the same way as in the first problem but... (line 46)
    edist = [[math.inf for _ in range(len(B) + 1)] for _ in range(len(A) + 1)]
    for i in range(len(B) + 1):
        edist[0][i] = i
    for j in range(len(A) + 1):
        # ... with a difference here: make deletions from the beginning for free
        edist[j][0] = 0
    for i in range(1, len(A) + 1):
        for j in range(1, len(B) + 1):
            if A[i - 1] == B[j - 1]:
                edist[i][j] = edist[i - 1][j - 1]
            else:
                edist[i][j] = 1 + min(edist[i - 1][j], edist[i][j - 1], edist[i - 1][j - 1])

    # This makes the deletions at the end for free as well
    return min([edist[i][-1] for i in range(len(A) + 1)])

if __name__ == "__main__":
    print(edistance("good", "bad"))
    print(weighted_edistance("good", "bad", 1, 2, 5))
    print(edistance_substring("good", "bad"))