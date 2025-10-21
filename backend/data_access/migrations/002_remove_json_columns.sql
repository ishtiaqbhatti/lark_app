-- data_access/migrations/002_remove_json_columns.sql

-- This migration is intentionally left blank.
-- SQLite does not support dropping columns.
-- The data from the JSON columns will be migrated to the new tables in the application logic.
-- The old columns will be ignored by the application.
