x, p, y = int(input()), int(input()), int(input())
i = 1
while x < y:
    x *= (1 + p/100)
    x = round(x, 2)
    i += 1
    
 print("end")