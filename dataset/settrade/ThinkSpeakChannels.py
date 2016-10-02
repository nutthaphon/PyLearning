'''
Created on Oct 2, 2016

@author: nutt
'''

from twisted.internet import reactor
from twisted.web.client import Agent,  readBody

class UpdateChannelFeed:
    
    def __init__(self, *args, **kwargs):

        print "KWARGS =>", kwargs
        if 'query' in kwargs:
            print "Found query in KWARGS =>", kwargs['query']
            self.query = kwargs['query']
        else:
            print "Not found query in KWARGS"
            
    def cbBody(self, body):
        if body == '0':
            print 'Fail to update data!'
        else:
            print 'Update completed.'
        
    def cbRequest(self, response):
        d = readBody(response)
        d.addCallback(self.cbBody)
        return d
    
    def cbShutdown(self, ignored):
        reactor.stop()      #@UndefinedVariable
        
    
    def StartReactor(self):
        agent = Agent(reactor)
        d = agent.request(
            'GET',
            'https://api.thingspeak.com/update?'+self.query,
            None,
            None)
        d.addCallback(self.cbRequest)
        d.addBoth(self.cbShutdown)
        
        reactor.run()           #@UndefinedVariable
        
#ts=UpdateChannelFeed(query='api_key=QX8WJQHT10DRQ144&field1=10&field2=20&field3=30')
#ts.StartReactor()
