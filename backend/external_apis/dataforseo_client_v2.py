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

        # Make limits configurable
        self.keyword_ideas_limit = self.config.get("KEYWORD_IDEAS_MODE_LIMIT", 10)
        self.keyword_suggestions_limit = self.config.get("KEYWORD_SUGGESTIONS_MODE_LIMIT", 100)
        self.related_keywords_limit = self.config.get("RELATED_KEYWORDS_MODE_LIMIT", 100)


    def _enforce_api_filter_limit(
        self, filters: Optional[List[Any]], max_limit: int = 8
    ) -> Optional[List[Any]]:
        """
        Enforces the API filter limit (max 8 conditions) by truncating the filter list.
        This is a backend safeguard if frontend validation is bypassed.
        """
        if not filters:
            return None

        # Count actual filter conditions (which are lists, not "and"/"or" strings)
        condition_elements = [f for f in filters if isinstance(f, list)]
        if len(condition_elements) <= max_limit:
            return filters  # No need to truncate

        self.logger.warning(
            f"Backend safeguard: API filter list exceeds {max_limit} conditions ({len(condition_elements)} found). Truncating to the first {max_limit} conditions."
        )

        truncated_filters = []
        condition_count = 0
        for item in filters:
            if isinstance(item, list):  # This is a condition
                if condition_count < max_limit:
                    truncated_filters.append(item)
                    condition_count += 1
                else:
                    break  # Stop adding conditions
            elif truncated_filters and isinstance(truncated_filters[-1], list):
                # Add logical operator only if it follows a condition and we're still building
                truncated_filters.append(item)

        # Ensure the list doesn't end with a dangling logical operator
        if (
            truncated_filters
            and isinstance(truncated_filters[-1], str)
            and truncated_filters[-1].lower() in ["and", "or"]
        ):
            truncated_filters.pop()

        return truncated_filters

    def _post_request(
        self, endpoint: str, data: List[Dict[str, Any]], tag: Optional[str] = None
    ) -> Tuple[Optional[Dict[str, Any]], float]:
        """
        Handles the actual POST request to the API, with retries and exponential backoff for rate limits.
        """
        cache_key_string = json.dumps(
            {
                "endpoint": endpoint,
                "data": data,
                "filters": data[0].get("filters") if data else None,
            },
            sort_keys=True,
        )
        cache_key = hashlib.md5(cache_key_string.encode("utf-8")).hexdigest()

        if self.enable_cache:
            cached_response = self.db_manager.get_api_cache(cache_key)
            if cached_response:
                self.logger.info(f"Cache HIT for endpoint {endpoint} with tag '{tag}'.")
                return cached_response, 0.0

        self.logger.info(
            f"Cache MISS for endpoint {endpoint} with tag '{tag}'. Making live API call."
        )

        if tag:
            for task_item in data:
                if isinstance(task_item, dict):
                    task_item["tag"] = tag

        full_url = f"{self.base_url.rstrip('/')}/{endpoint.lstrip('/')}"
        self.logger.info(
            f"Making POST request to {full_url} with data: {json.dumps(data)}"
        )
        retries = 3
        backoff_factor = 5

        for attempt in range(retries):
            try:
                response = requests.post(
                    full_url, headers=self.headers, data=json.dumps(data), timeout=120
                )

                # W20 FIX: Early exit for critical top-level HTTP errors
                if response.status_code >= 500:
                    self.logger.error(
                        f"DataForSEO API returned a server error ({response.status_code}). Aborting after {attempt + 1} attempts."
                    )
                    return None, 0.0  # Do not retry on server errors

                response.raise_for_status()  # Raise HTTPError for 4xx client errors

                response_json = response.json()

                # W20 FIX: Check top-level status_code from DataForSEO
                if response_json.get("status_code") != 20000:
                    self.logger.error(
                        f"DataForSEO API returned non-20000 status_code: {response_json.get('status_code')} - {response_json.get('status_message')}"
                    )
                    # No retry for auth errors, etc.
                    if response_json.get("status_code") in [40101, 40102, 40103]:
                        return None, 0.0

                # W20 FIX: Log critical task-level errors
                if response_json.get("tasks_error", 0) > 0:
                    for task in response_json.get("tasks", []):
                        if task.get("status_code") != 20000:
                            # Log specific, known critical errors
                            if task.get("status_code") == 40501:  # Duplicate crawl host
                                self.logger.critical(
                                    f"CRITICAL API ERROR (40501): Duplicate crawl host detected for URL {task.get('data', {}).get('url')}. This batch is invalid."
                                )
                            else:
                                self.logger.warning(
                                    f"Task-level error for {task.get('data', {}).get('url', 'N/A')}: {task.get('status_code')} - {task.get('status_message')}"
                                )

                cost = response_json.get("cost", 0.0)

                if self.enable_cache:
                    self.db_manager.set_api_cache(cache_key, response_json)

                return response_json, cost

            except requests.exceptions.HTTPError as e:
                # This will now primarily catch 4xx errors
                if (
                    response.status_code == 429 and attempt < retries - 1
                ):  # Specifically handle rate limits
                    wait_time = backoff_factor * (2**attempt)
                    self.logger.warning(
                        f"Rate limit exceeded (429). Retrying in {wait_time} seconds... (Attempt {attempt + 1}/{retries})"
                    )
                    time.sleep(wait_time)
                    continue
                else:
                    self.logger.error(
                        f"HTTP error during DataForSEO API request to {full_url}: {e}",
                        exc_info=True,
                    )
                    return None, 0.0
            except requests.exceptions.RequestException as e:
                self.logger.error(
                    f"Network error during DataForSEO API request to {full_url}: {e}",
                    exc_info=True,
                )
                if attempt < retries - 1:
                    time.sleep(backoff_factor * (2**attempt))
                    continue
                return None, 0.0

        return None, 0.0

    def _prioritize_and_limit_filters(self, filters: Optional[List[Any]]) -> List[Any]:
        """Enforces the 8-filter maximum rule by prioritizing essential filters."""
        if not filters:
            return []

        # Count actual filter conditions (excluding logical operators like "and", "or")
        condition_count = sum(1 for f in filters if isinstance(f, list))

        # If already within the limit, return as is.
        if condition_count <= 8:
            return filters

        self.logger.warning(
            f"Filter list exceeds 8 conditions ({condition_count} found). Prioritizing essential filters."
        )

        # Simple prioritization logic: Keep filters based on field name presence
        # Prioritized fields (essential for targeting): keyword_difficulty, search_volume, main_intent, competition_level, cpc, competition
        PRIORITIZED_FIELDS = [
            "keyword_difficulty",
            "search_volume",
            "main_intent",
            "competition_level",
            "cpc",
            "competition",
        ]

        prioritized_filters = []
        other_filters = []

        # Iterate through the filters to separate prioritized from others
        for element in filters:
            if isinstance(element, list) and len(element) >= 3:
                # Assuming element[0] is the field name, like "keyword_info.search_volume"
                field_name = element[0].lower()
                is_priority = any(
                    p_field in field_name for p_field in PRIORITIZED_FIELDS
                )

                if is_priority:
                    prioritized_filters.append(element)
                else:
                    other_filters.append(element)
            else:
                # Logical operators ('and', 'or') will be re-added later if needed
                pass

        # Combine prioritized filters (up to 8 slots)
        limited_filters_list = []  # Only actual conditions

        # 1. Add prioritized filters first
        for f in prioritized_filters:
            if len(limited_filters_list) < 8:
                limited_filters_list.append(f)
            else:
                break

        # 2. Fill remaining slots with non-prioritized filters if space permits
        for f in other_filters:
            if len(limited_filters_list) < 8:
                limited_filters_list.append(f)
            else:
                break

        # Reconstruct the filter list with "and" operators
        final_filters_structure = []
        for i, filt in enumerate(limited_filters_list):
            final_filters_structure.append(filt)
            if i < len(limited_filters_list) - 1:
                final_filters_structure.append("and")

        return final_filters_structure

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

    def get_content_onpage_data(
        self,
        urls: List[str],
        client_cfg: Dict[str, Any],
        enable_javascript: bool = False,
    ) -> Tuple[Optional[List[Dict[str, Any]]], float]:
        """
        Performs OnPage scans using the Content Parsing endpoint, with control over JS rendering.
        This function now sends requests for multiple URLs in parallel using a thread pool
        for improved performance, as the endpoint does not support batch processing.
        """
        if not urls:
            return [], 0.0

        self.logger.info(
            f"Fetching OnPage Content Parsing data for {len(urls)} URLs with enable_javascript={enable_javascript} in parallel..."
        )

        all_tasks = []
        total_cost = 0.0

        # Helper function to be executed in each thread
        def _fetch_single_url(url: str) -> Tuple[Optional[Dict[str, Any]], float]:
            post_data = [
                {
                    "url": url,
                    "enable_javascript": enable_javascript,
                    "store_raw_html": True,
                    "markdown_view": True,
                    "disable_cookie_popup": client_cfg.get(
                        "onpage_disable_cookie_popup", True
                    ),
                }
            ]
            tag = f"onpage_content_parsing_js_{str(enable_javascript).lower()}:{urlparse(url).netloc}"
            return self._post_request(self.ONPAGE_CONTENT_PARSING, post_data, tag=tag)

        # Use a ThreadPoolExecutor to send requests concurrently
        # The number of workers can be tuned, but 5 is a safe default to avoid overwhelming the API
        with ThreadPoolExecutor(max_workers=5) as executor:
            # map executes the function for each item in the urls list
            future_to_url = {
                executor.submit(_fetch_single_url, url): url for url in urls
            }
            for future in as_completed(future_to_url):
                url = future_to_url[future]
                try:
                    response, cost = future.result()
                    total_cost += cost
                    if response and response.get("tasks"):
                        all_tasks.extend(response["tasks"])
                    else:
                        self.logger.error(
                            f"Failed to get a valid response for content_parsing for URL: {url}"
                        )
                        all_tasks.append(
                            {
                                "status_code": 50000,
                                "status_message": "No response from API",
                                "data": {"url": url},
                            }
                        )
                except Exception as exc:
                    self.logger.error(f"{url} generated an exception: {exc}")
                    all_tasks.append(
                        {
                            "status_code": 50001,
                            "status_message": f"Request generated an exception: {exc}",
                            "data": {"url": url},
                        }
                    )

        if all_tasks:
            return all_tasks, total_cost

        self.logger.error(
            f"Failed to get any response for any of the {len(urls)} URLs."
        )
        return [
            {
                "status_code": 50000,
                "status_message": "No response from API",
                "data": {"url": url},
            }
            for url in urls
        ], 0.0

    def get_serp_results(
        self,
        keyword: str,
        location_code: int,
        language_code: str,
        client_cfg: Dict[str, Any],
        serp_call_params: Optional[Dict[str, Any]] = None,
    ) -> Tuple[Optional[Dict[str, Any]], float]:
        """
        Fetches the advanced SERP data for a single keyword, with caching.
        """
        device = client_cfg.get("device", "desktop")
        self.logger.info(
            f"Fetching live SERP results for '{keyword}' on device '{device}'..."
        )
        endpoint = self.SERP_ADVANCED
        base_serp_params = {
            "keyword": keyword,
            "location_code": location_code,
            "language_code": language_code,
            "group_organic_results": False,  # NEW: Ensure no grouping for full analysis
        }
        if serp_call_params:
            base_serp_params.update(serp_call_params)

        if client_cfg.get("calculate_rectangles", False):
            base_serp_params["calculate_rectangles"] = True

        base_serp_params["depth"] = int(base_serp_params.get("depth", 10))

        # Add advanced features from client_cfg if they are enabled.
        if client_cfg.get("calculate_rectangles", False):
            base_serp_params["calculate_rectangles"] = True

        paa_depth = client_cfg.get("people_also_ask_click_depth", 0)
        if isinstance(paa_depth, int) and 1 <= paa_depth <= 4:
            base_serp_params["people_also_ask_click_depth"] = paa_depth

        # W3 FIX: Add support for loading AI overview asynchronously
        if client_cfg.get("load_async_ai_overview", False):
            base_serp_params["load_async_ai_overview"] = True

        # W11 FIX: Include URL removal parameters
        remove_params_str = client_cfg.get("serp_remove_from_url_params")
        if remove_params_str:
            # Assuming config value is a comma-separated string of parameters
            params_list = [p.strip() for p in remove_params_str.split(",") if p.strip()]

            # W14 FIX: Validate and clip URL removal parameters (max 10)
            if len(params_list) > 10:
                self.logger.warning(
                    f"Configuration defined {len(params_list)} parameters for removal, but DataForSEO limit is 10. Truncating."
                )

            base_serp_params["remove_from_url"] = params_list[:10]

        # Ensure device and OS are passed based on client config
        device = client_cfg.get("device", "desktop")
        os_name = client_cfg.get("os", "windows")

        # Adjust OS if device is mobile for compatibility
        if device == "mobile" and os_name not in ["android", "ios"]:
            os_name = "android"

        base_serp_params["device"] = device
        base_serp_params["os"] = os_name

        request_tag = f"serp_advanced:{keyword[:50]}"
        response, cost = self._post_request(
            endpoint, [base_serp_params], tag=request_tag
        )

        if response and response.get("tasks") and response["tasks"][0].get("result"):
            result_data = response["tasks"][0]["result"][0]
            sanitized_result_data = DataForSEOMapper.sanitize_serp_overview_response(
                result_data
            )  # ADDED SANITIZATION
            return sanitized_result_data, cost

        return None, cost

    def post_with_paging(
        self,
        endpoint: str,
        initial_task: Dict[str, Any],
        max_pages: int,
        paginated: bool = True,
        tag: Optional[str] = None,
    ) -> Tuple[List[Dict[str, Any]], float]:
        """
        Executes a POST request and, if paginated=True, recursively retrieves all results using the correct pagination method.
        """
        all_items = []
        total_cost = 0.0
        current_task = initial_task.copy()

        if "filters" in current_task and (
            current_task["filters"] is None or len(current_task["filters"]) == 0
        ):
            current_task.pop("filters")

        page_count = 0
        previous_offset_token = None  # ADDED: For infinite loop prevention

        while True:
            if not paginated and page_count > 0:
                break

            if page_count >= max_pages:
                self.logger.info(
                    f"Reached max page limit ({max_pages}) for endpoint {endpoint}."
                )
                break

            page_count += 1
            self.logger.info(
                f"Submitting task to {endpoint} (Page {page_count}/{max_pages})..."
            )

            request_tag = (
                tag + f":p{page_count}"
                if tag
                else endpoint.split("/")[-1] + f":p{page_count}"
            )
            response, cost = self._post_request(
                endpoint, [current_task], tag=request_tag
            )
            total_cost += cost

            if (
                not response
                or response.get("status_code") != 20000
                or response.get("tasks_error", 0) > 0
            ):
                self.logger.error(
                    f"Paging for endpoint {endpoint} failed on page {page_count}. Response: {response}"
                )
                break

            tasks = response.get("tasks", [])
            if not tasks or "result" not in tasks[0]:
                self.logger.info(
                    f"No 'result' field in the first task for endpoint {endpoint} on page {page_count}. Stopping pagination."
                )
                break

            task_result = tasks[0].get("result")
            if not task_result:
                self.logger.info(
                    f"Task result is empty for endpoint {endpoint} on page {page_count}. Stopping pagination."
                )
                break

            items_count = 0
            offset_token = None
            if task_result and isinstance(task_result, list) and len(task_result) > 0:
                offset_token = task_result[0].get("offset_token")
                for result_item in task_result:
                    # Capture items from the main list
                    items = result_item.get("items")
                    if items:
                        items_count += len(items)
                        all_items.extend(items)

                    # Capture the valuable seed_keyword_data if it exists (from Keyword Suggestions)
                    # and if this is specifically from the Keyword Suggestions API.
                    # This avoids adding the same seed_keyword twice if it was also in the 'items' list
                    # or if the main search (e.g., Keyword Ideas) already returned it.
                    if endpoint == self.LABS_KEYWORD_SUGGESTIONS:
                        seed_data = result_item.get("seed_keyword_data")
                        if isinstance(seed_data, dict) and seed_data.get("keyword"):
                            seed_data["discovery_source"] = (
                                "keyword_suggestions_seed"  # Mark its source
                            )
                            all_items.append(
                                DataForSEOMapper.sanitize_keyword_data_item(seed_data)
                            )  # ADDED SANITIZATION

            if not paginated or page_count >= max_pages or items_count == 0:
                break

            if offset_token:
                # ADDED: Infinite loop prevention check
                if offset_token == previous_offset_token:
                    self.logger.warning(
                        f"API returned a duplicate offset_token. Halting pagination to prevent infinite loop for endpoint {endpoint}."
                    )
                    break
                previous_offset_token = offset_token  # Update the previous token

                current_task = {
                    "offset_token": offset_token,
                    "limit": initial_task.get("limit", 1000),
                }
                if "filters" in initial_task and initial_task["filters"] is not None:
                    current_task["filters"] = initial_task["filters"]
                if "order_by" in initial_task and initial_task["order_by"] is not None:
                    current_task["order_by"] = initial_task["order_by"]

                time.sleep(1)
            else:
                break

        return all_items, total_cost

    def _group_urls_by_domain(
        self, urls: List[str], max_domains: int = 5, batch_size: int = 20
    ) -> List[List[str]]:
        """
        Groups URLs into batches that comply with the identical-domain limit and batch size.
        """
        from collections import defaultdict, deque

        domain_cache = {}

        def get_domain(url):
            if url not in domain_cache:
                try:
                    domain_cache[url] = urlparse(url).netloc
                except Exception:
                    self.logger.warning(f"Could not parse domain for URL: {url}")
                    domain_cache[url] = url
            return domain_cache[url]

        # Use deques for efficient popping from the left
        domain_groups = defaultdict(deque)
        for url in urls:
            domain_groups[get_domain(url)].append(url)

        batches = []

        # Continue as long as there are URLs to process
        while sum(len(q) for q in domain_groups.values()) > 0:
            current_batch = []
            domain_counts = defaultdict(int)

            # A set of domains that have reached their limit for the current batch
            exhausted_domains = set()

            # Loop until the batch is full or no more URLs can be added
            while len(current_batch) < batch_size:
                url_added_in_this_pass = False

                # Iterate through domains that have URLs and are not exhausted for this batch
                for domain, url_queue in domain_groups.items():
                    if len(current_batch) >= batch_size:
                        break

                    if url_queue and domain not in exhausted_domains:
                        if domain_counts[domain] < max_domains:
                            current_batch.append(url_queue.popleft())
                            domain_counts[domain] += 1
                            url_added_in_this_pass = True
                        else:
                            exhausted_domains.add(domain)

                # If we went through all domains and couldn't add a single URL, stop filling this batch
                if not url_added_in_this_pass:
                    break

            if current_batch:
                batches.append(current_batch)
            # If we created an empty batch and there are still urls, something is wrong.
            # This should not happen with this logic, but as a safeguard:
            elif sum(len(q) for q in domain_groups.values()) > 0:
                self.logger.error(
                    "Could not form a valid batch. Breaking to prevent infinite loop."
                )
                break

        self.logger.info(f"Grouped {len(urls)} URLs into {len(batches)} batches.")
        return batches

    def _convert_filters_to_api_format(
        self, filters: Optional[List[Dict[str, Any]]]
    ) -> Optional[List[Any]]:
        if not filters:
            return None

        api_filters = []
        for i, f in enumerate(filters):
            api_filters.append([f["field"], f["operator"], f["value"]])
            if i < len(filters) - 1:
                api_filters.append("and")
        return api_filters

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
        pages_to_fetch: Optional[int] = None,
        related_keywords_depth: Optional[int] = None,
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
        max_pages = pages_to_fetch or client_cfg.get("discovery_max_pages", 1)

        # Dynamic parameters (fall back to client_cfg if override is None)
        ignore_synonyms = (
            ignore_synonyms_override
            if ignore_synonyms_override is not None
            else client_cfg.get("discovery_ignore_synonyms", False)
        )
        include_clickstream = (
            include_clickstream_override
            if include_clickstream_override is not None
            else client_cfg.get("include_clickstream_data", False)
        )
        closely_variants = (
            closely_variants_override
            if closely_variants_override is not None
            else client_cfg.get("closely_variants", False)
        )
        exact_match = (
            exact_match_override
            if exact_match_override is not None
            else client_cfg.get("exact_match", False)
        )

        if "keyword_ideas" in discovery_modes:
            self.logger.info(
                f"Fetching keyword ideas for {len(seed_keywords)} seeds..."
            )
            ideas_endpoint = self.LABS_KEYWORD_IDEAS

            sanitized_ideas_filters = self._prioritize_and_limit_filters(
                self._convert_filters_to_api_format(filters.get("ideas"))
            )

            ideas_task = {
                "keywords": seed_keywords,
                "location_code": location_code,
                "language_code": language_code,
                "limit": self.keyword_ideas_limit,
                "include_serp_info": True,
                "ignore_synonyms": ignore_synonyms,
                "closely_variants": closely_variants,
                "filters": sanitized_ideas_filters,
                "order_by": order_by.get("ideas") if order_by else None,
                "include_clickstream_data": include_clickstream,
            }
            ideas_items, cost = self.post_with_paging(
                ideas_endpoint, ideas_task, max_pages=max_pages, tag="discovery_ideas"
            )
            total_cost += cost

            for item in ideas_items:
                item["discovery_source"] = "keyword_ideas"
                item["depth"] = 0
                all_items.append(DataForSEOMapper.sanitize_keyword_data_item(item))
            self.logger.info(f"Found {len(ideas_items)} ideas from Keyword Ideas API.")

        if "keyword_suggestions" in discovery_modes:
            self.logger.info("Fetching keyword suggestions in parallel...")
            suggestions_endpoint = self.LABS_KEYWORD_SUGGESTIONS
            with ThreadPoolExecutor(max_workers=10) as executor:
                future_to_seed = {}
                for seed_keyword in seed_keywords:
                    suggestions_task = {
                        "keyword": seed_keyword,
                        "location_code": location_code,
                        "language_code": language_code,
                        "limit": self.keyword_suggestions_limit,
                        "include_serp_info": True,
                        "exact_match": exact_match,
                        "ignore_synonyms": ignore_synonyms,
                        "include_seed_keyword": True,
                        "filters": self._prioritize_and_limit_filters(
                            self._convert_filters_to_api_format(filters.get("suggestions"))
                        ),
                        "order_by": order_by.get("suggestions") if order_by else None,
                        "include_clickstream_data": include_clickstream,
                    }
                    future = executor.submit(
                        self.post_with_paging,
                        suggestions_endpoint,
                        suggestions_task,
                        max_pages=max_pages,
                        tag=f"discovery_suggestions:{seed_keyword[:20]}",
                    )
                    future_to_seed[future] = seed_keyword

                for future in as_completed(future_to_seed):
                    seed = future_to_seed[future]
                    try:
                        suggestions_items, cost = future.result()
                        total_cost += cost
                        for item in suggestions_items:
                            item["discovery_source"] = "keyword_suggestions"
                            item["depth"] = 0
                            all_items.append(DataForSEOMapper.sanitize_keyword_data_item(item))
                        self.logger.info(f"Found {len(suggestions_items)} suggestions for '{seed}'.")
                    except Exception as exc:
                        self.logger.error(f"'{seed}' generated an exception: {exc}")

        if "related_keywords" in discovery_modes:
            self.logger.info("Fetching related keywords in parallel...")
            related_endpoint = self.LABS_RELATED_KEYWORDS
            with ThreadPoolExecutor(max_workers=10) as executor:
                future_to_seed = {}
                for seed in seed_keywords:
                    related_task = {
                        "keyword": seed,
                        "location_code": location_code,
                        "language_code": language_code,
                        "depth": related_keywords_depth or 1,
                        "limit": self.related_keywords_limit,
                        "include_serp_info": True,
                        "filters": self._prioritize_and_limit_filters(
                            self._convert_filters_to_api_format(filters.get("related"))
                        ),
                        "order_by": order_by.get("related") if order_by else None,
                        "include_clickstream_data": include_clickstream,
                        "replace_with_core_keyword": client_cfg.get(
                            "discovery_replace_with_core_keyword", False
                        ),
                    }
                    future = executor.submit(
                        self.post_with_paging,
                        related_endpoint,
                        related_task,
                        max_pages=max_pages,
                        tag=f"discovery_related:{seed[:20]}",
                    )
                    future_to_seed[future] = seed

                for future in as_completed(future_to_seed):
                    seed = future_to_seed[future]
                    try:
                        related_items, cost = future.result()
                        total_cost += cost
                        for item in related_items:
                            keyword_data = item.get("keyword_data")
                            if keyword_data:
                                keyword_data["discovery_source"] = "related"
                                keyword_data["depth"] = item.get("depth")
                                all_items.append(
                                    DataForSEOMapper.sanitize_keyword_data_item(keyword_data)
                                )
                    except Exception as exc:
                        self.logger.error(f"'{seed}' generated an exception: {exc}")
            self.logger.info(f"Total raw items from all sources: {len(all_items)}")

        return all_items, total_cost
