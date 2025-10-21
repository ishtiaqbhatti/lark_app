# data_access/queries.py

# --- Table Creation ---
CREATE_OPPORTUNITIES_TABLE = """
CREATE TABLE IF NOT EXISTS opportunities (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    keyword TEXT NOT NULL,
    status TEXT NOT NULL DEFAULT 'pending',
    client_id TEXT NOT NULL DEFAULT 'default',
    date_added TEXT NOT NULL,
    date_processed TEXT,
    strategic_score REAL,
    blog_qualification_status TEXT,
    blog_qualification_reason TEXT,
    keyword_info TEXT,
    keyword_properties TEXT,
    search_intent_info TEXT,
    serp_overview TEXT,
    score_breakdown TEXT,
    full_data TEXT NOT NULL,
    blueprint_data TEXT,
    ai_content_json TEXT,
    ai_content_model TEXT,
    featured_image_url TEXT,
    featured_image_local_path TEXT,
    in_article_images_data TEXT,
    social_media_posts_json TEXT,
    social_media_posts_status TEXT DEFAULT 'draft', -- NEW COLUMN
    last_workflow_step TEXT,
    error_message TEXT,
    wordpress_payload_json TEXT,
    final_package_json TEXT,
    slug TEXT UNIQUE,
    run_id INTEGER,
    keyword_info_normalized_with_bing TEXT,
    keyword_info_normalized_with_clickstream TEXT,
    monthly_searches TEXT,
    traffic_value REAL DEFAULT 0,
    check_url TEXT,
    related_keywords TEXT,
    keyword_categories TEXT,
     core_keyword TEXT,
    published_url TEXT,
     UNIQUE(keyword, client_id)
 );"""

CREATE_CLIENTS_TABLE = """
CREATE TABLE IF NOT EXISTS clients (
    client_id TEXT PRIMARY KEY,
    client_name TEXT NOT NULL,
    date_created TEXT NOT NULL
);
"""

CREATE_CLIENT_SETTINGS_TABLE = """
CREATE TABLE IF NOT EXISTS client_settings (
    client_id TEXT PRIMARY KEY,
    openai_api_key TEXT,
    pexels_api_key TEXT,
    location_code INTEGER,
    language_code TEXT,
    target_domain TEXT,
    device TEXT,
    os TEXT,
    informational_score REAL,
    commercial_score REAL,
    transactional_score REAL,
    navigational_score REAL,
    question_keyword_bonus REAL,
    ease_of_ranking_weight INTEGER,
    traffic_potential_weight INTEGER,
    commercial_intent_weight INTEGER,
    growth_trend_weight INTEGER,
    serp_features_weight INTEGER,
    serp_freshness_weight INTEGER,
    serp_volatility_weight INTEGER,
    competitor_weakness_weight INTEGER,
    max_cpc_for_scoring REAL,
    max_sv_for_scoring INTEGER,
    max_domain_rank_for_scoring INTEGER,
    max_referring_domains_for_scoring INTEGER,
    max_avg_referring_domains_filter INTEGER,
    featured_snippet_bonus REAL,
    ai_overview_bonus REAL,
    serp_freshness_bonus_max REAL,
    serp_freshness_old_threshold_days INTEGER,
    serp_volatility_stable_threshold_days INTEGER,
    enforce_intent_filter INTEGER,
    allowed_intents TEXT,
    require_question_keywords INTEGER,
    negative_keywords TEXT,
    min_monthly_trend_percentage REAL,
    min_competitor_word_count INTEGER,
    max_competitor_technical_warnings INTEGER,
    competitor_blacklist_domains TEXT,
    ugc_and_parasite_domains TEXT,
    num_competitors_to_analyze INTEGER,
    num_common_headings INTEGER,
    num_unique_angles INTEGER,
    max_initial_serp_urls_to_analyze INTEGER,
    calculate_rectangles INTEGER,
    people_also_ask_click_depth INTEGER,
    min_search_volume INTEGER,
    max_keyword_difficulty INTEGER,
    ai_content_model TEXT,
    num_in_article_images INTEGER,
    use_pexels_first INTEGER,
    cleanup_local_images INTEGER,
    onpage_enable_javascript INTEGER,
    onpage_load_resources INTEGER,
    onpage_disable_cookie_popup INTEGER,
    onpage_return_despite_timeout INTEGER,
    onpage_enable_browser_rendering INTEGER,
    onpage_store_raw_html INTEGER,
    onpage_validate_micromarkup INTEGER,
    onpage_check_spell INTEGER,
    onpage_accept_language TEXT,
    onpage_custom_user_agent TEXT,
    onpage_max_domains_per_request INTEGER,
    onpage_max_tasks_per_request INTEGER,
    onpage_enable_switch_pool INTEGER,
    onpage_browser_screen_resolution_ratio REAL,
    discovery_exact_match INTEGER,
    onpage_enable_custom_js INTEGER,
    onpage_custom_js TEXT,
    platforms TEXT,


    enable_automated_internal_linking INTEGER,
    db_type TEXT,
    max_words_for_ai_analysis INTEGER,
    ai_generation_temperature REAL,
    recommended_word_count_multiplier REAL,
    max_avg_lcp_time INTEGER,
    prohibited_intents TEXT,
    load_async_ai_overview INTEGER,
    onpage_custom_checks_thresholds TEXT,
    serp_remove_from_url_params TEXT,
     schema_author_type TEXT,
     client_knowledge_base TEXT,
    wordpress_url TEXT,
    wordpress_user TEXT,
    wordpress_app_password TEXT,
    wordpress_seo_plugin TEXT,
    default_wordpress_categories TEXT,
    default_wordpress_tags TEXT,
     last_updated TEXT NOT NULL,
     FOREIGN KEY (client_id) REFERENCES clients (client_id)
 );"""

INSERT_CLIENT_SETTINGS = """
INSERT INTO client_settings (client_id, brand_tone, target_audience, terms_to_avoid) VALUES (%s, %s, %s, %s)
ON CONFLICT (client_id) DO UPDATE SET brand_tone = %s, target_audience = %s, terms_to_avoid = %s
"""

SELECT_CLIENT_SETTINGS = """
SELECT brand_tone, target_audience, terms_to_avoid FROM client_settings WHERE client_id = %s;
"""

CREATE_DISCOVERY_RUNS_TABLE = """
CREATE TABLE IF NOT EXISTS discovery_runs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    client_id TEXT NOT NULL,
    start_time TEXT NOT NULL,
    end_time TEXT,
    status TEXT NOT NULL,
    parameters TEXT,
    results_summary TEXT,
    log_file_path TEXT,
    error_message TEXT,
    FOREIGN KEY (client_id) REFERENCES clients (client_id)
);
"""

CREATE_SCHEMA_VERSION_TABLE = """
CREATE TABLE IF NOT EXISTS schema_version (
    version INTEGER PRIMARY KEY,
    applied_at TEXT NOT NULL
);
"""

# NEW: Add a query to get current schema version
GET_SCHEMA_VERSION = """
SELECT version FROM schema_version ORDER BY version DESC LIMIT 1;
"""

# NEW: Add a query to insert schema version
INSERT_SCHEMA_VERSION = """
INSERT INTO schema_version (version, applied_at) VALUES (?, ?);
"""

CREATE_API_CACHE_TABLE = """
CREATE TABLE IF NOT EXISTS api_cache (
    key TEXT PRIMARY KEY,
    data TEXT NOT NULL,
    timestamp REAL NOT NULL,
    ttl_days INTEGER NOT NULL
);
"""

# --- Cache table queries (related to migration 002_add_slug_and_cache_table.sql)
INSERT_API_CACHE = """
INSERT OR REPLACE INTO api_cache (key, data, timestamp, ttl_days)
VALUES (?, ?, ?, ?);
"""

SELECT_API_CACHE = """
SELECT data, timestamp, ttl_days FROM api_cache WHERE key = ?;
"""

DELETE_EXPIRED_API_CACHE = """
DELETE FROM api_cache WHERE timestamp + (ttl_days * 86400) < ?;
"""

DELETE_API_CACHE_BY_KEY = """
DELETE FROM api_cache WHERE key = ?;
"""

TRUNCATE_API_CACHE = """
DELETE FROM api_cache;
"""

# --- Opportunity Queries ---
INSERT_OPPORTUNITY_OR_IGNORE = """
INSERT OR IGNORE INTO opportunities 
(keyword, client_id, date_added, full_data)
VALUES (?, ?, ?, ?);
"""

INSERT_OPPORTUNITY_WITH_BLUEPRINT = """
INSERT OR IGNORE INTO opportunities
(keyword, client_id, date_added, full_data, blueprint_data, slug)
VALUES (?, ?, ?, ?, ?, ?);
"""

SELECT_PENDING_OPPORTUNITIES = """
SELECT * FROM opportunities 
WHERE status = 'pending' AND client_id = ?;
"""

SELECT_ALL_OPPORTUNITIES_BY_CLIENT = """
SELECT * FROM opportunities 
WHERE client_id = ?
ORDER BY date_added DESC;
"""

SELECT_OPPORTUNITY_BY_ID = """
SELECT * FROM opportunities WHERE id = ?;
"""

SELECT_ALL_PROCESSED_KEYWORDS = """
SELECT keyword FROM opportunities 
WHERE client_id = ? AND status NOT IN ('rejected', 'failed');
"""

UPDATE_OPPORTUNITY_STATUS_WITH_DATE = """
UPDATE opportunities SET status = ?, date_processed = ? WHERE id = ?;
"""

UPDATE_OPPORTUNITY_STATUS = """
UPDATE opportunities SET status = ? WHERE id = ?;
"""

UPDATE_OPPORTUNITY_WORKFLOW_STATE = """
UPDATE opportunities SET last_workflow_step = ?, status = ?, error_message = ? WHERE id = ?;
"""

UPDATE_OPPORTUNITY_BLUEPRINT = """
UPDATE opportunities
SET blueprint_data = ?
WHERE id = ?;
"""

UPDATE_OPPORTUNITY_BLUEPRINT_AND_SLUG = """
UPDATE opportunities
SET blueprint_data = ?, slug = ?
WHERE id = ?;
"""

UPDATE_OPPORTUNITY_AI_CONTENT = """
UPDATE opportunities
SET ai_content_json = ?, ai_content_model = ?, date_processed = ?
WHERE id = ?;
"""

UPDATE_OPPORTUNITY_IMAGES = """
UPDATE opportunities SET featured_image_url = ?, featured_image_local_path = ?, in_article_images_data = ? WHERE id = ?;
"""

UPDATE_OPPORTUNITY_SOCIAL_POSTS = """
UPDATE opportunities SET social_media_posts_json = ? WHERE id = ?;
"""

SELECT_ALL_OPPORTUNITIES_FOR_EXPORT = """
SELECT * FROM opportunities ORDER BY client_id, date_added DESC;
"""

SELECT_PROCESSED_OPPORTUNITIES = """
SELECT * FROM opportunities
WHERE client_id = ? AND blueprint_data IS NOT NULL
ORDER BY date_processed DESC;
"""

UPDATE_OPPORTUNITY_WORDPRESS_PAYLOAD = (
    "UPDATE opportunities SET wordpress_payload_json = ? WHERE id = ?;"
)

UPDATE_OPPORTUNITY_FINAL_PACKAGE = (
    "UPDATE opportunities SET final_package_json = ? WHERE id = ?;"
)

# --- Dashboard Queries ---
COUNT_OPPORTUNITIES_BY_STATUS = """
SELECT status, COUNT(*) as count FROM opportunities WHERE client_id = ? GROUP BY status;
"""

SUM_DISCOVERY_COST_BY_CLIENT = """
SELECT SUM(CAST(JSON_EXTRACT(results_summary, '$.total_cost') AS REAL)) FROM discovery_runs WHERE client_id = ?;
"""

SUM_ANALYSIS_COST_BY_CLIENT = """
SELECT SUM(CAST(JSON_EXTRACT(blueprint_data, '$.metadata.total_api_cost') AS REAL)) FROM opportunities WHERE client_id = ?;
"""

SELECT_RECENTLY_GENERATED = """
SELECT id, keyword, status, date_processed FROM opportunities 
WHERE client_id = ? AND status = 'generated' 
ORDER BY date_processed DESC 
LIMIT 5;
"""


# --- Client Queries ---
INSERT_CLIENT = """
INSERT INTO clients (client_id, client_name, date_created) VALUES (?, ?, ?);
"""

SELECT_ALL_CLIENTS = """
SELECT client_id, client_name FROM clients ORDER BY date_created DESC;
"""

SELECT_CLIENT_SETTINGS = """
SELECT * FROM client_settings WHERE client_id = ?;
"""

# --- Discovery Run Queries ---
INSERT_DISCOVERY_RUN = """
INSERT INTO discovery_runs (client_id, start_time, status, parameters)
VALUES (?, ?, ?, ?);
"""

UPDATE_DISCOVERY_RUN_STATUS = """
UPDATE discovery_runs SET status = ? WHERE id = ?;
"""

UPDATE_DISCOVERY_RUN_COMPLETED = """
UPDATE discovery_runs SET end_time = ?, status = 'completed', results_summary = ? WHERE id = ?;
"""

UPDATE_DISCOVERY_RUN_FAILED = """
UPDATE discovery_runs SET end_time = ?, status = 'failed', error_message = ? WHERE id = ?;
"""

SELECT_ALL_DISCOVERY_RUNS_BY_CLIENT = """
SELECT * FROM discovery_runs WHERE client_id = ? ORDER BY start_time DESC;
"""

SELECT_ALL_DISCOVERY_RUNS_BY_CLIENT_PAGINATED = """
SELECT * FROM discovery_runs WHERE client_id = ? ORDER BY start_time DESC LIMIT ? OFFSET ?;
"""

SELECT_DISCOVERY_RUN_BY_ID = """
SELECT * FROM discovery_runs WHERE id = ?;
"""

SELECT_KEYWORDS_FOR_RUN_BY_REASON = """
SELECT * FROM opportunities WHERE run_id = ? AND blog_qualification_reason = ?;
"""

UPDATE_DISCOVERY_RUN_LOG_PATH = """
UPDATE discovery_runs SET log_file_path = ? WHERE id = ?;
"""

SELECT_OPPORTUNITY_BY_SLUG = """

SELECT * FROM opportunities WHERE slug = ?;

"""


CREATE_JOBS_TABLE = """

CREATE TABLE IF NOT EXISTS jobs (

    id TEXT PRIMARY KEY,

    status TEXT NOT NULL,

    progress INTEGER NOT NULL,

    result TEXT,

    error TEXT,

    started_at REAL NOT NULL,

    finished_at REAL

);

"""

GET_JOB = "SELECT * FROM jobs WHERE id = ?;"

UPDATE_JOB_STATUS_DIRECT = """
UPDATE jobs SET status = ?, progress = ?, finished_at = ? WHERE id = ?;
"""

UPDATE_JOB = """

INSERT OR REPLACE INTO jobs (id, status, progress, result, error, started_at, finished_at)

VALUES (?, ?, ?, ?, ?, ?, ?);

"""

GET_ALL_JOBS = "SELECT * FROM jobs ORDER BY started_at DESC LIMIT 100;"

CREATE_CONTENT_HISTORY_TABLE = """
CREATE TABLE IF NOT EXISTS content_history (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    opportunity_id INTEGER NOT NULL,
    timestamp TEXT NOT NULL,
    ai_content_json TEXT NOT NULL,
    restored_from_id INTEGER,
    FOREIGN KEY (opportunity_id) REFERENCES opportunities (id)
);
"""

# In data_access/queries.py, add history queries:
INSERT_CONTENT_HISTORY = """
INSERT INTO content_history
(opportunity_id, timestamp, ai_content_json)
VALUES (?, ?, ?);
"""

SELECT_CONTENT_HISTORY_BY_OPP_ID = """
SELECT id, opportunity_id, timestamp, ai_content_json FROM content_history
WHERE opportunity_id = ?
ORDER BY timestamp DESC;
"""

# Update/Add status update query:
UPDATE_OPPORTUNITY_AI_CONTENT_AND_STATUS = """
UPDATE opportunities
SET ai_content_json = ?, ai_content_model = ?, date_processed = ?, status = ?
WHERE id = ?;
"""

# In data_access/queries.py, define template queries:
COUNT_ALL_OPPORTUNITIES_BY_CLIENT = """
SELECT COUNT(*) FROM opportunities
WHERE client_id = ? 
"""

SELECT_ALL_OPPORTUNITIES_PAGINATED = """
SELECT {select_columns} FROM opportunities
WHERE client_id = ? {where_clause}
ORDER BY {order_by} {order_direction}
LIMIT ? OFFSET ?;
"""

SEARCH_OPPORTUNITIES_BY_KEYWORD = """
SELECT id, keyword, status FROM opportunities
WHERE client_id = ? AND keyword LIKE ?
ORDER BY date_added DESC
LIMIT 20;
"""

SELECT_HIGH_PRIORITY_OPPORTUNITIES = """
SELECT id, keyword, strategic_score, score_breakdown, keyword_info, keyword_properties, traffic_value FROM opportunities
WHERE client_id = ? AND status = 'validated'
ORDER BY strategic_score DESC
LIMIT ?;
"""

SELECT_ACTION_ITEMS = """
SELECT id, keyword, status, error_message, COALESCE(date_processed, date_added) as updated_at, strategic_score FROM opportunities
WHERE client_id = ? AND status IN ('paused_for_approval', 'failed')
ORDER BY updated_at DESC;
"""

CREATE_CONTENT_FEEDBACK_TABLE = """
CREATE TABLE IF NOT EXISTS content_feedback (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    opportunity_id INTEGER NOT NULL,
    rating INTEGER NOT NULL, -- 1-5 scale
    comments TEXT,
    timestamp TEXT NOT NULL,
    FOREIGN KEY (opportunity_id) REFERENCES opportunities (id)
);
"""

INSERT_CONTENT_FEEDBACK = """
INSERT INTO content_feedback (opportunity_id, rating, comments, timestamp)
VALUES (?, ?, ?, ?);
"""

UPDATE_OPPORTUNITY_SCORES = """
UPDATE opportunities
SET strategic_score = ?, score_breakdown = ?, blueprint_data = ?
WHERE id = ?;
"""

UPDATE_GENERATED_CONTENT_AND_STATUS = """
UPDATE opportunities
SET
    ai_content_json = ?,
    ai_content_model = ?,
    featured_image_url = ?,
    featured_image_local_path = ?,
    in_article_images_data = ?,
    social_media_posts_json = ?,
    final_package_json = ?,
    status = 'generated',
    last_workflow_step = 'generation_complete',
    date_processed = ?,
    total_api_cost = ?
WHERE id = ?;
"""

INSERT_DEFAULT_QUALIFICATION_SETTINGS = """
INSERT INTO qualification_settings (
    client_id, ease_of_ranking_weight, traffic_potential_weight, commercial_intent_weight,
    serp_features_weight, growth_trend_weight, serp_freshness_weight, serp_volatility_weight,
    competitor_weakness_weight, competitor_performance_weight, min_search_volume, max_keyword_difficulty,
    negative_keywords, prohibited_intents, max_y_pixel_threshold,
    max_forum_results_in_top_10, max_ecommerce_results_in_top_10,
    disallowed_page_types_in_top_3
) VALUES (?, 40, 15, 5, 5, 5, 5, 5, 20, 5, 100, 80, 'login,free,cheap', 'navigational', 800, 3, 2, 'E-commerce,Forum')
"""

FAIL_STALE_JOBS = """
UPDATE jobs
SET status = 'failed', error = ?, finished_at = ?
WHERE status = 'running';
"""