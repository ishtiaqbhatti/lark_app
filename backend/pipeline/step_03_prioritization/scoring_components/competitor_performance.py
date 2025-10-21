from typing import Dict, Any, Tuple
import logging

logger = logging.getLogger(__name__)


def _normalize_value(
    value: float, target_value: float, is_lower_better: bool = True
) -> float:
    """Helper to normalize a value to a 0-100 scale, with target_value being ideal."""
    if value is None or target_value is None or target_value == 0:
        return 50.0  # Neutral score if data is missing or target is zero

    if is_lower_better:
        # Example: LCP target 2500ms.
        # If value is 1250, score = 100. If value is 5000, score = 0.
        # This formula provides 100 at 0, 50 at target, 0 at 2*target
        score = max(0.0, min(100.0, 100 * (1 - (value / (2 * target_value)))))
    else:
        # Example: High metric, higher is better. e.g. High security score
        score = max(
            0.0, min(100.0, 100 * (value / (2 * target_value)))
        )  # Max out at 2*target for 100, linear

    return score


def calculate_competitor_performance_score(
    opportunity: Dict[str, Any], config: Dict[str, Any]
) -> Tuple[float, Dict[str, Any]]:
    """
    Calculates a score based on the technical performance (e.g., Core Web Vitals)
    of top organic competitors. Weak competitor performance indicates a higher opportunity.
    """
    if not isinstance(opportunity, dict) or not opportunity.get("blueprint"):
        return 50.0, {"message": "Invalid opportunity data for scoring."}

    competitor_analysis = opportunity["blueprint"].get("competitor_analysis", [])
    if not competitor_analysis:
        return 50.0, {
            "message": "No competitor analysis available for performance scoring."
        }

    lcp_times = []
    for comp in competitor_analysis:
        if (
            comp.get("page_timing")
            and comp["page_timing"].get("largest_contentful_paint") is not None
        ):
            lcp_times.append(comp["page_timing"]["largest_contentful_paint"])

    if not lcp_times:
        return 50.0, {"message": "No LCP data available from competitors."}

    avg_lcp_ms = sum(lcp_times) / len(lcp_times)

    # Get the target LCP from client config (lower is better for performance)
    # This target defines what "good" performance is. Competitors worse than this are an opportunity.
    target_good_lcp_ms = config.get(
        "max_avg_lcp_time", 2500
    )  # Default to 2.5s as a good target

    # Score: higher if competitors' LCP is high (poor performance)
    # We want to invert the normalization: a higher LCP (worse performance) means higher score (better opportunity)
    # If avg_lcp_ms is 2*target_good_lcp_ms, score is 100. If it's target_good_lcp_ms, score is 50.
    score = _normalize_value(avg_lcp_ms, target_good_lcp_ms, is_lower_better=False)

    explanation = f"Average competitor LCP is {avg_lcp_ms:.0f}ms. Higher value indicates worse competitor performance, which is a better opportunity. Target LCP for good performance is {target_good_lcp_ms}ms."
    breakdown = {
        "Avg. Competitor LCP": {
            "value": f"{avg_lcp_ms:.0f}ms",
            "score": round(score),
            "explanation": explanation,
        }
    }

    return round(score), breakdown
