# api/routers/settings.py
import logging
from fastapi import APIRouter, Depends, HTTPException
from typing import Dict, Any
from data_access.database_manager import DatabaseManager
from ..dependencies import get_db, get_orchestrator
from backend.pipeline import WorkflowOrchestrator

router = APIRouter()
logger = logging.getLogger(__name__)

@router.get("/settings/{client_id}", response_model=Dict[str, Any])
async def get_settings_endpoint(
    client_id: str,
    db: DatabaseManager = Depends(get_db),
    orchestrator: WorkflowOrchestrator = Depends(get_orchestrator),
):
    """Endpoint for fetching all client-specific settings."""
    if client_id != orchestrator.client_id:
        raise HTTPException(
            status_code=403,
            detail="You do not have permission to access this client's resources.",
        )
    try:
        settings = db.get_client_settings(client_id)
        if not settings:
            raise HTTPException(status_code=404, detail="Settings not found for this client.")
        return settings
    except Exception as e:
        logger.error(f"Failed to retrieve settings for client {client_id}: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Failed to retrieve settings.")

@router.put("/settings/{client_id}", response_model=Dict[str, str])
async def update_settings_endpoint(
    client_id: str,
    settings: Dict[str, Any],
    db: DatabaseManager = Depends(get_db),
    orchestrator: WorkflowOrchestrator = Depends(get_orchestrator),
):
    """Endpoint for updating client-specific settings."""
    if client_id != orchestrator.client_id:
        raise HTTPException(
            status_code=403,
            detail="You do not have permission to access this client's resources.",
        )
    try:
        db.update_client_settings(client_id, settings)
        return {"message": "Settings updated successfully."}
    except Exception as e:
        logger.error(f"Failed to update settings for client {client_id}: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Failed to update settings.")
