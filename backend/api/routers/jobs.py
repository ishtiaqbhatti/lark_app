# api/routers/jobs.py

import logging
from fastapi import APIRouter, Depends, HTTPException
from jobs import JobManager
from ..dependencies import get_job_manager
from ..models import JobResponse

router = APIRouter()
logger = logging.getLogger(__name__)


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
