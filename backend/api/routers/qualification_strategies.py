# api/routers/qualification_strategies.py

import logging
from fastapi import APIRouter, Depends, HTTPException
from typing import Dict, Any, List
from data_access.database_manager import DatabaseManager
from ..dependencies import get_db, get_orchestrator
from backend.pipeline import WorkflowOrchestrator

router = APIRouter()
logger = logging.getLogger(__name__)


@router.get(
    "/clients/{client_id}/qualification-strategies", response_model=List[Dict[str, Any]]
)
async def get_qualification_strategies_endpoint(
    client_id: str,
    db: DatabaseManager = Depends(get_db),
    orchestrator: WorkflowOrchestrator = Depends(get_orchestrator),
):
    """
    Retrieves all qualification strategies for a specific client.
    """
    logger.info(f"Received request for qualification strategies for client {client_id}")
    if client_id != orchestrator.client_id:
        raise HTTPException(
            status_code=403,
            detail="You do not have permission to access this client's resources.",
        )
    strategies = db.get_qualification_strategies(client_id)
    return strategies


@router.post(
    "/clients/{client_id}/qualification-strategies", response_model=Dict[str, Any]
)
async def create_qualification_strategy_endpoint(
    client_id: str,
    strategy: Dict[str, Any],
    db: DatabaseManager = Depends(get_db),
    orchestrator: WorkflowOrchestrator = Depends(get_orchestrator),
):
    """
    Creates a new qualification strategy for a specific client.
    """
    logger.info(
        f"Received request to create qualification strategy for client {client_id}"
    )
    if client_id != orchestrator.client_id:
        raise HTTPException(
            status_code=403,
            detail="You do not have permission to access this client's resources.",
        )
    strategy_id = db.create_qualification_strategy(client_id, strategy)
    return {"id": strategy_id}


@router.put("/qualification-strategies/{strategy_id}", response_model=Dict[str, str])
async def update_qualification_strategy_endpoint(
    strategy_id: int,
    strategy: Dict[str, Any],
    db: DatabaseManager = Depends(get_db),
    orchestrator: WorkflowOrchestrator = Depends(get_orchestrator),
):
    """
    Updates a qualification strategy.
    """
    logger.info(f"Received request to update qualification strategy {strategy_id}")
    # Auth check
    strat_to_update = db.get_qualification_strategy_by_id(strategy_id)
    if not strat_to_update:
        raise HTTPException(status_code=404, detail="Strategy not found.")
    if strat_to_update["client_id"] != orchestrator.client_id:
        raise HTTPException(
            status_code=403,
            detail="You do not have permission to modify this resource.",
        )

    db.update_qualification_strategy(strategy_id, strategy)
    return {"message": "Qualification strategy updated successfully."}


@router.delete("/qualification-strategies/{strategy_id}", response_model=Dict[str, str])
async def delete_qualification_strategy_endpoint(
    strategy_id: int,
    db: DatabaseManager = Depends(get_db),
    orchestrator: WorkflowOrchestrator = Depends(get_orchestrator),
):
    """
    Deletes a qualification strategy.
    """
    logger.info(f"Received request to delete qualification strategy {strategy_id}")
    # Auth check
    strat_to_delete = db.get_qualification_strategy_by_id(strategy_id)
    if not strat_to_delete:
        raise HTTPException(status_code=404, detail="Strategy not found.")
    if strat_to_delete["client_id"] != orchestrator.client_id:
        raise HTTPException(
            status_code=403,
            detail="You do not have permission to delete this resource.",
        )

    db.delete_qualification_strategy(strategy_id)
    return {"message": "Qualification strategy deleted successfully."}
