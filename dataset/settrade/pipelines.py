# -*- coding: utf-8 -*-

import pymongo
from scrapy.conf import settings
from scrapy.exceptions import DropItem
from scrapy import log

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


class SettradePipeline(object):
    def process_item(self, item, spider):
        return item

class MongoDBPipeline(object):

    def __init__(self):
        connection = pymongo.MongoClient(
            settings['MONGODB_SERVER'],
            settings['MONGODB_PORT']
        )
        self.db = connection[settings['MONGODB_DB']]
        #self.collection = db[settings['MONGODB_COLLECTION']]
        print "MongoDB connected."

    def process_item(self, item, spider):
        valid = True
        for data in item:
            if not data:
                valid = False
                raise DropItem("Missing {0}!".format(data))
        if valid:
            mgcollection = item['StockCollection']
            mgdocument = item[1:]
            print "document ", mgdocument , " importing.. to ", mgcollection
            self.collection = self.db[settings[mgcollection]]
            self.collection.insert(dict(mgdocument))
            log.msg("Question added to MongoDB database!",
                    level=log.DEBUG, spider=spider)
        return item

