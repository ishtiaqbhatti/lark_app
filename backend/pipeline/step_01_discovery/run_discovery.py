import logging
from typing import List, Dict, Any, Optional

from data_access.database_manager import DatabaseManager
from external_apis.dataforseo_client_v2 import DataForSEOClientV2
from pipeline.step_01_discovery.keyword_expander import KeywordExpander
from pipeline.step_01_discovery.disqualification_rules import (
    apply_disqualification_rules,
)
from pipeline.step_01_discovery.cannibalization_checker import CannibalizationChecker
from pipeline.step_03_prioritization.scoring_engine import ScoringEngine
from pipeline.step_01_discovery.blog_content_qualifier import assign_status_from_score
from backend.services.serp_analysis_service import SerpAnalysisService


def run_discovery_phase(
    seed_keywords: List[str],
    dataforseo_client: DataForSEOClientV2,
    db_manager: "DatabaseManager",
    client_id: str,
    client_cfg: Dict[str, Any],
    discovery_modes: List[str],
    filters: Optional[List[Any]],
    order_by: Optional[List[str]],
    limit: Optional[int] = None,
    depth: Optional[int] = None,
    ignore_synonyms: Optional[bool] = False,
    include_clickstream_data: Optional[bool] = None,
    closely_variants: Optional[bool] = None,
    negative_keywords: Optional[List[str]] = None,
    run_logger: Optional[logging.Logger] = None,
) -> Dict[str, Any]:
    logger = run_logger or logging.getLogger(__name__)
    logger.info("--- Starting Discovery Phase ---")

    # INITIALIZE COST TRACKER:
    total_api_cost = 0.0
    cost_breakdown = {
        "keyword_ideas": 0.0,
        "keyword_suggestions": 0.0,
        "related_keywords": 0.0,
    }

    expander = KeywordExpander(dataforseo_client, client_cfg, logger)
    cannibalization_checker = CannibalizationChecker(
        client_cfg.get("target_domain"), dataforseo_client, client_cfg, db_manager
    )
    scoring_engine = ScoringEngine(client_cfg)

    existing_keywords = set(db_manager.get_all_processed_keywords_for_client(client_id))
    logger.info(f"Found {len(existing_keywords)} existing keywords to exclude.")

    # Expansion
    expansion_result = expander.expand_seed_keyword(
        seed_keywords,
        discovery_modes,
        filters,
        order_by,
        existing_keywords,
        limit,
        depth,
        ignore_synonyms,
    )

    all_expanded_keywords = expansion_result.get("final_keywords", [])
    
    # ADD EXPANSION COST:
    expansion_cost = expansion_result.get("total_cost", 0.0)
    total_api_cost += expansion_cost
    
    # DISTRIBUTE COST BY SOURCE:
    for source, count in expansion_result.get("raw_counts", {}).items():
        if count > 0:
            # Estimate cost per source based on count proportion
            proportion = count / max(expansion_result.get("total_raw_count", 1), 1)
            cost_breakdown[source] = expansion_cost * proportion

    logger.info(f"Expansion cost: ${expansion_cost:.4f}")

    # Scoring and Qualification
    processed_opportunities = []
    disqualification_reasons = {}
    status_counts = {"qualified": 0, "review": 0, "rejected": 0}

    for opp in all_expanded_keywords:
        # ... existing scoring logic ...
        processed_opportunities.append(opp)

    passed_count = status_counts.get("qualified", 0) + status_counts.get("review", 0)
    rejected_count = status_counts.get("rejected", 0)

    logger.info(f"Scoring complete. Passed: {passed_count}, Rejected: {rejected_count}")
    logger.info(f"Total API cost: ${total_api_cost:.4f}")

    stats = {
        **expansion_result,
        "disqualification_reasons": disqualification_reasons,
        "disqualified_count": rejected_count,
        "final_qualified_count": passed_count,
        "cost_breakdown": cost_breakdown,  # ADD THIS
    }

    return {
        "stats": stats,
        "total_cost": total_api_cost,  # ACCURATE TOTAL
        "opportunities": processed_opportunities,
    }
