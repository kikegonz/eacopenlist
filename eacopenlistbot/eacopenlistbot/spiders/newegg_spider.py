# -*- coding: utf-8 -*-


import scrapy
from scrapy.http import Request
from eacopenlistbot.items import EaCOpenListBotItem
import nltk
import re


class Newegg(scrapy.Spider):
    name = "Newegg"
    allowed_domains = ["newegg.com"]

    def __init__(self, argument=None, *args, **kwargs):
        super(Newegg, self).__init__(*args, **kwargs)
        #With the argument variable we tell the spider the category and so the start_urls
        #execution example
        #scrapy crawl Newegg -a argument=Cells
        self.category = argument  # In case we use the category at the pipeline
        self.index = 1
        if self.category == "Cells":
            self.start_urls = [
                #newegg unlocked, news cell phones
                "http://www.newegg.com/Product/ProductList.aspx?Submit=ENE&IsNodeId=1&N=100026674%204814",
                ]
        elif self.category == "Tablets":
            self.start_urls = [
                "http://",
                ]

    def parse(self, response):
        #Next Button
        self.index += 1
        #Since next button is a javascript code at newegg.com we look for the easiest way to implement it
        #We'll concatenate the string &PAge= sequentially till the last page plus one that will not exist and will stop the crawler'
        nextstart = self.start_urls[0] + "&Page=" + str(self.index)
        yield Request(nextstart, self.parse)

        #we get the product links in walmart site
        sitelinks = response.xpath('//div/a[@title="View Details"]/@href').extract()
        for sitelink in sitelinks:
            #the strip() methode removes the carriage returns from the got link
            yield Request(sitelink.strip(), self.parse)

        item = EaCOpenListBotItem()
        product = response.xpath('//div/h1/span[@itemprop="name"]/text()').extract()
        #We remove any comma and tag from the product to keep the output csv format
        if product:
            product = product[0].strip()
            item["product"] = re.sub(",", "", product)
        vendor = response.xpath('//div[@class="objOption"]/a/@title').extract()
        if vendor:
            item["vendor"] = vendor[0]
        default = response.xpath('//div[@id="Specs"]').extract()
        if default:
            #we tokenize the text crawled to keep the output csv format
            item["default"] = self.tokenize(default[0])
        yield item

    def tokenize(self, text):
        #This function goal is to tokenize the text crawled avoiding carriage returns, blanks, stopwords, html tags, etc
        text = re.sub("\r\n", "", text)
        pattern = r'''(?x)    # set flag to allow verbose regexps
            ([^ ",<>()\t\n=])+  # All the characters we want to strip out
            '''
        text = nltk.regexp_tokenize(text, pattern)
        stopwords = nltk.corpus.stopwords.words('english')
        text = [w.lower() for w in text]
        text = [w for w in text if w not in stopwords]
        return text
