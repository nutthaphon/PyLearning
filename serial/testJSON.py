'''
Created on Sep 19, 2016

@author: nutt
'''

import json


json_string = json.dumps([1, 2, 3, "a", "b", "c"])
print json.loads(json_string)
