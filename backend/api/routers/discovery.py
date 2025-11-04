import logging
import json # NEW: For filters_json parsing
from fastapi import APIRouter, Depends, HTTPException
from data_access.database_manager import DatabaseManager
from backend.pipeline import WorkflowOrchestrator
from services.discovery_service import DiscoveryService
from ..dependencies import get_db, get_orchestrator, get_discovery_service
from typing import Optional
from ..models import (
    JobResponse,
    DiscoveryRunRequest,
    DiscoveryRunResponse,
)

router = APIRouter()
logger = logging.getLogger(__name__)


@router.get("/clients/{client_id}/discovery-runs", response_model=DiscoveryRunResponse)
async def get_discovery_runs_for_client(
    client_id: str,
    page: int = 1,
    limit: int = 10,
    search_query: Optional[str] = None,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    discovery_service: DiscoveryService = Depends(get_discovery_service),
):
    """Endpoint to get paginated discovery runs for a client with filters."""
    filters = {
        "search_query": search_query,
        "start_date": start_date,
        "end_date": end_date,
    }
    runs, total_count = discovery_service.get_all_discovery_runs_paginated(
        client_id, page, limit, filters
    )
    return {
        "items": runs,
        "total_items": total_count,
        "page": page,
        "limit": limit,
    }


@router.get("/discovery-runs/{run_id}")
async def get_discovery_run_details(
    run_id: int,
    discovery_service: DiscoveryService = Depends(get_discovery_service),
):
    """Endpoint to get detailed information about a single discovery run."""
    run_details = discovery_service.get_discovery_run_details(run_id)
    if not run_details:
        raise HTTPException(status_code=404, detail="Discovery run not found.")
    return run_details


@router.get("/discovery-runs/{run_id}/keywords")
async def get_discovery_run_keywords(
    run_id: int,
    discovery_service: DiscoveryService = Depends(get_discovery_service),
):
    """Endpoint to get all keywords for a specific discovery run."""
    keywords = discovery_service.get_keywords_for_run(run_id)
    return keywords





# NEW: Add an endpoint to expose discovery goals and their default KD/SV for frontend
@router.get("/discovery/goals-and-defaults")
async def get_discovery_goals_and_defaults(
    orchestrator: WorkflowOrchestrator = Depends(get_orchestrator)
):
    """
    Returns the list of available discovery goals and their default SV/KD values
    for frontend pre-filling.
    """
    goals_list = orchestrator.client_cfg.get("discovery_goals", [])
    response_data = []
    for goal_name in goals_list:
        preset = orchestrator.global_cfg_manager.get_goal_preset_config(goal_name)
        response_data.append({
            "name": goal_name,
            "default_sv": preset.get("default_sv"),
            "default_kd": preset.get("default_kd"),
        })
    return response_data


@router.post("/clients/{client_id}/discovery-runs-async", response_model=JobResponse)
async def start_discovery_run_async(
    client_id: str,
    request: DiscoveryRunRequest,
    db: DatabaseManager = Depends(get_db),
    orchestrator: WorkflowOrchestrator = Depends(get_orchestrator),
    discovery_service: DiscoveryService = Depends(get_discovery_service),
):
    if client_id != orchestrator.client_id:
        raise HTTPException(
            status_code=403,
            detail="You do not have permission to access this client's resources.",
        )
    try:
        goal_preset = orchestrator.global_cfg_manager.get_goal_preset_config(request.discovery_goal)
        if not goal_preset:
            raise HTTPException(status_code=400, detail=f"Discovery goal '{request.discovery_goal}' not found in configuration.")

        raw_order_by = goal_preset.get("order_by")
        parsed_order_by = None
        if isinstance(raw_order_by, str) and raw_order_by:
            parsed_order_by = [s.strip() for s in raw_order_by.split('|') if s.strip()]
            if not parsed_order_by:
                parsed_order_by = None
        elif isinstance(raw_order_by, list) and raw_order_by:
            parsed_order_by = raw_order_by

        # Simplified parameters block
        parameters = {
            "seed_keywords": request.seed_keywords,
            "discovery_goal": request.discovery_goal,
            "min_search_volume": request.min_search_volume,
            "max_keyword_difficulty": request.max_keyword_difficulty,
            "discovery_modes": orchestrator.client_cfg.get("discovery_strategies", ["Keyword Ideas"]),
            "filters_override": request.filters_override,
            "limit": request.limit,
            "depth": request.depth,
            "ignore_synonyms": request.ignore_synonyms,
            "include_clickstream_data": request.include_clickstream_data,
            "closely_variants": request.closely_variants,
            "exact_match": request.exact_match,
        }
        run_id = discovery_service.create_discovery_run(client_id=client_id, parameters=parameters)

        job_id = orchestrator.run_discovery_and_save(
            run_id,
            request.seed_keywords,
            parameters["discovery_modes"],
            goal_preset.get("filters"),
            parsed_order_by, # Pass the correctly parsed order_by
            request.filters_override,
            request.limit,
            request.depth,
            request.ignore_synonyms,
            request.include_clickstream_data,
            request.closely_variants,
            request.exact_match,
        )
        return {"job_id": job_id, "message": f"Discovery run job {job_id} started."}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(
            f"Failed to start discovery run for client {client_id}: {e}", exc_info=True
        )
        raise HTTPException(
            status_code=500, detail=f"Failed to start discovery run: {e}"
        )



# Modify rerun_discovery_run (to ensure goal-based parameters are used if present in original run)
@router.post("/discovery-runs/rerun/{run_id}")
async def rerun_discovery_run(
    run_id: int,
    orchestrator: WorkflowOrchestrator = Depends(get_orchestrator),
    db: DatabaseManager = Depends(get_db),
):
    """
    Initiates a new discovery run using the parameters from a previous run.
    """
    previous_run = db.get_discovery_run_by_id(run_id)
    if not previous_run:
        raise HTTPException(status_code=404, detail="Discovery run not found.")

    if previous_run["client_id"] != orchestrator.client_id:
        raise HTTPException(
            status_code=403, detail="You do not have permission to re-run this job."
        )

    try:
        parameters = previous_run.get("parameters", {})
        # If the original run was goal-based, reconstruct its filters and order_by
        discovery_goal = parameters.get("discovery_goal")
        min_search_volume_rerun = parameters.get("min_search_volume") # Get user's original SV
        max_keyword_difficulty_rerun = parameters.get("max_keyword_difficulty") # Get user's original KD

        filters = None
        order_by = None

        if discovery_goal:
            goal_preset = orchestrator.global_cfg_manager.get_goal_preset_config(discovery_goal)
            if not goal_preset:
                logger.error(f"Rerun failed: Discovery goal '{discovery_goal}' from previous run {run_id} not found in current configuration.")
                raise HTTPException(status_code=500, detail=f"Discovery goal '{discovery_goal}' from previous run not found in current configuration. Please update settings.")

            filters = json.loads(json.dumps(goal_preset.get("filters", []))) # Deep copy
            raw_order_by = goal_preset.get("order_by")
            if isinstance(raw_order_by, str) and raw_order_by:
                order_by = [s.strip() for s in raw_order_by.split('|') if s.strip()]
                if not order_by:
                    order_by = None
            elif isinstance(raw_order_by, list) and raw_order_by:
                order_by = raw_order_by
            
            # Apply user overrides from the previous run to the goal's filters
            for i, f_item in enumerate(filters):
                if f_item["field"] == "keyword_info.search_volume" and min_search_volume_rerun is not None:
                    filters[i]["value"] = min_search_volume_rerun
                elif f_item["field"] == "keyword_properties.keyword_difficulty" and max_keyword_difficulty_rerun is not None:
                    filters[i]["value"] = max_keyword_difficulty_rerun
        else:
            # Fallback to direct filters/order_by if not goal-based (legacy runs)
            filters = parameters.get("filters")
            raw_order_by = parameters.get("order_by")
            if isinstance(raw_order_by, str) and raw_order_by:
                order_by = [s.strip() for s in raw_order_by.split('|') if s.strip()]
                if not order_by:
                    order_by = None
            elif isinstance(raw_order_by, list) and raw_order_by:
                order_by = raw_order_by
        
        new_run_parameters = {
            "seed_keywords": seed_keywords,
            "discovery_goal": discovery_goal, # Preserve goal if existed
            "min_search_volume": min_search_volume_rerun, # Preserve user SV
            "max_keyword_difficulty": max_keyword_difficulty_rerun, # Preserve user KD
            "discovery_modes": discovery_modes,
            "filters": goal_preset.get("filters"), # Pass the raw goal filters
            "order_by": goal_preset.get("order_by"), # Pass the raw goal order_by
            "filters_override": filters_override,
            "limit": limit,
            "depth": depth,
            "ignore_synonyms": ignore_synonyms,
            "include_clickstream_data": include_clickstream_data,
            "closely_variants": closely_variants,
            "exact_match": exact_match,
        }

        new_run_id = orchestrator.db_manager.create_discovery_run(
            client_id=previous_run["client_id"], parameters=new_run_parameters
        )
        job_id = orchestrator.run_discovery_and_save(
            new_run_id,
            seed_keywords,
            discovery_modes,
            goal_preset.get("filters"), # Pass the raw goal filters
            goal_preset.get("order_by"), # Pass the raw goal order_by
            filters_override,
            limit,
            depth,
            ignore_synonyms=ignore_synonyms,
            include_clickstream_data=include_clickstream_data,
            closely_variants=closely_variants,
            exact_match=exact_match,
        )

        return {
            "job_id": job_id,
            "message": f"Re-run of job {run_id} started as new job {job_id}.",
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to re-run discovery run {run_id}: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Failed to start re-run: {e}")
