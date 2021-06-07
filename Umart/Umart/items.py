# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class UmartItem(scrapy.Item):
    ShopSourceID = scrapy.Field()
    Url = scrapy.Field()
    BaseUrl = scrapy.Field()
    SKU = scrapy.Field()
    MPN = scrapy.Field()
    Model = scrapy.Field()
    Title = scrapy.Field()
    PriceIncTax = scrapy.Field()
    IsInStock = scrapy.Field()
    QuantityAvailable = scrapy.Field()
