# core/discovery_defaults.py
"""
Centralized configuration defaults for keyword discovery and disqualification rules.

This module contains all default thresholds, limits, and magic numbers used throughout
the discovery pipeline. Values can be overridden via client_cfg.

Usage:
    from core.discovery_defaults import DISCOVERY_DEFAULTS
    threshold = client_cfg.get("min_search_volume", DISCOVERY_DEFAULTS["MIN_SEARCH_VOLUME"])
"""

DISCOVERY_DEFAULTS = {
    # === SEARCH VOLUME THRESHOLDS ===
    "MIN_SEARCH_VOLUME": 100,
    "HIGH_VALUE_SV_OVERRIDE": 10000,
    
    # === KEYWORD DIFFICULTY LIMITS ===
    "MAX_KD_HARD_LIMIT": 70,
    "LONG_TAIL_KD_THRESHOLD": 30,  # KD threshold for long-tail opportunities
    
    # === TREND ANALYSIS ===
    "YEARLY_TREND_DECLINE_THRESHOLD": -25,  # Percent
    "QUARTERLY_TREND_DECLINE_THRESHOLD": 0,  # Percent
    "TREND_LOOKBACK_MONTHS": 4,
    "TREND_DECLINE_RATIO": 0.5,  # 50% decline triggers warning
    "SEARCH_VOLUME_VOLATILITY_THRESHOLD": 1.5,  # Std dev / mean ratio
    
    # === SEASONALITY DETECTION ===
    "STRONG_SEASONAL_FACTOR": 5.0,  # Peak is 5x average
    "MODERATE_SEASONAL_FACTOR": 3.0,  # Peak is 3x average
    "MILD_SEASONAL_FACTOR": 2.0,  # Peak is 2x average
    
    # === COMPETITION METRICS ===
    "MAX_PAID_COMPETITION_SCORE": 0.8,
    "MAX_HIGH_TOP_OF_PAGE_BID": 15.0,  # USD
    "HIGH_VALUE_CPC_OVERRIDE": 5.0,  # USD
    "MAX_REFERRING_MAIN_DOMAINS_LIMIT": 100,
    "MAX_AVG_DOMAIN_RANK_THRESHOLD": 500,
    "MAX_PAGES_TO_DOMAIN_RATIO": 15,
    
    # === KEYWORD STRUCTURE ===
    "MIN_KEYWORD_WORD_COUNT": 2,
    "MAX_KEYWORD_WORD_COUNT": 8,
    "LONG_TAIL_WORD_COUNT_THRESHOLD": 5,
    "LONG_TAIL_MIN_SEARCH_VOLUME": 20,  # Lower SV acceptable for long-tail
    
    # === SERP ANALYSIS ===
    "CROWDED_SERP_FEATURES_THRESHOLD": 4,
    "HOSTILE_SERP_FEATURE_COUNT_THRESHOLD": 3,  # Number of hostile features to trigger rejection
    "MIN_SERP_STABILITY_DAYS": 14,
    "STALE_SERP_DATA_THRESHOLD_DAYS": 90,  # 3 months
    
    # === SCORING THRESHOLDS ===
    "QUALIFIED_THRESHOLD": 70,  # Score to auto-qualify
    "REVIEW_THRESHOLD": 30,  # Score for manual review
    
    # === INTENT CONFIGURATION ===
    "ALLOWED_INTENTS": ["informational"],
    "PROHIBITED_INTENTS": ["navigational"],
    
    # === API BEHAVIOR ===
    "DISCOVERY_IGNORE_SYNONYMS": False,
    "INCLUDE_CLICKSTREAM_DATA": False,
    "CLOSELY_VARIANTS": True,  # Changed default to True
    "DISCOVERY_EXACT_MATCH": False,
    "DEFAULT_LIMIT": 700,
    "MAX_LIMIT": 1000,
    "DEFAULT_RELATED_KEYWORDS_DEPTH": 1,
    
    # === CONTENT PRODUCTION ESTIMATES ===
    "BASE_CONTENT_PRODUCTION_HOURS": 2,
    "BASE_WORD_COUNT": 1000,
    "VIDEO_PRODUCTION_HOURS_ADDITION": 8,
    "EXPERT_CONTENT_WORD_COUNT": 2000,
    "EXPERT_CONTENT_HOURS": 8,
    "HIGH_COMPETITION_WORD_COUNT": 3000,
    "HIGH_COMPETITION_HOURS": 12,
}

# Hostile SERP features that indicate non-blog-friendly SERPs
HOSTILE_SERP_FEATURES = {
    # E-commerce/Shopping
    "shopping",
    "popular_products",
    "refine_products",
    "explore_brands",
    # Local business
    "local_pack",
    "map",
    "local_services",
    # Google tools/utilities
    "google_flights",
    "google_hotels",
    "hotels_pack",
    "math_solver",
    "currency_box",
    "stocks_box",
    # Other specific intents
    "app",
    "jobs",
}

# SERP features that compete for attention but don't necessarily mean rejection
ATTENTION_COMPETING_FEATURES = {
    "carousel",
    "featured_snippet",
    "people_also_ask",
    "images",
    "video",
    "short_videos",
}

# Technical topic indicators for content difficulty assessment
TECHNICAL_TOPIC_INDICATORS = [
    "api", "algorithm", "architecture", "protocol", "encryption",
    "optimization", "configuration", "implementation", "integration",
    "debugging", "framework", "library", "sdk", "cli", "authentication",
    "authorization", "middleware", "backend", "frontend", "database",
    "query", "schema", "migration", "deployment", "devops", "cicd",
    "container", "kubernetes", "docker", "microservices", "serverless",
]

# Valid filter operators for API requests
VALID_FILTER_OPERATORS = [
    "regex", "not_regex", "<", "<=", ">", ">=", "=", "<>",
    "in", "not_in", "match", "not_match", "ilike", "not_ilike",
    "like", "not_like", "has_not"
]

# Fields forbidden from API filters (internal use only)
FORBIDDEN_API_FILTER_FIELDS = [
    "relevance",
    "sv_bing",
    "sv_clickstream",
]
