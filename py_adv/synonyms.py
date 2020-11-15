N = int(input())
words = {}
for _ in range(N):
    inpt = input().split()
    words[inpt[0]] = inpt[1]
inpt = input()
for k, v in words.items():
    if k == inpt:
        print(v)
        break
    elif v == inpt:
        print(k)
        break
