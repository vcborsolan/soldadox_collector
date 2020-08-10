# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class SoldadoxItem(scrapy.Item):
    # define the fields for your item here like:
    value = scrapy.Field()
    title = scrapy.Field() 
    publication = scrapy.Field() 
    description = scrapy.Field()
    cod = scrapy.Field()
    category = scrapy.Field()
    types = scrapy.Field()
    images = scrapy.Field()
    state = scrapy.Field()
    region = scrapy.Field()
    subregion = scrapy.Field()
    cep = scrapy.Field()
    neighborhood = scrapy.Field()
    url = scrapy.Field()
    car = scrapy.Field()
