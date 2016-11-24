from lxml import html
import requests
import re
import json

class LoblawsScraper:
	def cleanPrice(self, stringParts):
		if stringParts[2] == '100':
			return float(stringParts[0])
		elif stringParts[2] == 'kg':
			return float(float(stringParts[0])/10)
		elif stringParts[2] == 'lb':
			return float((float(stringParts[0])*2.2/10))
		else:
			print stringParts[2]
			exit()
	def scrape(self):
		urlList = [
			"https://www.loblaws.ca/Food/Fruits-%26-Vegetables/Fruit/Apples-%26-Pears/plp/LSL001001001001",
			"https://www.loblaws.ca/Food/Fruits-%26-Vegetables/Fruit/Avocado-%26-Tropical/plp/LSL001001001002",
			"https://www.loblaws.ca/Food/Fruits-%26-Vegetables/Fruit/Bananas-%26-Plantains/plp/LSL001001001003",
			"https://www.loblaws.ca/Food/Fruits-%26-Vegetables/Fruit/Berries-%26-Cherries/plp/LSL001001001004",
			"https://www.loblaws.ca/Food/Fruits-%26-Vegetables/Fruit/Grapes/plp/LSL001001001007",
			"https://www.loblaws.ca/Food/Fruits-%26-Vegetables/Fruit/Lemons-%26-Limes/plp/LSL001001001005",
			"https://www.loblaws.ca/Food/Fruits-%26-Vegetables/Fruit/Oranges-%26-Citrus/plp/LSL001001001006",
			"https://www.loblaws.ca/Food/Fruits-%26-Vegetables/Fruit/Peaches%2C-Nectarines-%26-Stone-Fruit/plp/LSL001001001009",
			"https://www.loblaws.ca/Food/Fruits-%26-Vegetables/Fruit/Watermelons-%26-Melons/plp/LSL001001001008",
			"https://www.loblaws.ca/Food/Fruits-%26-Vegetables/Vegetable/Asparagus%2C-Eggplant-%26-Zucchini/plp/LSL001001002004",
			"https://www.loblaws.ca/Food/Fruits-%26-Vegetables/Vegetable/Broccoli%2C-Cabbages-%26-Cauliflower/plp/LSL001001002003",
			"https://www.loblaws.ca/Food/Fruits-%26-Vegetables/Vegetable/Ginger%2C-Garlic-%26-Sprout/plp/LSL001001002010",
			"https://www.loblaws.ca/Food/Fruits-%26-Vegetables/Vegetable/Mushrooms-%26-Truffles/plp/LSL001001002006",
			"https://www.loblaws.ca/Food/Fruits-%26-Vegetables/Vegetable/Leeks%2C-Cucumbers-%26-Celery/plp/LSL001001002007",
			"https://www.loblaws.ca/Food/Fruits-%26-Vegetables/Vegetable/Lettuce-%26-Leafy-Vegetables/plp/LSL001001002008",
			"https://www.loblaws.ca/Food/Fruits-%26-Vegetables/Vegetable/Peas%2C-Beans-%26-Corn/plp/LSL001001002005",
			"https://www.loblaws.ca/Food/Fruits-%26-Vegetables/Vegetable/Peppers-%26-Tomatoes/plp/LSL001001002009",
			"https://www.loblaws.ca/Food/Fruits-%26-Vegetables/Vegetable/Potato%2C-Onions-%26-Carrots/plp/LSL001001002001",
			"https://www.loblaws.ca/Food/Fruits-%26-Vegetables/Vegetable/Squash-%26-Pumpkins/plp/LSL001001002002",
			"https://www.loblaws.ca/Food/Fruits-%26-Vegetables/Packaged-Salads/plp/LSL001001003000",
			"https://www.loblaws.ca/Food/Fruits-%26-Vegetables/Fresh-Herbs/plp/LSL001001004000"
			]

		returnHash = {}
		for url in urlList:
			try:
				page = requests.get(url, timeout=5)
			except:
				print "Error accsessing Loblaws website"
				return{}
			items = re.findall('Quick View for (.+?).\n', page.content)
			roughPrices = re.findall('EA,(.+?),', page.content)
			if len(roughPrices) == len(items):
				pricesFound = len(roughPrices)
				for i in range(0,pricesFound):
					if len(roughPrices[i]) > 1:
						splitPrice = roughPrices[i][23:].split(' ')	
						if len(splitPrice) > 2:
							returnHash[items[i]] = self.cleanPrice(splitPrice)
		return returnHash
