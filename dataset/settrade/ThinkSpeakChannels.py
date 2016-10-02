'''
Created on Oct 2, 2016

@author: nutt
'''
from pprint import pformat
from twisted.internet import reactor
from twisted.web.client import Agent, Response, readBody
from twisted.web.http_headers import Headers
from twisted.internet.defer import Deferred
from twisted.internet.protocol import Protocol
from decor.Asterisk_Parameter_Arguments import args

class UpdateChannelFeed:
    
    def __init__(self, *args, **kwargs):
        super(UpdateChannelFeed, self).__init__(*args, **kwargs)
        print "KWARGS =>", kwargs
        if 'query' in kwargs:
            print "Found query in KWARGS =>", kwargs['query']
            self.query = kwargs['query'].split(',')
        else:
            print "Not found query in KWARGS"
            
    def cbBody(self, body):
        print('Response body:')
        stock_list = body.split(',')
        print('No. of Stock is ', len(stock_list))
        print(stock_list)
        
    def cbRequest(self, response):
        #print 'Response version:', response.version
        #print 'Response code:', response.code
        #print 'Response phrase:', response.phrase
        #print 'Response headers:'
        #print pformat(list(response.headers.getAllRawHeaders()))
        
        #finished = Deferred()
        #response.deliverBody(BeginningPrinter(finished))
        #print "Return: " + response.deliverBody
        #print stock_dict.stockname
        d = readBody(response)
        d.addCallback(self.cbBody)
        return d
    
    def cbShutdown(self, ignored):
        reactor.stop()      #@UndefinedVariable
        
    
    def StartReactor(self):
        agent = Agent(reactor)
        # https://api.thingspeak.com/update?api_key=QX8WJQHT10DRQ144&field1=0
        d = agent.request(
            'GET',
            'https://api.thingspeak.com/update?'+self.query,
            None,
            None)
        d.addCallback(self.cbRequest)
        d.addBoth(self.cbShutdown)
        
        reactor.run()           #@UndefinedVariable
        


