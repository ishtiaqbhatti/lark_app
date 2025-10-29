import logging
from fastapi import APIRouter, Depends, HTTPException
from data_access.database_manager import DatabaseManager
from backend.pipeline import WorkflowOrchestrator
from services.discovery_service import DiscoveryService
from ..dependencies import get_db, get_orchestrator, get_discovery_service
from ..models import (
    JobResponse,
    DiscoveryRunRequest,
)  # Ensure DiscoveryRunRequest is imported

# --- NEW IMPORTS AND MODELS FOR FRONTEND FEATURES ---
from typing import Dict


# --- END NEW IMPORTS AND MODELS ---

router = APIRouter()
logger = logging.getLogger(__name__)


@router.get("/discovery/available-filters")
async def get_available_filters():
    """
    Returns a curated list of available discovery modes, filters, and sorting options,
    structured to be easily consumable by the frontend.
    """
    base_filters = [
        {
            "name": "search_volume",
            "label": "Search Volume",
            "type": "number",
            "operators": [">", "<", "="],
        },
        {
            "name": "keyword_difficulty",
            "label": "Keyword Difficulty",
            "type": "number",
            "operators": [">", "<", "="],
        },
        {
            "name": "main_intent",
            "label": "Search Intent",
            "type": "select",
            "options": ["informational", "navigational", "commercial", "transactional"],
            "operators": ["="],
        },
        {
            "name": "competition_level",
            "label": "Competition Level",
            "type": "select",
            "options": ["LOW", "MEDIUM", "HIGH"],
            "operators": ["="],
        },
        {"name": "cpc", "label": "CPC", "type": "number", "operators": [">", "<", "="]},
    ]

    base_sorting = [
        {"name": "search_volume", "label": "Search Volume"},
        {"name": "keyword_difficulty", "label": "Keyword Difficulty"},
        {"name": "cpc", "label": "CPC"},
        {"name": "competition", "label": "Competition"},
    ]

    def construct_paths(prefix, items):
        new_items = []
        for item in items:
            new_item = item.copy()
            if "search_volume" in new_item["name"]:
                new_item["name"] = f"{prefix}keyword_info.search_volume"
            elif "keyword_difficulty" in new_item["name"]:
                new_item["name"] = f"{prefix}keyword_properties.keyword_difficulty"
            elif "main_intent" in new_item["name"]:
                new_item["name"] = f"{prefix}search_intent_info.main_intent"
            elif "competition_level" in new_item["name"]:
                new_item["name"] = f"{prefix}keyword_info.competition_level"
            elif "cpc" in new_item["name"]:
                new_item["name"] = f"{prefix}keyword_info.cpc"
            elif "competition" in new_item["name"]:
                new_item["name"] = f"{prefix}keyword_info.competition"
            new_items.append(new_item)
        return new_items

    return [
        {
            "id": "keyword_ideas",
            "name": "Broad Market Research",
            "description": "Get a wide range of keyword ideas related to your topic.",
            "filters": construct_paths("", base_filters),
            "sorting": [{"name": "relevance", "label": "Relevance"}]
            + construct_paths("", base_sorting),
            "defaults": {
                "filters": [
                    {"field": "keyword_info.search_volume", "operator": ">", "value": 500},
                    {"field": "keyword_properties.keyword_difficulty", "operator": "<", "value": 30},
                ],
                "order_by": ["keyword_info.search_volume,desc"],
            },
        },
        {
            "id": "keyword_suggestions",
            "name": "Long-Tail Keywords",
            "description": "Find specific, multi-word keywords that are easier to rank for.",
            "filters": construct_paths("", base_filters),
            "sorting": construct_paths("", base_sorting),
            "defaults": {
                "filters": [
                    {"field": "keyword_info.search_volume", "operator": ">", "value": 100},
                    {"field": "keyword_properties.keyword_difficulty", "operator": "<", "value": 20},
                ],
                "order_by": ["keyword_info.search_volume,desc"],
            },
        },
        {
            "id": "related_keywords",
            "name": "Semantic Keyword Expansion",
            "description": "Find semantically related terms to expand content depth and discover related topics.",
            "filters": construct_paths("keyword_data.", base_filters),
            "sorting": construct_paths("keyword_data.", base_sorting),
            "defaults": {
                "filters": [
                    {"field": "keyword_data.keyword_info.search_volume", "operator": ">", "value": 100},
                ],
                "order_by": ["keyword_data.keyword_info.search_volume,desc"],
            },
        },
        {
            "id": "find_questions",
            "name": "Customer Questions",
            "description": "Find out what questions your customers are asking about your topic.",
            "filters": construct_paths("", base_filters),
            "sorting": construct_paths("", base_sorting),
            "defaults": {
                "filters": [
                    {"field": "keyword_info.search_volume", "operator": ">", "value": 50},
                ],
                "order_by": ["keyword_info.search_volume,desc"],
            },
        },
    ]


@router.post("/clients/{client_id}/discovery-runs-async", response_model=JobResponse)
async def start_discovery_run_async(
    client_id: str,
    request: DiscoveryRunRequest,
    orchestrator: WorkflowOrchestrator = Depends(get_orchestrator),
    discovery_service: DiscoveryService = Depends(get_discovery_service),
):
    if client_id != orchestrator.client_id:
        raise HTTPException(
            status_code=403,
            detail="You do not have permission to access this client's resources.",
        )
    try:
        filters = request.filters
        limit = request.limit or 1000
        discovery_modes = request.discovery_modes
        depth = request.depth

        if not depth:
            if limit <= 500:
                depth = 2
            elif limit <= 2000:
                depth = 3
            else:
                depth = 4

        parameters = {
            "seed_keywords": request.seed_keywords,
            "negative_keywords": request.negative_keywords,
            "discovery_modes": discovery_modes,
            "filters": filters,
            "order_by": request.order_by,
            "filters_override": request.filters_override,
            "limit": limit,
            "depth": depth,
            "discovery_max_pages": request.discovery_max_pages,
            "include_clickstream_data": request.include_clickstream_data,  # NEW
            "closely_variants": request.closely_variants,  # NEW
            "ignore_synonyms": request.ignore_synonyms,  # NEW
        }
        run_id = discovery_service.create_discovery_run(
            client_id=client_id, parameters=parameters
        )

        job_id = orchestrator.run_discovery_and_save(
            run_id,
            request.seed_keywords,
            discovery_modes,
            filters,
            request.order_by,
            request.filters_override,
            limit,
            depth,
            request.ignore_synonyms,
            request.include_clickstream_data,  # NEW
            request.closely_variants,  # NEW
            request.negative_keywords,
            request.discovery_max_pages,
        )
        return {"job_id": job_id, "message": f"Discovery run job {job_id} started."}
    except Exception as e:
        logger.error(
            f"Failed to start discovery run for client {client_id}: {e}", exc_info=True
        )
        raise HTTPException(
            status_code=500, detail=f"Failed to start discovery run: {e}"
        )


@router.get("/clients/{client_id}/discovery-runs")
async def get_discovery_runs(
    client_id: str,
    page: int = 1,
    limit: int = 10,
    db: DatabaseManager = Depends(get_db),
    orchestrator: WorkflowOrchestrator = Depends(get_orchestrator),
):
    if client_id != orchestrator.client_id:
        raise HTTPException(
            status_code=403,
            detail="You do not have permission to access this client's resources.",
        )
    runs, total_count = db.get_all_discovery_runs_paginated(client_id, page, limit)
    if not runs:
        return {"items": [], "total_items": 0, "page": page, "limit": limit}
    return {"items": runs, "total_items": total_count, "page": page, "limit": limit}





@router.post("/discovery-runs/rerun/{run_id}")
async def rerun_discovery_run(
    run_id: int,
    orchestrator: WorkflowOrchestrator = Depends(get_orchestrator),
    db: DatabaseManager = Depends(get_db),  # current_client_id dependency removed here
):
    """
    Initiates a new discovery run using the parameters from a previous run.
    """
    previous_run = db.get_discovery_run_by_id(run_id)
    if not previous_run:
        raise HTTPException(status_code=404, detail="Discovery run not found.")

    # Authorization check within the function (using orchestrator's client_id)
    if (
        previous_run["client_id"] != orchestrator.client_id
    ):  # Use orchestrator's client_id
        raise HTTPException(
            status_code=403, detail="You do not have permission to re-run this job."
        )

    try:
        parameters = previous_run.get("parameters", {})
        seed_keywords = parameters.get("seed_keywords", [])
        filters = parameters.get("filters")
        order_by = parameters.get("order_by")
        filters_override = parameters.get("filters_override", {})
        limit = parameters.get("limit")
        depth = parameters.get("depth")

        if not seed_keywords:
            raise HTTPException(
                status_code=400, detail="No seed keywords found in the original run."
            )

        # Dynamic discovery logic based on limit
        limit = limit or 1000
        discovery_modes = ["keyword_ideas", "keyword_suggestions", "related_keywords"]

        if depth is None:
            if limit <= 500:
                depth = 2
            elif limit <= 2000:
                depth = 3
            else:
                depth = 4

        # Reconstruct parameters for the new run to be created
        new_run_parameters = {
            "seed_keywords": seed_keywords,
            "discovery_modes": discovery_modes,
            "filters": filters,
            "order_by": order_by,
            "filters_override": filters_override,
            "limit": limit,
            "depth": depth,
        }

        new_run_id = orchestrator.db_manager.create_discovery_run(
            client_id=previous_run["client_id"], parameters=new_run_parameters
        )
        job_id = orchestrator.run_discovery_and_save(
            new_run_id,
            seed_keywords,
            discovery_modes,
            filters,
            order_by,
            filters_override,
            limit,
            depth,
        )

        return {
            "job_id": job_id,
            "message": f"Re-run of job {run_id} started as new job {job_id}.",
        }
    except Exception as e:
        logger.error(f"Failed to re-run discovery run {run_id}: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Failed to start re-run: {e}")


@router.get("/discovery-runs/{run_id}/keywords")
async def get_run_keywords(
    run_id: int,
    db: DatabaseManager = Depends(get_db),
    orchestrator: WorkflowOrchestrator = Depends(get_orchestrator),
):
    """
    Retrieves all keywords that were added to the database as part of a specific discovery run.
    """
    run = db.get_discovery_run_by_id(run_id)
    if not run:
        raise HTTPException(status_code=404, detail="Discovery run not found.")
    if (
        run["client_id"] != orchestrator.client_id
    ):  # Use orchestrator's client_id for auth
        raise HTTPException(
            status_code=403,
            detail="You do not have permission to access these keywords.",
        )

    try:
        keywords = db.get_keywords_for_run(run_id)
        return keywords
    except Exception as e:
        logger.error(
            f"Failed to retrieve keywords for run {run_id}: {e}", exc_info=True
        )
        raise HTTPException(status_code=500, detail=f"Failed to retrieve keywords: {e}")


@router.get("/discovery-runs/{run_id}/keywords/{reason}")
async def get_run_keywords_by_reason(
    run_id: int,
    reason: str,
    db: DatabaseManager = Depends(get_db),
    orchestrator: WorkflowOrchestrator = Depends(get_orchestrator),
):
    """
    Retrieves all keywords that were added to the database as part of a specific discovery run
    that were disqualified for a specific reason.
    """
    run = db.get_discovery_run_by_id(run_id)
    if not run:
        raise HTTPException(status_code=404, detail="Discovery run not found.")
    if (
        run["client_id"] != orchestrator.client_id
    ):  # Use orchestrator's client_id for auth
        raise HTTPException(
            status_code=403,
            detail="You do not have permission to access these keywords.",
        )

    try:
        keywords = db.get_keywords_for_run_by_reason(run_id, reason)
        return keywords
    except Exception as e:
        logger.error(
            f"Failed to retrieve keywords for run {run_id} and reason {reason}: {e}",
            exc_info=True,
        )
        raise HTTPException(status_code=500, detail=f"Failed to retrieve keywords: {e}")


@router.get(
    "/discovery-runs/{run_id}/disqualification-reasons", response_model=Dict[str, int]
)
async def get_disqualification_reasons_endpoint(
    run_id: int, discovery_service: DiscoveryService = Depends(get_discovery_service)
):
    """
    Retrieves a summary of disqualification reasons for a specific discovery run.
    """
    logger.info(f"Received request for disqualification reasons for run {run_id}")
    reasons = discovery_service.get_disqualification_reasons(run_id)
    return reasons
