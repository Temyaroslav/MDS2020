w = {}
while True:
    inpt = input()
    if inpt != '':
        inpt = inpt.split()
        for i in inpt:
            if i not in w:
                w[i] = 0
            w[i] += 1
    else:
        m = max(list(w.values()))
        freq = []
        for k, v in w.items():
            if v == m:
                freq.append(k)
        freq.sort()
        print(freq[0])
        break
