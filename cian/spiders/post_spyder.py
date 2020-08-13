import scrapy
from cian.items import CianItem


class CianParser(scrapy.Spider):
    name = "cian-page"
    start_urls = [
        'https://cian.ru/cat.php?deal_type=sale&engine_version=2&offer_type=flat&region=1&room1=1&room2=1']

    def parse(self, response):
        item = CianItem()
        item['urls'] = response.xpath('//div[@data-name="TopDescription"]/descendant::node()/@href').extract()
        item['desc'] = response.xpath('//div[@data-name="TopTitle"]/descendant::node()/text()').extract()
        item['jkname'] = response.xpath('//div[@data-name="JkName"]/div/a/text()').extract()  # ??
        item['deadline'] = response.xpath('//div[@data-name="Deadline"]/text()').extract()  # ?
        item['address'] = response.xpath('//div[@data-name="AddressItem"]/span/@content').extract()
        item['metro'] = response.xpath('//div[@data-name="Underground"]/a/div[2]/text()').extract()  # ??
        item['price'] = response.xpath('//div[@data-name="TopPrice"]/div[1]/text()').extract()  # ??
        item['price_pm'] = response.xpath('//div[@data-name="TopPrice"]/div[2]/text()').extract()  # ??
        item['phone'] = response.xpath('//span[@data-name="PhoneText"]/text()').extract()  # ? click ?

        yield item
