# -*- coding: utf-8 -*-
import scrapy,csv,re,json
from scrapy import Request
from meituan.items import ShopItem

class ShopInfoSpider(scrapy.Spider):
    name = 'shopinfo'
    handle_httpstatus_list = [302]
    def start_requests(self):
        urls = []
        with open('shop_urls.csv','r', encoding="utf-8") as f:
            reader = csv.reader(f)
            for row in reader:
                if row[1] != 'url':
                    urls.append(row[1])
        for url in urls:
            print(url)
            if url:
                print(1)
                yield Request(url=url, callback=self.parse)
                pass

    def parse(self, response):
        shop_item = ShopItem()
        jsons = response.xpath('/html/body/script[@crossorigin="anonymous"]/text()')
        for data in jsons:
            js = data.extract()
            shopinfo = re.search('"rdploc":\[(.*?)\]', js)
            if shopinfo:
                data = shopinfo.group(1)
                res = json.loads(data)
                shop_item["cityId"] = res.get('cityId')
                shop_item["poiid"] = res.get('poiid')
                shop_item["name"] = res.get('name')
                shop_item["lat"] = res.get('lat')
                shop_item["lng"] = res.get('lng')
                shop_item["addr"] = res.get('addr')
                shop_item["phone"] = res.get('phone')
                shop_item["frontImg"] = res.get('frontImg')
                shop_item["showStatus"] = res.get('showStatus')
                shop_item["avgScore"] = res.get('avgScore')
                shop_item["showType"] = res.get('showType')
                shop_item["isQueuing"] = res.get('isQueuing')
                shop_item["areaid"] = res.get('areaid')
                shop_item["areaName"] = res.get('areaName')
                shop_item["districtid"] = res.get('districtid')
                shop_item["districtname"] = res.get('districtname')
                shop_item["avgPrice"] = res.get('avgPrice')
                shop_item["iUrl"] = res.get('iUrl')
                yield shop_item