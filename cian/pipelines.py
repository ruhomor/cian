# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import json
import pandas as pd


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


class CianPipelineAppendAll:  # TODO fix indices
    def __init__(self):
        self.df = pd.DataFrame(columns=['desc', 'jkname', 'deadline', 'address', 'urls', 'price', 'price_pm', 'phone'])

    def close_spider(self, spider):
        with open('items.csv', 'a') as self.file:
            self.df.to_csv(self.file, header=False)
        self.file.close()

    def process_item(self, item, spider):
        self.df = self.df.append(dict(item), ignore_index=True)
        return item


class CianPipelineAppendOneByOne:  # TODO fix indices
    def __init__(self):
        self.df = pd.DataFrame(columns=['desc', 'jkname', 'deadline', 'address', 'urls', 'price', 'price_pm', 'phone'])
        self.file = open('items.csv', 'a')

    def close_spider(self, spider):
        self.file.close()

    def process_item(self, item, spider):
        self.df.append(dict(item), ignore_index=True).to_csv(self.file, header=False)
        return item
