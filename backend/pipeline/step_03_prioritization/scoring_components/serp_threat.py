# pipeline/step_03_prioritization/scoring_components/serp_threat.py
from typing import Dict, Any, Tuple


def calculate_serp_threat_score(
    data: Dict[str, Any], config: Dict[str, Any]
) -> Tuple[float, Dict[str, Any]]:
    """
    Calculates a unified "threat" score for the SERP. A lower score is better.
    This score is inverted for the final calculation (higher threat = lower opportunity).
    """
    if not isinstance(data, dict):
        return 0, {"message": "Invalid data format for scoring."}

    serp_info = data.get("serp_info") if isinstance(data.get("serp_info"), dict) else {}
    serp_types = set(serp_info.get("serp_item_types", []))

    threat_level = 0
    notes = []

    # Threat 1: Hostile, non-blog features
    HOSTILE_FEATURES = {
        "shopping",
        "popular_products",
        "local_pack",
        "google_flights",
        "google_hotels",
        "app",
        "jobs",
        "math_solver",
        "currency_box",
    }
    found_hostile = serp_types.intersection(HOSTILE_FEATURES)
    if found_hostile:
        threat_level += 50
        notes.append(f"Hostile features found ({', '.join(found_hostile)})")

    # Threat 2: AI Overview
    if "ai_overview" in serp_types:
        threat_level += config.get("ai_overview_penalty", 25)
        notes.append("AI Overview is present")

    # Threat 3: Paid Ads (implicit threat)
    if "paid" in serp_types:
        threat_level += 10
        notes.append("Paid ads are present")

    # Normalize the threat level to a 0-100 score
    final_threat_score = min(100, threat_level)

    # The final score is inverted: 100 is low threat, 0 is high threat.
    opportunity_score = 100 - final_threat_score

    explanation = (
        "Score reflects threats to organic CTR. " + "; ".join(notes)
        if notes
        else "No major threats found."
    )
    breakdown = {
        "SERP Threat": {
            "value": f"{final_threat_score}%",
            "score": opportunity_score,
            "explanation": explanation,
        }
    }

    return opportunity_score, breakdown
