class Buffer:
    def __init__(self, maxsize):
        self.maxsize = maxsize
        self.buffer = []

    def add(self, *a):
        list(map(lambda x: self.buffer.append(x), a))
        if len(self.buffer) >= self.maxsize:
            k, v = len(self.buffer) // self.maxsize, len(self.buffer) % self.maxsize
            for i in range(1, k + 1):
                print(sum(self.buffer[(i - 1) * self.maxsize : i * self.maxsize]))
            self.buffer = [] if v == 0 else self.buffer[-v:]
        return

    def get_current_part(self):
        return self.buffer
