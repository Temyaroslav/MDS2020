class NonPositiveError(Exception):
    pass

class PositiveList(list):
    def append(self, num):
        if num <= 0:
            raise NonPositiveError
        super(PositiveList, self).append(num)
        return
