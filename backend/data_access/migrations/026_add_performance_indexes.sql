-- Add performance indexes for discovery queries

-- Index on search_history for client queries
CREATE INDEX IF NOT EXISTS idx_search_history_client_created ON search_history (client_id, created_at);

-- Index on keyword_results for search_id lookups
CREATE INDEX IF NOT EXISTS idx_keyword_results_search_id ON keyword_results (search_id);

-- Index on keyword_results for keyword lookups (deduplication)
CREATE INDEX IF NOT EXISTS idx_keyword_results_keyword_lower ON keyword_results (LOWER(keyword));

-- Composite index for status filtering
CREATE INDEX IF NOT EXISTS idx_keyword_results_search_status ON keyword_results (search_id, blog_qualification_status);

-- Index for opportunity score sorting
CREATE INDEX IF NOT EXISTS idx_keyword_results_opp_score ON keyword_results (opportunity_score);
