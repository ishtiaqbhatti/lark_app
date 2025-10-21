import logging
from typing import Dict, Any, List
import json


class StrategicDecisionEngine:
    """
    Analyzes SERP and competitor data to recommend a specific content strategy.
    """

    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.logger = logging.getLogger(self.__class__.__name__)

    def determine_strategy(
        self,
        serp_overview: Dict[str, Any],
        competitor_analysis: List[Dict[str, Any]],
        content_intelligence: Dict[str, Any],
    ) -> Dict[str, Any]:
        """
        Determines the optimal content format and strategic goal based on the analysis data.
        """
        content_format = serp_overview.get(
            "dominant_content_format", "Comprehensive Article"
        )
        strategic_goal = "Create a definitive guide that outranks competitors through superior depth and quality."

        top_results = serp_overview.get("top_organic_results", [])

        # --- START MODIFICATION ---
        # Check if deep analysis was performed to adjust logic
        deep_analysis_enabled = self.config.get(
            "enable_deep_competitor_analysis", False
        )

        # NEW: Repurpose focus_competitors for SERP-only mode
        focus_competitors_info = []
        if deep_analysis_enabled and competitor_analysis:
            focus_competitors_info = [
                {"url": c.get("url"), "onpage_score": c.get("onpage_score")}
                for c in competitor_analysis
                if c and c.get("url")
            ][:3]
        else:
            # In SERP-only mode, we can show top organic results as "focus competitors"
            focus_competitors_info = [
                {"url": r.get("url"), "title": r.get("title")} for r in top_results[:3]
            ]

        # NEW: Detect rating-heavy SERPs based on serp_overview data
        rating_count = sum(
            1
            for r in top_results
            if r.get("rating") and r["rating"].get("value") is not None
        )
        avg_rating_value = (
            sum(
                r["rating"]["value"]
                for r in top_results
                if r.get("rating") and r["rating"].get("value")
            )
            / rating_count
            if rating_count > 0
            else 0
        )

        if rating_count >= 3 and avg_rating_value >= 4.0:
            content_format = "Review Article"
            strategic_goal = "Produce an authoritative review or comparison that leverages strong social proof and clearly outlines pros/cons, aiming for rich snippets."
            # Prioritize this strategy by returning early after setting it
            return {
                "content_format": content_format,
                "strategic_goal": strategic_goal,
                "focus_competitors": focus_competitors_info,
                "final_qualification_assessment": {
                    "scorecard": self.generate_qualification_scorecard(
                        {
                            "serp_overview": serp_overview,
                            "competitor_analysis": competitor_analysis,
                            "content_intelligence": content_intelligence,
                        }
                    ),
                    **self._determine_final_recommendation(
                        self.generate_qualification_scorecard(
                            {
                                "serp_overview": serp_overview,
                                "competitor_analysis": competitor_analysis,
                                "content_intelligence": content_intelligence,
                            }
                        )
                    ),
                },
            }

        # ... (existing dynamic content format recommendations, e.g., Recipe, Scholarly, etc. - no change) ...

        # Rule: Weak competition (applies only if deep analysis was performed)
        if (
            content_format == "Comprehensive Article"
            and deep_analysis_enabled
            and competitor_analysis
        ):
            onpage_scores = [
                c.get("onpage_score")
                for c in competitor_analysis
                if c and c.get("onpage_score")
            ]
            if onpage_scores and (sum(onpage_scores) / len(onpage_scores)) < 60:
                strategic_goal = "Exploit the technical weaknesses of competitors by creating a fast, well-structured, and technically superior article."

        # FINAL QUALIFICATION GATE
        scorecard = self.generate_qualification_scorecard(
            {
                "serp_overview": serp_overview,
                "competitor_analysis": competitor_analysis,
                "content_intelligence": content_intelligence,
            }
        )
        recommendation = self._determine_final_recommendation(scorecard)
        # --- END MODIFICATION ---

        return {
            "content_format": content_format,
            "strategic_goal": strategic_goal,
            "focus_competitors": focus_competitors_info,  # Use the conditionally populated info
            "final_qualification_assessment": {
                "scorecard": scorecard,
                **recommendation,
            },
        }

    def generate_qualification_scorecard(self, analysis_data: dict) -> dict:
        """Generates a scorecard of qualification factors, adapted for SERP-only mode."""
        serp_overview = analysis_data.get("serp_overview", {})
        competitor_analysis = analysis_data.get("competitor_analysis", [])

        # --- START MODIFICATION ---
        deep_analysis_enabled = self.config.get(
            "enable_deep_competitor_analysis", False
        )

        hostility_score = 0
        for item in serp_overview.get("items", []):  # Iterate through raw SERP items
            if item.get("rank_absolute", 99) <= 10:
                # Count known hostile/attention-grabbing features
                if item.get("type") in [
                    "video",
                    "local_pack",
                    "carousel",
                    "twitter",
                    "shopping",
                    "app",
                    "short_videos",
                    "images",
                ]:
                    hostility_score += 1
                # Knowledge Graph with AI Overview is a stronger signal
                elif item.get("type") == "knowledge_graph" and (
                    "ai_overview_item" in json.dumps(item)
                ):  # Check for AI overview within KG items
                    hostility_score += 2
                elif item.get("type") == "ai_overview":  # Direct AI overview item
                    hostility_score += 2

        is_hostile_serp_environment = hostility_score > 5
        has_ai_overview = serp_overview.get("serp_has_ai_overview", False) or (
            "ai_overview_content" in serp_overview
            and serp_overview["ai_overview_content"] is not None
        )

        # Average competitor weaknesses calculation
        average_competitor_weaknesses = 0
        if deep_analysis_enabled and competitor_analysis:
            technical_warnings = [
                w
                for comp in competitor_analysis
                for w in comp.get("technical_warnings", [])
            ]
            average_competitor_weaknesses = (
                (len(technical_warnings) / len(competitor_analysis))
                if competitor_analysis
                else 0
            )
        else:
            # If deep analysis is disabled, we cannot assess technical weaknesses directly,
            # so we could default to a neutral or slightly positive value to avoid premature disqualification.
            average_competitor_weaknesses = 2  # Assume a moderate level if unknown

        # Has clear content angle (now based purely on content_intelligence from SERP)
        content_intelligence = analysis_data.get("content_intelligence", {})
        has_clear_content_angle = bool(
            content_intelligence.get("unique_angles_to_include")
            or content_intelligence.get("core_questions_answered_by_competitors")
        )

        # Is intent well-defined (now based on all SERP features)
        is_intent_well_defined = bool(
            serp_overview.get("paa_questions")
            or serp_overview.get("extracted_serp_features")
            or serp_overview.get("top_organic_faqs")  # NEW
            or serp_overview.get("top_organic_sitelinks")  # NEW
        )

        return {
            "hostility_score": hostility_score,
            "is_hostile_serp_environment": is_hostile_serp_environment,
            "has_ai_overview": has_ai_overview,
            "average_competitor_weaknesses": average_competitor_weaknesses,
            "has_clear_content_angle": has_clear_content_angle,
            "is_intent_well_defined": is_intent_well_defined,
        }
        # --- END MODIFICATION ---

    def _determine_final_recommendation(self, scorecard: dict) -> dict:
        """Determines the final go/no-go recommendation."""
        confidence_score = 100
        positive_factors = []
        negative_factors = []

        if scorecard["is_hostile_serp_environment"]:
            confidence_score -= 30
            negative_factors.append("SERP is dominated by non-article formats.")
        if scorecard["has_ai_overview"]:
            confidence_score -= 15
            negative_factors.append(
                "Google AI Overview is present, increasing ranking difficulty."
            )
        if scorecard["average_competitor_weaknesses"] < 2:
            confidence_score -= 20
            negative_factors.append("Competitors are technically strong.")
        if scorecard["average_competitor_weaknesses"] > 4:
            confidence_score += 10
            positive_factors.append(
                "Competitors show significant technical weaknesses."
            )
        if not scorecard["has_clear_content_angle"]:
            confidence_score -= 40
            negative_factors.append("No clear content differentiation angle was found.")
        if scorecard["has_clear_content_angle"]:
            positive_factors.append("A unique content angle has been identified.")
        if scorecard["is_intent_well_defined"]:
            positive_factors.append("User intent is well-defined by SERP features.")

        if confidence_score >= 80:
            recommendation = "Proceed"
        elif 50 <= confidence_score < 80:
            recommendation = "Proceed with Caution"
        else:
            recommendation = "Reject"

        return {
            "recommendation": recommendation,
            "confidence_score": confidence_score,
            "positive_factors": positive_factors,
            "negative_factors": negative_factors,
        }
