# backend/pipeline/orchestrator/validation_orchestrator.py
import logging
import traceback

logger = logging.getLogger(__name__)


class ValidationOrchestrator:
    def run_validation_phase(self, opportunity_id: int):
        """
        Runs a cost-effective final validation gate before committing to a full analysis.
        Makes one live SERP call and a deep cannibalization check.
        """
        opportunity = self.db_manager.get_opportunity_by_id(opportunity_id)
        if not opportunity:
            return {
                "status": "failed",
                "message": f"Opportunity ID {opportunity_id} not found.",
            }

        self.logger.info(
            f"--- Orchestrator: Starting Live SERP Validation for '{opportunity.get('keyword')}' ---"
        )
        self.db_manager.update_opportunity_workflow_state(
            opportunity_id, "validation_started", "in_progress"
        )
        total_cost = 0.0

        try:
            from core.serp_analyzer import FullSerpAnalyzer

            serp_analyzer = FullSerpAnalyzer(self.dataforseo_client, self.client_cfg)
            serp_overview, serp_api_cost = serp_analyzer.analyze_serp(
                opportunity.get("keyword")
            )
            total_cost += serp_api_cost
            if not serp_overview:
                raise ValueError("Failed to retrieve live SERP data for validation.")

            from pipeline.step_04_analysis.run_analysis import run_final_validation

            is_valid, reason = run_final_validation(
                serp_overview, opportunity, self.client_cfg, self.dataforseo_client
            )

            if is_valid:
                self.db_manager.update_opportunity_workflow_state(
                    opportunity_id, "validation_passed", "validated"
                )
                self.logger.info(
                    f"Validation PASSED for '{opportunity.get('keyword')}'."
                )
                return {
                    "status": "success",
                    "message": "Validation passed. Ready for full analysis.",
                    "api_cost": total_cost,
                }
            else:
                self.db_manager.update_opportunity_status(opportunity_id, "rejected")
                self.db_manager.update_opportunity_workflow_state(
                    opportunity_id,
                    "validation_failed",
                    "rejected",
                    error_message=reason,
                )
                self.logger.warning(
                    f"Validation FAILED for '{opportunity.get('keyword')}': {reason}"
                )
                return {"status": "failed", "message": reason, "api_cost": total_cost}
        except Exception as e:
            error_msg = f"Validation phase failed unexpectedly: {e}"
            self.logger.error(f"{error_msg}\n{traceback.format_exc()}")
            self.db_manager.update_opportunity_workflow_state(
                opportunity_id, "validation_failed", "failed", error_message=str(e)
            )
            return {"status": "failed", "message": str(e), "api_cost": total_cost}

    def _run_validation_background(self, job_id: str, opportunity_id: int):
        """Internal method to execute the validation phase for a job."""
        self.job_manager.update_job_status(job_id, "running", progress=0)
        try:
            result = self.run_validation_phase(opportunity_id)

            if result["status"] == "success":
                self.job_manager.update_job_status(
                    job_id, "completed", progress=100, result=result
                )
            else:
                self.job_manager.update_job_status(
                    job_id, "failed", progress=100, error=result["message"]
                )
            return result
        except Exception as e:
            error_msg = f"Validation background failed: {e}\n{traceback.format_exc()}"
            self.logger.error(error_msg)
            self.db_manager.update_opportunity_workflow_state(
                opportunity_id, "validation_failed", "failed", str(e)
            )
            self.job_manager.update_job_status(
                job_id, "failed", progress=100, error=str(e)
            )
            raise

    def run_validation(self, opportunity_id: int) -> str:
        """Public method to initiate the validation phase asynchronously."""
        self.logger.info(
            f"--- Orchestrator: Initiating Validation for Opportunity ID: {opportunity_id} (Async) ---"
        )
        job_id = self.job_manager.create_job(
            target_function=self._run_validation_background, args=(opportunity_id,)
        )
        return job_id
