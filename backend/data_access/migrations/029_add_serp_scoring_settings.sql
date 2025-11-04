ALTER TABLE client_settings ADD COLUMN serp_freshness_weight INTEGER DEFAULT 5;
ALTER TABLE client_settings ADD COLUMN serp_volatility_weight INTEGER DEFAULT 5;
ALTER TABLE client_settings ADD COLUMN serp_freshness_old_threshold_days INTEGER DEFAULT 180;
ALTER TABLE client_settings ADD COLUMN serp_volatility_stable_threshold_days INTEGER DEFAULT 90;
