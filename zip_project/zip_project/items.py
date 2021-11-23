# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

#import scrapy

from scrapy.item import Item, Field
class The_Urge_Item(Item):
	# Primary fields
	brand = Field()
	description = Field()

	price = Field() 
	previous_price = Field()
	
	website = Field() 	 
	
	date = Field()


