# -*- coding: utf-8 -*-


import scrapy
from scrapy.http import Request
from eacopenlistbot.items import EaCOpenListBotItem
import nltk


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
        product = response.xpath('//div[@class="js-ellipsis module"]/p/b/text()').extract()
        if product:
            product = product[0].lower()  # In order to tag colours properly at the preprocess function
            item["product"] = self.ie_preprocess(product)

        vendor = response.xpath('//div/a/span[@itemprop="brand"]/text()').extract()
        if vendor:
            item["vendor"] = self.ie_preprocess(vendor[0])

        default = response.xpath('//div[@class="js-ellipsis module"]').extract()
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