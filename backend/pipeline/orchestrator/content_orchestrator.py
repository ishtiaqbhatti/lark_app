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
        This is the complete, final version of this function.
        """
        opportunity = self.db_manager.get_opportunity_by_id(opportunity_id)
        if not opportunity:
            error_msg = f"Opportunity {opportunity_id} not found."
            self.logger.error(error_msg)
            self.job_manager.update_job_status(job_id, "failed", error=error_msg)
            return

        if opportunity.get("status") not in ["analyzed", "paused_for_approval"]:
            error_msg = f"Invalid state for content generation: '{opportunity.get("status")}'. Must be 'analyzed' or 'paused_for_approval'."
            self.logger.error(error_msg)
            self.job_manager.update_job_status(job_id, "failed", error=error_msg)
            return

        self.db_manager.update_opportunity_workflow_state(
            opportunity_id, "content_creation_started", "running"
        )
        self.job_manager.update_job_status(
            job_id, "running", progress=5, result={"step": "Initializing Generation"}
        )

        try:
            # --- START COST TRACKING MODIFICATION ---
            total_api_cost = opportunity.get("blueprint", {}).get("metadata", {}).get("total_api_cost", 0.0)
            self.logger.info(f"Initial cost from blueprint: ${total_api_cost:.4f}")
            # --- END COST TRACKING MODIFICATION ---

            self.job_manager.update_job_status(
                job_id, "running", progress=10, result={"step": "Building Content Tree"}
            )
            act = self._build_abstract_content_tree(opportunity)

            from agents.article_generator import SectionalArticleGenerator

            sectional_generator = SectionalArticleGenerator(
                self.openai_client, self.client_cfg, self.db_manager
            )

            full_article_context_for_conclusion = ""
            previous_content = ""
            for i, node in enumerate(act):
                progress = 15 + int((i / len(act)) * 40)
                self.job_manager.update_job_status(
                    job_id,
                    "running",
                    progress=progress,
                    result={"step": f"Generating: {node['title']}"},
                )

                content_html, cost = None, 0.0
                if node["type"] == "introduction":
                    content_html, cost = sectional_generator.generate_introduction(
                        opportunity
                    )
                elif node["type"] == "section_h2":
                    content_html, cost = sectional_generator.generate_section(
                        opportunity,
                        node["title"],
                        node.get("sub_points", []),
                        previous_content,
                    )
                elif node["type"] == "conclusion":
                    content_html, cost = sectional_generator.generate_conclusion(
                        opportunity, full_article_context_for_conclusion
                    )
                
                total_api_cost += cost # Aggregate cost

                if content_html:
                    node["content_html"] = content_html
                    full_article_context_for_conclusion += (
                        f"<h2>{node['title']}</h2>\n{content_html}\n"
                    )
                    previous_content = content_html
                else:
                    raise RuntimeError(
                        f"Failed to generate content for section '{node['title']}'."
                    )

            self.job_manager.update_job_status(
                job_id, "running", progress=60, result={"step": "Assembling Article"}
            )
            final_html_parts = [
                f"<h2>{node['title']}</h2>\n{node['content_html']}" for node in act
            ]
            final_article_html = "\n".join(final_html_parts)

            opportunity["ai_content"] = {"article_body_html": final_article_html}

            MAX_REFINEMENT_ATTEMPTS = 3
            current_html = opportunity["ai_content"]["article_body_html"]
            final_audit_results = {}

            for attempt in range(MAX_REFINEMENT_ATTEMPTS):
                self.job_manager.update_job_status(
                    job_id,
                    "running",
                    progress=65 + (attempt * 5),
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
                    self.logger.info(
                        f"Audit passed on attempt {attempt + 1}. No refinement needed."
                    )
                    break

                self.logger.warning(
                    f"Audit failed on attempt {attempt + 1}. Issues found: {len(structured_issues)}. Triggering self-healing."
                )
                self.job_manager.update_job_status(
                    job_id,
                    "running",
                    progress=70 + (attempt * 5),
                    result={"step": f"Self-Healing (Attempt {attempt + 1})"},
                )

                all_refinement_commands = []
                for issue in structured_issues:
                    if issue["issue"] == "unresolved_placeholder":
                        all_refinement_commands.append(
                            "- CRITICAL FIX: Remove all image placeholders like '[[IMAGE_ID:...]]' from the text."
                        )
                    elif issue["issue"] == "empty_heading":
                        all_refinement_commands.append(
                            f"- FIX: The following heading tag is empty: `{issue['context']}`. Based on the surrounding content, either remove this tag entirely or populate it with a relevant heading."
                        )
                    elif issue["issue"] == "short_paragraph":
                        all_refinement_commands.append(
                            f"- FIX: The paragraph `{issue['context']}` is too brief. Expand this paragraph to be at least 3 sentences long, providing more detail, or merge it with an adjacent paragraph if appropriate."
                        )
                    elif issue["issue"] == "word_count_deviation":
                        target_word_count = (
                            opportunity.get("blueprint", {})
                            .get("ai_content_brief", {})
                            .get("target_word_count", 1500)
                        )
                        all_refinement_commands.append(
                            f"- FIX: The article's word count is significantly off target. Review the entire article and expand or condense it to be approximately {target_word_count} words. {issue['context']}"
                        )

                if not all_refinement_commands:
                    break

                combined_command = (
                    "Please refine the entire HTML document by addressing the following issues:\n"
                    + "\n".join(all_refinement_commands)
                )

                refine_prompt_messages = [
                    {
                        "role": "system",
                        "content": "You are an expert content editor. You will receive a full HTML document and a list of specific issues to fix. Apply all fixes and return ONLY the complete, corrected HTML document. Preserve all original HTML tags and structure unless a fix requires changing them. Do not add any introductory text, just the refined HTML.",
                    },
                    {
                        "role": "user",
                        "content": f"COMMANDS:\n{combined_command}\n\nFULL HTML TO FIX:\n```html\n{current_html}\n```",
                    },
                ]

                refined_html, error = self.openai_client.call_chat_completion(
                    messages=refine_prompt_messages,
                    model=self.client_cfg.get("default_model", "gpt-5-nano"),
                    temperature=0.2,
                )
                total_api_cost += self.openai_client.latest_cost # Aggregate cost

                if error or not refined_html:
                    self.logger.error(
                        f"AI Refinement Agent failed on attempt {attempt + 1}: {error}"
                    )
                    break

                current_html = (
                    refined_html.strip()
                    .removeprefix("```html")
                    .removesuffix("```")
                    .strip()
                )

            opportunity["ai_content"]["article_body_html"] = current_html
            opportunity["ai_content"]["audit_results"] = final_audit_results

            self.job_manager.update_job_status(
                job_id,
                "running",
                progress=85,
                result={"step": "Generating Images & Social Posts"},
            )
            featured_image_data, image_cost = self.image_generator.generate_featured_image(
                opportunity
            )
            total_api_cost += image_cost
            social_posts, social_cost = self.social_crafter.craft_posts(opportunity)
            total_api_cost += social_cost

            self.job_manager.update_job_status(
                job_id,
                "running",
                progress=90,
                result={"step": "Formatting & Internal Linking"},
            )
            internal_link_suggestions, link_cost = (
                self.internal_linking_suggester.suggest_links(
                    opportunity["ai_content"]["article_body_html"],
                    opportunity.get("blueprint", {})
                    .get("ai_content_brief", {})
                    .get("key_entities_to_mention", []),
                    self.client_cfg.get("target_domain"),
                    self.client_id,
                )
            )
            total_api_cost += link_cost

            final_package = self.html_formatter.format_final_package(
                opportunity,
                internal_linking_suggestions=internal_link_suggestions,
                in_article_images_data=[],
            )

            self.job_manager.update_job_status(
                job_id, "running", progress=95, result={"step": "Saving to Database"}
            )
            self.db_manager.save_full_content_package(
                opportunity_id,
                opportunity["ai_content"],
                self.client_cfg.get("ai_content_model", "gpt-4o"),
                featured_image_data,
                [],
                social_posts,
                final_package,
                total_api_cost, # Pass total cost
            )

            self.job_manager.update_job_status(
                job_id,
                "completed",
                progress=100,
                result={
                    "status": "success",
                    "message": "Content generation completed.",
                },
            )

        except Exception as e:
            error_msg = (
                f"Agentic content generation failed: {e}\n{traceback.format_exc()}"
            )
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
        self.logger.info(
            f"--- Orchestrator: Initiating Full Content Generation for Opportunity ID: {opportunity_id} (Async) ---"
        )
        job_id = self.job_manager.create_job(
            self.client_id,
            target_function=self._run_full_content_generation_background,
            args=(opportunity_id, overrides),
        )
        return job_id
