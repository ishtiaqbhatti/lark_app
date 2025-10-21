# backend/services/serp_analysis_service.py

from typing import Dict, Any, List
from backend.core.serp_analyzer import FullSerpAnalyzer
from backend.external_apis.dataforseo_client_v2 import DataForSEOClientV2


class SerpAnalysisService:
    def __init__(self, dataforseo_client: DataForSEOClientV2, config: Dict[str, Any]):
        self.serp_analyzer = FullSerpAnalyzer(dataforseo_client, config)
        self.dataforseo_client = dataforseo_client
        self.config = config

    def analyze_serp_for_blog_opportunity(
        self, serp_results: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Analyzes the SERP data to determine if there is a good opportunity for a blog article.
        """
        if not serp_results or not serp_results.get("top_organic_results"):
            return {
                "blog_opportunity": False,
                "opportunity_score": 0,
                "competitor_urls": [],
            }

        top_results = serp_results.get("top_organic_results", [])
        blog_count = 0
        competitor_urls = []

        for result in top_results[:10]:
            page_type = result.get("page_type")
            if page_type == "blog" or page_type == "news":
                blog_count += 1
                competitor_urls.append(result.get("url"))

        # Simple logic: if there are at least 3 blog/news articles in the top 10,
        # it's a good opportunity.
        blog_opportunity = blog_count >= 3
        opportunity_score = blog_count / 10.0

        return {
            "blog_opportunity": blog_opportunity,
            "opportunity_score": opportunity_score,
            "competitor_urls": competitor_urls,
        }

    def analyze_keywords_serp(
        self, keywords_data: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """
        Analyzes the SERP data for a list of keywords.
        """
        for keyword_data in keywords_data:
            keyword = keyword_data.get("keyword")
            if keyword:
                serp_results, _ = self.serp_analyzer.analyze_serp(keyword)
                serp_analysis = self.analyze_serp_for_blog_opportunity(serp_results)

                # Add competitor content if it's a blog opportunity
                if serp_analysis["blog_opportunity"]:
                    competitor_content, _ = (
                        self.dataforseo_client.get_content_onpage_data(
                            serp_analysis["competitor_urls"], self.config
                        )
                    )
                    serp_analysis["competitor_content"] = competitor_content
                else:
                    serp_analysis["competitor_content"] = []

                keyword_data["serp_analysis"] = serp_analysis

        return keywords_data
