# -*- coding: utf-8 -*-

import pymongo
from scrapy.conf import settings
from scrapy.exceptions import DropItem
from scrapy import log

from bson.objectid import ObjectId

from datetime import datetime, date, time, timedelta
from pytz import timezone

import pytz
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
        utc = pytz.utc
        bangkok=timezone('Asia/Bangkok')

        for data in item:
            if not data:
                valid = False
                raise DropItem("Missing {0}!".format(data))
        
        if not item.get('UpdateDT'):
            valid = False
            raise DropItem("Missing Date/Time!")
        
        if valid:
            stock_collection = item.pop('StockCollection')
            
            dt  = datetime.strptime(item.get('UpdateDT'), "%d/%m/%Y %H:%M:%S")
            dt1 = bangkok.localize(dt, is_dst=False)
            dt1_utc = dt1.astimezone(utc)

            print "document ", dict(item) , " importing.. to ", stock_collection
            self.collection = self.db[stock_collection]
            
            result = self.collection.replace_one(
                {
                    "UpdateDT": dt1_utc
                },
                {
                    u'AccTotalVal': float(item['AccTotalVal'].strip()) if len(item['AccTotalVal'].strip()) > 0 else None,
                    u'AccTotalVol': float(item['AccTotalVol'].strip()) if len(item['AccTotalVal'].strip()) > 0 else None,
                    u'Chg': float(item['Chg'].strip()) if len(item['AccTotalVal'].strip()) > 0 else None,
                    u'Last': float(item['Last'].strip()) if len(item['AccTotalVal'].strip()) > 0 else None,
                    u'Prior': float(item['Prior'].strip()) if len(item['AccTotalVal'].strip()) > 0 else None,
                    u'UpdateDT': dt1_utc,
                    u'Value': float(item['Value'].strip()) if len(item['AccTotalVal'].strip()) > 0 else None,
                    u'Volume': float(item['Volume'].strip()) if len(item['AccTotalVal'].strip()) > 0 else None
                },
                True)
            print "Updated= ", result.modified_count, " or Insert New= ", result.upserted_id       
            #log.msg("Question added to MongoDB database!", level=log.DEBUG, spider=spider)
        return item

