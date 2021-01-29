class Deque:

    def __init__(self):
        self._size = 6000
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


def process_deque(commands):
    deque = Deque()
    res = []
    for command in commands:
        command = command.split()
        if len(command) == 2:
            if command[0] == 'push_front':
                res.append(deque.push_front(int(command[1])))
            elif command[0] == 'push_back':
                res.append(deque.push_back(int(command[1])))
        else:
            if command[0] == 'pop_front':
                res.append(deque.pop_front())
            elif command[0] == 'pop_back':
                res.append(deque.pop_back())
            elif command[0] == 'front':
                res.append(deque.front())
            elif command[0] == 'back':
                res.append(deque.back())
            elif command[0] == 'clear':
                res.append(deque.clear())
            elif command[0] == 'size':
                res.append(deque.size())

    return res


if __name__ == "__main__":
    test_cmd = ["push_front 1", "push_front 2", "push_back 6", "front", "back", "clear", "size", "back"]
    # should print ["ok", "ok", "ok", 2, 6, "ok", 0, "error"]
    print(process_deque(test_cmd))

    test_cmd = ["pop_front", "back", "push_back 2", "size"]
    # # should print ["error", "error", "ok", 1]
    print(process_deque(test_cmd))

    test_cmd = ["push_back 1", "push_front 10", "push_front 4", "push_front 5", "back", "pop_back", "pop_back", "back"]
    # should print ["ok", "ok", "ok", "ok", 1, 1, 10, 4]
    print(process_deque(test_cmd))