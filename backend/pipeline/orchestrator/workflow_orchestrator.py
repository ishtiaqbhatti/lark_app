# backend/pipeline/orchestrator/workflow_orchestrator.py
import logging
import traceback
import threading

logger = logging.getLogger(__name__)


class WorkflowOrchestrator:
    def _run_full_auto_workflow_background(
        self, job_id: str, opportunity_id: int, override_validation: bool
    ):
        """Internal method to execute the full workflow from validation to generation."""
        try:
            self.db_manager.update_opportunity_workflow_state(
                opportunity_id, "in_progress", "running"
            )
            self.job_manager.update_job_progress(job_id, "Workflow Started", "Starting full automation workflow.")

            if not override_validation:
                self.job_manager.update_job_progress(job_id, "Validation", "Running validation checks.")
                validation_result = self.run_validation_phase(opportunity_id)
                if validation_result.get("status") == "failed":
                    self.logger.warning(
                        f"Workflow for opportunity {opportunity_id} stopped due to validation failure: {validation_result.get('message')}"
                    )
                    raise RuntimeError(f"Validation failed: {validation_result.get('message')}")
            else:
                self.logger.info(
                    f"Validation step skipped for opportunity {opportunity_id} due to override."
                )
                self.job_manager.update_job_progress(job_id, "Validation", "Validation skipped by user override.")
                self.db_manager.update_opportunity_workflow_state(
                    opportunity_id,
                    "validation_overridden",
                    "validated",
                    error_message="Validation manually overridden.",
                )

            self.job_manager.update_job_progress(job_id, "Analysis", "Starting in-depth analysis.")
            analysis_result = self.run_analysis_phase(
                opportunity_id, selected_competitor_urls=None
            )
            if analysis_result.get("status") == "failed":
                reason = f"Disqualified during analysis: {analysis_result.get('message')}"
                self.logger.warning(
                    f"Full auto workflow for {opportunity_id} stopped: {reason}"
                )
                raise RuntimeError(reason)

            self.db_manager.update_opportunity_workflow_state(
                opportunity_id,
                "analysis_completed",
                "paused_for_approval",
                error_message="Awaiting user approval to proceed to content generation.",
            )
            self.job_manager.update_job_progress(job_id, "Paused", "Analysis complete. Awaiting user approval.", status="paused")
            self.logger.info(
                f"Full auto workflow for {opportunity_id} paused after analysis, awaiting user approval."
            )
            # This background job ends here. A new one is started by the 'approve_analysis' endpoint.
            # So, we set the job to a 'paused' but technically 'completed' state from the runner's perspective.
            self.job_manager.update_job_status(job_id, "paused", progress=50, result={"status": "paused", "message": "Awaiting approval."})

        except Exception as e:
            error_msg = f"Full auto workflow for {opportunity_id} failed: {e}"
            self.logger.error(f"{error_msg}\n{traceback.format_exc()}")
            # The job's _run_job wrapper will catch this and handle the final 'failed' state.
            raise

    def run_full_auto_workflow(
        self, opportunity_id: int, override_validation: bool = False
    ) -> str:
        """Public method to initiate the full auto workflow asynchronously."""
        self.logger.info(
            f"--- Orchestrator: Initiating Full Auto Workflow for Opportunity ID: {opportunity_id} (Async) with override: {override_validation} ---"
        )
        job_id = self.job_manager.create_job(
            target_function=self._run_full_auto_workflow_background,
            args=(opportunity_id, override_validation),
        )
        return job_id

    def _run_full_automation_workflow_background(
        self, job_id: str, opportunity_id: int, override_validation: bool
    ):
        """Internal method for the true 'fire and forget' full automation workflow."""
        try:
            self.db_manager.update_opportunity_workflow_state(
                opportunity_id, "in_progress", "running"
            )
            self.job_manager.update_job_progress(job_id, "Workflow Started", "Starting full automation workflow.")

            if not override_validation:
                self.job_manager.update_job_progress(job_id, "Validation", "Running validation checks.")
                validation_result = self.run_validation_phase(opportunity_id)
                if validation_result.get("status") == "failed":
                    self.logger.warning(
                        f"Automation for opportunity {opportunity_id} stopped due to validation failure: {validation_result.get('message')}"
                    )
                    raise RuntimeError(f"Validation failed: {validation_result.get('message')}")
            else:
                self.logger.info(
                    f"Validation step skipped for opportunity {opportunity_id} due to override."
                )
                self.job_manager.update_job_progress(job_id, "Validation", "Validation skipped by user override.")
                self.db_manager.update_opportunity_workflow_state(
                    opportunity_id,
                    "validation_overridden",
                    "validated",
                    error_message="Validation manually overridden.",
                )

            self.job_manager.update_job_progress(job_id, "Analysis", "Starting in-depth analysis.")
            analysis_result = self.run_analysis_phase(
                opportunity_id, selected_competitor_urls=None
            )
            if analysis_result.get("status") == "failed":
                reason = f"Disqualified during analysis: {analysis_result.get('message')}"
                self.logger.warning(
                    f"Full automation for {opportunity_id} stopped: {reason}"
                )
                raise RuntimeError(reason)

            self.logger.info(
                f"Analysis complete for {opportunity_id}, proceeding directly to content generation."
            )
            self.job_manager.update_job_progress(job_id, "Content Generation", "Analysis complete, starting content generation.")

            # This now calls the content generation logic which also uses update_job_progress
            self._run_full_content_generation_background(job_id, opportunity_id, overrides=None)
            
            # The _run_job wrapper will mark the job as completed.
            # We add the redirect_url to the result.
            final_result = {
                "status": "success",
                "message": "Full automation workflow completed successfully.",
                "redirect_url": f"/opportunities/{opportunity_id}"
            }
            self.job_manager.update_job_status(job_id, "completed", progress=100, result=final_result)

        except Exception as e:
            error_msg = f"Full automation workflow for {opportunity_id} failed: {e}"
            self.logger.error(f"{error_msg}\n{traceback.format_exc()}")
            # The job's _run_job wrapper will catch this and handle the final 'failed' state.
            raise
    
    # ... (keep existing public methods like run_full_automation_workflow) ...

    def continue_workflow_after_approval(self, job_id: str, opportunity_id: int, overrides: dict = None) -> str:
        """
        Continues a paused workflow job after user approval, proceeding to content generation.
        This now creates a NEW job for the content generation phase.
        """
        self.logger.info(
            f"Attempting to resume workflow from job {job_id} on opportunity {opportunity_id}."
        )

        job_info = self.job_manager.get_job_status(job_id)
        if not job_info or job_info.get("status") != "paused":
            error_msg = f"Cannot resume job {job_id}: Job not found or not in 'paused' state. Current status: {job_info.get('status') if job_info else 'Not Found'}."
            self.logger.error(error_msg)
            raise ValueError(error_msg)

        self.db_manager.update_opportunity_status(opportunity_id, "in_progress")

        # Create a new job for the content generation part of the workflow
        new_job_id = self.job_manager.create_job(
            target_function=self._run_full_content_generation_background,
            args=(opportunity_id, overrides),
        )
        
        # Link the old job to the new one for traceability if needed
        self.job_manager.update_job_status(job_id, "completed", progress=100, result={"status": "resumed", "next_job_id": new_job_id})

        return new_job_id

    def _run_content_refresh_workflow_background(
        self, job_id: str, opportunity_id: int
    ):
        """Internal method to execute content refresh for a job."""
        try:
            opportunity = self.db_manager.get_opportunity_by_id(opportunity_id)
            if not opportunity:
                raise ValueError("Opportunity not found for content refresh.")

            self.logger.info(
                f"--- Orchestrator: Starting Content Refresh Workflow for '{opportunity.get('keyword')}' ---"
            )
            self.db_manager.update_opportunity_workflow_state(
                opportunity_id, "refresh_started", "running"
            )
            self.job_manager.update_job_progress(job_id, "Refresh Started", "Re-analyzing content and SERP data.")

            analysis_result = self.run_analysis_phase(
                opportunity_id, selected_competitor_urls=None
            )
            if analysis_result.get("status") == "failed":
                raise RuntimeError(f"Refresh failed during analysis: {analysis_result.get('message')}")

            opportunity = self.db_manager.get_opportunity_by_id(opportunity_id)
            if not opportunity or opportunity.get("status") != "analyzed":
                raise RuntimeError("Opportunity not in 'analyzed' state after refresh analysis.")

            self.job_manager.update_job_progress(job_id, "Content Generation", "Analysis complete, re-generating content.")
            
            self._run_full_content_generation_background(job_id, opportunity_id, overrides=None)

            self.db_manager.update_opportunity_workflow_state(
                opportunity_id,
                "refresh_completed",
                "generated",
                error_message="Content refreshed.",
            )
            
            final_result = {
                "status": "success",
                "message": "Content refresh completed successfully.",
                "redirect_url": f"/opportunities/{opportunity_id}"
            }
            self.job_manager.update_job_status(job_id, "completed", progress=100, result=final_result)
            self.logger.info(f"Content refresh for opportunity {opportunity_id} completed successfully.")

        except Exception as e:
            error_msg = f"Content refresh workflow failed for opportunity {opportunity_id}: {e}\n{traceback.format_exc()}"
            self.logger.error(error_msg)
            self.db_manager.update_opportunity_workflow_state(
                opportunity_id, "refresh_failed", "failed", str(e)
            )
            # The job's _run_job wrapper will catch this and handle the final 'failed' state.
            raise

    def run_content_refresh_workflow(self, opportunity_id: int) -> str:
        """Public method to initiate an asynchronous content refresh workflow."""
        self.logger.info(
            f"--- Orchestrator: Initiating Content Refresh Workflow for Opportunity ID: {opportunity_id} (Async) ---"
        )
        job_id = self.job_manager.create_job(
            target_function=self._run_content_refresh_workflow_background,
            args=(opportunity_id,),
        )
        return job_id
