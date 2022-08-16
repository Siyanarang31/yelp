# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class YelpItem(scrapy.Item):
    stars = scrapy.Field()
    username = scrapy.Field()
    title = scrapy.Field()
    reviewtext = scrapy.Field()
    permalink = scrapy.Field()
    reviewlocation = scrapy.Field()
    reviewdate = scrapy.Field()
    pass
