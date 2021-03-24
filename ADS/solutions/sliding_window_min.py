class Stack:

    def __init__(self):
        self.stack = []

    def push(self, key):
        self.stack.append(key)

    def pop(self):
        return self.stack.pop()

    def empty(self):
        return len(self.stack) == 0

    def top(self):
        return self.stack[-1]

    def __str__(self):
        return str(self.stack)


class MaxStack:

    def __init__(self):
        self.stack = Stack()
        self.max_stack = Stack()

    def push(self, key):
        self.stack.push(key)
        cur_max = self.max_stack.top() if not self.max_stack.empty() else None
        to_push = max(key, cur_max) if cur_max is not None else key
        self.max_stack.push(to_push)

    def pop(self):
        self.max_stack.pop()
        return self.stack.pop()

    def top(self):
        return self.stack.top()

    def max(self):
        return self.max_stack.top()

    def empty(self):
        return self.stack.empty()

    def __str__(self):
        return 'stack: ' + str(self.stack) + '\nmax_stack: ' + str(self.max_stack) + '\n'


class TwoStacksQueue:

    def __init__(self):
        self.to_enqueue = MaxStack()
        self.to_dequeue = MaxStack()

    def empty(self):
        return self.to_enqueue.empty() and self.to_dequeue.empty()

    def enqueue(self, key):
        self.to_enqueue.push(key)

    def dequeue(self):
        if self.to_dequeue.empty():
            while not self.to_enqueue.empty():
                self.to_dequeue.push(self.to_enqueue.pop())
        return self.to_dequeue.pop()

    def max(self):
        m1 = self.to_enqueue.max() if not self.to_enqueue.empty() else None
        m2 = self.to_dequeue.max() if not self.to_dequeue.empty() else None
        if m1 is not None and m2 is not None:
            return max(m1, m2)
        elif m1 is not None:
            return m1
        else:
            return m2

    def __str__(self):
        return str(self.to_enqueue) + str(self.to_dequeue)


def sliding_window_min(input, k):
    a = [-x for x in input]
    result = []
    q = TwoStacksQueue()
    for i in range(k):
        q.enqueue(a[i])
    result.append(-q.max())
    for i in range(k, len(a)):
        q.dequeue()
        q.enqueue(a[i])
        if q.max() is None:
            print(q)
        result.append(-q.max())
    return result


# some test code
if __name__ == "__main__":
    test_a, test_k = [1, 3, 4, 5, 2, 7], 3
    # should print [1, 3, 2, 2]
    print(sliding_window_min(test_a, test_k))

    test_a, test_k = [5, 4, 10, 1], 2
    # should print [4, 4, 1]
    print(sliding_window_min(test_a, test_k))

    test_a, test_k = [10, 20, 6, 10, 8], 5
    # should print [6]
    print(sliding_window_min(test_a, test_k))