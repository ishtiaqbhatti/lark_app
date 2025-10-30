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
    discovery_max_pages: Optional[int] = None,
    run_logger: Optional[logging.Logger] = None,
) -> Dict[str, Any]:
    logger = run_logger or logging.getLogger(__name__)
    logger.info("--- Starting Consolidated Keyword Discovery & Scoring Phase ---")

    expander = KeywordExpander(dataforseo_client, client_cfg, logger)
    cannibalization_checker = CannibalizationChecker(
        client_cfg.get("target_domain"), dataforseo_client, client_cfg, db_manager
    )
    scoring_engine = ScoringEngine(client_cfg)

    # 1. Get keywords that already exist for this client to avoid API calls for them.
    existing_keywords = set(db_manager.get_all_processed_keywords_for_client(client_id))
    logger.info(
        f"Found {len(existing_keywords)} existing keywords to exclude from API request."
    )
    
    # 1b. Early cannibalization check on seed keywords
    # Filter out seed keywords that already exist (would be caught later anyway)
    original_seed_count = len(seed_keywords)
    seed_keywords = [kw for kw in seed_keywords if kw.lower() not in existing_keywords]
    
    if len(seed_keywords) < original_seed_count:
        logger.info(
            f"Early cannibalization filter: Removed {original_seed_count - len(seed_keywords)} "
            f"seed keywords that already exist in database."
        )
    
    if not seed_keywords:
        logger.warning("All seed keywords already exist in database. Skipping discovery.")
        return {
            "stats": {
                "total_cost": 0.0,
                "raw_counts": {},
                "total_raw_count": 0,
                "total_unique_count": 0,
                "disqualification_reasons": {"Already exists in database": original_seed_count},
                "disqualified_count": original_seed_count,
                "final_qualified_count": 0,
            },
            "total_cost": 0.0,
            "opportunities": [],
        }

    # 2. Expand seed keywords into a large list of opportunities.
    expansion_result = expander.expand_seed_keyword(
        seed_keywords,
        discovery_modes,
        filters,
        order_by,
        existing_keywords,
        limit,
        depth,
        ignore_synonyms,
        discovery_max_pages,
    )

    all_expanded_keywords = expansion_result.get("final_keywords", [])
    total_cost = expansion_result.get("total_cost", 0.0)

    # --- Negative Keyword Filtering ---
    if negative_keywords:
        initial_count = len(all_expanded_keywords)
        # Normalize negative keywords to lowercase for case-insensitive matching
        lower_negative_keywords = [kw.lower() for kw in negative_keywords]
        
        all_expanded_keywords = [
            opp for opp in all_expanded_keywords
            if not any(neg_kw in opp.get('keyword', '').lower() for neg_kw in lower_negative_keywords)
        ]
        
        removed_count = initial_count - len(all_expanded_keywords)
        if removed_count > 0:
            logger.info(f"Removed {removed_count} keywords based on negative keyword list.")

    # --- Scoring and Disqualification Loop (Consolidated Logic) ---
    processed_opportunities = []
    disqualification_reasons = {}
    status_counts = {"qualified": 0, "review": 0, "rejected": 0}
    required_keys = [
        "keyword_info",
        "keyword_properties",
        "serp_info",
        "search_intent_info",
    ]

    for opp in all_expanded_keywords:
        # Pre-validation of opportunity structure
        missing_keys = [
            key for key in required_keys if key not in opp or opp[key] is None
        ]
        if missing_keys:
            logger.warning(
                f"Skipping opportunity '{opp.get('keyword')}' due to missing required data: {', '.join(missing_keys)}"
            )
            continue

        # 3. Apply Hard Disqualification Rules (Cannibalization, Negative Keywords, etc.)
        is_disqualified, reason, is_hard_stop = apply_disqualification_rules(
            opp, client_cfg, cannibalization_checker
        )

        if is_disqualified and is_hard_stop:
            opp["status"] = "rejected"
            opp["blog_qualification_status"] = "rejected"
            opp["blog_qualification_reason"] = reason
            status_counts["rejected"] += 1
            disqualification_reasons[reason] = (
                disqualification_reasons.get(reason, 0) + 1
            )
        else:
            # 4. Score the remaining keywords
            score, breakdown = scoring_engine.calculate_score(opp)
            opp["strategic_score"] = score
            opp["score_breakdown"] = breakdown

            # 5. Assign Status based on Strategic Score
            status, reason = assign_status_from_score(opp, score, client_cfg)
            opp["status"] = status
            opp["blog_qualification_status"] = status
            opp["blog_qualification_reason"] = reason
            status_counts[status.split("_")[0]] = (
                status_counts.get(status.split("_")[0], 0) + 1
            )  # count qualified/review/rejected

        processed_opportunities.append(opp)

    disqualified_count = status_counts.get("rejected", 0)
    passed_count = status_counts.get("qualified", 0) + status_counts.get("review", 0)

    logger.info(
        f"Scoring and Qualification complete. Passed: {passed_count}, Rejected: {disqualified_count}."
    )

    stats = {
        **expansion_result,
        "disqualification_reasons": disqualification_reasons,
        "disqualified_count": disqualified_count,
        "final_qualified_count": passed_count,
    }

    return {
        "stats": stats,
        "total_cost": total_cost,
        "opportunities": processed_opportunities,
    }
