-- data_access/migrations/009_add_trend_weight.sql

ALTER TABLE qualification_settings ADD COLUMN trend_weight REAL;
