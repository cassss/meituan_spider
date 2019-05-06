# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
# import redis
import pymongo
from scrapy.conf import settings

class MeituanPipeline(object):
    def __init__(self):
        self.client = pymongo.MongoClient(host=settings['MONGO_HOST'], port=settings['MONGO_PORT'])
        # self.r = redis.Redis(host='localhost', port=6379, decode_responses=True)
        # self.got_poi = self.r.lrange("got_poi", 0, -1)
        self.db = self.client[settings['MONGO_DB']]  # 获得数据库的句柄
        
    def process_item(self, item, spider):
        if spider.name == "shopdata":
            coll = self.db["shop_url"]  # 获得collection的句柄
            urlItem = dict(item)  # 把item转化成字典形式
            coll.insert(urlItem)  # 向数据库插入一条记录
        return item
