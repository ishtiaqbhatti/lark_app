-- NEW COLUMNS FOR CLIENT_SETTINGS
ALTER TABLE client_settings ADD COLUMN discovery_max_pages INTEGER DEFAULT 100;
ALTER TABLE client_settings ADD COLUMN discovery_related_depth INTEGER DEFAULT 1;
ALTER TABLE client_settings ADD COLUMN discovery_exact_match BOOLEAN DEFAULT FALSE;

-- COLUMNS FOR AI TOPIC CLUSTERS (from Task 3)
ALTER TABLE opportunities ADD COLUMN ai_topic_clusters TEXT;
ALTER TABLE opportunities ADD COLUMN is_question BOOLEAN DEFAULT FALSE;
