def exception_logger(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except (ArithmeticError, AssertionError, ZeroDivisionError) as err:
            print(err.__class__.__name__)
    return inner
