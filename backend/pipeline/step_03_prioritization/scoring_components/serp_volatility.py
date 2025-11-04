# backend/pipeline/step_03_prioritization/scoring_components/serp_volatility.py
from typing import Dict, Any, Tuple
from datetime import datetime, timezone

def calculate_serp_volatility_score(data: Dict[str, Any], config: Dict[str, Any]) -> Tuple[float, Dict[str, Any]]:
    """
    Calculates a score based on SERP stability. A more volatile (frequently changing) SERP
    can be an opportunity as it suggests Google is actively looking for better results.
    Score increases with higher volatility (shorter interval between updates).
    """
    serp_info = data.get("serp_info") if isinstance(data.get("serp_info"), dict) else {}
    last_update_str = serp_info.get("last_updated_time")
    prev_update_str = serp_info.get("previous_updated_time")

    if not last_update_str or not prev_update_str:
        return 50.0, {"SERP Stability": {"value": "N/A", "score": 50, "explanation": "Insufficient data for SERP volatility calculation."}}

    try:
        last_update = datetime.fromisoformat(last_update_str.replace(" +00:00", "")).replace(tzinfo=timezone.utc)
        prev_update = datetime.fromisoformat(prev_update_str.replace(" +00:00", "")).replace(tzinfo=timezone.utc)
        
        days_between_updates = abs((last_update - prev_update).days)

        stable_threshold = config.get("serp_volatility_stable_threshold_days", 90) # Default: 3 months
        
        # Score is inverted: shorter interval (more volatile) = higher score
        # Example: 0 days = 100 score, stable_threshold days = 0 score
        score = min(100, max(0, 100 - ((days_between_updates / stable_threshold) * 100)))

        explanation = f"SERP typically updates every {days_between_updates} days. More frequent updates (shorter intervals) indicate higher volatility, suggesting an opportunity."
        breakdown = {"SERP Stability": {"value": f"{days_between_updates} days", "score": round(score), "explanation": explanation}}
        return round(score), breakdown
    except (ValueError, TypeError):
        return 50.0, {"SERP Stability": {"value": "Error", "score": 50, "explanation": "Could not parse SERP update timestamps for volatility."}}