-- data_access/migrations/019_add_core_keyword_and_competitor_metrics_to_opportunities.sql

-- Add new columns for direct access to frequently used keyword metrics
ALTER TABLE opportunities ADD COLUMN cpc REAL DEFAULT 0.0;
ALTER TABLE opportunities ADD COLUMN competition REAL DEFAULT 0.0;
ALTER TABLE opportunities ADD COLUMN main_intent TEXT DEFAULT 'informational';
ALTER TABLE opportunities ADD COLUMN search_volume_trend_json TEXT;

-- Add new columns for storing aggregated competitor data for easier access
ALTER TABLE opportunities ADD COLUMN competitor_social_media_tags_json TEXT;
ALTER TABLE opportunities ADD COLUMN competitor_page_timing_json TEXT;

-- Create indexes on these new columns for improved query performance
CREATE INDEX idx_opportunities_cpc ON opportunities (cpc);
CREATE INDEX idx_opportunities_competition ON opportunities (competition);
CREATE INDEX idx_opportunities_main_intent ON opportunities (main_intent);
