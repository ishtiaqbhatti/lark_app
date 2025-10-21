# services/qualification_service.py

from typing import List, Dict, Any, Optional
from .keyword_data_aggregator import KeywordDataAggregator
from .disqualification_service import DisqualificationService
from .scoring_service import ScoringService
from .serp_analysis_service import SerpAnalysisService


class QualificationService:
    def __init__(
        self,
        keyword_data_aggregator: KeywordDataAggregator,
        disqualification_service: DisqualificationService,
        scoring_service: ScoringService,
        serp_analysis_service: SerpAnalysisService,
    ):
        self.keyword_data_aggregator = keyword_data_aggregator
        self.disqualification_service = disqualification_service
        self.scoring_service = scoring_service
        self.serp_analysis_service = serp_analysis_service

    def qualify_keywords(
        self,
        client_id: str,
        seed_keywords: List[str],
        discovery_modes: List[str],
        filters: Optional[List[Any]],
        order_by: Optional[List[str]],
        limit: Optional[int],
        depth: Optional[int],
        ignore_synonyms: Optional[bool],
    ) -> List[Dict[str, Any]]:
        """
        Orchestrates the entire qualification flow.
        """
        keyword_data = self.keyword_data_aggregator.get_keyword_data(
            seed_keywords,
            discovery_modes,
            filters,
            order_by,
            limit,
            depth,
            ignore_synonyms,
        )

        analyzed_keywords = self.serp_analysis_service.analyze_keywords_serp(
            keyword_data
        )

        qualified_keywords = self.disqualification_service.disqualify(
            client_id, analyzed_keywords
        )

        scored_keywords = []
        for keyword in qualified_keywords:
            score, breakdown = self.scoring_service.calculate_score(client_id, keyword)
            keyword["strategic_score"] = score
            keyword["score_breakdown"] = breakdown
            scored_keywords.append(keyword)

        return scored_keywords
