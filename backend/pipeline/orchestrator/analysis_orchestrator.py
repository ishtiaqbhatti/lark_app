# backend/pipeline/orchestrator/analysis_orchestrator.py
import logging
import traceback
from typing import Dict, Any, List, Optional

logger = logging.getLogger(__name__)


class AnalysisOrchestrator:
    def run_analysis_phase(
        self,
        opportunity_id: int,
        selected_competitor_urls: Optional[List[str]] = None,
        use_cached_serp: bool = False,
    ) -> Dict[str, Any]:
        opportunity = self.db_manager.get_opportunity_by_id(opportunity_id)
        if not opportunity:
            return {
                "status": "failed",
                "message": f"Opportunity ID {opportunity_id} not found.",
            }

        keyword = opportunity.get("keyword")
        self.logger.info(
            f"--- Orchestrator: Starting Full Analysis for '{keyword}' ---"
        )
        self.db_manager.update_opportunity_workflow_state(
            opportunity_id, "analysis_started", "in_progress"
        )
        total_api_cost = 0.0

        try:
            # 1. Fetch Live SERP Data
            if use_cached_serp and opportunity.get("full_data", {}).get(
                "serp_overview"
            ):
                self.logger.info(f"Using cached SERP data for '{keyword}'...")
                live_serp_data = opportunity["full_data"]["serp_overview"]
                serp_api_cost = 0.0
            else:
                self.logger.info(f"Running live SERP data fetch for '{keyword}'...")
                from core.serp_analyzer import FullSerpAnalyzer

                serp_analyzer = FullSerpAnalyzer(
                    self.dataforseo_client, self.client_cfg
                )
                live_serp_data, serp_api_cost = serp_analyzer.analyze_serp(keyword)
                total_api_cost += serp_api_cost

            if not live_serp_data:
                self.logger.error(f"Failed to retrieve live SERP data for analysis for keyword: {keyword}")
                raise ValueError("Failed to retrieve live SERP data for analysis.")

            # --- START MODIFICATION ---
            # 2. NEW: Pre-Analysis Validation Gate (Safeguard for AI Calls)
            # Count valid "blog/article" results in top 15
            top_results_for_validation = live_serp_data.get("top_organic_results", [])[
                :15
            ]
            min_relevant_results = self.client_cfg.get(
                "min_relevant_analysis_results", 3
            )
            article_type_results_count = sum(
                1
                for r in top_results_for_validation
                if r.get("page_type") in ["Blog/Article", "News"]
            )

            if article_type_results_count < min_relevant_results:
                reason = f"Analysis failed: SERP is dominated by non-article formats ({article_type_results_count} relevant results found in top 15), making it unsuitable for this workflow."
                self.db_manager.update_opportunity_workflow_state(
                    opportunity_id, "pre_analysis_validation_failed", "failed", reason
                )
                self.logger.warning(f"Analysis halted for '{keyword}': {reason}")
                return {
                    "status": "failed",
                    "message": reason,
                    "api_cost": total_api_cost,
                }

            self.logger.info(
                f"Pre-analysis validation passed for '{keyword}' ({article_type_results_count} relevant results in top 15). Proceeding with blueprint generation."
            )
            # --- END MODIFICATION ---

            # 3. Conditional Competitor OnPage Analysis
            competitor_analysis = []
            competitor_api_cost = 0.0

            if self.client_cfg.get("enable_deep_competitor_analysis", False):
                self.logger.info(
                    "Deep competitor analysis is ENABLED. Running OnPage competitor analysis."
                )
                from pipeline.step_04_analysis.competitor_analyzer import (
                    FullCompetitorAnalyzer,
                )

                competitor_analyzer = FullCompetitorAnalyzer(
                    self.dataforseo_client, self.client_cfg
                )
                top_organic_urls = [
                    result["url"]
                    for result in live_serp_data.get("top_organic_results", [])[
                        : self.client_cfg.get("num_competitors_to_analyze", 5)
                    ]
                ]
                competitor_analysis, competitor_api_cost = (
                    competitor_analyzer.analyze_competitors(
                        top_organic_urls, selected_competitor_urls
                    )
                )
                total_api_cost += competitor_api_cost
            else:
                self.logger.info(
                    "Deep competitor analysis is DISABLED. Skipping OnPage competitor analysis."
                )

            # 4. Content Intelligence Synthesis
            from pipeline.step_04_analysis.content_analyzer import ContentAnalyzer

            content_analyzer = ContentAnalyzer(self.openai_client, self.client_cfg)
            content_intelligence, content_api_cost = (
                content_analyzer.synthesize_content_intelligence(
                    keyword,
                    live_serp_data,
                    competitor_analysis,  # Pass this list; it will be empty for the fast workflow
                )
            )
            total_api_cost += content_api_cost

            # 5. Determine Strategy & Generate Outline
            from pipeline.step_05_strategy.decision_engine import (
                StrategicDecisionEngine,
            )

            strategy_engine = StrategicDecisionEngine(self.client_cfg)
            recommended_strategy = strategy_engine.determine_strategy(
                live_serp_data, competitor_analysis, content_intelligence
            )

            ai_outline, outline_api_cost = content_analyzer.generate_ai_outline(
                keyword, live_serp_data, content_intelligence
            )
            total_api_cost += outline_api_cost
            content_intelligence.update(ai_outline)

            if not content_intelligence.get("article_structure"):
                self.logger.critical(
                    f"AI outline generation failed to produce an 'article_structure' for keyword: {keyword}."
                )
                raise ValueError("AI outline generation failed.")

            # 6. Assemble and Save Blueprint & Re-Score
            analysis_data = {
                "serp_overview": live_serp_data,
                "competitor_analysis": competitor_analysis,
                "content_intelligence": content_intelligence,
                "recommended_strategy": recommended_strategy,
            }

            blueprint = self.blueprint_factory.create_blueprint(
                seed_topic=keyword,
                winning_keyword_data=opportunity.get("full_data", {}).copy(),
                analysis_data=analysis_data,
                total_api_cost=total_api_cost,
                client_id=opportunity.get("client_id"),
            )

            opportunity["blueprint"] = blueprint

            final_score, final_score_breakdown = self.scoring_engine.calculate_score(
                opportunity
            )

            self.db_manager.update_opportunity_scores(
                opportunity_id, final_score, final_score_breakdown, blueprint
            )
            self.db_manager.update_opportunity_workflow_state(
                opportunity_id, "analysis_completed", "paused_for_approval"
            )

            return {
                "status": "success",
                "message": "Analysis phase completed and opportunity re-scored.",
                "api_cost": total_api_cost,
            }

        except Exception as e:
            error_message = f"Analysis phase failed unexpectedly: {e}"
            self.logger.error(f"{error_message}\n{traceback.format_exc()}")
            self.db_manager.update_opportunity_workflow_state(
                opportunity_id, "analysis_failed", "failed", error_message=str(e)
            )
            return {"status": "failed", "message": str(e), "api_cost": total_api_cost}

    def _run_analysis_background(
        self,
        job_id: str,
        opportunity_id: int,
        selected_competitor_urls: Optional[List[str]],
    ):
        try:
            self.run_analysis_phase(opportunity_id, selected_competitor_urls)
            self.job_manager.update_job_status(job_id, "completed", progress=100)
        except Exception as e:
            self.job_manager.update_job_status(job_id, "failed", error=str(e))
            raise

    def run_full_analysis(
        self, opportunity_id: int, selected_competitor_urls: Optional[List[str]] = None
    ) -> str:
        job_id = self.job_manager.create_job(
            self.client_id,
            target_function=self._run_analysis_background,
            args=(opportunity_id, selected_competitor_urls),
        )
        return job_id
