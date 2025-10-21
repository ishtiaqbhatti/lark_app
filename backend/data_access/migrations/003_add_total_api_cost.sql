-- Add a column to store the total API cost for the entire workflow
ALTER TABLE opportunities ADD COLUMN total_api_cost REAL DEFAULT 0.0;
