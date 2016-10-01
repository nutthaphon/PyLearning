'''
Created on Sep 27, 2016

@author: nutt
'''

import scrapy
from scrapy.crawler import CrawlerRunner
from scrapy.crawler import CrawlerProcess
from scrapy.utils.log import configure_logging

from twisted.internet import reactor

from dataset.settrade.QueryStockSymbol import QueryStockSymbol
from dataset.settrade.spiders.SettradeSpider import SettradeSpider

'''
# Online retrieve stock symbol from settrade
stock=QueryStockSymbol()
stock.StartReactor()

'http://www.settrade.com/servlet/IntradayStockChartDataServlet?symbol='
'''

stock_list = ['ADVANC','INTUCH','CPF']

#";".join(["%s=%s" % (k, v) for k, v in params.items()])  ',stock'`

urls = ",".join(["http://www.settrade.com/servlet/IntradayStockChartDataServlet?symbol=%s" % stock for stock in stock_list])

print "URLS=",urls
#quit()

spider1 = SettradeSpider()

configure_logging({'LOG_FORMAT': '%(levelname)s: %(message)s'})


'''
runner = CrawlerRunner()

d = runner.crawl(spider1, start_urls=urls)
d.addBoth(lambda _: reactor.stop()) #@UndefinedVariable
reactor.run() #@UndefinedVariable the script will block here until the crawling is finished

#-a start_urls=''http://www.settrade.com/servlet/IntradayStockChartDataServlet?symbol=INTUCH','http://www.settrade.com/servlet/IntradayStockChartDataServlet?symbol=CPF','http://www.settrade.com/servlet/IntradayStockChartDataServlet?symbol=ADVANC''
'''
process = CrawlerProcess({
            'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
        })
        
process.crawl(spider1, start_urls=urls)
process.start() # the script will block here until the crawling is finished

