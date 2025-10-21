# pipeline/step_03_prioritization/scoring_components/serp_volatility.py
from typing import Dict, Any, Tuple
from datetime import datetime


def calculate_serp_volatility_score(
    data: Dict[str, Any], config: Dict[str, Any]
) -> Tuple[float, Dict[str, Any]]:
    """
    Calculates a score based on SERP stability. A more volatile SERP can be an opportunity.
    """
    if not isinstance(data, dict):
        return 50.0, {
            "SERP Stability": {
                "value": "N/A",
                "score": 50,
                "explanation": "Invalid data format.",
            }
        }

    serp_info = data.get("serp_info") if isinstance(data.get("serp_info"), dict) else {}
    breakdown = {}

    last_update_str = serp_info.get("last_updated_time")
    prev_update_str = serp_info.get("previous_updated_time")

    if not last_update_str or not prev_update_str:
        return 50.0, {
            "SERP Stability": {
                "value": "N/A",
                "score": 50,
                "explanation": "Insufficient data to calculate SERP volatility.",
            }
        }

    try:
        last_update = datetime.fromisoformat(last_update_str.replace(" +00:00", ""))
        prev_update = datetime.fromisoformat(prev_update_str.replace(" +00:00", ""))
        days_between_updates = (last_update - prev_update).days

        stable_threshold = config.get("serp_volatility_stable_threshold_days", 30)

        score = 0.0
        if days_between_updates < 7:  # Highly volatile
            score = 100.0
        elif days_between_updates < 21:  # Moderately volatile
            score = 75.0
        elif days_between_updates < stable_threshold:  # Relatively stable
            score = 50.0
        else:  # Very stable
            score = 25.0

        explanation = f"SERP updated every {days_between_updates} days. More frequent updates can signal an opportunity."
        breakdown["SERP Stability"] = {
            "value": f"{days_between_updates} days",
            "score": score,
            "explanation": explanation,
        }
        return score, breakdown

    except (ValueError, TypeError):
        return 50.0, {
            "SERP Stability": {
                "value": "Error",
                "score": 50,
                "explanation": "Could not parse SERP update timestamps.",
            }
        }
