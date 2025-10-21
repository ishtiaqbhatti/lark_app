# pipeline/step_03_prioritization/scoring_components/serp_crowding.py
from typing import Dict, Any, Tuple


def calculate_serp_crowding_score(
    data: Dict[str, Any], config: Dict[str, Any]
) -> Tuple[float, Dict[str, Any]]:
    """
    Calculates a score based on how crowded the SERP is with attention-grabbing features.
    A less crowded SERP is a better opportunity.
    """
    if not isinstance(data, dict):
        return 0, {"message": "Invalid data format for scoring."}

    serp_info = data.get("serp_info") if isinstance(data.get("serp_info"), dict) else {}
    serp_types = set(serp_info.get("serp_item_types", []))

    # Define features that compete for user attention
    CROWDING_FEATURES = {
        "video",
        "short_videos",
        "images",
        "people_also_ask",
        "carousel",
        "multi_carousel",
        "featured_snippet",
        "ai_overview",
    }

    crowding_feature_count = len(serp_types.intersection(CROWDING_FEATURES))

    # The score is inverted: more features = lower score
    if crowding_feature_count >= 5:
        score = 0.0
    elif crowding_feature_count == 4:
        score = 25.0
    elif crowding_feature_count == 3:
        score = 50.0
    elif crowding_feature_count == 2:
        score = 75.0
    elif crowding_feature_count == 1:
        score = 90.0
    else:
        score = 100.0

    explanation = f"{crowding_feature_count} attention-grabbing features found. A lower count is better."
    breakdown = {
        "SERP Crowding": {
            "value": crowding_feature_count,
            "score": score,
            "explanation": explanation,
        }
    }

    return score, breakdown
