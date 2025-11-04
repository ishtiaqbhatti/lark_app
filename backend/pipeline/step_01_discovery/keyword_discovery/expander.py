# pipeline/step_01_discovery/keyword_discovery/expander.py
import logging
import json # NEW import for json.dumps
from typing import List, Dict, Any, Optional

from external_apis.dataforseo_client_v2 import DataForSEOClientV2
from backend.data_mappers.dataforseo_mapper import DataForSEOMapper # NEW: Import for sanitization
from .filters import sanitize_filters_for_api # <--- 1. IMPORT THE FUNCTION


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
        filters: Optional[List[Dict[str, Any]]], # This is already the merged, goal-based filter list
        order_by: Optional[List[str]], # This is already the merged, goal-based order_by list
        existing_keywords: set,
        limit: Optional[int] = None,
        depth: Optional[int] = None,
        ignore_synonyms: Optional[bool] = False, # Legacy parameter, new overrides are preferred
        # NEW params for direct passthrough from DiscoveryRunRequest
        include_clickstream_data_override: Optional[bool] = None,
        closely_variants_override: Optional[bool] = None,
        exact_match_override: Optional[bool] = None,
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

        # Determine final parameter values, prioritizing overrides -> request -> client_cfg -> hardcoded default
        final_ignore_synonyms = ignore_synonyms if ignore_synonyms is not None else self.config.get("discovery_ignore_synonyms", False)
        final_include_clickstream_data = include_clickstream_data_override if include_clickstream_data_override is not None else self.config.get("include_clickstream_data", False)
        final_closely_variants = closely_variants_override if closely_variants_override is not None else self.config.get("closely_variants", True)
        final_exact_match = exact_match_override if exact_match_override is not None else self.config.get("discovery_exact_match", False)

        # --- Filter and Order_by Transformation Logic ---
        
        # 2. CALL THE SANITIZER FUNCTION HERE
        if filters:
            filters = sanitize_filters_for_api(filters)

        # The `filters` and `order_by` lists are now unified from goal presets.
        # The DataForSEOClientV2 will handle the transformation of the filters.
        structured_filters = {
            "Keyword Ideas": filters,
            "Keyword Suggestions": filters,
            "Related Keywords": filters,
        }

        ideas_suggestions_orderby_for_api = []
        related_orderby_for_api = []
        if order_by:
            for rule_str in order_by:
                parts = rule_str.split(',')
                field = parts[0]
                direction = parts[1]

                cleaned_field = field
                if field.startswith("keyword_data."):
                    cleaned_field = field[len("keyword_data."):]
                ideas_suggestions_orderby_for_api.append(f"{cleaned_field},{direction}")

                prefixed_field = field
                if not field.startswith("keyword_data."):
                    prefixed_field = f"keyword_data.{field}"
                related_orderby_for_api.append(f"{prefixed_field},{direction}")


        structured_orderby = {
            "Keyword Ideas": ideas_suggestions_orderby_for_api,
            "Keyword Suggestions": ideas_suggestions_orderby_for_api,
            "Related Keywords": related_orderby_for_api,
        }
        # --- END Filter and Order_by Transformation Logic ---


        # Make a single burst call to the DataForSEOClientV2 with comprehensive error handling
        try:
            all_ideas, total_cost = self.client.get_keyword_ideas(
                seed_keywords=seed_keywords,
                location_code=location_code,
                language_code=language_code,
                client_cfg=self.config,
                discovery_modes=discovery_modes,
                filters=structured_filters,
                order_by=structured_orderby,
                limit=limit,
                depth=depth,
                ignore_synonyms_override=final_ignore_synonyms,
                include_clickstream_override=final_include_clickstream_data,
                closely_variants_override=final_closely_variants,
                exact_match_override=final_exact_match,
            )
        except ConnectionError as e:
            self.logger.error(f"Network connection error during keyword expansion: {str(e)}")
            raise RuntimeError(
                "Failed to connect to DataForSEO API. Please check your internet connection and try again."
            ) from e
        except TimeoutError as e:
            self.logger.error(f"API request timeout during keyword expansion: {str(e)}")
            raise RuntimeError(
                "DataForSEO API request timed out. The request may be too large. Try reducing the number of seed keywords or using stricter filters."
            ) from e
        except ValueError as e:
            # Catches invalid filter syntax, invalid parameters, etc.
            self.logger.error(f"Invalid request parameters during keyword expansion: {str(e)}")
            raise ValueError(
                f"Invalid parameters sent to DataForSEO API: {str(e)}. Please check your filters and configuration."
            ) from e
        except PermissionError as e:
            # Catches API quota exceeded, rate limits, authentication failures
            self.logger.error(f"API authorization/quota error during keyword expansion: {str(e)}")
            raise PermissionError(
                "DataForSEO API quota exceeded or authentication failed. Please check your API credits and credentials."
            ) from e
        except Exception as e:
            # Catch-all for unexpected errors
            self.logger.error(f"Unexpected error during keyword expansion: {str(e)}", exc_info=True)
            raise RuntimeError(
                f"Unexpected error during keyword expansion: {str(e)}. Please contact support if this persists."
            ) from e
        if not all_ideas:
            self.logger.warning(
                "Burst discovery completed but returned zero results. This may indicate overly restrictive filters or no data available for the seed keywords."
            )
        else:
            self.logger.info(
                f"Burst discovery completed successfully. Found {len(all_ideas)} raw keyword ideas. Cost: ${total_cost:.4f}"
            )

        # Filter out any duplicates and existing keywords from the burst results
        final_keywords_deduplicated = []
        seen_keywords = set(
            existing_keywords
        )

        raw_counts = {"Keyword Ideas": 0, "Keyword Suggestions": 0, "Related Keywords": 0} # Corrected keys to match discovery_source from client_cfg list
        for item in all_ideas:
            kw_text = item.get("keyword", "").lower()
            if kw_text and kw_text not in seen_keywords:
                final_keywords_deduplicated.append(item)
                seen_keywords.add(kw_text)
                source = item.get("discovery_source")
                # Correctly map source names for counts based on how `discovery_source` is set in get_keyword_ideas
                if source == "keyword_ideas":
                    raw_counts["Keyword Ideas"] += 1
                elif source == "keyword_suggestions": # This includes 'keyword_suggestions_seed' too
                    raw_counts["Keyword Suggestions"] += 1
                elif source == "related":
                    raw_counts["Related Keywords"] += 1
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
            "total_raw_count": len(all_ideas),
            "total_unique_count": len(final_keywords_deduplicated),
            "final_keywords": final_keywords_deduplicated,
        }
