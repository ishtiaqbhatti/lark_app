# api/routers/qualification_settings.py

import logging
from fastapi import APIRouter, Depends, HTTPException
from typing import Dict, Any
from data_access.database_manager import DatabaseManager
from ..dependencies import get_db, get_orchestrator
from backend.pipeline import WorkflowOrchestrator

router = APIRouter()
logger = logging.getLogger(__name__)


@router.get(
    "/clients/{client_id}/qualification-settings", response_model=Dict[str, Any]
)
async def get_qualification_settings_endpoint(
    client_id: str,
    db: DatabaseManager = Depends(get_db),
    orchestrator: WorkflowOrchestrator = Depends(get_orchestrator),
):
    """
    Retrieves the qualification settings for a specific client.
    """
    logger.info(f"Received request for qualification settings for client {client_id}")
    if client_id != orchestrator.client_id:
        raise HTTPException(
            status_code=403,
            detail="You do not have permission to access this client's resources.",
        )
    settings = db.get_qualification_settings(client_id)
    if not settings:
        raise HTTPException(status_code=404, detail="Qualification settings not found")
    return settings


@router.put(
    "/clients/{client_id}/qualification-settings", response_model=Dict[str, Any]
)
async def update_qualification_settings_endpoint(
    client_id: str,
    settings: Dict[str, Any],
    db: DatabaseManager = Depends(get_db),
    orchestrator: WorkflowOrchestrator = Depends(get_orchestrator),
):
    """
    Updates the qualification settings for a specific client.
    """
    logger.info(
        f"Received request to update qualification settings for client {client_id}"
    )
    if client_id != orchestrator.client_id:
        raise HTTPException(
            status_code=403,
            detail="You do not have permission to access this client's resources.",
        )
    db.update_qualification_settings(client_id, settings)
    return {"message": "Qualification settings updated successfully."}
