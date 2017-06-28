# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class CrpnItem(scrapy.Item):
    title = scrapy.Field()
    tender_number = scrapy.Field()
    tender_type = scrapy.Field()
    tender_person = scrapy.Field()
    address = scrapy.Field()
    contact_person = scrapy.Field()
    tel_number = scrapy.Field()
    start_time = scrapy.Field()
    doc_sell_period = scrapy.Field()
    bid_open_time = scrapy.Field()
    bid_open_address = scrapy.Field()
    url = scrapy.Field()
    doc_sell_price = scrapy.Field()
    doc_sell_address = scrapy.Field()
    doc_send_address = scrapy.Field()
    tender_requirement = scrapy.Field()
    region = scrapy.Field()
    material_detail = scrapy.Field()
    file_url = scrapy.Field()
    path = scrapy.Field()
    pass
