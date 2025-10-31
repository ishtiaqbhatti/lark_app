-- Add top-level columns to the opportunities table for frequently accessed data
ALTER TABLE opportunities ADD COLUMN search_volume INTEGER;
ALTER TABLE opportunities ADD COLUMN keyword_difficulty INTEGER;

-- Backfill the new columns with data from the existing JSON blobs
UPDATE opportunities
SET
    search_volume = CAST(JSON_EXTRACT(full_data, '$.keyword_info.search_volume') AS INTEGER),
    keyword_difficulty = CAST(JSON_EXTRACT(full_data, '$.keyword_properties.keyword_difficulty') AS INTEGER)
WHERE full_data IS NOT NULL AND (search_volume IS NULL OR keyword_difficulty IS NULL);
