
## Phase 5: Input Validation and Security (Issues #14, #17, #24, #25)

### Task 5.1: Add Prompt Injection Prevention
**Priority:** CRITICAL - Security
**File:** `agents/article_generator.py`

**Exact Changes:**
```python
# ADD NEW METHOD at top of SectionalArticleGenerator class (after __init__):
    def _sanitize_prompt_input(self, user_input: str, max_length: int = 5000) -> str:
        """
        Sanitizes user input before inserting into prompts to prevent injection attacks.
        """
        if not isinstance(user_input, str):
            return ""
        
        # Truncate to prevent excessive token usage
        sanitized = user_input[:max_length]
        
        # Remove or escape potential prompt injection patterns
        # Remove system-level instructions
        dangerous_patterns = [
            "ignore previous instructions",
            "ignore all previous",
            "disregard previous",
            "new instructions:",
            "system:",
            "assistant:",
            "[SYSTEM]",
            "[INST]",
        ]
        
        sanitized_lower = sanitized.lower()
        for pattern in dangerous_patterns:
            if pattern in sanitized_lower:
                self.logger.warning(f"Potential prompt injection detected: '{pattern}' in input")
                # Replace the pattern with safe text
                sanitized = sanitized.replace(pattern, "[filtered]")
                sanitized = sanitized.replace(pattern.upper(), "[filtered]")
                sanitized = sanitized.replace(pattern.title(), "[filtered]")
        
        return sanitized

# THEN UPDATE generate_section method:
# FIND (line 80-95):
    def generate_section(
        self,
        opportunity: Dict[str, Any],
        section_title: str,
        section_sub_points: List[str],
        previous_section_content: str,
    ) -> Tuple[Optional[str], float]:
        brief = opportunity.get("blueprint", {}).get("ai_content_brief", {})
        prompt = f"""
        You are an expert SEO content writer and subject matter expert. Your task is to write a single, detailed section for a blog post about "{opportunity["keyword"]}".

        **Current Section to Write:** "{section_title}"
        **Key Sub-points to cover in this section:** {", ".join(section_sub_points) if section_sub_points else "N/A"}
        **Content from the Previous Section (for transition and context):**
        ...{previous_section_content[-1000:]}...

# REPLACE WITH:
    def generate_section(
        self,
        opportunity: Dict[str, Any],
        section_title: str,
        section_sub_points: List[str],
        previous_section_content: str,
    ) -> Tuple[Optional[str], float]:
        brief = opportunity.get("blueprint", {}).get("ai_content_brief", {})
        
        # Sanitize all user-controlled inputs
        safe_keyword = self._sanitize_prompt_input(opportunity.get("keyword", ""), max_length=200)
        safe_section_title = self._sanitize_prompt_input(section_title, max_length=500)
        safe_sub_points = [self._sanitize_prompt_input(sp, max_length=200) for sp in (section_sub_points or [])]
        safe_previous_content = self._sanitize_prompt_input(previous_section_content[-1000:], max_length=1000)
        
        prompt = f"""
        You are an expert SEO content writer and subject matter expert. Your task is to write a single, detailed section for a blog post about "{safe_keyword}".

        **Current Section to Write:** "{safe_section_title}"
        **Key Sub-points to cover in this section:** {", ".join(safe_sub_points) if safe_sub_points else "N/A"}
        **Content from the Previous Section (for transition and context):**
        ...{safe_previous_content}...
```

---

### Task 5.2: Add API Route Input Validation
**Priority:** HIGH
**File:** `api/routers/opportunities.py`

**Exact Changes:**
```python
# FIND (line 95-120 in update_opportunity_content_endpoint):
@router.put("/opportunities/{opportunity_id}/content", response_model=Dict[str, str])
async def update_opportunity_content_endpoint(
    opportunity_id: int,
    payload: ContentUpdatePayload,
    db: DatabaseManager = Depends(get_db),
    orchestrator: WorkflowOrchestrator = Depends(get_orchestrator),  # Add this
):
    """Updates the main HTML content of an opportunity's ai_content blob with server-side sanitization."""
    logger.info(f"Received manual content update for opportunity {opportunity_id}")
    from datetime import datetime

    try:
        current_opp = db.get_opportunity_by_id(opportunity_id)
        if not current_opp:
            raise HTTPException(status_code=404, detail="Opportunity not found.")

# REPLACE WITH:
@router.put("/opportunities/{opportunity_id}/content", response_model=Dict[str, str])
async def update_opportunity_content_endpoint(
    opportunity_id: int,
    payload: ContentUpdatePayload,
    db: DatabaseManager = Depends(get_db),
    orchestrator: WorkflowOrchestrator = Depends(get_orchestrator),
):
    """Updates the main HTML content of an opportunity's ai_content blob with server-side sanitization."""
    logger.info(f"Received manual content update for opportunity {opportunity_id}")
    from datetime import datetime

    # Validate opportunity_id is positive integer
    if opportunity_id <= 0:
        raise HTTPException(status_code=400, detail="Invalid opportunity_id")
    
    # Validate payload size (prevent DoS via large payloads)
    if len(payload.article_body_html) > 5_000_000:  # 5MB limit
        raise HTTPException(
            status_code=413,
            detail="Content exceeds maximum size of 5MB"
        )

    try:
        current_opp = db.get_opportunity_by_id(opportunity_id)
        if not current_opp:
            raise HTTPException(status_code=404, detail="Opportunity not found.")
```

---

### Task 5.3: Add Logging Redaction for Sensitive Data
**Priority:** MEDIUM
**File:** Create new utility file `core/logging_utils.py`

**Exact Changes:**
```python
# CREATE NEW FILE: backend/core/logging_utils.py

import re
from typing import Any, Dict


def redact_sensitive_data(data: Any) -> Any:
    """
    Recursively redacts sensitive information from data structures before logging.
    """
    if isinstance(data, dict):
        redacted = {}
        for key, value in data.items():
            # Redact keys that might contain sensitive info
            if any(sensitive in key.lower() for sensitive in [
                'password', 'api_key', 'token', 'secret', 'credential',
                'authorization', 'auth', 'app_password'
            ]):
                redacted[key] = "***REDACTED***"
            else:
                redacted[key] = redact_sensitive_data(value)
        return redacted
    
    elif isinstance(data, list):
        return [redact_sensitive_data(item) for item in data]
    
    elif isinstance(data, str):
        # Redact API keys in strings (pattern: alphanumeric strings > 20 chars)
        if len(data) > 20 and re.match(r'^[a-zA-Z0-9_-]+$', data):
            return f"{data[:4]}...{data[-4:]}"
        return data
    
    else:
        return data


def safe_log_dict(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Returns a safe-to-log version of a dictionary with sensitive data redacted.
    """
    return redact_sensitive_data(data)
```

**Then update logging calls throughout:**

**File:** `api/routers/clients.py`

```python
# ADD IMPORT at top:
from backend.core.logging_utils import safe_log_dict

# FIND (line 37-40):
@router.get("/clients")
async def get_all_clients(db: DatabaseManager = Depends(get_db)):
    logger.info("Received request for /clients")
    clients = db.get_clients()
    logger.info(f"Found clients: {clients}")

# REPLACE WITH:
@router.get("/clients")
async def get_all_clients(db: DatabaseManager = Depends(get_db)):
    logger.info("Received request for /clients")
    clients = db.get_clients()
    logger.info(f"Found {len(clients)} clients")  # Don't log full client data
```

---

## Phase 6: Filter and Validation Fixes (Issues #48, #50, #51, #58, #59)

### Task 6.1: Enforce 8-Filter Maximum AFTER Conversion
**Priority:** HIGH
**File:** `external_apis/dataforseo_client_v2.py`

**Exact Changes:**
```python
# FIND (line 242-290, the _prioritize_and_limit_filters method):
    def _prioritize_and_limit_filters(self, filters: Optional[List[Any]]) -> List[Any]:
        """Enforces the 8-filter maximum rule by prioritizing essential filters."""
        if not filters:
            return []

        # Count actual filter conditions (excluding logical operators like "and", "or")
        condition_count = sum(1 for f in filters if isinstance(f, list))

        # If already within the limit, return as is.
        if condition_count <= 8:
            return filters

# REPLACE WITH:
    def _prioritize_and_limit_filters(self, filters: Optional[List[Any]]) -> List[Any]:
        """
        Enforces the 8-filter maximum rule by prioritizing essential filters.
        MUST be called AFTER _convert_filters_to_api_format.
        
        Per API docs: "you can add several filters at once (8 filters maximum)"
        """
        if not filters:
            return []

        # Count actual filter conditions (excluding logical operators like "and", "or")
        condition_count = sum(1 for f in filters if isinstance(f, list))

        # If already within the limit, return as is.
        if condition_count <= 8:
            return filters
        
        self.logger.warning(
            f"Filter list contains {condition_count} conditions, exceeding API maximum of 8. "
            "Applying prioritization to reduce to 8 filters."
        )
```

**Then update call order in get_keyword_ideas:**

```python
# FIND (line 440-445):
            sanitized_ideas_filters = self._prioritize_and_limit_filters(
                self._convert_filters_to_api_format(filters.get("ideas"))
            )

# This is already correct order: convert first, then limit
# But add comment to make it explicit:

# REPLACE WITH:
            # CRITICAL: Must convert to API format FIRST, then enforce limit
            # because conversion can expand filters (e.g., 'in' operator)
            converted_ideas_filters = self._convert_filters_to_api_format(filters.get("ideas"))
            sanitized_ideas_filters = self._prioritize_and_limit_filters(converted_ideas_filters)
```

---

### Task 6.2: Add Forbidden Filter Field Validation
**Priority:** MEDIUM
**File:** `pipeline/step_01_discovery/keyword_discovery/filters.py`

**Exact Changes:**
```python
# FIND (line 10-17, the sanitize_filters_for_api function):
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
```python
                logger.warning(
                    f"Forbidden field '{field_path}' detected in API filter. Removing it."
                )
                continue
        sanitized.append(item)
    return sanitized

# REPLACE WITH:
def sanitize_filters_for_api(filters: List[Any]) -> List[Any]:
    """
    Removes any filters attempting to use forbidden internal metrics or data sources.
    Per API docs: "note that you can not filter the results by `relevance`"
    """
    if not filters:
        return []
    
    sanitized = []
    removed_count = 0
    
    for item in filters:
        if isinstance(item, list) and len(item) >= 1 and isinstance(item[0], str):
            field_path = item[0].lower()
            
            # Check against forbidden fields
            if any(forbidden in field_path for forbidden in FORBIDDEN_API_FILTER_FIELDS):
                logger.warning(
                    f"Forbidden field '{field_path}' detected in API filter. Removing it."
                )
                removed_count += 1
                continue
        
        sanitized.append(item)
    
    # Clean up trailing logical operators if filters were removed
    if sanitized and isinstance(sanitized[-1], str) and sanitized[-1].lower() in ["and", "or"]:
        sanitized.pop()
    
    # Clean up leading logical operators
    if sanitized and isinstance(sanitized[0], str) and sanitized[0].lower() in ["and", "or"]:
        sanitized.pop(0)
    
    if removed_count > 0:
        logger.info(f"Removed {removed_count} forbidden filter(s) from API request")
    
    return sanitized
```

---

### Task 6.3: Add Filter Operator Type Validation
**Priority:** MEDIUM
**File:** `external_apis/dataforseo_client_v2.py`

**Exact Changes:**
```python
# ADD NEW METHOD after _validate_and_limit_order_by (around line 395):

    def _validate_filter_operator(self, field: str, operator: str, value: Any) -> bool:
        """
        Validates that the operator is compatible with the field type.
        
        Per API docs:
        - bool: only =, <>
        - num: <, <=, >, >=, =, <>, in, not_in
        - str: match, not_match, like, not_like, ilike, not_ilike, in, not_in, =, <>, regex, not_regex
        - array.str: has, has_not
        - array.num: has, has_not
        - time: <, >
        """
        # Mapping of field patterns to their types based on API documentation
        field_type_map = {
            "competition": "num",
            "competition_level": "str",
            "cpc": "num",
            "search_volume": "num",
            "keyword_difficulty": "num",
            "main_intent": "str",
            "foreign_intent": "array.str",
            "serp_item_types": "array.str",
            "categories": "array.num",
            "is_another_language": "bool",
            "is_normalized": "bool",
            "_time": "time",  # Any field ending in _time
            "year": "num",
            "month": "num",
            "backlinks": "num",
            "dofollow": "num",
            "rank": "num",
            "depth": "num",
        }
        
        # Determine field type
        field_type = None
        field_lower = field.lower()
        for pattern, ftype in field_type_map.items():
            if pattern in field_lower:
                field_type = ftype
                break
        
        if field_type is None:
            # Default to string if unknown
            field_type = "str"
        
        # Valid operators per type
        valid_operators = {
            "bool": {"=", "<>"},
            "num": {"<", "<=", ">", ">=", "=", "<>", "in", "not_in"},
            "str": {"match", "not_match", "like", "not_like", "ilike", "not_ilike", 
                   "in", "not_in", "=", "<>", "regex", "not_regex"},
            "array.str": {"has", "has_not"},
            "array.num": {"has", "has_not"},
            "time": {"<", ">"},
        }
        
        allowed = valid_operators.get(field_type, valid_operators["str"])
        
        if operator not in allowed:
            self.logger.warning(
                f"Invalid operator '{operator}' for field '{field}' (type: {field_type}). "
                f"Allowed operators: {allowed}"
            )
            return False
        
        return True

# THEN UPDATE _convert_filters_to_api_format to use validation:
# FIND (updated version from Task 2.7, around line 365-375):
            if not all(k in f for k in ["field", "operator", "value"]):
                self.logger.warning(f"Filter missing required keys: {f}")
                continue
            
            # Per API docs: 'in' and 'not_in' operators work with array values directly
            # DO NOT expand into multiple 'or' conditions
            api_filters.append([f["field"], f["operator"], f["value"]])

# REPLACE WITH:
            if not all(k in f for k in ["field", "operator", "value"]):
                self.logger.warning(f"Filter missing required keys: {f}")
                continue
            
            # Validate operator is compatible with field type
            if not self._validate_filter_operator(f["field"], f["operator"], f["value"]):
                self.logger.warning(f"Skipping invalid filter: {f}")
                continue
            
            # Per API docs: 'in' and 'not_in' operators work with array values directly
            # DO NOT expand into multiple 'or' conditions
            api_filters.append([f["field"], f["operator"], f["value"]])
```

---

### Task 6.4: Add Regex Length Validation
**Priority:** MEDIUM
**File:** Already done in Task 2.4 - Verify it's complete

---

### Task 6.5: Add Pagination Limit Validation
**Priority:** MEDIUM
**File:** `api/routers/opportunities.py`

**Exact Changes:**
```python
# FIND (line 35-50 in get_all_opportunities_summary_endpoint):
async def get_all_opportunities_summary_endpoint(
    client_id: str,
    status: Optional[str] = None,
    keyword: Optional[str] = None,
    page: int = 1,
    limit: int = 20,
    sort_by: str = "date_added",
    sort_direction: str = "desc",
    opportunities_service: OpportunitiesService = Depends(get_opportunities_service),
    orchestrator: WorkflowOrchestrator = Depends(get_orchestrator),
):
    """Endpoint for fetching a paginated summary of opportunities for the main table view."""
    if client_id != orchestrator.client_id:
        raise HTTPException(
            status_code=403,
            detail="You do not have permission to access this client's resources.",
        )
    params = {

# REPLACE WITH:
async def get_all_opportunities_summary_endpoint(
    client_id: str,
    status: Optional[str] = None,
    keyword: Optional[str] = None,
    page: int = 1,
    limit: int = 20,
    sort_by: str = "date_added",
    sort_direction: str = "desc",
    opportunities_service: OpportunitiesService = Depends(get_opportunities_service),
    orchestrator: WorkflowOrchestrator = Depends(get_orchestrator),
):
    """Endpoint for fetching a paginated summary of opportunities for the main table view."""
    if client_id != orchestrator.client_id:
        raise HTTPException(
            status_code=403,
            detail="You do not have permission to access this client's resources.",
        )
    
    # Validate pagination parameters
    if page < 1:
        raise HTTPException(status_code=400, detail="page must be >= 1")
    
    if limit < 1 or limit > 100:
        raise HTTPException(status_code=400, detail="limit must be between 1 and 100")
    
    # Validate sort_by against whitelist
    allowed_sort_fields = {
        "strategic_score", "date_added", "keyword", "status",
        "search_volume", "keyword_difficulty", "cpc"
    }
    if sort_by not in allowed_sort_fields:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid sort_by field. Allowed: {allowed_sort_fields}"
        )
    
    # Validate sort_direction
    if sort_direction not in ["asc", "desc"]:
        raise HTTPException(status_code=400, detail="sort_direction must be 'asc' or 'desc'")
    
    params = {
```

---

## Phase 7: Data Type and Structure Fixes (Issues #12, #21, #22, #68, #75, #78)

### Task 7.1: Fix Search Volume Trend Type Handling
**Priority:** MEDIUM
**File:** `data_mappers/dataforseo_mapper.py`

**Exact Changes:**
```python
# FIND in sanitize_keyword_data_item method (around line 130-150):
            # Ensure individual monthly_searches items are sanitized for type consistency
            if isinstance(sanitized_item["keyword_info"].get("monthly_searches"), list):
                for month_data in sanitized_item["keyword_info"]["monthly_searches"]:
                    if isinstance(month_data, dict):
                        month_data["year"] = int(month_data.get("year") or 0)
                        month_data["month"] = int(month_data.get("month") or 0)
                        month_data["search_volume"] = int(
                            month_data.get("search_volume") or 0
                        )

# ADD AFTER THIS BLOCK:
            # Sanitize search_volume_trend - per API docs, these are integers (percentage changes)
            if isinstance(sanitized_item["keyword_info"].get("search_volume_trend"), dict):
                trend = sanitized_item["keyword_info"]["search_volume_trend"]
                trend["monthly"] = int(trend.get("monthly") or 0)
                trend["quarterly"] = int(trend.get("quarterly") or 0)
                trend["yearly"] = int(trend.get("yearly") or 0)
```

---

### Task 7.2: Fix DateTime Parsing to Match API Format Exactly
**Priority:** MEDIUM
**File:** `core/utils.py`

**Exact Changes:**
```python
# FIND (line 70-100, the parse_datetime_string function):
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

# REPLACE WITH:
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
```

---

### Task 7.3: Add Type Hints Using Pydantic Models
**Priority:** MEDIUM
**File:** Create new file `data_access/api_models.py`

**Exact Changes:**
```python
# CREATE NEW FILE: backend/data_access/api_models.py

from pydantic import BaseModel, Field, validator
from typing import Optional, List, Dict, Any
from datetime import datetime


class KeywordInfoModel(BaseModel):
    """Strongly typed model for keyword_info from DataForSEO API."""
    se_type: str
    last_updated_time: str
    competition: float = Field(ge=0.0, le=1.0)
    competition_level: Optional[str] = Field(None, pattern="^(LOW|MEDIUM|HIGH)$")
    cpc: float = Field(ge=0.0)
    search_volume: int = Field(ge=0)
    low_top_of_page_bid: float = Field(ge=0.0)
    high_top_of_page_bid: float = Field(ge=0.0)
    categories: List[int] = []
    monthly_searches: List[Dict[str, int]] = []
    search_volume_trend: Dict[str, int] = {}
    
    @validator('competition', 'cpc', 'low_top_of_page_bid', 'high_top_of_page_bid', pre=True)
    def convert_to_float(cls, v):
        """Ensure numeric fields are floats."""
        if v is None:
            return 0.0
        return float(v)
    
    @validator('search_volume', pre=True)
    def convert_to_int(cls, v):
        """Ensure search volume is int."""
        if v is None:
            return 0
        return int(v)


class KeywordPropertiesModel(BaseModel):
    """Strongly typed model for keyword_properties from DataForSEO API."""
    se_type: str
    core_keyword: Optional[str] = None
    synonym_clustering_algorithm: Optional[str] = None
    keyword_difficulty: int = Field(ge=0, le=100)
    detected_language: str
    is_another_language: bool
    
    @validator('keyword_difficulty', pre=True)
    def convert_to_int(cls, v):
        if v is None:
            return 0
        return int(v)


class SerpInfoModel(BaseModel):
    """Strongly typed model for serp_info from DataForSEO API."""
    se_type: str
    check_url: Optional[str] = None
    serp_item_types: List[str] = []
    se_results_count: int = 0  # CRITICAL: Always int after sanitization
    last_updated_time: Optional[str] = None
    previous_updated_time: Optional[str] = None
    
    @validator('se_results_count', pre=True)
    def convert_se_results_count(cls, v):
        """
        CRITICAL FIX: se_results_count is STRING in Keyword Ideas/Suggestions API response.
        Per API docs, this field type varies by endpoint.
        """
        if v is None:
            return 0
        if isinstance(v, str):
            try:
                return int(v)
            except (ValueError, TypeError):
                return 0
        return int(v)


class SearchIntentInfoModel(BaseModel):
    """Strongly typed model for search_intent_info from DataForSEO API."""
    se_type: str
    main_intent: str = Field(pattern="^(informational|navigational|commercial|transactional)$")
    foreign_intent: Optional[List[str]] = None  # Can be null per API docs
    last_updated_time: Optional[str] = None
    
    @validator('foreign_intent', pre=True)
    def handle_null_foreign_intent(cls, v):
        """Per API docs: foreign_intent is null when there are no foreign intents."""
        if v is None:
            return []
        if isinstance(v, list):
            return v
        return []


class AvgBacklinksInfoModel(BaseModel):
    """Strongly typed model for avg_backlinks_info from DataForSEO API."""
    se_type: str
    backlinks: float = 0.0
    dofollow: float = 0.0
    referring_pages: float = 0.0
    referring_domains: float = 0.0
    referring_main_domains: float = 0.0
    rank: float = 0.0
    main_domain_rank: float = 0.0
    last_updated_time: Optional[str] = None
    
    @validator('*', pre=True)
    def convert_to_float(cls, v):
        """Ensure all numeric fields are floats."""
        if v is None:
            return 0.0
        return float(v)
```

**Note:** These models can be gradually integrated into the codebase to replace Dict[str, Any] type hints.

---

### Task 7.4: Fix Division by Zero in Scoring Components
**Priority:** MEDIUM
**File:** `pipeline/step_03_prioritization/scoring_components/traffic_potential.py`

**Exact Changes:**
```python
# FIND (line 5-15, the _normalize_value helper):
def _normalize_value(value: float, max_value: float, invert: bool = False) -> float:
    """Helper to normalize a value to a 0-100 scale."""
    if value is None or max_value is None or max_value == 0:
        return 0.0

    normalized = min(float(value) / float(max_value), 1.0)

    if invert:
        return (1 - normalized) * 100
    return normalized * 100

# REPLACE WITH:
def _normalize_value(value: float, max_value: float, invert: bool = False) -> float:
    """Helper to normalize a value to a 0-100 scale with safe division."""
    if value is None or max_value is None:
        return 0.0
    
    # Prevent division by zero
    if max_value == 0:
        return 0.0
    
    # Ensure we're working with numbers
    try:
        value_float = float(value)
        max_float = float(max_value)
    except (ValueError, TypeError):
        return 0.0

    normalized = min(value_float / max_float, 1.0)

    if invert:
        return (1 - normalized) * 100
    return normalized * 100
```

**Repeat this fix in ALL scoring component files:**
- `ease_of_ranking.py`
- `commercial_intent.py`
- `competitor_weakness.py`
- `competitor_performance.py`

Use the exact same replacement for the `_normalize_value` function in each file.

---

### Task 7.5: Fix Type Confusion in Trend Analysis
**Priority:** MEDIUM
**File:** `pipeline/step_01_discovery/disqualification_rules.py`

**Exact Changes:**
```python
# FIND (line 173-200, the trend analysis section):
    trends = keyword_info.get("search_volume_trend", {})
    try:
        yearly_trend = trends.get("yearly")
        quarterly_trend = trends.get("quarterly")

        yearly_threshold = client_cfg.get("yearly_trend_decline_threshold", -25)
        quarterly_threshold = client_cfg.get("quarterly_trend_decline_threshold", 0)

        yearly_check = utils.safe_compare(yearly_trend, yearly_threshold, "lt")
        quarterly_check = utils.safe_compare(quarterly_trend, quarterly_threshold, "lt")

        if yearly_check and quarterly_check:
            return (
                True,
                f"Rule 6: Consistently declining trend. Yearly trend: {yearly_trend}% (below {yearly_threshold}% threshold), Quarterly trend: {quarterly_trend}% (below {quarterly_threshold}% threshold). Consider manual review for seasonality.",
                False,
            )
    except TypeError:
        logging.getLogger(__name__).error(
            f"TypeError during trend analysis for keyword '{keyword}'. "
            f"trends.get('yearly') value: {trends.get('yearly')}, type: {type(trends.get('yearly'))}. "
            f"trends.get('quarterly') value: {trends.get('quarterly')}, type: {type(trends.get('quarterly'))}."
        )
        return (
            True,
            "Rule 6: Failed to process trend data due to invalid format.",
            False,
        )

# REPLACE WITH:
    trends = keyword_info.get("search_volume_trend", {})
    if not isinstance(trends, dict):
        logging.getLogger(__name__).warning(
            f"search_volume_trend is not a dict for keyword '{keyword}': {type(trends)}"
        )
        trends = {}
    
    # Per API docs: trend values are integers (percentage change)
    yearly_trend = trends.get("yearly")
    quarterly_trend = trends.get("quarterly")
    
    # Validate and convert to int
    try:
        if yearly_trend is not None:
            yearly_trend = int(yearly_trend)
        if quarterly_trend is not None:
            quarterly_trend = int(quarterly_trend)
    except (ValueError, TypeError) as e:
        logging.getLogger(__name__).error(
            f"Failed to convert trend data to int for keyword '{keyword}'. "
            f"yearly: {trends.get('yearly')} (type: {type(trends.get('yearly'))}), "
            f"quarterly: {trends.get('quarterly')} (type: {type(trends.get('quarterly'))}). "
            f"Error: {e}"
        )
        return (
            True,
            "Rule 6: Invalid trend data format.",
            False,
        )

    yearly_threshold = client_cfg.get("yearly_trend_decline_threshold", -25)
    quarterly_threshold = client_cfg.get("quarterly_trend_decline_threshold", 0)

    yearly_check = utils.safe_compare(yearly_trend, yearly_threshold, "lt")
    quarterly_check = utils.safe_compare(quarterly_trend, quarterly_threshold, "lt")

    if yearly_check and quarterly_check:
        return (
            True,
            f"Rule 6: Consistently declining trend. Yearly trend: {yearly_trend}% (below {yearly_threshold}% threshold), Quarterly trend: {quarterly_trend}% (below {quarterly_threshold}% threshold). Consider manual review for seasonality.",
            False,
        )
```

---

### Task 7.6: Add Status and Intent Enums
**Priority:** LOW
**File:** Create new file `core/enums.py`

**Exact Changes:**
```python
# CREATE NEW FILE: backend/core/enums.py

from enum import Enum


class OpportunityStatus(str, Enum):
    """Valid opportunity status values."""
    PENDING = "pending"
    RUNNING = "running"
    IN_PROGRESS = "in_progress"
    VALIDATED = "validated"
    ANALYZED = "analyzed"
    PAUSED_FOR_APPROVAL = "paused_for_approval"
    GENERATED = "generated"
    PUBLISHED = "published"
    FAILED = "failed"
    REJECTED = "rejected"
    REJECTED_BY_USER = "rejected_by_user"
    REFRESH_STARTED = "refresh_started"


class SearchIntent(str, Enum):
    """Valid search intent values per DataForSEO API."""
    INFORMATIONAL = "informational"
    NAVIGATIONAL = "navigational"
    COMMERCIAL = "commercial"
    TRANSACTIONAL = "transactional"


class CompetitionLevel(str, Enum):
    """Valid competition level values per DataForSEO API."""
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"


class JobStatus(str, Enum):
    """Valid job status values."""
    PENDING = "pending"
    RUNNING = "running"
    PAUSED = "paused"
    COMPLETED = "completed"
    FAILED = "failed"


class SocialMediaStatus(str, Enum):
    """Valid social media post status values."""
    DRAFT = "draft"
    APPROVED = "approved"
    REJECTED = "rejected"
    SCHEDULED = "scheduled"
    PUBLISHED = "published"
```

**Then update code to use enums:**

**File:** `api/routers/orchestrator.py`

```python
# ADD IMPORT at top:
from backend.core.enums import SocialMediaStatus

# FIND (line 320-335):
    """Endpoint to update the status of social media posts (e.g., 'approved', 'rejected')."""
    try:
        opportunity = db.get_opportunity_by_id(opportunity_id)
        if not opportunity:
            raise HTTPException(status_code=404, detail="Opportunity not found.")

        if opportunity["client_id"] != orchestrator.client_id:
            raise HTTPException(
                status_code=403,
                detail="You do not have permission to access this opportunity.",
            )

        valid_statuses = ["draft", "approved", "rejected", "scheduled", "published"]
        if request.new_status not in valid_statuses:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid status: {request.new_status}. Must be one of {valid_statuses}.",
            )

# REPLACE WITH:
    """Endpoint to update the status of social media posts (e.g., 'approved', 'rejected')."""
    try:
        opportunity = db.get_opportunity_by_id(opportunity_id)
        if not opportunity:
            raise HTTPException(status_code=404, detail="Opportunity not found.")

        if opportunity["client_id"] != orchestrator.client_id:
            raise HTTPException(
                status_code=403,
                detail="You do not have permission to access this opportunity.",
            )

        # Use enum for validation
        try:
            validated_status = SocialMediaStatus(request.new_status)
        except ValueError:
            valid_statuses = [s.value for s in SocialMediaStatus]
            raise HTTPException(
                status_code=400,
                detail=f"Invalid status: {request.new_status}. Must be one of {valid_statuses}.",
            )
```

---

## Phase 8: Configuration and Settings Fixes (Issues #9, #18, #32)

### Task 8.1: Add Safe Configuration Parsing with Try-Catch
**Priority:** HIGH
**File:** `app_config/manager.py`

**Exact Changes:**
```python
# FIND (line 90-145, in _load_and_validate_global method):
        # Load all settings from settings.ini
        for section in self.config_parser.sections():
            for key, value in self.config_parser.items(section):
                try:
                    target_type = self._setting_types.get(key)
                    if target_type is bool:
                        settings[key] = self.config_parser.getboolean(section, key)
                    elif target_type is int:
                        settings[key] = self.config_parser.getint(section, key)
                    elif target_type is float:
                        settings[key] = self.config_parser.getfloat(section, key)
                    elif target_type is list:
                        raw_values = self._get_list_from_config(section, key)
                        if key == "serp_feature_filters":
                            parsed_filters = []
                            for f_str in raw_values:
                                if f_str.startswith("no_"):
                                    parsed_filters.append(
                                        {"type": "has_not", "feature": f_str[3:]}
                                    )
                                elif f_str.startswith("has_"):
                                    parsed_filters.append(
                                        {"type": "has", "feature": f_str[4:]}
                                    )
                            settings[key] = parsed_filters
                        else:
                            settings[key] = raw_values
                    else:  # Default to string if no type is mapped
                        settings[key] = value
                except Exception as e:
                    self.logger.critical(
                        f"FATAL CONFIG ERROR: Could not parse key [{section}]{key} with value '{value}' to expected type: {e}"
                    )
                    raise ValueError(
                        f"Configuration key parsing failed for [{section}]{key}. Value: '{value}'."
                    )

# REPLACE WITH:
        # Load all settings from settings.ini with enhanced error handling
        parsing_errors = []
        
        for section in self.config_parser.sections():
            for key, value in self.config_parser.items(section):
                try:
                    target_type = self._setting_types.get(key)
                    
                    if target_type is bool:
                        try:
                            settings[key] = self.config_parser.getboolean(section, key)
                        except ValueError as e:
                            self.logger.error(
                                f"Failed to parse boolean for [{section}]{key}='{value}'. Using False. Error: {e}"
                            )
                            settings[key] = False
                            parsing_errors.append(f"{section}.{key}")
                    
                    elif target_type is int:
                        try:
                            settings[key] = self.config_parser.getint(section, key)
                        except ValueError as e:
                            self.logger.error(
                                f"Failed to parse integer for [{section}]{key}='{value}'. Using 0. Error: {e}"
                            )
                            settings[key] = 0
                            parsing_errors.append(f"{section}.{key}")
                    
                    elif target_type is float:
                        try:
                            settings[key] = self.config_parser.getfloat(section, key)
                        except ValueError as e:
                            self.logger.error(
                                f"Failed to parse float for [{section}]{key}='{value}'. Using 0.0. Error: {e}"
                            )
                            settings[key] = 0.0
                            parsing_errors.append(f"{section}.{key}")
                    ```python
                    
                    elif target_type is list:
                        try:
                            raw_values = self._get_list_from_config(section, key)
                            if key == "serp_feature_filters":
                                parsed_filters = []
                                for f_str in raw_values:
                                    if f_str.startswith("no_"):
                                        parsed_filters.append(
                                            {"type": "has_not", "feature": f_str[3:]}
                                        )
                                    elif f_str.startswith("has_"):
                                        parsed_filters.append(
                                            {"type": "has", "feature": f_str[4:]}
                                        )
                                settings[key] = parsed_filters
                            else:
                                settings[key] = raw_values
                        except Exception as e:
                            self.logger.error(
                                f"Failed to parse list for [{section}]{key}='{value}'. Using empty list. Error: {e}"
                            )
                            settings[key] = []
                            parsing_errors.append(f"{section}.{key}")
                    
                    else:  # Default to string if no type is mapped
                        settings[key] = value
                
                except Exception as e:
                    self.logger.error(
                        f"Unexpected error parsing [{section}]{key}='{value}': {e}. Skipping this setting."
                    )
                    parsing_errors.append(f"{section}.{key}")
        
        if parsing_errors:
            self.logger.warning(
                f"Configuration parsing completed with {len(parsing_errors)} errors. "
                f"Problematic keys: {', '.join(parsing_errors[:10])}"
            )

        self.logger.info("Global settings loaded.")
        return settings
```

---

## Phase 9: API Response Validation and Error Recovery (Issues #65, #66, #69, #72)

### Task 9.1: Add Null Checks for Optional API Fields
**Priority:** HIGH
**File:** `pipeline/step_03_prioritization/scoring_components/traffic_potential.py`

**Exact Changes:**
```python
# FIND (line 35-55):
def calculate_traffic_potential_score(
    data: Dict[str, Any], config: Dict[str, Any]
) -> Tuple[float, Dict[str, Any]]:
    """
    Calculates a blended score based on both commercial traffic value and raw audience size.
    """
    if not isinstance(data, dict):
        return 0, {"message": "Invalid data format for scoring."}

    keyword_info = (
        data.get("keyword_info") if isinstance(data.get("keyword_info"), dict) else {}
    )
    sv = keyword_info.get("search_volume", 0) or 0
    cpc = keyword_info.get("cpc", 0.0) or 0.0

# REPLACE WITH:
def calculate_traffic_potential_score(
    data: Dict[str, Any], config: Dict[str, Any]
) -> Tuple[float, Dict[str, Any]]:
    """
    Calculates a blended score based on both commercial traffic value and raw audience size.
    Handles null values from API responses gracefully.
    """
    if not isinstance(data, dict):
        return 0, {"message": "Invalid data format for scoring."}

    keyword_info = data.get("keyword_info")
    if not isinstance(keyword_info, dict):
        return 0, {"message": "Missing keyword_info data for scoring."}
    
    # Per API docs: search_volume and cpc can be null in some cases
    sv = keyword_info.get("search_volume")
    if sv is None:
        sv = 0
    else:
        try:
            sv = int(sv)
        except (ValueError, TypeError):
            sv = 0
    
    cpc = keyword_info.get("cpc")
    if cpc is None:
        cpc = 0.0
    else:
        try:
            cpc = float(cpc)
        except (ValueError, TypeError):
            cpc = 0.0
```

---

### Task 9.2: Add Validation for Clickstream Fields
**Priority:** MEDIUM
**File:** Create validation helper in `data_mappers/dataforseo_mapper.py`

**Exact Changes:**
```python
# ADD NEW METHOD at the end of DataForSEOMapper class (around line 280):

    @staticmethod
    def validate_clickstream_data_available(item: Dict[str, Any]) -> bool:
        """
        Validates that clickstream data fields are present in the response.
        
        Per API docs: These fields are null unless include_clickstream_data=true:
        - clickstream_keyword_info
        - keyword_info_normalized_with_clickstream
        - keyword_info_normalized_with_bing
        """
        has_clickstream = (
            item.get("clickstream_keyword_info") is not None or
            item.get("keyword_info_normalized_with_clickstream") is not None or
            item.get("keyword_info_normalized_with_bing") is not None
        )
        
        if not has_clickstream:
            logging.getLogger(__name__).debug(
                f"Clickstream data not available for keyword '{item.get('keyword')}'. "
                "This is expected if include_clickstream_data was not set to true."
            )
        
        return has_clickstream
```

**Then add checks where clickstream data is used:**

**File:** `pipeline/step_03_prioritization/scoring_components/traffic_potential.py`

```python
# FIND (after imports, add):
from backend.data_mappers.dataforseo_mapper import DataForSEOMapper

# FIND in calculate_traffic_potential_score (around line 50):
    # 1. Calculate Traffic Value Score
    traffic_value = sv * cpc

# ADD BEFORE THIS:
    # Warn if using basic search volume without clickstream normalization
    if not DataForSEOMapper.validate_clickstream_data_available(data):
        logging.getLogger(__name__).debug(
            f"Scoring keyword without clickstream data normalization. "
            "Consider enabling include_clickstream_data for more accurate metrics."
        )
```

---

### Task 9.3: Add SERP Item Types Validation
**Priority:** LOW
**File:** `data_mappers/dataforseo_mapper.py`

**Exact Changes:**
```python
# ADD NEW CONSTANT at top of file (after imports):
# Exhaustive list of valid SERP item types per DataForSEO API documentation
VALID_SERP_ITEM_TYPES = {
    "answer_box", "app", "carousel", "multi_carousel", "featured_snippet",
    "google_flights", "google_reviews", "third_party_reviews", "google_posts",
    "images", "jobs", "knowledge_graph", "local_pack", "hotels_pack", "map",
    "organic", "paid", "people_also_ask", "related_searches", "people_also_search",
    "shopping", "top_stories", "twitter", "video", "events", "mention_carousel",
    "recipes", "top_sights", "scholarly_articles", "popular_products", "podcasts",
    "questions_and_answers", "find_results_on", "stocks_box", "visual_stories",
    "commercial_units", "local_services", "google_hotels", "math_solver",
    "currency_box", "product_considerations", "found_on_web", "short_videos",
    "refine_products", "explore_brands", "perspectives", "discussions_and_forums",
    "compare_sites", "courses", "ai_overview"
}

# THEN ADD NEW METHOD in DataForSEOMapper class:
    @staticmethod
    def validate_serp_item_types(serp_item_types: List[str]) -> List[str]:
        """
        Validates SERP item types against the official API list.
        Returns only valid types and logs warnings for unknown types.
        """
        if not isinstance(serp_item_types, list):
            logger.warning(f"serp_item_types is not a list: {type(serp_item_types)}")
            return []
        
        validated = []
        invalid_types = []
        
        for item_type in serp_item_types:
            if not isinstance(item_type, str):
                logger.warning(f"SERP item type is not a string: {type(item_type)}")
                continue
            
            if item_type in VALID_SERP_ITEM_TYPES:
                validated.append(item_type)
            else:
                invalid_types.append(item_type)
        
        if invalid_types:
            logger.warning(
                f"Unknown SERP item types detected (API may have been updated): {invalid_types}"
            )
        
        return validated

# THEN UPDATE sanitize_keyword_data_item to use validation:
# FIND (in sanitize_keyword_data_item, around line 165):
        # Sanitize serp_info (crucial for se_results_count string/int issue)
        if isinstance(sanitized_item.get("serp_info"), dict):
            sanitized_item["serp_info"] = DataForSEOMapper._sanitize_serp_info(
                sanitized_item["serp_info"]
            )
            sanitized_item["serp_info"]["serp_item_types"] = (
                sanitized_item["serp_info"].get("serp_item_types") or []
            )

# REPLACE WITH:
        # Sanitize serp_info (crucial for se_results_count string/int issue)
        if isinstance(sanitized_item.get("serp_info"), dict):
            sanitized_item["serp_info"] = DataForSEOMapper._sanitize_serp_info(
                sanitized_item["serp_info"]
            )
            # Validate SERP item types against official list
            raw_serp_types = sanitized_item["serp_info"].get("serp_item_types") or []
            sanitized_item["serp_info"]["serp_item_types"] = DataForSEOMapper.validate_serp_item_types(raw_serp_types)
```

---

### Task 9.4: Add Configuration Validation on Startup
**Priority:** MEDIUM
**File:** `app_config/manager.py`

**Exact Changes:**
```python
# ADD NEW METHOD after _load_and_validate_global (around line 155):

    def validate_configuration_integrity(self) -> List[str]:
        """
        Validates configuration for common issues and inconsistencies.
        Returns list of validation warnings.
        """
        warnings = []
        
        # Validate weight totals
        weight_keys = [
            "ease_of_ranking_weight",
            "traffic_potential_weight",
            "commercial_intent_weight",
            "serp_features_weight",
            "growth_trend_weight",
            "serp_freshness_weight",
            "serp_volatility_weight",
            "competitor_weakness_weight",
            "competitor_performance_weight",
        ]
        
        total_weight = sum(self._global_settings.get(k, 0) for k in weight_keys)
        if total_weight == 0:
            warnings.append("CRITICAL: All scoring weights are 0. Scoring will not work.")
        elif total_weight != 100:
            warnings.append(
                f"WARNING: Scoring weights sum to {total_weight}, not 100. "
                "This is allowed but may indicate misconfiguration."
            )
        
        # Validate threshold ranges
        if self._global_settings.get("min_search_volume", 0) > self._global_settings.get("max_sv_for_scoring", 100000):
            warnings.append(
                "WARNING: min_search_volume is greater than max_sv_for_scoring. "
                "This may cause unexpected scoring behavior."
            )
        
        # Validate API keys are present
        required_keys = ["dataforseo_login", "dataforseo_password", "openai_api_key"]
        for key in required_keys:
            if not self._global_settings.get(key):
                warnings.append(f"CRITICAL: Required API credential '{key}' is not set.")
        
        # Validate filter limit settings
        max_filters = 8  # Per API docs
        # This is informational only
        
        # Validate discovery modes
        discovery_strategies = self._global_settings.get("discovery_strategies", [])
        if not discovery_strategies:
            warnings.append("WARNING: No discovery_strategies configured.")
        
        # Validate depth setting for related keywords
        related_depth = self._global_settings.get("discovery_related_depth", 1)
        if related_depth < 0 or related_depth > 4:
            warnings.append(
                f"WARNING: discovery_related_depth={related_depth} is outside valid range [0-4]. "
                "API will reject requests."
            )
        
        return warnings

# THEN CALL THIS IN __init__:
# FIND (line 65-70):
        self._configure_logging()
        self._global_settings = self._load_and_validate_global()

# REPLACE WITH:
        self._configure_logging()
        self._global_settings = self._load_and_validate_global()
        
        # Validate configuration integrity
        config_warnings = self.validate_configuration_integrity()
        if config_warnings:
            self.logger.warning(
                f"Configuration validation found {len(config_warnings)} issue(s):"
            )
            for warning in config_warnings:
                self.logger.warning(f"  - {warning}")
```

---

## Phase 10: Business Logic Fixes (Issues #36-40, #64, #70, #71, #77)

### Task 10.1: Fix Pagination Logic with total_count
**Priority:** HIGH
**File:** `external_apis/dataforseo_client_v2.py`

**Exact Changes:**
```python
# FIND (line 395-425 in post_with_paging method):
            if response and response.get("tasks"):
                for task in response["tasks"]:
                    task_url = task.get("data", {}).get("url")

                    # Explicit Failure Criteria Check: Task failed OR result is malformed/empty
                    if (
                        task.get("status_code") != 20000
                        or not task.get("result")
                        or not task["result"][0].get("items")
                    ):

            items_count = 0
            offset_token = None
            if task_result and isinstance(task_result, list) and len(task_result) > 0:
                offset_token = task_result[0].get("offset_token")
                for result_item in task_result:
                    # Capture items from the main list
                    items = result_item.get("items")
                    if items:
                        items_count += len(items)
                        all_items.extend(items)

            if not paginated or page_count >= max_pages or items_count == 0:
                break

# REPLACE WITH:
            items_count = 0
            offset_token = None
            total_count = None
            current_offset = 0
            
            if task_result and isinstance(task_result, list) and len(task_result) > 0:
                first_result = task_result[0]
                offset_token = first_result.get("offset_token")
                total_count = first_result.get("total_count")
                current_offset = first_result.get("offset", 0)
                
                for result_item in task_result:
                    # Handle different response structures per endpoint (from Task 2.1)
                    if endpoint == self.LABS_RELATED_KEYWORDS:
                        # [Related Keywords extraction logic from Task 2.1]
                        items = result_item.get("items", [])
                        for item in items:
                            keyword_data = item.get("keyword_data")
                            if keyword_data:
                                keyword_data["depth"] = item.get("depth", 0)
                                keyword_data["related_keywords"] = item.get("related_keywords", [])
                                keyword_data["discovery_source"] = "related_keywords"
                                all_items.append(DataForSEOMapper.sanitize_keyword_data_item(keyword_data))
                                items_count += 1
                        
                        seed_keyword_data = result_item.get("seed_keyword_data")
                        if isinstance(seed_keyword_data, list):
                            for seed_item in seed_keyword_data:
                                if isinstance(seed_item, dict) and seed_item.get("keyword"):
                                    seed_item["discovery_source"] = "related_keywords_seed"
                                    all_items.append(DataForSEOMapper.sanitize_keyword_data_item(seed_item))
                        elif isinstance(seed_keyword_data, dict) and seed_keyword_data.get("keyword"):
                            seed_keyword_data["discovery_source"] = "related_keywords_seed"
                            all_items.append(DataForSEOMapper.sanitize_keyword_data_item(seed_keyword_data))
                    
                    elif endpoint == self.LABS_KEYWORD_SUGGESTIONS:
                        items = result_item.get("items", [])
                        if items:
                            items_count += len(items)
                            for item in items:
                                item["discovery_source"] = "keyword_suggestions"
                                all_items.append(DataForSEOMapper.sanitize_keyword_data_item(item))
                        
                        seed_data = result_item.get("seed_keyword_data")
                        if isinstance(seed_data, dict) and seed_data.get("keyword"):
                            seed_data["discovery_source"] = "keyword_suggestions_seed"
                            all_items.append(DataForSEOMapper.sanitize_keyword_data_item(seed_data))
                    
                    else:
                        # Keyword Ideas and other endpoints
                        items = result_item.get("items", [])
                        if items:
                            items_count += len(items)
                            for item in items:
                                if not item.get("discovery_source"):
                                    item["discovery_source"] = "keyword_ideas"
                                all_items.append(DataForSEOMapper.sanitize_keyword_data_item(item))

            # Improved pagination logic using total_count
            if not paginated or page_count >= max_pages:
                break
            
            # Check if we've retrieved all available results
            if total_count is not None and len(all_items) >= total_count:
                self.logger.info(
                    f"Retrieved all {total_count} available results for {endpoint}. Stopping pagination."
                )
                break
            
            # Also check if no items were returned on this page
            if items_count == 0:
                self.logger.info(
                    f"No items returned on page {page_count} for {endpoint}. Stopping pagination."
                )
                break
```

---

### Task 10.2: Add Centralized Cost Tracking
**Priority:** MEDIUM
**File:** Create new file `core/cost_tracker.py`

**Exact Changes:**
```python
# CREATE NEW FILE: backend/core/cost_tracker.py

import threading
from typing import Dict, Any, List
from datetime import datetime


class CostTracker:
    """
    Centralized cost tracking for all API calls in a workflow.
    Thread-safe implementation for concurrent operations.
    """
    
    def __init__(self):
        self._lock = threading.Lock()
        self._costs: Dict[str, List[Dict[str, Any]]] = {}
    
    def track_cost(
        self,
        workflow_id: str,
        service: str,
        cost: float,
        details: str = ""
    ):
        """
        Records a cost entry for a specific workflow.
        
        Args:
            workflow_id: Unique identifier for the workflow (e.g., job_id, opportunity_id)
            service: Name of the service (e.g., "DataForSEO SERP", "OpenAI Generation")
            cost: Cost in USD
            details: Additional context about the API call
        """
        with self._lock:
            if workflow_id not in self._costs:
                self._costs[workflow_id] = []
            
            self._costs[workflow_id].append({
                "timestamp": datetime.now().isoformat(),
                "service": service,
                "cost": round(cost, 6),
                "details": details
            })
    
    def get_workflow_cost(self, workflow_id: str) -> float:
        """Returns total cost for a specific workflow."""
        with self._lock:
            if workflow_id not in self._costs:
                return 0.0
            return sum(entry["cost"] for entry in self._costs[workflow_id])
    
    def get_workflow_breakdown(self, workflow_id: str) -> List[Dict[str, Any]]:
        """Returns detailed cost breakdown for a workflow."""
        with self._lock:
            return self._costs.get(workflow_id, []).copy()
    
    def clear_workflow(self, workflow_id: str):
        """Clears cost data for a completed workflow."""
        with self._lock:
            if workflow_id in self._costs:
                del self._costs[workflow_id]
```

**Then integrate into WorkflowOrchestrator:**

**File:** `pipeline/orchestrator/main.py`

```python
# ADD IMPORT:
from backend.core.cost_tracker import CostTracker

# FIND in __init__ method (around line 45-60):
        self.content_auditor = ContentAuditor()
        self.prompt_assembler = DynamicPromptAssembler(self.db_manager)
        self.serp_analysis_service = SerpAnalysisService(self.dataforseo_client, self.client_cfg)

# ADD AFTER:
        self.cost_tracker = CostTracker()
```

**Then update content_orchestrator.py to use it:**

**File:** `pipeline/orchestrator/content_orchestrator.py`

```python
# FIND (line 50-55):
            # --- START COST TRACKING MODIFICATION ---
            total_api_cost = opportunity.get("blueprint", {}).get("metadata", {}).get("total_api_cost", 0.0)
            self.logger.info(f"Initial cost from blueprint: ${total_api_cost:.4f}")
            # --- END COST TRACKING MODIFICATION ---

# REPLACE WITH:
            # Initialize centralized cost tracking
            workflow_cost_id = f"generation_{opportunity_id}"
            
            # Start with costs from blueprint (analysis phase)
            blueprint_cost = opportunity.get("blueprint", {}).get("metadata", {}).get("total_api_cost", 0.0)
            if blueprint_cost > 0:
                self.cost_tracker.track_cost(
                    workflow_cost_id,
                    "Previous Analysis Phase",
                    blueprint_cost,
                    "Costs from blueprint generation"
                )
            
            self.logger.info(f"Initial cost from blueprint: ${blueprint_cost:.4f}")

# THEN UPDATE cost tracking throughout:
# FIND (around line 100):
                total_api_cost += cost # Aggregate cost

# REPLACE WITH:
                self.cost_tracker.track_cost(
                    workflow_cost_id,
                    f"Content Generation - {node['title'][:30]}",
                    cost,
                    f"Generated {node['type']} section"
                )

# FIND (around line 170):
            total_api_cost += image_cost
            social_posts, social_cost = self.social_crafter.craft_posts(opportunity)
            total_api_cost += social_cost

# REPLACE WITH:
            if image_cost > 0:
                self.cost_tracker.track_cost(
                    workflow_cost_id,
                    "Featured Image Generation",
                    image_cost,
                    "Pexels API or image generation"
                )
            
            social_posts, social_cost = self.social_crafter.craft_posts(opportunity)
            if social_cost > 0:
                self.cost_tracker.track_cost(
                    workflow_cost_id,
                    "Social Media Post Generation",
                    social_cost,
                    f"Generated {len(social_posts) if social_posts else 0} posts"
                )

# FIND (around line 180):
            total_api_cost += link_cost

# REPLACE WITH:
            if link_cost > 0:
                self.cost_tracker.track_cost(
                    workflow_cost_id,
                    "Internal Linking Suggestions",
                    link_cost,
                    f"Generated {len(internal_link_suggestions) if internal_link_suggestions else 0} suggestions"
                )

# FIND (at the end before saving, around line 190):
            self.db_manager.save_full_content_package(
                opportunity_id,
                opportunity["ai_content"],
                self.client_cfg.get("ai_content_model", "gpt-4o"),
                featured_image_data,
                [],
                social_posts,
                final_package,
                total_api_cost, # Pass total cost
            )

# REPLACE WITH:
            # Get final total cost from tracker
            total_api_cost = self.cost_tracker.get_workflow_cost(workflow_cost_id)
            cost_breakdown = self.cost_tracker.get_workflow_breakdown(workflow_cost_id)
            
            self.logger.info(f"Total content generation cost: ${total_api_cost:.4f}")
            self.logger.info(f"Cost breakdown: {len(cost_breakdown)} API calls")
            
            self.db_manager.save_full_content_package(
                opportunity_id,
                opportunity["ai_content"],
                self.client_cfg.get("ai_content_model", "gpt-4o"),
                featured_image_data,
                [],
                social_posts,
                final_package,
                total_api_cost,
            )
            
            # Clear cost tracking data for this workflow
            self.cost_tracker.clear_workflow(workflow_cost_id)
```

---

### Task 10.3: Add Early Cannibalization Check
**Priority:** MEDIUM
**File:** `pipeline/step_01_discovery/run_discovery.py`

**Exact Changes:**
```python
# FIND (line 30-45):
    # 1. Get keywords that already exist for this client to avoid API calls for them.
    existing_keywords = set(db_manager.get_all_processed_keywords_for_client(client_id))
    logger.info(
        f"Found {len(existing_keywords)} existing keywords to exclude from API request."
    )

    # 2. Expand seed keywords into a large list of opportunities.
    expansion_result = expander.expand_seed_keyword(
        seed_keywords,
        discovery_modes,
        filters,
        order_by,
        existing_keywords,
        limit,
        depth,
        ignore_synonyms,
        discovery_max_pages,
    )

# REPLACE WITH:
    # 1. Get keywords that already exist for this client to avoid API calls for them.
    existing_keywords = set(db_manager.get_all_processed_keywords_for_client(client_id))
    logger.info(
        f"Found {len(existing_keywords)} existing keywords to exclude from API request."
    )
    
    # 1b. Early cannibalization check on seed keywords
    # Filter out seed keywords that already exist (would be caught later anyway)
    original_seed_count = len(seed_keywords)
    seed_keywords = [kw for kw in seed_keywords if kw.lower() not in existing_keywords]
    
    if len(seed_keywords) < original_seed_count:
        logger.info(
            f"Early cannibalization filter: Removed {original_seed_count - len(seed_keywords)} "
            f"seed keywords that already exist in database."
        )
    
    if not seed_keywords:
        logger.warning("All seed keywords already exist in database. Skipping discovery.")
        return {
            "stats": {
                "total_cost": 0.0,
                "raw_counts": {},
                "total_raw_count": 0,
                "total_unique_count": 0,
                "disqualification_reasons": {"Already exists in database": original_seed_count},
                "disqualified_count": original_seed_count,
                "final_qualified_count": 0,
            },
            "total_cost": 0.0,
            "opportunities": [],
        }

    # 2. Expand seed keywords into a large list of opportunities.
    expansion_result = expander.expand_seed_keyword(
        seed_keywords,
        discovery_modes,
        filters,
        order_by,
        existing_keywords,
        limit,
        depth,
        ignore_synonyms,
        discovery_max_pages,
    )
```

---

### Task 10.4: Add Depth Validation
**Priority:** MEDIUM
**File:** Already covered in Task 2.6 - Verify complete

---

### Task 10.5: Add Keyword Lowercase Normalization
**Priority:** LOW
**File:** `pipeline/step_01_discovery/run_discovery.py`

**Exact Changes:**
```python
# FIND (line 95-110, in the deduplication loop):
        final_keywords_deduplicated = []
        seen_keywords = set(
            existing_keywords
        )  # Start with already existing to prevent re-adding

        # Recalculate raw counts per source based on `discovery_source` field added by get_keyword_ideas
        raw_counts = {"keyword_ideas": 0, "suggestions": 0, "related": 0}
        for item in all_expanded_keywords:
            kw_text = item.get("keyword", "").lower()
            if kw_text and kw_text not in seen_keywords:
                final_keywords_deduplicated.append(item)
                seen_keywords.add(kw_text)

# REPLACE WITH:
        final_keywords_deduplicated = []
        # Convert existing keywords to lowercase set for case-insensitive comparison
        # Per API docs: "keywords will be converted to lowercase format"
        seen_keywords = set(kw.lower() for kw in existing_keywords)

        # Recalculate raw counts per source based on `discovery_source` field
        raw_counts = {"keyword_ideas": 0, "keyword_suggestions": 0, "related_keywords": 0}
        
        for item in all_expanded_keywords:
            # Normalize keyword to lowercase per API behavior
            kw_text = item.get("keyword", "")
            if not kw_text:
                continue
            
            kw_normalized = kw_text.lower().strip()
            
            if kw_normalized and kw_normalized not in seen_keywords:
                # Store normalized version back
                item["keyword"] = kw_normalized
                final_keywords_deduplicated.append(item)
                seen_keywords.add(kw_normalized)
                
                # Track source counts
                source = item.get("discovery_source", "unknown")
                if source in raw_counts:
                    raw_counts[source] += 1
            elif kw_normalized:
                logger.debug(
                    f"Skipping duplicate or existing keyword: {kw_text}"
                )
```

---
