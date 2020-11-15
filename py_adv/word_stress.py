N = int(input())
words = {}
for _ in range(N):
    inpt = input()
    if inpt.lower() not in words:
        words[inpt.lower()] = []
    words[inpt.lower()].append(inpt)
sentence = input().split()
c = 0
for w in sentence:
    s = sum(1 for l in w if l.isupper())
    if s == 1:
        if w.lower() in words:
            if w not in words[w.lower()]:
                c += 1
    else:
        # print(w)
        c += 1
# print(words)
print(c)
