class Deque:

    def __init__(self):
        self._size = 150000
        self._front = -1
        self._rear = 0
        self.queue = [0] * self._size

    def is_empty(self):
        return self._front == -1

    def is_full(self):
        return self._front == self._rear + 1 or (self._front == 0 and self._rear == self._size - 1)

    def clear(self):
        self._front = -1
        self._rear = 0
        self.queue = [0] * self._size
        return 'ok'

    def front(self):
        if self.is_empty():
            return 'error'
        return self.queue[self._front]

    def back(self):
        if self.is_empty():
            return 'error'
        return self.queue[self._rear]

    def push_front(self, key):
        if self._front == -1:
            self._front = 0
            self._rear = 0
        elif self._front == 0:
            self._front = self._size - 1
        else:
            self._front -= 1

        self.queue[self._front] = key
        return 'ok'

    def push_back(self, key):
        if self._front == -1:
            self._front = 0
            self._rear = 0
        elif self._rear == self._size - 1:
            self._rear = 0
        else:
            self._rear += 1

        self.queue[self._rear] = key
        return 'ok'

    def pop_front(self):
        if self.is_empty():
            return 'error'
        res = self.queue[self._front]
        self.queue[self._front] = 0
        if self._front == self._rear:
            self._front = -1
            self._rear = 0
        else:
            if self._front == self._size - 1:
                self._front = 0
            else:
                self._front += 1
        return res

    def pop_back(self):
        if self.is_empty():
            return 'error'
        res = self.queue[self._rear]
        self.queue[self._rear] = 0
        if self._front == self._rear:
            self._front = -1
            self._rear = 0
        else:
            if self._rear == 0:
                self._rear = self._size - 1
            else:
                self._rear -= 1
        return res

    def size(self):
        if self.is_empty():
            return 0
        if self.is_full():
            return self._size
        if self._front == self._rear:
            return 1
        elif self._front < self._rear:
            return self._rear + 1
        elif self._front > self._rear:
            return self._rear + 1 + self._size - self._front


def sliding_window_min(a, k):
    dequeue = Deque()
    for i in range(k):
        while not dequeue.is_empty() and a[i] <= a[dequeue.back()]:
            dequeue.pop_back()
        dequeue.push_back(i)
    window = []
    for i in range(k, len(a)):
        window.append(a[dequeue.front()])

        while not dequeue.is_empty() and dequeue.front() <= i - k:
            dequeue.pop_front()

        while not dequeue.is_empty() and a[i] <= a[dequeue.back()]:
            dequeue.pop_back()

        dequeue.push_back(i)

    window.append(a[dequeue.front()])

    return window


# some test.py code
if __name__ == "__main__":
    test_a, test_k = [12, 1, 78, 90, 57, 89, 56], 3
    # should print [1, 3, 2, 2]
    print(sliding_window_min(test_a, test_k))

    test_a, test_k = [5, 4, 10, 1], 2
    # should print [4, 4, 1]
    print(sliding_window_min(test_a, test_k))

    test_a, test_k = [10, 20, 6, 10, 8], 5
    # should print [6]
    print(sliding_window_min(test_a, test_k))

