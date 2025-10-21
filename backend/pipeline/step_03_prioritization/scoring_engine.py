import logging
from typing import Dict, Any, Tuple
from .scoring_components import (
    calculate_ease_of_ranking_score,
    calculate_traffic_potential_score,
    calculate_commercial_intent_score,
    calculate_growth_trend_score,
    calculate_serp_features_score,
    calculate_serp_volatility_score,
    calculate_competitor_weakness_score,
    calculate_serp_crowding_score,
    calculate_keyword_structure_score,
    calculate_serp_threat_score,
    calculate_volume_volatility_score,
    calculate_serp_freshness_score,
    calculate_competitor_performance_score,  # ADDED THIS IMPORT
)


class ScoringEngine:
    """
    Calculates a strategic score for each keyword opportunity by orchestrating
    a suite of modular scoring components.
    """

    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.logger = logging.getLogger(self.__class__.__name__)

    def calculate_score(
        self, opportunity: Dict[str, Any]
    ) -> Tuple[float, Dict[str, Any]]:
        """
        Calculates the final opportunity score by combining weighted scores
        from all registered scoring components.
        """
        if not isinstance(opportunity, dict):
            self.logger.warning(
                "Invalid data format passed to calculate_score. Expected a dictionary."
            )
            return 0.0, {"error": "Invalid data format."}

        breakdown = {}
        data_source = opportunity.get("full_data", opportunity)

        # --- Execute all scoring components ---
        ease_score, ease_breakdown = calculate_ease_of_ranking_score(
            data_source, self.config
        )
        breakdown["ease_of_ranking"] = {
            "name": "Ease of Ranking",
            "score": ease_score,
            "breakdown": ease_breakdown,
        }

        traffic_score, traffic_breakdown = calculate_traffic_potential_score(
            data_source, self.config
        )
        breakdown["traffic_potential"] = {
            "name": "Traffic Potential",
            "score": traffic_score,
            "breakdown": traffic_breakdown,
        }

        intent_score, intent_breakdown = calculate_commercial_intent_score(
            data_source, self.config
        )
        breakdown["commercial_intent"] = {
            "name": "Commercial Intent",
            "score": intent_score,
            "breakdown": intent_breakdown,
        }

        trend_score, trend_breakdown = calculate_growth_trend_score(
            data_source, self.config
        )
        breakdown["growth_trend"] = {
            "name": "Growth Trend",
            "score": trend_score,
            "breakdown": trend_breakdown,
        }

        features_score, features_breakdown = calculate_serp_features_score(
            data_source, self.config
        )
        breakdown["serp_features"] = {
            "name": "SERP Opportunity",
            "score": features_score,
            "breakdown": features_breakdown,
        }

        volatility_score, volatility_breakdown = calculate_serp_volatility_score(
            data_source, self.config
        )
        breakdown["serp_volatility"] = {
            "name": "SERP Volatility",
            "score": volatility_score,
            "breakdown": volatility_breakdown,
        }

        weakness_score, weakness_breakdown = calculate_competitor_weakness_score(
            data_source, self.config
        )
        breakdown["competitor_weakness"] = {
            "name": "Competitor Weakness",
            "score": weakness_score,
            "breakdown": weakness_breakdown,
        }

        crowding_score, crowding_breakdown = calculate_serp_crowding_score(
            data_source, self.config
        )
        breakdown["serp_crowding"] = {
            "name": "SERP Crowding",
            "score": crowding_score,
            "breakdown": crowding_breakdown,
        }

        structure_score, structure_breakdown = calculate_keyword_structure_score(
            data_source, self.config
        )
        breakdown["keyword_structure"] = {
            "name": "Keyword Structure",
            "score": structure_score,
            "breakdown": structure_breakdown,
        }

        threat_score, threat_breakdown = calculate_serp_threat_score(
            data_source, self.config
        )
        breakdown["serp_threat"] = {
            "name": "SERP Threat",
            "score": threat_score,
            "breakdown": threat_breakdown,
        }

        volume_volatility_score, volume_volatility_breakdown = (
            calculate_volume_volatility_score(data_source, self.config)
        )
        breakdown["volume_volatility"] = {
            "name": "Volume Volatility",
            "score": volume_volatility_score,
            "breakdown": volume_volatility_breakdown,
        }

        freshness_score, freshness_breakdown = calculate_serp_freshness_score(
            data_source, self.config
        )
        breakdown["serp_freshness"] = {
            "name": "SERP Freshness",
            "score": freshness_score,
            "breakdown": freshness_breakdown,
        }

        performance_score, performance_breakdown = (
            calculate_competitor_performance_score(opportunity, self.config)
        )
        breakdown["competitor_performance"] = {
            "name": "Competitor Tech Performance",
            "score": performance_score,
            "breakdown": performance_breakdown,
        }
        # --- Apply weights from config and calculate final score ---
        weights = {
            "ease": self.config.get("ease_of_ranking_weight", 25),
            "traffic": self.config.get("traffic_potential_weight", 20),
            "intent": self.config.get("commercial_intent_weight", 15),
            "weakness": self.config.get("competitor_weakness_weight", 10),
            "structure": self.config.get("keyword_structure_weight", 5),
            "trend": self.config.get("growth_trend_weight", 5),
            "features": self.config.get("serp_features_weight", 5),
            "crowding": self.config.get("serp_crowding_weight", 5),
            "volatility": self.config.get("serp_volatility_weight", 5),
            "threat": self.config.get("serp_threat_weight", 5),
            "freshness": self.config.get("serp_freshness_weight", 0),
            "competitor_performance": self.config.get(
                "competitor_performance_weight", 5
            ),  # ADDED THIS LINE
            "volume_volatility": self.config.get("volume_volatility_weight", 0),
        }

        total_weight = sum(weights.values())
        if total_weight == 0:
            return 0.0, breakdown  # Avoid division by zero

        final_score = (
            (ease_score * weights["ease"])
            + (traffic_score * weights["traffic"])
            + (intent_score * weights["intent"])
            + (weakness_score * weights["weakness"])
            + (structure_score * weights["structure"])
            + (trend_score * weights["trend"])
            + (features_score * weights["features"])
            + (crowding_score * weights["crowding"])
            + (volatility_score * weights["volatility"])
            + (threat_score * weights["threat"])
            + (freshness_score * weights["freshness"])
            + (volume_volatility_score * weights["volume_volatility"])
            + (performance_score * weights["competitor_performance"])  # ADDED THIS LINE
        ) / total_weight

        for key, breakdown_data in breakdown.items():
            # Map breakdown key to weight key
            weight_key_map = {
                "ease_of_ranking": "ease",
                "traffic_potential": "traffic",
                "commercial_intent": "intent",
                "competitor_weakness": "weakness",
                "keyword_structure": "structure",
                "growth_trend": "trend",
                "serp_features": "features",
                "serp_crowding": "crowding",
                "serp_volatility": "volatility",
                "serp_threat": "threat",
                "volume_volatility": "volume_volatility",
                "serp_freshness": "freshness",
                "competitor_performance": "competitor_performance",  # ADDED THIS LINE
            }
            weight_key = weight_key_map.get(key, "")
            breakdown_data["weight"] = weights.get(weight_key, 0)

        return round(final_score, 2), breakdown
