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
    Per API docs: "note that you can not filter the results by `relevance`"
    """
    if not filters:
        return []
    
    sanitized = []
    removed_count = 0
    
    for item in filters:
        if isinstance(item, list) and len(item) >= 1 and isinstance(item[0], str):
            field_path = item[0].lower()
            
            # Check against forbidden fields
            if any(forbidden in field_path for forbidden in FORBIDDEN_API_FILTER_FIELDS):
                logger.warning(
                    f"Forbidden field '{field_path}' detected in API filter. Removing it."
                )
                removed_count += 1
                continue
        
        sanitized.append(item)
    
    # Clean up trailing logical operators if filters were removed
    if sanitized and isinstance(sanitized[-1], str) and sanitized[-1].lower() in ["and", "or"]:
        sanitized.pop()
    
    # Clean up leading logical operators
    if sanitized and isinstance(sanitized[0], str) and sanitized[0].lower() in ["and", "or"]:
        sanitized.pop(0)
    
    if removed_count > 0:
        logger.info(f"Removed {removed_count} forbidden filter(s) from API request")
    
    return sanitized


def build_discovery_filters(config: Dict[str, Any]) -> Tuple[List[Any], List[Any]]:
    """
    Builds filter lists for API-side filtering for KD, SV, Competition, and Intent.
    Returns (filters_for_ideas_and_suggestions, filters_for_related_keywords)
    
    CRITICAL: Related Keywords requires 'keyword_data.' prefix for ALL fields per API docs.
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
                ["keyword_data.keyword_info.competition_level", "in", allowed_comp_levels],
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

    # REMOVED: closely_variants from filters - it's a top-level parameter, not a filter
    # It will be handled in Task 2.6

    # CPC Range Filters
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

    # Competition Range Filters
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

    # Max Competition Level Filter
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

    # Regex Filter
    search_phrase_regex = config.get("search_phrase_regex")
    if search_phrase_regex and search_phrase_regex.strip():
        # Validate regex length (max 1000 chars per API docs)
        if len(search_phrase_regex) > 1000:
            logger.warning(
                f"Regex pattern exceeds 1000 character limit ({len(search_phrase_regex)} chars). Truncating."
            )
            search_phrase_regex = search_phrase_regex[:1000]
        
        std_api_filters.extend([["keyword", "regex", search_phrase_regex], "and"])
        rel_api_filters.extend(
            [["keyword_data.keyword", "regex", search_phrase_regex], "and"]
        )

    # Remove trailing "and" operators
    if std_api_filters and std_api_filters[-1] == "and":
        std_api_filters.pop()
    if rel_api_filters and rel_api_filters[-1] == "and":
        rel_api_filters.pop()

    # Apply sanitation
    std_api_filters = sanitize_filters_for_api(std_api_filters)
    rel_api_filters = sanitize_filters_for_api(rel_api_filters)

    logger.info(f"Built standard API filters: {json.dumps(std_api_filters)}")
    logger.info(f"Built related API filters: {json.dumps(rel_api_filters)}")

    return std_api_filters, rel_api_filters
