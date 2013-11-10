# -*- coding: UTF-8 -*-
from scrapy.spider import BaseSpider
from tutorial.items import DmozItem, ContactItem
from scrapy.selector import Selector
from scrapy.http import Request
import json
class DmozSpider(BaseSpider):
	name = "dmoz"
	allowed_domains = ["mall.edai.com"]
	start_urls = ["http://mall.edai.com/index/1"]
	index = 12550
	host = "http://mall.edai.com/index/"
	out = "out/"
	items = []

	def parse(self, response):
		while self.index < 12555:
			self.index += 1
			yield Request(url = self.host + str(self.index), callback = self.parse_item)
	def parse_item(self, response):
		item = DmozItem()
		itemContact = ContactItem()

		sel = Selector(response)
#		print u'提示信息'
#		print sel.xpath('//title').xpath('text()').extract()[0]
		if response.url.startswith('http://bj.edai.com'): 
			open('log/log.txt', 'ab').write('page not exists: ' + response.url + '\n') 
			return
		if sel.xpath('//title').xpath('text()').extract() == [u'提示信息']:
			open('log/log.txt', 'ab').write('page error: ' + response.url + '\n') 
			return
		file_page = open(self.out + str(response.url.split("/")[-1] + '.json'), 'wb')
		file_contact = open('log/contact.json', 'ab')
		item['link'] = response.url
		item['body'] = response.body
#		print response.url.split("/")[-1]
#		print type(response.url.split("/")[-1])
#		if response.url.split("/")[-1] == "140002" or response.url.split("/")[-1] == "140055":
#				open(response.url.split("/")[-1], 'wb').write(response.body)
#		self.items.append(item)
#		if len(self.items) % self.limit == 0:
		page = json.dumps(dict(item))
		file_page.write(page)
		
		if sel.xpath('//div[@class="c_contact"]/ul/li[1]/text()'):
				itemContact['person'] = sel.xpath('//div[@class="c_contact"]/ul/li[1]/text()').extract()[0]
				itemContact['phone'] = sel.xpath('//div[@class="c_contact"]/ul/li[2]').re(r'(\d+)')[0]
		contact = json.dumps(dict(itemContact))
		file_contact.write(contact + '\n')

		self.items = []
