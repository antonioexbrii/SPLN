import scrapy
import re

def getNumber(number):
	number = re.sub(r'\.([0-9])k',r'\1 00', number)
	number = re.sub(r'comments',r'', number)
	number = re.sub(r'\ ',r'', number)
	return number



class QuotesByAuthor(scrapy.Spider):
	name = "lol"
	def start_requests(self):
		urls = [
			'https://www.reddit.com/r/leagueoflegends/',
		]
		for url in urls:
			yield scrapy.Request(url=url, callback=self.parse)
	def parse(self, response):
		page = response.url.split("/")[-2]
		filename = "Reddit_%s.json" % page
		with open(filename, 'w') as f:
			for item in response.css('div.scrollerItem'):
				votes = item.css('div._1rZYMD_4xY3gRcSS3p8ODO::text').get()
				comments = item.css('span.FHCV02u6Cp2zYL0fhQPsO::text').get()
				json = {
					"title" : item.css('div._3wiKjmhpIpoTE2r5KCm2o6').xpath('span/a/h2/text()').get(),
					"upVotes": getNumber(votes),
					"number_comments": getNumber(comments),
					"author": item.css('div.s1qo48hh-0').xpath('a/text()').get()
				}
				self.log(json)
				f.write(str(json))
				f.write(',\n')
			self.log("Fechou ficheiro %s" % filename)
