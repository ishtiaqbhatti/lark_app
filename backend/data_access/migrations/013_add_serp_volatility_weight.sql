-- data_access/migrations/013_add_serp_volatility_weight.sql

ALTER TABLE qualification_settings ADD COLUMN serp_volatility_weight REAL;
