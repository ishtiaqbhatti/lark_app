-- data_access/migrations/012_add_seasonality_weight.sql

ALTER TABLE qualification_settings ADD COLUMN seasonality_weight REAL;
