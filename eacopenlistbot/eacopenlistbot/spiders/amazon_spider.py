# -*- coding: utf-8 -*-


import scrapy
from scrapy.http import Request
from eacopenlistbot.items import EaCOpenListBotItem


class Amazon(scrapy.Spider):
    name = "Amazon"
    allowed_domains = ["amazon.es"]

    def __init__(self, argument=None, *args, **kwargs):
        super(Amazon, self).__init__(*args, **kwargs)
        #With the argument variable we tell the spider the category and so the start_urls
        #execution example
        #scrapy crawl Amazon -a argument=Cells
        self.category = argument  # In case we use the category at the pipeline
        if self.category == "Cells":
            self.start_urls = [
                "http://www.amazon.es/gp/bestsellers/electronics/934197031/ref=zg_bs_nav_e_2_665492031_pg_1?ie=UTF8&pg=1",
                "http://www.amazon.es/gp/bestsellers/electronics/934197031/ref=zg_bs_nav_e_2_665492031_pg_2?ie=UTF8&pg=2",
                "http://www.amazon.es/gp/bestsellers/electronics/934197031/ref=zg_bs_nav_e_2_665492031_pg_3?ie=UTF8&pg=3",
                "http://www.amazon.es/gp/bestsellers/electronics/934197031/ref=zg_bs_nav_e_2_665492031_pg_4?ie=UTF8&pg=4",
                "http://www.amazon.es/gp/bestsellers/electronics/934197031/ref=zg_bs_nav_e_2_665492031_pg_5?ie=UTF8&pg=5"
                ]
        elif self.category == "Tablets":
            self.start_urls = [
                "http://www.amazon.es/gp/bestsellers/computers/938010031/ref=zg_bs_nav_computers_1_computers",
                "http://www.amazon.es/gp/bestsellers/computers/938010031/ref=zg_bs_nav_computers_1_computers#2",
                "http://www.amazon.es/gp/bestsellers/computers/938010031/ref=zg_bs_nav_computers_1_computers#3",
                "http://www.amazon.es/gp/bestsellers/computers/938010031/ref=zg_bs_nav_computers_1_computers#4",
                "http://www.amazon.es/gp/bestsellers/computers/938010031/ref=zg_bs_nav_computers_1_computers#5"
                ]

    def parse(self, response):
        #we get the most selled products in amazon site
        amazonlinks = response.xpath('//div[@class="zg_title"]/a/@href').extract()

        for amazonlink in amazonlinks:
            #the strip() methode removes the carriage returns from the got link
            yield Request(amazonlink.strip(), self.parse)

        item = EaCOpenListBotItem()
        if self.category == "Cells":
            item["cam"] = response.xpath('//tr[td[contains(text(),"ptico")]]/td[@class="value"]/text()').extract()
            item["product"] = response.xpath('//tr[td="Nombre del modelo"]/td[@class="value"]/text()').extract()
        elif self.category == "Tablets":
            item["product"] = response.xpath('//tr[td="Series"]/td[@class="value"]/text()').extract()
        #Common xpath links to Cells and Tablets
        item["resol"] = response.xpath('//tr[td[contains(text(),"n de pantalla")]]/td[@class="value"]/text()').extract()
        item["cpu"] = response.xpath('//tr[td="Velocidad del procesador"]/td[@class="value"]/text()').extract()
        item["harddisk"] = response.xpath('//tr[td="Capacidad del disco duro"]/td[@class="value"]/text()').extract()
        item["ram"] = response.xpath('//tr[td[contains(text(),"Capacidad de la memoria RAM")]]/td[@class="value"]/text()').extract()
        item["os"] = response.xpath('//tr[td="Sistema operativo"]/td[@class="value"]/text()').extract()
        item["dimensions"] = response.xpath('//tr[td="Dimensiones del producto"]/td[@class="value"]/text()').extract()
        item["weight"] = response.xpath('//tr[td="Peso del producto"]/td[@class="value"]/text()').extract()
        item["vendor"] = response.xpath('//tr[td="Marca"]/td[@class="value"]/text()').extract()
        yield item
