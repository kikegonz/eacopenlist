# -*- coding: utf-8 -*-


import scrapy
from scrapy.http import Request
from eacopenlistbot.items import EaCOpenListBotItem
import re


class Mysmartprice(scrapy.Spider):
    name = "Mysmartprice"
    allowed_domains = ["mysmartprice.com"]

    def __init__(self, argument=None, *args, **kwargs):
        super(Mysmartprice, self).__init__(*args, **kwargs)
        #With the argument variable we tell the spider the category and so the start_urls
        #execution example
        #scrapy crawl Mysmartprice -a argument=Cells
        self.category = argument  # In case we use the category at the pipeline
        if self.category == "Cells":
            self.start_urls = [
                #mysmartprice cell phones
                "http://www.mysmartprice.com/mobile/pricelist/mobile-price-list-in-india.html#subcategory=mobile",
                ]
        elif self.category == "Tablets":
            self.start_urls = [
                "http://",
                ]

    def parse(self, response):
        #Next Button
        nextstart = response.xpath('//a[text()="Next"]/@href').extract()
        if nextstart:
            nextstart = self.start_urls[0] + nextstart[0]
            #If there is a next button we click on it
            yield Request(nextstart, self.parse)

        #we get the product links in mysmartprice site
        sitelinks = response.xpath('//div/a[@class="prdct-item__name"]/@href').extract()
        for sitelink in sitelinks:
            #the strip() methode removes the carriage returns from the got link
            yield Request(sitelink.strip(), self.parse)

        item = EaCOpenListBotItem()
        product = response.xpath('//div/h1[@class="prdct-dtl__ttl"]/text()').extract()
        if product:
            item["product"] = self.csv_preprocess(product[0])

        vendor = response.xpath('//div/img[@class="prdct-dtl__brnd-img"]/@alt').extract()
        if vendor:
            item["vendor"] = vendor[0]

        default = response.xpath('//div[@data-id="technical-specifications"]').extract()
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
        text = re.sub(r'\(|\)|®|\[|\]', " ", text)  # Avoiding unneeded or undesired symbols
        return text