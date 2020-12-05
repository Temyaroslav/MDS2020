class FlashError(Exception):
    pass

class FlashMaxFileSizeError(FlashError):
    pass

class FlashMemoryLimitError(FlashError):
    pass

class Flash:
    def __init__(self, capacity, max_file_size=None):
        self._capacity = capacity
        self._max_file_size = max_file_size

    def write(self, v):
        if self._max_file_size:
            if v > self._max_file_size:
                raise FlashMaxFileSizeError
        if v <= self._capacity:
            self._capacity -= v
        else:
            raise FlashMemoryLimitError
        return
