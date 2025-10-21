-- data_access/migrations/016_add_review_threshold.sql

ALTER TABLE qualification_settings ADD COLUMN review_threshold REAL;
