# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import sys
reload(sys)
sys.setdefaultencoding("utf-8")


class SinaComPipeline(object):

    def process_item(self, item, spider):

        Filename = item['sonUrls'][7:-6].replace('/','_')
        with open(item['subFilename'] + '\\' + Filename + '.txt', 'w') as f:
            f.write(item['content'])

        return item
