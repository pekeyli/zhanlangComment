# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymongo
from scrapy.exceptions import DropItem
from scrapy import log
from scrapy.conf import settings
# class ZhanlangcommentPipeline(object):
#
#     def process_item(self, item, spider):
#         return item
#定义数据库的连接
class MongoDBPipeline(object):
    def __init__(self):
        connection = pymongo.MongoClient(settings['MONGODB_SERVER'], settings['MONGODB_PORT'])
        db = connection[settings['MONGODB_DB']]
        self.collection = db[settings['MONGODB_COLLECTION']]
    #判断数据是否有效，如果有效则将item插入到数据库中，否则丢掉这个item
    def process_item(self, item, spider):
        valid = True
        for data in item:
            if not data:
                valid = False
                raise DropItem("Missing {0}!".format(data))
        if valid:
            self.collection.insert(dict(item))
            log.msg("Question added to MongoDB database!", level=log.DEBUG, spider=spider)
        return item
