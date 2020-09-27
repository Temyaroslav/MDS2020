n = int(input())
if n == 0:
    print(0)
elif n == 1:
    print(1)
else:
    s = 0; i = 2
    old, new = 0, 1
    while True:
        holder = new
        new += old
        old = holder
        if new == n:
            print(i)
            break
        elif new > n:
            print(-1)
            break
        i += 1