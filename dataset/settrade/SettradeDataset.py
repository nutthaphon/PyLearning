'''
Created on Sep 26, 2016

@author: nutt
'''

import scrapy

from pprint import pformat

from twisted.internet import reactor
from twisted.web.client import Agent, Response, readBody
from twisted.web.http_headers import Headers

from twisted.internet.defer import Deferred
from twisted.internet.protocol import Protocol
from twisted.internet.error import DNSLookupError
from twisted.internet.error import TimeoutError, TCPTimedOutError

from scrapy.spidermiddlewares.httperror import HttpError
from scrapy.crawler import CrawlerRunner
from scrapy.crawler import CrawlerProcess
from scrapy.utils.log import configure_logging

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

'''

agent = Agent(reactor)

d = agent.request(
    'GET',
    'http://www.settrade.com/StaticPage/capture/alllst.html',
    None,
    None)

def cbBody(body):
    print('Response body:')
    stock_list = body.split(',')
    print('No. of Stock is ', len(stock_list))
    print(stock_list)
    
def cbRequest(response):
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
    d.addCallback(cbBody)
    return d

d.addCallback(cbRequest)

def cbShutdown(ignored):
    reactor.stop()      #@UndefinedVariable
d.addBoth(cbShutdown)

reactor.run()           #@UndefinedVariable
'''

stock_list = {'ADVANC', 'INTUCH', 'CPF'}
start_urls = []

for item in stock_list:
    start_urls.append("http://www.settrade.com/servlet/IntradayStockChartDataServlet?symbol=" + item)

class SettradeSpider(scrapy.Spider):
    

    name = "settrade_dataset"

    settrade_headers={
        'Accept-Language': 'en-US,en;q=0.8,th;q=0.6',
        'Referer': 'http://www.settrade.com/C13_FastQuoteChart.jsp?stockSymbol=CPF&symbolType=s',
        'Accept-Encoding': 'gzip, deflate, sdch'}
    
    def start_requests(self):
        for u in start_urls:
            yield scrapy.Request(u, 
                                 callback=self.parse_httpbin,
                                 errback=self.errback_httpbin,
                                 method='GET',
                                 headers=self.settrade_headers,
                                 dont_filter=False)

    def parse_httpbin(self, response):
        self.logger.info('Got successful response from {}'.format(response.url))
        print response.body;

    def errback_httpbin(self, failure):
        # log all failures
        self.logger.error(repr(failure))

        # in case you want to do something special for some errors,
        # you may need the failure's type:

        if failure.check(HttpError):
            # these exceptions come from HttpError spider middleware
            # you can get the non-200 response
            response = failure.value.response
            self.logger.error('HttpError on %s', response.url)

        elif failure.check(DNSLookupError):
            # this is the original request
            request = failure.request
            self.logger.error('DNSLookupError on %s', request.url)

        elif failure.check(TimeoutError, TCPTimedOutError):
            request = failure.request
            self.logger.error('TimeoutError on %s', request.url)
            

process = CrawlerProcess({
    'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
})

process.crawl(SettradeSpider)
process.start() # the script will block here until the crawling is finished



