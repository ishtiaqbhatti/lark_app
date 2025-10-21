# services/keyword_data_aggregator.py

from typing import List, Dict, Any, Optional
from external_apis.dataforseo_client_v2 import DataForSEOClientV2


class KeywordDataAggregator:
    def __init__(
        self, dataforseo_client: DataForSEOClientV2, client_cfg: Dict[str, Any]
    ):
        self.dataforseo_client = dataforseo_client
        self.client_cfg = client_cfg

    def get_keyword_data(
        self,
        seed_keywords: List[str],
        discovery_modes: List[str],
        filters: Optional[List[Any]],
        order_by: Optional[List[str]],
        limit: Optional[int],
        depth: Optional[int],
        ignore_synonyms: Optional[bool],
    ) -> List[Dict[str, Any]]:
        """
        Calls the keyword discovery endpoints, deduplicates the results, and returns a unified list of keyword data objects.
        """
        # W21 FIX: Set default order_by if not provided, now structured as a dict
        if not order_by:
            ideas_suggestions_orderby = [
                "keyword_properties.keyword_difficulty,asc",
                "keyword_info.search_volume,desc",
            ]
            related_orderby = [
                "keyword_data.keyword_properties.keyword_difficulty,asc",
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

        # Structure filters for the client
        ideas_suggestions_filters = []
        if filters:
            for f in filters:
                new_filter = f.copy()
                if "field" in new_filter and new_filter["field"].startswith(
                    "keyword_data."
                ):
                    new_filter["field"] = new_filter["field"][len("keyword_data.") :]
                ideas_suggestions_filters.append(new_filter)

        structured_filters = {
            "ideas": ideas_suggestions_filters,
            "suggestions": ideas_suggestions_filters,
            "related": filters,  # Related keeps the prefix
        }

        all_ideas, _ = self.dataforseo_client.get_keyword_ideas(
            seed_keywords=seed_keywords,
            location_code=self.client_cfg.get("location_code"),
            language_code=self.client_cfg.get("language_code"),
            client_cfg=self.client_cfg,
            discovery_modes=discovery_modes,
            filters=structured_filters,
            order_by=structured_orderby,
            limit=limit,
            depth=depth,
            ignore_synonyms=ignore_synonyms,
        )

        final_keywords_deduplicated = []
        seen_keywords = set()
        for item in all_ideas:
            kw_text = item.get("keyword", "").lower()
            if kw_text and kw_text not in seen_keywords:
                final_keywords_deduplicated.append(item)
                seen_keywords.add(kw_text)

        return final_keywords_deduplicated
