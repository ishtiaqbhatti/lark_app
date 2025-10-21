-- data_access/migrations/001_add_new_tables.sql

CREATE TABLE keyword_info (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    opportunity_id INTEGER NOT NULL,
    search_volume INTEGER,
    keyword_difficulty INTEGER,
    cpc REAL,
    competition REAL,
    search_volume_trend TEXT,
    FOREIGN KEY (opportunity_id) REFERENCES opportunities (id)
);

CREATE TABLE serp_overview (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    opportunity_id INTEGER NOT NULL,
    serp_has_featured_snippet BOOLEAN,
    serp_has_video_results BOOLEAN,
    serp_has_ai_overview BOOLEAN,
    people_also_ask TEXT,
    ai_overview_content TEXT,
    featured_snippet_content TEXT,
    avg_referring_domains_top5_organic REAL,
    avg_main_domain_rank_top5_organic REAL,
    serp_last_updated_days_ago INTEGER,
    dominant_content_format TEXT,
    FOREIGN KEY (opportunity_id) REFERENCES opportunities (id)
);
