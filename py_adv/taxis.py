dist = list(map(int, input().split()))
fares = list(map(int, input().split()))
dist = list(zip(dist, range(len(dist))))
fares = list(zip(fares, range(len(fares))))

dist.sort(key=lambda x: x[0])
fares.sort(key=lambda x: x[0], reverse=True)

res = map(lambda x: (x[0][1], x[1][1]), zip(dist, fares))
res = list(sorted(res, key=lambda x: x[0]))
_, res = zip(*res)
print(*res)
