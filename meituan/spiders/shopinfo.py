# -*- coding: utf-8 -*-
import scrapy,csv,re,json
from scrapy import Request
from meituan.items import ShopItem

class ShopInfoSpider(scrapy.Spider):
    name = 'shopinfo'
    handle_httpstatus_list = [302]
    def start_requests(self):
        urls = []
        with open('url.csv','r', encoding="utf-8") as f:
            reader = csv.reader(f)
            for row in reader:
                if row[1] != 'url':
                    print(row[1])
                    urls.append(row[1])
        for url in urls:
            yield Request(url=url, callback=self.parse, dont_filter=True)

    def parse(self, response):
        shop_item = ShopItem()
        jsons = response.xpath('/html/body/script[@crossorigin="anonymous"]/text()')
        for data in jsons:
            js = data.extract()
            shopinfo = re.search('"rdploc":\[(.*?)\]', js)
            if shopinfo:
                data = shopinfo.group(1)
                res = json.loads(data)
                print(type(res), res)
                shop_item["name"]  = res.get('name')
                shop_item["phone"] = res.get('phone')
                shop_item["lat"]   = res.get('lat')
                shop_item["lng"]   = res.get('lng')
                shop_item["addr"]  = res.get('addr')
                yield shop_item