from ADS.stack import Stack


class Queue:
    def __init__(self, max_len=100):
        self.head = 0
        self.tail = 0
        self.queue = [0] * max_len
        self.max_len = max_len

    def enqueue(self, key):
        self.queue[self.tail] = key
        self.tail = (self.tail + 1) % self.max_len

    def dequeue(self):
        res = self.queue[self.head]
        self.head = (self.head + 1) % self.max_len
        return res

    def empty(self):
        return self.head == self.tail

    def __str__(self):
        i = self.head
        q = []
        while i != self.tail:
            q.append(self.queue[i])
            i = (i + 1) % self.max_len
        return str(q)


class TwoStacksQueue:
    def __init__(self):
        self.to_enqueue = Stack()
        self.to_dequeue = Stack()

    def enqueue(self, key):
        self.to_enqueue.push(key)

    def dequeue(self):
        if self.to_dequeue.empty():
            while not self.to_enqueue.empty():
                self.to_dequeue.push(self.to_enqueue.pop())
        return self.to_dequeue.pop()

    def empty(self):
        return self.to_dequeue.empty() and self.to_enqueue.empty()

    def __str__(self):
        en = eval(str(self.to_enqueue))
        deq = list(reversed(eval(str(self.to_dequeue))))
        return str(en + deq)


if __name__ == '__main__':
    q = Queue()
    q.enqueue(17)
    q.enqueue(6)
    q.enqueue(8)
    q.dequeue()
    q.enqueue(17)
    q.dequeue()
    q.enqueue(2)
    q.enqueue(5)
    q.dequeue()
    q.enqueue(9)
    print(q)