# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from w3lib.html import remove_tags
from scrapy.loader.processors import Join, MapCompose, TakeFirst, Compose
import re
import dateparser

class Annonce(scrapy.Item):
    # define the fields for your item here like:
    url = scrapy.Field(output_processor=TakeFirst())
    titre = scrapy.Field(input_processor=MapCompose(str.strip),
                         output_processor=TakeFirst())
    prix = scrapy.Field(input_processor=MapCompose(str.strip, lambda s: s.replace('\xa0\u20ac', '')),
                        output_processor=TakeFirst())
    date = scrapy.Field(input_processor=MapCompose(str.strip, lambda s: re.search(r'(\d \w+ à \d+:\d+)', s).group(1)),
                        output_processor=Compose(TakeFirst(),lambda d: dateparser.parse(d).timestamp()))
    description = scrapy.Field(input_processor=MapCompose(remove_tags, str.strip),
                               output_processor=Join())
    pass
