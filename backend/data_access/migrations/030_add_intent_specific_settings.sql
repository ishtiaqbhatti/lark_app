ALTER TABLE qualification_settings ADD COLUMN informational_max_high_top_of_page_bid REAL DEFAULT 5.0;
ALTER TABLE qualification_settings ADD COLUMN commercial_max_high_top_of_page_bid REAL DEFAULT 20.0;
ALTER TABLE qualification_settings ADD COLUMN transactional_max_high_top_of_page_bid REAL DEFAULT 30.0;
ALTER TABLE qualification_settings ADD COLUMN informational_max_kd_hard_limit INTEGER DEFAULT 60;
ALTER TABLE qualification_settings ADD COLUMN commercial_max_kd_hard_limit INTEGER DEFAULT 80;
ALTER TABLE qualification_settings ADD COLUMN transactional_max_kd_hard_limit INTEGER DEFAULT 90;
