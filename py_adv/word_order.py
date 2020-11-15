words = {}
text = []
while True:
    inpt = input()
    if inpt != '':
        inpt = inpt.split()
        text += inpt
        for w in inpt:
            if w not in words:
                words[w] = 0
            print(words[w], sep=' ', end=' ', flush=True)
            words[w] += 1
    else:
        # for w in text:
        #     print(words[w], sep=' ',  end=' ', flush=True)
        break
