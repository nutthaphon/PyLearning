'''
Created on Sep 27, 2016

@author: nutt
'''
from pprint import pformat
from twisted.internet import reactor
from twisted.web.client import Agent, Response, readBody
from twisted.web.http_headers import Headers
from twisted.internet.defer import Deferred
from twisted.internet.protocol import Protocol

class BeginningPrinter(Protocol):
    def __init__(self, finished):
        self.finished = finished
        self.remaining = 1024 * 10
        self.buff = None

    def dataReceived(self, bytes):
        if self.buff is None:
            self.buff = bytes
        else:
            self.buff += bytes
        #if self.remaining:
        #   display = bytes[:self.remaining]
        #    
        #    #print 'Some data received:'
        #    print display
        #    self.remaining -= len(display)
        #self.stockname = str(bytes).split(',')
        #print self.stockname
    def connectionLost(self, reason):
        self.stockname = str(self.buff).split(',')
        print 'Finished receiving body:', reason.getErrorMessage()
        print 'Number of Element:', len(self.stockname)
        self.finished.callback(None)
        #print str(self.buff).split(',')
        #self.finished.callback(self.buff)


class QueryStockSymbol:
    
    
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
        
        d = agent.request(
            'GET',
            'http://www.settrade.com/StaticPage/capture/alllst.html',
            None,
            None)
        d.addCallback(self.cbRequest)
        d.addBoth(self.cbShutdown)
        
        reactor.run()           #@UndefinedVariable

