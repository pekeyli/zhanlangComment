# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy

#本页面用来定义数据存储的信息，简化插入数据库的操作
class ZhanlangcommentItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    username = scrapy.Field()
    time = scrapy.Field()
    comment = scrapy.Field()

    pass
