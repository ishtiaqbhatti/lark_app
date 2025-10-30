# pipeline/step_03_prioritization/scoring_components/ease_of_ranking.py
import math
from typing import Dict, Any, Tuple


def _normalize_value(value: float, max_value: float, invert: bool = False) -> float:
    """Helper to normalize a value to a 0-100 scale with safe division."""
    if value is None or max_value is None:
        return 0.0
    
    # Prevent division by zero
    if max_value == 0:
        return 0.0
    
    # Ensure we're working with numbers
    try:
        value_float = float(value)
        max_float = float(max_value)
    except (ValueError, TypeError):
        return 0.0

    normalized = min(value_float / max_float, 1.0)

    if invert:
        return (1 - normalized) * 100
    return normalized * 100


def calculate_ease_of_ranking_score(
    data: Dict[str, Any], config: Dict[str, Any]
) -> Tuple[float, Dict[str, Any]]:
    """Calculates a score based on how easy it is to rank for the keyword."""
    if not isinstance(data, dict):
        return 0, {"message": "Invalid data format for scoring."}

    breakdown = {}
    keyword_props = (
        data.get("keyword_properties")
        if isinstance(data.get("keyword_properties"), dict)
        else {}
    )
    avg_backlinks = (
        data.get("avg_backlinks_info")
        if isinstance(data.get("avg_backlinks_info"), dict)
        else {}
    )
    serp_info = data.get("serp_info") if isinstance(data.get("serp_info"), dict) else {}

    # 1. Keyword Difficulty (KD)
    kd = keyword_props.get("keyword_difficulty", 50)
    kd_score = _normalize_value(kd, 100, invert=True)
    breakdown["Keyword Difficulty"] = {
        "value": kd,
        "score": round(kd_score),
        "explanation": "Lower is better.",
    }

    # 2. Average Main Domain Rank of competitors
    domain_rank = avg_backlinks.get("main_domain_rank", 500)
    max_rank = config.get("max_domain_rank_for_scoring", 1000)
    domain_rank_score = _normalize_value(domain_rank, max_rank, invert=True)
    breakdown["Avg. Domain Rank"] = {
        "value": f"{domain_rank:.0f}",
        "score": round(domain_rank_score),
        "explanation": f"Normalized against a max of {max_rank}. Lower is better.",
    }

    # 3. Average Page Rank of top competing pages
    page_rank = avg_backlinks.get("rank", 50)
    page_rank_score = _normalize_value(page_rank, 100, invert=True)
    breakdown["Avg. Page Rank"] = {
        "value": f"{page_rank:.0f}",
        "score": round(page_rank_score),
        "explanation": "Represents page-level authority. Lower is better.",
    }

    # 4. Dofollow Ratio
    total_backlinks = avg_backlinks.get("backlinks", 0)
    dofollow_backlinks = avg_backlinks.get("dofollow", 0)
    dofollow_ratio = dofollow_backlinks / total_backlinks if total_backlinks > 0 else 0
    dofollow_score = _normalize_value(
        dofollow_ratio, 1, invert=True
    )  # Lower ratio is better
    breakdown["Dofollow Ratio"] = {
        "value": f"{dofollow_ratio:.1%}",
        "score": round(dofollow_score),
        "explanation": "Ratio of dofollow links. A lower ratio indicates weaker competitor backlink profiles.",
    }

    # 5. Search Engine Results Count
    results_count = serp_info.get("se_results_count", 1_000_000)
    if results_count > 0:
        log_score = _normalize_value(
            math.log(results_count + 1), math.log(1_000_000_000 + 1), invert=True
        )
    else:
        log_score = 100.0
    breakdown["Total Results"] = {
        "value": f"{results_count:,}",
        "score": round(log_score),
        "explanation": "Log-normalized. Fewer competing pages is better.",
    }

    # Weighted average for final score
    final_score = (
        (kd_score * 0.40)
        + (domain_rank_score * 0.25)
        + (page_rank_score * 0.20)
        + (dofollow_score * 0.10)
        + (log_score * 0.05)
    )
    return round(final_score), breakdown
