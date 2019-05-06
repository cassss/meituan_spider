# -*- coding: utf-8 -*-
import scrapy,csv,re,json,redis
from scrapy import Request
from meituan.items import shopUrlItem

class ShopInfoSpider(scrapy.Spider):
    name = 'shopinfo'
    
    def start_requests(self):
        rds = redis.Redis(host='localhost', port=6379, decode_responses=True)
        cate2s = rds.lrange("cate2", 0, -1)
        has_got = rds.lrange("has_got_url", 0, -1)
        with open('littleUrl.csv','r', encoding="utf-8") as f:
            reader = csv.reader(f)
            for row in reader:
                if row[2] != 'url':
                    cid = re.search(r"cid=(.*)&", row[2]).group(1)
                    if cid in cate2s:
                        # break
                        if row[2] not in has_got:
                            yield Request(url=row[2], callback=self.parse, dont_filter=True)

    def parse(self, response):
        url_item = shopUrlItem()
        rds = redis.Redis(host='localhost', port=6379, decode_responses=True)
        shops = response.xpath('//*[@id="deals"]/dl[@class="list"]/dd[@class="poi-list-item"]')
        allid = response.xpath('//*[@id="nav-bread"]/a[-1]')
        bid = re.search(r"bid=([0-9]+)", response.url).group(1)
        cid = re.search(r"cid=([0-9]+)", response.url).group(1)
        # shops = response.xpath('//*[@id="deals"]/dl[@class="list"]/dd[@class="poi-list-item"]/a/@href').extract()
        if len(shops) > 0:
            for shop in shops:
                # yield Request(shop, callback=self.getShopInfo)
                shop_url = shop.xpath('./a[@gaevent="imt/poilist/item"]/@href').extract()[0]
                url_item["url"]  = shop_url
                url_item["name"] = shop.xpath('.//span[@class="poiname"]/text()').extract()[0]
                url_item["poiid"]  = re.search(r"poi/([0-9]+)", shop_url).group(1)
                url_item["cid"]  = cid
                url_item["bid"]  = bid
                print(url_item["url"],"\n")
                yield url_item
            rds.lpush("has_got_url", response.url)
        else:
            rds.lpush("null_url", response.url)
        
        next_url = response.xpath('//*[@id="deals"]//div[@class="pager"]/a[@gaevent="imt/deal/list/pageNext"]/@href').extract()
        if next_url:
            next_url = "https://%s&cid=%d&bid=%d"%(next_url[0], int(cid), int(bid))
            yield Request(next_url, callback=self.parse)
    def getShopInfo(self, response):
        print(rds.lpush("shop_info", response.body))
        
        # for data in jsons:
        #     js = data.extract()
        #     shopinfo = re.search('"rdploc":\[(.*?)\]', js)
        #     if shopinfo:
        #         data = shopinfo.group(1)
        #         res = json.loads(data)
        #         shop_item["cityId"] = res.get('cityId')
        #         shop_item["poiid"] = res.get('poiid')
        #         shop_item["name"] = res.get('name')
        #         shop_item["lat"] = res.get('lat')
        #         shop_item["lng"] = res.get('lng')
        #         shop_item["addr"] = res.get('addr')
        #         shop_item["phone"] = res.get('phone')
        #         shop_item["frontImg"] = res.get('frontImg')
        #         shop_item["showStatus"] = res.get('showStatus')
        #         shop_item["avgScore"] = res.get('avgScore')
        #         shop_item["showType"] = res.get('showType')
        #         shop_item["isQueuing"] = res.get('isQueuing')
        #         shop_item["areaid"] = res.get('areaid')
        #         shop_item["areaName"] = res.get('areaName')
        #         shop_item["districtid"] = res.get('districtid')
        #         shop_item["districtname"] = res.get('districtname')
        #         shop_item["avgPrice"] = res.get('avgPrice')
        #         shop_item["iUrl"] = res.get('iUrl')
        #         yield shop_item