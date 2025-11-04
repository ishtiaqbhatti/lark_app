# Keyword Discovery Configuration Guide

## Overview

This guide explains all configuration options available for the keyword discovery pipeline. Each setting controls how keywords are discovered, evaluated, and prioritized.

## Quick Start

1. Copy `config/example_client_config.json` to `config/client_<your_client_id>.json`
2. Update `client_id`, `target_domain`, and business context fields
3. Adjust thresholds based on your client's domain authority and goals
4. Test with a small seed keyword list before full deployment

## Configuration Sections

### 1. API & Data Source Settings

```json
{
  "location_code": 2840,
  "language_code": "en",
  "include_clickstream_data": true
}
```

**`location_code`** (integer, required)
- Geographic location for search data
- Use `2840` for United States
- Get full list from: `https://api.dataforseo.com/v3/dataforseo_labs/locations_and_languages`

**`language_code`** (string, required)
- Language for keywords
- Use `"en"` for English
- Must match available languages for the location

**`include_clickstream_data`** (boolean, default: `false`)
- When `true`: Returns real user behavior data (more accurate, 2x cost)
- When `false`: Returns Google Ads estimates only
- **Recommendation:** Set to `true` for accurate volume data

---

### 2. Keyword Discovery Behavior

```json
{
  "closely_variants": true,
  "discovery_ignore_synonyms": false,
  "discovery_exact_match": false
}
```

**`closely_variants`** (boolean, default: `true`) ⭐ CRITICAL SETTING
- When `true`: Includes plurals, synonyms, reordered phrases
  - Example: "running shoes" → "runners shoes", "shoes for running"
- When `false`: ONLY exact matches
- **Impact:** Setting to `false` reduces results by 60-70%
- **Recommendation:** Keep `true` unless doing branded research

**`discovery_ignore_synonyms`** (boolean, default: `false`)
- When `true`: Excludes highly similar keywords, returns only core terms
- When `false`: Returns all variations
- **Use Case:** Set to `true` to reduce data volume for clustering

**`discovery_exact_match`** (boolean, default: `false`)
- When `true`: Returns only keywords containing exact seed phrase
- When `false`: Returns related concepts and variations
- **Use Case:** Set to `true` for narrow, specific research

---

### 3. Search Volume Thresholds

```json
{
  "min_search_volume": 100,
  "high_value_sv_override_threshold": 10000
}
```

**`min_search_volume`** (integer, default: `100`)
- Minimum monthly searches required
- **Recommendations by site type:**
  - New site (DA < 20): `20-50`
  - Growing site (DA 20-40): `50-100`
  - Established site (DA 40-60): `100-500`
  - Authority site (DA 60+): `500+`

**`high_value_sv_override_threshold`** (integer, default: `10000`)
- Keywords above this bypass some restrictions
- **Rationale:** High-volume keywords are worth pursuing even if competitive

---

### 4. Keyword Difficulty Limits

```json
{
  "max_kd_hard_limit": 70,
  "long_tail_kd_threshold": 30,
  "long_tail_min_search_volume": 20
}
```

**`max_kd_hard_limit`** (integer, default: `70`)
- Maximum keyword difficulty (0-100 scale)
- **Recommendations by Domain Authority:**
  - DA < 20: `max_kd = 25`
  - DA 20-40: `max_kd = 40`
  - DA 40-60: `max_kd = 60`
  - DA 60-80: `max_kd = 75`
  - DA 80+: `max_kd = 90`

**`long_tail_kd_threshold`** (integer, default: `30`)
- KD limit for long-tail keywords (5+ words)
- These get special treatment due to specificity

**`long_tail_min_search_volume`** (integer, default: `20`)
- Lower SV threshold for long-tail opportunities
- **Rationale:** "How to set up email marketing for small law firms" might only get 20 searches/month but has high intent

---

### 5. Trend Analysis

```json
{
  "yearly_trend_decline_threshold": -25,
  "quarterly_trend_decline_threshold": 0,
  "search_volume_volatility_threshold": 1.5
}
```

**`yearly_trend_decline_threshold`** (integer, default: `-25`)
- Reject if year-over-year decline exceeds this percentage
- **Example:** `-25` means reject if volume dropped more than 25% vs last year
- **Caution:** Don't set too strict or you'll miss seasonal keywords

**`quarterly_trend_decline_threshold`** (integer, default: `0`)
- Reject if last quarter declined vs previous quarter
- **Note:** System now detects seasonality and exempts seasonal keywords

**`search_volume_volatility_threshold`** (float, default: `1.5`)
- Ratio of standard deviation to mean
- Higher values indicate unstable search patterns
- **Recommendation:** Increase to `2.0+` to allow seasonal keywords

---

### 6. Competition Metrics

```json
{
  "max_paid_competition_score": 0.8,
  "max_high_top_of_page_bid": 15.0,
  "high_value_cpc_override_threshold": 5.0
}
```

**`max_paid_competition_score`** (float 0-1, default: `0.8`)
- Google Ads competition level
- **Note:** High paid competition ≠ high organic competition
- **Recommendation:** Set to `0.9` for B2B/SaaS (high CPC indicates value)

**`max_high_top_of_page_bid`** (float USD, default: `15.0`)
- Maximum CPC bid to allow
- **Use Case:** Prevents targeting ultra-expensive keywords
- **B2B Exception:** Increase to `50.0+` for enterprise SaaS

**`high_value_cpc_override_threshold`** (float USD, default: `5.0`)
- CPC above this bypasses some restrictions
- **Rationale:** High CPC = proven commercial value

---

### 7. SERP Environment

```json
{
  "crowded_serp_features_threshold": 4,
  "hostile_serp_feature_count_threshold": 3,
  "min_serp_stability_days": 14
}
```

**`crowded_serp_features_threshold`** (integer, default: `4`)
- Number of SERP features (PAA, videos, images) before rejecting
- **Impact:** Stricter settings eliminate many viable keywords
- **Recommendation:** Set to `5-6` (blogs can compete alongside features)

**`hostile_serp_feature_count_threshold`** (integer, default: `3`)
- Triggers rejection when hostile features (shopping, local, tools) exceed this AND no organic results present
- **Examples of hostile:** Shopping results, flight search, currency calculator
- **Recommendation:** Keep at `3` (default is well-calibrated)

**`min_serp_stability_days`** (integer, default: `14`)
- Minimum days between SERP updates
- If SERPs change faster, keyword is too volatile
- **Recommendation:** `14-21` days for most industries

---

### 8. Search Intent Filtering

```json
{
  "allowed_intents": ["informational"],
  "prohibited_intents": ["navigational"]
}
```

**`allowed_intents`** (array of strings)
- Primary intent keyword must have
- **Options:** `"informational"`, `"commercial"`, `"transactional"`, `"navigational"`
- **Recommendations by content strategy:**
  - **Pure blog:** `["informational"]`
  - **Review/comparison site:** `["informational", "commercial"]`
  - **E-commerce content:** `["informational", "commercial", "transactional"]`

**`prohibited_intents`** (array of strings)
- Secondary intents that trigger rejection
- **Default:** `["navigational"]` (brand searches like "facebook login")
- **Caution:** Don't prohibit `"commercial"` unless purely educational site

---

### 9. Scoring Thresholds

```json
{
  "qualified_threshold": 70,
  "review_threshold": 50
}
```

**`qualified_threshold`** (integer 0-100, default: `70`)
- Auto-approve keywords scoring above this
- **Recommendations:**
  - Aggressive strategy: `60-65`
  - Balanced strategy: `70`
  - Conservative strategy: `75-80`

**`review_threshold`** (integer 0-100, default: `50`)
- Keywords between review and qualified need manual review
- Below this score = auto-reject
- **Tip:** Lower to `40-45` to capture more marginal opportunities

---

### 10. Negative Keywords

```json
{
  "negative_keywords": ["porn", "crack", "cheap", "near me"]
}
```

**Purpose:** Hard-block specific terms regardless of other metrics

**Common categories to exclude:**
- Adult content: `"porn"`, `"xxx"`, `"sex"`
- Piracy: `"torrent"`, `"crack"`, `"free download"`
- Low-intent: `"cheap"`, `"free"`, `"coupon"`
- Local (if not local business): `"near me"`, `"in [city]"`
- Competitors: Brand names you don't want to target
