ALTER TABLE opportunities ADD COLUMN run_id INTEGER;
CREATE INDEX IF NOT EXISTS idx_opportunities_run_id ON opportunities (run_id);
