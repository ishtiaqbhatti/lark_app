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
from core.utils import estimate_content_difficulty



def run_discovery_phase(
    seed_keywords: List[str],
    dataforseo_client: DataForSEOClientV2,
    db_manager: "DatabaseManager",
    client_id: str,
    client_cfg: Dict[str, Any],
    discovery_modes: List[str],
    filters: Optional[List[Dict[str, Any]]], # It now receives the merged list of filters
    order_by: Optional[List[str]],
    limit: Optional[int] = None,
    depth: Optional[int] = None,
    ignore_synonyms: Optional[bool] = False,
    # NEW params for direct passthrough
    include_clickstream_data: Optional[bool] = None,
    closely_variants: Optional[bool] = None,
    exact_match: Optional[bool] = None,
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

    # 2. Expand seed keywords into a large list of opportunities.
    expansion_result = expander.expand_seed_keyword(
        seed_keywords,
        discovery_modes,
        filters, # Pass the merged filters here
        order_by,
        existing_keywords,
        limit,
        depth,
        ignore_synonyms,
        # NEW params
        include_clickstream_data,
        closely_variants,
        exact_match,
    )

    all_expanded_keywords = expansion_result.get("final_keywords", [])
    total_cost = expansion_result.get("total_cost", 0.0)

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
            )
            
            # 6. NEW: Add content difficulty assessment for qualified/review keywords
            if status in ["qualified", "review"]:
                difficulty_data = estimate_content_difficulty(opp)
                opp["content_difficulty"] = difficulty_data
                logger.debug(
                    f"Content difficulty for '{opp.get('keyword')}': "
                    f"{difficulty_data['difficulty_level']} "
                    f"({difficulty_data['estimated_word_count']} words, "
                    f"{difficulty_data['production_time_hours']} hours)"
                )

        processed_opportunities.append(opp)

    qualified_count = status_counts.get("qualified", 0)
    review_count = status_counts.get("review", 0)
    rejected_count = status_counts.get("rejected", 0)
    passed_count = qualified_count + review_count
    
    # Calculate additional statistics
    total_processed = len(processed_opportunities)
    qualification_rate = (qualified_count / total_processed * 100) if total_processed > 0 else 0
    
    # Count opportunities by difficulty level
    difficulty_breakdown = {"easy": 0, "medium": 0, "hard": 0, "expert": 0}
    long_tail_count = 0
    seasonal_count = 0
    
    for opp in processed_opportunities:
        if opp.get("content_difficulty"):
            level = opp["content_difficulty"].get("difficulty_level", "unknown")
            if level in difficulty_breakdown:
                difficulty_breakdown[level] += 1
        
        if opp.get("is_long_tail_opportunity"):
            long_tail_count += 1
        
        seasonality = opp.get("seasonality_analysis", {})
        if seasonality.get("is_seasonal"):
            seasonal_count += 1
    
    logger.info("=" * 80)
    logger.info("DISCOVERY PHASE COMPLETE - SUMMARY STATISTICS")
    logger.info("=" * 80)
    logger.info(f"Total Keywords Processed: {total_processed}")
    logger.info(f"API Cost: ${expansion_result.get('total_cost', 0):.4f}")
    logger.info("-" * 80)
    logger.info("STATUS BREAKDOWN:")
    logger.info(f"  ✅ Qualified: {qualified_count} ({qualification_rate:.1f}%)")
    logger.info(f"  ⚠️  Review: {review_count}")
    logger.info(f"  ❌ Rejected: {rejected_count}")
    logger.info("-" * 80)
    logger.info("CONTENT DIFFICULTY DISTRIBUTION:")
    for level, count in difficulty_breakdown.items():
        if count > 0:
            logger.info(f"  {level.capitalize()}: {count}")
    logger.info("-" * 80)
    logger.info("SPECIAL OPPORTUNITIES:")
    logger.info(f"  🎯 Long-tail opportunities: {long_tail_count}")
    logger.info(f"  📅 Seasonal keywords: {seasonal_count}")
    logger.info("-" * 80)
    
    if disqualification_reasons:
        logger.info("TOP DISQUALIFICATION REASONS:")
        sorted_reasons = sorted(
            disqualification_reasons.items(), 
            key=lambda x: x[1], 
            reverse=True
        )[:5]
        for reason, count in sorted_reasons:
            logger.info(f"  • {reason}: {count}")
    
    logger.info("=" * 80)

    stats = {
        **expansion_result,
        "disqualification_reasons": disqualification_reasons,
        "disqualified_count": rejected_count,
        "final_qualified_count": qualified_count,
        "review_count": review_count,
        "total_passed_count": passed_count,
        "qualification_rate": round(qualification_rate, 2),
        "difficulty_breakdown": difficulty_breakdown,
        "long_tail_count": long_tail_count,
        "seasonal_count": seasonal_count,
    }

    return {
        "stats": stats,
        "total_cost": total_cost,
        "opportunities": processed_opportunities,
    }
