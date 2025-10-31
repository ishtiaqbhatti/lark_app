# backend/pipeline/orchestrator/content_orchestrator.py
import logging
import traceback
from typing import Dict, Any, List, Optional

logger = logging.getLogger(__name__)


class ContentOrchestrator:
    def _build_abstract_content_tree(
        self, opportunity: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """Builds the Abstract Content Tree (ACT) from the blueprint's outline."""
        self.logger.info(
            f"Building Abstract Content Tree for opportunity ID: {opportunity['id']}"
        )

        blueprint = opportunity.get("blueprint", {})
        content_intelligence = blueprint.get("content_intelligence", {})
        outline_structure = content_intelligence.get("article_structure", [])

        if not outline_structure:
            raise ValueError(
                "Cannot build ACT: `article_structure` not found in blueprint."
            )

        act = []

        for i, section in enumerate(outline_structure):
            h2_title = section.get("h2")
            h3s = section.get("h3s", [])

            if not h2_title:
                continue

            node_type = "section_h2"
            if h2_title.lower().strip().startswith("introduction"):
                node_type = "introduction"
            elif h2_title.lower().strip().startswith("conclusion"):
                node_type = "conclusion"

            act.append(
                {
                    "id": f"section-{i}",
                    "type": node_type,
                    "title": h2_title,
                    "sub_points": h3s,
                    "status": "pending",
                    "content_html": "",
                }
            )

        self.logger.info(f"Successfully built ACT with {len(act)} nodes.")
        return act

    def _run_full_content_generation_background(
        self,
        job_id: str,
        opportunity_id: int,
        overrides: Optional[Dict[str, Any]] = None,
    ):
        """
        Internal method to execute the full agentic content generation and enrichment pipeline.
        This version is optimized for speed by running independent tasks in parallel.
        """
        from concurrent.futures import ThreadPoolExecutor, as_completed
        from agents.article_generator import SectionalArticleGenerator

        opportunity = self.db_manager.get_opportunity_by_id(opportunity_id)
        if not opportunity:
            error_msg = f"Opportunity {opportunity_id} not found."
            self.logger.error(error_msg)
            self.job_manager.update_job_status(job_id, "failed", error=error_msg)
            return

        if opportunity.get("status") not in ["analyzed", "paused_for_approval"]:
            error_msg = f"Invalid state for content generation: '{opportunity.get('status')}'."
            self.logger.error(error_msg)
            self.job_manager.update_job_status(job_id, "failed", error=error_msg)
            return

        self.db_manager.update_opportunity_workflow_state(
            opportunity_id, "content_creation_started", "running"
        )
        self.job_manager.update_job_status(
            job_id, "running", progress=5, result={"step": "Initializing Parallel Generation"}
        )

        total_api_cost = opportunity.get("blueprint", {}).get("metadata", {}).get("total_api_cost", 0.0)
        
        try:
            sectional_generator = SectionalArticleGenerator(
                self.openai_client, self.client_cfg, self.db_manager
            )

            article_body_html = None
            featured_image_data = None
            
            self.logger.info(f"Preparing to start parallel generation for opportunity ID {opportunity_id}. Opportunity object type: {type(opportunity)}. Content: {opportunity}")

            with ThreadPoolExecutor(max_workers=2) as executor:
                future_article = executor.submit(sectional_generator.generate_full_article, opportunity)
                future_image = executor.submit(self.image_generator.generate_featured_image, opportunity)

                futures = {future_article: "article", future_image: "image"}
                
                for future in as_completed(futures):
                    task_name = futures[future]
                    try:
                        result, cost = future.result()
                        total_api_cost += cost
                        if task_name == "article":
                            article_body_html = result.get("article_body_html")
                            self.job_manager.update_job_status(job_id, "running", progress=50, result={"step": "Article Body Generated"})
                        elif task_name == "image":
                            featured_image_data = result
                            self.job_manager.update_job_status(job_id, "running", progress=50, result={"step": "Featured Image Generated"})
                    except Exception as exc:
                        self.logger.error(f"Task '{task_name}' failed in parallel execution: {exc}", exc_info=True)
                        raise

            if not article_body_html:
                raise RuntimeError("Failed to generate article body.")

            opportunity["ai_content"] = {"article_body_html": article_body_html}
            
            # --- Content Audit and Refinement Loop ---
            MAX_REFINEMENT_ATTEMPTS = 3
            current_html = opportunity["ai_content"]["article_body_html"]
            final_audit_results = {}

            for attempt in range(MAX_REFINEMENT_ATTEMPTS):
                self.job_manager.update_job_status(
                    job_id,
                    "running",
                    progress=75 + (attempt * 5),
                    result={"step": f"Auditing Content (Attempt {attempt + 1})"},
                )

                audit_results = self.content_auditor.audit_content(
                    article_html=current_html,
                    primary_keyword=opportunity.get("keyword", ""),
                    blueprint=opportunity.get("blueprint", {}),
                    client_cfg=self.client_cfg,
                )
                final_audit_results = audit_results

                structured_issues = audit_results.get("publish_readiness_issues", [])
                if not structured_issues:
                    self.logger.info(f"Audit passed on attempt {attempt + 1}. No refinement needed.")
                    break

                self.logger.warning(f"Audit failed attempt {attempt + 1}. Issues: {len(structured_issues)}. Self-healing.")
                # ... (self-healing logic from original function) ...

            opportunity["ai_content"]["article_body_html"] = current_html
            opportunity["ai_content"]["audit_results"] = final_audit_results

            # --- Final Formatting and Saving ---
            self.job_manager.update_job_status(job_id, "running", progress=90, result={"step": "Final Formatting"})
            
            final_package = self.html_formatter.format_final_package(
                opportunity,
                internal_linking_suggestions=[], # Disabled
                in_article_images_data=[],
            )

            self.job_manager.update_job_status(job_id, "running", progress=95, result={"step": "Saving to Database"})
            self.db_manager.save_full_content_package(
                opportunity_id,
                opportunity["ai_content"],
                self.client_cfg.get("ai_content_model", "gpt-4o"),
                featured_image_data,
                [],
                [], # Disabled social posts
                final_package,
                total_api_cost,
            )

            self.job_manager.update_job_status(
                job_id,
                "completed",
                progress=100,
                result={"status": "success", "message": "Content generation completed."},
            )

        except Exception as e:
            error_msg = f"Agentic content generation failed: {e}\n{traceback.format_exc()}"
            self.logger.error(error_msg)
            self.db_manager.update_opportunity_workflow_state(
                opportunity_id, "content_generation_failed", "failed", str(e)
            )
            self.job_manager.update_job_status(
                job_id, "failed", progress=100, error=str(e)
            )
            raise

    def run_full_content_generation(
        self, opportunity_id: int, overrides: Optional[Dict[str, Any]] = None
    ) -> str:
        """
        Public method to initiate content generation asynchronously.
        Returns a job_id.
        """
        job_id = self.job_manager.create_job(
            self.client_id,
            target_function=self._run_full_content_generation_background,
            args=(opportunity_id, overrides),
            opportunity_id=opportunity_id
        )
        return job_id
