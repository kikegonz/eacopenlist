# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class EaCOpenListBotItem(scrapy.Item):
    vendor = scrapy.Field()
    product = scrapy.Field()
    default = scrapy.Field()
    pass