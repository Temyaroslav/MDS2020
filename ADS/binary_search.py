def merge(a, b):
    result = []
    i, j = 0, 0
    while i < len(a) and j < len(b):
        if a[i] < b[j]:
            result.append(a[i])
            i += 1
        else:
            result.append(b[j])
            j += 1
    while i < len(a):
        result.append(a[i])
        i += 1
    while j < len(b):
        result.append(b[j])
        j += 1
    return result



def mergesort(a):
    if len(a) <= 1:
        return a
    mid = len(a) // 2
    left = mergesort(a[:mid])
    right = mergesort(a[mid:])
    print(left, right)
    return merge(left, right)


def bsearch(A, t):
    l = 0
    r = len(A)
    while l < r:
        mid = (l + r) // 2
        if A[mid] == t:
            return mid
        if A[mid] > t:
            r = mid
        else:
            l = mid + 1
    return -1


def bs(A, l, r, t):
    if l >= r:
        return -1
    mid = (l + r) // 2
    if A[mid] == t:
        return mid
    if A[mid] > t:
        print('yo')
        return bs(A, l, mid, t)
    print('yo')
    return bs(A, mid + 1, r, t)


def bsearch1(arr, key):
    low, high = 0, len(arr)
    while high - low >= 1:
        mid = (low + high) // 2
        if arr[mid] == key:
            return mid
        elif arr[mid] < key:
            low = mid
        else:
            high = mid
    return None

def bsearch3(arr, key):
    n = len(arr)
    if n < 2:
        return 0 if (n == 1 and arr[0] == key) else None
    m = int(0.5 * n)
    # if arr[m] == key:
    #     return m
    if arr[m] > key:
        print('yo')
        return bsearch3(arr[:m], key)
    print('yo')
    result = bsearch3(arr[m :], key)
    return result + m if result != None else None


if __name__ == '__main__':
    # mergesort([7, 3, 2, 1, 10, 5, 6, 8])
    A = [0, 1, 2, 3]
    # A = [0, 0, 1, 1, 1, 1, 2, 3, 4]
    # print(bs(A, 0, len(A), 2))
    print(bsearch(A, 0))
    print('='*10)
    print(bsearch1(A, 0))
