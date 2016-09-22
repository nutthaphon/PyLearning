def logger(func):
    def inner(*args, **kwargs): #1
        print "Arguments were: %s, %s" % (args, kwargs)
        return func(*args, **kwargs) #2
    return inner

@logger
def foo1(x, y=1):
    return x * y

@logger
def foo2():
    return 2

foo1(5, 4)

foo1(1)

foo2()



