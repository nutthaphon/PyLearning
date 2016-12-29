'''
Created on Sep 26, 2016

@author: nutt

Example of Scrapy command with arguments
$ scrapy crawl settrade_dataset -a start_urls=''http://www.settrade.com/servlet/IntradayStockChartDataServlet?symbol=INTUCH','http://www.settrade.com/servlet/IntradayStockChartDataServlet?symbol=CPF','http://www.settrade.com/servlet/IntradayStockChartDataServlet?symbol=ADVANC''

Example of job argument on Scrapinghub
start_urls => http://www.settrade.com/servlet/IntradayStockChartDataServlet?symbol=INTUCH,http://www.settrade.com/servlet/IntradayStockChartDataServlet?symbol=CPF,http://www.settrade.com/servlet/IntradayStockChartDataServlet?symbol=ADVANC
'''

import scrapy
import csv
import json
from twisted.internet.error import DNSLookupError
from twisted.internet.error import TimeoutError, TCPTimedOutError
from scrapy.spidermiddlewares.httperror import HttpError
from scrapy.crawler import CrawlerRunner
from scrapy.crawler import CrawlerProcess
from scrapy.utils.log import configure_logging

from settrade.items import SettradeItem
#from dataset.settrade.ThinkSpeakChannels import UpdateChannelFeed
from datetime import datetime, date, time

class SettradeSpider(scrapy.Spider):
    
    name = "settrade_dataset"
    
    settrade_headers={
        'Accept-Language': 'en-US,en;q=0.8,th;q=0.6',
        'Referer': 'http://www.settrade.com/C13_FastQuoteChart.jsp?stockSymbol=CPF&symbolType=s',
        'Accept-Encoding': 'gzip, deflate, sdch'}
    
    def __init__(self, *args, **kwargs):
        super(SettradeSpider, self).__init__(*args, **kwargs)
        
        print "KWARGS =>", kwargs
        if 'start_urls' in kwargs:
            print "Found start_urls in KWARGS =>", kwargs['start_urls']
            self.start_urls = kwargs['start_urls'].split(',')
        else:
            print "Not found start_urls in KWARGS"
            
    
    def start_requests(self):
        print "Loop of start_urls:", self.start_urls 

        for u in self.start_urls:   
            yield scrapy.Request(u, 
                                 callback=self.parse_httpbin,
                                 errback=self.errback_httpbin,
                                 method='GET',
                                 headers=self.settrade_headers,
                                 dont_filter=False)
        

    def parse_httpbin(self, response):
        self.logger.info('Got successful response from {}'.format(response.url))
        csv_header = [];
        reader = csv.reader(response.body.split('\n'), delimiter=',')
        for i, row in enumerate(reader):
            if i == 0:
                stock = row[0]
                print "Stock=>", stock
            elif i == 1: # Skip default header
                #print "Header=>" , row
                csv_header = ['UpdateDT', 'Prior', 'Last', 'Chg', 'Volume', 'Value', 'AccTotalVol', 'AccTotalVal'] 
                #print "Header=>", csv_header
            else:
                #print row
                item = SettradeItem()
                item['StockCollection'] = stock
                for j,col in enumerate(row): #row= ['27/12/2016 09:50:00', '49.25', '49.25', '', '0', '', '0', '']
                    #print "j=", j, ", col=", col, "\n"
                    if j == 0: #Convert UpdateDT to ISO format
                        dt = datetime.strptime(col, "%d/%m/%Y %H:%M:%S")
                        dtz = dt.isoformat()+'.000+07:00'      #"2016-12-27T09:50:00.000+07:00"
                        item[csv_header[j]] = dtz
                    else:
                        item[csv_header[j]] = col
                yield item
        '''
        #print response.body;
        l=1
        
        
        EachLineBody = response.body.splitlines()
        for row in EachLineBody:
            #print "Row length=", len(row)
            if l > 1 and len(row) > 0: #Skip 1st row 
                cols = row.split(',')
                print cols
                #print "Date=", cols[0] ,", Fruit=", cols[1], ", Amount=", cols[2]
            l+=1
        '''
        #ts=UpdateChannelFeed(query='api_key=QX8WJQHT10DRQ144&field1=10&field2=20&field3=30')
        #ts.StartReactor()
    
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
            



