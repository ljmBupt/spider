from scrapy.spider import BaseSpider
from tutorial.items import DmozItem
from scrapy.http import Request
import json
class DmozSpider(BaseSpider):
	name = "dmoz"
	allowed_domains = ["mall.edai.com", "bj.edai.com"]
	start_urls = ["http://mall.edai.com/index/1"]
	index = 0
	host = "http://mall.edai.com/index/"
	out = "out/"
	items = []
	count = 1
	limit = 10
	def parse(self, response):
		while self.index < 100:
			self.index += 1
			yield Request(url = self.host + str(self.index), callback = self.parse_item)
	def parse_item(self, response):
		item = DmozItem()
		if response.url == 'http://bj.edai.com':
			yield item
		item['body'] = response.body
		item['link'] = response.url
		self.items.append(item)
		if len(self.items) % self.limit == 0:
			open(self.out + str(self.count), 'wb').write(json.dumps(self.items))
			self.count += 1
			self.items = []
		yield item
