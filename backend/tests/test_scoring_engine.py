import pytest
from pipeline.step_03_prioritization.scoring_engine import ScoringEngine

@pytest.fixture
def scoring_engine():
    # Provide a mock config with all necessary keys for scoring
    config = {
        "max_sv_for_scoring": 100000, "max_cpc_for_scoring": 10.0,
        "max_domain_rank_for_scoring": 1000, "max_referring_domains_for_scoring": 100,
        "ease_of_ranking_weight": 40, "traffic_potential_weight": 20,
        "commercial_intent_weight": 15, "competitor_weakness_weight": 10,
        # Add all other weights and config keys used by scoring components
    }
    return ScoringEngine(config)

def test_basic_scoring(scoring_engine):
    opportunity_data = {
        "keyword_info": {"search_volume": 5000, "cpc": 2.5},
        "keyword_properties": {"keyword_difficulty": 30},
        "avg_backlinks_info": {"main_domain_rank": 600, "referring_main_domains": 20},
        "search_intent_info": {"main_intent": "informational"},
        "serp_info": {"serp_item_types": ["featured_snippet"]}
    }
    score, breakdown = scoring_engine.calculate_score({"full_data": opportunity_data})
    assert 0 <= score <= 100
    assert "ease_of_ranking" in breakdown
    assert "traffic_potential" in breakdown
