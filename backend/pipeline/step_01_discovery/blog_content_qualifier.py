# pipeline/step_01_discovery/blog_content_qualifier.py
from typing import Dict, Any, Tuple
from .disqualification_rules import apply_disqualification_rules


def assign_status_from_score(
    opportunity: Dict[str, Any], score: float, client_cfg: Dict[str, Any]
) -> Tuple[str, str]:
    """
    Assigns a final status to a keyword based on its score and hard disqualification rules.
    """
    # First, check for hard-stop, non-negotiable disqualification rules.
    is_disqualified, reason, is_hard_stop = apply_disqualification_rules(
        opportunity, client_cfg, cannibalization_checker=None
    )

    if is_disqualified and is_hard_stop:
        return "rejected", reason

    # If not hard-stopped, categorize based on the strategic score.
    if score >= client_cfg.get("qualified_threshold", 90):
        return "qualified", "Qualified: High strategic score."
    else:
        return "review", f"Review: Moderate strategic score ({score:.1f})."
