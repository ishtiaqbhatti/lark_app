import logging
import bleach
import json
from typing import Optional, List, Dict, Any
from fastapi import APIRouter, Depends, HTTPException
from data_access.database_manager import DatabaseManager
from fastapi.concurrency import run_in_threadpool
from services.opportunities_service import OpportunitiesService
from ..dependencies import get_db, get_opportunities_service, get_orchestrator
from ..models import (
    OpportunityListResponse,
    ContentHistoryItem,
    RestoreRequest,
    SocialMediaPostsUpdate,
    ContentUpdatePayload,
)
from pydantic import BaseModel
from .. import globals as api_globals
from backend.pipeline import WorkflowOrchestrator

router = APIRouter()
logger = logging.getLogger(__name__)


@router.get("/settings/discovery-strategies", response_model=List[str])
async def get_discovery_strategies():
    """Returns the available discovery strategies from the global config."""
    strategies = api_globals.config_manager.get_global_config().get(
        "discovery_strategies", []
    )
    return strategies


class ContentFeedbackRequest(BaseModel):
    rating: int
    comments: Optional[str] = None


@router.get(
    "/clients/{client_id}/opportunities/summary", response_model=OpportunityListResponse
)
async def get_all_opportunities_summary_endpoint(
    client_id: str,
    status: Optional[str] = None,
    keyword: Optional[str] = None,
    page: int = 1,
    limit: int = 20,
    sort_by: str = "date_added",
    sort_direction: str = "desc",
    opportunities_service: OpportunitiesService = Depends(get_opportunities_service),
    orchestrator: WorkflowOrchestrator = Depends(get_orchestrator),
):
    """Endpoint for fetching a paginated summary of opportunities for the main table view."""
    if client_id != orchestrator.client_id:
        raise HTTPException(
            status_code=403,
            detail="You do not have permission to access this client's resources.",
        )
    params = {
        "status": status,
        "keyword": keyword,
        "page": page,
        "limit": limit,
        "sort_by": sort_by,
        "sort_direction": sort_direction,
    }
    opportunities, total_count = await run_in_threadpool(
        opportunities_service.get_all_opportunities_summary,
        client_id,
        params,
        select_columns="id, keyword, status, date_added, strategic_score, cpc, competition, main_intent, blog_qualification_status, blog_qualification_reason, latest_job_id, cluster_name, full_data",
    )
    return {
        "items": opportunities,
        "total_items": total_count,
        "page": page,
        "limit": limit,
    }


@router.get(
    "/clients/{client_id}/opportunities/by-cluster",
    response_model=Dict[str, List[Dict[str, Any]]],
)
async def get_opportunities_by_cluster_endpoint(
    client_id: str,
    opportunities_service: OpportunitiesService = Depends(get_opportunities_service),
    orchestrator: WorkflowOrchestrator = Depends(get_orchestrator),
):
    """
    Retrieves all opportunities for a client, grouped by cluster.
    """
    if client_id != orchestrator.client_id:
        raise HTTPException(
            status_code=403,
            detail="You do not have permission to access this client's resources.",
        )
    opportunities_by_cluster = await run_in_threadpool(
        opportunities_service.get_opportunities_by_cluster, client_id
    )
    return opportunities_by_cluster


@router.get("/discovery-runs/{run_id}/clustered-keywords", response_model=Dict[str, List[Dict[str, Any]]])
async def get_clustered_run_keywords(
    run_id: int,
    db: DatabaseManager = Depends(get_db),
    orchestrator: WorkflowOrchestrator = Depends(get_orchestrator),
    opportunities_service: OpportunitiesService = Depends(get_opportunities_service),
):
    """
    Retrieves keywords for a specific discovery run, grouped by their primary category.
    """
    run = db.get_discovery_run_by_id(run_id)
    if not run:
        raise HTTPException(status_code=404, detail="Discovery run not found.")
    if run["client_id"] != orchestrator.client_id:
        raise HTTPException(
            status_code=403,
            detail="You do not have permission to access this run's keywords.",
        )

    try:
        keywords = db.get_keywords_for_run(run_id)
        clustered_keywords = opportunities_service.group_by_category(keywords)
        return clustered_keywords
    except Exception as e:
        logger.error(
            f"Failed to retrieve or cluster keywords for run {run_id}: {e}", exc_info=True
        )
        raise HTTPException(status_code=500, detail=f"Failed to process keywords: {e}")


@router.get("/discovery-runs/{run_id}/grouped-keywords", response_model=Dict[str, List[Dict[str, Any]]])
async def get_grouped_run_keywords(
    run_id: int,
    db: DatabaseManager = Depends(get_db),
    orchestrator: WorkflowOrchestrator = Depends(get_orchestrator),
    opportunities_service: OpportunitiesService = Depends(get_opportunities_service),
):
    """
    Retrieves keywords for a specific discovery run, grouped by their core_keyword.
    """
    run = db.get_discovery_run_by_id(run_id)
    if not run:
        raise HTTPException(status_code=404, detail="Discovery run not found.")
    if run["client_id"] != orchestrator.client_id:
        raise HTTPException(
            status_code=403,
            detail="You do not have permission to access this run's keywords.",
        )

    try:
        keywords = db.get_keywords_for_run(run_id)
        grouped_keywords = opportunities_service.group_by_core_keyword(keywords)
        return grouped_keywords
    except Exception as e:
        logger.error(
            f"Failed to retrieve or group keywords for run {run_id}: {e}", exc_info=True
        )
        raise HTTPException(status_code=500, detail=f"Failed to process keywords: {e}")


@router.put("/opportunities/{opportunity_id}/status", response_model=Dict[str, str])
async def update_opportunity_status_endpoint(
    opportunity_id: int, status: str, db: DatabaseManager = Depends(get_db)
):
    """
    Manually updates the status of an opportunity.
    """
    logger.info(
        f"Received request to update status for opportunity {opportunity_id} to {status}"
    )
    db.update_opportunity_status(opportunity_id, status)
    return {"message": "Opportunity status updated successfully."}


@router.post("/opportunities/bulk-action", response_model=Dict[str, str])
async def bulk_action_endpoint(
    action: str, opportunity_ids: List[int], db: DatabaseManager = Depends(get_db)
):
    """
    Performs a bulk action on a list of opportunities.
    """
    logger.info(
        f"Received request to perform bulk action '{action}' on {len(opportunity_ids)} opportunities"
    )
    for opportunity_id in opportunity_ids:
        if action == "reject":
            db.update_opportunity_status(opportunity_id, "rejected")
        elif action == "approve":
            db.update_opportunity_status(opportunity_id, "qualified")

    return {"message": "Bulk action completed successfully."}


@router.post("/opportunities/compare", response_model=List[Dict[str, Any]])
async def compare_opportunities_endpoint(
    opportunity_ids: List[int], db: DatabaseManager = Depends(get_db)
):
    """
    Retrieves a list of opportunities for comparison.
    """
    logger.info(f"Received request to compare {len(opportunity_ids)} opportunities")
    opportunities = []
    for opportunity_id in opportunity_ids:
        opportunity = db.get_opportunity_by_id(opportunity_id)
        if opportunity:
            opportunities.append(opportunity)

    return opportunities


@router.get(
    "/clients/{client_id}/opportunities/search", response_model=List[Dict[str, Any]]
)
async def search_opportunities_endpoint(
    client_id: str,
    query: str,
    db: DatabaseManager = Depends(get_db),
    orchestrator: WorkflowOrchestrator = Depends(get_orchestrator),
):
    logger.info(f"Received search request for client {client_id} with query: '{query}'")
    if client_id != orchestrator.client_id:
        raise HTTPException(
            status_code=403,
            detail="You do not have permission to access this client's resources.",
        )
    if len(query) < 3:
        return []

    opportunities = db.search_opportunities(client_id, query)
    return opportunities


@router.get("/opportunities/{opportunity_id}", response_model=Dict[str, Any])
async def get_opportunity_by_id_endpoint(
    opportunity_id: int,
    db: DatabaseManager = Depends(get_db),
    orchestrator: WorkflowOrchestrator = Depends(get_orchestrator),  # Add this
):
    logger.info(f"Received request for opportunity {opportunity_id}")
    opportunity = db.get_opportunity_by_id(opportunity_id)
    if not opportunity:
        raise HTTPException(status_code=404, detail="Opportunity not found")
    # Add authorization check
    if opportunity["client_id"] != orchestrator.client_id:
        raise HTTPException(
            status_code=403,
            detail="You do not have permission to access this opportunity.",
        )

    # W23 FIX: Manually parse the blueprint from full_data if it exists
    if opportunity.get("full_data") and isinstance(opportunity["full_data"], str):
        try:
            full_data_json = json.loads(opportunity["full_data"])
            if "blueprint" in full_data_json:
                opportunity["blueprint"] = full_data_json["blueprint"]
            if "serp_overview" in full_data_json:
                opportunity["serp_overview"] = full_data_json["serp_overview"]
        except json.JSONDecodeError:
            logger.warning(
                f"Could not decode full_data JSON for opportunity {opportunity_id}."
            )

    logger.info(f"Retrieved opportunity from DB: {opportunity}")
    return opportunity


@router.get(
    "/opportunities/{opportunity_id}/content-history",
    response_model=List[ContentHistoryItem],
)
async def get_content_history_endpoint(
    opportunity_id: int, db: DatabaseManager = Depends(get_db)
):
    logger.info(f"Fetching content history for opportunity {opportunity_id}")
    history = db.get_content_history(opportunity_id)
    if not history:
        return []
    return history


@router.post(
    "/opportunities/{opportunity_id}/restore-content", response_model=Dict[str, Any]
)
async def restore_content_version_endpoint(
    opportunity_id: int, request: RestoreRequest, db: DatabaseManager = Depends(get_db)
):
    logger.info(
        f"Restoring content version from {request.version_timestamp} for opportunity {opportunity_id}"
    )
    try:
        restored_content = db.restore_content_version(
            opportunity_id, request.version_timestamp
        )
        if restored_content:
            return {
                "message": "Content version restored successfully.",
                "restored_content": restored_content,
            }
        else:
            raise HTTPException(
                status_code=404, detail="Failed to restore content version."
            )
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        logger.error(
            f"Error restoring content for opportunity {opportunity_id}: {e}",
            exc_info=True,
        )
        raise HTTPException(
            status_code=500,
            detail="An internal error occurred during content restoration.",
        )


@router.put(
    "/opportunities/{opportunity_id}/social-media-posts", response_model=Dict[str, str]
)
async def update_social_media_posts_endpoint(
    opportunity_id: int,
    payload: SocialMediaPostsUpdate,
    db: DatabaseManager = Depends(get_db),
    orchestrator: WorkflowOrchestrator = Depends(get_orchestrator),  # Add this
):
    logger.info(f"Updating social media posts for opportunity {opportunity_id}")
    try:
        opportunity = db.get_opportunity_by_id(opportunity_id)
        if not opportunity:
            raise HTTPException(status_code=404, detail="Opportunity not found")
        if opportunity["client_id"] != orchestrator.client_id:
            raise HTTPException(
                status_code=403,
                detail="You do not have permission to access this opportunity.",
            )
        db.update_opportunity_social_posts(opportunity_id, payload.social_media_posts)
        return {"message": "Social media posts updated successfully."}
    except Exception as e:
        logger.error(
            f"Error updating social media posts for opportunity {opportunity_id}: {e}",
            exc_info=True,
        )
        raise HTTPException(
            status_code=500, detail="Failed to update social media posts."
        )


@router.put("/opportunities/{opportunity_id}/content", response_model=Dict[str, str])
async def update_opportunity_content_endpoint(
    opportunity_id: int,
    payload: ContentUpdatePayload,
    db: DatabaseManager = Depends(get_db),
    orchestrator: WorkflowOrchestrator = Depends(get_orchestrator),  # Add this
):
    """Updates the main HTML content of an opportunity's ai_content blob with server-side sanitization."""
    logger.info(f"Received manual content update for opportunity {opportunity_id}")
    from datetime import datetime

    try:
        current_opp = db.get_opportunity_by_id(opportunity_id)
        if not current_opp:
            raise HTTPException(status_code=404, detail="Opportunity not found.")

        if current_opp["client_id"] != orchestrator.client_id:
            raise HTTPException(
                status_code=403,
                detail="You do not have permission to access this opportunity.",
            )

        # 1. SERVER-SIDE SANITIZATION (CRITICAL SECURITY FIX)
        ALLOWED_TAGS = bleach.sanitizer.ALLOWED_TAGS + [
            "h1",
            "h2",
            "h3",
            "h4",
            "h5",
            "h6",
            "p",
            "br",
            "a",
            "i",
            "u",
            "em",
            "strong",
            "blockquote",
            "li",
            "ul",
            "ol",
            "img",
            "div",
            "span",
            "table",
            "thead",
            "tbody",
            "tr",
            "td",
            "th",
            "code",
            "pre",
        ]
        ALLOWED_ATTRIBUTES_SAFE = {
            "*": ["id", "class"],
            "a": ["href", "title"],
            "img": ["src", "alt", "width", "height"],
        }

        clean_html = bleach.clean(
            payload.article_body_html,
            tags=ALLOWED_TAGS,
            attributes=ALLOWED_ATTRIBUTES_SAFE,
        )

        # 2. Save the current version to history before overwriting
        current_ai_content = current_opp.get("ai_content", {})
        if current_ai_content:
            db.save_content_version_to_history(
                opportunity_id,
                current_ai_content,
                timestamp=f"{datetime.now().isoformat()} (Before Manual Edit)",
            )

        # 3. Update the content with the new payload
        updated_ai_content = current_ai_content.copy()
        updated_ai_content["article_body_html"] = clean_html

        # Use the query that also updates status and timestamp
        db.update_opportunity_ai_content_and_status(
            opportunity_id,
            updated_ai_content,
            current_opp.get("ai_content_model"),
            "generated",  # Reset status to 'generated' to reflect it's ready
        )
        return {"message": "Content updated and previous version saved to history."}
    except Exception as e:
        logger.error(
            f"Error updating content for opportunity {opportunity_id}: {e}",
            exc_info=True,
        )
        raise HTTPException(
            status_code=500, detail="Failed to update content due to a server error."
        )


@router.post(
    "/opportunities/{opportunity_id}/override-disqualification",
    response_model=Dict[str, str],
)
async def override_disqualification_endpoint(
    opportunity_id: int, db: DatabaseManager = Depends(get_db)
):
    """Manually overrides a 'failed' or 'rejected' qualification status."""
    success = db.override_disqualification(opportunity_id)
    if not success:
        raise HTTPException(
            status_code=404,
            detail="Opportunity not found or its status did not permit an override.",
        )
    return {
        "message": "Opportunity has been re-qualified and moved to the pending queue."
    }


@router.post("/opportunities/{opportunity_id}/feedback", response_model=Dict[str, str])
async def submit_content_feedback_endpoint(
    opportunity_id: int,
    request: ContentFeedbackRequest,
    db: DatabaseManager = Depends(get_db),
):
    """Submits user feedback for the generated content."""
    if not (1 <= request.rating <= 5):
        raise HTTPException(status_code=400, detail="Rating must be between 1 and 5.")
    try:
        db.save_content_feedback(opportunity_id, request.rating, request.comments)
        return {"message": "Feedback submitted successfully."}
    except Exception as e:
        logger.error(
            f"Error submitting feedback for opportunity {opportunity_id}: {e}",
            exc_info=True,
        )
        raise HTTPException(status_code=500, detail="Failed to submit feedback.")
