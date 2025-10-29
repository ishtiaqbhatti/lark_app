import logging
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import SQLAlchemyError
from data_access.database_manager import DatabaseManager
from backend.pipeline import WorkflowOrchestrator
from services.discovery_service import DiscoveryService
from ..dependencies import get_db, get_orchestrator, get_discovery_service
from ..models import (
    JobResponse,
    DiscoveryRunRequest,
)  # Ensure DiscoveryRunRequest is imported

from utils.exceptions import (
    ValidationException,
    ResourceNotFoundException,
    DataForSEOAPIException,
    RateLimitException,
    BaseAPIException
)
from slowapi import Limiter
from fastapi import Request

limiter = Limiter(key_func=lambda request: request.state.client_id)

# --- END NEW IMPORTS AND MODELS ---

router = APIRouter()
logger = logging.getLogger(__name__)


@router.get("/discovery/available-filters")
async def get_available_filters():
    """
    Returns all available filters for the frontend.
    """
    base_filters = [
        {
            "name": "search_volume",
            "label": "Search Volume",
            "type": "number",
            "operators": [">", "<", "=", ">=", "<="],
        },
        {
            "name": "keyword_difficulty",
            "label": "Keyword Difficulty",
            "type": "number",
            "operators": [">", "<", "=", ">=", "<="],
        },
        {
            "name": "main_intent",
            "label": "Search Intent",
            "type": "select",
            "options": ["informational", "navigational", "commercial", "transactional"],
            "operators": ["=", "in"],
        },
        {
            "name": "competition_level",
            "label": "Competition Level",
            "type": "select",
            "options": ["LOW", "MEDIUM", "HIGH"],
            "operators": ["=", "in"],
        },
        {
            "name": "cpc",
            "label": "CPC (Cost Per Click)",
            "type": "number",
            "operators": [">", "<", "=", ">=", "<="],
        },
        {
            "name": "competition",
            "label": "Competition Score",
            "type": "number",
            "operators": [">", "<", "=", ">=", "<="],
        },
        # ADD THESE:
        {
            "name": "backlinks",
            "label": "Average Backlinks (Top 10)",
            "type": "number",
            "operators": [">", "<", "=", ">=", "<="],
        },
        {
            "name": "referring_domains",
            "label": "Referring Domains (Top 10)",
            "type": "number",
            "operators": [">", "<", "=", ">=", "<="],
        },
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
            base_name = new_item["name"]
            
            # MAP TO CORRECT PATHS:
            if base_name == "search_volume":
                new_item["name"] = f"{prefix}keyword_info.search_volume"
            elif base_name == "keyword_difficulty":
                new_item["name"] = f"{prefix}keyword_properties.keyword_difficulty"
            elif base_name == "main_intent":
                new_item["name"] = f"{prefix}search_intent_info.main_intent"
            elif base_name == "competition_level":
                new_item["name"] = f"{prefix}keyword_info.competition_level"
            elif base_name == "cpc":
                new_item["name"] = f"{prefix}keyword_info.cpc"
            elif base_name == "competition":
                new_item["name"] = f"{prefix}keyword_info.competition"
            elif base_name == "backlinks":
                new_item["name"] = f"{prefix}avg_backlinks_info.backlinks"
            elif base_name == "referring_domains":
                new_item["name"] = f"{prefix}avg_backlinks_info.referring_domains"
            
            new_items.append(new_item)
        return new_items

    return [
        {
            "id": "keyword_ideas",
            "name": "Broad Market Research",
            "description": "Wide range of keyword ideas related to your topic.",
            "filters": construct_paths("", base_filters),
            "sorting": [{"name": "relevance", "label": "Relevance"}]
            + construct_paths("", base_sorting),
            "defaults": {
                "filters": [
                    {"field": "keyword_info.search_volume", "operator": ">=", "value": 500},
                    {"field": "keyword_info.search_volume", "operator": "<=", "value": 50000},
                    {"field": "keyword_properties.keyword_difficulty", "operator": "<=", "value": 40},
                    {"field": "keyword_info.competition_level", "operator": "in", "value": ["LOW", "MEDIUM"]},
                    {"field": "search_intent_info.main_intent", "operator": "=", "value": "informational"},
                    {"field": "avg_backlinks_info.backlinks", "operator": "<=", "value": 100},
                    {"field": "avg_backlinks_info.referring_domains", "operator": "<=", "value": 50},
                    {"field": "keyword_info.cpc", "operator": ">=", "value": 0.30},
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
@limiter.limit("10/minute")  # MAX 10 DISCOVERY RUNS PER MINUTE
async def start_discovery_run_async(
    request: Request,  # ADD THIS
    client_id: str,
    discovery_request: DiscoveryRunRequest,  # RENAMED TO AVOID CONFLICT
    orchestrator: WorkflowOrchestrator = Depends(get_orchestrator),
    discovery_service: DiscoveryService = Depends(get_discovery_service),
):
    request.state.client_id = client_id
    if client_id != orchestrator.client_id:
        raise ValidationException("Permission denied", field="client_id")
    
    try:
        # SANITIZE INPUTS:
        seed_keywords = sanitize_keyword_list(discovery_request.seed_keywords)
        negative_keywords = sanitize_keyword_list(discovery_request.negative_keywords or [])
        
        if discovery_request.filters:
            filters = sanitize_filters(discovery_request.filters)
            validate_regex_filter(filters)
        else:
            filters = None

        if filters and len(filters) > 8:
            raise ValidationException("Maximum 8 filter conditions allowed. Please reduce filters.", field="filters")
        
        # Convert to API format
        api_filters = convert_frontend_filters_to_api_format(filters)

        # NOW INJECT NEGATIVE KEYWORDS CORRECTLY:
        if negative_keywords:
            if api_filters:
                for neg_kw in negative_keywords:
                    api_filters.append('and')
                    api_filters.append(['keyword', 'not_match', neg_kw.strip()])
            else:
                api_filters = []
                for i, neg_kw in enumerate(negative_keywords):
                    api_filters.append(['keyword', 'not_match', neg_kw.strip()])
                    if i < len(negative_keywords) - 1:
                        api_filters.append('and')

        # VALIDATE DISCOVERY MODES
        discovery_modes = discovery_request.discovery_modes
        if not discovery_modes or len(discovery_modes) == 0:
            raise ValidationException("At least one discovery mode must be selected.", field="discovery_modes")
        
        valid_modes = ["keyword_ideas", "keyword_suggestions", "related_keywords"]
        invalid_modes = [m for m in discovery_modes if m not in valid_modes]
        if invalid_modes:
            raise ValidationException(f"Invalid discovery modes: {', '.join(invalid_modes)}. Valid modes are: {', '.join(valid_modes)}", field="discovery_modes")

        # CREATE STRUCTURED FILTERS
        structured_filters = {
            "ideas": api_filters.copy() if api_filters else None,
            "suggestions": api_filters.copy() if api_filters else None,
            "related": None
        }
        
        if api_filters:
            related_filters = []
            for item in api_filters:
                if isinstance(item, list):
                    field = item[0]
                    if not field.startswith('keyword_data.') and field != 'keyword':
                        field = f'keyword_data.{field}'
                    related_filters.append([field, item[1], item[2]])
                else:
                    related_filters.append(item)
            structured_filters["related"] = related_filters

        limit = discovery_request.limit or 1000
        depth = discovery_request.depth
        if not depth:
            depth = 3 if limit <= 2000 else 4

        parameters = {
            "seed_keywords": seed_keywords,
            "negative_keywords": negative_keywords,
            "discovery_modes": discovery_modes,
            "filters": structured_filters,
            "order_by": discovery_request.order_by,
            "disqualification_rules_override": discovery_request.disqualification_rules_override,
            "limit": limit,
            "depth": depth,
            "include_clickstream_data": discovery_request.include_clickstream_data,
            "closely_variants": discovery_request.closely_variants,
            "ignore_synonyms": discovery_request.ignore_synonyms,
        }
        
        try:
            run_id = discovery_service.create_discovery_run(client_id=client_id, parameters=parameters)
            job_id = orchestrator.run_discovery_and_save(
                run_id,
                seed_keywords,
                discovery_modes,
                structured_filters,
                discovery_request.order_by,
                discovery_request.disqualification_rules_override,
                limit,
                depth,
                discovery_request.ignore_synonyms,
                discovery_request.include_clickstream_data,
                discovery_request.closely_variants,
                negative_keywords,
            )
            return {"job_id": job_id, "message": f"Discovery run job {job_id} started."}
        except SQLAlchemyError as db_error:
            logger.error(f"Database error: {db_error}", exc_info=True)
            raise BaseAPIException(status_code=500, detail="Database operation failed.", error_code="DATABASE_ERROR")
    
    except ValidationException:
        raise
    except Exception as e:
        logger.error(f"Unexpected error: {e}", exc_info=True)
        raise BaseAPIException(status_code=500, detail="An unexpected error occurred.", error_code="INTERNAL_SERVER_ERROR")


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


@router.post("/discovery/pre-check", response_model=Dict[str, List[str]])
async def pre_check_keywords_endpoint(
    request: Dict[str, List[str]],
    db: DatabaseManager = Depends(get_db),
    orchestrator: WorkflowOrchestrator = Depends(get_orchestrator),
):
    """
    Checks a list of seed keywords to see if they already exist in the database for the client.
    """
    seed_keywords = request.get("seed_keywords", [])
    if not seed_keywords:
        return {"existing_keywords": []}

    try:
        existing_keywords = db.check_existing_keywords(orchestrator.client_id, seed_keywords)
        return {"existing_keywords": existing_keywords}
    except Exception as e:
        logger.error(f"Failed to pre-check keywords: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Failed to check keywords.")
