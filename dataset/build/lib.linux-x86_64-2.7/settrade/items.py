# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field

class SettradeItem(Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    StockCollection = Field()
    UpdateDT = Field()
    Prior = Field()
    Last = Field()
    Chg = Field()
    Volume = Field()
    Value = Field()
    AccTotalVol = Field()
    AccTotalVal = Field()
