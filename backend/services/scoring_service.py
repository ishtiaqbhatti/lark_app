# services/scoring_service.py

from typing import Dict, Any, Tuple
from data_access.database_manager import DatabaseManager


class ScoringService:
    def __init__(self, db_manager: DatabaseManager):
        self.db_manager = db_manager

    def calculate_score(
        self, client_id: str, keyword_data: Dict[str, Any]
    ) -> Tuple[float, Dict[str, Any]]:
        """
        Calculates a strategic score for a keyword based on the client's qualification settings.
        """
        qualification_settings = self.db_manager.get_qualification_settings(client_id)

        traffic_potential_weight = qualification_settings.get(
            "traffic_potential_weight", 0
        )
        cpc_weight = qualification_settings.get("cpc_weight", 0)
        search_intent_weight = qualification_settings.get("search_intent_weight", 0)
        competitor_strength_weight = qualification_settings.get(
            "competitor_strength_weight", 0
        )
        serp_features_weight = qualification_settings.get("serp_features_weight", 0)
        trend_weight = qualification_settings.get("trend_weight", 0)
        seasonality_weight = qualification_settings.get("seasonality_weight", 0)
        serp_volatility_weight = qualification_settings.get("serp_volatility_weight", 0)

        search_volume = keyword_data.get(
            "keyword_info_normalized_with_clickstream", {}
        ).get("search_volume", 0)
        keyword_difficulty = keyword_data.get("keyword_properties", {}).get(
            "keyword_difficulty", 0
        )
        cpc = keyword_data.get("keyword_info", {}).get("cpc", 0)
        main_intent = keyword_data.get("search_intent_info", {}).get("main_intent")
        avg_referring_domains = keyword_data.get("avg_backlinks_info", {}).get(
            "referring_domains", 0
        )
        serp_item_types = keyword_data.get("serp_info", {}).get("serp_item_types", [])
        monthly_searches = keyword_data.get("keyword_info", {}).get(
            "monthly_searches", []
        )
        serp_last_updated_days_ago = keyword_data.get("serp_overview", {}).get(
            "serp_last_updated_days_ago"
        )
        serp_update_interval_days = keyword_data.get("serp_overview", {}).get(
            "serp_update_interval_days"
        )

        traffic_potential_score = search_volume * (1 - (keyword_difficulty / 100))
        cpc_score = cpc * 100
        competitor_strength_score = 100 - (avg_referring_domains / 10)
        serp_features_score = 0
        if "featured_snippet" in serp_item_types:
            serp_features_score += 20
        if "video" in serp_item_types:
            serp_features_score += 10
        if "ai_overview" in serp_item_types:
            serp_features_score -= 10

        trend_score = 0
        if len(monthly_searches) > 1:
            latest_search_volume = monthly_searches[0]["search_volume"]
            oldest_search_volume = monthly_searches[-1]["search_volume"]
            if oldest_search_volume > 0:
                trend_score = (
                    (latest_search_volume - oldest_search_volume) / oldest_search_volume
                ) * 100

        seasonality_score = 0
        if len(monthly_searches) > 11:
            # Calculate the average search volume for each month
            monthly_averages = [0] * 12
            for i in range(12):
                monthly_averages[i] = monthly_searches[i]["search_volume"]

            # Calculate the standard deviation of the monthly averages
            mean = sum(monthly_averages) / 12
            variance = sum([((x - mean) ** 2) for x in monthly_averages]) / 12
            std_dev = variance**0.5

            # Normalize the standard deviation to a score between 0 and 100
            if mean > 0:
                seasonality_score = 100 - (std_dev / mean) * 100

        serp_volatility_score = 0
        if (
            serp_last_updated_days_ago is not None
            and serp_update_interval_days is not None
        ):
            if serp_update_interval_days > 0:
                serp_volatility_score = (
                    100 - (serp_last_updated_days_ago / serp_update_interval_days) * 100
                )

        search_intent_score = 0
        if main_intent == "informational":
            search_intent_score = 100 * qualification_settings.get(
                "informational_intent_weight", 0
            )
        elif main_intent == "navigational":
            search_intent_score = 50 * qualification_settings.get(
                "navigational_intent_weight", 0
            )
        elif main_intent == "commercial":
            search_intent_score = 75 * qualification_settings.get(
                "commercial_intent_weight", 0
            )
        elif main_intent == "transactional":
            search_intent_score = 90 * qualification_settings.get(
                "transactional_intent_weight", 0
            )

        score = (
            (traffic_potential_score * traffic_potential_weight)
            + (cpc_score * cpc_weight)
            + (search_intent_score * search_intent_weight)
            + (competitor_strength_score * competitor_strength_weight)
            + (serp_features_score * serp_features_weight)
            + (trend_score * trend_weight)
            + (seasonality_score * seasonality_weight)
            + (serp_volatility_score * serp_volatility_weight)
        )

        breakdown = {
            "traffic_potential_score": traffic_potential_score,
            "cpc_score": cpc_score,
            "search_intent_score": search_intent_score,
            "competitor_strength_score": competitor_strength_score,
            "serp_features_score": serp_features_score,
            "trend_score": trend_score,
            "seasonality_score": seasonality_score,
            "serp_volatility_score": serp_volatility_score,
        }

        return score, breakdown
