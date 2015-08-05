# -*- coding: utf-8 -*-


import scrapy
from scrapy.http import Request
from eacopenlistbot.items import EaCOpenListBotItem
import nltk
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
                "http://www.overstock.com/Electronics/Unlocked-Cell-Phones/18602/subcat.html?sort=Top+Sellers",
                ]
        elif self.category == "Tablets":
            self.start_urls = [
                "http://",
                ]

    def parse(self, response):
        #we get the product links in Overstock site
        sitelinks = response.xpath('//div/a[@class="pro-thumb"]/@href').extract()
        for sitelink in sitelinks:
            #the strip() methode removes the carriage returns from the got link
            yield Request(sitelink.strip(), self.parse)

        item = EaCOpenListBotItem()
        product = response.xpath('//div/span[@itemprop="name"]/h1/text()').extract()
        #We remove any comma from the product to keep the output csv format
        if product:
            item["product"] = re.sub(",", "", product[0])
        default = response.xpath('//div[@class="description toggle-content"]').extract()
        if default:
            #we tokenize the text crawled to keep the output csv format
            item["default"] = self.tokenize(default[0])
        yield item

    def tokenize(self, text):
        #This function goal is to tokenize the text crawled avoiding carriage returns, blanks, stopwords, html tags, etc
        text = re.sub("\n", "", text)
        text = re.sub("\t", "", text)
        text = re.sub("\r", "", text)
        pattern = r'''(?x)    # set flag to allow verbose regexps
            [^ ",<>()\t\n=]+  # All the characters we want to strip out
            '''
        text = nltk.regexp_tokenize(text, pattern)
        stopwords = nltk.corpus.stopwords.words('english')
        text = [w.lower() for w in text]
        text = [w for w in text if w not in stopwords]
        return text
