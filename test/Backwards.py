class Backwards:
    def __init__(self, val):
        self.val = val
        self.pos = len(val)
 
    def __iter__(self):
        return self
 
    def next(self):
        # We're done
        if self.pos <= 0:
            raise StopIteration
 
        self.pos = self.pos - 1
        return self.val[self.pos]