# FILE: data_mappers/dataforseo_mapper.py

from typing import Dict, Any
import logging
from backend.core.utils import parse_datetime_string  # ADDED IMPORT
import json

logger = logging.getLogger(__name__)


class DataForSEOMapper:
    """
    Provides static methods to sanitize and normalize raw DataForSEO API responses
    immediately after they are received, before they enter the main pipeline.
    Ensures consistent data types and handles common API quirks.
    """

    @staticmethod
    def _sanitize_serp_info(serp_info: Dict[str, Any]) -> Dict[str, Any]:
        """Sanitizes the 'serp_info' object, specifically handling 'se_results_count' and datetimes."""
        if isinstance(serp_info.get("se_results_count"), str):
            try:
                serp_info["se_results_count"] = int(serp_info["se_results_count"])
            except (ValueError, TypeError):
                logger.warning(
                    f"Failed to convert 'se_results_count' (was string) to int. Setting to 0. Raw: {serp_info.get('se_results_count')}"
                )
                serp_info["se_results_count"] = 0

        # Sanitize datetime fields
        serp_info["last_updated_time"] = parse_datetime_string(
            serp_info.get("last_updated_time")
        )
        serp_info["previous_updated_time"] = parse_datetime_string(
            serp_info.get("previous_updated_time")
        )

        return serp_info

    @staticmethod
    def sanitize_keyword_data_item(item: Dict[str, Any]) -> Dict[str, Any]:
        """
        Sanitizes a single keyword data item (e.g., from keyword_ideas, keyword_suggestions, related_keywords).
        Applies cleaning to nested structures like 'keyword_info', 'keyword_properties', 'serp_info'.
        """
        if not isinstance(item, dict):
            logger.warning(
                f"Invalid item type received for sanitization: {type(item)}. Skipping."
            )
            return {}

        sanitized_item = item.copy()

        # Sanitize keyword_info
        if isinstance(sanitized_item.get("keyword_info"), dict):
            # Ensure CPC and Competition are floats, defaulting to 0.0 if missing or None
            sanitized_item["keyword_info"]["cpc"] = float(
                sanitized_item["keyword_info"].get("cpc") or 0.0
            )
            sanitized_item["keyword_info"]["competition"] = float(
                sanitized_item["keyword_info"].get("competition") or 0.0
            )

            # Ensure other numeric fields are handled
            sanitized_item["keyword_info"]["search_volume"] = int(
                sanitized_item["keyword_info"].get("search_volume") or 0
            )
            sanitized_item["keyword_info"]["low_top_of_page_bid"] = float(
                sanitized_item["keyword_info"].get("low_top_of_page_bid") or 0.0
            )
            sanitized_item["keyword_info"]["high_top_of_page_bid"] = float(
                sanitized_item["keyword_info"].get("high_top_of_page_bid") or 0.0
            )

            # Sanitize last_updated_time
            sanitized_item["keyword_info"]["last_updated_time"] = parse_datetime_string(
                sanitized_item["keyword_info"].get("last_updated_time")
            )

            # Ensure monthly_searches are properly parsed if they are raw strings
            if isinstance(sanitized_item["keyword_info"].get("monthly_searches"), str):
                try:
                    sanitized_item["keyword_info"]["monthly_searches"] = json.loads(
                        sanitized_item["keyword_info"]["monthly_searches"]
                    )
                except json.JSONDecodeError:
                    logger.warning(
                        f"Failed to parse monthly_searches JSON string for keyword '{sanitized_item.get('keyword')}'. Resetting."
                    )
                    sanitized_item["keyword_info"]["monthly_searches"] = []

            # Ensure individual monthly_searches items are sanitized for type consistency
            if isinstance(sanitized_item["keyword_info"].get("monthly_searches"), list):
                for month_data in sanitized_item["keyword_info"]["monthly_searches"]:
                    if isinstance(month_data, dict):
                        month_data["year"] = int(month_data.get("year") or 0)
                        month_data["month"] = int(month_data.get("month") or 0)
                        month_data["search_volume"] = int(
                            month_data.get("search_volume") or 0
                        )

        # Sanitize keyword_properties
        if isinstance(sanitized_item.get("keyword_properties"), dict):
            sanitized_item["keyword_properties"]["keyword_difficulty"] = int(
                sanitized_item["keyword_properties"].get("keyword_difficulty") or 0
            )

        # Sanitize search_intent_info
        if isinstance(sanitized_item.get("search_intent_info"), dict):
            sanitized_item["search_intent_info"]["foreign_intent"] = (
                sanitized_item["search_intent_info"].get("foreign_intent") or []
            )
            sanitized_item["search_intent_info"]["last_updated_time"] = (
                parse_datetime_string(
                    sanitized_item["search_intent_info"].get("last_updated_time")
                )
            )

        # Sanitize serp_info (crucial for se_results_count string/int issue)
        if isinstance(sanitized_item.get("serp_info"), dict):
            sanitized_item["serp_info"] = DataForSEOMapper._sanitize_serp_info(
                sanitized_item["serp_info"]
            )
            sanitized_item["serp_info"]["serp_item_types"] = (
                sanitized_item["serp_info"].get("serp_item_types") or []
            )

        # Sanitize avg_backlinks_info
        if isinstance(sanitized_item.get("avg_backlinks_info"), dict):
            for key in [
                "backlinks",
                "dofollow",
                "referring_pages",
                "referring_domains",
                "referring_main_domains",
                "rank",
                "main_domain_rank",
            ]:
                sanitized_item["avg_backlinks_info"][key] = float(
                    sanitized_item["avg_backlinks_info"].get(key) or 0.0
                )
            sanitized_item["avg_backlinks_info"]["last_updated_time"] = (
                parse_datetime_string(
                    sanitized_item["avg_backlinks_info"].get("last_updated_time")
                )
            )

        # Keyword Info Normalized with Bing
        for normalized_key in [
            "keyword_info_normalized_with_bing",
            "keyword_info_normalized_with_clickstream",
        ]:
            if isinstance(sanitized_item.get(normalized_key), dict):
                normalized_data = sanitized_item[normalized_key]
                normalized_data["search_volume"] = int(
                    normalized_data.get("search_volume") or 0
                )
                normalized_data["last_updated_time"] = parse_datetime_string(
                    normalized_data.get("last_updated_time")
                )
                if isinstance(normalized_data.get("monthly_searches"), list):
                    for month_data in normalized_data["monthly_searches"]:
                        if isinstance(month_data, dict):
                            month_data["year"] = int(month_data.get("year") or 0)
                            month_data["month"] = int(month_data.get("month") or 0)
                            month_data["search_volume"] = int(
                                month_data.get("search_volume") or 0
                            )

        return sanitized_item

    @staticmethod
    def sanitize_serp_overview_response(serp_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Sanitizes a full SERP overview response from FullSerpAnalyzer.analyze_serp.
        Ensures consistent types for nested items, especially 'pixel_rank_data' and 'top_organic_results'.
        """
        sanitized_serp_data = serp_data.copy()

        # Sanitize top-level date/time fields
        sanitized_serp_data["datetime"] = parse_datetime_string(
            sanitized_serp_data.get("datetime")
        )
        sanitized_serp_data["last_updated_time"] = parse_datetime_string(
            sanitized_serp_data.get("last_updated_time")
        )
        sanitized_serp_data["previous_updated_time"] = parse_datetime_string(
            sanitized_serp_data.get("previous_updated_time")
        )

        # Sanitize pixel_rank_data
        if isinstance(sanitized_serp_data.get("raw_pixel_ranking_data"), list):
            for item in sanitized_serp_data["raw_pixel_ranking_data"]:
                if isinstance(item.get("rectangle"), dict):
                    item["rectangle"]["x"] = float(item["rectangle"].get("x") or 0.0)
                    item["rectangle"]["y"] = float(item["rectangle"].get("y") or 0.0)
                    item["rectangle"]["width"] = float(
                        item["rectangle"].get("width") or 0.0
                    )
                    item["rectangle"]["height"] = float(
                        item["rectangle"].get("height") or 0.0
                    )
                item["rank_absolute"] = int(item.get("rank_absolute") or 0)
                item["rank_group"] = int(item.get("rank_group") or 0)

        if sanitized_serp_data.get("first_organic_y_pixel") is not None:
            sanitized_serp_data["first_organic_y_pixel"] = float(
                sanitized_serp_data["first_organic_y_pixel"]
            )

        # Sanitize top_organic_results
        if isinstance(sanitized_serp_data.get("top_organic_results"), list):
            for result in sanitized_serp_data["top_organic_results"]:
                result["rank"] = int(result.get("rank") or 0)
                if isinstance(result.get("rating"), dict):
                    result["rating"]["value"] = float(
                        result["rating"].get("value") or 0.0
                    )
                    result["rating"]["votes_count"] = int(
                        result["rating"].get("votes_count") or 0
                    )
                    result["rating"]["rating_max"] = int(
                        result["rating"].get("rating_max") or 0
                    )

                # Ensure about_this_result_search_terms and related_terms are lists
                result["about_this_result_search_terms"] = (
                    result.get("about_this_result_search_terms") or []
                )
                result["about_this_result_related_terms"] = (
                    result.get("about_this_result_related_terms") or []
                )

        sanitized_serp_data["people_also_ask"] = (
            sanitized_serp_data.get("people_also_ask") or []
        )
        sanitized_serp_data["related_searches"] = (
            sanitized_serp_data.get("related_searches") or []
        )
        sanitized_serp_data["extracted_serp_features"] = (
            sanitized_serp_data.get("extracted_serp_features") or []
        )

        if isinstance(sanitized_serp_data.get("ai_overview_items"), list):
            for ai_item in sanitized_serp_data["ai_overview_items"]:
                ai_item["rank_group"] = int(ai_item.get("rank_group") or 0)
                ai_item["rank_absolute"] = int(ai_item.get("rank_absolute") or 0)
                if isinstance(ai_item.get("references"), list):
                    for ref in ai_item["references"]:
                        ref["date"] = parse_datetime_string(ref.get("date"))
                        ref["timestamp"] = parse_datetime_string(ref.get("timestamp"))
                if isinstance(ai_item.get("table"), dict):
                    if not isinstance(ai_item["table"].get("table_header"), list):
                        ai_item["table"]["table_header"] = []
                    if not isinstance(ai_item["table"].get("table_content"), list):
                        ai_item["table"]["table_content"] = []

        return sanitized_serp_data

    @staticmethod
    def sanitize_onpage_data_item(item: Dict[str, Any]) -> Dict[str, Any]:
        """
        Sanitizes a single OnPage API response item from `get_onpage_data_for_urls`.
        Ensures consistent data types for numeric fields, especially in 'meta' and 'page_timing'.
        """
        sanitized_item = item.copy()

        # Sanitize meta fields
        meta = sanitized_item.get("meta", {})
        if isinstance(meta, dict):
            meta["charset"] = int(meta.get("charset") or 0)
            meta["internal_links_count"] = int(meta.get("internal_links_count") or 0)
            meta["external_links_count"] = int(meta.get("external_links_count") or 0)
            meta["inbound_links_count"] = int(meta.get("inbound_links_count") or 0)
            meta["images_count"] = int(meta.get("images_count") or 0)
            meta["images_size"] = int(meta.get("images_size") or 0)
            meta["scripts_count"] = int(meta.get("scripts_count") or 0)
            meta["scripts_size"] = int(meta.get("scripts_size") or 0)
            meta["stylesheets_count"] = int(meta.get("stylesheets_count") or 0)
            meta["stylesheets_size"] = int(meta.get("stylesheets_size") or 0)
            meta["title_length"] = int(meta.get("title_length") or 0)
            meta["description_length"] = int(meta.get("description_length") or 0)
            meta["render_blocking_scripts_count"] = int(
                meta.get("render_blocking_scripts_count") or 0
            )
            meta["render_blocking_stylesheets_count"] = int(
                meta.get("render_blocking_stylesheets_count") or 0
            )
            meta["cumulative_layout_shift"] = float(
                meta.get("cumulative_layout_shift") or 0.0
            )

            # Sanitize date/time fields
            meta["last_updated_time"] = parse_datetime_string(
                meta.get("last_updated_time")
            )

            content_meta = meta.get("content", {})
            if isinstance(content_meta, dict):
                content_meta["plain_text_size"] = int(
                    content_meta.get("plain_text_size") or 0
                )
                content_meta["plain_text_rate"] = float(
                    content_meta.get("plain_text_rate") or 0.0
                )
                content_meta["plain_text_word_count"] = int(
                    content_meta.get("plain_text_word_count") or 0
                )
                content_meta["automated_readability_index"] = float(
                    content_meta.get("automated_readability_index") or 0.0
                )
                content_meta["coleman_liau_readability_index"] = float(
                    content_meta.get("coleman_liau_readability_index") or 0.0
                )
                content_meta["dale_chall_readability_index"] = float(
                    content_meta.get("dale_chall_readability_index") or 0.0
                )
                content_meta["flesch_kincaid_readability_index"] = float(
                    content_meta.get("flesch_kincaid_readability_index") or 0.0
                )
                content_meta["smog_readability_index"] = float(
                    content_meta.get("smog_readability_index") or 0.0
                )
                content_meta["description_to_content_consistency"] = float(
                    content_meta.get("description_to_content_consistency") or 0.0
                )
                content_meta["title_to_content_consistency"] = float(
                    content_meta.get("title_to_content_consistency") or 0.0
                )
                content_meta["meta_keywords_to_content_consistency"] = float(
                    content_meta.get("meta_keywords_to_content_consistency") or 0.0
                )
            sanitized_item["meta"] = meta

        # Sanitize page_timing fields
        page_timing = sanitized_item.get("page_timing", {})
        if isinstance(page_timing, dict):
            page_timing["time_to_interactive"] = int(
                page_timing.get("time_to_interactive") or 0
            )
            page_timing["dom_complete"] = int(page_timing.get("dom_complete") or 0)
            page_timing["largest_contentful_paint"] = float(
                page_timing.get("largest_contentful_paint") or 0.0
            )
            page_timing["first_input_delay"] = float(
                page_timing.get("first_input_delay") or 0.0
            )
            page_timing["connection_time"] = int(
                page_timing.get("connection_time") or 0
            )
            page_timing["time_to_secure_connection"] = int(
                page_timing.get("time_to_secure_connection") or 0
            )
            page_timing["request_sent_time"] = int(
                page_timing.get("request_sent_time") or 0
            )
            page_timing["waiting_time"] = int(page_timing.get("waiting_time") or 0)
            page_timing["download_time"] = int(page_timing.get("download_time") or 0)
            page_timing["duration_time"] = int(page_timing.get("duration_time") or 0)
            page_timing["fetch_start"] = int(page_timing.get("fetch_start") or 0)
            page_timing["fetch_end"] = int(page_timing.get("fetch_end") or 0)
            sanitized_item["page_timing"] = page_timing

        # Sanitize top-level numeric fields
        sanitized_item["onpage_score"] = float(
            sanitized_item.get("onpage_score") or 0.0
        )
        sanitized_item["total_dom_size"] = int(
            sanitized_item.get("total_dom_size") or 0
        )
        sanitized_item["size"] = int(sanitized_item.get("size") or 0)
        sanitized_item["encoded_size"] = int(sanitized_item.get("encoded_size") or 0)
        sanitized_item["total_transfer_size"] = int(
            sanitized_item.get("total_transfer_size") or 0
        )
        sanitized_item["url_length"] = int(sanitized_item.get("url_length") or 0)
        sanitized_item["relative_url_length"] = int(
            sanitized_item.get("relative_url_length") or 0
        )

        # Sanitize fetch_time
        sanitized_item["fetch_time"] = parse_datetime_string(
            sanitized_item.get("fetch_time")
        )

        # Sanitize cache_control ttl
        if isinstance(sanitized_item.get("cache_control"), dict):
            sanitized_item["cache_control"]["ttl"] = int(
                sanitized_item["cache_control"].get("ttl") or 0
            )

        # Sanitize last_modified dates
        if isinstance(sanitized_item.get("last_modified"), dict):
            sanitized_item["last_modified"]["header"] = parse_datetime_string(
                sanitized_item["last_modified"].get("header")
            )
            sanitized_item["last_modified"]["sitemap"] = parse_datetime_string(
                sanitized_item["last_modified"].get("sitemap")
            )
            sanitized_item["last_modified"]["meta_tag"] = parse_datetime_string(
                sanitized_item["last_modified"].get("meta_tag")
            )

        return sanitized_item
