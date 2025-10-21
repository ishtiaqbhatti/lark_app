# backend/pipeline/orchestrator/social_orchestrator.py
import logging
import traceback

logger = logging.getLogger(__name__)


class SocialOrchestrator:
    def _run_social_posts_regeneration_background(
        self, job_id: str, opportunity_id: int
    ):
        """Internal method to regenerate social media posts."""
        self.job_manager.update_job_status(
            job_id, "running", progress=10, result={"step": "Crafting Social Posts"}
        )
        try:
            opportunity = self.db_manager.get_opportunity_by_id(opportunity_id)
            if not opportunity:
                raise ValueError("Opportunity not found for social media regeneration.")

            opportunity["client_cfg"] = self.client_cfg

            social_posts, cost = self.social_crafter.craft_posts(opportunity)
            if social_posts:
                self.db_manager.update_opportunity_social_posts(
                    opportunity_id, social_posts
                )

            result_message = {
                "status": "success",
                "message": "Social media posts regenerated successfully.",
                "api_cost": cost,
            }
            self.job_manager.update_job_status(
                job_id, "completed", progress=100, result=result_message
            )
            return result_message

        except Exception as e:
            error_msg = (
                f"Social media post regeneration failed: {e}\n{traceback.format_exc()}"
            )
            self.logger.error(error_msg)
            self.job_manager.update_job_status(
                job_id, "failed", progress=100, error=str(e)
            )
            raise

    def regenerate_social_posts(self, opportunity_id: int) -> str:
        """Public method to initiate social media post regeneration asynchronously."""
        self.logger.info(
            f"--- Orchestrator: Initiating Social Media Post Regeneration for Opportunity ID: {opportunity_id} (Async) ---"
        )
        job_id = self.job_manager.create_job(
            target_function=self._run_social_posts_regeneration_background,
            args=(opportunity_id,),
        )
        return job_id
