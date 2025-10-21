-- data_access/migrations/017_add_strategies_table.sql

CREATE TABLE qualification_strategies (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    client_id TEXT NOT NULL,
    name TEXT NOT NULL,
    traffic_potential_weight REAL,
    keyword_difficulty_weight REAL,
    cpc_weight REAL,
    search_intent_weight REAL,
    min_search_volume INTEGER,
    max_keyword_difficulty INTEGER,
    negative_keywords TEXT,
    prohibited_intents TEXT,
    informational_intent_weight REAL,
    navigational_intent_weight REAL,
    commercial_intent_weight REAL,
    transactional_intent_weight REAL,
    competitor_strength_weight REAL,
    serp_features_weight REAL,
    trend_weight REAL,
    seasonality_weight REAL,
    serp_volatility_weight REAL,
    review_threshold REAL,
    disqualification_rules TEXT,
    brand_keywords TEXT,
    competitor_brand_keywords TEXT,
    FOREIGN KEY (client_id) REFERENCES clients (client_id)
);
