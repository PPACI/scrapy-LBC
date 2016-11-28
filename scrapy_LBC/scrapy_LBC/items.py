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


def remove_empty_string(string_list):
    return [element for element in string_list if element != '']


def make_dict_from_list(string_list):
    tags = dict()
    for i in range(0, len(string_list) - 1, 2):
        tags[string_list[i].replace(' ', '_')] = string_list[i + 1]
    return tags


def convert_to_number(element):
    try:
        return int(element)
    except ValueError:
        try:
            return float(element)
        except ValueError:
            return element


def remove_unit(element):
    if isinstance(element, str):
        g = re.fullmatch("(\d+(?:\ \d+)*)\ ?\w+", element)
        if g is not None:
            return convert_to_number(g.group(1).replace(' ', ''))
        else:
            return element
    else:
        return element


def post_operation(tags):
    try:
        tags['Référence'] = str(tags['Référence'])
    except KeyError:
        pass
    return tags


class Annonce(scrapy.Item):
    # define the fields for your item here like:
    url = scrapy.Field(output_processor=TakeFirst())
    titre = scrapy.Field(input_processor=MapCompose(str.strip),
                         output_processor=TakeFirst())
    prix = scrapy.Field(
        input_processor=MapCompose(str.strip, lambda s: s.replace('\xa0\u20ac', ''), lambda s: s.replace(' ', '')),
        output_processor=Compose(TakeFirst(), int))
    date = scrapy.Field(input_processor=MapCompose(str.strip, lambda s: re.search(r'(\d+ \w+ à \d+:\d+)', s).group(1)),
                        output_processor=Compose(TakeFirst(), lambda d: dateparser.parse(d).isoformat()))
    description = scrapy.Field(input_processor=MapCompose(remove_tags, str.strip),
                               output_processor=Join())
    tag = scrapy.Field(
        input_processor=Compose(MapCompose(str.strip, convert_to_number, remove_unit), remove_empty_string,
                                make_dict_from_list),
        output_processor=Compose(TakeFirst(), post_operation))
