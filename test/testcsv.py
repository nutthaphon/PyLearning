'''
Created on Sep 28, 2016

@author: nutt
'''


examdata1 = '''
4/5/2015 13:34,Apples,73
4/5/2015 3:41,Cherries,85
4/6/2015 12:46,Pears,14
4/8/2015 8:59,Oranges,52
4/10/2015 2:07,Apples,152
4/10/2015 18:10,Bananas,23
4/10/2015 2:40,Strawberries,98
'''

l=1
for row in examdata1.splitlines():
    if l>1: #Skip 1st row
        cols = row.split(',')
        print "Date=", cols[0] ,", Fruit=", cols[1], ", Amount=", cols[2]
    l+=1
