# -*- coding: utf-8 -*-


import scrapy
from scrapy.http import Request
from eacopenlistbot.items import EaCOpenListBotItem


class Walmart(scrapy.Spider):
    name = "Walmart"
    allowed_domains = ["walmart.com"]

    def __init__(self, argument=None, *args, **kwargs):
        super(Walmart, self).__init__(*args, **kwargs)
        #With the argument variable we tell the spider the category and so the start_urls
        #execution example
        #scrapy crawl walmart -a argument=Cells
        self.category = argument  # In case we use the category at the pipeline
        if self.category == "Cells":
            self.start_urls = [
                "http://www.walmart.com/browse/cell-phones/unlocked-phones/1105910_1073085",
                ]
        elif self.category == "Tablets":
            self.start_urls = [
                "http://",
                ]

    def parse(self, response):
        #Next Button
        nextstart = response.xpath('//div/a[@class="paginator-btn paginator-btn-next"]/@href').extract()
        if nextstart:
            nextstart = self.start_urls[0] + nextstart[0]
            #If there is a next button we click on it
            yield Request(nextstart, self.parse)

        #we get the unlocked cells list from walmart
        sitelinks = response.xpath('//div/a[@class="js-product-title"]/@href').extract()
        for sitelink in sitelinks:
            #the strip() methode removes the carriage returns from the got link
            sitelink = "http://www.walmart.com" + sitelink.strip()
            yield Request(sitelink, self.parse)

        item = EaCOpenListBotItem()
        product = response.xpath('//div[@class="js-ellipsis module"]/p/b').extract()
        if product:
            item["product"] = product[0]
        item["vendor"] = response.xpath('//div/a[@id="brand"]/text()').extract()
        item["default"] = response.xpath('//div[@class="js-ellipsis module"]').extract()
        yield item