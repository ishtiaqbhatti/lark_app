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
        filters: Optional[List[Dict[str, Any]]], # The merged list from router
        order_by: Optional[List[str]],
        existing_keywords: set,
        limit: Optional[int] = None,
        depth: Optional[int] = None,
        ignore_synonyms: Optional[bool] = False, # Legacy parameter, new overrides are preferred
        # NEW params for direct passthrough from DiscoveryRunRequest
        include_clickstream_data: Optional[bool] = None,
        closely_variants: Optional[bool] = None,
        exact_match: Optional[bool] = None,
    ) -> Dict[str, Any]:
        """
        Delegates the keyword expansion to the new NewKeywordExpander.
        """
        self.logger.info(
            f"Starting keyword expansion with {len(seed_keywords)} seeds and modes: {discovery_modes}"
        )

        results = self.expander.expand(
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

        self.logger.info(
            f"Keyword expansion complete. Found {results['total_unique_count']} unique keywords."
        )

        return results
