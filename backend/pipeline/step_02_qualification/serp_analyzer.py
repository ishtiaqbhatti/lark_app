import logging
from typing import Dict, Any, Tuple, Optional

from external_apis.dataforseo_client_v2 import DataForSEOClientV2
from datetime import datetime


class SerpAnalyzer:
    """
    Analyzes the SERP for a given keyword to extract key insights.
    """

    def __init__(self, client: DataForSEOClientV2, config: Dict[str, Any]):
        self.client = client
        self.config = config
        self.logger = logging.getLogger(self.__class__.__name__)

    def analyze_serp(self, keyword: str) -> Tuple[Optional[Dict[str, Any]], float]:
        """
        Fetches SERP data and extracts insights like featured snippets, PAA, etc.
        """
        location_code = self.config.get("location_code")
        language_code = self.config.get("language_code")

        serp_results, cost = self.client.get_serp_results(
            keyword, location_code, language_code
        )

        if not serp_results:
            return None, cost

        analysis = {
            "serp_has_featured_snippet": False,
            "serp_has_video_results": False,
            "serp_has_ai_overview": False,
            "people_also_ask": [],
            "top_organic_results": [],
            "serp_last_updated_days_ago": None,
        }

        item_types = serp_results.get("item_types", [])
        if "featured_snippet" in item_types:
            analysis["serp_has_featured_snippet"] = True
        if "video" in item_types:
            analysis["serp_has_video_results"] = True
        if "ai_overview" in item_types:
            analysis["serp_has_ai_overview"] = True

        # Extract PAA and top organic results
        for item in serp_results.get("items", []):
            if item.get("type") == "people_also_ask":
                analysis["people_also_ask"] = [
                    q.get("title") for q in item.get("items", []) if q.get("title")
                ]
            elif item.get("type") == "organic":
                analysis["top_organic_results"].append(
                    {
                        "rank": item.get("rank_absolute"),
                        "url": item.get("url"),
                        "title": item.get("title"),
                        "domain": item.get("domain"),
                        "main_domain_rank": item.get(
                            "main_domain_rank", 1000
                        ),  # Default to low rank
                    }
                )

        # Calculate SERP freshness
        datetime_str = serp_results.get("datetime")
        if datetime_str:
            try:
                serp_date = datetime.strptime(datetime_str, "%Y-%m-%d %H:%M:%S +00:00")
                analysis["serp_last_updated_days_ago"] = (
                    datetime.utcnow() - serp_date
                ).days
            except ValueError:
                self.logger.warning(f"Could not parse SERP datetime: {datetime_str}")

        return analysis, cost
