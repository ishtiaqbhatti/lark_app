# backend/pipeline/orchestrator/cost_estimator.py
import logging
from typing import Dict, Any, Optional

logger = logging.getLogger(__name__)


class CostEstimator:
    def estimate_action_cost(
        self,
        action: str,
        opportunity_id: Optional[int] = None,
        discovery_params: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """
        Estimates the API cost for a given workflow action without executing it.
        - For 'discovery', uses discovery_params.
        - For other actions, uses opportunity_id.
        """
        estimated_cost = 0.0
        explanation = []

        if action == "discovery":
            if not discovery_params:
                raise ValueError(
                    "discovery_params are required for 'discovery' action estimation."
                )

            KEYWORD_IDEAS_RATE = 0.005
            KEYWORD_SUGGESTIONS_RATE = 0.005
            RELATED_KEYWORDS_RATE = 0.005

            seed_keywords = discovery_params.get("seed_keywords", [])
            discovery_modes = discovery_params.get("discovery_modes", [])
            max_pages = self.client_cfg.get("discovery_max_pages", 1)
            num_seeds = len(seed_keywords)

            if "keyword_ideas" in discovery_modes:
                cost = KEYWORD_IDEAS_RATE * max_pages
                estimated_cost += cost
                explanation.append(
                    {
                        "service": "Keyword Ideas API",
                        "details": f"1 call x {max_pages} page(s) @ ${KEYWORD_IDEAS_RATE}/call",
                        "cost": cost,
                    }
                )

            if "keyword_suggestions" in discovery_modes:
                cost = KEYWORD_SUGGESTIONS_RATE * num_seeds * max_pages
                estimated_cost += cost
                explanation.append(
                    {
                        "service": "Keyword Suggestions API",
                        "details": f"{num_seeds} seed(s) x {max_pages} page(s) @ ${KEYWORD_SUGGESTIONS_RATE}/call",
                        "cost": cost,
                    }
                )

            if "related_keywords" in discovery_modes:
                cost = RELATED_KEYWORDS_RATE * num_seeds * max_pages
                estimated_cost += cost
                explanation.append(
                    {
                        "service": "Related Keywords API",
                        "details": f"{num_seeds} seed(s) x {max_pages} page(s) @ ${RELATED_KEYWORDS_RATE}/call",
                        "cost": cost,
                    }
                )

            return {"total_cost": estimated_cost, "breakdown": explanation}

        if not opportunity_id:
            raise ValueError(f"opportunity_id is required for action '{action}'.")

        opportunity = self.db_manager.get_opportunity_by_id(opportunity_id)
        if not opportunity:
            raise ValueError("Opportunity not found.")

        if action == "analyze" or action == "validate":
            serp_base_cost = 0.005
            serp_cost_explanation = (
                f"1 x SERP Live Advanced call (~${serp_base_cost:.3f} base)"
            )

            if self.client_cfg.get("load_async_ai_overview", False):
                serp_base_cost += 0.002
                serp_cost_explanation += " + $0.002 (Async AI Overview)"

            if self.client_cfg.get("calculate_rectangles", False):
                serp_base_cost += 0.002
                serp_cost_explanation += " + $0.002 (Pixel Ranking)"

            paa_depth = self.client_cfg.get("people_also_ask_click_depth", 0)
            if isinstance(paa_depth, int) and paa_depth > 0:
                paa_cost = paa_depth * 0.00015
                serp_base_cost += paa_cost
                serp_cost_explanation += f" + ${paa_cost:.5f} (PAA Depth {paa_depth})"

            estimated_cost += serp_base_cost
            explanation.append(
                {
                    "service": "SERP Live Advanced Task",
                    "details": serp_cost_explanation,
                    "cost": serp_base_cost,
                }
            )

            if action == "analyze":
                num_competitors = self.client_cfg.get("num_competitors_to_analyze", 5)

                ONPAGE_BASIC_RATE = 0.000125
                ONPAGE_RENDER_RATE = 0.00425
                ONPAGE_CUSTOM_JS_RATE = 0.00025

                if self.client_cfg.get("onpage_enable_browser_rendering", False):
                    onpage_per_task_cost = ONPAGE_RENDER_RATE
                    onpage_cost_explanation = f"x OnPage Instant Pages (Browser Rendering ON @ ${onpage_per_task_cost:.5f} each)"
                else:
                    onpage_per_task_cost = ONPAGE_BASIC_RATE
                    onpage_cost_explanation = f"x OnPage Instant Pages (Basic Crawl @ ${onpage_per_task_cost:.5f} each)"

                if self.client_cfg.get("onpage_enable_custom_js", False):
                    onpage_per_task_cost += ONPAGE_CUSTOM_JS_RATE
                    onpage_cost_explanation += " + $0.00025 (Custom JavaScript)"

                onpage_cost = num_competitors * onpage_per_task_cost
                estimated_cost += onpage_cost

                explanation.append(
                    {
                        "service": f"{num_competitors} Competitor OnPage Tasks",
                        "details": onpage_cost_explanation,
                        "cost": onpage_cost,
                    }
                )

            ai_analysis_cost = 0.05
            estimated_cost += ai_analysis_cost
            explanation.append(
                {
                    "service": "OpenAI Analysis Buffer",
                    "details": "1 x OpenAI GPT-4o call for analysis",
                    "cost": ai_analysis_cost,
                }
            )

        elif action == "generate":
            model = self.client_cfg.get("ai_content_model", "gpt-4o")

            pricing = self.client_cfg.get("OPENAI_PRICING", {})
            input_rate = pricing.get(f"{model}_input", 5.00) / 1000000
            output_rate = pricing.get(f"{model}_output", 15.00) / 1000000

            article_input_tokens = 10000
            article_output_tokens = 5000
            article_cost = (article_input_tokens * input_rate) + (
                article_output_tokens * output_rate
            )

            social_cost = (2000 * input_rate) + (500 * output_rate)

            buffer_tokens = 5000
            buffer_cost = (
                (buffer_tokens * input_rate) + (buffer_tokens * output_rate)
            ) * 0.5

            estimated_cost += article_cost
            explanation.append(
                {
                    "service": "AI Article Generation",
                    "details": f"1 x OpenAI {model} call (10k in, 5k out)",
                    "cost": article_cost,
                }
            )

            estimated_cost += social_cost
            explanation.append(
                {
                    "service": "AI Social Posts",
                    "details": f"1 x OpenAI {model} call (2k in, 0.5k out)",
                    "cost": social_cost,
                }
            )

            estimated_cost += buffer_cost
            explanation.append(
                {
                    "service": "AI Refinement/Linking Buffer",
                    "details": "50% chance of refinement/linking tokens",
                    "cost": buffer_cost,
                }
            )

            if self.client_cfg.get("use_pexels_first", True):
                explanation.append(
                    {
                        "service": "Image Sourcing (Pexels)",
                        "details": "Cost: $0.00",
                        "cost": 0.00,
                    }
                )
            else:
                image_cost = self.client_cfg.get("num_in_article_images", 0) * 0.04
                estimated_cost += image_cost
                explanation.append(
                    {
                        "service": f"Image Generation ({self.client_cfg.get('default_image_model', 'dall-e-3')})",
                        "details": f"Estimated {self.client_cfg.get('num_in_article_images', 0)} images @ $0.04 each",
                        "cost": image_cost,
                    }
                )

        elif action == "validate":
            # Assuming SERP_LIVE_ADVANCED_RATE is 0.020 USD
            SERP_LIVE_ADVANCED_RATE = 0.020
            validation_cost = SERP_LIVE_ADVANCED_RATE
            details = f"1 x SERP Live Advanced call (~${SERP_LIVE_ADVANCED_RATE:.3f})"
            if self.client_cfg.get("load_async_ai_overview", False):
                validation_cost += 0.002
                details += " + $0.002 for asynchronous AI Overview retrieval."
            estimated_cost += validation_cost
            explanation.append(
                {
                    "service": "SERP Validation",
                    "details": details,
                    "cost": validation_cost,
                }
            )

        return {"estimated_cost": round(estimated_cost, 2), "explanation": explanation}
