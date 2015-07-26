# -*- coding: utf-8 -*-


import scrapy
from scrapy.http import Request
from eacopenlistbot.items import EaCOpenListBotItem


class Amazon(scrapy.Spider):
    name = "Amazon"
    allowed_domains = ["amazon.com"]

    def __init__(self, argument=None, *args, **kwargs):
        super(Amazon, self).__init__(*args, **kwargs)
        #With the argument variable we tell the spider the category and so the start_urls
        #execution example
        #scrapy crawl Amazon -a argument=Cells
        self.category = argument  # In case we use the category at the pipeline
        if self.category == "Cells":
            self.start_urls = [
                #amazon unlocked, news cell phones
                "http://www.amazon.com/gp/search/ref=sr_nr_p_n_feature_keywords_0?fst=as%3Aoff&rh=n%3A2335752011%2Cn%3A!2335753011%2Cn%3A7072561011%2Cn%3A2407749011%2Cp_n_condition-type%3A6503240011%2Cp_n_feature_keywords_six_browse-bin%3A8079970011&bbn=2407749011&ie=UTF8&qid=1437858715&rnid=8079965011",
                ]
        elif self.category == "Tablets":
            self.start_urls = [
                "http://",
                ]

    def parse(self, response):
        #Next Button
        nextstart = response.xpath('//span/a[@class="pagnNext"]/@href').extract()
        if nextstart:
            nextstart = self.start_urls[0] + nextstart[0]
            #If there is a next button we click on it
            yield Request(nextstart, self.parse)

        #we get the most selled products in amazon site
        sitelinks = response.xpath('//div/a[@class="a-link-normal a-text-normal"]/@href').extract()
        for sitelink in sitelinks:
            #the strip() methode removes the carriage returns from the got link
            yield Request(sitelink.strip(), self.parse)

        item = EaCOpenListBotItem()
        item["product"] = response.xpath('//div/h1/span[@id="productTitle"]/text()').extract()
        item["vendor"] = response.xpath('//tr[td="Marca"]/td[@class="value"]/text()').extract()
        item["default"] = response.xpath('//div[@class="a-box-inner"]/ul').extract()
        yield item
