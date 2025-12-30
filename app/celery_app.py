import os
from celery import Celery
from app.config import settings

BROKER = os.getenv("CELERY_BROKER_URL", "redis://localhost:6379/0")
BACKEND = os.getenv("CELERY_RESULT_BACKEND", "redis://localhost:6379/1")

celery_app = Celery(
    "energy_platform",
    broker=BROKER,
    backend=BACKEND,
    include=["app.tasks.storage_tasks"],  # make it explicit
)

celery_app.conf.update(
    task_serializer="json",
    result_serializer="json",
    accept_content=["json"],
    timezone="UTC",
    enable_utc=True,
)

from app.startup.scraper_registry import register_scrapers
register_scrapers()
