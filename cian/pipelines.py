# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import json


class CianPipeline:
    def __init__(self):
        self.info = []

    def close_spider(self, spider):
        self.file = open('items.jl', 'w')
        self.file.write(json.dumps(self.info))
        self.file.close()

    def process_item(self, item, spider):
        self.info.append(dict(item))
        return item
