def main(n):
    if n == 1:
        return n
    else:
        return n * main(n - 1)
    return m

if __name__ == '__main__':
    n = int(input())
    if n == 0:
        print(1)
    else:
        print(main(n))
