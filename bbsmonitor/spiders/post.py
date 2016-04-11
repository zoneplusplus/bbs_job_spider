# -*- coding: utf-8 -*-
import json
import sys
from scrapy.spiders import CrawlSpider
from scrapy.selector import Selector
from scrapy.http import Request
from bbsmonitor.items import BbsmonitorItem

default_encoding = 'utf-8'
reload(sys)
sys.setdefaultencoding(default_encoding)

class BbSpider(CrawlSpider):
    name = "rspider"
    redis_key = "rspider:start_urls"
    start_urls=[]
    start_urls.append('http://bbs.hfut.edu.cn/forum/forum-55-2.html')
 
    for i in range(3, 1300):
     link='http://bbs.hfut.edu.cn/forum/'
     nextlink='forum-55-'+str(i)+'.html'
     link=link+nextlink
     print link
     start_urls.append(link)

    def start_requests(self):
        for url in self.start_urls:
          yield Request(url, cookies={'Text1':'', 'Password1':''}, callback=self.parse)

    def parse(self, response):
        selector = Selector(response)

        pos_name=selector.xpath('//span[contains(@id, "thread")]/a/text()').extract()
        pos_author=selector.xpath('//td[contains(@class, "author")]//cite/a/text()').extract()
        pos_response=selector.xpath('//td[contains(@class, "nums")]/strong/text()').extract()\

        for i in range(len(pos_name)):
            item=BbsmonitorItem()
            item['pos_name']= pos_name[i]
            item['pos_author']=pos_author[i]
            item['pos_response']=pos_response[i]
            yield  item
        print "done!"