from __future__ import annotations
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from celery.result import AsyncResult
from app.celery_app import celery_app
from app.config import settings

router = APIRouter(tags=["tasks"])


class AgsiRequest(BaseModel):
    zone: str = "eu"
    pages: int | None = None


class AlsiRequest(BaseModel):
    country: str = "EU"
    pages: int | None = None


@router.post("/agsi")
def enqueue_agsi(req: AgsiRequest):
    if not settings.CELERY_ENABLED:
        raise HTTPException(status_code=400, detail="CELERY_ENABLED=false")

    # Import here so importing the router doesn't force-import tasks in celery-off mode
    from app.tasks.storage_tasks import scrape_agsi_task

    job = scrape_agsi_task.delay(req.zone, req.pages)
    return {"task_id": job.id}


@router.post("/alsi")
def enqueue_alsi(req: AlsiRequest):
    if not settings.CELERY_ENABLED:
        raise HTTPException(status_code=400, detail="CELERY_ENABLED=false")

    from app.tasks.storage_tasks import scrape_alsi_task

    job = scrape_alsi_task.delay(req.country, req.pages)
    return {"task_id": job.id}


@router.get("/{task_id}")
def task_status(task_id: str):
    res = AsyncResult(task_id, app=celery_app)

    payload = {
        "task_id": task_id,
        "status": res.status,  # PENDING/STARTED/SUCCESS/FAILURE/RETRY
        "ready": res.ready(),
    }
    if res.ready():
        payload["result"] = res.result if res.successful() else str(res.result)

    return payload
