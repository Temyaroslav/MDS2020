s = int(input())
s %= 24 * 3600
h = s // 3600
s %= 3600
m = s // 60
s %= 60
print("%d:%02d:%02d" % (h, m, s))