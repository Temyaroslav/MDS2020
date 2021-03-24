from collections import deque


class MyDeque:

    def __init__(self):
        self.s = deque()

    def push_front(self, num):
        self.s.appendleft(int(num))
        return 'ok'

    def push_back(self, num):
        self.s.append(int(num))
        return 'ok'

    def pop_front(self):
        if len(self.s) != 0:
            return self.s.popleft()
        else:
            return 'error'

    def pop_back(self):
        if len(self.s) != 0:
            return self.s.pop()
        else:
            return 'error'

    def front(self):
        if len(self.s) != 0:
            return self.s[0]
        else:
            return 'error'

    def back(self):
        if len(self.s) != 0:
            return self.s[-1]
        else:
            return 'error'

    def clear(self):
        self.s.clear()
        return 'ok'

    def size(self):
        return len(self.s)


def process_deque(commands):
    result = []
    d = MyDeque()
    for a in commands:
        if ' ' in a:
            command, num = a.split(' ')
            if command == 'push_front':
                result.append(d.push_front(num))
            else:
                result.append(d.push_back(num))
        else:
            if a == 'pop_front':
                result.append(d.pop_front())
            elif a == 'pop_back':
                result.append(d.pop_back())
            elif a == 'front':
                result.append(d.front())
            elif a == 'back':
                result.append(d.back())
            elif a == 'size':
                result.append(d.size())
            else:
                result.append(d.clear())
    return result


# some test code
if __name__ == "__main__":
    test_cmd = ["push_front 1", "push_front 2", "push_back 6", "front", "back", "clear", "size", "back"]
    # should print ["ok", "ok", "ok", 2, 6, "ok", 0, "error"]
    print(process_deque(test_cmd))

    test_cmd = ["pop_front", "back", "push_back 2", "size"]
    # should print ["error", "error", "ok", 1]
    print(process_deque(test_cmd))

    test_cmd = ["push_back 1", "push_front 10", "push_front 4", "push_front 5", "back", "pop_back", "pop_back", "back"]
    # should print ["ok", "ok", "ok", "ok", 1, 1, 10, 4]
    print(process_deque(test_cmd))