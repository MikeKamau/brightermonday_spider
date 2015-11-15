from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy import Selector
from brightermonday_sample.items import BrightermondaySampleItem

class MySpider(CrawlSpider):
    name = "craig"
    allowed_domains = ["brightermonday.co.ke"]
    start_urls = ["https://brightermonday.co.ke/search/jobs-in-it-telecoms"]

    rules = (
        Rule(LinkExtractor(allow=(), restrict_xpaths=('//a[@rel="next"]',)), callback="parse_items", follow= True),
    )

    def parse_items(self, response):
        hxs = Selector(response)
        titles = hxs.xpath('//a[starts-with(@title, "More")]')
	items = []
        for title in titles:
           item = BrightermondaySampleItem()
           item["link"] = title.xpath("@href").extract()
	   item["title"] = title.xpath("h4/text()").extract()
           items.append(item)
	return(items)
