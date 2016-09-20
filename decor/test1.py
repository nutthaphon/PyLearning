def decorator(fn):
    def inner(n):
        return fn(n) + 1
    return inner
 
@decorator
def f(n):
    return n + 1