# -*- coding: utf-8 -*-


import scrapy
from scrapy.http import Request
from eacopenlistbot.items import EaCOpenListBotItem
import re


class Overstock(scrapy.Spider):
    name = "Overstock"
    allowed_domains = ["overstock.com"]

    def __init__(self, argument=None, *args, **kwargs):
        super(Overstock, self).__init__(*args, **kwargs)
        #With the argument variable we tell the spider the category and so the start_urls
        #execution example
        #scrapy crawl Overstock -a argument=Cells
        self.category = argument  # In case we use the category at the pipeline
        if self.category == "Cells":
            self.start_urls = [
                #Overstock unlocked cell phones
                "http://www.overstock.com/Electronics/Cell-Phones/912/cat.html?sort=New%20Arrivals",
                ]
        elif self.category == "Tablets":
            self.start_urls = [
                "http://",
                ]

    def parse(self, response):
        #There isn't next button code since it is javascript code under scroll event
        #We will sort by new arrivals to minimize the impact in knowing new products
        #we get the product links in Overstock site
        sitelinks = response.xpath('//div/a[@class="pro-thumb"]/@href').extract()
        for sitelink in sitelinks:
            #the strip() methode removes the carriage returns from the got link
            yield Request(sitelink.strip(), self.parse)

        item = EaCOpenListBotItem()
        product = response.xpath('//div[@class="product-title"]/h1/text()').extract()
        if product:
            item["product"] = self.csv_preprocess(product[0])

        vendor = response.xpath('//div/span[@id="brand-name"]/a/text()').extract()
        if vendor:
            item["vendor"] = vendor[0]

        default = response.xpath('//div[@class="description toggle-content"]').extract()
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
