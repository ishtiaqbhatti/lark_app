# pipeline/step_01_discovery/keyword_discovery/filters.py
import json
import logging
from typing import List, Any, Tuple, Dict

logger = logging.getLogger(__name__)

FORBIDDEN_API_FILTER_FIELDS = [
    "relevance",
    "sv_bing",
    "sv_clickstream",
]  # Define forbidden fields


def sanitize_filters_for_api(filters: List[Any]) -> List[Any]:
    """
    Removes any filters attempting to use forbidden internal metrics or data sources.
    """
    sanitized = []
    for item in filters:
        if isinstance(item, list) and len(item) >= 1 and isinstance(item[0], str):
            field_path = item[0].lower()
            if any(
                forbidden in field_path for forbidden in FORBIDDEN_API_FILTER_FIELDS
            ):
                logger.warning(
                    f"Forbidden field '{field_path}' detected in API filter. Removing it."
                )
                continue
        sanitized.append(item)
    return sanitized


def add_serp_feature_filters(config: Dict[str, Any], std_api_filters: List[Any], rel_api_filters: List[Any]):
    """Adds SERP feature filters to the standard and related filters lists."""
    required_serp_features = config.get("required_serp_features")
    if required_serp_features:
        for feature in required_serp_features:
            std_api_filters.extend([["serp_info.serp_item_types", "in", [feature]], "and"])
            rel_api_filters.extend([["keyword_data.serp_info.serp_item_types", "in", [feature]], "and"])

    excluded_serp_features = config.get("excluded_serp_features")
    if excluded_serp_features:
        for feature in excluded_serp_features:
            std_api_filters.extend([["serp_info.serp_item_types", "not_in", [feature]], "and"])
            rel_api_filters.extend([["keyword_data.serp_info.serp_item_types", "not_in", [feature]], "and"])


def build_discovery_filters(config: Dict[str, Any]) -> Tuple[List[Any], List[Any]]:
    """
    Builds filter lists for API-side filtering for KD, SV, Competition, and Intent.
    """
    std_api_filters = []
    rel_api_filters = []

    min_sv = config.get("min_search_volume")
    if min_sv is not None:
        std_api_filters.extend([["keyword_info.search_volume", ">=", min_sv], "and"])
        rel_api_filters.extend(
            [["keyword_data.keyword_info.search_volume", ">=", min_sv], "and"]
        )

    max_kd = config.get("max_keyword_difficulty")
    if max_kd is not None:
        std_api_filters.extend(
            [["keyword_properties.keyword_difficulty", "<=", max_kd], "and"]
        )
        rel_api_filters.extend(
            [
                ["keyword_data.keyword_properties.keyword_difficulty", "<=", max_kd],
                "and",
            ]
        )

    allowed_comp_levels = config.get("allowed_competition_levels")
    if allowed_comp_levels:
        std_api_filters.extend(
            [["keyword_info.competition_level", "in", allowed_comp_levels], "and"]
        )
        rel_api_filters.extend(
            [
                [
                    "keyword_data.keyword_info.competition_level",
                    "in",
                    allowed_comp_levels,
                ],
                "and",
            ]
        )

    allowed_intents = config.get("allowed_intents")
    if config.get("enforce_intent_filter", False) and allowed_intents:
        std_api_filters.extend(
            [["search_intent_info.main_intent", "in", allowed_intents], "and"]
        )
        rel_api_filters.extend(
            [
                ["keyword_data.search_intent_info.main_intent", "in", allowed_intents],
                "and",
            ]
        )

    # NEW: Closely Variants
    closely_variants = config.get("closely_variants")
    if closely_variants is not None:
        std_api_filters.extend(
            [["closely_variants", "=", closely_variants], "and"]
        )  # This param is at top level
        # Related keywords endpoint does not have closely_variants

    # NEW: CPC Range Filters
    min_cpc_filter = config.get("min_cpc_filter")
    max_cpc_filter = config.get("max_cpc_filter")
    if min_cpc_filter is not None:
        std_api_filters.extend([["keyword_info.cpc", ">=", min_cpc_filter], "and"])
        rel_api_filters.extend(
            [["keyword_data.keyword_info.cpc", ">=", min_cpc_filter], "and"]
        )
    if max_cpc_filter is not None:
        std_api_filters.extend([["keyword_info.cpc", "<=", max_cpc_filter], "and"])
        rel_api_filters.extend(
            [["keyword_data.keyword_info.cpc", "<=", max_cpc_filter], "and"]
        )

    # NEW: Competition Range Filters
    min_competition = config.get("min_competition")
    max_competition = config.get("max_competition")
    if min_competition is not None:
        std_api_filters.extend(
            [["keyword_info.competition", ">=", min_competition], "and"]
        )
        rel_api_filters.extend(
            [["keyword_data.keyword_info.competition", ">=", min_competition], "and"]
        )
    if max_competition is not None:
        std_api_filters.extend(
            [["keyword_info.competition", "<=", max_competition], "and"]
        )
        rel_api_filters.extend(
            [["keyword_data.keyword_info.competition", "<=", max_competition], "and"]
        )

    # NEW: Max Competition Level Filter
    max_competition_level = config.get("max_competition_level")
    if max_competition_level:
        levels = ["LOW", "MEDIUM", "HIGH"]
        allowed_levels = levels[: levels.index(max_competition_level) + 1]
        std_api_filters.extend(
            [["keyword_info.competition_level", "in", allowed_levels], "and"]
        )
        rel_api_filters.extend(
            [
                ["keyword_data.keyword_info.competition_level", "in", allowed_levels],
                "and",
            ]
        )

    # NEW: Regex Filter (from Task 34)
    search_phrase_regex = config.get("search_phrase_regex")
    if search_phrase_regex and search_phrase_regex.strip():
        std_api_filters.extend([["keyword", "regex", search_phrase_regex], "and"])
        rel_api_filters.extend(
            [["keyword_data.keyword", "regex", search_phrase_regex], "and"]
        )

    add_serp_feature_filters(config, std_api_filters, rel_api_filters)

    if std_api_filters:
        std_api_filters.pop()
    if rel_api_filters:
        rel_api_filters.pop()

    # Apply sanitation (Weakness 3.7 Fix)
    std_api_filters = sanitize_filters_for_api(std_api_filters)
    rel_api_filters = sanitize_filters_for_api(rel_api_filters)

    logger.info(f"Built standard API filters: {json.dumps(std_api_filters)}")
    logger.info(f"Built related API filters: {json.dumps(rel_api_filters)}")

    return std_api_filters, rel_api_filters

