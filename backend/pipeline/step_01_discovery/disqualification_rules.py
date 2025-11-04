# pipeline/step_01_discovery/disqualification_rules.py
import logging
import re
from typing import Dict, Any, Tuple, Optional
from datetime import datetime
import numpy as np
from core import utils
from core.utils import get_reliable_search_volume, detect_seasonal_pattern
from core.discovery_defaults import DISCOVERY_DEFAULTS, HOSTILE_SERP_FEATURES

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

    # New Rule: Reject if SV or KD data is missing (null)
    # Use reliable search volume from clickstream data when available
    search_volume = get_reliable_search_volume(opportunity)
    keyword_difficulty = keyword_props.get("keyword_difficulty")

    # A search volume of 0 is a valid reason to disqualify based on client strategy.
    if search_volume is None or search_volume == 0:
        return True, "Rule 0: Rejected due to zero or null Search Volume.", True
    
    # A keyword difficulty of 0 is a valid, desirable metric. Only reject if data is missing.
    if keyword_difficulty is None:
        return True, "Rule 0: Rejected due to null Keyword Difficulty.", True

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
    min_sv = client_cfg.get("min_search_volume", DISCOVERY_DEFAULTS["MIN_SEARCH_VOLUME"])
    if utils.safe_compare(search_volume, min_sv, "lt"):
        return (
            True,
            f"Rule 5: Below search volume floor (minimum: {min_sv} SV). Current: {search_volume} SV.",
            False,
        )

    trends = opportunity.get("keyword_info", {}).get("search_volume_trend", {})
    if trends:
        if not isinstance(trends, dict):
            logging.getLogger(__name__).warning(
                f"Skipping trend analysis for keyword '{keyword}' due to unexpected data type for trends: {type(trends)}"
            )
            return False, None, False
        try:
            yearly_trend = trends.get("yearly") if trends.get("yearly") is not None else 0
            quarterly_trend = trends.get("quarterly") if trends.get("quarterly") is not None else 0

            yearly_threshold = client_cfg.get(
                "yearly_trend_decline_threshold", 
                DISCOVERY_DEFAULTS["YEARLY_TREND_DECLINE_THRESHOLD"]
            )
            quarterly_threshold = client_cfg.get(
                "quarterly_trend_decline_threshold", 
                DISCOVERY_DEFAULTS["QUARTERLY_TREND_DECLINE_THRESHOLD"]
            )

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
                "search_volume_volatility_threshold", 
                DISCOVERY_DEFAULTS["SEARCH_VOLUME_VOLATILITY_THRESHOLD"]
            )
            std_dev_to_mean_ratio = np.std(volumes) / np.mean(volumes)
            if std_dev_to_mean_ratio > volatility_threshold:
                return (
                    True,
                    f"Rule 7: Extreme search volume volatility. Std Dev / Mean ratio: {std_dev_to_mean_ratio:.2f} (above {volatility_threshold} threshold). Could indicate a fleeting trend or strong seasonality. Manual review recommended.",
                    False,
                )

    # Rule 7b: Check for recent sharp decline using raw monthly searches
    # BUT: Skip this check if keyword shows seasonal pattern
    monthly_searches_from_keyword_info = keyword_info.get("monthly_searches", [])
    seasonality_data = detect_seasonal_pattern(monthly_searches_from_keyword_info)
    
    # Store seasonality data for later use in scoring
    opportunity["seasonality_analysis"] = seasonality_data
    
    if not seasonality_data.get("is_seasonal", False):
        # Only check for decline if NOT seasonal
        if monthly_searches_from_keyword_info and len(monthly_searches_from_keyword_info) >= 4:
            try:
                sorted_searches = sorted(
                    monthly_searches_from_keyword_info, 
                    key=lambda x: (x["year"], x["month"]), 
                    reverse=True
                )
                if len(sorted_searches) >= 4:
                    latest_vol = sorted_searches[0].get("search_volume")
                    past_vol = sorted_searches[3].get("search_volume")

                    if latest_vol is not None and past_vol is not None and past_vol > 0:
                        if (latest_vol / past_vol) < 0.5:
                            return (
                                True,
                                "Rule 7b: Recent sharp decline in search volume (>50% drop in last 3 months). Not seasonal pattern.",
                                False,
                            )
            except (TypeError, KeyError):
                logging.getLogger(__name__).warning(
                    f"Could not parse monthly_searches for recent trend analysis on keyword '{keyword}'."
                )
    else:
        logging.getLogger(__name__).info(
            f"Skipping decline check for '{keyword}' - detected {seasonality_data.get('pattern_type')} pattern "
            f"(peak in month {seasonality_data.get('peak_month')}, factor: {seasonality_data.get('seasonality_factor')})"
        )

    # Tier 3: Commercial & Competitive Analysis
    max_competition = client_cfg.get(
        "max_paid_competition_score", 
        DISCOVERY_DEFAULTS["MAX_PAID_COMPETITION_SCORE"]
    )
    if utils.safe_compare(
        keyword_info.get("competition"),
        max_competition,
        "gt",
    ) and (keyword_info.get("competition_level") == "HIGH"):
        return True, "Rule 8: Excessive paid competition.", False

    max_cpc = client_cfg.get(
        "max_high_top_of_page_bid", 
        DISCOVERY_DEFAULTS["MAX_HIGH_TOP_OF_PAGE_BID"]
    )
    if utils.safe_compare(
        keyword_info.get("high_top_of_page_bid"),
        max_cpc,
        "gt",
    ):
        return (
            True,
            f"Rule 9: Prohibitively high CPC bids (>${max_cpc:.2f}).",
            False,
        )

    max_kd = client_cfg.get("max_kd_hard_limit", DISCOVERY_DEFAULTS["MAX_KD_HARD_LIMIT"])
    if utils.safe_compare(
        keyword_props.get("keyword_difficulty"),
        max_kd,
        "gt",
    ):
        return (
            True,
            f"Rule 10: Extreme keyword difficulty (>{max_kd}).",
            False,
        )

    max_ref_domains = client_cfg.get(
        "max_referring_main_domains_limit", 
        DISCOVERY_DEFAULTS["MAX_REFERRING_MAIN_DOMAINS_LIMIT"]
    )
    if utils.safe_compare(
        avg_backlinks.get("referring_main_domains"),
        max_ref_domains,
        "gt",
    ):
        return (
            True,
            f"Rule 11: Overly authoritative competitor domains (>{max_ref_domains} referring main domains).",
            False,
        )

    max_domain_rank = client_cfg.get(
        "max_avg_domain_rank_threshold", 
        DISCOVERY_DEFAULTS["MAX_AVG_DOMAIN_RANK_THRESHOLD"]
    )
    if utils.safe_compare(
        avg_backlinks.get("main_domain_rank"),
        max_domain_rank,
        "lt",
    ):
        return (
            True,
            f"Rule 12: SERP dominated by high-authority domains (avg rank < {max_domain_rank}).",
            False,
        )

    if (avg_backlinks.get("referring_domains") or 0) > 0:
        pages_to_domain_ratio = (avg_backlinks.get("referring_pages") or 0) / (
            avg_backlinks.get("referring_domains") or 1
        )
        max_ratio = client_cfg.get(
            "max_pages_to_domain_ratio", 
            DISCOVERY_DEFAULTS["MAX_PAGES_TO_DOMAIN_RATIO"]
        )
        if pages_to_domain_ratio > max_ratio:
            return (
                True,
                f"Rule 13: Potential spammy competitor profile (page/domain ratio: {pages_to_domain_ratio:.1f} > {max_ratio}).",
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
    is_question = utils.is_question_keyword(keyword)

    min_wc = client_cfg.get("min_keyword_word_count", DISCOVERY_DEFAULTS["MIN_KEYWORD_WORD_COUNT"])
    max_wc = client_cfg.get("max_keyword_word_count", DISCOVERY_DEFAULTS["MAX_KEYWORD_WORD_COUNT"])

    is_outside_range = word_count < min_wc or word_count > max_wc

    # Rule 15 (Refined with override): Check word count and potentially override for high-value keywords
    if is_outside_range and not is_question:
        sv = search_volume  # Use reliable search volume from earlier
        cpc = keyword_info.get("cpc")
        if cpc is None:
            cpc = 0.0

        high_sv_override = client_cfg.get(
            "high_value_sv_override_threshold", 
            DISCOVERY_DEFAULTS["HIGH_VALUE_SV_OVERRIDE"]
        )
        high_cpc_override = client_cfg.get(
            "high_value_cpc_override_threshold", 
            DISCOVERY_DEFAULTS["HIGH_VALUE_CPC_OVERRIDE"]
        )
        
        # NEW: Long-tail keyword exception (5+ words get special treatment)
        long_tail_threshold = client_cfg.get(
            "long_tail_word_count_threshold", 
            DISCOVERY_DEFAULTS["LONG_TAIL_WORD_COUNT_THRESHOLD"]
        )
        is_long_tail = word_count >= long_tail_threshold
        
        # Long-tail keywords get lower KD tolerance and are valuable even with lower SV
        if is_long_tail:
            kd = keyword_props.get("keyword_difficulty", 100)
            long_tail_kd_max = client_cfg.get(
                "long_tail_kd_threshold", 
                DISCOVERY_DEFAULTS["LONG_TAIL_KD_THRESHOLD"]
            )
            long_tail_min_sv = client_cfg.get(
                "long_tail_min_search_volume", 
                DISCOVERY_DEFAULTS["LONG_TAIL_MIN_SEARCH_VOLUME"]
            )
            if kd <= long_tail_kd_max and sv >= long_tail_min_sv:
                logging.getLogger(__name__).info(
                    f"Override: Long-tail keyword ({word_count} words, KD={kd}) with low competition bypasses word count rule for '{keyword}'."
                )
                # Store this as a "long_tail_opportunity" flag for scoring
                opportunity["is_long_tail_opportunity"] = True
                pass  # Allow the keyword to proceed
            elif sv >= high_sv_override or cpc >= high_cpc_override:
                logging.getLogger(__name__).info(
                    f"Override: High value long-tail keyword bypasses word count rule for '{keyword}'."
                )
                pass
            else:
                return (
                    True,
                    f"Rule 15: Long-tail keyword ({word_count} words) has insufficient value (SV={sv}, KD={kd}).",
                    False,
                )
        elif sv >= high_sv_override or cpc >= high_cpc_override:
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

    from core.discovery_defaults import ATTENTION_COMPETING_FEATURES
    
    crowded_threshold = client_cfg.get(
        "crowded_serp_features_threshold", 
        DISCOVERY_DEFAULTS["CROWDED_SERP_FEATURES_THRESHOLD"]
    )
    if len(serp_types.intersection(ATTENTION_COMPETING_FEATURES)) > crowded_threshold:
        return (
            True,
            f"Rule 17: SERP is overly crowded (>{crowded_threshold} attention-grabbing features).",
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

    # NEW: Check SERP data freshness before stability check
    if serp_info.get("last_updated_time"):
        try:
            last_update = datetime.fromisoformat(
                serp_info["last_updated_time"].replace(" +00:00", "")
            )
            serp_age_days = (datetime.now() - last_update).days
            
            # Flag stale data but don't disqualify (add to opportunity metadata)
            if serp_age_days > 90:  # 3+ months old
                opportunity["serp_data_quality_warning"] = f"SERP data is {serp_age_days} days old (stale)"
                logging.getLogger(__name__).warning(
                    f"Stale SERP data for '{keyword}': {serp_age_days} days old. Consider manual review for fast-changing topics."
                )
            
            # Original stability check
            if serp_info.get("previous_updated_time"):
                prev_update = datetime.fromisoformat(
                    serp_info["previous_updated_time"].replace(" +00:00", "")
                )
                days_between_updates = (last_update - prev_update).days
                min_stability = client_cfg.get(
                    "min_serp_stability_days", 
                    DISCOVERY_DEFAULTS["MIN_SERP_STABILITY_DAYS"]
                )
                if days_between_updates < min_stability:
                    return (
                        True,
                        f"Rule 19: Unstable SERP (updated every {days_between_updates} days, minimum: {min_stability}).",
                        False,
                    )
        except ValueError:
            logging.getLogger(__name__).warning(
                f"Could not parse SERP update times for '{keyword}': {serp_info.get('last_updated_time')}, {serp_info.get('previous_updated_time')}"
            )
        except Exception as e:
            logging.getLogger(__name__).error(
                f"Unexpected error checking SERP freshness for '{keyword}': {str(e)}"
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
    Rule 16: Disqualifies keywords where the SERP is COMPLETELY dominated by features 
    hostile to blog content, with NO organic results present.
    
    Updated logic: Only reject if hostile features exist AND there are few/no organic results.
    This prevents false rejections of keywords where blogs can still rank alongside features.
    """
    serp_info = opportunity.get("serp_info", {})
    if not serp_info:
        return False, None  # Cannot analyze if SERP info is missing

    serp_types = set(serp_info.get("serp_item_types", []))

    # Use centralized hostile features definition
    found_hostile_features = serp_types.intersection(HOSTILE_SERP_FEATURES)

    # NEW LOGIC: Check if organic results are present
    has_organic = "organic" in serp_types
    hostile_count = len(found_hostile_features)
    
    # Only reject if BOTH conditions are true:
    # 1. Multiple hostile features present (configurable threshold)
    # 2. No organic results OR very few organic signals
    hostile_threshold = DISCOVERY_DEFAULTS["HOSTILE_SERP_FEATURE_COUNT_THRESHOLD"]
    if hostile_count >= hostile_threshold and not has_organic:
        return (
            True,
            f"Rule 16: SERP is completely hostile to blog content. Contains {hostile_count} dominant non-article features ({', '.join(found_hostile_features)}) with NO organic results.",
        )
    
    # If hostile features exist but organic results also present, issue warning but don't reject
    if hostile_count >= 2 and has_organic:
        logging.getLogger(__name__).info(
            f"SERP has {hostile_count} competing features but organic results present: {', '.join(found_hostile_features)}"
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
