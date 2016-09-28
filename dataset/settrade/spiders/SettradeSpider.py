'''
Created on Sep 26, 2016

@author: nutt
'''

import scrapy


from twisted.internet.error import DNSLookupError
from twisted.internet.error import TimeoutError, TCPTimedOutError

from scrapy.spidermiddlewares.httperror import HttpError
from scrapy.crawler import CrawlerRunner
from scrapy.crawler import CrawlerProcess
from scrapy.utils.log import configure_logging



class SettradeSpider(scrapy.Spider):
    

    name = "settrade_dataset"
    
    settrade_headers={
        'Accept-Language': 'en-US,en;q=0.8,th;q=0.6',
        'Referer': 'http://www.settrade.com/C13_FastQuoteChart.jsp?stockSymbol=CPF&symbolType=s',
        'Accept-Encoding': 'gzip, deflate, sdch'}
    
    def __init__(self, *args, **kwargs):
        super(SettradeSpider, self).__init__(*args, **kwargs)
        
        if 'start_urls' in kwargs:
            print "found with =>", kwargs['start_urls']
        else:
            print "not found with =>" , self.start_urls
            
    
    def start_requests(self):
        #print "another arg:", args
        for u in self.start_urls:   
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
            



