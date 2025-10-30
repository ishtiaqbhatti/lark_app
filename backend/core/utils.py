# core/utils.py
import logging
import re
from typing import Optional, Union, Dict
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
    Parses a DataForSEO datetime string into a consistent ISO format string.
    
    Per API docs, format is: "yyyy-mm-dd hh-mm-ss +00:00"
    Example: "2019-11-15 12:57:46 +00:00"
    
    Returns ISO format string or None if parsing fails.
    """
    if not dt_str:
        return None
    
    if not isinstance(dt_str, str):
        logging.getLogger(__name__).warning(
            f"datetime value is not a string: {type(dt_str)}"
        )
        return None

    # API format is consistent: "yyyy-mm-dd hh-mm-ss +00:00"
    # We need to parse this exact format and convert to ISO
    try:
        # Remove timezone offset and parse
        cleaned_dt_str = dt_str.replace(" +00:00", "").strip()
        parsed_dt = datetime.strptime(cleaned_dt_str, "%Y-%m-%d %H:%M:%S")
        return parsed_dt.isoformat()
    except ValueError:
        # Fallback for edge cases (malformed data)
        logging.getLogger(__name__).warning(
            f"Could not parse datetime string with expected format: {dt_str}"
        )
        
        # Try alternate formats as fallback
        alternate_formats = [
            "%Y-%m-%dT%H:%M:%S",
            "%Y-%m-%d %H:%M:%S.%f",
            "%Y-%m-%d",
        ]
        
        cleaned_dt_str = dt_str.replace(" +00:00", "").strip()
        for fmt in alternate_formats:
            try:
                return datetime.strptime(cleaned_dt_str, fmt).isoformat()
            except ValueError:
                continue
        
        logging.getLogger(__name__).error(
            f"Failed to parse datetime string with any known format: {dt_str}. Returning None."
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
