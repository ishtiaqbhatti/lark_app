-- data_access/migrations/018_add_job_id_and_cluster_name.sql

ALTER TABLE opportunities ADD COLUMN latest_job_id TEXT;
ALTER TABLE opportunities ADD COLUMN cluster_name TEXT;