-- Add a column to store the total API cost for a discovery run
ALTER TABLE discovery_runs ADD COLUMN total_api_cost REAL DEFAULT 0.0;
