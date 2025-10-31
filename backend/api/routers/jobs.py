# api/routers/jobs.py

import logging
from fastapi import APIRouter, Depends, HTTPException
from jobs import JobManager
from ..dependencies import get_job_manager, get_db, get_orchestrator
from ..models import JobResponse
from data_access.database_manager import DatabaseManager
from backend.pipeline import WorkflowOrchestrator
from typing import List, Dict, Any

router = APIRouter()
logger = logging.getLogger(__name__)


@router.get("/jobs/active", response_model=List[Dict[str, Any]])
async def get_active_jobs_for_client(
    db: DatabaseManager = Depends(get_db),
    orchestrator: WorkflowOrchestrator = Depends(get_orchestrator),
):
    """Retrieves all 'running' or 'pending' jobs for the current client."""
    try:
        client_id = orchestrator.client_id
        active_jobs = db.get_active_jobs_by_client(client_id)
        return active_jobs
    except Exception as e:
        logger.error(f"Failed to retrieve active jobs for client {orchestrator.client_id}: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Failed to retrieve active jobs.")

@router.get("/jobs/{job_id}", response_model=JobResponse)
async def get_job_status(
    job_id: str, job_manager: JobManager = Depends(get_job_manager)
):
    """
    Retrieves the status of a background job.
    """
    logger.info(f"Received request for job status for job_id: {job_id}")
    job = job_manager.get_job_status(job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")

    return {
        "job_id": job["id"],
        "message": f"Status: {job['status']}",
        "status": job["status"],
        "progress": job["progress"],
        "result": job.get("result"),
        "error": job.get("error"),
        "progress_log": job.get("progress_log"),
    }
