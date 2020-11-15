def main(n):
    if n == 1 or n == 2:
        return 1
    else:
        return main(n - 2) + main(n - 1)

if __name__ == '__main__':
    n = int(input())
    if n == 0:
        print(0)
    else:
        print(main(n))
