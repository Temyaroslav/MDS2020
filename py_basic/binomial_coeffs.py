N, a, b = int(input()), int(input()), int(input())
C = dict()

for n in range(N+1):
    C[n, 0] = 1
    C[n, n] = 1
    
    for k in range(1, n):
        C[n, k] = C[n - 1, k - 1] + C[n - 1, k]

for i in range(N+1):
    print(C[N, i] * a**(N - i) * b**i)