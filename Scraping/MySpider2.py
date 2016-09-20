from twisted.internet import reactor
import scrapy
from scrapy.crawler import CrawlerRunner
from scrapy.utils.log import configure_logging


class MySpider(scrapy.Spider):
    # Your spider definition
    name = 'blogspider'
    start_urls = ['https://blog.scrapinghub.com']
    
    custom_settings = {
        'DOWNLOAD_DELAY': '0',
        'COOKIES_ENABLED': 'True',
    }
    
    def parse(self, response):
        for title in response.css('h2.entry-title'):
            yield {'title': title.css('a ::text').extract_first()}

        next_page = response.css('div.prev-post > a ::attr(href)').extract_first()
        if next_page:
            yield scrapy.Request(response.urljoin(next_page), callback=self.parse)
        

configure_logging({'LOG_FORMAT': '%(levelname)s: %(message)s'})
runner = CrawlerRunner()

d = runner.crawl(MySpider)
d.addBoth(lambda _: reactor.stop()) #@UndefinedVariable
reactor.run() #@UndefinedVariable the script will block here until the crawling is finished



