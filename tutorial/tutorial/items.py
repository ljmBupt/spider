# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field

class DmozItem(Item):
	body = Field()
	link = Field()

class ContactItem(Item):
	person = Field()
	phone = Field()
