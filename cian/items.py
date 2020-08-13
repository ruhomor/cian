# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class CianItem(scrapy.Item):
    # define the fields for your item here like:
    desc = scrapy.Field()
    jkname = scrapy.Field()
    deadline = scrapy.Field()
    address = scrapy.Field()
    urls = scrapy.Field()
    metro = scrapy.Field()
    price = scrapy.Field()
    price_pm = scrapy.Field()
    pass
