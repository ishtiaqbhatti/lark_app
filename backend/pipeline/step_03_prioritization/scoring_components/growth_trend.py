# pipeline/step_03_prioritization/scoring_components/growth_trend.py
from typing import Dict, Any, Tuple
import math


def calculate_growth_trend_score(
    data: Dict[str, Any], config: Dict[str, Any]
) -> Tuple[float, Dict[str, Any]]:
    """
    Calculates a volume-weighted score based on the keyword's search volume trend.
    """
    if not isinstance(data, dict):
        return 0, {"message": "Invalid data format for scoring."}

    keyword_info = (
        data.get("keyword_info") if isinstance(data.get("keyword_info"), dict) else {}
    )
    trends = (
        keyword_info.get("search_volume_trend")
        if isinstance(keyword_info.get("search_volume_trend"), dict)
        else {}
    )
    sv = keyword_info.get("search_volume", 0) or 0

    yearly = trends.get("yearly", 0)
    quarterly = trends.get("quarterly", 0)
    monthly = trends.get("monthly", 0)

    def score_trend(value):
        if value is None:
            return 50  # Neutral score for missing data
        if value > 25:
            return 100
        if value > 10:
            return 75
        if value < -25:
            return 0
        if value < -10:
            return 25
        return 50

    yearly_score = score_trend(yearly)
    quarterly_score = score_trend(quarterly)
    monthly_score = score_trend(monthly)

    base_trend_score = (
        (yearly_score * 0.3) + (quarterly_score * 0.4) + (monthly_score * 0.3)
    )

    # Weight the trend score by search volume magnitude
    # A log scale helps moderate the effect of massive search volumes
    sv_weight = min(
        math.log(sv + 1) / math.log(100000), 1.0
    )  # Normalize against 100k SV

    # Final score is a blend: 70% trend, 30% volume weight. This prevents tiny keywords with huge trends from dominating.
    final_score = (base_trend_score * 0.7) + (sv_weight * 100 * 0.3)

    explanation = f"Weighted score from trends (Y:{yearly}%, Q:{quarterly}%, M:{monthly}%) and search volume."
    breakdown = {
        "Growth Trend": {
            "value": f"{yearly}% YoY",
            "score": round(final_score),
            "explanation": explanation,
        }
    }
    return round(final_score), breakdown
