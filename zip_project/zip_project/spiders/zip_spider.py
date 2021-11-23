import scrapy
from scrapy.loader import ItemLoader
from zip_project.items import The_Urge_Item
from scrapy.loader.processors import MapCompose, Join
import datetime
from urllib.parse import urljoin
import re
import math


class PostsSpider(scrapy.Spider):
	name = 'The_Urge'
	start_urls = ['https://theurge.com/']
	
	def parse(self,response):
		max_items = 300
		items_per_page = 20
		self.total_page_max = int(max_items/items_per_page)
		self.extracted_page_count = 0

		catagory_urls = response.xpath('//*[@class="_3EoM2"]//@href').extract()
		catagories_pages = {}		
		
		for cat_url in catagory_urls:
			print('yielding',urljoin(response.url,cat_url))	
			#yield scrapy.Request(urljoin(response.url,catagory_urls[0]),callback = self.parse_content) ##If this is the first 
		
		#yield scrapy.Request('https://theurge.com/women/search/?cat=clothing-dresses',callback = self.parse_content) ##If this is the first 
		
	def parse_content(self,response):
		self.extracted_page_count += 1
		total_cat_items = int(response.xpath('//*[@class="_3-VCf"]/text()').re('^\d{0,10}\+')[0].replace('+',''))
		items_per_page = 20

		if ('page=' in response.url) == False:
			page = 1
			next_url = response.url.replace('?cat',f'?page={str(page+1)}&cat') #creating the url for the next pagination
		else:
			page = int(re.findall('page=\d{0,10}&',response.url)[0].replace('page=','').replace('&',''))
			next_url = response.url.replace(f'page={page}',f'page={page+1}') #creating the url for the next pagination

		print('page number',page)
		print('response.url',response.url)
		print('total extracted_page_count',self.extracted_page_count)

		yield self.parse_item(response)

		if (self.extracted_page_count < self.total_page_max) and (page <= math.floor(total_cat_items/items_per_page)+1):
			yield scrapy.Request(next_url, callback=self.parse_content)

	def parse_item(self,response): ## method for adding more fields
		l = ItemLoader(item = The_Urge_Item(),response = response)
		l.add_xpath('price','//*[@class="eP0wn _2xJnS"]',MapCompose(lambda i: i.replace(',', ''), float),re ='\d{1,3}(?:[.,]\d{3})*(?:[.,]\d{2})')
		l.add_xpath('name','//*[@class = "_3I42k"]/text()')
		l.add_xpath('website','//*[@class = "ZV4Wf"]/text()')
		l.add_value('date',datetime.datetime.now())
		return l.load_item()

	# def parse(self,response):
	# 	item = The_Urge_Item()
	# 	item['price'] = response.xpath('//*[@class="eP0wn _2xJnS"]').re(r'\d{1,3}(?:[.,]\d{3})*(?:[.,]\d{2})')
	# 	return item

	# def parse(self,response):
	# 	page = response.url.split('/')[-1]
	# 	filename = 'theurge-%s.html' % page
	# 	with open(filename,'wb') as f:
	# 		f.write(response.body)
