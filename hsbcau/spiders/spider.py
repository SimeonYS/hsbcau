import re
import scrapy
from scrapy.loader import ItemLoader
from ..items import HsbcauItem
from itemloaders.processors import TakeFirst

pattern = r'(\xa0)?'

class HsbcauSpider(scrapy.Spider):
	name = 'hsbcau'
	start_urls = ['https://www.about.hsbc.com.au/news-and-media']

	def parse(self, response):
		post_links = response.xpath('//span[@class="tabular-list__title-wrapper"]/a/@href').getall()
		for link in post_links:
			if not "pdf" in link:
				yield response.follow(link, self.parse_post)

	def parse_post(self, response):
		date = response.xpath('//p[@class="page-description__meta"]/text()').get()
		title = response.xpath('//h1/text()').get()
		content = response.xpath('//div[@class="page-description__summary"]//text()').getall() + response.xpath('//div[@class="layout--9-3"][last()]//text()').getall()
		content = [p.strip() for p in content if p.strip()]
		content = re.sub(pattern, "",' '.join(content))

		item = ItemLoader(item=HsbcauItem(), response=response)
		item.default_output_processor = TakeFirst()

		item.add_value('title', title)
		item.add_value('link', response.url)
		item.add_value('content', content)
		item.add_value('date', date)

		yield item.load_item()
