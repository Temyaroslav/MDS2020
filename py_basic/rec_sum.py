def main(n):
    if n == 0:
        return n
    else:
        return n % 10 + main(n // 10)

if __name__ == '__main__':
    n = int(input())
    print(main(n))
