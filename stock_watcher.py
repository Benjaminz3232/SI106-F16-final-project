# Benjamin Zeffer's SI 106 Final Project

######################################################
# Import statements ##################################
######################################################

import urllib2
import requests
import json
import sys
import demjson
import unittest
from pprint import pprint

try:
    from urllib.request import Request, urlopen
except:
    from urllib2 import Request, urlopen

######################################################
# GETTING STOCK DATA #################################
######################################################

try:
	cache_file = open("cache_nums.json", "r")
	cache_contents = cache_file.read()
	CACHE_DICTION = json.loads(cache_contents)
	cache_file.close()
except:
	CACHE_DICTION = {}

class StockData():
    def __init__(self):
        self.base_url = "http://finance.google.com/finance/info?client=ig&q="

    def get_caching(self, symbol, exchange):
    	full_url = self.base_url + "{},{}".format(symbol,exchange)

    	if full_url in CACHE_DICTION:
    		print("STOCK DATA:")
    		print("using cache...\n")

    		response_text = CACHE_DICTION[full_url]

    	else:
    		print("STOCK DATA:")
    		print("fetching...\n")

    		response = requests.get(full_url)
    		CACHE_DICTION[full_url] = response.text
    		response_text = response.text

    		cache_file = open("cache_nums.json", "w")
    		cache_file.write(json.dumps(CACHE_DICTION))
    		cache_file.close()

    	return response_text
    
    def get(self, symbol, exchange):
        content = self.get_caching(symbol, exchange)
        data = json.loads(content[3:])
        x = data[0]
        return x

if __name__ == "__main__":
    s = StockData()

    print("\n")

    exchange = raw_input("Enter an exchange: ")
    stock = raw_input("Enter a stock symbol: ")

    print("\n")

    try:
        quote = s.get(stock,exchange)
    except:
        print("Invalid stock code/exchange")

######################################################
# STOCK DATA CLASSES AND FUNCTIONS ###################
######################################################

class Stock():
	def __init__(self, d):
		self.Exchange = d['e']
		self.StockSymbol = d['t']
		self.ID = d['id']
		self.LastTradePrice = d['l']
		self.Change = d['c']
		self.ChangePercent = d['cp']
		self.LastTradeSize = d['s']
		self.PreviousClosePrice = d['pcls_fix']
		self.LastTradeDateTimeLong = d['lt']

		try:
			self.Dividend = d['div']
			self.Yield = d['yld']
		except:
			pass

		try:
			self.ExtHrsLastTradePrice = d['el']
			self.ExtHrsChange = d['ec']
			self.ExtHrsChangePercent = d['ecp']
			self.ExtHrsLastTradeDateTimeLong = d['elt']
		except:
			pass

	def stockvars_reg(self):
		stocknums = {
			'1                     Exchange' : self.Exchange, 
			'2                  StockSymbol' : self.StockSymbol,
			'3                           ID' : self.ID,
			'4               LastTradePrice' : self.LastTradePrice,
			'5                       Change' : self.Change,
			'6                ChangePercent' : self.ChangePercent,
			'7                LastTradeSize' : self.LastTradeSize,
			'8           PreviousClosePrice' : self.PreviousClosePrice,
			'9        LastTradeDateTimeLong' : self.LastTradeDateTimeLong
		}
		return stocknums

	def stockvars_irreg(self):
		stocknums_irreg = {
			'10                    Dividend' : self.Dividend,
			'11                       Yield' : self.Yield
		}
		return stocknums_irreg

	def stockvars_exthrs(self):
		stocknums_exthrs = {
			'12        ExtHrsLastTradePrice' : self.ExtHrsLastTradePrice,
			'13                ExtHrsChange' : self.ExtHrsChange,
			'14         ExtHrsChangePercent' : self.ExtHrsChangePercent,
			'15 ExtHrsLastTradeDateTimeLong' : self.ExtHrsLastTradeDateTimeLong
		}
		return stocknums_exthrs

def sort_stocknums(obj):
	return json.dumps(obj, sort_keys=True, indent=2)

def printing():
	new_stock = Stock(quote)
	new_stock_dict = new_stock.stockvars_reg()
	print(sort_stocknums(new_stock_dict))

	try:
		new_stock_dict1 = new_stock.stockvars_irreg()
		print(sort_stocknums(new_stock_dict1))
	except:
		pass

	try:
		new_stock_dict2 = new_stock.stockvars_exthrs()
		print(sort_stocknums(new_stock_dict2))
	except:
		pass

printing()

#####################################################
# GETTING NEWS DATA #################################
#####################################################

try:
	cache_news_file = open("cache_news.json", "r")
	cache_news_contents = cache_news_file.read()
	CACHE_NEWS_DICTION = json.loads(cache_news_contents)
	cache_news_file.close()
except:
	CACHE_NEWS_DICTION = {}

def buildNewsUrl(symbol, qs="&start=0&num=3"):
	full_url = "http://www.google.com/finance/company_news?output=json&q=" + symbol + qs
	return full_url

def getNewsCaching():
	full_url = buildNewsUrl(stock)

	if full_url in CACHE_NEWS_DICTION:
		print("using cache...\n\n")

		response_text = CACHE_NEWS_DICTION[full_url]
	else:
		print("fetching...\n\n")

		response = requests.get(full_url)
		CACHE_NEWS_DICTION[full_url] = response.text
		response_text = response.text

		cache_news_file = open("cache_news.json", "w")
		cache_news_file.write(json.dumps(CACHE_NEWS_DICTION))
		cache_news_file.close()

	return response_text

def requestNews(symbol):
	content = getNewsCaching()
	content_json = demjson.decode(content)
	print("Total news about this stock: ", content_json['total_number_of_news'])
	article_json = []
	news_json = content_json['clusters']
	for cluster in news_json:
		for article in cluster:
			if article == 'a':
				article_json.extend(cluster[article])
	
	return article_json

######################################################
# NEWS DATA & STOCK PREDICTOR ##############
######################################################

def sort_newsdata(obj):
	return json.dumps(obj, sort_keys = True, indent=2)

print("\n\nNEWS ARTICLES:")

article = requestNews(stock)
news_words = []

num_articles = len(article)
for x in range(num_articles):
	news_data = {
		'1    Title' : article[x]['t'],
		'2   Source' : article[x]['s'],
		'3  Created' : article[x]['d'],
		'4 Contents' : article[x]['sp']
	}

	for words in news_data.values():
		wrds = words.split()
		for words in wrds:
			news_words.append(words)

	print(sort_newsdata(news_data))

pos_ws = []
f = open('positive-words.txt', 'r')

for l in f.readlines()[35:]:
    pos_ws.append(unicode(l.strip()))
f.close()

neg_ws = []
f = open('negative-words.txt', 'r')
for l in f.readlines()[35:]:
    neg_ws.append(unicode(l.strip()))

emotion_score = 0
for words in news_words:
	if words in pos_ws:
		emotion_score += 1
for words in news_words:
	if words in neg_ws:
		emotion_score += -1

if emotion_score > 0:
	print("\nPREDICTION:  stock will increase\n")
elif emotion_score < 0:
	print("\nPREDICTION:  stock will decrease\n")
else:
	print("\nPREDICTION:  stock will stay the same\n")

######################################################
# TEST CASES #########################################
######################################################

class Stock_Data(unittest.TestCase):
	def test_1(self):
		self.assertEqual(type(quote), type({}))

	def test_2(self):
		self.assertEqual(len(quote), 16) # SHOULD FAIL WHEN THE STOCK MARKET IS CLOSED
	def test_3(self):
		self.assertEqual(len(quote), 27) # SHOULD FAIL WHEN THE STOCK MARKET IS OPEN

	def test_4(self):
		self.assertEqual(quote[u"e"], exchange)
	def test_5(self):
		self.assertEqual(quote[u"t"], stock)

class Stock_News(unittest.TestCase):
	def test_1(self):
		self.assertEqual(type(news_data['1    Title']), type(u""))
	def test_2(self):
		self.assertEqual(type(news_data['2   Source']), type(u""))
	def test_3(self):
		self.assertEqual(type(news_data['3  Created']), type(u""))
	def test_4(self):
		self.assertEqual(type(news_data['4 Contents']), type(u""))

	def test_5(self):
		self.assertEqual(type(article), type([]))

if __name__ == '__main__':
	unittest.main(verbosity=0)