import logging
from typing import List, Dict, Any, Tuple

from external_apis.dataforseo_client_v2 import DataForSEOClientV2


class CompetitorAnalyzer:
    """
    Analyzes top organic competitors from SERP data.
    """

    def __init__(self, client: DataForSEOClientV2, config: Dict[str, Any]):
        self.client = client
        self.config = config
        self.logger = logging.getLogger(self.__class__.__name__)
        self.min_word_count = self.config.get("min_competitor_word_count", 300)

    def analyze_competitors(
        self, top_results: List[Dict[str, Any]]
    ) -> Tuple[List[Dict[str, Any]], float]:
        """
        Fetches OnPage data for top competitors and performs a basic analysis.
        """
        if not top_results:
            return [], 0.0

        # Limit the number of competitors to analyze based on config
        num_to_analyze = self.config.get("num_competitors_to_analyze", 5)
        competitor_urls = [
            res["url"] for res in top_results[:num_to_analyze] if res.get("url")
        ]

        onpage_results, cost = self.client.get_onpage_data_for_urls(competitor_urls)

        if not onpage_results:
            return [], cost

        analyzed_competitors = []
        for result in onpage_results:
            if "error" in result:
                self.logger.warning(
                    f"Could not analyze competitor {result.get('url')}: {result.get('error')}"
                )
                continue

            content_meta = result.get("meta", {}).get("content", {})
            word_count = content_meta.get("plain_text_word_count")
            if word_count and word_count >= self.min_word_count:
                analyzed_competitors.append(
                    {
                        "url": result.get("url"),
                        "word_count": word_count,
                        "readability_score": content_meta.get(
                            "flesch_kincaid_readability_index"
                        ),
                        "onpage_score": result.get("onpage_score"),
                        "internal_links": result.get("meta", {}).get(
                            "internal_links_count"
                        ),
                        "external_links": result.get("meta", {}).get(
                            "external_links_count"
                        ),
                        "headings": result.get("meta", {}).get("htags"),
                    }
                )

        return analyzed_competitors, cost
