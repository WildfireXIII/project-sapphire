import sapphire.utility

#from sapphire.scrapers import reuters_v1 as reuters
from sapphire.managers.rss import RSSManager
from sapphire.utility.logging import registerLogger, ConsoleLogger

print("--------------------------------------------------")
print("\tTEST 1 - scraping metadata")
print("--------------------------------------------------")
sapphire.utility.readConfig("config.json")


cl = ConsoleLogger({"[ALL]":{"color":"white"}, "DEBUG":{"color":"yellow"}}, {"RSS Manager":{"color":"brightcyan"}}, True, True)
registerLogger(cl)

rss_man = RSSManager()
articles = rss_man.scrapeSource('reuters')
rss_man.saveMetadata(articles)


#scraper = reuters.RSSScraper()
#scraper.run("worldnews")
print("==================================================")
