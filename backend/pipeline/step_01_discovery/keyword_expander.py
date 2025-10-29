# pipeline/step_01_discovery/keyword_expander.py
import logging
from typing import List, Dict, Any, Optional
from external_apis.dataforseo_client_v2 import DataForSEOClientV2
from .keyword_discovery.expander import NewKeywordExpander


class KeywordExpander:
    """
    A wrapper class that uses the new modular keyword expansion system.
    """

    def __init__(
        self,
        client: DataForSEOClientV2,
        config: Dict[str, Any],
        run_logger: Optional[logging.Logger] = None,
    ):
        self.client = client
        self.config = config
        self.logger = run_logger or logging.getLogger(self.__class__.__name__)
        self.expander = NewKeywordExpander(client, config, self.logger)

    def expand_seed_keyword(
        self,
        seed_keywords: List[str],
        discovery_modes: List[str],
        filters: Optional[List[Any]],
        order_by: Optional[List[str]],
        existing_keywords: set,
        limit: Optional[int] = None,
        depth: Optional[int] = None,
        ignore_synonyms: Optional[bool] = False,
    ) -> Dict[str, Any]:
        """
        Efficient keyword expansion with O(1) deduplication.
        """
        self.logger.info(f"Starting expansion with {len(seed_keywords)} seeds")

        # Prepare structured filters
        related_filters = filters
        ideas_filters = []
        if filters:
            for f in filters:
                new_filter = f.copy()
                if "field" in new_filter and new_filter["field"].startswith("keyword_data."):
                    new_filter["field"] = new_filter["field"][len("keyword_data."):]
                ideas_filters.append(new_filter)
        suggestions_filters = ideas_filters
        structured_filters = {
            "ideas": ideas_filters,
            "suggestions": suggestions_filters,
            "related": related_filters,
        }

        # Prepare structured order_by
        if not order_by:
            structured_orderby = {
                "ideas": ["keyword_info.search_volume,desc"],
                "suggestions": ["keyword_info.search_volume,desc"],
                "related": ["keyword_data.keyword_info.search_volume,desc"],
            }
        else:
            structured_orderby = {
                "ideas": order_by,
                "suggestions": order_by,
                "related": [f"keyword_data.{rule}" for rule in order_by],
            }

        results = self.expander.expand(
            seed_keywords,
            discovery_modes,
            structured_filters,
            structured_orderby,
            existing_keywords,
            limit,
            depth,
            ignore_synonyms,
        )

        # EFFICIENT DEDUPLICATION USING SET:
        final_keywords_deduplicated = []
        seen_keywords = set(existing_keywords)  # Start with existing
        
        raw_counts = {"keyword_ideas": 0, "suggestions": 0, "related": 0}
        
        for item in results.get("final_keywords", []):
            kw_text = item.get("keyword", "").lower()
            
            # O(1) LOOKUP:
            if kw_text and kw_text not in seen_keywords:
                final_keywords_deduplicated.append(item)
                seen_keywords.add(kw_text)  # O(1) INSERT
                
                source = item.get("discovery_source")
                if source in raw_counts:
                    raw_counts[source] += 1

        self.logger.info(
            f"Deduplication complete. {len(final_keywords_deduplicated)} unique keywords from {len(results.get('final_keywords', []))} total."
        )

        return {
            **results,
            "total_unique_count": len(final_keywords_deduplicated),
            "final_keywords": final_keywords_deduplicated,
            "raw_counts": raw_counts,
        }
