-- data_access/migrations/008_add_serp_features_weight.sql

ALTER TABLE qualification_settings ADD COLUMN serp_features_weight REAL;
