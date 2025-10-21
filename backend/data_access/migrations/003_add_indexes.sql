-- data_access/migrations/003_add_indexes.sql

CREATE INDEX idx_opportunities_status ON opportunities (status);
CREATE INDEX idx_opportunities_client_id ON opportunities (client_id);
CREATE INDEX idx_opportunities_strategic_score ON opportunities (strategic_score);
CREATE INDEX idx_opportunities_run_id ON opportunities (run_id);
CREATE INDEX idx_opportunities_keyword_id ON opportunities (keyword_id);
CREATE INDEX idx_opportunities_slug ON opportunities (slug);
