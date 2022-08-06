# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class SportAnalyticsItem(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field()
    source_website = scrapy.Field()
    video_url = scrapy.Field()
    pass
