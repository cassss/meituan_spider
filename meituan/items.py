# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class MeituanItem(scrapy.Item):
    # define the fields for your item here like:
    region_url = scrapy.Field()
    pass

class RegionItem(scrapy.Item):
    # define the fields for your item here like:
    region_url = scrapy.Field()
    pass

class CityItem(scrapy.Item):
    # define the fields for your item here like:
    city_url = scrapy.Field()
    name     = scrapy.Field()
    pass

class UrlItem(scrapy.Item):
    url  = scrapy.Field()
    city = scrapy.Field()
    pass

class ShopItem(scrapy.Item):

    cityId = scrapy.Field()
    poiid = scrapy.Field()
    name = scrapy.Field()
    lat = scrapy.Field()
    lng = scrapy.Field()
    addr = scrapy.Field()
    phone = scrapy.Field()
    frontImg = scrapy.Field()
    showStatus = scrapy.Field()
    avgScore = scrapy.Field()
    showType = scrapy.Field()
    isQueuing = scrapy.Field()
    areaid = scrapy.Field()
    areaName = scrapy.Field()
    districtid = scrapy.Field()
    districtname = scrapy.Field()
    avgPrice = scrapy.Field()
    iUrl = scrapy.Field()
    pass
