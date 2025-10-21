-- data_access/migrations/006_add_intent_weights.sql

ALTER TABLE qualification_settings ADD COLUMN informational_intent_weight REAL;
ALTER TABLE qualification_settings ADD COLUMN navigational_intent_weight REAL;
ALTER TABLE qualification_settings ADD COLUMN commercial_intent_weight REAL;
ALTER TABLE qualification_settings ADD COLUMN transactional_intent_weight REAL;
