import logging
from typing import List, Dict, Any

from .scoring_engine import ScoringEngine


def run_prioritization_phase(
    opportunities: List[Dict[str, Any]], client_cfg: Dict[str, Any]
) -> List[Dict[str, Any]]:
    """
    Orchestrates the prioritization phase.

    1. Scores each opportunity based on a weighted formula.
    2. Sorts the opportunities by their calculated score.

    Returns a sorted list of opportunities with scoring data.
    """
    logger = logging.getLogger(__name__)
    logger.info("--- Starting Prioritization Phase ---")

    scoring_engine = ScoringEngine(client_cfg)

    # 1. Score Opportunities
    scored_opportunities = []
    for opp in opportunities:
        score, score_breakdown = scoring_engine.calculate_score(opp)
        opp["strategic_score"] = score
        # Add the focused competition score directly into the breakdown for persistence
        if "low_competition_score" in score_breakdown:
            opp["low_competition_score"] = score_breakdown["low_competition_score"][
                "score"
            ]
        opp["score_breakdown"] = score_breakdown
        scored_opportunities.append(opp)

    # 2. Sort Opportunities
    sorted_opportunities = sorted(
        scored_opportunities, key=lambda x: x["strategic_score"], reverse=True
    )

    logger.info(f"  -> Scored and sorted {len(sorted_opportunities)} opportunities.")
    logger.info("--- Prioritization Phase Complete ---")

    return sorted_opportunities
