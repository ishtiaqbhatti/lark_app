-- data_access/migrations/026_add_composite_indexes.sql

-- Composite index for common filtering query (client + status + score)
CREATE INDEX IF NOT EXISTS idx_opportunities_client_status_score 
ON opportunities (client_id, status, strategic_score DESC);

-- Composite index for qualified opportunities
CREATE INDEX IF NOT EXISTS idx_opportunities_qualified 
ON opportunities (client_id, blog_qualification_status, strategic_score DESC)
WHERE status NOT IN ('rejected', 'failed');

-- Composite index for date-based queries
CREATE INDEX IF NOT EXISTS idx_opportunities_client_date 
ON opportunities (client_id, date_added DESC);

-- Composite index for search functionality
CREATE INDEX IF NOT EXISTS idx_opportunities_keyword_search 
ON opportunities (client_id, keyword);

-- Index for job status queries
CREATE INDEX IF NOT EXISTS idx_jobs_status_started 
ON jobs (status, started_at DESC);

-- Index for discovery run queries
CREATE INDEX IF NOT EXISTS idx_discovery_runs_client_status 
ON discovery_runs (client_id, status, start_time DESC);

-- Index for content feedback queries
CREATE INDEX IF NOT EXISTS idx_content_feedback_opportunity 
ON content_feedback (opportunity_id, rating DESC);

-- Index for content history queries  
CREATE INDEX IF NOT EXISTS idx_content_history_opportunity_timestamp 
ON content_history (opportunity_id, timestamp DESC);
