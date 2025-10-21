import logging
from typing import Dict, Any


class SummaryGenerator:
    """
    Generates a human-readable strategic summary of a keyword opportunity.
    """

    def __init__(self):
        self.logger = logging.getLogger(self.__class__.__name__)

    def generate_summary(self, opportunity: Dict[str, Any]) -> str:
        """Builds a narrative summary based on the opportunity's data."""
        full_data = opportunity.get("full_data", {})
        score_breakdown = full_data.get("score_breakdown", {})

        # Check qualification status first
        quality_status = full_data.get("quality_status", "passed")
        cannibal_status = full_data.get("cannibalization_status", "passed")
        if quality_status == "failed" or cannibal_status == "failed":
            reasons = ", ".join(full_data.get("reasons", ["Unknown reason"]))
            return f"**Disqualified:** This keyword was filtered out. Reason(s): {reasons}."

        # Build summary for qualified keywords using the new breakdown
        intent = full_data.get("search_intent_info", {}).get("main_intent", "unknown")
        summary_parts = [f"This is a promising **{intent.upper()}** opportunity."]

        ease_of_ranking_score = score_breakdown.get("ease_of_ranking", {}).get(
            "score", 0
        )
        if ease_of_ranking_score < 60:
            summary_parts.append(
                "However, the SERP shows some competitive challenges that will require a strong article."
            )
        elif ease_of_ranking_score < 85:
            summary_parts.append(
                "The competitive landscape appears favorable, with weaknesses to exploit."
            )
        else:  # 85+
            summary_parts.append(
                "The competitive landscape appears **extremely favorable**, with clear technical and content weaknesses among top competitors."
            )

        traffic_score = score_breakdown.get("traffic_potential", {}).get("score", 0)
        if traffic_score > 70:
            summary_parts.append("It has **excellent traffic potential**.")
        elif traffic_score > 40:
            summary_parts.append("It has solid traffic potential.")

        commercial_score = score_breakdown.get("commercial_intent", {}).get("score", 0)
        if commercial_score > 85:
            summary_parts.append(
                "The keyword shows **strong commercial value**, making it a high-priority target."
            )
        elif commercial_score > 60:
            summary_parts.append("It has good commercial value.")

        return " ".join(summary_parts)

    def generate_score_narrative(self, score_breakdown: Dict[str, Any]) -> str:
        narrative_parts = []
        if not score_breakdown:
            return "No score breakdown available to generate a narrative."

        # Ease of Ranking
        ease_score = score_breakdown.get("ease_of_ranking", {}).get("score", 0)
        if ease_score >= 80:
            narrative_parts.append(
                "Ranks highly due to a **very weak competitive landscape**."
            )
        elif ease_score >= 60:
            narrative_parts.append(
                "Has a good chance to rank because of a **favorable competitive landscape**."
            )
        else:
            narrative_parts.append(
                "Faces **strong competition**, making it a challenging keyword to rank for."
            )

        # Traffic Potential
        traffic_score = score_breakdown.get("traffic_potential", {}).get("score", 0)
        if traffic_score >= 75:
            narrative_parts.append("It has **excellent traffic potential**.")
        elif traffic_score >= 50:
            narrative_parts.append("It has **solid traffic potential**.")
        else:
            narrative_parts.append("Its traffic potential is moderate.")

        # Commercial Intent
        commercial_score = score_breakdown.get("commercial_intent", {}).get("score", 0)
        if commercial_score >= 80:
            narrative_parts.append("The keyword shows **strong commercial value**.")
        elif commercial_score >= 50:
            narrative_parts.append("It has **good commercial value**.")

        return "Overall: " + " ".join(narrative_parts)
