# backend/pipeline/step_03_prioritization/scoring_components/serp_freshness.py
from typing import Dict, Any, Tuple
from datetime import datetime, timezone

def calculate_serp_freshness_score(data: Dict[str, Any], config: Dict[str, Any]) -> Tuple[float, Dict[str, Any]]:
    """
    Calculates a score based on SERP freshness. An older SERP is generally a better opportunity.
    Score increases as the SERP gets older.
    """
    serp_info = data.get("serp_info") if isinstance(data.get("serp_info"), dict) else {}
    last_update_str = serp_info.get("last_updated_time")

    if not last_update_str:
        return 50.0, {"Freshness": {"value": "N/A", "score": 50, "explanation": "No freshness data available to calculate SERP freshness score."}}

    try:
        last_update = datetime.fromisoformat(last_update_str.replace(" +00:00", "")).replace(tzinfo=timezone.utc)
        current_time_utc = datetime.now(timezone.utc)
        days_since_update = (current_time_utc - last_update).days
        
        old_threshold = config.get("serp_freshness_old_threshold_days", 180) # Default: 6 months
        
        # Linear scaling: 0 days = 0 score, old_threshold days = 100 score
        score = min(100, max(0, (days_since_update / old_threshold) * 100))

        explanation = f"SERP last updated {days_since_update} days ago. Older SERPs (threshold > {old_threshold} days) represent a better opportunity for new content."
        breakdown = {"Freshness": {"value": f"{days_since_update} days", "score": round(score), "explanation": explanation}}
        return round(score), breakdown
    except (ValueError, TypeError):
        return 50.0, {"Freshness": {"value": "Error", "score": 50, "explanation": "Could not parse update timestamp for SERP freshness."}}