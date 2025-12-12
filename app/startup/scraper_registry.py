from scraper.factory.scraper_factory import ScraperFactory
from app.storage.agsi_scraper import AgsiScraper
from app.storage.alsi_scraper import AlsiScraper

def register_scrapers():
    # AGSI
    ScraperFactory.register("agsi_fetch", AgsiScraper.for_fetch_only)
    ScraperFactory.register("agsi_scrape", AgsiScraper.for_persistence)

    # ALSI
    ScraperFactory.register("alsi_fetch", AlsiScraper.for_fetch_only)
    ScraperFactory.register("alsi_scrape", AlsiScraper.for_persistence)
