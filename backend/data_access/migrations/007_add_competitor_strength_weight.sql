-- data_access/migrations/007_add_competitor_strength_weight.sql

ALTER TABLE qualification_settings ADD COLUMN competitor_strength_weight REAL;
