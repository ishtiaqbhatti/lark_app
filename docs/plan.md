# AI CODING AGENT IMPLEMENTATION PLAN
## Complete Step-by-Step Instructions with Exact Code Changes

---

## 📋 OVERVIEW
- **Total Tasks:** 15 priority fixes
- **Estimated Total Time:** 8-12 hours
- **Order:** Must be executed sequentially (dependencies managed)

---

## TASK 1: Fix `closely_variants` Parameter Default to Enable Keyword Variations

### File: `keyword_discovery/expander.py`
### Lines to Modify: 73-75

**CURRENT CODE:**
```python
        final_ignore_synonyms = ignore_synonyms if ignore_synonyms is not None else self.config.get("discovery_ignore_synonyms", False)
        final_include_clickstream_data = include_clickstream_data_override if include_clickstream_data_override is not None else self.config.get("include_clickstream_data", False)
        final_closely_variants = closely_variants_override if closely_variants_override is not None else self.config.get("closely_variants", False)
```

**REPLACE WITH:**
```python
        final_ignore_synonyms = ignore_synonyms if ignore_synonyms is not None else self.config.get("discovery_ignore_synonyms", False)
        final_include_clickstream_data = include_clickstream_data_override if include_clickstream_data_override is not None else self.config.get("include_clickstream_data", False)
        final_closely_variants = closely_variants_override if closely_variants_override is not None else self.config.get("closely_variants", True)
```

**CHANGE SUMMARY:** Changed default from `False` to `True` on line 75

---

## TASK 2: Add Helper Function for Reliable Search Volume Using Clickstream Data

### File: `core/utils.py`
### Action: ADD NEW FUNCTION at the end of the file

**ADD THIS COMPLETE FUNCTION:**
```python


def get_reliable_search_volume(keyword_data: Dict[str, Any]) -> int:
    """
    Returns the most reliable search volume metric by prioritizing clickstream data
    over Google Ads data. Clickstream data reflects actual user behavior and is
    typically 15-30% more accurate for low-to-medium volume keywords.
    
    Priority order:
    1. Clickstream-normalized data (real user behavior)
    2. Bing-normalized data (cross-platform validation)
    3. Standard keyword_info data (Google Ads estimates)
    
    Args:
        keyword_data: Dictionary containing keyword metrics from DataForSEO
        
    Returns:
        Integer search volume, or 0 if no data available
    """
    # First priority: Clickstream data
    clickstream_data = keyword_data.get("keyword_info_normalized_with_clickstream")
    if clickstream_data and clickstream_data.get("search_volume") is not None:
        return clickstream_data.get("search_volume", 0)
    
    # Second priority: Bing-normalized data
    bing_data = keyword_data.get("keyword_info_normalized_with_bing")
    if bing_data and bing_data.get("search_volume") is not None:
        return bing_data.get("search_volume", 0)
    
    # Fallback: Standard Google data
    keyword_info = keyword_data.get("keyword_info", {})
    return keyword_info.get("search_volume", 0)
```

---

## TASK 3: Add Seasonal Pattern Detection Function

### File: `core/utils.py`
### Action: ADD NEW FUNCTION after the function added in Task 2

**ADD THIS COMPLETE FUNCTION:**
```python


def detect_seasonal_pattern(monthly_searches: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Detects if a keyword has a seasonal search pattern by analyzing year-over-year
    consistency and peak-to-average ratios.
    
    A keyword is considered seasonal if:
    - Peak month volume is 3x+ the average
    - Pattern repeats across multiple years (if data available)
    
    Args:
        monthly_searches: List of dicts with 'year', 'month', 'search_volume' keys
        
    Returns:
        Dict with keys:
        - is_seasonal (bool)
        - peak_month (int): Month number (1-12) of typical peak, or None
        - seasonality_factor (float): Peak volume / average volume ratio
        - pattern_type (str): "strong_seasonal", "moderate_seasonal", or "evergreen"
    """
    if not monthly_searches or len(monthly_searches) < 6:
        return {
            "is_seasonal": False,
            "peak_month": None,
            "seasonality_factor": 1.0,
            "pattern_type": "insufficient_data"
        }
    
    # Extract volumes and calculate basic stats
    volumes = [m.get("search_volume", 0) for m in monthly_searches if m.get("search_volume") is not None]
    
    if not volumes or sum(volumes) == 0:
        return {
            "is_seasonal": False,
            "peak_month": None,
            "seasonality_factor": 1.0,
            "pattern_type": "no_data"
        }
    
    avg_volume = sum(volumes) / len(volumes)
    max_volume = max(volumes)
    seasonality_factor = max_volume / avg_volume if avg_volume > 0 else 1.0
    
    # Find peak month (most recent occurrence)
    peak_month = None
    for search in monthly_searches:
        if search.get("search_volume") == max_volume:
            peak_month = search.get("month")
            break
    
    # Determine seasonality classification
    if seasonality_factor >= 5.0:
        pattern_type = "strong_seasonal"
        is_seasonal = True
    elif seasonality_factor >= 3.0:
        pattern_type = "moderate_seasonal"
        is_seasonal = True
    elif seasonality_factor >= 2.0:
        pattern_type = "mild_seasonal"
        is_seasonal = True
    else:
        pattern_type = "evergreen"
        is_seasonal = False
    
    return {
        "is_seasonal": is_seasonal,
        "peak_month": peak_month,
        "seasonality_factor": round(seasonality_factor, 2),
        "pattern_type": pattern_type
    }
```

---

## TASK 4: Add Content Difficulty Estimation Function

### File: `core/utils.py`
### Action: ADD NEW FUNCTION after the function added in Task 3

**ADD THIS COMPLETE FUNCTION:**
```python


def estimate_content_difficulty(opportunity: Dict[str, Any]) -> Dict[str, Any]:
    """
    Estimates the difficulty of creating content for a given keyword opportunity
    based on SERP analysis, competitor content requirements, and topic complexity.
    
    Factors considered:
    - Average content length of top-ranking pages
    - Presence of rich media requirements (video, images)
    - Technical topic indicators
    - Number of SERP features competing for attention
    
    Args:
        opportunity: Dictionary containing keyword data and SERP info
        
    Returns:
        Dict with keys:
        - difficulty_level (str): "easy", "medium", "hard", or "expert"
        - estimated_word_count (int): Recommended content length
        - requires_video (bool): Whether video content is likely needed
        - requires_expert (bool): Whether subject matter expert is needed
        - production_time_hours (int): Estimated hours to produce
    """
    serp_info = opportunity.get("serp_info", {})
    keyword_props = opportunity.get("keyword_properties", {})
    avg_backlinks = opportunity.get("avg_backlinks_info", {})
    keyword = opportunity.get("keyword", "")
    
    difficulty_level = "easy"
    estimated_word_count = 1000
    requires_video = False
    requires_expert = False
    production_time_hours = 2
    
    # Check SERP features
    serp_types = set(serp_info.get("serp_item_types", []))
    
    # Video requirement detection
    if "video" in serp_types or "short_videos" in serp_types:
        requires_video = True
        difficulty_level = "hard"
        production_time_hours += 8
    
    # Competitor authority check
    referring_domains = avg_backlinks.get("referring_main_domains", 0)
    if referring_domains > 50:
        estimated_word_count = 2000
        difficulty_level = "medium"
        production_time_hours = 6
    
    if referring_domains > 100:
        estimated_word_count = 3000
        difficulty_level = "hard"
        production_time_hours = 12
        requires_expert = True
    
    # Technical topic detection (based on keyword patterns)
    technical_indicators = [
        "api", "algorithm", "architecture", "protocol", "encryption",
        "optimization", "configuration", "implementation", "integration",
        "debugging", "framework", "library", "sdk", "cli"
    ]
    
    keyword_lower = keyword.lower()
    if any(indicator in keyword_lower for indicator in technical_indicators):
        requires_expert = True
        if difficulty_level == "easy":
            difficulty_level = "medium"
        estimated_word_count = max(estimated_word_count, 2000)
        production_time_hours = max(production_time_hours, 8)
    
    # Adjust for keyword difficulty
    kd = keyword_props.get("keyword_difficulty", 0)
    if kd > 60 and difficulty_level != "expert":
        difficulty_level = "hard"
        production_time_hours = max(production_time_hours, 10)
    
    # SERP feature crowding adjustment
    attention_features = {"carousel", "featured_snippet", "people_also_ask", "images", "shopping"}
    crowding_count = len(serp_types.intersection(attention_features))
    if crowding_count >= 3:
        estimated_word_count += 500
        production_time_hours += 2
    
    return {
        "difficulty_level": difficulty_level,
        "estimated_word_count": estimated_word_count,
        "requires_video": requires_video,
        "requires_expert": requires_expert,
        "production_time_hours": production_time_hours
    }
```

---

## TASK 5: Update Disqualification Rules to Use Reliable Search Volume

### File: `disqualification_rules.py`
### Lines to Modify: 1-6 (imports section)

**CURRENT CODE:**
```python
# pipeline/step_01_discovery/disqualification_rules.py
import logging
import re
from typing import Dict, Any, Tuple, Optional
from datetime import datetime
import numpy as np
from core import utils
```

**REPLACE WITH:**
```python
# pipeline/step_01_discovery/disqualification_rules.py
import logging
import re
from typing import Dict, Any, Tuple, Optional
from datetime import datetime
import numpy as np
from core import utils
from core.utils import get_reliable_search_volume, detect_seasonal_pattern
```

### Lines to Modify: 60-68

**CURRENT CODE:**
```python
    # New Rule: Reject if SV or KD data is missing (null)
    search_volume = keyword_info.get("search_volume")
    keyword_difficulty = keyword_props.get("keyword_difficulty")

    # A search volume of 0 is a valid reason to disqualify based on client strategy.
    if search_volume is None or search_volume == 0:
        return True, "Rule 0: Rejected due to zero or null Search Volume.", True
    
    # A keyword difficulty of 0 is a valid, desirable metric. Only reject if data is missing.
    if keyword_difficulty is None:
        return True, "Rule 0: Rejected due to null Keyword Difficulty.", True
```

**REPLACE WITH:**
```python
    # New Rule: Reject if SV or KD data is missing (null)
    # Use reliable search volume from clickstream data when available
    search_volume = get_reliable_search_volume(opportunity)
    keyword_difficulty = keyword_props.get("keyword_difficulty")

    # A search volume of 0 is a valid reason to disqualify based on client strategy.
    if search_volume is None or search_volume == 0:
        return True, "Rule 0: Rejected due to zero or null Search Volume.", True
    
    # A keyword difficulty of 0 is a valid, desirable metric. Only reject if data is missing.
    if keyword_difficulty is None:
        return True, "Rule 0: Rejected due to null Keyword Difficulty.", True
```

### Lines to Modify: 99-102

**CURRENT CODE:**
```python
    # Tier 2: Volume & Trend Analysis
    if utils.safe_compare(
        keyword_info.get("search_volume"), client_cfg.get("min_search_volume"), "lt"
    ):
```

**REPLACE WITH:**
```python
    # Tier 2: Volume & Trend Analysis
    if utils.safe_compare(
        search_volume, client_cfg.get("min_search_volume"), "lt"
    ):
```

### Lines to Modify: 104-107

**CURRENT CODE:**
```python
        return (
            True,
            f"Rule 5: Below search volume floor (minimum: {client_cfg.get('min_search_volume', 100)} SV). Current: {keyword_info.get('search_volume', 0)} SV.",
            False,
        )
```

**REPLACE WITH:**
```python
        return (
            True,
            f"Rule 5: Below search volume floor (minimum: {client_cfg.get('min_search_volume', 100)} SV). Current: {search_volume} SV.",
            False,
        )
```

---

## TASK 6: Add Seasonal Pattern Exception to Trend Decline Rule

### File: `disqualification_rules.py`
### Lines to Modify: 141-174

**CURRENT CODE:**
```python
    # Rule 7b: Check for recent sharp decline using raw monthly searches
    monthly_searches = opportunity.get(
        "monthly_searches", []
    )  # Get from opportunity object, which is deserialized
    if monthly_searches and len(monthly_searches) >= 4:
        # Sort by year and month to ensure correctness (most recent first for trend)
        try:
            sorted_searches = sorted(
                monthly_searches, key=lambda x: (x["year"], x["month"]), reverse=True
            )
            if len(sorted_searches) >= 4:
                # Compare latest month with 3 months prior (index 0 vs index 3)
                latest_vol = sorted_searches[0].get("search_volume")
                past_vol = sorted_searches[3].get("search_volume")

                if latest_vol is not None and past_vol is not None and past_vol > 0:
                    if (
                        latest_vol / past_vol
                    ) < 0.5:  # If volume has dropped by more than 50% in 3 months
                        return (
                            True,
                            "Rule 7b: Recent sharp decline in search volume (>50% drop in last 3 months).",
                            False,
                        )
        except (TypeError, KeyError):
            logging.getLogger(__name__).warning(
                f"Could not parse monthly_searches for recent trend analysis on keyword '{keyword}'."
            )
```

**REPLACE WITH:**
```python
    # Rule 7b: Check for recent sharp decline using raw monthly searches
    # BUT: Skip this check if keyword shows seasonal pattern
    monthly_searches_from_keyword_info = keyword_info.get("monthly_searches", [])
    seasonality_data = detect_seasonal_pattern(monthly_searches_from_keyword_info)
    
    # Store seasonality data for later use in scoring
    opportunity["seasonality_analysis"] = seasonality_data
    
    if not seasonality_data.get("is_seasonal", False):
        # Only check for decline if NOT seasonal
        if monthly_searches_from_keyword_info and len(monthly_searches_from_keyword_info) >= 4:
            try:
                sorted_searches = sorted(
                    monthly_searches_from_keyword_info, 
                    key=lambda x: (x["year"], x["month"]), 
                    reverse=True
                )
                if len(sorted_searches) >= 4:
                    latest_vol = sorted_searches[0].get("search_volume")
                    past_vol = sorted_searches[3].get("search_volume")

                    if latest_vol is not None and past_vol is not None and past_vol > 0:
                        if (latest_vol / past_vol) < 0.5:
                            return (
                                True,
                                "Rule 7b: Recent sharp decline in search volume (>50% drop in last 3 months). Not seasonal pattern.",
                                False,
                            )
            except (TypeError, KeyError):
                logging.getLogger(__name__).warning(
                    f"Could not parse monthly_searches for recent trend analysis on keyword '{keyword}'."
                )
    else:
        logging.getLogger(__name__).info(
            f"Skipping decline check for '{keyword}' - detected {seasonality_data.get('pattern_type')} pattern "
            f"(peak in month {seasonality_data.get('peak_month')}, factor: {seasonality_data.get('seasonality_factor')})"
        )
```

---

## TASK 7: Relax Hostile SERP Rule to Check for Organic Presence

### File: `disqualification_rules.py`
### Lines to Modify: 297-334 (the entire _check_hostile_serp_environment function)

**CURRENT CODE:**
```python
def _check_hostile_serp_environment(
    opportunity: Dict[str, Any],
) -> Tuple[bool, Optional[str]]:
    """
    Rule 16: Disqualifies keywords where the SERP is dominated by features hostile to blog content.
    """
    serp_info = opportunity.get("serp_info", {})
    if not serp_info:
        return False, None  # Cannot analyze if SERP info is missing

    serp_types = set(serp_info.get("serp_item_types", []))

    # Define hostile features based on detailed SERP analysis
    HOSTILE_FEATURES = {
        # Strong transactional/e-commerce intent
        "shopping",
        "popular_products",
        "refine_products",
        "explore_brands",
        # Strong local intent
        "local_pack",
        "map",
        "local_services",
        # Purely transactional/utility intent (Google-owned tools)
        "google_flights",
        "google_hotels",
        "hotels_pack",
        # App-related intent
        "app",
        # Job-seeking intent
        "jobs",
        # Direct utility/tool intent
        "math_solver",
        "currency_box",
        "stocks_box",
    }

    found_hostile_features = serp_types.intersection(HOSTILE_FEATURES)

    if found_hostile_features:
        return (
            True,
            f"Rule 16: SERP is hostile to blog content. Contains dominant non-article features: {', '.join(found_hostile_features)}.",
        )

    return False, None
```

**REPLACE WITH:**
```python
def _check_hostile_serp_environment(
    opportunity: Dict[str, Any],
) -> Tuple[bool, Optional[str]]:
    """
    Rule 16: Disqualifies keywords where the SERP is COMPLETELY dominated by features 
    hostile to blog content, with NO organic results present.
    
    Updated logic: Only reject if hostile features exist AND there are few/no organic results.
    This prevents false rejections of keywords where blogs can still rank alongside features.
    """
    serp_info = opportunity.get("serp_info", {})
    if not serp_info:
        return False, None  # Cannot analyze if SERP info is missing

    serp_types = set(serp_info.get("serp_item_types", []))

    # Define hostile features based on detailed SERP analysis
    HOSTILE_FEATURES = {
        # Strong transactional/e-commerce intent
        "shopping",
        "popular_products",
        "refine_products",
        "explore_brands",
        # Strong local intent
        "local_pack",
        "map",
        "local_services",
        # Purely transactional/utility intent (Google-owned tools)
        "google_flights",
        "google_hotels",
        "hotels_pack",
        # App-related intent
        "app",
        # Job-seeking intent
        "jobs",
        # Direct utility/tool intent
        "math_solver",
        "currency_box",
        "stocks_box",
    }

    found_hostile_features = serp_types.intersection(HOSTILE_FEATURES)

    # NEW LOGIC: Check if organic results are present
    has_organic = "organic" in serp_types
    hostile_count = len(found_hostile_features)
    
    # Only reject if BOTH conditions are true:
    # 1. Multiple hostile features present (3+)
    # 2. No organic results OR very few organic signals
    if hostile_count >= 3 and not has_organic:
        return (
            True,
            f"Rule 16: SERP is completely hostile to blog content. Contains {hostile_count} dominant non-article features ({', '.join(found_hostile_features)}) with NO organic results.",
        )
    
    # If hostile features exist but organic results also present, issue warning but don't reject
    if hostile_count >= 2 and has_organic:
        logging.getLogger(__name__).info(
            f"SERP has {hostile_count} competing features but organic results present: {', '.join(found_hostile_features)}"
        )
    
    return False, None
```

---

## TASK 8: Add Long-Tail Keyword Handling to Word Count Rule

### File: `disqualification_rules.py`
### Lines to Modify: 218-243

**CURRENT CODE:**
```python
    word_count = len(keyword.split())
    is_question = utils.is_question_keyword(keyword)  # This now exists

    min_wc = client_cfg.get("min_keyword_word_count", 2)
    max_wc = client_cfg.get("max_keyword_word_count", 8)

    is_outside_range = word_count < min_wc or word_count > max_wc

    # Rule 15 (Refined with override): Check word count and potentially override for high-value keywords
    if is_outside_range and not is_question:
        sv = keyword_info.get("search_volume", 0)
        cpc = keyword_info.get("cpc")  # Get the value, which could be None
        if cpc is None:
            cpc = 0.0  # Default to 0.0 if it's None

        high_sv_override = client_cfg.get("high_value_sv_override_threshold", 10000)
        high_cpc_override = client_cfg.get("high_value_cpc_override_threshold", 5.0)

        if sv >= high_sv_override or cpc >= high_cpc_override:
            logging.getLogger(__name__).info(
                f"Override: High value SV/CPC bypasses word count rule for '{keyword}'."
            )
            pass  # Allow the keyword to proceed
        else:
            return (
                True,
                f"Rule 15: Non-question keyword word count ({word_count}) is outside the acceptable range ({min_wc}-{max_wc} words).",
                False,
            )
```

**REPLACE WITH:**
```python
    word_count = len(keyword.split())
    is_question = utils.is_question_keyword(keyword)

    min_wc = client_cfg.get("min_keyword_word_count", 2)
    max_wc = client_cfg.get("max_keyword_word_count", 8)

    is_outside_range = word_count < min_wc or word_count > max_wc

    # Rule 15 (Refined with override): Check word count and potentially override for high-value keywords
    if is_outside_range and not is_question:
        sv = search_volume  # Use reliable search volume from earlier
        cpc = keyword_info.get("cpc")
        if cpc is None:
            cpc = 0.0

        high_sv_override = client_cfg.get("high_value_sv_override_threshold", 10000)
        high_cpc_override = client_cfg.get("high_value_cpc_override_threshold", 5.0)
        
        # NEW: Long-tail keyword exception (5+ words get special treatment)
        is_long_tail = word_count >= 5
        
        # Long-tail keywords get lower KD tolerance and are valuable even with lower SV
        if is_long_tail:
            kd = keyword_props.get("keyword_difficulty", 100)
            if kd <= 30 and sv >= 20:  # Very low competition + minimal volume
                logging.getLogger(__name__).info(
                    f"Override: Long-tail keyword ({word_count} words, KD={kd}) with low competition bypasses word count rule for '{keyword}'."
                )
                # Store this as a "long_tail_opportunity" flag for scoring
                opportunity["is_long_tail_opportunity"] = True
                pass  # Allow the keyword to proceed
            elif sv >= high_sv_override or cpc >= high_cpc_override:
                logging.getLogger(__name__).info(
                    f"Override: High value long-tail keyword bypasses word count rule for '{keyword}'."
                )
                pass
            else:
                return (
                    True,
                    f"Rule 15: Long-tail keyword ({word_count} words) has insufficient value (SV={sv}, KD={kd}).",
                    False,
                )
        elif sv >= high_sv_override or cpc >= high_cpc_override:
            logging.getLogger(__name__).info(
                f"Override: High value SV/CPC bypasses word count rule for '{keyword}'."
            )
            pass  # Allow the keyword to proceed
        else:
            return (
                True,
                f"Rule 15: Non-question keyword word count ({word_count}) is outside the acceptable range ({min_wc}-{max_wc} words).",
                False,
            )
```

---

## TASK 9: Add SERP Data Freshness Check

### File: `disqualification_rules.py`
### Lines to Modify: 268-281

**CURRENT CODE:**
```python
    if serp_info.get("last_updated_time") and serp_info.get("previous_updated_time"):
        try:
            last_update = datetime.fromisoformat(
                serp_info["last_updated_time"].replace(" +00:00", "")
            )
            prev_update = datetime.fromisoformat(
                serp_info["previous_updated_time"].replace(" +00:00", "")
            )
            days_between_updates = (last_update - prev_update).days
            if days_between_updates < client_cfg.get("min_serp_stability_days", 14):
                return (
                    True,
                    f"Rule 19: Unstable SERP (updated every {days_between_updates} days).",
                    False,
                )
```

**REPLACE WITH:**
```python
    # NEW: Check SERP data freshness before stability check
    if serp_info.get("last_updated_time"):
        try:
            last_update = datetime.fromisoformat(
                serp_info["last_updated_time"].replace(" +00:00", "")
            )
            serp_age_days = (datetime.now() - last_update).days
            
            # Flag stale data but don't disqualify (add to opportunity metadata)
            if serp_age_days > 90:  # 3+ months old
                opportunity["serp_data_quality_warning"] = f"SERP data is {serp_age_days} days old (stale)"
                logging.getLogger(__name__).warning(
                    f"Stale SERP data for '{keyword}': {serp_age_days} days old. Consider manual review for fast-changing topics."
                )
            
            # Original stability check
            if serp_info.get("previous_updated_time"):
                prev_update = datetime.fromisoformat(
                    serp_info["previous_updated_time"].replace(" +00:00", "")
                )
                days_between_updates = (last_update - prev_update).days
                if days_between_updates < client_cfg.get("min_serp_stability_days", 14):
                    return (
                        True,
                        f"Rule 19: Unstable SERP (updated every {days_between_updates} days).",
                        False,
                    )
```

**ALSO MODIFY:** Add exception handling continuation

### Lines to Modify: 282-288

**CURRENT CODE:**
```python
        except ValueError:
            logging.getLogger(__name__).warning(
                f"Could not parse SERP update times for '{keyword}': {serp_info.get('last_updated_time')}, {serp_info.get('previous_updated_time')}"
            )
```

**REPLACE WITH:**
```python
        except ValueError:
            logging.getLogger(__name__).warning(
                f"Could not parse SERP update times for '{keyword}': {serp_info.get('last_updated_time')}, {serp_info.get('previous_updated_time')}"
            )
        except Exception as e:
            logging.getLogger(__name__).error(
                f"Unexpected error checking SERP freshness for '{keyword}': {str(e)}"
            )
```

---

## TASK 10: Add Content Difficulty Assessment to Discovery Results

### File: `run_discovery.py`
### Lines to Modify: 1-10 (imports section)

**CURRENT CODE:**
```python
import logging
from typing import List, Dict, Any, Optional

from data_access.database_manager import DatabaseManager
from external_apis.dataforseo_client_v2 import DataForSEOClientV2
from pipeline.step_01_discovery.keyword_expander import KeywordExpander
from pipeline.step_01_discovery.disqualification_rules import (
    apply_disqualification_rules,
)
from pipeline.step_01_discovery.cannibalization_checker import CannibalizationChecker
from pipeline.step_03_prioritization.scoring_engine import ScoringEngine
from pipeline.step_01_discovery.blog_content_qualifier import assign_status_from_score
```

**REPLACE WITH:**
```python
import logging
from typing import List, Dict, Any, Optional

from data_access.database_manager import DatabaseManager
from external_apis.dataforseo_client_v2 import DataForSEOClientV2
from pipeline.step_01_discovery.keyword_expander import KeywordExpander
from pipeline.step_01_discovery.disqualification_rules import (
    apply_disqualification_rules,
)
from pipeline.step_01_discovery.cannibalization_checker import CannibalizationChecker
from pipeline.step_03_prioritization.scoring_engine import ScoringEngine
from pipeline.step_01_discovery.blog_content_qualifier import assign_status_from_score
from core.utils import estimate_content_difficulty
```

### Lines to Modify: 82-102

**CURRENT CODE:**
```python
        else:
            # 4. Score the remaining keywords
            score, breakdown = scoring_engine.calculate_score(opp)
            opp["strategic_score"] = score
            opp["score_breakdown"] = breakdown

            # 5. Assign Status based on Strategic Score
            status, reason = assign_status_from_score(opp, score, client_cfg)
            pp["status"] = status
            opp["blog_qualification_status"] = status
            opp["blog_qualification_reason"] = reason
            status_counts[status.split("_")[0]] = (
                status_counts.get(status.split("_")[0], 0) + 1
            )  # count qualified/review/rejected

        processed_opportunities.append(opp)
```

**REPLACE WITH:**
```python
        else:
            # 4. Score the remaining keywords
            score, breakdown = scoring_engine.calculate_score(opp)
            opp["strategic_score"] = score
            opp["score_breakdown"] = breakdown

            # 5. Assign Status based on Strategic Score
            status, reason = assign_status_from_score(opp, score, client_cfg)
            opp["status"] = status
            opp["blog_qualification_status"] = status
            opp["blog_qualification_reason"] = reason
            status_counts[status.split("_")[0]] = (
                status_counts.get(status.split("_")[0], 0) + 1
            )
            
            # 6. NEW: Add content difficulty assessment for qualified/review keywords
            if status in ["qualified", "review"]:
                difficulty_data = estimate_content_difficulty(opp)
                opp["content_difficulty"] = difficulty_data
                logger.debug(
                    f"Content difficulty for '{opp.get('keyword')}': "
                    f"{difficulty_data['difficulty_level']} "
                    f"({difficulty_data['estimated_word_count']} words, "
                    f"{difficulty_data['production_time_hours']} hours)"
                )

        processed_opportunities.append(opp)
```

---

## TASK 11: Add Error Handling to Keyword Expansion

### File: `keyword_discovery/expander.py`
### Lines to Modify: 73-87

**CURRENT CODE:**
```python
        # Make a single burst call to the DataForSEOClientV2
        all_ideas, total_cost = self.client.get_keyword_ideas(
            seed_keywords=seed_keywords,
            location_code=location_code,
            language_code=language_code,
            client_cfg=self.config,
            discovery_modes=discovery_modes,
            filters=structured_filters, # Use the structured filters
            order_by=structured_orderby, # Use the structured order_by
            limit=limit,
            depth=depth, # This depth is for Related Keywords API specifically
            ignore_synonyms_override=final_ignore_synonyms,
            include_clickstream_override=final_include_clickstream_data,
            closely_variants_override=final_closely_variants,
            exact_match_override=final_exact_match,
        )
```

**REPLACE WITH:**
```python
        # Make a single burst call to the DataForSEOClientV2 with comprehensive error handling
        try:
            all_ideas, total_cost = self.client.get_keyword_ideas(
                seed_keywords=seed_keywords,
                location_code=location_code,
                language_code=language_code,
                client_cfg=self.config,
                discovery_modes=discovery_modes,
                filters=structured_filters,
                order_by=structured_orderby,
                limit=limit,
                depth=depth,
                ignore_synonyms_override=final_ignore_synonyms,
                include_clickstream_override=final_include_clickstream_data,
                closely_variants_override=final_closely_variants,
                exact_match_override=final_exact_match,
            )
        except ConnectionError as e:
            self.logger.error(f"Network connection error during keyword expansion: {str(e)}")
            raise RuntimeError(
                "Failed to connect to DataForSEO API. Please check your internet connection and try again."
            ) from e
        except TimeoutError as e:
            self.logger.error(f"API request timeout during keyword expansion: {str(e)}")
            raise RuntimeError(
                "DataForSEO API request timed out. The request may be too large. Try reducing the number of seed keywords or using stricter filters."
            ) from e
        except ValueError as e:
            # Catches invalid filter syntax, invalid parameters, etc.
            self.logger.error(f"Invalid request parameters during keyword expansion: {str(e)}")
            raise ValueError(
                f"Invalid parameters sent to DataForSEO API: {str(e)}. Please check your filters and configuration."
            ) from e
        except PermissionError as e:
            # Catches API quota exceeded, rate limits, authentication failures
            self.logger.error(f"API authorization/quota error during keyword expansion: {str(e)}")
            raise PermissionError(
                "DataForSEO API quota exceeded or authentication failed. Please check your API credits and credentials."
            ) from e
        except Exception as e:
            # Catch-all for unexpected errors
            self.logger.error(f"Unexpected error during keyword expansion: {str(e)}", exc_info=True)
            raise RuntimeError(
                f"Unexpected error during keyword expansion: {str(e)}. Please contact support if this persists."
            ) from e
```

### Lines to Modify: 88-91

**CURRENT CODE:**
```python
        self.logger.info(
            f"Burst discovery completed. Found {len(all_ideas)} raw keyword ideas. Cost: ${total_cost:.4f}"
        )
```

**REPLACE WITH:**
```python
        if not all_ideas:
            self.logger.warning(
                "Burst discovery completed but returned zero results. This may indicate overly restrictive filters or no data available for the seed keywords."
            )
        else:
            self.logger.info(
                f"Burst discovery completed successfully. Found {len(all_ideas)} raw keyword ideas. Cost: ${total_cost:.4f}"
            )
```

---

## TASK 12: Improve Filter System with Pre-Validation

### File: `keyword_discovery/filters.py`
### Lines to Modify: 1-30 (entire file)

**CURRENT CODE:**
```python
# pipeline/step_01_discovery/keyword_discovery/filters.py
import json
import logging
from typing import List, Any, Tuple, Dict

logger = logging.getLogger(__name__)

FORBIDDEN_API_FILTER_FIELDS = [
    "relevance",
    "sv_bing",
    "sv_clickstream",
]  # Define forbidden fields


def sanitize_filters_for_api(filters: List[Any]) -> List[Any]:
    """
    Removes any filters attempting to use forbidden internal metrics or data sources.
    """
    sanitized = []
    for item in filters:
        if isinstance(item, list) and len(item) >= 1 and isinstance(item[0], str):
            field_path = item[0].lower()
            if any(
                forbidden in field_path for forbidden in FORBIDDEN_API_FILTER_FIELDS
            ):
                logger.warning(
                    f"Forbidden field '{field_path}' detected in API filter. Removing it."
                )
                continue
        sanitized.append(item)
    return sanitized
```

**REPLACE WITH:**
```python
# pipeline/step_01_discovery/keyword_discovery/filters.py
import json
import logging
from typing import List, Any, Tuple, Dict, Optional

logger = logging.getLogger(__name__)

FORBIDDEN_API_FILTER_FIELDS = [
    "relevance",
    "sv_bing",
    "sv_clickstream",
]

VALID_OPERATORS = [
    "regex", "not_regex", "<", "<=", ">", ">=", "=", "<>", 
    "in", "not_in", "match", "not_match", "ilike", "not_ilike", 
    "like", "not_like"
]


def validate_filter_structure(filter_item: Any) -> Tuple[bool, Optional[str]]:
    """
    Validates that a filter item has the correct structure.
    
    Expected format: [field, operator, value] or logical operator string ("and"/"or")
    
    Returns:
        Tuple of (is_valid, error_message)
    """
    # Allow logical operators
    if isinstance(filter_item, str) and filter_item.lower() in ["and", "or"]:
        return True, None
    
    # Allow nested filter arrays
    if isinstance(filter_item, list):
        # Check if it's a nested array of filters
        if len(filter_item) > 0 and isinstance(filter_item[0], list):
            # Recursively validate nested filters
            for nested_item in filter_item:
                is_valid, error = validate_filter_structure(nested_item)
                if not is_valid:
                    return False, error
            return True, None
        
        # Validate standard filter format: [field, operator, value]
        if len(filter_item) != 3:
            return False, f"Filter must have exactly 3 elements [field, operator, value], got {len(filter_item)}"
        
        field, operator, value = filter_item
        
        if not isinstance(field, str):
            return False, f"Filter field must be a string, got {type(field).__name__}"
        
        if not isinstance(operator, str):
            return False, f"Filter operator must be a string, got {type(operator).__name__}"
        
        if operator not in VALID_OPERATORS:
            return False, f"Invalid operator '{operator}'. Valid operators: {', '.join(VALID_OPERATORS)}"
        
        # Validate value type based on operator
        if operator in ["in", "not_in"]:
            if not isinstance(value, (list, tuple)):
                return False, f"Operator '{operator}' requires a list/array value, got {type(value).__name__}"
        
        return True, None
    
    return False, f"Invalid filter structure: {type(filter_item).__name__}"


def sanitize_filters_for_api(filters: List[Any]) -> List[Any]:
    """
    Validates and removes any filters attempting to use forbidden internal metrics 
    or data sources. Also validates filter structure.
    
    Args:
        filters: List of filter conditions
        
    Returns:
        List of validated and sanitized filters
        
    Raises:
        ValueError: If filter structure is invalid
    """
    if not filters:
        return []
    
    sanitized = []
    removed_count = 0
    
    for idx, item in enumerate(filters):
        # Validate structure first
        is_valid, error_msg = validate_filter_structure(item)
        if not is_valid:
            logger.error(f"Invalid filter structure at index {idx}: {error_msg}")
            raise ValueError(f"Filter validation failed at index {idx}: {error_msg}")
        
        # Check for forbidden fields
        if isinstance(item, list) and len(item) >= 1 and isinstance(item[0], str):
            field_path = item[0].lower()
            if any(forbidden in field_path for forbidden in FORBIDDEN_API_FILTER_FIELDS):
                logger.warning(
                    f"Forbidden field '{field_path}' detected in API filter at index {idx}. Removing it."
                )
                removed_count += 1
                continue
        
        sanitized.append(item)
    
    if removed_count > 0:
        logger.info(f"Removed {removed_count} invalid filter(s) from API request")
    
    return sanitized
```

---

## TASK 13: Add Configuration Defaults File for Magic Numbers

### File: `core/discovery_defaults.py` (NEW FILE)
### Action: CREATE NEW FILE with this complete content:

```python
# core/discovery_defaults.py
"""
Centralized configuration defaults for keyword discovery and disqualification rules.

This module contains all default thresholds, limits, and magic numbers used throughout
the discovery pipeline. Values can be overridden via client_cfg.

Usage:
    from core.discovery_defaults import DISCOVERY_DEFAULTS
    threshold = client_cfg.get("min_search_volume", DISCOVERY_DEFAULTS["MIN_SEARCH_VOLUME"])
"""

DISCOVERY_DEFAULTS = {
    # === SEARCH VOLUME THRESHOLDS ===
    "MIN_SEARCH_VOLUME": 100,
    "HIGH_VALUE_SV_OVERRIDE": 10000,
    
    # === KEYWORD DIFFICULTY LIMITS ===
    "MAX_KD_HARD_LIMIT": 70,
    "LONG_TAIL_KD_THRESHOLD": 30,  # KD threshold for long-tail opportunities
    
    # === TREND ANALYSIS ===
    "YEARLY_TREND_DECLINE_THRESHOLD": -25,  # Percent
    "QUARTERLY_TREND_DECLINE_THRESHOLD": 0,  # Percent
    "TREND_LOOKBACK_MONTHS": 4,
    "TREND_DECLINE_RATIO": 0.5,  # 50% decline triggers warning
    "SEARCH_VOLUME_VOLATILITY_THRESHOLD": 1.5,  # Std dev / mean ratio
    
    # === SEASONALITY DETECTION ===
    "STRONG_SEASONAL_FACTOR": 5.0,  # Peak is 5x average
    "MODERATE_SEASONAL_FACTOR": 3.0,  # Peak is 3x average
    "MILD_SEASONAL_FACTOR": 2.0,  # Peak is 2x average
    
    # === COMPETITION METRICS ===
    "MAX_PAID_COMPETITION_SCORE": 0.8,
    "MAX_HIGH_TOP_OF_PAGE_BID": 15.0,  # USD
    "HIGH_VALUE_CPC_OVERRIDE": 5.0,  # USD
    "MAX_REFERRING_MAIN_DOMAINS_LIMIT": 100,
    "MAX_AVG_DOMAIN_RANK_THRESHOLD": 500,
    "MAX_PAGES_TO_DOMAIN_RATIO": 15,
    
    # === KEYWORD STRUCTURE ===
    "MIN_KEYWORD_WORD_COUNT": 2,
    "MAX_KEYWORD_WORD_COUNT": 8,
    "LONG_TAIL_WORD_COUNT_THRESHOLD": 5,
    "LONG_TAIL_MIN_SEARCH_VOLUME": 20,  # Lower SV acceptable for long-tail
    
    # === SERP ANALYSIS ===
    "CROWDED_SERP_FEATURES_THRESHOLD": 4,
    "HOSTILE_SERP_FEATURE_COUNT_THRESHOLD": 3,  # Number of hostile features to trigger rejection
    "MIN_SERP_STABILITY_DAYS": 14,
    "STALE_SERP_DATA_THRESHOLD_DAYS": 90,  # 3 months
    
    # === SCORING THRESHOLDS ===
    "QUALIFIED_THRESHOLD": 70,  # Score to auto-qualify
    "REVIEW_THRESHOLD": 50,  # Score for manual review
    
    # === INTENT CONFIGURATION ===
    "ALLOWED_INTENTS": ["informational"],
    "PROHIBITED_INTENTS": ["navigational"],
    
    # === API BEHAVIOR ===
    "DISCOVERY_IGNORE_SYNONYMS": False,
    "INCLUDE_CLICKSTREAM_DATA": False,
    "CLOSELY_VARIANTS": True,  # Changed default to True
    "DISCOVERY_EXACT_MATCH": False,
    "DEFAULT_LIMIT": 700,
    "MAX_LIMIT": 1000,
    "DEFAULT_RELATED_KEYWORDS_DEPTH": 1,
    
    # === CONTENT PRODUCTION ESTIMATES ===
    "BASE_CONTENT_PRODUCTION_HOURS": 2,
    "BASE_WORD_COUNT": 1000,
    "VIDEO_PRODUCTION_HOURS_ADDITION": 8,
    "EXPERT_CONTENT_WORD_COUNT": 2000,
    "EXPERT_CONTENT_HOURS": 8,
    "HIGH_COMPETITION_WORD_COUNT": 3000,
    "HIGH_COMPETITION_HOURS": 12,
}

# Hostile SERP features that indicate non-blog-friendly SERPs
HOSTILE_SERP_FEATURES = {
    # E-commerce/Shopping
    "shopping",
    "popular_products",
    "refine_products",
    "explore_brands",
    # Local business
    "local_pack",
    "map",
    "local_services",
    # Google tools/utilities
    "google_flights",
    "google_hotels",
    "hotels_pack",
    "math_solver",
    "currency_box",
    "stocks_box",
    # Other specific intents
    "app",
    "jobs",
}

# SERP features that compete for attention but don't necessarily mean rejection
ATTENTION_COMPETING_FEATURES = {
    "carousel",
    "featured_snippet",
    "people_also_ask",
    "images",
    "video",
    "short_videos",
}

# Technical topic indicators for content difficulty assessment
TECHNICAL_TOPIC_INDICATORS = [
    "api", "algorithm", "architecture", "protocol", "encryption",
    "optimization", "configuration", "implementation", "integration",
    "debugging", "framework", "library", "sdk", "cli", "authentication",
    "authorization", "middleware", "backend", "frontend", "database",
    "query", "schema", "migration", "deployment", "devops", "cicd",
    "container", "kubernetes", "docker", "microservices", "serverless",
]

# Valid filter operators for API requests
VALID_FILTER_OPERATORS = [
    "regex", "not_regex", "<", "<=", ">", ">=", "=", "<>",
    "in", "not_in", "match", "not_match", "ilike", "not_ilike",
    "like", "not_like"
]

# Fields forbidden from API filters (internal use only)
FORBIDDEN_API_FILTER_FIELDS = [
    "relevance",
    "sv_bing",
    "sv_clickstream",
]
```

---

## TASK 14: Update Disqualification Rules to Use Centralized Defaults

### File: `disqualification_rules.py`
### Lines to Modify: 1-8 (imports section)

**CURRENT CODE:**
```python
# pipeline/step_01_discovery/disqualification_rules.py
import logging
import re
from typing import Dict, Any, Tuple, Optional
from datetime import datetime
import numpy as np
from core import utils
from core.utils import get_reliable_search_volume, detect_seasonal_pattern
```

**REPLACE WITH:**
```python
# pipeline/step_01_discovery/disqualification_rules.py
import logging
import re
from typing import Dict, Any, Tuple, Optional
from datetime import datetime
import numpy as np
from core import utils
from core.utils import get_reliable_search_volume, detect_seasonal_pattern
from core.discovery_defaults import DISCOVERY_DEFAULTS, HOSTILE_SERP_FEATURES
```

### Lines to Modify: 103-107

**CURRENT CODE:**
```python
    # Tier 2: Volume & Trend Analysis
    if utils.safe_compare(
        search_volume, client_cfg.get("min_search_volume"), "lt"
    ):
        return (
            True,
            f"Rule 5: Below search volume floor (minimum: {client_cfg.get('min_search_volume', 100)} SV). Current: {search_volume} SV.",
            False,
        )
```

**REPLACE WITH:**
```python
    # Tier 2: Volume & Trend Analysis
    min_sv = client_cfg.get("min_search_volume", DISCOVERY_DEFAULTS["MIN_SEARCH_VOLUME"])
    if utils.safe_compare(search_volume, min_sv, "lt"):
        return (
            True,
            f"Rule 5: Below search volume floor (minimum: {min_sv} SV). Current: {search_volume} SV.",
            False,
        )
```

### Lines to Modify: 116-120

**CURRENT CODE:**
```python
            yearly_threshold = client_cfg.get("yearly_trend_decline_threshold", -25)
            quarterly_threshold = client_cfg.get("quarterly_trend_decline_threshold", 0)
```

**REPLACE WITH:**
```python
            yearly_threshold = client_cfg.get(
                "yearly_trend_decline_threshold", 
                DISCOVERY_DEFAULTS["YEARLY_TREND_DECLINE_THRESHOLD"]
            )
            quarterly_threshold = client_cfg.get(
                "quarterly_trend_decline_threshold", 
                DISCOVERY_DEFAULTS["QUARTERLY_TREND_DECLINE_THRESHOLD"]
            )
```

### Lines to Modify: 135-138

**CURRENT CODE:**
```python
        if len(volumes) > 1 and np.mean(volumes) > 0:
            volatility_threshold = client_cfg.get(
                "search_volume_volatility_threshold", 1.5
            )
```

**REPLACE WITH:**
```python
        if len(volumes) > 1 and np.mean(volumes) > 0:
            volatility_threshold = client_cfg.get(
                "search_volume_volatility_threshold", 
                DISCOVERY_DEFAULTS["SEARCH_VOLUME_VOLATILITY_THRESHOLD"]
            )
```

### Lines to Modify: 177-182

**CURRENT CODE:**
```python
    # Tier 3: Commercial & Competitive Analysis
    if utils.safe_compare(
        keyword_info.get("competition"),
        client_cfg.get("max_paid_competition_score", 0.8),
        "gt",
    ) and (keyword_info.get("competition_level") == "HIGH"):
```

**REPLACE WITH:**
```python
    # Tier 3: Commercial & Competitive Analysis
    max_competition = client_cfg.get(
        "max_paid_competition_score", 
        DISCOVERY_DEFAULTS["MAX_PAID_COMPETITION_SCORE"]
    )
    if utils.safe_compare(
        keyword_info.get("competition"),
        max_competition,
        "gt",
    ) and (keyword_info.get("competition_level") == "HIGH"):
```

### Lines to Modify: 185-191

**CURRENT CODE:**
```python
    if utils.safe_compare(
        keyword_info.get("high_top_of_page_bid"),
        client_cfg.get("max_high_top_of_page_bid", 15.0),
        "gt",
    ):
        return (
            True,
            f"Rule 9: Prohibitively high CPC bids (>${client_cfg.get('max_high_top_of_page_bid', 15.00)}).",
            False,
        )
```

**REPLACE WITH:**
```python
    max_cpc = client_cfg.get(
        "max_high_top_of_page_bid", 
        DISCOVERY_DEFAULTS["MAX_HIGH_TOP_OF_PAGE_BID"]
    )
    if utils.safe_compare(
        keyword_info.get("high_top_of_page_bid"),
        max_cpc,
        "gt",
    ):
        return (
            True,
            f"Rule 9: Prohibitively high CPC bids (>${max_cpc:.2f}).",
            False,
        )
```

### Lines to Modify: 193-199

**CURRENT CODE:**
```python
    if utils.safe_compare(
        keyword_props.get("keyword_difficulty"),
        client_cfg.get("max_kd_hard_limit", 70),
        "gt",
    ):
        return (
            True,
            f"Rule 10: Extreme keyword difficulty (>{client_cfg.get('max_kd_hard_limit', 70)}).",
            False,
        )
```

**REPLACE WITH:**
```python
    max_kd = client_cfg.get("max_kd_hard_limit", DISCOVERY_DEFAULTS["MAX_KD_HARD_LIMIT"])
    if utils.safe_compare(
        keyword_props.get("keyword_difficulty"),
        max_kd,
        "gt",
    ):
        return (
            True,
            f"Rule 10: Extreme keyword difficulty (>{max_kd}).",
            False,
        )
```

### Lines to Modify: 201-207

**CURRENT CODE:**
```python
    if utils.safe_compare(
        avg_backlinks.get("referring_main_domains"),
        client_cfg.get("max_referring_main_domains_limit", 100),
        "gt",
    ):
        return (
            True,
            f"Rule 11: Overly authoritative competitor domains (>{client_cfg.get('max_referring_main_domains_limit', 100)} referring main domains).",
            False,
        )
```

**REPLACE WITH:**
```python
    max_ref_domains = client_cfg.get(
        "max_referring_main_domains_limit", 
        DISCOVERY_DEFAULTS["MAX_REFERRING_MAIN_DOMAINS_LIMIT"]
    )
    if utils.safe_compare(
        avg_backlinks.get("referring_main_domains"),
        max_ref_domains,
        "gt",
    ):
        return (
            True,
            f"Rule 11: Overly authoritative competitor domains (>{max_ref_domains} referring main domains).",
            False,
        )
```

### Lines to Modify: 209-215

**CURRENT CODE:**
```python
    if utils.safe_compare(
        avg_backlinks.get("main_domain_rank"),
        client_cfg.get("max_avg_domain_rank_threshold", 500),
        "lt",
    ):
        return (
            True,
            f"Rule 12: SERP dominated by high-authority domains (avg rank < {client_cfg.get('max_avg_domain_rank_threshold', 500)}).",
            False,
        )
```

**REPLACE WITH:**
```python
    max_domain_rank = client_cfg.get(
        "max_avg_domain_rank_threshold", 
        DISCOVERY_DEFAULTS["MAX_AVG_DOMAIN_RANK_THRESHOLD"]
    )
    if utils.safe_compare(
        avg_backlinks.get("main_domain_rank"),
        max_domain_rank,
        "lt",
    ):
        return (
            True,
            f"Rule 12: SERP dominated by high-authority domains (avg rank < {max_domain_rank}).",
            False,
        )
```

### Lines to Modify: 217-223

**CURRENT CODE:**
```python
    if (avg_backlinks.get("referring_domains") or 0) > 0:
        pages_to_domain_ratio = (avg_backlinks.get("referring_pages") or 0) / (
            avg_backlinks.get("referring_domains") or 1
        )
        if pages_to_domain_ratio > client_cfg.get("max_pages_to_domain_ratio", 15):
            return (
                True,
                "Rule 13: Potential spammy competitor profile (high page/domain ratio).",
                False,
            )
```

**REPLACE WITH:**
```python
    if (avg_backlinks.get("referring_domains") or 0) > 0:
        pages_to_domain_ratio = (avg_backlinks.get("referring_pages") or 0) / (
            avg_backlinks.get("referring_domains") or 1
        )
        max_ratio = client_cfg.get(
            "max_pages_to_domain_ratio", 
            DISCOVERY_DEFAULTS["MAX_PAGES_TO_DOMAIN_RATIO"]
        )
        if pages_to_domain_ratio > max_ratio:
            return (
                True,
                f"Rule 13: Potential spammy competitor profile (page/domain ratio: {pages_to_domain_ratio:.1f} > {max_ratio}).",
                False,
            )
```

### Lines to Modify: 235-240

**CURRENT CODE:**
```python
    min_wc = client_cfg.get("min_keyword_word_count", 2)
    max_wc = client_cfg.get("max_keyword_word_count", 8)
```

**REPLACE WITH:**
```python
    min_wc = client_cfg.get("min_keyword_word_count", DISCOVERY_DEFAULTS["MIN_KEYWORD_WORD_COUNT"])
    max_wc = client_cfg.get("max_keyword_word_count", DISCOVERY_DEFAULTS["MAX_KEYWORD_WORD_COUNT"])
```

### Lines to Modify: 248-250

**CURRENT CODE:**
```python
        high_sv_override = client_cfg.get("high_value_sv_override_threshold", 10000)
        high_cpc_override = client_cfg.get("high_value_cpc_override_threshold", 5.0)
```

**REPLACE WITH:**
```python
        high_sv_override = client_cfg.get(
            "high_value_sv_override_threshold", 
            DISCOVERY_DEFAULTS["HIGH_VALUE_SV_OVERRIDE"]
        )
        high_cpc_override = client_cfg.get(
            "high_value_cpc_override_threshold", 
            DISCOVERY_DEFAULTS["HIGH_VALUE_CPC_OVERRIDE"]
        )
```

### Lines to Modify: 252-256

**CURRENT CODE:**
```python
        # NEW: Long-tail keyword exception (5+ words get special treatment)
        is_long_tail = word_count >= 5
        
        # Long-tail keywords get lower KD tolerance and are valuable even with lower SV
        if is_long_tail:
            kd = keyword_props.get("keyword_difficulty", 100)
            if kd <= 30 and sv >= 20:  # Very low competition + minimal volume
```

**REPLACE WITH:**
```python
        # NEW: Long-tail keyword exception (5+ words get special treatment)
        long_tail_threshold = client_cfg.get(
            "long_tail_word_count_threshold", 
            DISCOVERY_DEFAULTS["LONG_TAIL_WORD_COUNT_THRESHOLD"]
        )
        is_long_tail = word_count >= long_tail_threshold
        
        # Long-tail keywords get lower KD tolerance and are valuable even with lower SV
        if is_long_tail:
            kd = keyword_props.get("keyword_difficulty", 100)
            long_tail_kd_max = client_cfg.get(
                "long_tail_kd_threshold", 
                DISCOVERY_DEFAULTS["LONG_TAIL_KD_THRESHOLD"]
            )
            long_tail_min_sv = client_cfg.get(
                "long_tail_min_search_volume", 
                DISCOVERY_DEFAULTS["LONG_TAIL_MIN_SEARCH_VOLUME"]
            )
            if kd <= long_tail_kd_max and sv >= long_tail_min_sv:
```

### Lines to Modify: 287-291

**CURRENT CODE:**
```python
    serp_types = set(serp_info.get("serp_item_types", []))

    crowded_features = {
        "video",
        "images",
        "people_also_ask",
        "carousel",
        "featured_snippet",
        "short_videos",
    }
    if len(serp_types.intersection(crowded_features)) > client_cfg.get(
        "crowded_serp_features_threshold", 4
    ):
```

**REPLACE WITH:**
```python
    serp_types = set(serp_info.get("serp_item_types", []))

    from core.discovery_defaults import ATTENTION_COMPETING_FEATURES
    
    crowded_threshold = client_cfg.get(
        "crowded_serp_features_threshold", 
        DISCOVERY_DEFAULTS["CROWDED_SERP_FEATURES_THRESHOLD"]
    )
    if len(serp_types.intersection(ATTENTION_COMPETING_FEATURES)) > crowded_threshold:
```

### Lines to Modify: 293-296

**CURRENT CODE:**
```python
        return (
            True,
            f"Rule 17: SERP is overly crowded (>{client_cfg.get('crowded_serp_features_threshold', 4)} attention-grabbing features).",
            False,
        )
```

**REPLACE WITH:**
```python
        return (
            True,
            f"Rule 17: SERP is overly crowded (>{crowded_threshold} attention-grabbing features).",
            False,
        )
        ```

### Lines to Modify: 306-310

**CURRENT CODE:**
```python
                days_between_updates = (last_update - prev_update).days
                if days_between_updates < client_cfg.get("min_serp_stability_days", 14):
                    return (
                        True,
                        f"Rule 19: Unstable SERP (updated every {days_between_updates} days).",
                        False,
                    )
```

**REPLACE WITH:**
```python
                days_between_updates = (last_update - prev_update).days
                min_stability = client_cfg.get(
                    "min_serp_stability_days", 
                    DISCOVERY_DEFAULTS["MIN_SERP_STABILITY_DAYS"]
                )
                if days_between_updates < min_stability:
                    return (
                        True,
                        f"Rule 19: Unstable SERP (updated every {days_between_updates} days, minimum: {min_stability}).",
                        False,
                    )
```

### Lines to Modify: 343-367 (update _check_hostile_serp_environment function to use constants)

**FIND THIS CODE IN THE FUNCTION:**
```python
    # Define hostile features based on detailed SERP analysis
    HOSTILE_FEATURES = {
        # Strong transactional/e-commerce intent
        "shopping",
        "popular_products",
        "refine_products",
        "explore_brands",
        # Strong local intent
        "local_pack",
        "map",
        "local_services",
        # Purely transactional/utility intent (Google-owned tools)
        "google_flights",
        "google_hotels",
        "hotels_pack",
        # App-related intent
        "app",
        # Job-seeking intent
        "jobs",
        # Direct utility/tool intent
        "math_solver",
        "currency_box",
        "stocks_box",
    }

    found_hostile_features = serp_types.intersection(HOSTILE_FEATURES)
```

**REPLACE WITH:**
```python
    # Use centralized hostile features definition
    found_hostile_features = serp_types.intersection(HOSTILE_SERP_FEATURES)
```

### Lines to Modify: 374-377

**CURRENT CODE:**
```python
    # Only reject if BOTH conditions are true:
    # 1. Multiple hostile features present (3+)
    # 2. No organic results OR very few organic signals
    if hostile_count >= 3 and not has_organic:
```

**REPLACE WITH:**
```python
    # Only reject if BOTH conditions are true:
    # 1. Multiple hostile features present (configurable threshold)
    # 2. No organic results OR very few organic signals
    hostile_threshold = DISCOVERY_DEFAULTS["HOSTILE_SERP_FEATURE_COUNT_THRESHOLD"]
    if hostile_count >= hostile_threshold and not has_organic:
```

---

## TASK 15: Update Core Utils to Use Centralized Configuration

### File: `core/utils.py`
### Action: Update the detect_seasonal_pattern function to use constants

**FIND THIS CODE (added in Task 3):**
```python
    # Determine seasonality classification
    if seasonality_factor >= 5.0:
        pattern_type = "strong_seasonal"
        is_seasonal = True
    elif seasonality_factor >= 3.0:
        pattern_type = "moderate_seasonal"
        is_seasonal = True
    elif seasonality_factor >= 2.0:
        pattern_type = "mild_seasonal"
        is_seasonal = True
    else:
        pattern_type = "evergreen"
        is_seasonal = False
```

**REPLACE WITH:**
```python
    from core.discovery_defaults import DISCOVERY_DEFAULTS
    
    # Determine seasonality classification
    if seasonality_factor >= DISCOVERY_DEFAULTS["STRONG_SEASONAL_FACTOR"]:
        pattern_type = "strong_seasonal"
        is_seasonal = True
    elif seasonality_factor >= DISCOVERY_DEFAULTS["MODERATE_SEASONAL_FACTOR"]:
        pattern_type = "moderate_seasonal"
        is_seasonal = True
    elif seasonality_factor >= DISCOVERY_DEFAULTS["MILD_SEASONAL_FACTOR"]:
        pattern_type = "mild_seasonal"
        is_seasonal = True
    else:
        pattern_type = "evergreen"
        is_seasonal = False
```

### File: `core/utils.py`
### Action: Update estimate_content_difficulty function to use constants

**FIND THIS CODE (added in Task 4):**
```python
    difficulty_level = "easy"
    estimated_word_count = 1000
    requires_video = False
    requires_expert = False
    production_time_hours = 2
```

**REPLACE WITH:**
```python
    from core.discovery_defaults import DISCOVERY_DEFAULTS, TECHNICAL_TOPIC_INDICATORS
    
    difficulty_level = "easy"
    estimated_word_count = DISCOVERY_DEFAULTS["BASE_WORD_COUNT"]
    requires_video = False
    requires_expert = False
    production_time_hours = DISCOVERY_DEFAULTS["BASE_CONTENT_PRODUCTION_HOURS"]
```

**FIND THIS CODE:**
```python
    # Video requirement detection
    if "video" in serp_types or "short_videos" in serp_types:
        requires_video = True
        difficulty_level = "hard"
        production_time_hours += 8
```

**REPLACE WITH:**
```python
    # Video requirement detection
    if "video" in serp_types or "short_videos" in serp_types:
        requires_video = True
        difficulty_level = "hard"
        production_time_hours += DISCOVERY_DEFAULTS["VIDEO_PRODUCTION_HOURS_ADDITION"]
```

**FIND THIS CODE:**
```python
    # Competitor authority check
    referring_domains = avg_backlinks.get("referring_main_domains", 0)
    if referring_domains > 50:
        estimated_word_count = 2000
        difficulty_level = "medium"
        production_time_hours = 6
    
    if referring_domains > 100:
        estimated_word_count = 3000
        difficulty_level = "hard"
        production_time_hours = 12
        requires_expert = True
```

**REPLACE WITH:**
```python
    # Competitor authority check
    referring_domains = avg_backlinks.get("referring_main_domains", 0)
    if referring_domains > 50:
        estimated_word_count = DISCOVERY_DEFAULTS["EXPERT_CONTENT_WORD_COUNT"]
        difficulty_level = "medium"
        production_time_hours = DISCOVERY_DEFAULTS["EXPERT_CONTENT_HOURS"]
    
    if referring_domains > 100:
        estimated_word_count = DISCOVERY_DEFAULTS["HIGH_COMPETITION_WORD_COUNT"]
        difficulty_level = "hard"
        production_time_hours = DISCOVERY_DEFAULTS["HIGH_COMPETITION_HOURS"]
        requires_expert = True
```

**FIND THIS CODE:**
```python
    # Technical topic detection (based on keyword patterns)
    technical_indicators = [
        "api", "algorithm", "architecture", "protocol", "encryption",
        "optimization", "configuration", "implementation", "integration",
        "debugging", "framework", "library", "sdk", "cli"
    ]
    
    keyword_lower = keyword.lower()
    if any(indicator in keyword_lower for indicator in technical_indicators):
```

**REPLACE WITH:**
```python
    # Technical topic detection (based on keyword patterns)
    keyword_lower = keyword.lower()
    if any(indicator in keyword_lower for indicator in TECHNICAL_TOPIC_INDICATORS):
```

**FIND THIS CODE:**
```python
        requires_expert = True
        if difficulty_level == "easy":
            difficulty_level = "medium"
        estimated_word_count = max(estimated_word_count, 2000)
        production_time_hours = max(production_time_hours, 8)
```

**REPLACE WITH:**
```python
        requires_expert = True
        if difficulty_level == "easy":
            difficulty_level = "medium"
        estimated_word_count = max(estimated_word_count, DISCOVERY_DEFAULTS["EXPERT_CONTENT_WORD_COUNT"])
        production_time_hours = max(production_time_hours, DISCOVERY_DEFAULTS["EXPERT_CONTENT_HOURS"])
```

**FIND THIS CODE:**
```python
    # Adjust for keyword difficulty
    kd = keyword_props.get("keyword_difficulty", 0)
    if kd > 60 and difficulty_level != "expert":
        difficulty_level = "hard"
        production_time_hours = max(production_time_hours, 10)
    
    # SERP feature crowding adjustment
    attention_features = {"carousel", "featured_snippet", "people_also_ask", "images", "shopping"}
    crowding_count = len(serp_types.intersection(attention_features))
```

**REPLACE WITH:**
```python
    # Adjust for keyword difficulty
    kd = keyword_props.get("keyword_difficulty", 0)
    if kd > 60 and difficulty_level != "expert":
        difficulty_level = "hard"
        production_time_hours = max(production_time_hours, DISCOVERY_DEFAULTS["EXPERT_CONTENT_HOURS"] + 2)
    
    # SERP feature crowding adjustment
    from core.discovery_defaults import ATTENTION_COMPETING_FEATURES
    crowding_count = len(serp_types.intersection(ATTENTION_COMPETING_FEATURES))
```

---

## TASK 16: Update Filter Module to Use Centralized Configuration

### File: `keyword_discovery/filters.py`
### Lines to Modify: 1-5 (imports)

**CURRENT CODE:**
```python
# pipeline/step_01_discovery/keyword_discovery/filters.py
import json
import logging
from typing import List, Any, Tuple, Dict, Optional

logger = logging.getLogger(__name__)
```

**REPLACE WITH:**
```python
# pipeline/step_01_discovery/keyword_discovery/filters.py
import json
import logging
from typing import List, Any, Tuple, Dict, Optional
from core.discovery_defaults import VALID_FILTER_OPERATORS, FORBIDDEN_API_FILTER_FIELDS

logger = logging.getLogger(__name__)
```

### Lines to Modify: 7-20

**CURRENT CODE:**
```python
FORBIDDEN_API_FILTER_FIELDS = [
    "relevance",
    "sv_bing",
    "sv_clickstream",
]

VALID_OPERATORS = [
    "regex", "not_regex", "<", "<=", ">", ">=", "=", "<>", 
    "in", "not_in", "match", "not_match", "ilike", "not_ilike", 
    "like", "not_like"
]
```

**REPLACE WITH:**
```python
# Use centralized configuration from discovery_defaults
# (No local redefinition needed - imported at top)
```

### Lines to Modify: 44-46

**CURRENT CODE:**
```python
        if operator not in VALID_OPERATORS:
            return False, f"Invalid operator '{operator}'. Valid operators: {', '.join(VALID_OPERATORS)}"
```

**REPLACE WITH:**
```python
        if operator not in VALID_FILTER_OPERATORS:
            return False, f"Invalid operator '{operator}'. Valid operators: {', '.join(VALID_FILTER_OPERATORS)}"
```

---

## TASK 17: Add Comprehensive Logging for Discovery Statistics

### File: `run_discovery.py`
### Lines to Modify: 104-115

**CURRENT CODE:**
```python
    disqualified_count = status_counts.get("rejected", 0)
    passed_count = status_counts.get("qualified", 0) + status_counts.get("review", 0)

    logger.info(
        f"Scoring and Qualification complete. Passed: {passed_count}, Rejected: {disqualified_count}."
    )

    stats = {
        **expansion_result,
        "disqualification_reasons": disqualification_reasons,
        "disqualified_count": disqualified_count,
        "final_qualified_count": passed_count,
    }
```

**REPLACE WITH:**
```python
    qualified_count = status_counts.get("qualified", 0)
    review_count = status_counts.get("review", 0)
    rejected_count = status_counts.get("rejected", 0)
    passed_count = qualified_count + review_count
    
    # Calculate additional statistics
    total_processed = len(processed_opportunities)
    qualification_rate = (qualified_count / total_processed * 100) if total_processed > 0 else 0
    
    # Count opportunities by difficulty level
    difficulty_breakdown = {"easy": 0, "medium": 0, "hard": 0, "expert": 0}
    long_tail_count = 0
    seasonal_count = 0
    
    for opp in processed_opportunities:
        if opp.get("content_difficulty"):
            level = opp["content_difficulty"].get("difficulty_level", "unknown")
            if level in difficulty_breakdown:
                difficulty_breakdown[level] += 1
        
        if opp.get("is_long_tail_opportunity"):
            long_tail_count += 1
        
        seasonality = opp.get("seasonality_analysis", {})
        if seasonality.get("is_seasonal"):
            seasonal_count += 1
    
    logger.info("=" * 80)
    logger.info("DISCOVERY PHASE COMPLETE - SUMMARY STATISTICS")
    logger.info("=" * 80)
    logger.info(f"Total Keywords Processed: {total_processed}")
    logger.info(f"API Cost: ${expansion_result.get('total_cost', 0):.4f}")
    logger.info("-" * 80)
    logger.info("STATUS BREAKDOWN:")
    logger.info(f"  ✅ Qualified: {qualified_count} ({qualification_rate:.1f}%)")
    logger.info(f"  ⚠️  Review: {review_count}")
    logger.info(f"  ❌ Rejected: {rejected_count}")
    logger.info("-" * 80)
    logger.info("CONTENT DIFFICULTY DISTRIBUTION:")
    for level, count in difficulty_breakdown.items():
        if count > 0:
            logger.info(f"  {level.capitalize()}: {count}")
    logger.info("-" * 80)
    logger.info("SPECIAL OPPORTUNITIES:")
    logger.info(f"  🎯 Long-tail opportunities: {long_tail_count}")
    logger.info(f"  📅 Seasonal keywords: {seasonal_count}")
    logger.info("-" * 80)
    
    if disqualification_reasons:
        logger.info("TOP DISQUALIFICATION REASONS:")
        sorted_reasons = sorted(
            disqualification_reasons.items(), 
            key=lambda x: x[1], 
            reverse=True
        )[:5]
        for reason, count in sorted_reasons:
            logger.info(f"  • {reason}: {count}")
    
    logger.info("=" * 80)

    stats = {
        **expansion_result,
        "disqualification_reasons": disqualification_reasons,
        "disqualified_count": rejected_count,
        "final_qualified_count": qualified_count,
        "review_count": review_count,
        "total_passed_count": passed_count,
        "qualification_rate": round(qualification_rate, 2),
        "difficulty_breakdown": difficulty_breakdown,
        "long_tail_count": long_tail_count,
        "seasonal_count": seasonal_count,
    }
```

---

## TASK 18: Add Example Configuration File for Client Settings

### File: `config/example_client_config.json` (NEW FILE)
### Action: CREATE NEW FILE with this complete content:

```json
{
  "_comment": "Example client configuration for keyword discovery pipeline",
  "_documentation": "All threshold values shown are defaults. Override any value to customize behavior for specific clients.",
  
  "client_id": "example_client_001",
  "client_name": "Example SaaS Company",
  "target_domain": "example.com",
  
  "_section_api_settings": "=== API & DATA SOURCE SETTINGS ===",
  "location_code": 2840,
  "location_name": "United States",
  "language_code": "en",
  "language_name": "English",
  "include_clickstream_data": true,
  "_note_clickstream": "Enable for more accurate search volume (doubles API cost)",
  
  "_section_discovery_behavior": "=== KEYWORD DISCOVERY BEHAVIOR ===",
  "discovery_ignore_synonyms": false,
  "closely_variants": true,
  "_note_closely_variants": "IMPORTANT: Set to true to include plural forms, synonyms, and variations (recommended)",
  "discovery_exact_match": false,
  "_note_exact_match": "Set to true only for very specific branded keyword research",
  
  "_section_volume_thresholds": "=== SEARCH VOLUME THRESHOLDS ===",
  "min_search_volume": 50,
  "_note_min_sv": "Lowered from default 100 to capture long-tail opportunities",
  "high_value_sv_override_threshold": 5000,
  "_note_high_sv": "Keywords above this volume bypass some restrictions",
  
  "_section_difficulty_limits": "=== KEYWORD DIFFICULTY LIMITS ===",
  "max_kd_hard_limit": 60,
  "_note_kd": "Adjusted for mid-authority site (DA ~40). Lower for new sites, higher for established brands",
  "long_tail_kd_threshold": 35,
  "long_tail_min_search_volume": 20,
  "_note_long_tail": "Long-tail keywords (5+ words) can have lower volume but should have low competition",
  
  "_section_trend_analysis": "=== TREND & SEASONALITY ===",
  "yearly_trend_decline_threshold": -30,
  "quarterly_trend_decline_threshold": -10,
  "_note_trends": "More lenient than defaults to avoid over-filtering declining-but-viable keywords",
  "search_volume_volatility_threshold": 2.0,
  "_note_volatility": "Increased to allow moderately seasonal keywords",
  
  "_section_competition": "=== COMPETITION & COMMERCIAL METRICS ===",
  "max_paid_competition_score": 0.9,
  "max_high_top_of_page_bid": 20.0,
  "high_value_cpc_override_threshold": 8.0,
  "_note_cpc": "Higher CPC tolerance for B2B/SaaS (indicates commercial value)",
  "max_referring_main_domains_limit": 150,
  "max_avg_domain_rank_threshold": 400,
  "max_pages_to_domain_ratio": 20,
  
  "_section_keyword_structure": "=== KEYWORD STRUCTURE RULES ===",
  "min_keyword_word_count": 2,
  "max_keyword_word_count": 10,
  "_note_word_count": "Increased max to capture long-tail B2B queries",
  "long_tail_word_count_threshold": 5,
  
  "_section_serp_analysis": "=== SERP ENVIRONMENT ===",
  "crowded_serp_features_threshold": 5,
  "_note_crowded": "Increased tolerance for SERP features (we can compete with good content)",
  "hostile_serp_feature_count_threshold": 3,
  "min_serp_stability_days": 21,
  "stale_serp_data_threshold_days": 60,
  "_note_serp_data": "Stricter freshness requirement for fast-moving SaaS industry",
  
  "_section_intent_filtering": "=== SEARCH INTENT FILTERING ===",
  "allowed_intents": ["informational", "commercial"],
  "_note_intents": "Including 'commercial' for product comparison content strategy",
  "prohibited_intents": ["navigational"],
  "_note_prohibited": "Navigational queries rarely convert for non-brand content",
  
  "_section_scoring": "=== SCORING & QUALIFICATION THRESHOLDS ===",
  "qualified_threshold": 65,
  "_note_qualified": "Lowered slightly to be less restrictive (default: 70)",
  "review_threshold": 45,
  "_note_review": "Lowered to capture more marginal opportunities for manual review (default: 50)",
  
  "_section_negative_keywords": "=== NEGATIVE KEYWORD FILTERS ===",
  "negative_keywords": [
    "porn", "xxx", "nude", "sex",
    "torrent", "crack", "keygen", "pirate",
    "cheap", "discount", "coupon",
    "near me", "in [city]",
    "competitor_brand_name"
  ],
  "_note_negative": "Customize this list based on your brand values and business model",
  
  "_section_content_production": "=== CONTENT PRODUCTION ESTIMATES ===",
  "base_content_production_hours": 3,
  "base_word_count": 1200,
  "_note_production": "Adjusted for your team's actual production capabilities",
  "video_production_hours_addition": 12,
  "expert_content_word_count": 2500,
  "expert_content_hours": 10,
  "high_competition_word_count": 3500,
  "high_competition_hours": 16,
  
  "_section_business_context": "=== BUSINESS CONTEXT (FOR FUTURE USE) ===",
  "domain_authority": 42,
  "content_velocity": 8,
  "_note_velocity": "Articles published per month",
  "business_model": "saas",
  "_note_business_model": "Options: saas, ecommerce, affiliate, local, b2b_services",
  "target_audience": "business_professionals",
  "_note_audience": "Options: beginners, professionals, experts, general_consumers",
  "primary_monetization": "lead_generation",
  "_note_monetization": "Options: lead_generation, ecommerce_sales, ad_revenue, affiliate_commissions"
}
```

---

## TASK 19: Create README Documentation for Configuration

### File: `docs/CONFIGURATION_GUIDE.md` (NEW FILE)
### Action: CREATE NEW FILE with this complete content:

```markdown
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
- Competitors: Brand names you don't want to