class MinHeap(object):
    def __init__(self):
        self.heap = []

    def _sift_up(self, item):
        parent = (item - 1) // 2
        if item > 0 and self.heap[item] < self.heap[parent]:
            self.heap[item], self.heap[parent] = self.heap[parent], self.heap[item]
            self._sift_up(parent)

    def _sift_down(self, item):
        l_child = item * 2 + 1
        r_child = item * 2 + 2

        if l_child < len(self.heap) and self.heap[l_child] < self.heap[item]:
            self.heap[item], self.heap[l_child] = self.heap[l_child], self.heap[item]
            self._sift_down(l_child)

        if r_child < len(self.heap) and self.heap[r_child] < self.heap[item]:
            self.heap[item], self.heap[r_child] = self.heap[r_child], self.heap[item]
            self._sift_down(r_child)

    def push(self, elem):
        self.heap.append(elem)
        self._sift_up(len(self.heap) - 1)

    def view(self):
        return self.heap[0]

    def pop(self):
        self.heap[0], self.heap[-1] = self.heap[-1], self.heap[0]
        elem = self.heap.pop()
        self._sift_down(0)
        return elem


def _sift_up(arr, item):
    parent = (item - 1) // 2
    if item > 0 and arr[item] < arr[parent]:
        arr[item], arr[parent] = arr[parent], arr[item]
        _sift_up(arr, parent)


def heapify_min(arr):
    n = len(arr)

    for i in reversed(range(n)):
        _sift_up(arr, i)


def heapify(arr, i, n):
    largest = i
    l, r = i * 2 + 1, i * 2 + 2
    for child in (l, r):
        if child < n and arr[largest] < arr[child]:
            largest = child
    if largest != i:
        arr[i], arr[largest] = arr[largest], arr[i]
        heapify(arr, largest, n)


def buildMaxHeap(arr):
    n = len(arr)
    start = n // 2 - 1

    for i in range(start, -1, -1):
        heapify(arr, i, n)


def heapsort(arr):
    n = len(arr)
    buildMaxHeap(arr)
    for i in range(n - 1, 0, -1):
        arr[0], arr[i] = arr[i], arr[0]
        heapify(arr, 0, i)

    return arr


if __name__ == '__main__':
    arr = [3, 2, 1]
    heapify_min(arr)
    print(arr)
    # print(heapsort(arr))
