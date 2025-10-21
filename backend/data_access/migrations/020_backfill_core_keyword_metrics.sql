-- data_access/migrations/020_backfill_core_keyword_metrics.sql

-- Backfill cpc, competition, main_intent, and search_volume_trend_json from existing keyword_info and search_intent_info JSON blobs
UPDATE opportunities
SET
    cpc = CAST(JSON_EXTRACT(keyword_info, '$.cpc') AS REAL),
    competition = CAST(JSON_EXTRACT(keyword_info, '$.competition') AS REAL),
    main_intent = JSON_EXTRACT(search_intent_info, '$.main_intent'),
    search_volume_trend_json = JSON_EXTRACT(keyword_info, '$.search_volume_trend')
WHERE
    keyword_info IS NOT NULL AND search_intent_info IS NOT NULL;

-- Backfill aggregated competitor social media tags and page timing from blueprint_data
-- This requires iterating through the competitor_analysis array within blueprint_data
-- Note: SQLite's JSON functions can be limited for complex array aggregation directly in SQL.
-- This might require application-level backfill for more complex aggregations if `blueprint_data` is large.
-- For a simple direct copy of the *first* competitor's data (as an example), or an empty JSON if none:
UPDATE opportunities
SET
    competitor_social_media_tags_json = (
        SELECT CASE
            WHEN JSON_EXTRACT(blueprint_data, '$.competitor_analysis[0].social_media_tags') IS NOT NULL
            THEN JSON_EXTRACT(blueprint_data, '$.competitor_analysis[0].social_media_tags')
            ELSE '{}'
        END
    ),
    competitor_page_timing_json = (
        SELECT CASE
            WHEN JSON_EXTRACT(blueprint_data, '$.competitor_analysis[0].page_timing') IS NOT NULL
            THEN JSON_EXTRACT(blueprint_data, '$.competitor_analysis[0].page_timing')
            ELSE '{}'
        END
    )
WHERE
    blueprint_data IS NOT NULL;
