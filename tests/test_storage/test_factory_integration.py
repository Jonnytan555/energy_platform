from scraper.factory import ScraperFactory
from app.storage.agsi_scraper import AgsiScraper


def test_factory_with_agsi_factories(monkeypatch):
    ScraperFactory._registry.clear()

    # register classmethods directly
    ScraperFactory.register("agsi_fetch", AgsiScraper.for_fetch_only)

    # create an instance
    scraper = ScraperFactory.create("agsi_fetch", "EU")

    # we don't call the network here – just assert type / attribute
    assert isinstance(scraper, AgsiScraper)
    assert scraper.request_handler.zone == "EU"
