class Stack:
    def __init__(self):
        self.stack = []

    def push(self, key):
        self.stack.append(key)

    def pop(self):
        return self.stack.pop()

    def top(self):
        return self.stack[-1]

    def empty(self):
        return len(self.stack) == 0

    def __str__(self):
        return str(self.stack)


class MaxStack:
    def __init__(self):
        self.stack = Stack()
        self.max_stack = Stack()

    def push(self, key):
        self.stack.push(key)
        cur_max = self.max_stack.top() if not self.max_stack.empty() else key
        to_push = max(cur_max, key)
        self.max_stack.push(to_push)

    def pop(self):
        self.max_stack.pop()
        return self.stack.pop()

    def top(self):
        return self.stack.top()

    def max(self):
        return self.max_stack.top()

    def __str__(self):
        return 'stack: ' + str(self.stack) + '\nmax: ' + str(self.max_stack)


def reverse_notation(s):
    '''
    To calculate reverse Polish notation expression stack data structure will be helpful.
    :param s: list, [4, 3, '-', 2, '*']
    :return:
    '''
    stack = []
    for i in range(len(s)):
        if not s[i] in ['+', '-', '*', '/']:
            stack.append(s[i])
        else:
            num2 = stack.pop()
            num1 = stack.pop()
            stack.append(eval(str(num1) + s[i] + str(num2)))

    return stack.pop()


if __name__ == '__main__':
    # s = Stack()
    # s.push(5)
    # s.push(10)
    # s.push(5)
    # s.pop()
    # s.top()
    # s.pop()
    # s.push(7)
    # s.top()
    # s.pop()
    # s.push(3)
    # s.push(6)
    # print(s)
    s = [4, 3, '-', 2, '*']
    print(reverse_notation(s))