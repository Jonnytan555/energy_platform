import pandas as pd

from app.config import settings

from scraper.scraper import Scraper
from scraper.persistence.postgres_persistence_handler import PostgresPersistenceHandler
from scraper.persistence.noop_persistence_handler import NoOpPersistenceHandler
from scraper.persistence.persistence_handler import PersistenceHandler

from app.storage.alsi_request_handler import AlsiRequestHandler
from app.storage.alsi_response_handler import AlsiResponseHandler


class AlsiScraper:
    """
    High-level ALSI scraper wrapper.

    Provides:
        • fetch_only() — API fetch + transform (NO persistence)
        • scrape() — API fetch + transform + Postgres SCD2 persistence

    Under the hood uses the generic Scraper pipeline from common-scraper.
    """

    def __init__(self, country: str = "EU", persistence_handler: PersistenceHandler | None = None):
        self.country = country

        # If no persistence is supplied → default to Postgres
        self.persistence_handler = persistence_handler or PostgresPersistenceHandler(
            db_host=settings.DATABASE_HOSTNAME,
            db_name=settings.DATABASE_NAME,
            user=settings.DATABASE_USER,
            password=settings.DATABASE_PASSWORD,
            port=settings.DATABASE_PORT,
            schema="public",
            table_name="alsi_timeseries",
            keys=["date"],
            columns_to_compare=[
                "lng_storage_gwh",
                "sendOut",
                "dtmi_gwh",
                "dtrs",
                "contractedCapacity",
                "availableCapacity",
            ],
            version_column="version",
            latest_column="is_latest",
        )

        # Build Scraper pipeline
        self._scraper = Scraper(
            request_handler=AlsiRequestHandler(country=self.country),
            response_handler=AlsiResponseHandler(),
            persistence_handler=self.persistence_handler,
        )

    # ----------------------------------------------------------------------
    # FACTORY METHODS (used by ScraperFactory)
    # ----------------------------------------------------------------------

    @classmethod
    def for_fetch_only(cls, country: str = "EU") -> "AlsiScraper":
        """
        Returns a scraper that does NOT persist — only fetch + transform.
        """
        return cls(
            country=country,
            persistence_handler=NoOpPersistenceHandler(),
        )

    @classmethod
    def for_persistence(cls, country: str = "EU") -> "AlsiScraper":
        """
        Returns a scraper that performs Postgres persistence (SCD-2).
        """
        return cls(country=country)

    # ----------------------------------------------------------------------
    # API METHODS CALLED BY ROUTERS
    # ----------------------------------------------------------------------

    def run(self, dropNa: bool = True) -> pd.DataFrame:
        """
        Entry point for both fetch_only and persistence modes.

        Scraper.scrape()
            • runs RequestHandler.handle()
            • runs ResponseHandler.handle()
            • runs PersistenceHandler.handle() (NoOp or Postgres)
        """
        return self._scraper.scrape(
            dropNa=dropNa,
            dtype=None,
            created_date_column="created_date",
        )
