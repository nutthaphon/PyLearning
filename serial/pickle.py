'''
Created on Sep 19, 2016

@author: nutt
'''
import cPickle


pickled_string = cPickle.dumps([1, 2, 3, "a", "b", "c"])
print cPickle.loads(pickled_string)