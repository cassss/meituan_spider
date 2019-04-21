# -*- coding: utf-8 -*-
import scrapy


class ExampleSpider(scrapy.Spider):
    name = 'example'
    start_urls = ['https://baidu.com']

    def parse(self, response):
        jss = response.xpath('/html/body/script')
        print(jss)
        for js in jss:
            print(jss.xpath('./text()').extract()[0])
        pass
