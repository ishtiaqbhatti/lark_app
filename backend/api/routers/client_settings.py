# api/routers/client_settings.py
# NEW FILE
from fastapi import APIRouter, Depends, HTTPException
from typing import Dict
from data_access.database_manager import DatabaseManager
from ..dependencies import get_db, get_orchestrator
from ..models import ClientSettings  # Assuming a Pydantic model exists
from backend.pipeline import WorkflowOrchestrator

router = APIRouter()


@router.get("/settings/{client_id}", response_model=ClientSettings)
async def get_client_settings_endpoint(
    client_id: str,
    db: DatabaseManager = Depends(get_db),
    orchestrator: WorkflowOrchestrator = Depends(get_orchestrator),
):
    if client_id != orchestrator.client_id:
        raise HTTPException(
            status_code=403,
            detail="You do not have permission to access this client's resources.",
        )
    settings = db.get_client_settings(client_id)
    if not settings:
        raise HTTPException(
            status_code=404, detail="Settings not found for this client."
        )
    return settings


@router.put("/settings/{client_id}", response_model=Dict[str, str])
async def update_client_settings_endpoint(
    client_id: str,
    settings: ClientSettings,
    db: DatabaseManager = Depends(get_db),
    orchestrator: WorkflowOrchestrator = Depends(get_orchestrator),
):
    if client_id != orchestrator.client_id:
        raise HTTPException(
            status_code=403,
            detail="You do not have permission to access this client's resources.",
        )
    try:
        db.update_client_settings(client_id, settings.dict())
        return {"message": "Settings updated successfully."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
