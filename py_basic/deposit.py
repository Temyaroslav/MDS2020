from math import ceil
p, x, y, k = int(input()), int(input()), int(input()), int(input())
x += y / 100
for _ in range(k):
    x *= (1 + p/100)
    x = round(x, 6)
    x = int(x) + int(x * 100 % 100) / 100
    # print(x)

print(int(x), int((x - int(x)) * 100), sep=' ')
