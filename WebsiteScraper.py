from LoblawsScraper import *
from MetroScraper import *
class WebsiteScraper():
	
	def scrape(self):
		scrapeResults = {}
		loblawsScraper = LoblawsScraper() 
		metroScraper = MetroScraper()
		scrapeResults["loblaws"] = loblawsScraper.scrape()
		scrapeResults["metro"] = metroScraper.scrape()
		return scrapeResults

if __name__ == "__main__":
	scraper = WebsiteScraper()
	scrapeResults = scraper.scrape()
	outputFile = open("scraped.json", "w")
	outputFile.write(json.dumps(scrapeResults))
	outputFile.close()
