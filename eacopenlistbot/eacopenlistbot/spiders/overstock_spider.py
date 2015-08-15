# -*- coding: utf-8 -*-


import scrapy
from scrapy.http import Request
from eacopenlistbot.items import EaCOpenListBotItem
import nltk


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
        product = response.xpath('//div/span[@itemprop="name"]/h1/text()').extract()
        if product:
            product = product[0].lower()  # In order to tag colours properly at the preprocess function
            item["product"] = self.ie_preprocess(product)

        default = response.xpath('//div[@class="description toggle-content"]').extract()
        if default:
            default = ''.join(default)  # ie_preprocess input is expected to be raw text
            item["default"] = self.ie_preprocess(default)
        yield item

    def ie_preprocess(self, text):
        #http://www.nltk.org/book/ch07.html   1.1 Information extraction Architecture
        sentences = nltk.sent_tokenize(text)
        sentences = [nltk.word_tokenize(sent) for sent in sentences]
        sentences = [nltk.pos_tag(sent) for sent in sentences]
        return sentences
