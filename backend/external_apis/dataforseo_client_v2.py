"""
This module provides a simplified and corrected client for the DataForSEO OnPage API,
focusing exclusively on the `instant_pages` endpoint.
"""

import base64
import json
import time
from typing import List, Dict, Any, Optional, Tuple
from concurrent.futures import ThreadPoolExecutor, as_completed
import logging
import requests
from urllib.parse import urlparse
import hashlib
from backend.data_access.database_manager import DatabaseManager
from backend.data_mappers.dataforseo_mapper import DataForSEOMapper
from backend.pipeline.step_01_discovery.keyword_discovery.filters import sanitize_filters_for_api, FORBIDDEN_API_FILTER_FIELDS # NEW: Import for filter sanitization


class DataForSEOClientV2:
    """
    A simplified client for the DataForSEO API, using only the `instant_pages` endpoint.
    """

    # W17 FIX: Move hardcoded endpoints to constants
    LABS_KEYWORD_IDEAS = "dataforseo_labs/google/keyword_ideas/live"
    LABS_KEYWORD_SUGGESTIONS = "dataforseo_labs/google/keyword_suggestions/live"
    LABS_RELATED_KEYWORDS = "dataforseo_labs/google/related_keywords/live"
    LABS_RANKED_KEYWORDS = "dataforseo_labs/google/ranked_keywords/live"
    LABS_COMPETITORS_DOMAIN = "dataforseo_labs/google/competitors_domain/live"
    SERP_ADVANCED = "serp/google/organic/live/advanced"
    ONPAGE_INSTANT_PAGES = "on_page/instant_pages"
    ONPAGE_CONTENT_PARSING = "on_page/content_parsing/live"  # Add this line

    KEYWORD_IDEAS_MODE_LIMIT = 1000 # Increased default limit as per API docs max
    KEYWORD_SUGGESTIONS_MODE_LIMIT = 1000 # Increased default limit
    RELATED_KEYWORDS_MODE_LIMIT = 1000 # Increased default limit

    def __init__(
        self,
        login: str,
        password: str,
        db_manager: DatabaseManager,
        config: Dict[str, Any],
        enable_cache: bool = True,
    ):
        self.base_url = "https://api.dataforseo.com/v3"
        if not login or not password:
            raise ValueError("DataForSEO API login and password cannot be empty.")
        credentials = f"{login}:{password}"
        self.headers = {
            "Authorization": f"Basic {base64.b64encode(credentials.encode()).decode()}",
            "Content-Type": "application/json",
        }
        self.logger = logging.getLogger(self.__class__.__name__)
        self.db_manager = db_manager
        self.config = config  # Store the config object
        self.enable_cache = enable_cache

    def _prioritize_and_limit_filters(self, filters: Optional[List[Any]]) -> List[Any]:
        """Enforces the 8-filter maximum rule by prioritizing essential filters."""
        if not filters:
            return []

        condition_count = sum(1 for f in filters if isinstance(f, list))
        if condition_count <= 8:
            # If 8 or fewer, just add "and" between them
            final_filters_structure = []
            for i, filt in enumerate(filters):
                final_filters_structure.append(filt)
                if i < len(filters) - 1:
                    final_filters_structure.append("and")
            return final_filters_structure

        self.logger.warning(
            f"Filter list exceeds 8 conditions ({condition_count} found). Prioritizing essential filters."
        )

        PRIORITIZED_FIELDS = [
            "keyword_difficulty", "search_volume", "main_intent", 
            "competition_level", "cpc", "competition", "is_another_language", "serp_item_types"
        ]

        prioritized_filters = []
        other_filters = []

        for element in filters:
            if isinstance(element, list) and len(element) >= 1:
                field_name = str(element[0]).lower()
                is_priority = any(p_field in field_name for p_field in PRIORITIZED_FIELDS)
                if is_priority:
                    prioritized_filters.append(element)
                else:
                    other_filters.append(element)

        limited_filters_list = prioritized_filters + other_filters
        limited_filters_list = limited_filters_list[:8]

        final_filters_structure = []
        for i, filt in enumerate(limited_filters_list):
            final_filters_structure.append(filt)
            if i < len(limited_filters_list) - 1:
                final_filters_structure.append("and")

        return final_filters_structure




    def _convert_filters_to_api_format(
        self, filters: Optional[List[List[Any]]]
    ) -> Optional[List[Any]]:
        """
        Converts a list of filter lists/strings into the DataForSEO Labs API's 
        list-of-lists format, sanitizes it, and enforces the 8-filter limit.
        This version specifically handles expanding 'has'/'has_not' filters that use an array value.
        """
        if not filters:
            return None

        # Filter out empty value filters, now accessing by index
        valid_filters = []
        for f in filters:
            if isinstance(f, list) and len(f) == 3:
                if f[2] is not None and f[2] != []:
                    valid_filters.append(f)
            elif isinstance(f, str): # Keep logical operators
                valid_filters.append(f)

        if not valid_filters:
            return None

        api_filters_conditions = []
        for f in valid_filters:
            if not isinstance(f, list):
                api_filters_conditions.append(f)
                continue

            field, op, value = f[0], f[1], f[2]
            
            if op in ["has", "has_not"] and isinstance(value, list):
                self.logger.info(f"Expanding '{op}' filter for field '{field}' into multiple conditions.")
                for item in value:
                    api_filters_conditions.append([field, op, item])
            else:
                api_filters_conditions.append([field, op, value])

        # 1. Sanitize to remove forbidden fields first
        sanitized_filters = sanitize_filters_for_api(api_filters_conditions)
        
        # 2. Prioritize and limit to 8 filters
        limited_filters = self._prioritize_and_limit_filters(sanitized_filters)
        
        if not limited_filters:
            return None
        
        return limited_filters

    def get_keyword_ideas(
        self,
        seed_keywords: List[str],
        location_code: int,
        language_code: str,
        client_cfg: Dict[str, Any],
        discovery_modes: List[str],
        filters: Dict[str, Any],
        order_by: Optional[Dict[str, List[str]]],
        limit: Optional[int] = None,
        depth: Optional[int] = None,
        ignore_synonyms_override: Optional[bool] = None,
        include_clickstream_override: Optional[bool] = None,
        closely_variants_override: Optional[bool] = None,
        exact_match_override: Optional[bool] = None,
    ) -> Tuple[List[Dict[str, Any]], float]:
        """
        Performs a comprehensive discovery burst using Keyword Ideas, Suggestions, and Related Keywords endpoints.
        """
        all_items = []
        total_cost = 0.0
        max_pages = client_cfg.get("discovery_max_pages", 1)

        def to_bool(value: Any) -> bool:
            if isinstance(value, bool):
                return value
            if isinstance(value, str):
                return value.lower() in ['true', '1', 't', 'y', 'yes']
            return bool(value)

        final_ignore_synonyms = to_bool(ignore_synonyms_override if ignore_synonyms_override is not None else self.config.get("discovery_ignore_synonyms", False))
        final_include_clickstream = to_bool(include_clickstream_override if include_clickstream_override is not None else self.config.get("include_clickstream_data", False))
        final_closely_variants = to_bool(closely_variants_override if closely_variants_override is not None else self.config.get("closely_variants", False))
        final_exact_match = to_bool(exact_match_override if exact_match_override is not None else self.config.get("discovery_exact_match", False))

        if "Keyword Ideas" in discovery_modes:
            self.logger.info(f"Fetching keyword ideas for {len(seed_keywords)} seeds...")
            ideas_endpoint = self.LABS_KEYWORD_IDEAS
            api_filters = self._convert_filters_to_api_format(filters.get("Keyword Ideas"))
            
            ideas_task = {
                "keywords": seed_keywords,
                "location_code": location_code,
                "language_code": language_code,
                "limit": limit if limit is not None else self.KEYWORD_IDEAS_MODE_LIMIT,
                "include_serp_info": True,
                "ignore_synonyms": final_ignore_synonyms,
                "closely_variants": final_closely_variants,
                "order_by": order_by.get("Keyword Ideas") if order_by else None,
                "include_clickstream_data": final_include_clickstream,
            }
            if api_filters:
                ideas_task["filters"] = api_filters
                
            ideas_response, cost = self._post_request(ideas_endpoint, [ideas_task], tag="discovery_ideas")
            ideas_items = (ideas_response["tasks"][0]["result"][0].get("items") or []) if ideas_response and ideas_response.get("tasks") and ideas_response["tasks"] and ideas_response["tasks"][0].get("result") and ideas_response["tasks"][0]["result"] else []
            total_cost += cost

            for item in ideas_items:
                item["discovery_source"] = "keyword_ideas"
                item["depth"] = 0
                all_items.append(DataForSEOMapper.sanitize_keyword_data_item(item))
            self.logger.info(f"Found {len(ideas_items)} ideas from Keyword Ideas API.")

        if "Keyword Suggestions" in discovery_modes:
            self.logger.info("Fetching keyword suggestions...")
            suggestions_endpoint = self.LABS_KEYWORD_SUGGESTIONS
            for seed_keyword in seed_keywords:
                api_filters = self._convert_filters_to_api_format(filters.get("Keyword Suggestions"))
                
                suggestions_task = {
                    "keyword": seed_keyword,
                    "location_code": location_code,
                    "language_code": language_code,
                    "limit": limit if limit is not None else self.KEYWORD_SUGGESTIONS_MODE_LIMIT,
                    "include_serp_info": True,
                    "exact_match": final_exact_match,
                    "ignore_synonyms": final_ignore_synonyms,
                    "include_seed_keyword": True,
                    "order_by": order_by.get("Keyword Suggestions"),
                    "include_clickstream_data": final_include_clickstream,
                }
                if api_filters:
                    suggestions_task["filters"] = api_filters

                suggestions_response, cost = self._post_request(suggestions_endpoint, [suggestions_task], tag=f"discovery_suggestions:{seed_keyword[:20]}")
                suggestions_items = (suggestions_response["tasks"][0]["result"][0].get("items") or []) if suggestions_response and suggestions_response.get("tasks") and suggestions_response["tasks"] and suggestions_response["tasks"][0].get("result") and suggestions_response["tasks"][0]["result"] else []
                total_cost += cost
                for item in suggestions_items:
                    item["discovery_source"] = "keyword_suggestions"
                    item["depth"] = 0
                    all_items.append(DataForSEOMapper.sanitize_keyword_data_item(item))
                self.logger.info(f"Found {len(suggestions_items)} suggestions for '{seed_keyword}'.")
                
        if "Related Keywords" in discovery_modes:
            self.logger.info("Fetching related keywords...")
            related_endpoint = self.LABS_RELATED_KEYWORDS
            seed_keywords_for_related = seed_keywords[:10]

            for seed in seed_keywords_for_related:
                related_filters_raw = filters.get("Related Keywords")
                if related_filters_raw:
                    for f in related_filters_raw:
                        if "field" in f and not f["field"].startswith("keyword_data."):
                            f["field"] = f"keyword_data.{f['field']}"
                
                api_filters = self._convert_filters_to_api_format(related_filters_raw)
                
                related_orderby = order_by.get("Related Keywords", [])
                api_orderby = []
                for rule in related_orderby:
                    parts = rule.split(',')
                    if len(parts) == 2:
                        field, direction = parts
                        if not field.startswith("keyword_data."):
                            field = f"keyword_data.{field}"
                        api_orderby.append(f"{field},{direction}")
                
                related_task = {
                    "keyword": seed,
                    "location_code": location_code,
                    "language_code": language_code,
                    "depth": 1,
                    "limit": limit if limit is not None else self.RELATED_KEYWORDS_MODE_LIMIT,
                    "include_serp_info": True,
                    "order_by": api_orderby if api_orderby else None,
                    "include_clickstream_data": final_include_clickstream,
                    "replace_with_core_keyword": client_cfg.get("discovery_replace_with_core_keyword", False),
                }
                if api_filters:
                    related_task["filters"] = api_filters

                related_response, cost = self._post_request(related_endpoint, [related_task], tag=f"discovery_related:{seed[:20]}")
                related_items = (related_response["tasks"][0]["result"][0].get("items") or []) if related_response and related_response.get("tasks") and related_response["tasks"] and related_response["tasks"][0].get("result") and related_response["tasks"][0]["result"] else []
                total_cost += cost
                for item in related_items:
                    keyword_data = item.get("keyword_data")
                    if keyword_data:
                        keyword_data["discovery_source"] = "related"
                        keyword_data["depth"] = item.get("depth")
                        all_items.append(DataForSEOMapper.sanitize_keyword_data_item(keyword_data))
            self.logger.info(f"Total raw items from all sources: {len(all_items)}")

        return all_items, total_cost

    def get_technical_onpage_data(
        self, urls: List[str], client_cfg: Dict[str, Any]
    ) -> Tuple[Optional[List[Dict[str, Any]]], float]:
        """
        Performs a batch OnPage scan using the Instant Pages endpoint to get technical SEO data.
        """
        if not urls:
            return [], 0.0

        self.logger.info(
            f"Fetching OnPage data for {len(urls)} URLs with device preset '{client_cfg.get('device', 'desktop')}' using Instant Pages..."
        )

        endpoint = self.ONPAGE_INSTANT_PAGES
        # Group URLs into batches that comply with max_domains and max_tasks
        url_batches = self._group_urls_by_domain(
            urls,
            max_domains=client_cfg.get("onpage_max_domains_per_request", 5),
            batch_size=client_cfg.get("onpage_max_tasks_per_request", 20),
        )

        all_results = []
        total_cost = 0.0

        for i, batch in enumerate(url_batches):
            post_data = []
            for url in batch:
                task_data = {
                    "url": url,
                    # W8 FIX: Use configured value, not hardcoded False
                    "enable_browser_rendering": client_cfg.get(
                        "onpage_enable_browser_rendering", False
                    ),
                    # W5 FIX: Inject critical analysis parameters
                    "validate_micromarkup": client_cfg.get(
                        "onpage_validate_micromarkup", False
                    ),
                    "return_despite_timeout": client_cfg.get(
                        "onpage_return_despite_timeout", False
                    ),
                    "check_spell": client_cfg.get("onpage_check_spell", False),
                    # W7 FIX: Inject language header
                    "accept_language": client_cfg.get("onpage_accept_language"),
                    # Include configured user agent if available
                    "custom_user_agent": client_cfg.get("onpage_custom_user_agent"),
                    "switch_pool": client_cfg.get("onpage_enable_switch_pool", False),
                }

                # Add ip_pool_for_scan if it's in the client config
                if "ip_pool_for_scan" in client_cfg:
                    task_data["ip_pool_for_scan"] = client_cfg["ip_pool_for_scan"]

                # W7 FIX & W17 FIX: Include custom screen resolution if rendering is enabled and validate its range
                screen_ratio = client_cfg.get("onpage_browser_screen_resolution_ratio")
                if screen_ratio is not None and (
                    task_data["enable_browser_rendering"]
                    or client_cfg.get("onpage_enable_javascript", False)
                ):
                    # W17 FIX: Validate the range [0.5, 3.0]
                    if 0.5 <= screen_ratio <= 3.0:
                        task_data["browser_screen_resolution_ratio"] = screen_ratio
                    else:
                        self.logger.error(
                            f"Invalid screen ratio configured: {screen_ratio}. Must be between 0.5 and 3.0. Omitting parameter."
                        )
                        # Parameter will be omitted if outside valid range, relying on DataForSEO default.

                # W9 FIX: Include custom checks threshold if provided in config (continues from Task 4.4)
                thresholds_str = client_cfg.get("onpage_custom_checks_thresholds")
                if thresholds_str:
                    try:
                        task_data["checks_threshold"] = json.loads(thresholds_str)
                    except json.JSONDecodeError:
                        self.logger.error(
                            "Failed to parse onpage_custom_checks_thresholds JSON from config. Using default thresholds."
                        )

                # W12 FIX: Include custom JS if enabled (continues from Task 12.4)
                if client_cfg.get("onpage_enable_custom_js", False):
                    custom_js_script = client_cfg.get("onpage_custom_js")
                    if custom_js_script:
                        task_data["custom_js"] = custom_js_script

                # Remove keys if their value is None to maintain a clean API request
                task_data = {k: v for k, v in task_data.items() if v is not None}
                post_data.append(task_data)

            # --- Attempt 1 for the batch ---
            response, cost = self._post_request(
                endpoint, post_data, tag=f"onpage_instant_pages_content:batch{i + 1}"
            )
            total_cost += cost

            current_batch_results = []
            failed_urls_in_batch = []

            if response and response.get("tasks"):
                for task in response["tasks"]:
                    task_url = task.get("data", {}).get("url")

                    # Explicit Failure Criteria Check: Task failed OR result is malformed/empty
                    if (
                        task.get("status_code") != 20000
                        or not task.get("result")
                        or not task["result"][0].get("items")
                    ):
                        self.logger.warning(
                            f"Task for URL {task_url} failed/malformed response (Status: {task.get('status_code')}). Queuing for retry."
                        )
                        failed_urls_in_batch.append(task_url)
                    else:
                        for result_item in task["result"]:
                            if result_item and result_item.get("items"):
                                current_batch_results.extend(
                                    [
                                        DataForSEOMapper.sanitize_onpage_data_item(it)
                                        for it in result_item["items"]
                                    ]
                                )  # ADDED SANITIZATION
            else:
                self.logger.error(
                    f"Failed to get any response for instant_pages batch starting with URL: {batch[0]}"
                )
                failed_urls_in_batch.extend(batch)

            # --- Retry mechanism for failed URLs in this batch ---
            if failed_urls_in_batch:
                self.logger.info(
                    f"Retrying {len(failed_urls_in_batch)} failed URLs from batch {i + 1}..."
                )

                should_switch_pool = client_cfg.get("onpage_enable_switch_pool", False)

                # W15 FIX: Re-group failed URLs to enforce the max_domains limit (5 domains max per request)
                max_domains_per_retry = client_cfg.get(
                    "onpage_max_domains_per_request", 5
                )
                retry_batches = self._group_urls_by_domain(
                    failed_urls_in_batch,
                    max_domains=max_domains_per_retry,
                    batch_size=client_cfg.get("onpage_max_tasks_per_request", 20),
                )

                current_retry_cost = 0.0

                for retry_batch in retry_batches:
                    retry_post_data = []
                    for url in retry_batch:
                        # Reconstruct task_data using original structure but force `return_despite_timeout`
                        original_task_data = next(
                            (item for item in post_data if item.get("url") == url), {}
                        )
                        retry_task_data = {
                            **original_task_data,
                            "return_despite_timeout": True,
                        }

                        if should_switch_pool:
                            retry_task_data["switch_pool"] = True

                        retry_post_data.append(retry_task_data)

                    retry_response, retry_cost = self._post_request(
                        endpoint,
                        retry_post_data,
                        tag=f"onpage_instant_pages_content:retry_batch{i + 1}",
                    )
                    current_retry_cost += retry_cost

                    # Process retry_response (existing logic, moved and adapted)
                    if retry_response and retry_response.get("tasks"):
                        for task in retry_response["tasks"]:
                            task_url = task.get("data", {}).get("url")
                            if task.get("status_code") == 20000 and task.get("result"):
                                for result_item in task["result"]:
                                    if result_item and result_item.get("items"):
                                        current_batch_results.extend(
                                            result_item["items"]
                                        )
                            else:
                                self.logger.warning(
                                    f"Retry task for URL {task_url} failed again (Status: {task.get('status_code')})."
                                )

                total_cost += current_retry_cost

            all_results.extend(current_batch_results)
        return all_results, total_cost

    def _post_request(
        self, endpoint: str, data: List[Dict[str, Any]], tag: Optional[str] = None
    ) -> Tuple[Optional[Dict[str, Any]], float]:
        """
        Handles the actual POST request to the API, with retries, exponential backoff,
        and intelligent caching that ignores failed responses.
        """
        cache_key_string = json.dumps({"endpoint": endpoint, "data": data}, sort_keys=True)
        cache_key = hashlib.md5(cache_key_string.encode("utf-8")).hexdigest()

        if self.enable_cache:
            cached_response = self.db_manager.get_api_cache(cache_key)
            if cached_response:
                self.logger.info(f"Cache HIT for endpoint {endpoint} with tag '{tag}'.")
                return cached_response, 0.0

        self.logger.info(f"Cache MISS for endpoint {endpoint} with tag '{tag}'. Making live API call.")

        if tag:
            for task_item in data:
                if isinstance(task_item, dict):
                    task_item["tag"] = tag

        full_url = f"{self.base_url.rstrip('/')}/{endpoint.lstrip('/')}"
        self.logger.info(f"Making POST request to {full_url} with data: {json.dumps(data)}")
        retries = 3
        backoff_factor = 5

        for attempt in range(retries):
            try:
                response = requests.post(full_url, headers=self.headers, data=json.dumps(data), timeout=120)

                if response.status_code >= 500:
                    self.logger.error(f"DataForSEO API returned a server error ({response.status_code}). Aborting.")
                    return None, 0.0

                response.raise_for_status()
                response_json = response.json()
                cost = response_json.get("cost", 0.0)

                is_successful_response = (
                    response_json.get("status_code") == 20000 and
                    response_json.get("tasks_error", 0) == 0 and
                    response_json.get("tasks") and
                    response_json["tasks"][0].get("status_code") == 20000
                )

                if is_successful_response:
                    if self.enable_cache:
                        self.db_manager.set_api_cache(cache_key, response_json)
                    return response_json, cost
                else:
                    error_task = response_json.get("tasks", [{}])[0]
                    status_code = error_task.get("status_code", response_json.get("status_code"))
                    status_message = error_task.get("status_message", response_json.get("status_message"))
                    self.logger.error(f"DataForSEO API returned an error. Code: {status_code}, Message: {status_message}. This response will NOT be cached.")
                    if status_code == 40501:
                        return response_json, cost

            except requests.exceptions.HTTPError as e:
                if response.status_code == 429 and attempt < retries - 1:
                    wait_time = backoff_factor * (2**attempt)
                    self.logger.warning(f"Rate limit exceeded (429). Retrying in {wait_time} seconds...")
                    time.sleep(wait_time)
                    continue
                else:
                    self.logger.error(f"HTTP error during API request: {e}", exc_info=True)
                    return None, 0.0
            except requests.exceptions.RequestException as e:
                self.logger.error(f"Network error during API request: {e}", exc_info=True)
                if attempt < retries - 1:
                    time.sleep(backoff_factor * (2**attempt))
                    continue
                return None, 0.0

        return None, 0.0