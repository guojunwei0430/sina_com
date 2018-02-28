# -*- coding: utf-8 -*-
import scrapy
from sina_com.items import SinaComItem
import os

import sys
reload(sys)
sys.setdefaultencoding("utf-8")


class SinaSpider(scrapy.Spider):
    name = 'sina'
    allowed_domains = ['sina.com.cn']
    start_urls = ['http://news.sina.com.cn/guide/']

    def parse(self, response):
        items = []
        parentTitle = response.xpath('//div[@id="tab01"]/div/h3/a/text()').extract()
        parentUrls = response.xpath('//div[@id="tab01"]/div/h3/a/@href').extract()

        subTitle = response.xpath('//div[@id="tab01"]/div//ul/li/a/text()').extract()
        subUrls = response.xpath('//div[@id="tab01"]/div//ul/li/a/@href').extract()

        for i in range(0, len(parentTitle)):
            parentFilename = '.\data\\' + parentTitle[i]
            if (not os.path.exists(parentFilename)):
                os.makedirs(parentFilename)

            for j in range(0, len(subUrls)):
                item = SinaComItem()

                item['parentTitle'] = parentTitle[i]
                item['parentUrls'] = parentUrls[i]
                if_belong = subUrls[j].startswith(parentUrls[i])
                if if_belong:
                    subFilename = parentFilename + '\\' + subTitle[j]
                    if (not os.path.exists(subFilename)):
                        os.makedirs(subFilename)

                    item['subTitle'] = subTitle[j]
                    item['subUrls'] = subUrls[j]
                    item['subFilename'] = subFilename

                    items.append(item)

        for item in items:
            yield scrapy.Request(url=item['subUrls'], meta={'meta_1': item}, callback=self.second_parse)

    def second_parse(self, response):

        meta_1 = response.meta['meta_1']
        sonUrls = response.xpath('//a/@href').extract()
        items = []
        for i in range(0, len(sonUrls)):
            if_belong = sonUrls[i].endswith('.shtml') and sonUrls[i].startswith(meta_1['parentUrls'])
            if if_belong:
                item = SinaComItem()
                item['parentTitle'] = meta_1['parentTitle']
                item['parentUrls'] = meta_1['parentUrls']
                item['subUrls'] = meta_1['subUrls']
                item['subTitle'] = meta_1['subTitle']
                item['subFilename'] = meta_1['subFilename']
                item['sonUrls'] = sonUrls[i]

                items.append(item)

        for item in items:
            yield scrapy.Request(url=item['sonUrls'], meta={'meta_2': item}, callback=self.detail_parse)

    def detail_parse(self, response):
        item = response.meta['meta_2']
        head = response.xpath("//h1[@class='main-title']/text()")
#        print '--------------'
#        print head
#        print '--------------'
        content_list = response.xpath('//div[@class="article"]/p/text()').extract()
        content = ''
        for content_one in content_list:
            content += ''.join(content_one)
#        print content
        if not head:
            head_f = []
        else:
            head_f = head.extract()[0]
        item['head'] = head_f
        item['content'] = content

        yield item
