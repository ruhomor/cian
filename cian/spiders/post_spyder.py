import scrapy
from cian.items import CianCard
from selenium import webdriver


class CianParser(scrapy.Spider):
    name = "cian-page"
    page_num = 1
    pages_to_scrap = 4
    start_urls = [
        'https://cian.ru/cat.php?deal_type=sale&engine_version=2&offer_type=flat&p=1&region=1&room1=1&room2=1']
    page = start_urls[0]

    def __init__(self):
        self.driver = webdriver.Chrome()

    def parse(self, response):
        item = CianCard()
        offers_wrapper = response.xpath('//div[@data-name="Offers"]')

        self.driver.get(self.page)

        while True: # clicks all phone buttons
            try:
                phone = self.driver.find_element_by_xpath('//button[@data-name="PhoneButton"]')
                phone.click()
            except:
                break

        for offer in offers_wrapper.xpath('//div[@data-name="TopOfferCard"]'):
            item['urls'] = offer.xpath('.//div[@data-name="TopDescription"]/descendant::node()/@href').extract()
            item['desc'] = offer.xpath('.//div[@data-name="TopTitle"]/descendant::node()/text()').extract()
            item['jkname'] = offer.xpath('.//div[@data-name="JkName"]/div/a/text()').extract()  # i dont like this xpath
            item['deadline'] = offer.xpath('.//div[@data-name="Deadline"]/text()').extract()  # i dont like this xpath
            item['address'] = offer.xpath('.//div[@data-name="AddressItem"]/span/@content').extract()
            item['metro'] = offer.xpath('.//div[@data-name="Underground"]/a/div[2]/text()').extract()  # i dont like this xpath
            item['price'] = offer.xpath('.//div[@data-name="TopPrice"]/div[1]/text()').extract()  # i dont like this xpath
            item['price_pm'] = offer.xpath('.//div[@data-name="TopPrice"]/div[2]/text()').extract()  # i dont like this xpath
            item['phone'] = offer.xpath('.//span[@data-name="PhoneText"]/text()').extract()  # i dont like this xpath ? click ?

            yield item
        if self.page_num < self.pages_to_scrap:
            yield response.follow(self.nextpage(), callback=self.parse)
        else:
            self.driver.close()


    def nextpage(self):
        self.page_num += 1
        self.page = f'https://cian.ru/cat.php?deal_type=sale&engine_version=2&offer_type=flat&p={self.page_num}&region=1&room1=1&room2=1'
        return self.page

class CianMobileParser(scrapy.Spider):
    name = "cian-mobile"
    #start_urls = ['https://www.cian.ru/kupit-kvartiru/']
    start_urls = ['https://www.cian.ru/kupit-mnogkomnatnuyu-kvartiru-panelniy-dom/'] # used for button testing
    more_clicks = 1

    def __init__(self):
        self.driver = webdriver.Chrome()

    def parse(self, response):
        item = CianCard()
        cards_wrapper = response.xpath('//div[@data-name="PageWrapper"]')
        self.driver.get(self.start_urls[0])
        next = self.driver.find_element_by_xpath('//div[@class="c-footer-tomobile"]/a')
        next.click()

        while True: # clicks button as long as it exists
            try:
                next = self.driver.find_element_by_xpath('//button[@data-mark="Button"]')
                next.click()
            except:
                break

        self.driver.close()

        a = 1
        for card in cards_wrapper.xpath('//section[@data-name="CardContainer"]'):
            a += 1
            item['urls'] = card.xpath('.//div[@data-name="LinkArea"]/descendant::node()/@href').extract_first()
            item['metro'] = card.xpath('.//div[@data-name="Underground"]/descendant::node()/text()').extract_first()
            item['jkname'] = card.xpath('.//a[@data-name="OptionalAnchor"]/text()').extract_first()
            item['address'] = card.xpath('.//div[@data-name="Address"]/text()').extract_first()
            item['price'] = card.xpath('.//div[@data-name="OfferHeader"]/text()').extract_first()
            yield item
            #item['address'] = response.xpath('//div[@data-name="AddressItem"]/span/@content').extract()
            #item['price'] = response.xpath(
            #    '//div[@data-name="TopPrice"]/div[1]/text()').extract()  # i dont like this xpath
            #item['price_pm'] = response.xpath(
            #    '//div[@data-name="TopPrice"]/div[2]/text()').extract()  # i dont like this xpath
            #item['phone'] = response.xpath(
            #    '//span[@data-name="PhoneText"]/text()').extract()  # i dont like this xpath ? click ?