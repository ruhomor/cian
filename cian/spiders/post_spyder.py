import scrapy
from cian.items import CianItem


class CianParser(scrapy.Spider):
    name = "cian-page"
    start_urls = [
        'https://cian.ru/cat.php?deal_type=sale&engine_version=2&offer_type=flat&region=1&room1=1&room2=1']


    def parse(self, response):
        item = CianItem()
        item['urls'] = response.xpath('//div[@class="undefined c6e8ba5398--main-info--oWcMk"]//a/@href').extract()
        item['metro'] = response.xpath('//div[@class="c6e8ba5398--underground-name--1efZ3"]/text()').extract()
        item['price'] = response.xpath('//div[@data-name="TopPrice"]/div[1]/text()').extract()
        with open("page.html", "wb") as f:
            f.write(response.body)
        yield item