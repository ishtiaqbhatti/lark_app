-- data_access/migrations/015_add_brand_keywords.sql

ALTER TABLE qualification_settings ADD COLUMN brand_keywords TEXT;
ALTER TABLE qualification_settings ADD COLUMN competitor_brand_keywords TEXT;
