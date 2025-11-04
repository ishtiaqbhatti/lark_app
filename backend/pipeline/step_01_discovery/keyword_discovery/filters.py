# pipeline/step_01_discovery/keyword_discovery/filters.py
import json
import logging
from typing import List, Any, Tuple, Dict, Optional
from core.discovery_defaults import VALID_FILTER_OPERATORS, FORBIDDEN_API_FILTER_FIELDS

logger = logging.getLogger(__name__)

# Use centralized configuration from discovery_defaults
# (No local redefinition needed - imported at top)


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
        
        if operator not in VALID_FILTER_OPERATORS:
            return False, f"Invalid operator '{operator}'. Valid operators: {', '.join(VALID_FILTER_OPERATORS)}"
        
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