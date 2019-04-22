import scrapy
import re

user = "http://www.reddit.com/user/"

def trimNumber(number):
	number = re.sub(r'\.(\d)k',r'\1 00', number)
	number = re.sub(r'comments',r'', number)
	number = re.sub(r'\s',r'', number)
	return number

def trimAuthor(author):
	author = re.sub(r'\w/',user, author)
	return author

def remExtras(text):
	text = re.sub(r'\t',r'\s', text)
	text = re.sub(r'\[[\s\w]+\]\s?',r'', text)
	text = re.sub(r'\s?\(.+\)\s?',r'', text)
	return text

class Reddit(scrapy.Spider):
	name = "reddit"
	def start_requests(self):
		urls = [
			'https://www.reddit.com/',
			'https://www.reddit.com/r/worldnews/',
			'https://www.reddit.com/r/gameofthrones/',
			'https://www.reddit.com/r/leagueoflegends/',
			'https://www.reddit.com/r/classicwow/',
		]
		for url in urls:
			yield scrapy.Request(url=url, callback=self.parse)

	def parse(self, response):
		page = response.url.split("/")[-2]
		filename = "Reddit_%s.json" % page
		votes_per_page = 0
		comments_per_page = 0
		removables = 0
		with open(filename, 'w') as f:
			f.write('[')
			for item in response.css('div.scrollerItem'):
				title = str(item.css('h2.s15fpu6f-0').xpath('text()').get())
				if re.match(r'\[.+\]', title):
					removables += 1
				if re.match(r'\(.+\)', title):
					removables += 1
				title = remExtras(title)

				votes = str(item.css('div._1rZYMD_4xY3gRcSS3p8ODO::text').get())
				votes = trimNumber(votes)
				if re.match(r'\d+', votes):
					votes_per_page = votes_per_page + int(votes)
				
				comments = str(item.css('span.FHCV02u6Cp2zYL0fhQPsO::text').get())
				comments = trimNumber(comments)
				if re.match(r'\d+', comments):
					comments_per_page = comments_per_page + int(comments)

				author = str(item.css('div.s1qo48hh-0').xpath('a/text()').get())
				json = {
					"title" : title,
					"upVotes": votes,
					"comments": comments,
					"author": trimAuthor(author)
				}
				if not re.match('None', title):
					self.log(json)
					f.write(str(json))
					f.write(',\n')
			f.write('{"votes per page": '+ str(votes_per_page) + ', "Comments per page": '+ str(comments_per_page) +', "Removables": '+str(removables)+'}]')
			self.log("Fechou ficheiro %s" % filename)
