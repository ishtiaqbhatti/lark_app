# core/utils.py
import logging
import re
from typing import Optional, Union, Dict, Any, List
from datetime import datetime


def slugify(text: str) -> str:
    """
    Convert a string to a URL-friendly slug.
    """
    if not text:
        return ""
    text = text.lower()
    # Remove special characters
    text = re.sub(r"[^\w\s-]", "", text)
    # Replace spaces with hyphens
    text = re.sub(r"\s+", "-", text)
    return text


def is_question_keyword(keyword: str) -> bool:
    """
    Checks if a keyword is likely a question.
    Covers common question formats and leading words.
    """
    if not keyword:
        return False

    keyword_lower = keyword.lower().strip()

    # Common question prefixes
    question_starters = [
        "what",
        "when",
        "where",
        "who",
        "why",
        "how",
        "which",
        "whose",
        "is",
        "are",
        "am",
        "was",
        "were",
        "do",
        "does",
        "did",
        "can",
        "could",
        "will",
        "would",
        "should",
        "may",
        "might",
        "have",
        "has",
        "had",
        "are there",
        "is there",
    ]

    # Check if the keyword starts with a question word or ends with a question mark
    if keyword_lower.endswith("?"):
        return True

    for starter in question_starters:
        if keyword_lower.startswith(starter + " "):
            return True

    return False


def safe_compare(
    value: Optional[Union[int, float]],
    threshold: Optional[Union[int, float]],
    operation: str,
) -> bool:
    """
    Safely compares a potentially None value against a potentially None threshold.
    Returns False if either value is None to prevent TypeErrors.

    :param value: The value to check (e.g., from API data).
    :param threshold: The threshold to compare against (e.g., from config).
    :param operation: The comparison to perform ('gt' for >, 'lt' for <).
    :return: Boolean result of the comparison, or False if unsafe.
    """
    if value is None or threshold is None:
        return False

    if operation == "gt":
        return value > threshold
    elif operation == "lt":
        return value < threshold

    return False


def parse_datetime_string(dt_str: Optional[str]) -> Optional[str]:
    """
    Parses a DataForSEO datetime string (e.g., "yyyy-mm-dd hh-mm-ss +00:00")
    into a consistent ISO format string or returns None.
    """
    if not dt_str:
        return None

    # Remove timezone offset for consistent parsing if it's always +00:00
    cleaned_dt_str = dt_str.replace(" +00:00", "").strip()

    formats = [
        "%Y-%m-%d %H:%M:%S",
        "%Y-%m-%dT%H:%M:%S",  # Added ISO 8601 format
        "%Y-%m-%d %H:%M:%S.%f",  # With microseconds
        "%Y-%m-%d",  # Date only
    ]

    for fmt in formats:
        try:
            return datetime.strptime(cleaned_dt_str, fmt).isoformat()
        except ValueError:
            pass

    logging.getLogger(__name__).warning(
        f"Could not parse datetime string: {dt_str}. Returning None."
    )
    return None


def calculate_serp_times(
    datetime_str: Optional[str], previous_datetime_str: Optional[str]
) -> Dict[str, Optional[int]]:
    """
    Calculates the age of the SERP and the interval between the last two updates.
    """
    days_ago = None
    update_interval_days = None

    if datetime_str:
        parsed_date_iso = parse_datetime_string(datetime_str)
        if parsed_date_iso:
            serp_date = datetime.fromisoformat(parsed_date_iso)
            days_ago = (datetime.utcnow() - serp_date).days
        else:
            logging.getLogger(__name__).warning(
                f"Could not parse SERP datetime for days_ago: {datetime_str}"
            )

    if datetime_str and previous_datetime_str:
        parsed_last_update_iso = parse_datetime_string(datetime_str)
        parsed_prev_update_iso = parse_datetime_string(previous_datetime_str)

        if parsed_last_update_iso and parsed_prev_update_iso:
            last_update_dt = datetime.fromisoformat(parsed_last_update_iso)
            prev_update_dt = datetime.fromisoformat(parsed_prev_update_iso)
            update_interval_days = abs((last_update_dt - prev_update_dt).days)
        else:
            logging.getLogger(__name__).warning(
                f"Could not parse SERP previous update times for interval: {datetime_str}, {previous_datetime_str}"
            )

    return {"days_ago": days_ago, "update_interval_days": update_interval_days}


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
    
    return {
        "is_seasonal": is_seasonal,
        "peak_month": peak_month,
        "seasonality_factor": round(seasonality_factor, 2),
        "pattern_type": pattern_type
    }


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
    
    from core.discovery_defaults import DISCOVERY_DEFAULTS, TECHNICAL_TOPIC_INDICATORS
    
    difficulty_level = "easy"
    estimated_word_count = DISCOVERY_DEFAULTS["BASE_WORD_COUNT"]
    requires_video = False
    requires_expert = False
    production_time_hours = DISCOVERY_DEFAULTS["BASE_CONTENT_PRODUCTION_HOURS"]
    
    # Check SERP features
    serp_types = set(serp_info.get("serp_item_types", []))
    
    # Video requirement detection
    if "video" in serp_types or "short_videos" in serp_types:
        requires_video = True
        difficulty_level = "hard"
        production_time_hours += DISCOVERY_DEFAULTS["VIDEO_PRODUCTION_HOURS_ADDITION"]
    
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
    
    # Technical topic detection (based on keyword patterns)
    keyword_lower = keyword.lower()
    if any(indicator in keyword_lower for indicator in TECHNICAL_TOPIC_INDICATORS):
        requires_expert = True
        if difficulty_level == "easy":
            difficulty_level = "medium"
        estimated_word_count = max(estimated_word_count, DISCOVERY_DEFAULTS["EXPERT_CONTENT_WORD_COUNT"])
        production_time_hours = max(production_time_hours, DISCOVERY_DEFAULTS["EXPERT_CONTENT_HOURS"])
    
    # Adjust for keyword difficulty
    kd = keyword_props.get("keyword_difficulty", 0)
    if kd > 60 and difficulty_level != "expert":
        difficulty_level = "hard"
        production_time_hours = max(production_time_hours, DISCOVERY_DEFAULTS["EXPERT_CONTENT_HOURS"] + 2)
    
    # SERP feature crowding adjustment
    from core.discovery_defaults import ATTENTION_COMPETING_FEATURES
    crowding_count = len(serp_types.intersection(ATTENTION_COMPETING_FEATURES))
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

