# -*- coding: utf-8 -*-

'''
import scrapy
from scrapy.http import Request
from eacopenlistbot.items import EaCOpenListBotItem
import re


class <Site_name>(scrapy.Spider):
    name = "<Site_name>"
    allowed_domains = ["<Site_Domain>"]

    def __init__(self, argument=None, *args, **kwargs):
        super(<Site_name>, self).__init__(*args, **kwargs)
        #With the argument variable we tell the spider the category and so the start_urls
        #execution example
        #scrapy crawl <Site_name> -a argument=Cells
        self.category = argument  # In case we use the category at the pipeline
        if self.category == "Cells":
            self.start_urls = [
                #unlocked, news cell phones
                "<URL for unlocked, news cell phones>",
                ]
        elif self.category == "Tablets":
            self.start_urls = [
                "http://",
                ]
        elif self.category == "<And so on with the rest of the categories>":
            self.start_urls = [
                "http://",
                ]

    def parse(self, response):
        #Next Button
        nextstart = response.xpath('xpath for next button').extract()
        if nextstart:
            nextstart = self.start_urls[0] + nextstart[0]
            #If there is a next button we click on it
            yield Request(nextstart, self.parse)

        #we get the product links at the site
        sitelinks = response.xpath('xpath for product links').extract()
        for sitelink in sitelinks:
            #the strip() methode removes the carriage returns from the got link
            yield Request(sitelink.strip(), self.parse)

        item = EaCOpenListBotItem()
        #taking the items and preprocessing them to information extraction
        product = response.xpath('xpath for web title or product name').extract()
        if product:
            item["product"] = self.csv_preprocess(product[0])

        vendor = response.xpath('xpath for vendor name').extract()
        if vendor:
            item["vendor"] = vendor[0]

        default = response.xpath('xpath for eatures table or text').extract()
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


'''