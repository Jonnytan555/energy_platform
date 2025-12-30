import asyncio
import logging

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc
from scraper.factory.scraper_factory import ScraperFactory
from app.auth.dependencies import get_current_user
from app.database import get_db
from app.models import AgsiTimeseries, AlsiTimeseries
from app.config import settings

log = logging.getLogger(__name__)

router = APIRouter(prefix="/storage", tags=["Storage"])

# ---------------- AGSI (API fetch + scrape) -----------------

@router.get("/agsi/{zone}/data")
async def get_agsi(
    zone: str,
    pages: int | None = Query(None, ge=1),
    current_user=Depends(get_current_user),
):
    scraper = ScraperFactory.create("agsi_fetch", zone)
    df = await scraper.fetch_only(pages_to_fetch=pages)
    return df.to_dict(orient="records")

@router.post("/agsi/{zone}/scrape")
async def scrape_agsi(
    zone: str,
    pages: int | None = Query(None, ge=1),
    current_user=Depends(get_current_user),
):
    if settings.CELERY_ENABLED:
        from app.tasks.storage_tasks import scrape_agsi_task

        job = scrape_agsi_task.delay(zone=zone, pages=pages)
        log.info("Queued tasks.scrape_agsi task_id=%s zone=%s pages=%s", job.id, zone, pages)
        return {"queued": True, "task_id": job.id}

    scraper = ScraperFactory.create("agsi_scrape", zone)
    df = await scraper.scrape(pages_to_fetch=pages)
    return df.to_dict(orient="records")

# ---------------- AGSI (DB latest-only) -----------------

@router.get("/agsi/{zone}/latest")
async def get_agsi_latest(
    limit: int = Query(365, ge=1, le=5000, description="Max rows to return"),
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user),
):
    """
    Returns ONLY rows where is_latest = true from Postgres, ordered newest first.
    Includes created_date.
    """
    q = (
        select(AgsiTimeseries)
        .where(AgsiTimeseries.is_latest.is_(True))
        .order_by(desc(AgsiTimeseries.date))
        .limit(limit)
    )
    result = await db.execute(q)
    rows = result.scalars().all()

    return [
        {
            "date": r.date.isoformat(),
            "gas_in_storage_gwh": r.gas_in_storage_gwh,
            "injection": r.injection,
            "withdrawal": r.withdrawal,
            "working_gas_gwh": r.working_gas_gwh,
            "full_pct": r.full_pct,
            "trend": r.trend,
            "version": r.version,
            "is_latest": r.is_latest,
            "created_date": r.created_date.isoformat() if r.created_date else None,
        }
        for r in rows
    ]

# ---------------- ALSI (API fetch + scrape) -----------------

@router.get("/alsi")
async def get_alsi(
    country: str = "EU",
    current_user=Depends(get_current_user),
):
    scraper = ScraperFactory.create("alsi_fetch", country)
    df = await asyncio.to_thread(scraper.run)
    return df.to_dict(orient="records")

@router.post("/alsi/scrape")
async def scrape_alsi(
    country: str = "EU",
    current_user=Depends(get_current_user),
):
    if settings.CELERY_ENABLED:
        from app.tasks.storage_tasks import scrape_alsi_task

        job = scrape_alsi_task.delay(country=country)
        log.info("Queued tasks.scrape_alsi task_id=%s country=%s", job.id, country)
        return {"queued": True, "task_id": job.id}

    scraper = ScraperFactory.create("alsi_scrape", country)
    df = await asyncio.to_thread(scraper.run)
    return {"rows_persisted": len(df), "data": df.to_dict(orient="records")}

# ---------------- ALSI (DB latest-only) -----------------

@router.get("/alsi/latest")
async def get_alsi_latest(
    limit: int = Query(365, ge=1, le=5000),
    db: AsyncSession = Depends(get_db),
    current_user=Depends(get_current_user),
):
    q = (
        select(AlsiTimeseries)
        .where(AlsiTimeseries.is_latest.is_(True))
        .order_by(desc(AlsiTimeseries.date))
        .limit(limit)
    )
    result = await db.execute(q)
    rows = result.scalars().all()

    return [
        {
            "date": r.date.isoformat(),
            "lng_storage_gwh": r.lng_storage_gwh,
            "sendOut": r.sendOut,
            "dtmi_gwh": r.dtmi_gwh,
            "dtrs": r.dtrs,
            "contractedCapacity": r.contractedCapacity,
            "availableCapacity": r.availableCapacity,
            "version": r.version,
            "is_latest": r.is_latest,
            "created_date": r.created_date.isoformat() if r.created_date else None,
        }
        for r in rows
    ]
