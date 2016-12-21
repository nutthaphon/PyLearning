from scrapy import Spider
from scrapy.selector import Selector

from stack.items import StackItem


class StackSpider(Spider):
    name = "stack"
    allowed_domains = ["stackoverflow.com"]
    start_urls = [
      #  "http://stackoverflow.com/questions?pagesize=50&sort=newest"
        "http://pantip.com/forum/mbk"
    ]

    def parse(self, response):
        questions = Selector(response).xpath('//div[@class="post-item-title"]')
        
        for question in questions:
            item = StackItem()
            item['title'] = question.xpath('@namespaceURI')
            item['url'] = question.xpath('a/@href')
            #print "Topic link = %s" % item['title']
            #    $x("//div[@class=\"post-item-title\"]")[0].innerText
            #item['url'] = question.xpath('a[@class="question-hyperlink"]/@href').extract()[0]
            yield item



