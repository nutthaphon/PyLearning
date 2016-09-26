def tag_wrap(tag):
    def decorator(fn):
        def inner(s):
            return '<%s>%s' % (fn(s), tag)
        return inner
    return decorator
 
@tag_wrap('b')
@tag_wrap('em')
def greet(name):
    return 'Hello, %s!' % name
 
print(greet('world'))