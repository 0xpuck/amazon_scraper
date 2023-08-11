# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html
import scrapy

class AmazonUkItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    asin = scrapy.Field()
    filter = scrapy.Field()
    name = scrapy.Field()
    price = scrapy.Field()
    voucher = scrapy.Field()
    link = scrapy.Field()