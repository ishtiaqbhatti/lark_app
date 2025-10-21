-- data_access/migrations/011_add_keywords_table.sql

CREATE TABLE keywords (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    keyword TEXT NOT NULL UNIQUE,
    search_volume INTEGER,
    keyword_difficulty INTEGER,
    cpc REAL,
    competition REAL,
    search_volume_trend TEXT,
    main_intent TEXT,
    core_keyword TEXT
);

ALTER TABLE opportunities ADD COLUMN keyword_id INTEGER REFERENCES keywords(id);
CREATE INDEX IF NOT EXISTS idx_opportunities_keyword_id ON opportunities (keyword_id);
