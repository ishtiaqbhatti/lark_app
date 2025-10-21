# pipeline/step_03_prioritization/scoring_components/traffic_potential.py
from typing import Dict, Any, Tuple


def _normalize_value(value: float, max_value: float, invert: bool = False) -> float:
    """Helper to normalize a value to a 0-100 scale."""
    if value is None or max_value is None or max_value == 0:
        return 0.0

    normalized = min(float(value) / float(max_value), 1.0)

    if invert:
        return (1 - normalized) * 100
    return normalized * 100


def calculate_traffic_potential_score(
    data: Dict[str, Any], config: Dict[str, Any]
) -> Tuple[float, Dict[str, Any]]:
    """
    Calculates a blended score based on both commercial traffic value and raw audience size.
    """
    if not isinstance(data, dict):
        return 0, {"message": "Invalid data format for scoring."}

    keyword_info = (
        data.get("keyword_info") if isinstance(data.get("keyword_info"), dict) else {}
    )
    sv = keyword_info.get("search_volume", 0) or 0
    cpc = keyword_info.get("cpc", 0.0) or 0.0

    # 1. Calculate Traffic Value Score
    traffic_value = sv * cpc
    max_traffic_value = config.get("max_traffic_value_for_scoring", 50000)
    traffic_value_score = _normalize_value(traffic_value, max_traffic_value)

    # 2. Calculate Raw Search Volume Score
    max_sv = config.get("max_sv_for_scoring", 100000)
    raw_sv_score = _normalize_value(sv, max_sv)

    # 3. Blend the scores to balance commercial value and audience size
    final_score = (traffic_value_score * 0.7) + (raw_sv_score * 0.3)

    explanation = f"Blended score: 70% from Est. Traffic Value (${traffic_value:,.0f}) and 30% from Raw SV ({sv})."
    breakdown = {
        "Traffic Potential": {
            "value": f"{sv} SV | ${cpc:.2f} CPC",
            "score": round(final_score),
            "explanation": explanation,
        }
    }

    return round(final_score), breakdown
