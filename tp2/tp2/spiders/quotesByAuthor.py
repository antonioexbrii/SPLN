import scrapy

class QuotesByAuthor(scrapy.Spider):
	name = "quotesauthors"
	def start_requests(self):
		urls = [
			'http://quotes.toscrape.com/page/1/',
			'http://quotes.toscrape.com/page/2/',
			'http://quotes.toscrape.com/page/3/',
		]
		for url in urls:
			yield scrapy.Request(url=url, callback=self.parse)
	def parse(self, response):
		page = response.url.split("/")[-2]
		filename = "quotesbyauthor-%s.json" % page
		with open(filename, 'w') as f:
			for quote in response.css('div.quote'):
				jsonitem = {
					'text':quote.css('span.text::text').get(),
					'author':quote.xpath('span/small/text()') .get(),
				}
				self.log(jsonitem)
				f.write(str(jsonitem))
				f.write(',\n')
			self.log("Fechou ficheiro %s" % filename)
