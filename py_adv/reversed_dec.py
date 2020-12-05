from functools import wraps

def reversed_dec(func):
    @wraps(func)
    def inner(*args, **kwargs):
        return func(*args[::-1], **kwargs)
    return inner
