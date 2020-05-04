# -*- coding: utf-8 -*-
from mendeley.items import MendeleyItem

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


class MendeleyPipeline(object):
    def process_item(self, item, spider):
        item['description'] = item['description'].replace('<strong>', '').replace('</strong>', '')
        item['title'] = item['title'].replace('<strong>', '').replace('</strong>', '')
        return item