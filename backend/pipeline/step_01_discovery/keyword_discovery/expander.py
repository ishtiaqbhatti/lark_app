# pipeline/step_01_discovery/keyword_discovery/expander.py
import logging
from typing import List, Dict, Any, Optional

from external_apis.dataforseo_client_v2 import DataForSEOClientV2


class NewKeywordExpander:
    def __init__(
        self,
        client: DataForSEOClientV2,
        config: Dict[str, Any],
        logger: Optional[logging.Logger] = None,
    ):
        self.client = client
        self.config = config
        self.logger = logger or logging.getLogger(self.__class__.__name__)

    def expand(
        self,
        seed_keywords: List[str],
        discovery_modes: List[str],
        filters: Optional[List[Any]],
        order_by: Optional[List[str]],
        existing_keywords: set,
        limit: Optional[int] = None,
        depth: Optional[int] = None,
        ignore_synonyms: Optional[bool] = False,
        discovery_max_pages: Optional[int] = None,
    ) -> Dict[str, Any]:
        if not discovery_modes:
            raise ValueError("At least one discovery mode must be selected.")

        # Filter out seed keywords that already exist
        original_seed_count = len(seed_keywords)
        seed_keywords = [
            kw for kw in seed_keywords if kw.lower() not in existing_keywords
        ]
        if not seed_keywords:
            self.logger.info(
                "All seed keywords already exist in the database. Skipping expansion."
            )
            return {
                "total_cost": 0.0,
                "raw_counts": {},
                "total_raw_count": 0,
                "total_unique_count": 0,
                "final_keywords": [],
            }
        self.logger.info(
            f"Filtered seed keywords from {original_seed_count} to {len(seed_keywords)}."
        )

        location_code = self.config.get("location_code")
        language_code = self.config.get("language_code")
        if not location_code or not language_code:
            raise ValueError("Location and language codes must be set.")

        # The frontend provides filters with 'keyword_data.' prefix, suitable for 'related_keywords'.
        # We need to create versions of these filters without the prefix for other modes.

        related_filters = filters
        ideas_filters = []
        if filters:
            for f in filters:
                new_filter = f.copy()
                if "field" in new_filter and new_filter["field"].startswith(
                    "keyword_data."
                ):
                    new_filter["field"] = new_filter["field"][len("keyword_data.") :]
                ideas_filters.append(new_filter)

        # Suggestions filters are the same as ideas filters (no prefix)
        suggestions_filters = ideas_filters

        structured_filters = {
            "ideas": ideas_filters,
            "suggestions": suggestions_filters,
            "related": related_filters,
        }

        # W21 FIX: Set default order_by if not provided, now structured as a dict
        if not order_by:
            ideas_suggestions_orderby = [
                "keyword_info.search_volume,desc",
            ]
            related_orderby = [
                "keyword_data.keyword_info.search_volume,desc",
            ]
            structured_orderby = {
                "ideas": ideas_suggestions_orderby,
                "suggestions": ideas_suggestions_orderby,
                "related": related_orderby,
            }
        else:
            # If order_by is provided from frontend, structure it for each mode
            related_orderby = [f"keyword_data.{rule}" for rule in order_by]
            structured_orderby = {
                "ideas": order_by,
                "suggestions": order_by,
                "related": related_orderby,
            }

        # Make a single burst call to the DataForSEOClientV2
        all_ideas, total_cost = self.client.get_keyword_ideas(
            seed_keywords=seed_keywords,
            location_code=location_code,
            language_code=language_code,
            client_cfg=self.config,
            discovery_modes=discovery_modes,
            filters=structured_filters,  # Use the structured filters directly
            order_by=structured_orderby,
            limit=limit,
            depth=depth,
            ignore_synonyms_override=ignore_synonyms,
            discovery_max_pages=discovery_max_pages,
        )
        self.logger.info(
            f"Burst discovery completed. Found {len(all_ideas)} raw keyword ideas. Cost: ${total_cost:.4f}"
        )

        # Filter out any duplicates and existing keywords from the burst results
        final_keywords_deduplicated = []
        seen_keywords = set(
            existing_keywords
        )  # Start with already existing to prevent re-adding

        # Recalculate raw counts per source based on `discovery_source` field added by get_keyword_ideas
        raw_counts = {"keyword_ideas": 0, "suggestions": 0, "related": 0}
        for item in all_ideas:
            kw_text = item.get("keyword", "").lower()
            if kw_text and kw_text not in seen_keywords:
                final_keywords_deduplicated.append(item)
                seen_keywords.add(kw_text)
                source = item.get("discovery_source")
                if source in raw_counts:
                    raw_counts[source] += 1
            elif kw_text:
                self.logger.debug(
                    f"Skipping duplicate or existing keyword: {item.get('keyword')}"
                )

        self.logger.info(
            f"Total unique new keywords after deduplication: {len(final_keywords_deduplicated)}"
        )

        return {
            "total_cost": total_cost,
            "raw_counts": raw_counts,
            "total_raw_count": len(all_ideas),  # Total raw from API before processing
            "total_unique_count": len(final_keywords_deduplicated),
            "final_keywords": final_keywords_deduplicated,
        }
