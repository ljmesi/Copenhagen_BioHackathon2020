# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

from scrapy import Field, Item

class MendeleyItem(Item):
    institutions = Field()
    title = Field()    
    dataTypes = Field()
    description = Field()
    doi = Field()
    publicationDate = Field()
    dateAvailable = Field()
    version = Field()
    accessRights = Field()
    containerURI = Field()
    externalSubjectAreas = Field()
    keywords = Field()
    authors = Field()
    method = Field()
    source = Field()
    type_cont = Field()
