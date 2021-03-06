    # -*- coding: utf-8 -*-


import scrapy
from scrapy.http import Request
from eacopenlistbot.items import EaCOpenListBotItem
import re


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
                #walmart unlocked, news cell phones
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

        #we get the product links in walmart site
        sitelinks = response.xpath('//div/a[@class="js-product-title"]/@href').extract()
        for sitelink in sitelinks:
            #the strip() methode removes the carriage returns from the got link
            sitelink = "http://www.walmart.com" + sitelink.strip()
            yield Request(sitelink, self.parse)

        item = EaCOpenListBotItem()
        product = response.xpath('//div/h1[@itemprop="name"]/span/text()').extract()
        if product:
            item["product"] = self.csv_preprocess(product[0])

        vendor = response.xpath('//div/a/span[@itemprop="brand"]/text()').extract()
        if vendor:
            item["vendor"] = vendor[0]

        default = response.xpath('//div[@class="js-ellipsis module"]/p/text()').extract()
        #if not default:
        #    default = response.body
        if default:
            #csv_preprocess input is expected to be raw text so we join all the items crawled in a string
            #We use the dot mark for later processing in order to tokenize sentences properly
            default = ' . '.join(default)
            item["default"] = self.csv_preprocess(default)
        yield item

    def csv_preprocess(self, text):
        #We remove any type of carriage return, tab and comma
        text = re.sub("\r\n", ". ", text)
        text = re.sub("\n", ". ", text)
        text = re.sub("\r", ". ", text)
        text = re.sub("\t", ". ", text)
        text = re.sub(",", " ", text)
        text = re.sub(r'<[^<]*?>', " ", text)  # Avoiding html tags
        text = re.sub(r'\s+', " ", text)  # Avoiding more than one blanks
        text = re.sub(r'\(|\)|®|\[|\]', " ", text) # Avoiding unneeded or undesired symbols
        return text