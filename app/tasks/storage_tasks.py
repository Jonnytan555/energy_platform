from __future__ import annotations

import asyncio
import inspect
from app.celery_app import celery_app


def _run_maybe_async(func, *args, **kwargs):
    """
    Run either a sync function or an async function and return its result.
    Works in a normal Celery sync worker process.
    """
    result = func(*args, **kwargs)
    if inspect.isawaitable(result):
        return asyncio.run(result)
    return result


@celery_app.task(name="tasks.scrape_agsi")
def scrape_agsi_task(zone: str = "eu", pages: int | None = None) -> dict:
    from scraper.factory.scraper_factory import ScraperFactory

    scraper = ScraperFactory.create("agsi_scrape", zone)

    if hasattr(scraper, "scrape"):
        df = _run_maybe_async(scraper.scrape, pages_to_fetch=pages)
    else:
        df = _run_maybe_async(scraper.run, pages_to_fetch=pages) if hasattr(scraper, "run") else None

    rows_persisted = len(df) if df is not None else 0

    return {
        "task": "agsi",
        "zone": zone,
        "pages": pages,
        "has_changes": rows_persisted > 0,
        "rows_persisted": rows_persisted,
    }


@celery_app.task(name="tasks.scrape_alsi")
def scrape_alsi_task(country: str = "EU", pages: int | None = None) -> dict:
    from scraper.factory.scraper_factory import ScraperFactory

    scraper = ScraperFactory.create("alsi_scrape", country)

    if pages is not None and hasattr(scraper, "run"):
        df = _run_maybe_async(scraper.run, pages_to_fetch=pages)
    else:
        df = _run_maybe_async(scraper.run) if hasattr(scraper, "run") else None

    rows_persisted = len(df) if df is not None else 0

    return {
        "task": "alsi",
        "country": country,
        "pages": pages,
        "has_changes": rows_persisted > 0,
        "rows_persisted": rows_persisted,
    }
