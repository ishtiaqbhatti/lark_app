# backend/pipeline/orchestrator/image_orchestrator.py
import logging
import traceback
import json

logger = logging.getLogger(__name__)


class ImageOrchestrator:
    def _run_single_image_generation_background(
        self, job_id: str, opportunity_id: int, original_prompt: str, new_prompt: str
    ):
        """Internal method to regenerate a single in-article image."""
        self.job_manager.update_job_status(job_id, "running", progress=0)

        try:
            opportunity = self.db_manager.get_opportunity_by_id(opportunity_id)
            if not opportunity or not opportunity.get("ai_content_json"):
                raise ValueError(
                    "Opportunity or content missing for single image regeneration."
                )

            opportunity["client_cfg"] = self.client_cfg

            self.job_manager.update_job_status(
                job_id,
                "running",
                progress=30,
                result={"step": "Generating single image"},
            )

            images_data, _ = self.image_generator.generate_images_from_prompts(
                [new_prompt]
            )

            if not images_data or not images_data[0]:
                raise RuntimeError("Image generation failed or returned no data.")

            new_image_data = images_data[0]

            self.job_manager.update_job_status(
                job_id,
                "running",
                progress=70,
                result={"step": "Updating content package"},
            )

            in_article_images = opportunity.get("in_article_images_data", [])
            if isinstance(in_article_images, str):
                in_article_images = (
                    json.loads(in_article_images) if in_article_images else []
                )

            updated_images = []
            found_and_updated = False
            for img in in_article_images:
                if img.get("original_prompt") == original_prompt:
                    img.update(new_image_data)
                    found_and_updated = True
                updated_images.append(img)

            if not found_and_updated:
                new_image_data["original_prompt"] = new_prompt
                updated_images.append(new_image_data)

            self.db_manager.update_opportunity_images(
                opportunity_id,
                opportunity.get("featured_image_url"),
                opportunity.get("featured_image_local_path"),
                updated_images,
            )

            final_package = self.html_formatter.format_final_package(opportunity)
            self.db_manager.update_opportunity_final_package(
                opportunity_id, final_package
            )

            result_message = {
                "status": "success",
                "message": f"Single image regenerated for prompt: {original_prompt}",
            }

            self.job_manager.update_job_status(
                job_id, "completed", progress=100, result=result_message
            )
            return result_message

        except Exception as e:
            error_msg = (
                f"Single image regeneration failed: {e}\n{traceback.format_exc()}"
            )
            self.logger.error(error_msg)
            self.job_manager.update_job_status(
                job_id, "failed", progress=100, error=str(e)
            )
            raise

    def regenerate_single_image(
        self, opportunity_id: int, original_prompt: str, new_prompt: str
    ) -> str:
        """Public method to initiate single image regeneration asynchronously."""
        self.logger.info(
            f"--- Orchestrator: Initiating Single Image Regeneration for Opportunity ID: {opportunity_id} (Async) ---"
        )
        job_id = self.job_manager.create_job(
            target_function=self._run_single_image_generation_background,
            args=(opportunity_id, original_prompt, new_prompt),
        )
        return job_id

    def _run_featured_image_regeneration_background(
        self, job_id: str, opportunity_id: int, prompt: str
    ):
        """Internal method to regenerate a featured image."""
        self.job_manager.update_job_status(
            job_id, "running", progress=10, result={"step": "Generating Featured Image"}
        )
        try:
            opportunity = self.db_manager.get_opportunity_by_id(opportunity_id)
            if not opportunity:
                raise ValueError(
                    "Opportunity not found for featured image regeneration."
                )

            opportunity["keyword"] = prompt
            opportunity["ai_content"] = {"meta_title": prompt}

            featured_image_data, cost = self.image_generator.generate_featured_image(
                opportunity
            )

            if featured_image_data:
                self.db_manager.update_opportunity_images(
                    opportunity_id,
                    featured_image_data.get("remote_url"),
                    featured_image_data.get("local_path"),
                    json.loads(opportunity.get("in_article_images_data", "[]")),
                )

            result_message = {
                "status": "success",
                "message": "Featured image regenerated successfully.",
                "api_cost": cost,
            }
            self.job_manager.update_job_status(
                job_id, "completed", progress=100, result=result_message
            )
            return result_message

        except Exception as e:
            error_msg = (
                f"Featured image regeneration failed: {e}\n{traceback.format_exc()}"
            )
            self.logger.error(error_msg)
            self.job_manager.update_job_status(
                job_id, "failed", progress=100, error=str(e)
            )
            raise

    def regenerate_featured_image(self, opportunity_id: int, prompt: str) -> str:
        """Public method to initiate featured image regeneration asynchronously."""
        self.logger.info(
            f"--- Orchestrator: Initiating Featured Image Regeneration for Opportunity ID: {opportunity_id} (Async) ---"
        )
        job_id = self.job_manager.create_job(
            target_function=self._run_featured_image_regeneration_background,
            args=(opportunity_id, prompt),
        )
        return job_id
