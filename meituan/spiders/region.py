# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request
from meituan.items import RegionItem,CityItem

class RegionSpider(scrapy.Spider):
    name = 'region'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36',
    }
    def start_requests(self):
        url = 'https://i.meituan.com/index/changecity/'
        yield Request(url, headers=self.headers, callback=self.parse)

    def parse(self, response):
        region_item  = RegionItem()
        regions = response.xpath('//*[@id="cityBox"]/div[4]/div/ul')
        for region in regions:
            region_url = region.xpath('./li[last()]/a/@href').extract()
            region_url = 'https:' + region_url[0]
            yield Request(region_url, headers=self.headers, callback=self.getCity)
            region_item['region_url'] = region_url
            # yield region_item
        pass

    def getCity(self, response):
        city_item = CityItem()
        citys = response.xpath('//*[@id="morecity"]/div[2]/ul/li')
        for city in citys:
            city     = city.xpath('./a')
            city_url = 'https:' + city.xpath('./@href').extract()[0] + 'all/'
            name     = city.xpath('./text()').extract()
            city_item['name']     = name
            city_item['city_url'] = city_url
            yield city_item
        pass