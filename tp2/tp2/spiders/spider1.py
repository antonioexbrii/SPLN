import scrapy
import re

user = "http://www.reddit.com/user/"

def trimNumber(number):
	number = re.sub(r'\.([0-9])k',r'\1 00', number)
	number = re.sub(r'comments',r'', number)
	number = re.sub(r'\ ',r'', number)
	return number

def trimAuthor(author):
	author = re.sub(r'\w/',user, author)
	return author


class Reddit(scrapy.Spider):
	name = "reddit"
	def start_requests(self):
		urls = [
			'https://www.reddit.com/',
			'https://www.reddit.com/r/leagueoflegends/',
			'https://www.reddit.com/r/gameofthrones/',
		]
		for url in urls:
			yield scrapy.Request(url=url, callback=self.parse)

	def parse(self, response):
		page = response.url.split("/")[-2]
		filename = "Reddit_%s.json" % page
		with open(filename, 'w') as f:
			f.write('[')
			for item in response.css('div.scrollerItem'):
				title = str(item.css('h2.s15fpu6f-0').xpath('text()').get())
				votes = str(item.css('div._1rZYMD_4xY3gRcSS3p8ODO::text').get())
				comments = str(item.css('span.FHCV02u6Cp2zYL0fhQPsO::text').get())
				author = str(item.css('div.s1qo48hh-0').xpath('a/text()').get())
				json = {
					"title" : title,
					"upVotes": trimNumber(votes),
					"number_comments": trimNumber(comments),
					"author": trimAuthor(author)
				}
				self.log(json)
				f.write(str(json))
				f.write(',\n')
			f.write("{}]")
			self.log("Fechou ficheiro %s" % filename)
