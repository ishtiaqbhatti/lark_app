# jobs.py
import threading
import time
import uuid
import logging
from typing import Dict, Any, Callable, Optional
from datetime import datetime
from backend.data_access import queries

# Import DatabaseManager
from backend.data_access.database_manager import DatabaseManager

logger = logging.getLogger(__name__)


class JobManager:
    """Manages asynchronous jobs, their status, and results, backed by a database."""

    # MODIFIED: __init__ now requires a db_manager
    def __init__(self, db_manager: DatabaseManager):
        self.db_manager = db_manager
        self.db_manager.fail_stale_jobs()
        # The in-memory job store and lock are no longer needed.
        # self.jobs: Dict[str, Dict[str, Any]] = {}
        # self.lock = threading.Lock()

    def create_job(
        self, client_id: str, target_function: Callable, args: tuple = (), kwargs: dict = {}, opportunity_id: Optional[int] = None
    ) -> str:
        """
        Creates a new job, saves its initial state, optionally links it to an opportunity,
        starts it in a thread, and returns its ID.
        """
        job_id = str(uuid.uuid4())
        job_info = {
            "id": job_id,
            "client_id": client_id,
            "status": "pending",
            "progress": 0,
            "result": None,
            "error": None,
            "started_at": time.time(),
            "finished_at": None,
            "function_name": target_function.__name__,
        }

        self.db_manager.update_job(job_info)

        # If an opportunity_id is provided, link it in the database
        if opportunity_id:
            self.db_manager.update_opportunity_latest_job_id(opportunity_id, job_id)

        logger.info(f"Job {job_id} created for client {client_id} and function {target_function.__name__}")
        thread = threading.Thread(
            target=self._run_job, args=(job_id, target_function, args, kwargs)
        )
        thread.daemon = True
        thread.start()
        return job_id

    def update_job_progress(self, job_id: str, step: str, message: str, status: Optional[str] = None):
        """Appends a progress log to the job record in the database."""
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "step": step,
            "message": message,
        }
        
        # This operation needs to be atomic to prevent race conditions.
        # We'll fetch the current job, update the log, and save it back.
        # A more advanced setup might use a database transaction or a JSON_APPEND function.
        job_info = self.get_job_status(job_id)
        if job_info:
            progress_log = job_info.get("progress_log", [])
            if isinstance(progress_log, str): # Handle case where it might be a JSON string
                try:
                    progress_log = json.loads(progress_log)
                except json.JSONDecodeError:
                    progress_log = []
            
            progress_log.append(log_entry)
            job_info["progress_log"] = progress_log

            # Optionally update the overall job status at the same time
            if status:
                job_info["status"] = status

            self.db_manager.update_job(job_info)

    def _run_job(
        self, job_id: str, target_function: Callable, args: tuple, kwargs: dict
    ):
        """Internal method to execute the target function and update job status in the DB."""
        logger.info(f"Job {job_id} starting. DB manager: {self.db_manager}")
        try:
            # Initialize the progress log
            self.update_job_status(job_id, "running", progress=5)
            self.update_job_progress(job_id, "Job Started", "The workflow is initializing.")
            
            result = target_function(job_id, *args, **kwargs)
            
            self.update_job_progress(job_id, "Job Finished", "The workflow completed successfully.")
            self.update_job_status(job_id, "completed", progress=100, result=result)
            logger.info(f"Job {job_id} completed successfully.")
        except Exception as e:
            error_message = f"Job {job_id} failed: {e}"
            logger.error(error_message, exc_info=True)
            self.update_job_progress(job_id, "Job Failed", str(e))
            self.update_job_status(job_id, "failed", progress=100, error=str(e))


    def get_job_status(self, job_id: str) -> Optional[Dict[str, Any]]:
        """Retrieves the current status of a job from the database."""
        # MODIFIED: Fetch from DB
        return self.db_manager.get_job(job_id)

    def update_job_status(
        self,
        job_id: str,
        status: str,
        progress: int,
        result: Optional[Dict[str, Any]] = None,
        error: Optional[str] = None,
    ):
        """
        Updates job status using a direct UPDATE query (W10 FIX).
        """
        conn = self.db_manager._get_conn()
        finished_at = (
            datetime.now().timestamp() if status in ["completed", "failed"] else None
        )

        if result or error:
            # If result/error is present, use the original UPDATE_JOB (INSERT OR REPLACE)
            # that handles all fields.
            job_info = self.db_manager.get_job(job_id)
            if job_info:
                job_info["status"] = status
                job_info["progress"] = progress
                job_info["result"] = result
                job_info["error"] = error
                job_info["finished_at"] = finished_at
                self.db_manager.update_job(job_info)
        else:
            # Execute the direct, optimized status/progress update
            # This avoids fetching the entire job record first. (W10 FIX)
            with conn:
                conn.execute(
                    queries.UPDATE_JOB_STATUS_DIRECT,
                    (status, progress, finished_at, job_id),
                )

    # Global job manager instance is no longer initialized here.
    # It will be initialized in api/main.py where it has access to the db_manager.
    # job_manager = JobManager()

    def cancel_job(self, job_id: str) -> bool:
        """Marks a job as 'failed' with a 'cancelled by user' message."""
        job_info = self.get_job_status(job_id)
        if job_info and job_info["status"] in ["pending", "running", "paused"]:
            # The crucial part: mark as failed in the DB so the running thread sees it
            self.update_job_status(
                job_id,
                "failed",
                job_info.get("progress", 0),
                error="Cancelled by user.",
            )
            logger.info(f"Job {job_id} was marked as 'failed' (cancelled by user).")
            return True
        return False
