import logging
from typing import List, Dict, Any, Tuple, Optional
from urllib.parse import urlparse
import textstat

from external_apis.dataforseo_client_v2 import DataForSEOClientV2


class FullCompetitorAnalyzer:
    """
    Performs a deep-dive analysis of top organic competitors using the OnPage Instant Pages API.
    """

    def __init__(self, client: DataForSEOClientV2, config: Dict[str, Any]):
        self.client = client
        self.config = config
        self.logger = logging.getLogger(self.__class__.__name__)
        self.min_word_count = self.config.get("min_competitor_word_count", 300)

        # Combine all blacklists dynamically

        excluded_domains_config = self.config.get(
            "competitor_analysis_excluded_domains", []
        )

        if isinstance(excluded_domains_config, str):
            excluded_domains = set(
                d.strip() for d in excluded_domains_config.split(",")
            )

        else:
            excluded_domains = set(excluded_domains_config)

        self.blacklist_domains = excluded_domains.union(
            set(self.config.get("ugc_and_parasite_domains", []))
        )

    def analyze_competitors(
        self, competitor_urls: List[str], selected_urls: Optional[List[str]] = None
    ) -> Tuple[List[Dict[str, Any]], float]:
        """
        Fetches and analyzes competitor data using a two-tier, adaptive fetching strategy.
        First attempts a cheap scan without JS, then retries failures with JS enabled.
        """
        urls_to_scan = selected_urls or competitor_urls
        if not urls_to_scan:
            return [], 0.0

        total_api_cost = 0.0
        successful_results = []
        urls_that_need_js_retry = []

        # --- Tier 1: Fast, cheap scan with JavaScript DISABLED ---
        self.logger.info(
            f"Starting Tier 1 analysis for {len(urls_to_scan)} URLs (JS disabled)."
        )
        try:
            initial_tasks, initial_cost = self.client.get_content_onpage_data(
                urls_to_scan, self.config, enable_javascript=False
            )
            total_api_cost += initial_cost

            for task in initial_tasks:
                task_url = task.get("data", {}).get("url")

                if task.get("result") is None:
                    self.logger.warning(
                        f"Tier 1 scan for {task_url} returned a null result. Queuing for JS-enabled retry."
                    )
                    urls_that_need_js_retry.append(task_url)
                    continue

                result = task.get("result", [{}])[0]

                if (
                    task.get("status_code") == 20000
                    and result.get("crawl_status") != "Page content is empty"
                    and result.get("items_count", 0) > 0
                ):
                    successful_results.extend(result.get("items", []))
                else:
                    self.logger.warning(
                        f"Tier 1 scan failed for {task_url}. Reason: {result.get('crawl_status', task.get('status_message'))}. Queuing for JS-enabled retry."
                    )
                    urls_that_need_js_retry.append(task_url)
        except Exception as e:
            self.logger.error(
                f"Error during Tier 1 competitor analysis: {e}", exc_info=True
            )

        # --- Tier 2: Slower, more expensive scan with JavaScript ENABLED for failures ---
        if urls_that_need_js_retry:
            self.logger.info(
                f"Starting Tier 2 analysis for {len(urls_that_need_js_retry)} failed URLs (JS enabled)."
            )
            try:
                retry_tasks, retry_cost = self.client.get_content_onpage_data(
                    urls_that_need_js_retry, self.config, enable_javascript=True
                )
                total_api_cost += retry_cost

                for task in retry_tasks:
                    task_url = task.get("data", {}).get("url")

                    if task.get("result") is None:
                        self.logger.error(
                            f"Tier 2 retry FAILED for {task_url}. Reason: API returned a null result. This URL will be excluded from analysis."
                        )
                        continue

                    result = task.get("result", [{}])[0]

                    if (
                        task.get("status_code") == 20000
                        and result.get("items_count", 0) > 0
                    ):
                        self.logger.info(
                            f"Tier 2 JS-enabled retry SUCCEEDED for {task_url}."
                        )
                        successful_results.extend(result.get("items", []))
                    else:
                        self.logger.error(
                            f"Tier 2 retry FAILED for {task_url}. Reason: {result.get('crawl_status', task.get('status_message'))}. This URL will be excluded from analysis."
                        )
            except Exception as e:
                self.logger.error(
                    f"Error during Tier 2 competitor analysis: {e}", exc_info=True
                )

        # --- Final Processing ---
        final_competitor_list = self._process_content_parsing_results(
            successful_results
        )

        return final_competitor_list, total_api_cost

    def _process_content_parsing_results(
        self, results: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """
        Processes the successful results from the Content Parsing API call into a standardized competitor object.
        """
        final_competitors = []
        for result in results:
            url = result.get("url")  # URL is at the top level in the new API response
            if not url or result.get("status_code") != 200:
                continue

            domain = urlparse(url).netloc
            if domain in self.blacklist_domains:
                self.logger.info(f"Skipping blacklisted competitor: {domain}")
                continue

            page_content = result.get("page_content", {})
            main_topic_content = ""
            headings = {"h1": [], "h2": [], "h3": [], "h4": [], "h5": [], "h6": []}

            # Extract main content and headings from the structured 'main_topic' array
            if page_content and page_content.get("main_topic"):
                for topic in page_content["main_topic"]:
                    h_level = topic.get("level")
                    h_title = topic.get("h_title")
                    if h_level and h_title:
                        tag = f"h{h_level}"
                        if tag in headings:
                            headings[tag].append(h_title)

                    if topic.get("primary_content"):
                        for pc in topic["primary_content"]:
                            if pc and pc.get("text"):
                                main_topic_content += pc["text"] + " "

            main_topic_content = main_topic_content.strip()

            # Manually calculate word count and readability
            word_count = len(main_topic_content.split())
            readability_score = None
            if (
                word_count > 100
            ):  # textstat needs a reasonable amount of text to be accurate
                try:
                    readability_score = textstat.flesch_kincaid_grade(
                        main_topic_content
                    )
                except Exception as e:
                    self.logger.warning(
                        f"Could not calculate readability for {url}: {e}"
                    )

            if word_count >= self.min_word_count:
                processed_competitor = {
                    "url": url,
                    "title": headings["h1"][0] if headings.get("h1") else None,
                    "word_count": word_count,
                    "readability_score": readability_score,
                    "headings": headings,
                    "main_content_text": main_topic_content,  # Clean text for readability calculation
                    "full_content_markdown": result.get(
                        "page_as_markdown"
                    ),  # Clean markdown for AI analysis
                    # Set technical fields to defaults as they are not available from this endpoint
                    "technical_warnings": [],
                    "page_timing": {},
                    "onpage_score": None,
                }
                final_competitors.append(processed_competitor)
            else:
                self.logger.info(
                    f"Skipping competitor {url} due to low parsed word count: {word_count}"
                )

        return final_competitors
