def log_calls(fn):
    ''' Wraps fn in a function named "inner" that writes
        the arguments and return value to logfile.log '''
    def inner(*args, **kwargs):
        # Call the function with the received arguments and
        # keyword arguments, storing the return value
        out = apply(fn, args, kwargs)
 
        # Write a line with the function name, its
        # arguments, and its return value to the log file
        with open('logfile.log', 'a') as logfile:
            logfile.write(
                '%s called with args %s and kwargs %s, returning %s\n' %
                (fn.__name__,  args, kwargs, out))
 
        # Return the return value
        return out
    return inner