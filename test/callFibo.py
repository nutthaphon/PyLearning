
from foo.fibo import fib, fib2, fib3


print('Call to fib3()')
fib3(100)
print('\n')

print('Call to fib2()')
fib2(100)
print('\n')

print('Call to fib()')
fib(1000)
print('\n')   

print('Call to instance of fib()')
fib=fib
fib(500)