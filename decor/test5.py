def b(fn):
    return lambda s: '<b>%s</b>' % fn(s)
 
def em(fn):
    return lambda s: '<em>%s</em>' % fn(s)
 
@b
@em
def greet(name):
    return 'Hello, %s!' % name


greet('world')