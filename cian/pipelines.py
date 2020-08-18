# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import json
import functools
import pandas as pd

from cian.items import CianCard


def check_spider_pipeline(process_item_method):
    """Декоратор для проверки необходимости вызова pipeline.
    Используем только упомянутые в spider.pipeline классы"""

    @functools.wraps(process_item_method)
    def wrapper(self, item, spider):

        if hasattr(spider, 'pipeline') and self.__class__ in spider.pipeline:
            # spider.log(msg % 'executing', level=log.DEBUG)
            return process_item_method(self, item, spider)
        else:
            # spider.log(msg % 'skipping', level=log.DEBUG)
            return item

    return wrapper


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
        self.df.append(dict(item), ignore_index=True)
        self.df.to_csv(self.file, header=False, encoding='utf-8')
        return item


class AppendToFilePipeline:

    def process_item(self, item, spider):

        #if isinstance(item, CianCard)
        if spider.name == 'cian-page':

            _item = dict(desc=item['desc'],
                         jkname=item['jkname'],
                         deadline=item['deadline'],
                         address=item['address'],
                         urls=item['urls'],
                         metro=item['metro'],
                         price=item['price'],
                         price_pm=item['price_pm'],
                         phone=item['phone'])

        elif spider.name == 'cian-mobile':

            _item = dict(jkname=item['jkname'],
                         address=item['address'],
                         urls=item['urls'],
                         metro=item['metro'],
                         price=item['price'],
                         )

        with open("data.json", mode='a', encoding='utf-8') as f:
            try:
                feeds = json.load(f)
            except:
                feeds = list()

            feeds.append(_item)
            json.dump(feeds, f, ensure_ascii=False)
        return item

    def close_spider(self, spider):
        spider.logger.info("-------------------------SPIDER CLOSED-------------------------")
