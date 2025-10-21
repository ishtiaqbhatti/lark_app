# api/dependencies.py
import os
from fastapi import Depends, HTTPException, Security, Request
from fastapi.security import APIKeyHeader
from data_access.database_manager import DatabaseManager
from backend.pipeline import WorkflowOrchestrator
from jobs import JobManager
from services.opportunities_service import OpportunitiesService
from services.discovery_service import DiscoveryService
from . import globals as api_globals


def get_db() -> DatabaseManager:
    """Dependency injector for DatabaseManager."""
    return api_globals.db_manager


def get_opportunities_service(
    db: DatabaseManager = Depends(get_db),
) -> OpportunitiesService:
    """Dependency injector for OpportunitiesService."""
    return OpportunitiesService(db)


def get_discovery_service(db: DatabaseManager = Depends(get_db)) -> DiscoveryService:
    """Dependency injector for DiscoveryService."""
    return DiscoveryService(db)


def get_job_manager() -> JobManager:
    """Dependency injector for JobManager."""
    return api_globals.job_manager


# Replace the entire `get_current_client_id` function with this:
def get_current_client_id(request: Request) -> str:
    """
    Dependency to get the current client_id from the X-Client-ID header.
    In a real multi-tenant application, this would also be validated against user's permissions.
    """
    client_id = request.headers.get("X-Client-ID")
    if not client_id:
        # Fallback to default if header is missing, or raise HTTPException
        # For development, we might fallback. For production, raising is safer.
        # raise HTTPException(status_code=400, detail="X-Client-ID header is required")
        return "Lark_Main_Site"  # Fallback for local dev/testing
    return client_id


# Update the `get_orchestrator` dependency to *not* directly use `get_current_client_id` within its signature
# because it will be passed explicitly to the endpoint if needed.
# Modify `get_orchestrator` signature from `get_orchestrator(client_id: str, ...)` to:
def get_orchestrator(
    request: Request,  # Add Request to get client_id
    db: DatabaseManager = Depends(get_db),
    jm: JobManager = Depends(get_job_manager),
) -> WorkflowOrchestrator:
    """
    Dependency injector for WorkflowOrchestrator.
    Creates a new instance for each request, configured for the specific client_id.
    """
    client_id = request.headers.get("X-Client-ID")  # Get client_id from request headers
    if not client_id:
        # Fallback to default for orchestrator initialization if header is missing
        client_id = "Lark_Main_Site"

    if not db.get_client_settings(client_id):
        raise HTTPException(
            status_code=404, detail=f"Client with ID '{client_id}' not found."
        )

    return WorkflowOrchestrator(api_globals.config_manager, db, client_id, jm)


API_KEY = os.getenv("INTERNAL_API_KEY")
API_KEY_NAME = "X-API-Key"
api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=True)


async def get_api_key(api_key: str = Security(api_key_header)):
    if api_key == API_KEY:
        return api_key
    else:
        raise HTTPException(status_code=403, detail="Could not validate credentials")
