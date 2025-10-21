-- data_access/migrations/014_add_disqualification_rules.sql

ALTER TABLE qualification_settings ADD COLUMN disqualification_rules TEXT;
