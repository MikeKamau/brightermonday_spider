from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy import Selector
from scrapy.http.request import Request
from brightermonday_sample.items import BrightermondaySampleItem
class MySpider(CrawlSpider):
	name = "bright"
	allowed_domains = ["brightermonday.co.ke"]
	start_urls = ["https://brightermonday.co.ke/search/jobs-in-it-telecoms"]

	rules = (
		
     	Rule(LinkExtractor(allow=(), restrict_xpaths=('//a[@rel="next"]',)), callback="parse_job_links", follow= True),
	)

	def parse_job_links(self, response):
		hxs = Selector(response)
		job_links = hxs.xpath('//a[starts-with(@title, "More")]/@href').extract()
		for job in job_links:
			yield Request( job, callback=self.parse_job_details)
        		
	def parse_job_details(self, response):
		hxs = Selector(response)
		item = BrightermondaySampleItem()
		item['link'] = response.url
		item['title'] = hxs.xpath('//h2/text()').extract()
		item['desc'] = hxs.xpath('//article[@class="resultDetail"]/p/text()').extract()
		return item