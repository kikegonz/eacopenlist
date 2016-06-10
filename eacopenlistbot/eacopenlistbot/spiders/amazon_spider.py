# -*- coding: utf-8 -*-


import scrapy
from scrapy.http import Request
from eacopenlistbot.items import EaCOpenListBotItem
import re


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

        #we get the product links in amazon site
        sitelinks = response.xpath('//div/a[@class="a-link-normal a-text-normal"]/@href').extract()
        for sitelink in sitelinks:
            #the strip() methode removes the carriage returns from the got link
            yield Request(sitelink.strip(), self.parse)

        item = EaCOpenListBotItem()
        #taking the items and preprocessing them to information extraction
        product = response.xpath('//div/h1/span[@id="productTitle"]/text()').extract()
        if product:
            item["product"] = self.csv_preprocess(product[0])

        vendor = response.xpath('//div/a[@id="brand"]/text()').extract()
        if vendor:
            item["vendor"] = vendor[0]

        default = response.xpath('//div[@id="feature-bullets"]/ul/li').extract()
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
