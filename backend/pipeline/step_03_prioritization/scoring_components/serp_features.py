# pipeline/step_03_prioritization/scoring_components/serp_features.py
from typing import Dict, Any, Tuple


def calculate_serp_features_score(
    data: Dict[str, Any], config: Dict[str, Any]
) -> Tuple[float, Dict[str, Any]]:
    """
    Calculates a score based on the SERP environment, rewarding opportunities
    and penalizing attention-grabbing distractions.
    """
    if not isinstance(data, dict):
        return 0, {"message": "Invalid data format for scoring."}

    serp_info = data.get("serp_info") if isinstance(data.get("serp_info"), dict) else {}
    serp_types = set(serp_info.get("serp_item_types", []))

    score = 50.0  # Start with a neutral base score
    notes = []

    # Positive modifiers for high-value features
    if "featured_snippet" in serp_types:
        score += config.get("featured_snippet_bonus", 40)
        notes.append("Featured Snippet (+40)")
    if "people_also_ask" in serp_types:
        score += 25
        notes.append("People Also Ask (+25)")

    # Negative modifiers for threats and attention-grabbing features
    if "ai_overview" in serp_types:
        score -= config.get("ai_overview_penalty", 20)
        notes.append("AI Overview (-20)")
    if "video" in serp_types or "short_videos" in serp_types:
        score -= 15
        notes.append("Video Results (-15)")
    if "images" in serp_types:
        score -= 10
        notes.append("Image Carousel (-10)")

    final_score = max(0, min(100.0, score))
    explanation = (
        "Score reflects SERP opportunities. " + ", ".join(notes)
        if notes
        else "Neutral SERP environment."
    )

    breakdown = {
        "SERP Opportunity": {
            "value": len(notes),
            "score": final_score,
            "explanation": explanation.strip(),
        }
    }
    return final_score, breakdown
