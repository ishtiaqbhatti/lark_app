# pipeline/step_03_prioritization/scoring_components/serp_freshness.py
from typing import Dict, Any, Tuple
from datetime import datetime


def calculate_serp_freshness_score(
    data: Dict[str, Any], config: Dict[str, Any]
) -> Tuple[float, Dict[str, Any]]:
    """
    Calculates a score based on SERP freshness. An older SERP is a better opportunity.
    """
    if not isinstance(data, dict):
        return 50.0, {
            "Freshness": {
                "value": "N/A",
                "score": 50,
                "explanation": "Invalid data format.",
            }
        }

    serp_info = data.get("serp_info") if isinstance(data.get("serp_info"), dict) else {}
    last_update_str = serp_info.get("last_updated_time")

    if not last_update_str:
        return 50.0, {
            "Freshness": {
                "value": "N/A",
                "score": 50,
                "explanation": "No freshness data.",
            }
        }

    try:
        last_update = datetime.fromisoformat(last_update_str.replace(" +00:00", ""))
        days_since_update = (datetime.now() - last_update).days

        # Score increases as the SERP gets older
        if days_since_update > 90:
            score = 100.0
        elif days_since_update > 60:
            score = 80.0
        elif days_since_update > 30:
            score = 60.0
        elif days_since_update > 14:
            score = 40.0
        else:
            score = 20.0

        explanation = f"SERP last updated {days_since_update} days ago. Older SERPs are better opportunities."
        breakdown = {
            "Freshness": {
                "value": f"{days_since_update} days",
                "score": score,
                "explanation": explanation,
            }
        }
        return score, breakdown

    except (ValueError, TypeError):
        return 50.0, {
            "Freshness": {
                "value": "Error",
                "score": 50,
                "explanation": "Could not parse update timestamp.",
            }
        }
