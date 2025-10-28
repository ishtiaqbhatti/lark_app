import logging
from pydantic import BaseModel
from typing import List
from fastapi import APIRouter, Depends, HTTPException
from data_access.database_manager import DatabaseManager
from ..dependencies import get_db, get_orchestrator
from .. import globals as api_globals
from backend.pipeline import WorkflowOrchestrator


class NewClientRequest(BaseModel):
    client_id: str
    client_name: str


router = APIRouter(prefix="/clients", tags=["clients"])
logger = logging.getLogger(__name__)


@router.get("/")
async def get_all_clients(db: DatabaseManager = Depends(get_db)):
    logger.info("Received request for /clients")
    clients = db.get_clients()
    logger.info(f"Found clients: {clients}")
    if not clients:
        return []
    return clients


@router.get("/{client_id}/settings")
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
            status_code=404, detail=f"Settings not found for client '{client_id}'"
        )
    return settings


@router.get("/{client_id}/dashboard-stats")
async def get_dashboard_stats_endpoint(
    client_id: str,
    db: DatabaseManager = Depends(get_db),
    orchestrator: WorkflowOrchestrator = Depends(get_orchestrator),
):
    if client_id != orchestrator.client_id:
        raise HTTPException(
            status_code=403,
            detail="You do not have permission to access this client's resources.",
        )
    stats = db.get_dashboard_stats(client_id)
    if not stats:
        raise HTTPException(
            status_code=404, detail=f"Stats not found for client '{client_id}'"
        )
    return stats


@router.get("/{client_id}/dashboard")
async def get_dashboard_data_endpoint(
    client_id: str,
    db: DatabaseManager = Depends(get_db),
    orchestrator: WorkflowOrchestrator = Depends(get_orchestrator),
):
    """Endpoint to fetch aggregated data for the main dashboard."""
    logger.info(f"Dashboard endpoint called for client: {client_id}")
    if client_id != orchestrator.client_id:
        raise HTTPException(
            status_code=403,
            detail="You do not have permission to access this client's resources.",
        )
    try:
        logger.info("Fetching dashboard data from database...")
        dashboard_data = db.get_dashboard_data(client_id)
        logger.info("Successfully fetched dashboard data.")
        if not dashboard_data:
            logger.warning(f"No dashboard data found for client {client_id}. Returning a default empty structure.")
            # Return a default, empty structure that matches the frontend's expectations
            return {
                "kpis": {
                    "totalOpportunities": 0,
                    "contentGenerated": 0,
                    "totalTrafficValue": 0,
                    "totalApiCost": 0,
                },
                "funnelData": [],
                "actionItems": {"awaitingApproval": [], "failed": []},
                "status_counts": {},
                "recent_items": [],
            }
        logger.info("Returning dashboard data.")
        return dashboard_data
    except Exception as e:
        logger.error(f"Error fetching dashboard data: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Internal Server Error")


@router.get("/{client_id}/processed-keywords")
async def get_processed_keywords_endpoint(
    client_id: str,
    db: DatabaseManager = Depends(get_db),
    orchestrator: WorkflowOrchestrator = Depends(get_orchestrator),
):
    """Retrieves all processed keywords for a client to prevent duplicates."""
    if client_id != orchestrator.client_id:
        raise HTTPException(
            status_code=403,
            detail="You do not have permission to access this client's resources.",
        )
    keywords = db.get_all_processed_keywords_for_client(client_id)
    return keywords


@router.post("/{client_id}/check-keywords")
async def check_existing_keywords_endpoint(
    client_id: str,
    keywords: List[str],
    db: DatabaseManager = Depends(get_db),
    orchestrator: WorkflowOrchestrator = Depends(get_orchestrator),
):
    """Checks a batch of keywords and returns which ones already exist."""
    if client_id != orchestrator.client_id:
        raise HTTPException(
            status_code=403,
            detail="You do not have permission to access this client's resources.",
        )
    existing = db.check_existing_keywords(client_id, keywords)
    return {"existing_keywords": existing}


# ADD the new endpoint to the router:
@router.get("/{client_id}/search-all-assets")
async def search_all_assets_endpoint(
    client_id: str,
    query: str,
    db: DatabaseManager = Depends(get_db),
    orchestrator: WorkflowOrchestrator = Depends(get_orchestrator),
):
    logger.info(
        f"Received search-all-assets request for client {client_id} with query: '{query}'"
    )
    if client_id != orchestrator.client_id:
        raise HTTPException(
            status_code=403,
            detail="You do not have permission to access this client's resources.",
        )
    if len(query) < 3:
        return []

    results = []

    # Search Opportunities
    opportunities = db.search_opportunities(client_id, query)
    for opp in opportunities:
        results.append({"id": opp["id"], "name": opp["keyword"], "type": "opportunity"})

    # Search Discovery Runs (by seed keywords or run status/error)
    discovery_runs = db.search_discovery_runs(client_id, query)
    for run in discovery_runs:
        seed_keywords_str = ", ".join(
            run.get("parameters", {}).get("seed_keywords", [])
        )
        results.append(
            {
                "id": run["id"],
                "name": f"Discovery Run #{run['id']}: {seed_keywords_str[:50]}...",
                "type": "discovery_run",
            }
        )

    # Deduplicate results by type-id if necessary (optional, but good practice)
    unique_results = {}
    for item in results:
        key = f"{item['type']}-{item['id']}"
        if key not in unique_results:
            unique_results[key] = item

    return list(unique_results.values())


@router.get("/{client_id}/opportunities/high-priority")
async def get_high_priority_opportunities_endpoint(
    client_id: str,
    limit: int = 5,
    db: DatabaseManager = Depends(get_db),
    orchestrator: WorkflowOrchestrator = Depends(get_orchestrator),
):
    """Retrieves a short list of the highest-scored, validated opportunities."""
    if client_id != orchestrator.client_id:
        raise HTTPException(
            status_code=403,
            detail="You do not have permission to access this client's resources.",
        )
    opportunities = db.get_high_priority_opportunities(client_id, limit)
    return opportunities


@router.post("/")
async def add_new_client(
    request: NewClientRequest, db: DatabaseManager = Depends(get_db)
):
    """Adds a new client to the database and initializes their settings."""
    try:
        # Ensure the config manager is available
        if not api_globals.config_manager:
            raise HTTPException(
                status_code=500, detail="Configuration manager not initialized."
            )

        default_settings = (
            api_globals.config_manager.get_default_client_settings_template()
        )

        success = db.add_client(
            client_id=request.client_id,
            client_name=request.client_name,
            default_settings=default_settings,
        )

        if success:
            return {"message": "Client added successfully."}
        else:
            # This could happen if the client_id already exists (IntegrityError)
            raise HTTPException(
                status_code=409,
                detail=f"Client with ID '{request.client_id}' already exists.",
            )
    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
        logger.error(
            f"Error adding new client '{request.client_name}': {e}", exc_info=True
        )
        raise HTTPException(status_code=500, detail="Failed to add new client.")
