# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
import os

import sys
reload(sys)
sys.setdefaultencoding("utf-8")


class SinaComItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    parentTitle = scrapy.Field()
    parentUrls = scrapy.Field()

    subTitle = scrapy.Field()
    subUrls =scrapy.Field()
    subFilename = scrapy.Field()

    sonUrls = scrapy.Field()

    head = scrapy.Field()
    content = scrapy.Field()
