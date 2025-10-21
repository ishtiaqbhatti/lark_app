-- data_access/migrations/005_add_qualification_columns.sql

ALTER TABLE opportunities ADD COLUMN strategic_score REAL;
ALTER TABLE opportunities ADD COLUMN score_breakdown TEXT;
ALTER TABLE opportunities ADD COLUMN qualification_status TEXT;
ALTER TABLE opportunities ADD COLUMN qualification_reason TEXT;
