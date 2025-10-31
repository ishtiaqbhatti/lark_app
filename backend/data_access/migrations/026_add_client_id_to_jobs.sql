-- Add client_id to the jobs table to associate jobs with clients
ALTER TABLE jobs ADD COLUMN client_id TEXT;

-- Add function_name to the jobs table for better UI descriptions
ALTER TABLE jobs ADD COLUMN function_name TEXT;

-- Create an index for efficient querying of active jobs by client
CREATE INDEX IF NOT EXISTS idx_jobs_client_id_status ON jobs (client_id, status);
