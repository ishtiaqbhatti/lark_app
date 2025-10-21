# pipeline/step_03_prioritization/scoring_components/competitor_weakness.py
from typing import Dict, Any, Tuple


def _normalize_value(value: float, max_value: float, invert: bool = False) -> float:
    """Helper to normalize a value to a 0-100 scale."""
    if value is None or max_value is None or max_value == 0:
        return 0.0

    normalized = min(float(value) / float(max_value), 1.0)

    if invert:
        return (1 - normalized) * 100
    return normalized * 100


def calculate_competitor_weakness_score(
    data: Dict[str, Any], config: Dict[str, Any]
) -> Tuple[float, Dict[str, Any]]:
    """
    Calculates a score based on the authority of ranking competitors using
    data available at the discovery phase (avg_backlinks_info).
    """
    if not isinstance(data, dict):
        return 0, {"message": "Invalid data format for scoring."}

    breakdown = {}
    avg_backlinks = (
        data.get("avg_backlinks_info")
        if isinstance(data.get("avg_backlinks_info"), dict)
        else {}
    )

    # 1. Average Main Domain Rank of competitors
    domain_rank = avg_backlinks.get("main_domain_rank", 500)
    max_rank = config.get("max_domain_rank_for_scoring", 1000)
    domain_rank_score = _normalize_value(domain_rank, max_rank, invert=True)
    breakdown["Avg. Domain Rank"] = {
        "value": f"{domain_rank:.0f}",
        "score": round(domain_rank_score),
        "explanation": f"Normalized against a max of {max_rank}. Lower is better.",
    }

    # 2. Average Referring Main Domains
    ref_domains = avg_backlinks.get("referring_main_domains", 50)
    max_ref_domains = config.get("max_referring_domains_for_scoring", 100)
    ref_domains_score = _normalize_value(ref_domains, max_ref_domains, invert=True)
    breakdown["Avg. Referring Domains"] = {
        "value": f"{ref_domains:.1f}",
        "score": round(ref_domains_score),
        "explanation": f"Normalized against a max of {max_ref_domains}. Lower is better.",
    }

    # Weighted average for final score
    final_score = (domain_rank_score * 0.6) + (ref_domains_score * 0.4)
    return round(final_score), breakdown
