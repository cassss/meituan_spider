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

    name   = scrapy.Field()
    phone  = scrapy.Field()
    lat    = scrapy.Field()
    lng    = scrapy.Field()
    addr   = scrapy.Field()
    pass
