# -*- coding: utf-8 -*-

# Scrapy settings for amazon_moviles project
#
# For simplicity, this file contains only the most important settings by
# default. All the other settings are documented here:
#
#     http://doc.scrapy.org/en/latest/topics/settings.html
#

BOT_NAME = 'eacopenlistbot'

SPIDER_MODULES = ['eacopenlistbot.spiders']
NEWSPIDER_MODULE = 'eacopenlistbot.spiders'

COOKIES_ENABLED = False
#USER_AGENT = "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:33.0) Gecko/20100101 Firefox/33.0"
USER_AGENT = 'pre_eacopenlistbot (+http://www.eacopenlist.org)'
DOWNLOAD_DELAY = 2.25
LOG_FILE = "log/crawlers.log"  # forced to run at same directory where scrapy.cfg exists
LOG_LEVEL = "INFO"
ITEM_PIPELINES = {'eacopenlistbot.pipelines.EaCOpenListBotPipeline': 300}
