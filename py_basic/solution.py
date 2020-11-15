def succ(x):
    return x + 1

def pre(x):
    return x - 1

def main(x, y):
    if y == 0:
        return x
    else:
        return main(succ(x), pre(y))

if __name__ == '__main__':
    print(main(int(input()), int(input())))
