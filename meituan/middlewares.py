# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html

import scrapy,redis,random,requests,json
from scrapy import signals,Request
from scrapy.downloadermiddlewares.useragent import UserAgentMiddleware

class MeituanSpiderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod

    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, dict or Item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Response, dict
        # or Item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)

class MeituanDownloaderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called

        return None

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)



class MyUserAgentMiddleware(UserAgentMiddleware):

    def process_request(self, request, spider):
        request.headers['User-Agent'] = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36"


class ProxyMiddleware(object): 

    def __init__(self, proxy_url):
        self.first = True
        self.proxy_url = proxy_url
        self.useing = ''

    @classmethod
    def from_crawler(cls, crawler):
        settings = crawler.settings
        return cls(settings.get('PROXY_URL'))

    def getProxy(self):
        r = redis.Redis(host='localhost', port=6379, decode_responses=True)
        urls_count = r.llen('proxy_url')
        print('代理数量:', urls_count)
        if urls_count <20:
            print('代理池不足正在获取新代理地址')
            proxy_url = self.proxy_url
            print(proxy_url)
            res = json.loads(str(requests.post('http://47.93.202.182:8080/api/getip',data={
                'my_token':'ysknb',
                'url'     : proxy_url
            }).content, encoding='utf-8'))
            print(res.get('code'))
            ips = res.get('msg')
            urls = []
            print('新代理数量:',len(ips))
            for ip in ips:
                url = 'http://' + ip.get('ip') + ':' + ip.get('port')
                r.lpush('proxy_url', url)
        urls  = r.lrange('proxy_url', 0, -1)
        proxy = random.choice(urls)
        r.set('useing_proxy', proxy)
        return proxy

    def dropProxy(self):
        r = redis.Redis(host='localhost', port=6379, decode_responses=True)
        useing = r.get('useing_proxy')
        r.lpush('bad_url', useing)
        r.ltrim('bad_url', 0, -1)
        if r.llen('bad_url') >20 :
            proxys = r.lrange('bad_url', 0, -1)
            print(proxys)
            for proxy in proxys:
                r.lrem('proxy_url', 0, proxy)
                r.lrem('bad_url', 0, proxy)
                pass
            

    def addProxy(self, request):
        proxy = self.getProxy()
        if proxy:
            request.meta['proxy'] = proxy
        return request

    # def getProxy(self):
    #     res = requests.get("http://127.0.0.1:5010/get/").content
    #     self.useing = str(res, encoding="utf-8")
    #     if self.useing == 'no proxy!':
    #         print('没有代理')
    #         return ''
    #     else:
    #         self.useing = 'http://' + self.useing
    #     return self.useing

    # def dropProxy(self):
        # requests.get("http://127.0.0.1:5010/delete/?proxy={}".format(self.useing))
        # pass

    def process_request(self, request, spider):
        if self.first:
            request = self.addProxy(request)
            self.first = False
            pass
        print("proxy:", request.meta['proxy'])

    def process_response(self, request, response, spider):
        '''对返回的response处理'''
        # 如果返回的response状态不是200，重新生成当前request对象
        if response.status != 200:
            self.dropProxy()
            request = self.addProxy(request)
            return request
        return response

    def process_exception(self, request, exception, spider):
        # 出现异常时（超时）使用代理
        print("\n出现异常:",exception, "\n")
        self.first = False
        self.dropProxy()
        request = self.addProxy(request)
        return request
