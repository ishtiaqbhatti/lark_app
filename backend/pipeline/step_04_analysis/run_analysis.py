import logging
from typing import Dict, Any, Optional, List, Tuple

from external_apis.dataforseo_client_v2 import DataForSEOClientV2
from external_apis.openai_client import OpenAIClientWrapper
from core.blueprint_factory import BlueprintFactory
from core.serp_analyzer import FullSerpAnalyzer
from .competitor_analyzer import FullCompetitorAnalyzer
from .content_analyzer import ContentAnalyzer
from pipeline.step_05_strategy.decision_engine import StrategicDecisionEngine
from pipeline.step_03_prioritization.scoring_engine import ScoringEngine

# --- NEW FUNCTION: run_final_validation ---
from urllib.parse import urlparse

# Then, replace the entire `run_final_validation` function with this new version.


def run_final_validation(
    live_serp_data: Dict[str, Any],
    opportunity: Dict[str, Any],
    client_cfg: Dict[str, Any],
    dataforseo_client: Any,
) -> Tuple[bool, Optional[str]]:
    full_data = opportunity.get("full_data", {})
    if not isinstance(full_data, dict):
        full_data = {}
    cached_serp_info = full_data.get("serp_info", {})
    cached_features = set(cached_serp_info.get("serp_item_types", []))
    live_features = set(live_serp_data.get("item_types", []))

    # NEW: Definitive Cannibalization Check (FIXED LOGIC)
    target_domain = client_cfg.get("target_domain", "").lower().replace("www.", "")
    if target_domain:
        for result in live_serp_data.get("top_organic_results", []):
            try:
                url_domain = (
                    urlparse(result.get("url", "")).netloc.lower().replace("www.", "")
                )
                # CRITICAL FIX: Check for exact match or subdomain suffix to avoid 'pet.com' matching 'competitor.com'
                if url_domain == target_domain or url_domain.endswith(
                    f".{target_domain}"
                ):
                    return (
                        False,
                        f"Final Validation Failed (Cannibalization): Target domain '{target_domain}' found in live SERP at URL '{result.get('url')}'.",
                    )
            except Exception:
                continue

    # Hostile features (configurable)
    hostile_features = set(
        client_cfg.get(
            "hostile_serp_features",
            [
                "shopping",
                "local_pack",
                "google_flights",
                "google_hotels",
                "popular_products",
            ],
        )
    )
    newly_added_hostile = live_features.intersection(
        hostile_features
    ) - cached_features.intersection(hostile_features)
    if newly_added_hostile:
        return (
            False,
            f"Final Validation Failed: Live SERP contains new hostile features: {', '.join(newly_added_hostile)}.",
        )

    # Non-blog content check (configurable domains & threshold)
    top_5_organic = live_serp_data.get("top_organic_results", [])[:5]
    non_blog_domains_cfg = set(client_cfg.get("final_validation_non_blog_domains", []))
    ugc_domains_cfg = set(
        client_cfg.get("ugc_and_parasite_domains", [])
    )  # Get from config

    hostile_domains = non_blog_domains_cfg.union(ugc_domains_cfg).union(
        client_cfg.get("competitor_blacklist_domains", [])
    )  # Combine all relevant hostile domains

    non_blog_count = sum(
        1
        for item in top_5_organic
        if any(domain in item.get("url", "") for domain in hostile_domains)
    )
    if non_blog_count >= client_cfg.get("max_non_blog_results", 4):
        return (
            False,
            "Final Validation Failed: Live SERP is dominated by non-blog/UGC/blacklisted content.",
        )

    # AI Overview comprehensiveness check (configurable threshold)
    disable_ai_overview_check = client_cfg.get("disable_ai_overview_check", False)
    if not disable_ai_overview_check:
        ai_overview_content = live_serp_data.get("ai_overview_content", "")
        if ai_overview_content and len(ai_overview_content.split()) > client_cfg.get(
            "max_ai_overview_words", 250
        ):
            return (
                False,
                "Final Validation Failed: AI Overview is too comprehensive, making a blog post redundant.",
            )

    # Organic visibility check (pixel ranking, configurable threshold)
    max_pixel_y = client_cfg.get("max_first_organic_y_pixel")
    if max_pixel_y is not None:
        first_organic_y = live_serp_data.get("first_organic_y_pixel")
        if first_organic_y is None:
            # Cannot check visibility without pixel data, proceed if other checks pass
            pass
        elif first_organic_y > max_pixel_y:
            return (
                False,
                f"Final Validation Failed: First organic result is too far down ({first_organic_y}px > {max_pixel_y}px).",
            )

    # NEW: LCP Check
    avg_lcp = live_serp_data.get("avg_page_timing", {}).get("largest_contentful_paint")
    if avg_lcp is not None and avg_lcp > client_cfg.get("max_avg_lcp_time", 4000):
        return (
            False,
            f"Final Validation Failed: Live SERP indicates poor page speed (Avg LCP: {avg_lcp}ms).",
        )

    return True, "Final validation passed."


# --- END NEW FUNCTION ---


def run_analysis_phase(
    opportunity: Dict[str, Any],
    openai_client: OpenAIClientWrapper,
    dataforseo_client: DataForSEOClientV2,
    client_cfg: Dict[str, Any],
    blueprint_factory: BlueprintFactory,
    scoring_engine: ScoringEngine,
    selected_competitor_urls: Optional[List[str]] = None,
) -> Tuple[Dict[str, Any], float]:
    logger = logging.getLogger(__name__)
    keyword = opportunity.get("keyword")
    logger.info(f"--- Starting Deep-Dive Analysis Phase for '{keyword}' ---")

    total_api_cost = 0.0

    serp_analyzer = FullSerpAnalyzer(dataforseo_client, client_cfg)
    competitor_analyzer = FullCompetitorAnalyzer(dataforseo_client, client_cfg)
    content_analyzer = ContentAnalyzer(openai_client, client_cfg)
    strategy_engine = StrategicDecisionEngine(client_cfg)
    # Blueprint factory is passed in, no need to re-initialize

    # 1. Make the single expensive, live SERP call for analysis
    logger.info(f"Making live SERP call for analysis of '{keyword}'...")
    serp_overview, serp_api_cost = serp_analyzer.analyze_serp(keyword)
    total_api_cost += serp_api_cost
    if not serp_overview:
        raise ValueError("Failed to retrieve live SERP data for analysis.")

    # VALIDATION GATE IS NOW REMOVED FROM THIS FUNCTION
    logger.info(f"Proceeding with full analysis for '{keyword}'.")

    # 2. On-Page competitor metadata and content analysis
    top_organic_urls = [
        result["url"]
        for result in serp_overview.get("top_organic_results", [])[
            : client_cfg.get("num_competitors_to_analyze", 5)
        ]
    ]
    competitor_analysis, competitor_api_cost = competitor_analyzer.analyze_competitors(
        top_organic_urls, selected_competitor_urls
    )
    total_api_cost += competitor_api_cost

    # 3. Content Intelligence Synthesis using the full content
    content_intelligence, content_api_cost = (
        content_analyzer.synthesize_content_intelligence(
            competitor_analysis,
            keyword,
            serp_overview.get("dominant_content_format", "Comprehensive Article"),
        )
    )
    total_api_cost += content_api_cost

    # 4. Determine Strategy
    recommended_strategy = strategy_engine.determine_strategy(
        serp_overview, competitor_analysis, content_intelligence
    )

    # 5. AI Content Outline Generation
    ai_outline, outline_api_cost = content_analyzer.generate_ai_outline(
        keyword, serp_overview, content_intelligence
    )
    total_api_cost += outline_api_cost
    content_intelligence.update(ai_outline)

    # 6. Assemble the final Blueprint
    analysis_data = {
        "serp_overview": serp_overview,
        "competitor_analysis": competitor_analysis,
        "content_intelligence": content_intelligence,
        "recommended_strategy": recommended_strategy,
    }

    blueprint = blueprint_factory.create_blueprint(
        seed_topic=keyword,
        winning_keyword_data=opportunity.get("full_data", {}).copy(),
        analysis_data=analysis_data,
        total_api_cost=total_api_cost,
        client_id=opportunity.get("client_id"),
    )

    opportunity["blueprint"] = blueprint

    # --- RE-SCORING ---
    # Re-calculate the strategic score with the new, rich data from the live SERP call
    # This ensures the score is based on the most accurate, up-to-date information
    final_score, final_score_breakdown = scoring_engine.calculate_score(opportunity)
    opportunity["strategic_score"] = final_score
    opportunity["score_breakdown"] = final_score_breakdown
    opportunity["full_data"]["strategic_score"] = final_score
    opportunity["full_data"]["score_breakdown"] = final_score_breakdown

    logger.info(f"  -> Final, updated strategic score: {final_score}")
    logger.info(f"  -> Total API Cost for Blueprint Generation: ${total_api_cost:.4f}")
    logger.info("--- Deep-Dive Analysis Phase Complete ---")

    return opportunity, total_api_cost
