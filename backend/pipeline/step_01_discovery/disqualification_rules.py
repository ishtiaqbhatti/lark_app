# pipeline/step_01_discovery/disqualification_rules.py
import logging
import re
from typing import Dict, Any, Tuple, Optional
from datetime import datetime
import numpy as np
from core import utils

from .cannibalization_checker import CannibalizationChecker


def apply_disqualification_rules(
    opportunity: Dict[str, Any],
    client_cfg: Dict[str, Any],
    cannibalization_checker: CannibalizationChecker,
) -> Tuple[bool, Optional[str], bool]:
    """
    Applies the comprehensive 20-rule set to disqualify a keyword based on data from the discovery phase.
    Reads all thresholds from client_cfg.
    Returns (is_disqualified, reason, is_hard_stop).
    """
    logging.getLogger(__name__).info("Strategic score is not used for disqualification.")
    keyword = opportunity.get("keyword", "Unknown Keyword")

    # --- Failsafe Validation ---
    required_keys = [
        "keyword_info",
        "keyword_properties",
        "serp_info",
        "search_intent_info",
    ]
    for key in required_keys:
        if key not in opportunity or opportunity[key] is None:
            logging.getLogger(__name__).warning(
                f"Disqualifying '{keyword}' due to missing or null '{key}' data."
            )
            return True, f"Rule 1: Missing critical data structure ({key}).", True

    serp_info = opportunity.get("serp_info", {})
    if not serp_info:
        logging.getLogger(__name__).warning(
            f"Disqualifying '{keyword}' due to empty 'serp_info' data."
        )
        return True, "Rule 1: Missing SERP info data.", True

    keyword_info = opportunity.get("keyword_info") or {}
    keyword_props = opportunity.get("keyword_properties") or {}
    avg_backlinks = opportunity.get("avg_backlinks_info") or {}
    intent_info = opportunity.get("search_intent_info") or {}

    # New Rule: Reject if SV or KD is 0 or null
    search_volume = keyword_info.get("search_volume")
    keyword_difficulty = keyword_props.get("keyword_difficulty")

    if search_volume is None or search_volume == 0:
        return True, "Rule 0: Rejected due to zero or null Search Volume.", True
    
    if keyword_difficulty is None or keyword_difficulty == 0:
        return True, "Rule 0: Rejected due to zero or null Keyword Difficulty.", True

    # Tier 1: Foundational Checks
    if not all([keyword_info, keyword_props, intent_info]):
        return (
            True,
            "Rule 1: Missing critical data structures (keyword_info, keyword_properties, or search_intent_info).",
            True,
        )

    # Rule 2: Check primary intent
    allowed_intents = client_cfg.get("allowed_intents", ["informational"])
    main_intent = intent_info.get("main_intent")
    foreign_intents = intent_info.get("foreign_intent", [])

    if main_intent not in allowed_intents:
        return True, f"Rule 2: Non-target main intent ('{main_intent}').", True

    # Rule 2b (NEW): Check secondary intents for prohibitive types
    prohibited_intents = set(client_cfg.get("prohibited_intents", ["navigational"]))
    foreign_intents = intent_info.get("foreign_intent", []) or []
    if not prohibited_intents.isdisjoint(set(foreign_intents)):
        offending_intents = prohibited_intents.intersection(set(foreign_intents))
        return (
            True,
            f"Rule 2b: Contains a prohibited secondary intent ({', '.join(offending_intents)}).",
            True,
        )

    if keyword_props.get("is_another_language"):
        return True, "Rule 3: Language mismatch.", True

    negative_keywords = set(
        kw.lower() for kw in client_cfg.get("negative_keywords", [])
    )
    core_keyword = keyword_props.get("core_keyword")
    if any(neg_kw in keyword.lower() for neg_kw in negative_keywords) or (
        core_keyword
        and any(neg_kw in core_keyword.lower() for neg_kw in negative_keywords)
    ):
        return True, "Rule 4: Contains a negative keyword.", True

    # Tier 2: Volume & Trend Analysis
    if utils.safe_compare(
        keyword_info.get("search_volume"), client_cfg.get("min_search_volume"), "lt"
    ):
        return (
            True,
            f"Rule 5: Below search volume floor (minimum: {client_cfg.get('min_search_volume', 100)} SV). Current: {keyword_info.get('search_volume', 0)} SV.",
            False,
        )

    trends = keyword_info.get("search_volume_trend", {})
    try:
        yearly_trend = trends.get("yearly")
        quarterly_trend = trends.get("quarterly")

        yearly_threshold = client_cfg.get("yearly_trend_decline_threshold", -25)
        quarterly_threshold = client_cfg.get("quarterly_trend_decline_threshold", 0)

        yearly_check = utils.safe_compare(yearly_trend, yearly_threshold, "lt")
        quarterly_check = utils.safe_compare(quarterly_trend, quarterly_threshold, "lt")

        if yearly_check and quarterly_check:
            return (
                True,
                f"Rule 6: Consistently declining trend. Yearly trend: {yearly_trend}% (below {yearly_threshold}% threshold), Quarterly trend: {quarterly_trend}% (below {quarterly_threshold}% threshold). Consider manual review for seasonality.",
                False,
            )
    except TypeError:
        logging.getLogger(__name__).error(
            f"TypeError during trend analysis for keyword '{keyword}'. "
            f"trends.get('yearly') value: {trends.get('yearly')}, type: {type(trends.get('yearly'))}. "
            f"trends.get('quarterly') value: {trends.get('quarterly')}, type: {type(trends.get('quarterly'))}."
        )
        return (
            True,
            "Rule 6: Failed to process trend data due to invalid format.",
            False,
        )

    monthly_searches = keyword_info.get("monthly_searches", [])
    if monthly_searches and len(monthly_searches) > 1:
        volumes = [
            ms["search_volume"]
            for ms in monthly_searches
            if ms.get("search_volume") is not None and ms["search_volume"] > 0
        ]
        if len(volumes) > 1 and np.mean(volumes) > 0:
            volatility_threshold = client_cfg.get(
                "search_volume_volatility_threshold", 1.5
            )
            std_dev_to_mean_ratio = np.std(volumes) / np.mean(volumes)
            if std_dev_to_mean_ratio > volatility_threshold:
                return (
                    True,
                    f"Rule 7: Extreme search volume volatility. Std Dev / Mean ratio: {std_dev_to_mean_ratio:.2f} (above {volatility_threshold} threshold). Could indicate a fleeting trend or strong seasonality. Manual review recommended.",
                    False,
                )

    # Rule 7b: Check for recent sharp decline using raw monthly searches
    monthly_searches = opportunity.get(
        "monthly_searches", []
    )  # Get from opportunity object, which is deserialized
    if monthly_searches and len(monthly_searches) >= 4:
        # Sort by year and month to ensure correctness (most recent first for trend)
        try:
            sorted_searches = sorted(
                monthly_searches, key=lambda x: (x["year"], x["month"]), reverse=True
            )
            if len(sorted_searches) >= 4:
                # Compare latest month with 3 months prior (index 0 vs index 3)
                latest_vol = sorted_searches[0].get("search_volume")
                past_vol = sorted_searches[3].get("search_volume")

                if latest_vol is not None and past_vol is not None and past_vol > 0:
                    if (
                        latest_vol / past_vol
                    ) < 0.5:  # If volume has dropped by more than 50% in 3 months
                        return (
                            True,
                            "Rule 7b: Recent sharp decline in search volume (>50% drop in last 3 months).",
                            False,
                        )
        except (TypeError, KeyError):
            logging.getLogger(__name__).warning(
                f"Could not parse monthly_searches for recent trend analysis on keyword '{keyword}'."
            )

    # Tier 3: Commercial & Competitive Analysis
    if utils.safe_compare(
        keyword_info.get("competition"),
        client_cfg.get("max_paid_competition_score", 0.8),
        "gt",
    ) and (keyword_info.get("competition_level") == "HIGH"):
        return True, "Rule 8: Excessive paid competition.", False

    if utils.safe_compare(
        keyword_info.get("high_top_of_page_bid"),
        client_cfg.get("max_high_top_of_page_bid", 15.0),
        "gt",
    ):
        return (
            True,
            f"Rule 9: Prohibitively high CPC bids (${client_cfg.get('max_high_top_of_page_bid', 15.00)}).",
            False,
        )

    if utils.safe_compare(
        keyword_props.get("keyword_difficulty"),
        client_cfg.get("max_kd_hard_limit", 70),
        "gt",
    ):
        return (
            True,
            f"Rule 10: Extreme keyword difficulty (>{client_cfg.get('max_kd_hard_limit', 70)}).",
            False,
        )

    if utils.safe_compare(
        avg_backlinks.get("referring_main_domains"),
        client_cfg.get("max_referring_main_domains_limit", 100),
        "gt",
    ):
        return (
            True,
            f"Rule 11: Overly authoritative competitor domains (>{client_cfg.get('max_referring_main_domains_limit', 100)} referring main domains).",
            False,
        )

    if utils.safe_compare(
        avg_backlinks.get("main_domain_rank"),
        client_cfg.get("max_avg_domain_rank_threshold", 500),
        "lt",
    ):
        return (
            True,
            f"Rule 12: SERP dominated by high-authority domains (avg rank < {client_cfg.get('max_avg_domain_rank_threshold', 500)}).",
            False,
        )

    if (avg_backlinks.get("referring_domains") or 0) > 0:
        pages_to_domain_ratio = (avg_backlinks.get("referring_pages") or 0) / (
            avg_backlinks.get("referring_domains") or 1
        )
        if pages_to_domain_ratio > client_cfg.get("max_pages_to_domain_ratio", 15):
            return (
                True,
                "Rule 13: Potential spammy competitor profile (high page/domain ratio).",
                False,
            )

    # Tier 4: Content, SERP & Keyword Structure

    # Rule: Check for hostile SERP environment
    is_hostile, hostile_reason = _check_hostile_serp_environment(opportunity)
    if is_hostile:
        return True, hostile_reason, True

    non_evergreen_pattern = _get_non_evergreen_year_pattern()
    if non_evergreen_pattern and re.search(non_evergreen_pattern, keyword):
        return (
            True,
            "Rule 14: Non-evergreen temporal keyword (matches pattern for past/current years).",
            False,
        )

    word_count = len(keyword.split())
    is_question = utils.is_question_keyword(keyword)  # This now exists

    min_wc = client_cfg.get("min_keyword_word_count", 2)
    max_wc = client_cfg.get("max_keyword_word_count", 8)

    is_outside_range = word_count < min_wc or word_count > max_wc

    # Rule 15 (Refined with override): Check word count and potentially override for high-value keywords
    if is_outside_range and not is_question:
        sv = keyword_info.get("search_volume", 0)
        cpc = keyword_info.get("cpc")  # Get the value, which could be None
        if cpc is None:
            cpc = 0.0  # Default to 0.0 if it's None

        high_sv_override = client_cfg.get("high_value_sv_override_threshold", 10000)
        high_cpc_override = client_cfg.get("high_value_cpc_override_threshold", 5.0)

        if sv >= high_sv_override or cpc >= high_cpc_override:
            logging.getLogger(__name__).info(
                f"Override: High value SV/CPC bypasses word count rule for '{keyword}'."
            )
            pass  # Allow the keyword to proceed
        else:
            return (
                True,
                f"Rule 15: Non-question keyword word count ({word_count}) is outside the acceptable range ({min_wc}-{max_wc} words).",
                False,
            )

    serp_info = opportunity.get("serp_info", {})
    serp_types = set(serp_info.get("serp_item_types", []))

    crowded_features = {
        "video",
        "images",
        "people_also_ask",
        "carousel",
        "featured_snippet",
        "short_videos",
    }
    if len(serp_types.intersection(crowded_features)) > client_cfg.get(
        "crowded_serp_features_threshold", 4
    ):
        return (
            True,
            f"Rule 17: SERP is overly crowded (>{client_cfg.get('crowded_serp_features_threshold', 4)} attention-grabbing features).",
            False,
        )

    # Rule 18: Check for navigational intent safely
    is_navigational = False
    if intent_info:
        if intent_info.get("main_intent") == "navigational":
            is_navigational = True
        else:
            foreign_intent = intent_info.get("foreign_intent")
            if foreign_intent and "navigational" in foreign_intent:
                is_navigational = True
    if is_navigational:
        return True, "Rule 18: Strong navigational intent.", True

    if serp_info.get("last_updated_time") and serp_info.get("previous_updated_time"):
        try:
            last_update = datetime.fromisoformat(
                serp_info["last_updated_time"].replace(" +00:00", "")
            )
            prev_update = datetime.fromisoformat(
                serp_info["previous_updated_time"].replace(" +00:00", "")
            )
            days_between_updates = (last_update - prev_update).days
            if days_between_updates < client_cfg.get("min_serp_stability_days", 14):
                return (
                    True,
                    f"Rule 19: Unstable SERP (updated every {days_between_updates} days).",
                    False,
                )
        except ValueError:
            logging.getLogger(__name__).warning(
                f"Could not parse SERP update times for '{keyword}': {serp_info.get('last_updated_time')}, {serp_info.get('previous_updated_time')}"
            )

    cpc_value = keyword_info.get("cpc")
    if cpc_value is None:
        cpc_value = 0.0
    if (
        intent_info.get("main_intent") in ["commercial", "transactional"]
        and cpc_value == 0
    ):
        return True, "Rule 20: Low-value commercial intent (zero CPC).", False

    return False, None, False


def _check_hostile_serp_environment(
    opportunity: Dict[str, Any],
) -> Tuple[bool, Optional[str]]:
    """
    Rule 16: Disqualifies keywords where the SERP is dominated by features hostile to blog content.
    """
    serp_info = opportunity.get("serp_info", {})
    if not serp_info:
        return False, None  # Cannot analyze if SERP info is missing

    serp_types = set(serp_info.get("serp_item_types", []))

    # Define hostile features based on detailed SERP analysis
    HOSTILE_FEATURES = {
        # Strong transactional/e-commerce intent
        "shopping",
        "popular_products",
        "refine_products",
        "explore_brands",
        # Strong local intent
        "local_pack",
        "map",
        "local_services",
        # Purely transactional/utility intent (Google-owned tools)
        "google_flights",
        "google_hotels",
        "hotels_pack",
        # App-related intent
        "app",
        # Job-seeking intent
        "jobs",
        # Direct utility/tool intent
        "math_solver",
        "currency_box",
        "stocks_box",
    }

    found_hostile_features = serp_types.intersection(HOSTILE_FEATURES)

    if found_hostile_features:
        return (
            True,
            f"Rule 16: SERP is hostile to blog content. Contains dominant non-article features: {', '.join(found_hostile_features)}.",
        )

    return False, None


def _get_non_evergreen_year_pattern() -> str:
    """
    Generates a regex pattern to find past years up to the current year,
    dynamically adjusting to avoid disqualifying valid keywords in the future.
    Example for current year 2024: \b(201\d|202[0-4])\b
    """
    current_year = datetime.now().year

    patterns = []
    # Handle decades before the current one (e.g., 2010s)
    for decade_start in range(2010, (current_year // 10) * 10, 10):
        patterns.append(
            f"{decade_start}|{decade_start + 1}|{decade_start + 2}|{decade_start + 3}|{decade_start + 4}|{decade_start + 5}|{decade_start + 6}|{decade_start + 7}|{decade_start + 8}|{decade_start + 9}"
        )

    # Handle years in the current decade up to the current year
    current_decade_start_year = (current_year // 10) * 10
    current_decade_years = [
        str(year) for year in range(current_decade_start_year, current_year + 1)
    ]
    if current_decade_years:
        patterns.append("|".join(current_decade_years))

    if not patterns:
        return ""  # Should not happen unless current_year is before 2010

    return r"\b(" + "|".join(patterns) + r")\b"
