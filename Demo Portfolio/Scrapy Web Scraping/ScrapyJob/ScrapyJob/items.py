# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

class JobItem(scrapy.Item):
    # Visible content
    title = scrapy.Field()
    employer = scrapy.Field()
    town = scrapy.Field()
    tags = scrapy.Field()
    stress_tags = scrapy.Field()
    timestamp = scrapy.Field()
    link = scrapy.Field()

    # Metadata from data-* attributes
    affiliation = scrapy.Field()
    item_name = scrapy.Field()
    application_type = scrapy.Field()
    category1 = scrapy.Field()
    category2 = scrapy.Field()
    category3 = scrapy.Field()
    category4 = scrapy.Field()
    category5 = scrapy.Field()
    category6 = scrapy.Field()
    currency = scrapy.Field()
    item_brand = scrapy.Field()
    item_id = scrapy.Field()
    linktarget = scrapy.Field()
    list_id = scrapy.Field()
    list_index = scrapy.Field()
    list_name = scrapy.Field()
    location_id = scrapy.Field()
    price = scrapy.Field()
    prof_category = scrapy.Field()
    prof_id = scrapy.Field()
    prof_name = scrapy.Field()
    prof_position = scrapy.Field()
    prof_product_name = scrapy.Field()
    quantity = scrapy.Field()
    row_number = scrapy.Field()
    value = scrapy.Field()
    variant = scrapy.Field()
    id = scrapy.Field()

