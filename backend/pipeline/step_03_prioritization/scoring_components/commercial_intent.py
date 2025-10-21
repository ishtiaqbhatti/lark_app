# pipeline/step_03_prioritization/scoring_components/commercial_intent.py
from typing import Dict, Any, Tuple
from backend.core import utils  # NEW: Import the utils module


def _normalize_value(value: float, max_value: float, invert: bool = False) -> float:
    """Helper to normalize a value to a 0-100 scale."""
    if value is None or max_value is None or max_value == 0:
        return 0.0

    normalized = min(float(value) / float(max_value), 1.0)

    if invert:
        return (1 - normalized) * 100
    return normalized * 100


def calculate_commercial_intent_score(
    data: Dict[str, Any], config: Dict[str, Any]
) -> Tuple[float, Dict[str, Any]]:
    """
    Calculates a score based on the keyword's strategic value for blog content,
    balancing commercial indicators with the type of user intent.
    """
    if not isinstance(data, dict):
        return 0, {"message": "Invalid data format for scoring."}

    keyword_info = (
        data.get("keyword_info") if isinstance(data.get("keyword_info"), dict) else {}
    )
    intent_info = (
        data.get("search_intent_info")
        if isinstance(data.get("search_intent_info"), dict)
        else {}
    )
    keyword = data.get("keyword", "")

    cpc = keyword_info.get("cpc", 0.0)
    if cpc is None:
        cpc = 0.0
    max_cpc = config.get("max_cpc_for_scoring", 10.0)
    cpc_score = _normalize_value(cpc, max_cpc)

    # Add bonus for wide CPC bid spread, indicating market inefficiency
    low_bid = keyword_info.get("low_top_of_page_bid", 0.0) or 0.0
    high_bid = keyword_info.get("high_top_of_page_bid", 0.0) or 0.0
    if low_bid > 0 and high_bid > low_bid:
        bid_spread_ratio = high_bid / low_bid
        if bid_spread_ratio > 5:  # e.g., low is $1, high is >$5
            cpc_score = min(100, cpc_score + 15)

    main_intent = intent_info.get("main_intent", "informational")
    foreign_intents = intent_info.get("foreign_intent", []) or []

    intent_scores = {
        "informational": 75,
        "commercial": 60,
        "transactional": 10,
        "navigational": 0,
    }
    intent_score = intent_scores.get(main_intent, 75)
    explanation = f"Base score for '{main_intent}' intent is {intent_score}."

    if main_intent == "informational" and (
        "commercial" in foreign_intents or "transactional" in foreign_intents
    ):
        intent_score = min(100, intent_score + 25)
        explanation += " Bonus for commercial secondary intent."

    # REPLACED: Use the centralized utility function
    if utils.is_question_keyword(keyword):
        intent_score = min(100, intent_score + 15)
        explanation += " Bonus for being a question keyword."

    competition_level = keyword_info.get("competition_level")
    if competition_level == "LOW":
        cpc_score = min(100, cpc_score + 20)

    final_score = (cpc_score * 0.5) + (intent_score * 0.5)
    breakdown = {
        "CPC & Competition": {
            "value": f"${cpc:.2f} ({competition_level})",
            "score": round(cpc_score),
            "explanation": "Normalized CPC, with bonuses for low competition and wide bid spread.",
        },
        "Strategic Intent": {
            "value": main_intent.title(),
            "score": round(intent_score),
            "explanation": explanation,
        },
    }
    return round(final_score), breakdown
