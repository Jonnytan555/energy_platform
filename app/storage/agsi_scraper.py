# app/storage/agsi_scraper.py

from __future__ import annotations

import pandas as pd

from app.config import settings

from scraper.scraper import Scraper
from scraper.persistence.postgres_persistence_handler import PostgresPersistenceHandler
from scraper.persistence.noop_persistence_handler import NoOpPersistenceHandler

from app.storage.agsi_request_handler import AgsiRequestHandler
from app.storage.agsi_response_handler import AgsiResponseHandler


class AgsiScraper:
    """
    High-level AGSI scraper – mirrors ALSI architecture.

    Two main usages via factories:
      - AgsiScraper.for_fetch_only(zone) → API → transform → return DataFrame
      - AgsiScraper.for_persistence(zone) → API → transform → SCD2 persist → return persisted rows
    """

    def __init__(
        self,
        zone: str,
        *,
        persistence_handler=None,
        allow_fallback: bool = True,
    ) -> None:
        # normalise zone a bit so you can pass "EU" / "eu"
        self.zone = zone.lower()
        self.allow_fallback = allow_fallback

        # ---------- Request / Response handlers ----------
        request = AgsiRequestHandler(
            zone=self.zone,
            allow_fallback=self.allow_fallback,
        )
        response = AgsiResponseHandler()

        # ---------- Persistence handler ----------
        self.persistence_handler = persistence_handler or PostgresPersistenceHandler(
            db_host=settings.DATABASE_HOSTNAME,
            db_name=settings.DATABASE_NAME,
            user=settings.DATABASE_USER,
            password=settings.DATABASE_PASSWORD,
            port=settings.DATABASE_PORT,
            schema="public",
            table_name="agsi_timeseries",
            # primary-key(s) for SCD2 comparison
            keys=["date"],  # ensure AgsiResponseHandler produces a 'date' column
            columns_to_compare=[
                "gas_in_storage_gwh",
                "injection",
                "withdrawal",
                "working_gas_gwh",
                "full_pct",
                "trend",
            ],
            version_column="version",
            latest_column="is_latest",
        )

        # ---------- Generic scraper pipeline ----------
        self._scraper = Scraper(
            request_handler=request,
            response_handler=response,
            persistence_handler=self.persistence_handler,
        )

    # ------------------------------------------------------------------
    # FACTORY HELPERS
    # ------------------------------------------------------------------

    @classmethod
    def for_fetch_only(cls, zone: str) -> "AgsiScraper":
        """
        Factory for an AGSI scraper that does NOT persist to Postgres.
        Good for FastAPI endpoints / ad-hoc calls.
        """
        return cls(
            zone=zone,
            persistence_handler=NoOpPersistenceHandler(),
            # For API clients it's usually better to bubble errors
            allow_fallback=False,
        )

    @classmethod
    def for_persistence(cls, zone: str) -> "AgsiScraper":
        """
        Factory for an AGSI scraper configured for Postgres SCD2 persistence.
        Here we also *do not* fallback silently – if AGSI is broken,
        we want the job to fail loudly.
        """
        return cls(
            zone=zone,
            persistence_handler=None,  # will default to PostgresPersistenceHandler
            allow_fallback=False,
        )

    # ------------------------------------------------------------------
    # PUBLIC API USED BY FASTAPI / JOBS
    # ------------------------------------------------------------------

    async def fetch_only(self, pages_to_fetch: int | None = None) -> pd.DataFrame:
        """
        Async fetch + transform only.

        pages_to_fetch:
            - None → fetch all pages
            - N    → fetch only the latest N pages
        """
        raw = await self._scraper.request_handler.handle_async(
            pages_to_fetch=pages_to_fetch
        )
        return self._scraper.response_handler.handle(raw)

    async def scrape(self, pages_to_fetch: int | None = None) -> pd.DataFrame:
        """
        Async full ETL: fetch → transform → persist.
        """
        raw = await self._scraper.request_handler.handle_async(
            pages_to_fetch=pages_to_fetch
        )
        df = self._scraper.response_handler.handle(raw)

        return self._scraper.persistence_handler.handle(
            df,
            dropNa=True,
            dtype=None,
            created_date_column="created_date",
        )
