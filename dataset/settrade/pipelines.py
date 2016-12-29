# -*- coding: utf-8 -*-

import pymongo
from scrapy.conf import settings
from scrapy.exceptions import DropItem
from scrapy import log

from bson.objectid import ObjectId

from datetime import datetime, date, time

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
            stock_collection = item.pop('StockCollection')
            
            dt = datetime.strptime(item.get('UpdateDT'), "%d/%m/%Y %H:%M:%S")
            
            #print "document ", item , " importing.. to ", stock_collection
            self.collection = self.db[stock_collection]
            #result = self.collection.replace_one(update_datetime_filter, dict(item), True)
            
            result = self.collection.replace_one(
                {"UpdateDT": dt},
                {
                    u'AccTotalVal': item['AccTotalVal'],
                    u'AccTotalVol': item['AccTotalVol'],
                    u'Chg': item['Chg'],
                    u'Last': item['Last'],
                    u'Prior': item['Prior'],
                    u'UpdateDT': dt,
                    u'Value': item['Value'],
                    u'Volume': item['Volume']
                },
                False)
            print "Updated= ", result.modified_count, " or Insert New= ", result.upserted_id       
            #log.msg("Question added to MongoDB database!", level=log.DEBUG, spider=spider)
        return item

