-- data_access/migrations/010_add_history_columns.sql

ALTER TABLE opportunities ADD COLUMN last_seen_at TEXT;
ALTER TABLE opportunities ADD COLUMN metrics_history TEXT;
