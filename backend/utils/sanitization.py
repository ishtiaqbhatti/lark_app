"""
Input sanitization utilities to prevent XSS and injection attacks.
"""

import html
import re
from typing import List, Dict, Any, Union

def sanitize_string(value: str, max_length: int = 1000) -> str:
    """
    Sanitizes a string input by:
    1. Trimming whitespace
    2. Escaping HTML entities
    3. Removing control characters
    4. Enforcing max length
    """
    if not isinstance(value, str):
        return ""
    
    # Trim and limit length
    value = value.strip()[:max_length]
    
    # Escape HTML entities
    value = html.escape(value)
    
    # Remove control characters except newline and tab
    value = re.sub(r'[\x00-\x08\x0B\x0C\x0E-\x1F\x7F]', '', value)
    
    return value

def sanitize_keyword_list(keywords: List[str]) -> List[str]:
    """
    Sanitizes a list of keywords.
    """
    sanitized = []
    for kw in keywords:
        clean_kw = sanitize_string(kw, max_length=500)
        if clean_kw:  # Only add non-empty keywords
            sanitized.append(clean_kw)
    
    return sanitized

def sanitize_filter_value(value: Any) -> Any:
    """
    Sanitizes filter values based on type.
    """
    if isinstance(value, str):
        return sanitize_string(value)
    elif isinstance(value, list):
        return [sanitize_filter_value(v) for v in value]
    elif isinstance(value, (int, float, bool)):
        return value
    elif value is None:
        return None
    else:
        return str(value)  # Convert unknown types to string

def sanitize_filters(filters: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Sanitizes filter structures.
    """
    sanitized = []
    for f in filters:
        sanitized.append({
            "field": sanitize_string(f.get("field", ""), max_length=200),
            "operator": sanitize_string(f.get("operator", ""), max_length=20),
            "value": sanitize_filter_value(f.get("value"))
        })
    return sanitized
