# -*- coding: utf-8 -*-
import scrapy,csv,codecs
from scrapy import Request
from meituan.items import UrlItem,ShopItem

class ShopSpider(scrapy.Spider):
    name = 'shop'
    def start_requests(self):
        urls = []
        with open('region.csv','rb') as f:
            reader = csv.reader(codecs.iterdecode(f, 'utf-8'))
            i = 0
            for row in reader:
                if row[0] != 'city_url':
                    urls.append(row[0])
                    break
        for url in urls:
            yield Request(url=url, callback=self.parse)

    def parse(self, response):
        url_item = UrlItem()
        buy_urls = response.xpath('//*[@id="deals"]/dl/dd[1]/dl/dd/a/@href').extract()
        city     = response.xpath('//*[@id="deal-list"]/footer/div[1]/div/a/text()').extract()[0]
        for buy_url in buy_urls:
            buy_url = 'https:' + buy_url
            # yield Request(buy_url, callback=self.getShopInfo)
            url_item['url'] = buy_url
            url_item['city'] = city
            yield url_item
            
        next_url = response.xpath('//*[@id="deals"]/dl/dd[2]/div/a[2]/@href').extract()[0]
        if next_url:
            next_url = 'https:' + next_url
            yield Request(url=next_url, callback=self.parse, dont_filter=True)
    
    # def getShopInfo(self, response):
    #     shop_item = ShopItem()
    #     jsons = response.xpath('/html/body/script[@crossorigin="anonymous"]/text()')
    #     for data in jsons:
    #         js = data.extract()
    #         shopinfo = re.search('"rdploc":\[(.*?)\]', js)
    #         if shopinfo:
    #             data = shopinfo.group(1)
    #             res = json.loads(data)
    #             print(type(res), res)
    #             shop_item["name"]  = res.get('name')
    #             shop_item["phone"] = res.get('phone')
    #             shop_item["lat"]   = res.get('lat')
    #             shop_item["lng"]   = res.get('lng')
    #             shop_item["addr"]  = res.get('addr')
    #             yield shop_item