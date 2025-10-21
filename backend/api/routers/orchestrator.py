import logging
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import Optional, Dict, List
from data_access.database_manager import DatabaseManager
from jobs import JobManager
from ..dependencies import get_db, get_job_manager, get_orchestrator
from ..models import (
    JobResponse,
    AnalysisRequest,
    AutoWorkflowRequest,
    RefineContentRequest,
    ApproveAnalysisRequest,
)  # Add ApproveAnalysisRequest
from backend.pipeline import WorkflowOrchestrator

router = APIRouter()
logger = logging.getLogger(__name__)


class GenerationRequest(BaseModel):
    model_override: Optional[str] = None
    temperature: Optional[float] = None


@router.post(
    "/orchestrator/{opportunity_id}/run-generation-async", response_model=JobResponse
)
async def run_generation_async_endpoint(
    opportunity_id: int,
    request: GenerationRequest,
    db: DatabaseManager = Depends(get_db),
    orchestrator: WorkflowOrchestrator = Depends(get_orchestrator),
):
    try:
        opportunity = db.get_opportunity_by_id(opportunity_id)
        if not opportunity:
            raise HTTPException(status_code=404, detail="Opportunity not found.")

        if opportunity["status"] in [
            "running",
            "in_progress",
            "pending",
            "refresh_started",
        ]:
            raise HTTPException(
                status_code=409,
                detail=f"A workflow is already active for this opportunity (Status: {opportunity['status']}).",
            )

        # Add authorization check
        if opportunity["client_id"] != orchestrator.client_id:
            raise HTTPException(
                status_code=403,
                detail="You do not have permission to access this opportunity.",
            )

        # orchestrator is already initialized with the correct client_id from the header
        job_id = orchestrator.run_full_content_generation(
            opportunity_id, request.model_override, request.temperature
        )
        return {
            "job_id": job_id,
            "message": f"Content generation job {job_id} started.",
        }
    except Exception as e:
        logger.error(
            f"Failed to start generation job for {opportunity_id}: {e}", exc_info=True
        )
        raise HTTPException(status_code=500, detail=str(e))


@router.post(
    "/orchestrator/{opportunity_id}/run-validation-async", response_model=JobResponse
)
async def run_validation_async_endpoint(
    opportunity_id: int,
    db: DatabaseManager = Depends(get_db),
    orchestrator: WorkflowOrchestrator = Depends(get_orchestrator),
):
    try:
        opportunity = db.get_opportunity_by_id(opportunity_id)
        if not opportunity:
            raise HTTPException(status_code=404, detail="Opportunity not found.")
        if opportunity["client_id"] != orchestrator.client_id:
            raise HTTPException(
                status_code=403,
                detail="You do not have permission to access this opportunity.",
            )
        job_id = orchestrator.run_validation(opportunity_id)
        return {"job_id": job_id, "message": f"Validation job {job_id} started."}
    except Exception as e:
        logger.error(
            f"Failed to start validation job for {opportunity_id}: {e}", exc_info=True
        )
        raise HTTPException(status_code=500, detail=str(e))


@router.post(
    "/orchestrator/{opportunity_id}/run-analysis-async", response_model=JobResponse
)
async def run_analysis_async_endpoint(
    opportunity_id: int,
    request: AnalysisRequest,
    db: DatabaseManager = Depends(get_db),
    orchestrator: WorkflowOrchestrator = Depends(get_orchestrator),
):
    try:
        opportunity = db.get_opportunity_by_id(opportunity_id)
        if not opportunity:
            raise HTTPException(status_code=404, detail="Opportunity not found.")

        if opportunity["status"] in [
            "running",
            "in_progress",
            "pending",
            "refresh_started",
        ]:
            raise HTTPException(
                status_code=409,
                detail=f"A workflow is already active for this opportunity (Status: {opportunity['status']}).",
            )

        if opportunity["client_id"] != orchestrator.client_id:
            raise HTTPException(
                status_code=403,
                detail="You do not have permission to access this opportunity.",
            )
        # --- START MODIFICATION ---
        # Pass selected_competitor_urls from the request
        job_id = orchestrator.run_full_analysis(
            opportunity_id, request.selected_competitor_urls
        )
        # --- END MODIFICATION ---
        return {"job_id": job_id, "message": f"Full analysis job {job_id} started."}
    except Exception as e:
        logger.error(
            f"Failed to start analysis job for {opportunity_id}: {e}", exc_info=True
        )
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/orchestrator/{opportunity_id}/full-prompt", response_model=str)
async def get_full_prompt_endpoint(
    opportunity_id: int,
    db: DatabaseManager = Depends(get_db),
    orchestrator: WorkflowOrchestrator = Depends(get_orchestrator),
):
    """Endpoint to get the full, flattened prompt for an opportunity."""
    try:
        opportunity = db.get_opportunity_by_id(opportunity_id)
        if not opportunity:
            raise HTTPException(status_code=404, detail="Opportunity not found.")
        if opportunity["client_id"] != orchestrator.client_id:
            raise HTTPException(
                status_code=403,
                detail="You do not have permission to access this opportunity.",
            )

        full_prompt = orchestrator.get_full_prompt_for_display(opportunity_id)
        if not full_prompt:
            raise HTTPException(
                status_code=404,
                detail="Prompt has not been generated yet or opportunity data is missing.",
            )
        return full_prompt
    except Exception as e:
        logger.error(
            f"Failed to get full prompt for {opportunity_id}: {e}", exc_info=True
        )
        raise HTTPException(status_code=500, detail=str(e))


@router.post(
    "/orchestrator/{opportunity_id}/regenerate-social-async", response_model=JobResponse
)
async def regenerate_social_async_endpoint(
    opportunity_id: int,
    db: DatabaseManager = Depends(get_db),
    orchestrator: WorkflowOrchestrator = Depends(get_orchestrator),
):
    """Endpoint to start a job for regenerating only the social media posts."""
    try:
        opportunity = db.get_opportunity_by_id(opportunity_id)
        if not opportunity:
            raise HTTPException(status_code=404, detail="Opportunity not found.")

        if opportunity["client_id"] != orchestrator.client_id:
            raise HTTPException(
                status_code=403,
                detail="You do not have permission to access this opportunity.",
            )

        job_id = orchestrator.regenerate_social_posts(opportunity_id)
        return {
            "job_id": job_id,
            "message": f"Social media post regeneration job {job_id} started.",
        }
    except Exception as e:
        logger.error(
            f"Failed to start social post regeneration for {opportunity_id}: {e}",
            exc_info=True,
        )
        raise HTTPException(status_code=500, detail=str(e))


class DiscoveryCostParams(BaseModel):
    seed_keywords: List[str]
    discovery_modes: List[str]
    # We only need fields that affect cost calculation
    discovery_max_pages: Optional[int] = 1


class CostEstimationRequest(BaseModel):
    action_type: str
    discovery_params: Optional[DiscoveryCostParams] = None


@router.post("/orchestrator/estimate-cost")
async def estimate_cost_endpoint(
    request: CostEstimationRequest,
    opportunity_id: Optional[int] = None,  # Make opportunity_id optional
    db: DatabaseManager = Depends(get_db),
    orchestrator: WorkflowOrchestrator = Depends(get_orchestrator),
):
    """
    Endpoint to estimate the cost of a workflow action.
    For 'discovery', it uses discovery_params.
    For other actions, it uses opportunity_id.
    """
    action = request.action_type.lower()
    ALLOWED_ACTIONS = {"analyze", "generate", "validate", "discovery"}

    if action not in ALLOWED_ACTIONS:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid action '{action}'. Must be one of: {', '.join(ALLOWED_ACTIONS)}.",
        )

    try:
        if action == "discovery":
            if not request.discovery_params:
                raise HTTPException(
                    status_code=400,
                    detail="discovery_params are required for 'discovery' action.",
                )
            # For discovery, we don't need to check for an opportunity
            cost_estimation = orchestrator.estimate_action_cost(
                action=action, discovery_params=request.discovery_params.dict()
            )
        else:
            if not opportunity_id:
                raise HTTPException(
                    status_code=400,
                    detail="opportunity_id is required for this action.",
                )

            opportunity = db.get_opportunity_by_id(opportunity_id)
            if not opportunity:
                raise HTTPException(status_code=404, detail="Opportunity not found")

            if opportunity["client_id"] != orchestrator.client_id:
                raise HTTPException(
                    status_code=403,
                    detail="You do not have permission to access this opportunity.",
                )

            cost_estimation = orchestrator.estimate_action_cost(
                action=action, opportunity_id=opportunity_id
            )

        return cost_estimation
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Failed to estimate cost for action {action}: {e}", exc_info=True)
        raise HTTPException(
            status_code=500, detail="Failed to estimate cost due to a server error."
        )


@router.get("/jobs/{job_id}/status")
async def get_job_status_endpoint(
    job_id: str, jm: JobManager = Depends(get_job_manager)
):
    """Endpoint to get the status of a background job."""
    logger.info(f"API: Received request for job status: {job_id}")
    job_status = jm.get_job_status(job_id)
    if not job_status:
        logger.warning(f"API: Job with ID {job_id} not found in JobManager.")
        raise HTTPException(status_code=404, detail="Job not found")
    logger.info(f"API: Found job {job_id}, status: {job_status.get('status')}")
    return {"job_id": job_status["id"], "message": f"Status: {job_status['status']}", **job_status}


@router.get("/jobs")
async def get_all_jobs_endpoint(db: DatabaseManager = Depends(get_db)):
    """Endpoint to get all jobs for the activity log."""
    try:
        jobs = db.get_all_jobs()
        return jobs
    except Exception as e:
        logger.error(f"Failed to retrieve all jobs: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Failed to retrieve jobs.")


@router.post("/jobs/{job_id}/cancel")
async def cancel_job_endpoint(job_id: str, jm: JobManager = Depends(get_job_manager)):
    """Endpoint to cancel a running job."""
    try:
        success = jm.cancel_job(job_id)
        if success:
            return {"message": "Job cancellation request sent."}
        else:
            raise HTTPException(
                status_code=404, detail="Job not found or already completed."
            )
    except Exception as e:
        logger.error(f"Failed to cancel job {job_id}: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Failed to cancel job.")


@router.post(
    "/orchestrator/{opportunity_id}/run-full-auto-async", response_model=JobResponse
)
async def run_full_auto_async_endpoint(
    opportunity_id: int,
    request: AutoWorkflowRequest,  # ADD request body
    db: DatabaseManager = Depends(
        get_db
    ),  # Ensure DatabaseManager is correctly imported and injected
    orchestrator: WorkflowOrchestrator = Depends(get_orchestrator),
):
    """Endpoint to start the full 'auto' workflow from validation to generation."""
    try:
        opportunity = db.get_opportunity_by_id(opportunity_id)
        if not opportunity:
            raise HTTPException(status_code=404, detail="Opportunity not found.")

        if opportunity["status"] in [
            "running",
            "in_progress",
            "pending",
            "refresh_started",
        ]:
            raise HTTPException(
                status_code=409,
                detail=f"A workflow is already active for this opportunity (Status: {opportunity['status']}).",
            )

        if opportunity["client_id"] != orchestrator.client_id:
            raise HTTPException(
                status_code=403,
                detail="You do not have permission to access this opportunity.",
            )

        job_id = orchestrator.run_full_auto_workflow(
            opportunity_id, request.override_validation
        )  # Pass override flag
        return {
            "job_id": job_id,
            "message": f"Full auto workflow job {job_id} started.",
        }
    except Exception as e:
        logger.error(
            f"Failed to start full auto workflow for {opportunity_id}: {e}",
            exc_info=True,
        )
        raise HTTPException(status_code=500, detail=str(e))


@router.post(
    "/orchestrator/{opportunity_id}/rerun-analysis-async", response_model=JobResponse
)
async def clear_cache_and_analyze_endpoint(
    opportunity_id: int,
    db: DatabaseManager = Depends(get_db),
    orchestrator: WorkflowOrchestrator = Depends(get_orchestrator),
):
    """Clears API cache for the opportunity's keyword and starts a new analysis job."""
    try:
        opportunity = db.get_opportunity_by_id(opportunity_id)
        if not opportunity:
            raise HTTPException(status_code=404, detail="Opportunity not found.")

        if opportunity["status"] in [
            "running",
            "in_progress",
            "pending",
            "refresh_started",
        ]:
            raise HTTPException(
                status_code=409,
                detail=f"A workflow is already active for this opportunity (Status: {opportunity['status']}).",
            )

        if opportunity["client_id"] != orchestrator.client_id:
            raise HTTPException(
                status_code=403,
                detail="You do not have permission to access this opportunity.",
            )

        job_id = orchestrator.run_full_analysis(opportunity_id)
        return {
            "job_id": job_id,
            "message": f"Cache cleared and analysis job {job_id} started.",
        }
    except Exception as e:
        logger.error(
            f"Failed to clear cache and analyze for {opportunity_id}: {e}",
            exc_info=True,
        )
        raise HTTPException(status_code=500, detail=str(e))


@router.get(
    "/orchestrator/{opportunity_id}/score-narrative", response_model=Dict[str, str]
)
async def get_score_narrative_endpoint(
    opportunity_id: int,
    db: DatabaseManager = Depends(get_db),
    orchestrator: WorkflowOrchestrator = Depends(get_orchestrator),
):
    """Endpoint to generate a human-readable narrative for the score breakdown."""
    try:
        opportunity = db.get_opportunity_by_id(opportunity_id)
        if not opportunity:
            raise HTTPException(status_code=404, detail="Opportunity not found.")
        if opportunity["client_id"] != orchestrator.client_id:
            raise HTTPException(
                status_code=403,
                detail="You do not have permission to access this opportunity.",
            )

        narrative = orchestrator.summary_generator.generate_score_narrative(
            opportunity.get("full_data", {}).get("score_breakdown", {})
        )
        return {"narrative": narrative}
    except Exception as e:
        logger.error(
            f"Failed to generate score narrative for {opportunity_id}: {e}",
            exc_info=True,
        )
        raise HTTPException(status_code=500, detail=str(e))


@router.post(
    "/orchestrator/{opportunity_id}/refresh-content-async", response_model=JobResponse
)
async def refresh_content_async_endpoint(
    opportunity_id: int,
    db: DatabaseManager = Depends(get_db),
    orchestrator: WorkflowOrchestrator = Depends(get_orchestrator),
):
    """Endpoint to trigger a refresh of an existing opportunity's content."""
    try:
        opportunity = db.get_opportunity_by_id(opportunity_id)
        if not opportunity:
            raise HTTPException(status_code=404, detail="Opportunity not found.")

        if opportunity["status"] in [
            "running",
            "in_progress",
            "pending",
            "refresh_started",
        ]:
            raise HTTPException(
                status_code=409,
                detail=f"A workflow is already active for this opportunity (Status: {opportunity['status']}).",
            )

        if opportunity["client_id"] != orchestrator.client_id:
            raise HTTPException(
                status_code=403,
                detail="You do not have permission to access this opportunity.",
            )

        job_id = orchestrator.run_content_refresh_workflow(opportunity_id)
        return {"job_id": job_id, "message": f"Content refresh job {job_id} started."}
    except Exception as e:
        logger.error(
            f"Failed to start content refresh for {opportunity_id}: {e}", exc_info=True
        )
        raise HTTPException(status_code=500, detail=str(e))


class FeaturedImageRequest(BaseModel):
    prompt: str


@router.post(
    "/orchestrator/{opportunity_id}/generate-featured-image-async",
    response_model=JobResponse,
)
async def generate_featured_image_async_endpoint(
    opportunity_id: int,
    request: FeaturedImageRequest,
    db: DatabaseManager = Depends(get_db),
    orchestrator: WorkflowOrchestrator = Depends(get_orchestrator),
):
    """Starts a job to generate a new featured image for an opportunity."""
    try:
        opportunity = db.get_opportunity_by_id(opportunity_id)
        if not opportunity:
            raise HTTPException(status_code=404, detail="Opportunity not found.")

        if opportunity["client_id"] != orchestrator.client_id:
            raise HTTPException(
                status_code=403,
                detail="You do not have permission to access this opportunity.",
            )

        job_id = orchestrator.regenerate_featured_image(opportunity_id, request.prompt)
        return {
            "job_id": job_id,
            "message": f"Featured image generation job {job_id} started.",
        }
    except Exception as e:
        logger.error(
            f"Failed to start featured image generation for {opportunity_id}: {e}",
            exc_info=True,
        )
        raise HTTPException(status_code=500, detail=str(e))


@router.post(
    "/orchestrator/{opportunity_id}/refine-content", response_model=Dict[str, str]
)
async def refine_content_endpoint(
    opportunity_id: int,
    request: RefineContentRequest,
    db: DatabaseManager = Depends(get_db),
    orchestrator: WorkflowOrchestrator = Depends(get_orchestrator),
):
    """Endpoint to refine a snippet of HTML content using an AI command."""
    try:
        opportunity = db.get_opportunity_by_id(opportunity_id)
        if not opportunity:
            raise HTTPException(status_code=404, detail="Opportunity not found.")

        if opportunity["client_id"] != orchestrator.client_id:
            raise HTTPException(
                status_code=403,
                detail="You do not have permission to access this opportunity.",
            )

        prompt_messages = [
            {
                "role": "system",
                "content": "You are an expert web content editor. You will receive a block of HTML and a specific command. Your task is to apply the command to the provided HTML segment and return ONLY the modified HTML block. You MUST preserve all original HTML tags, attributes (like IDs, classes, styles), and structure, only changing the text content or adding/removing tags as absolutely necessary to fulfill the command. Do not add any introductory or concluding remarks, just the refined HTML.",
            },
            {
                "role": "user",
                "content": f"Command: '{request.command}'\n\nHTML to modify:\n```html\n{request.html_content}\n```\n\nReturn ONLY the refined HTML:",
            },
        ]

        refined_html, error = orchestrator.openai_client.call_chat_completion(
            messages=prompt_messages,
            model=orchestrator.client_cfg.get("default_model", "gpt-5-nano"),
            temperature=0.4,
        )

        if error or not refined_html:
            raise HTTPException(
                status_code=500, detail=f"AI content refinement failed: {error}"
            )

        # Clean up potential markdown code block fences from the AI response
        refined_html = refined_html.strip()
        if refined_html.startswith("```html"):
            refined_html = refined_html[len("```html") :]
        if refined_html.endswith("```"):
            refined_html = refined_html[: -len("```")]

        return {"refined_html": refined_html.strip()}
    except Exception as e:
        logger.error(
            f"Failed to refine content for opp {opportunity_id}: {e}", exc_info=True
        )
        raise HTTPException(
            status_code=500, detail="Failed to refine content due to a server error."
        )


@router.post(
    "/orchestrator/{opportunity_id}/generate-content-override",
    response_model=JobResponse,
)
async def generate_content_override(
    opportunity_id: int,
    db: DatabaseManager = Depends(get_db),
    orchestrator: WorkflowOrchestrator = Depends(get_orchestrator),
):
    """Endpoint to manually trigger content generation override"""
    try:
        opportunity = db.get_opportunity_by_id(opportunity_id)
        if not opportunity:
            raise HTTPException(status_code=404, detail="Opportunity not found.")

        if opportunity["status"] in [
            "running",
            "in_progress",
            "pending",
            "refresh_started",
        ]:
            raise HTTPException(
                status_code=409,
                detail=f"A workflow is already active for this opportunity (Status: {opportunity['status']}).",
            )

        if opportunity["client_id"] != orchestrator.client_id:
            raise HTTPException(
                status_code=403,
                detail="You do not have permission to access this opportunity.",
            )
        job_id = orchestrator.run_full_auto_workflow(
            opportunity_id, True
        )  # Run with override = True
        return {
            "job_id": job_id,
            "message": f"Content generation override job {job_id} started.",
        }
    except Exception as e:
        logger.error(
            f"Failed to start content generation override for {opportunity_id}: {e}",
            exc_info=True,
        )
        raise HTTPException(status_code=500, detail=str(e))


@router.post(
    "/orchestrator/approve-analysis/{opportunity_id}", response_model=JobResponse
)
async def approve_analysis_endpoint(
    opportunity_id: int,
    request: ApproveAnalysisRequest,  # Use the new request body model
    db: DatabaseManager = Depends(get_db),
    jm: JobManager = Depends(get_job_manager),
    orchestrator: WorkflowOrchestrator = Depends(
        get_orchestrator
    ),  # Add orchestrator to get client_id
):
    """Endpoint to approve the analysis and continue the workflow by starting content generation with optional overrides."""
    try:
        opportunity = db.get_opportunity_by_id(opportunity_id)
        if not opportunity:
            raise HTTPException(status_code=404, detail="Opportunity not found.")

        if opportunity["status"] in [
            "running",
            "in_progress",
            "pending",
            "refresh_started",
        ]:
            raise HTTPException(
                status_code=409,
                detail=f"A workflow is already active for this opportunity (Status: {opportunity['status']}).",
            )

        # Add authorization check
        if opportunity["client_id"] != orchestrator.client_id:
            raise HTTPException(
                status_code=403,
                detail="You do not have permission to access this opportunity.",
            )

        # Convert Pydantic model to dict if it exists, else pass None
        overrides_dict = request.overrides.dict() if request.overrides else None

        job_id = orchestrator.run_full_content_generation(
            opportunity_id, overrides=overrides_dict
        )

        return {
            "job_id": job_id,
            "message": f"Analysis approved. Started content generation job {job_id}.",
        }
    except ValueError as ve:
        logger.error(
            f"State mismatch trying to approve analysis for {opportunity_id}: {ve}",
            exc_info=True,
        )
        raise HTTPException(
            status_code=409, detail=str(ve)
        )  # 409 Conflict for state issues
    except Exception as e:
        logger.error(
            f"Failed to approve analysis for {opportunity_id}: {e}", exc_info=True
        )
        raise HTTPException(status_code=500, detail=str(e))


@router.post(
    "/orchestrator/reject-opportunity/{opportunity_id}", response_model=Dict[str, str]
)
async def reject_opportunity_endpoint(
    opportunity_id: int,
    db: DatabaseManager = Depends(get_db),
):
    """Endpoint to reject the opportunity and set status to 'rejected'"""
    try:
        # This is a direct status update, no job manager needed for rejection itself
        db.update_opportunity_workflow_state(
            opportunity_id,
            "rejected_by_user",
            "rejected",
            error_message="Opportunity rejected by user.",
        )
        return {"message": "Opportunity rejected."}
    except Exception as e:
        logger.error(
            f"Failed to reject opportunity {opportunity_id}: {e}", exc_info=True
        )
        raise HTTPException(status_code=500, detail=str(e))


class SocialMediaStatusUpdateRequest(BaseModel):
    new_status: str


# Add this new endpoint at the end of the file:
@router.post(
    "/orchestrator/{opportunity_id}/social-media-status", response_model=Dict[str, str]
)
async def update_social_media_status_endpoint(
    opportunity_id: int,
    request: SocialMediaStatusUpdateRequest,
    db: DatabaseManager = Depends(get_db),
    orchestrator: WorkflowOrchestrator = Depends(
        get_orchestrator
    ),  # For client_id auth
):
    """Endpoint to update the status of social media posts (e.g., 'approved', 'rejected')."""
    try:
        opportunity = db.get_opportunity_by_id(opportunity_id)
        if not opportunity:
            raise HTTPException(status_code=404, detail="Opportunity not found.")

        if opportunity["client_id"] != orchestrator.client_id:
            raise HTTPException(
                status_code=403,
                detail="You do not have permission to access this opportunity.",
            )

        valid_statuses = ["draft", "approved", "rejected", "scheduled", "published"]
        if request.new_status not in valid_statuses:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid status: {request.new_status}. Must be one of {valid_statuses}.",
            )

        db.update_social_media_posts_status(opportunity_id, request.new_status)
        return {
            "message": "Social media posts status updated successfully.",
            "new_status": request.new_status,
        }
    except Exception as e:
        logger.error(
            f"Failed to update social media status for opportunity {opportunity_id}: {e}",
            exc_info=True,
        )
        raise HTTPException(status_code=500, detail=str(e))
