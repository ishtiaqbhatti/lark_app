import logging
from typing import Dict, Any, Tuple, Optional
from external_apis.dataforseo_client_v2 import DataForSEOClientV2
from core import utils
from core.serp_analyzers.featured_snippet_analyzer import FeaturedSnippetAnalyzer
from core.serp_analyzers.video_analyzer import VideoAnalyzer
from core.serp_analyzers.pixel_ranking_analyzer import PixelRankingAnalyzer
from core.page_classifier import PageClassifier
from core.serp_analyzers.disqualification_analyzer import DisqualificationAnalyzer


class FullSerpAnalyzer:
    """
    Performs a comprehensive analysis of the SERP for a given keyword.
    """

    def __init__(self, client: DataForSEOClientV2, config: Dict[str, Any]):
        self.client = client
        self.config = config
        self.logger = logging.getLogger(self.__class__.__name__)
        self.featured_snippet_analyzer = FeaturedSnippetAnalyzer()
        self.video_analyzer = VideoAnalyzer()
        self.pixel_ranking_analyzer = PixelRankingAnalyzer()
        self.page_classifier = PageClassifier(config)
        self.disqualification_analyzer = DisqualificationAnalyzer()

    def analyze_serp(self, keyword: str) -> Tuple[Optional[Dict[str, Any]], float]:
        """
        Fetches SERP data and extracts a wide range of insights, including rich SERP elements.
        """
        high_cost_operators = [
            "allinanchor:",
            "allintext:",
            "allintitle:",
            "allinurl:",
            "define:",
            "filetype:",
            "id:",
            "inanchor:",
            "info:",
            "intext:",
            "intitle:",
            "inurl:",
            "link:",
            "site:",
        ]
        keyword_lower = keyword.lower()

        if any(op in keyword_lower for op in high_cost_operators):
            raise ValueError(
                f"Keyword '{keyword}' contains a high-cost search operator. Please remove it and try again."
            )

        location_code = self.config.get("location_code")
        language_code = self.config.get("language_code")
        serp_call_params = {}

        serp_call_params["depth"] = 10  # Default to depth 10 for quick fetch

        paa_click_depth = self.config.get("people_also_ask_click_depth", 0)
        if isinstance(paa_click_depth, int) and 1 <= paa_click_depth <= 4:
            serp_call_params["people_also_ask_click_depth"] = paa_click_depth

        device = self.config.get("device", "desktop")
        os_name = self.config.get("os", "windows")
        if device == "mobile" and os_name not in ["android", "ios"]:
            os_name = "android"
        serp_call_params["device"] = device
        serp_call_params["os"] = os_name

                serp_results, cost = self.client.get_serp_results(

                    keyword,

                    location_code,

                    language_code,

                    client_cfg=self.config,

                    serp_call_params=serp_call_params,

                )

        

                if not serp_results:

                    self.logger.error(f"Failed to retrieve SERP results for keyword '{keyword}'")

                    return None, cost

                

                if not isinstance(serp_results, dict):

                    self.logger.error(f"SERP results is not a dictionary for keyword '{keyword}': {type(serp_results)}")

                    return None, cost

                

                if not serp_results.get("items"):

                    self.logger.warning(f"SERP results contain no items for keyword '{keyword}'")

                    return None, cost

        serp_times = utils.calculate_serp_times(
            serp_results.get("datetime"), serp_results.get("previous_updated_time")
        )

        analysis = {
            "serp_has_ai_overview": "ai_overview" in serp_results.get("item_types", []),
            "has_popular_products": "popular_products"
            in serp_results.get("item_types", []),
            "people_also_ask": [],  # Kept for backward compatibility, new field below is preferred
            "paa_questions": [],  # Primary field for cleaned PAA questions
            "top_organic_results": [],
            "related_searches": [],
            "knowledge_graph_data": {},  # Kept for backward compatibility
            "knowledge_graph_facts": [],  # NEW: Structured facts from KG
            "paid_ad_copy": [],  # NEW: Top paid ad titles/descriptions
            "ai_overview_content": None,
            "ai_overview_sources": [],  # NEW: URLs from AI Overview references
            "top_organic_faqs": [],  # NEW: FAQ questions from organic results
            "top_organic_sitelinks": [],  # NEW: Sitelinks from organic results
            "discussion_snippets": [],  # NEW: Snippets from discussions/forums/perspectives
            "product_considerations_summary": None,
            "refinement_chips": [],
            "extracted_serp_features": [],
            "serp_last_updated_days_ago": serp_times.get("days_ago"),
            "serp_update_interval_days": serp_times.get("update_interval_days"),
            "dominant_content_format": "Article",
        }

        analysis.update(self.featured_snippet_analyzer.analyze(serp_results))
        analysis.update(self.video_analyzer.analyze(serp_results))
        analysis.update(self.pixel_ranking_analyzer.analyze(serp_results))

        for item in serp_results.get("items") or []:
            item_type = item.get("type")

            # Organic Results
            if item_type == "organic":
                organic_result = {
                    "rank": item.get("rank_absolute"),
                    "url": item.get("url"),
                    "title": item.get("title"),
                    "domain": item.get("domain"),
                    "description": item.get("description"),
                    "page_type": self.page_classifier.classify(
                        item.get("url"), item.get("domain"), item.get("title")
                    ),
                }
                if item.get("rating"):
                    organic_result["rating"] = {
                        "value": item["rating"].get("value"),
                        "votes_count": item["rating"].get("votes_count"),
                        "rating_max": item["rating"].get("rating_max"),
                    }
                if item.get("about_this_result"):
                    organic_result["about_this_result_source_info"] = item[
                        "about_this_result"
                    ].get("source_info")
                    organic_result["about_this_result_search_terms"] = item[
                        "about_this_result"
                    ].get("search_terms")
                    organic_result["about_this_result_related_terms"] = item[
                        "about_this_result"
                    ].get("related_terms")

                # NEW: Extract FAQ and Sitelinks directly from organic results
                if item.get("faq") and item["faq"].get("items"):
                    analysis["top_organic_faqs"].extend(
                        [
                            faq_item.get("title")
                            for faq_item in item["faq"]["items"]
                            if faq_item.get("title")
                        ]
                    )
                if item.get("links"):
                    analysis["top_organic_sitelinks"].extend(
                        [
                            link.get("title")
                            for link in item["links"]
                            if link.get("title")
                        ]
                    )

                analysis["top_organic_results"].append(organic_result)

            # Paid Ads
            elif item_type == "paid":
                if item.get("title") and item.get("description"):
                    analysis["paid_ad_copy"].append(
                        {
                            "title": item.get("title"),
                            "description": item.get("description"),
                            "url": item.get("url"),
                        }
                    )

            # People Also Ask (PAA)
            elif item_type == "people_also_ask":
                all_paa_questions = []
                for paa_item in item.get("items") or []:
                    if paa_item and paa_item.get("title"):
                        (all_paa_questions.append(paa_item.get("title")),)
                    if paa_item and paa_item.get("expanded_element"):
                        for expanded_item in paa_item.get("expanded_element") or []:
                            if expanded_item and expanded_item.get("title"):
                                (all_paa_questions.append(expanded_item.get("title")),)
                analysis["paa_questions"] = list(set(all_paa_questions))
                analysis["people_also_ask"] = analysis[
                    "paa_questions"
                ]  # For backward compatibility

            # Knowledge Graph
            elif item_type == "knowledge_graph":
                analysis["knowledge_graph_data"] = {  # For backward compatibility
                    "title": item.get("title"),
                    "description": item.get("description"),
                    "url": item.get("url"),
                    "image_url": item.get("image_url"),
                }
                # NEW: Deep parse Knowledge Graph structured items
                if item.get("items"):
                    for kg_sub_item in item["items"]:
                        if (
                            kg_sub_item
                            and kg_sub_item.get("type") == "knowledge_graph_row_item"
                        ):
                            analysis["knowledge_graph_facts"].append(
                                f"{kg_sub_item.get('title')}: {kg_sub_item.get('text')}"
                            )
                        elif (
                            kg_sub_item
                            and kg_sub_item.get("type")
                            == "knowledge_graph_carousel_item"
                            and kg_sub_item.get("items")
                        ):
                            analysis["knowledge_graph_facts"].extend(
                                [
                                    carousel_el.get("title")
                                    for carousel_el in kg_sub_item["items"]
                                    if carousel_el.get("title")
                                ]
                            )
                        elif (
                            kg_sub_item
                            and kg_sub_item.get("type") == "knowledge_graph_list_item"
                            and kg_sub_item.get("items")
                        ):
                            analysis["knowledge_graph_facts"].extend(
                                [
                                    list_el.get("title")
                                    for list_el in kg_sub_item["items"]
                                    if list_el.get("title")
                                ]
                            )

            # AI Overview
            elif item_type == "ai_overview":
                ai_items = item.get("items") or []
                ai_parts = [
                    sub_item.get("markdown")
                    for sub_item in ai_items
                    if sub_item and sub_item.get("markdown")
                ]
                analysis["ai_overview_content"] = "\n".join(ai_parts)
                # NEW: Extract AI Overview References
                for sub_item in ai_items:
                    if sub_item and sub_item.get("references"):
                        analysis["ai_overview_sources"].extend(
                            [
                                ref.get("url")
                                for ref in sub_item["references"]
                                if ref.get("url")
                            ]
                        )

            # Discussions and Forums / Perspectives
            elif item_type in [
                "discussions_and_forums",
                "perspectives",
            ]:  # Combined handling
                if item.get("items"):
                    analysis["discussion_snippets"].extend(
                        [
                            d_item.get("title")
                            for d_item in item["items"]
                            if d_item.get("title")
                        ]
                    )

            # Related Searches
            elif item_type == "related_searches":
                related_items = item.get("items") or []
                for s in related_items:
                    if isinstance(s, str):
                        analysis["related_searches"].append(s)
                    elif isinstance(s, dict) and s.get("title"):
                        (analysis["related_searches"].append(s.get("title")),)

            # Product Considerations (existing)
            elif item_type == "product_considerations":
                title = item.get("title")
                items = item.get("items") or []
                if title and items:
                    considerations = [
                        sub.get("title") for sub in items if sub and sub.get("title")
                    ]
                    analysis["product_considerations_summary"] = (
                        f"{title}: {', '.join(considerations)}"
                    )

        # Deduplicate all lists
        analysis["ai_overview_sources"] = list(set(analysis["ai_overview_sources"]))
        analysis["top_organic_faqs"] = list(set(analysis["top_organic_faqs"]))
        analysis["top_organic_sitelinks"] = list(set(analysis["top_organic_sitelinks"]))
        analysis["discussion_snippets"] = list(set(analysis["discussion_snippets"]))

        # Determine dominant content format (existing logic)
        # ...

        disqualification_results = self.disqualification_analyzer.analyze(
            analysis, self.config
        )
        analysis.update(disqualification_results)

        return analysis, cost
