import scrapy
from cian.items import CianItem


class CianParser(scrapy.Spider):
    name = "cian-page"
    start_urls = [
        'https://cian.ru/cat.php?deal_type=sale&engine_version=2&offer_type=flat&region=1&room1=1&room2=1']

    def parse(self, response):
        item = CianItem()
        item['urls'] = response.xpath('//div[@data-name="TopDescription"]/span/a/@href').extract()
        item['name'] = response.xpath('//div[@data-name="JkName"]/div/a/text()').extract()
        item['metro'] = response.xpath('//div[@data-name="Underground"]/a/div[2]/text()').extract()
        item['price'] = response.xpath('//div[@data-name="TopPrice"]/div[1]/text()').extract()
        item['price_per_meter'] = response.xpath('//div[@data-name="TopPrice"]/div[2]/text()').extract()
        #with open("page.html", "wb") as f:
        #    f.write(response.body)
        yield item
