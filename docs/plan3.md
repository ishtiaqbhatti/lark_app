
## Phase 11: Comprehensive Sanitization Layer (Issues #26, #27, #34, #60, #73, #75)

### Task 11.1: Add Complete DataForSEO Response Sanitization
**Priority:** HIGH
**File:** `data_mappers/dataforseo_mapper.py`

**Exact Changes:**
```python
# ADD NEW METHOD at the end of DataForSEOMapper class:

    @staticmethod
    def sanitize_complete_api_response(
        response: Dict[str, Any],
        endpoint: str
    ) -> Dict[str, Any]:
        """
        Master sanitization method that validates and cleans an entire API response.
        
        Args:
            response: Raw response from DataForSEO API
            endpoint: The endpoint that was called (for context-specific sanitization)
        
        Returns:
            Fully sanitized response ready for processing
        """
        if not isinstance(response, dict):
            logger.error(f"API response is not a dictionary: {type(response)}")
            return {
                "status_code": 50
                ```python
            return {
                "status_code": 50000,
                "status_message": "Invalid response format",
                "tasks": [],
                "tasks_error": 1,
                "cost": 0.0
            }
        
        sanitized = response.copy()
        
        # Validate top-level response structure
        if "status_code" not in sanitized:
            logger.error("API response missing status_code field")
            sanitized["status_code"] = 50000
        
        if "tasks" not in sanitized or not isinstance(sanitized["tasks"], list):
            logger.error("API response missing or invalid 'tasks' array")
            sanitized["tasks"] = []
            sanitized["tasks_error"] = 1
            return sanitized
        
        # Sanitize each task
        for task_idx, task in enumerate(sanitized["tasks"]):
            if not isinstance(task, dict):
                logger.warning(f"Task {task_idx} is not a dictionary: {type(task)}")
                continue
            
            # Ensure task has required fields
            if "status_code" not in task:
                task["status_code"] = 50000
            
            if "result" not in task or not isinstance(task["result"], list):
                logger.warning(f"Task {task_idx} missing or invalid 'result' array")
                task["result"] = []
                continue
            
            # Sanitize result items based on endpoint type
            for result_idx, result_item in enumerate(task["result"]):
                if not isinstance(result_item, dict):
                    logger.warning(f"Result item {result_idx} in task {task_idx} is not a dictionary")
                    continue
                
                # Apply endpoint-specific sanitization
                if "keyword_ideas" in endpoint or "keyword_suggestions" in endpoint:
                    # Sanitize items array
                    if "items" in result_item and isinstance(result_item["items"], list):
                        result_item["items"] = [
                            DataForSEOMapper.sanitize_keyword_data_item(item)
                            for item in result_item["items"]
                            if isinstance(item, dict)
                        ]
                
                elif "related_keywords" in endpoint:
                    # Sanitize keyword_data objects
                    if "items" in result_item and isinstance(result_item["items"], list):
                        sanitized_items = []
                        for item in result_item["items"]:
                            if isinstance(item, dict) and "keyword_data" in item:
                                keyword_data = item["keyword_data"]
                                if isinstance(keyword_data, dict):
                                    sanitized_kw_data = DataForSEOMapper.sanitize_keyword_data_item(keyword_data)
                                    item["keyword_data"] = sanitized_kw_data
                                    sanitized_items.append(item)
                        result_item["items"] = sanitized_items
        
        return sanitized
```

**Then update _post_request to use this:**

**File:** `external_apis/dataforseo_client_v2.py`

```python
# FIND (line 100-110, before caching response):
                response_json = response.json()

                # W20 FIX: Check top-level status_code from DataForSEO
                if response_json.get("status_code") != 20000:
                    self.logger.error(
                        f"DataForSEO API returned non-20000 status_code: {response_json.get('status_code')} - {response_json.get('status_message')}"
                    )

# REPLACE WITH:
                response_json = response.json()
                
                # Apply comprehensive sanitization
                from backend.data_mappers.dataforseo_mapper import DataForSEOMapper
                response_json = DataForSEOMapper.sanitize_complete_api_response(
                    response_json,
                    endpoint
                )

                # Check top-level status_code from DataForSEO
                if response_json.get("status_code") != 20000:
                    self.logger.error(
                        f"DataForSEO API returned non-20000 status_code: {response_json.get('status_code')} - {response_json.get('status_message')}"
                    )
```

---

### Task 11.2: Refactor Duplicate Normalization Code
**Priority:** LOW
**File:** `data_mappers/dataforseo_mapper.py`

**Exact Changes:**
```python
# ADD NEW HELPER METHOD at the top of DataForSEOMapper class (after class definition):

    @staticmethod
    def _safe_convert_to_int(value: Any, default: int = 0) -> int:
        """Safely converts a value to integer, returning default on failure."""
        if value is None:
            return default
        try:
            return int(value)
        except (ValueError, TypeError):
            logger.warning(f"Could not convert value to int: {value} (type: {type(value)})")
            return default
    
    @staticmethod
    def _safe_convert_to_float(value: Any, default: float = 0.0) -> float:
        """Safely converts a value to float, returning default on failure."""
        if value is None:
            return default
        try:
            return float(value)
        except (ValueError, TypeError):
            logger.warning(f"Could not convert value to float: {value} (type: {type(value)})")
            return default

# THEN REPLACE all manual conversions with these helpers:
# FIND (in sanitize_keyword_data_item, around line 120-135):
            # Ensure CPC and Competition are floats, defaulting to 0.0 if missing or None
            sanitized_item["keyword_info"]["cpc"] = float(
                sanitized_item["keyword_info"].get("cpc") or 0.0
            )
            sanitized_item["keyword_info"]["competition"] = float(
                sanitized_item["keyword_info"].get("competition") or 0.0
            )

            # Ensure other numeric fields are handled
            sanitized_item["keyword_info"]["search_volume"] = int(
                sanitized_item["keyword_info"].get("search_volume") or 0
            )
            sanitized_item["keyword_info"]["low_top_of_page_bid"] = float(
                sanitized_item["keyword_info"].get("low_top_of_page_bid") or 0.0
            )
            sanitized_item["keyword_info"]["high_top_of_page_bid"] = float(
                sanitized_item["keyword_info"].get("high_top_of_page_bid") or 0.0
            )

# REPLACE WITH:
            # Ensure CPC and Competition are floats using safe conversion
            sanitized_item["keyword_info"]["cpc"] = DataForSEOMapper._safe_convert_to_float(
                sanitized_item["keyword_info"].get("cpc"), 0.0
            )
            sanitized_item["keyword_info"]["competition"] = DataForSEOMapper._safe_convert_to_float(
                sanitized_item["keyword_info"].get("competition"), 0.0
            )

            # Ensure other numeric fields are handled
            sanitized_item["keyword_info"]["search_volume"] = DataForSEOMapper._safe_convert_to_int(
                sanitized_item["keyword_info"].get("search_volume"), 0
            )
            sanitized_item["keyword_info"]["low_top_of_page_bid"] = DataForSEOMapper._safe_convert_to_float(
                sanitized_item["keyword_info"].get("low_top_of_page_bid"), 0.0
            )
            sanitized_item["keyword_info"]["high_top_of_page_bid"] = DataForSEOMapper._safe_convert_to_float(
                sanitized_item["keyword_info"].get("high_top_of_page_bid"), 0.0
            )
```

---

## Phase 12: Missing Features and Parameters (Issues #74, #76, #77)

### Task 12.1: Add replace_with_core_keyword Support
**Priority:** LOW
**File:** Already implemented in code - verify it's passed correctly

**Verification Only:** Check that this parameter is in the related_task dict (line 530 in dataforseo_client_v2.py)

---

### Task 12.2: Add UTF-8 Encoding Validation
**Priority:** LOW
**File:** `external_apis/dataforseo_client_v2.py`

**Exact Changes:**
```python
# ADD NEW METHOD in DataForSEOClientV2 class (after __init__):

    def _validate_utf8_keywords(self, keywords: List[str]) -> List[str]:
        """
        Validates and ensures keywords are properly UTF-8 encoded.
        Per API docs: "UTF-8 encoding"
        """
        validated = []
        for kw in keywords:
            if not isinstance(kw, str):
                self.logger.warning(f"Keyword is not a string: {type(kw)}. Skipping.")
                continue
            
            try:
                # Ensure it can be encoded as UTF-8
                kw.encode('utf-8')
                validated.append(kw)
            except UnicodeEncodeError as e:
                self.logger.error(
                    f"Keyword '{kw}' contains invalid UTF-8 characters: {e}. Skipping."
                )
        
        return validated

# THEN UPDATE get_keyword_ideas to use validation:
# FIND (updated from Task 2.5, around line 400-415):
        if len(seed_keywords) > 200:
            self.logger.warning(
                f"Seed keywords array exceeds API maximum of 200 keywords ({len(seed_keywords)} provided). "
                "Truncating to first 200 keywords."
            )
            seed_keywords = seed_keywords[:200]
        
        all_items = []

# ADD AFTER:
        # Validate UTF-8 encoding per API requirements
        seed_keywords = self._validate_utf8_keywords(seed_keywords)
        if not seed_keywords:
            self.logger.error("No valid UTF-8 keywords after validation.")
            return [], 0.0
```

---

### Task 12.3: Add API Request Structure Validation
**Priority:** LOW
**File:** `external_apis/dataforseo_client_v2.py`

**Exact Changes:**
```python
# ADD NEW METHOD after _validate_utf8_keywords:

    def _validate_task_structure(self, task_data: Dict[str, Any], endpoint: str) -> bool:
        """
        Validates that a task dictionary has the required structure before sending to API.
        
        Per API docs: "you should send all task parameters in the task array"
        """
        if not isinstance(task_data, dict):
            self.logger.error(f"Task data is not a dictionary for {endpoint}: {type(task_data)}")
            return False
        
        # Endpoint-specific required fields
        required_fields = {
            self.LABS_KEYWORD_IDEAS: ["keywords", "location_code", "language_code"],
            self.LABS_KEYWORD_SUGGESTIONS: ["keyword", "location_code", "language_code"],
            self.LABS_RELATED_KEYWORDS: ["keyword", "location_code", "language_code"],
            self.SERP_ADVANCED: ["keyword", "location_code", "language_code"],
            self.ONPAGE_INSTANT_PAGES: ["url"],
        }
        
        required = required_fields.get(endpoint, [])
        missing = [field for field in required if field not in task_data]
        
        if missing:
            self.logger.error(
                f"Task for {endpoint} missing required fields: {missing}. Task: {task_data}"
            )
            return False
        
        return True

# THEN UPDATE _post_request to validate before sending:
# FIND (line 75-85):
        full_url = f"{self.base_url.rstrip('/')}/{endpoint.lstrip('/')}"
        self.logger.info(
            f"Making POST request to {full_url} with data: {json.dumps(data)}"
        )
        retries = 3

# ADD BEFORE:
        # Validate task structure
        for task in data:
            if not self._validate_task_structure(task, endpoint):
                self.logger.error(f"Invalid task structure for {endpoint}. Aborting request.")
                return {
                    "status_code": 40000,
                    "status_message": "Invalid task structure - validation failed",
                    "tasks": [],
                    "tasks_error": 1,
                    "cost": 0.0
                }, 0.0
        
        full_url = f"{self.base_url.rstrip('/')}/{endpoint.lstrip('/')}"
        self.logger.info(
            f"Making POST request to {full_url} with data: {json.dumps(data)}"
        )
        retries = 3
```

---

## Phase 13: Update Frontend Filter Handling (Issues #45, #47, #49)

### Task 13.1: Fix Frontend Filter Path Construction
**Priority:** HIGH
**File:** `api/routers/discovery.py`

**Exact Changes:**
```python
# FIND (line 30-75, the construct_paths helper and its usage):
    def construct_paths(prefix, items):
        new_items = []
        for item in items:
            new_item = item.copy()
            if "search_volume" in new_item["name"]:
                new_item["name"] = f"{prefix}keyword_info.search_volume"
            elif "keyword_difficulty" in new_item["name"]:
                new_item["name"] = f"{prefix}keyword_properties.keyword_difficulty"
            elif "main_intent" in new_item["name"]:
                new_item["name"] = f"{prefix}search_intent_info.main_intent"
            elif "competition_level" in new_item["name"]:
                new_item["name"] = f"{prefix}keyword_info.competition_level"
            elif "cpc" in new_item["name"]:
                new_item["name"] = f"{prefix}keyword_info.cpc"
            elif "competition" in new_item["name"]:
                new_item["name"] = f"{prefix}keyword_info.competition"
            new_items.append(new_item)
        return new_items

# REPLACE WITH:
    def construct_paths(prefix, items):
        """
        Constructs filter paths with proper prefix for different API endpoints.
        
        CRITICAL: Related Keywords requires 'keyword_data.' prefix per API docs.
        Ideas and Suggestions use no prefix.
        """
        new_items = []
        for item in items:
            new_item = item.copy()
            field_name = new_item.get("name", "")
            
            # Map friendly names to API field paths
            if "search_volume" in field_name:
                new_item["name"] = f"{prefix}keyword_info.search_volume"
            elif "keyword_difficulty" in field_name:
                new_item["name"] = f"{prefix}keyword_properties.keyword_difficulty"
            elif "main_intent" in field_name:
                new_item["name"] = f"{prefix}search_intent_info.main_intent"
            elif "competition_level" in field_name:
                new_item["name"] = f"{prefix}keyword_info.competition_level"
            elif "cpc" in field_name:
                new_item["name"] = f"{prefix}keyword_info.cpc"
            elif "competition" in field_name:
                new_item["name"] = f"{prefix}keyword_info.competition"
            
            new_items.append(new_item)
        return new_items
    
    # Validate that we're constructing correct paths
    # For Related Keywords, prefix must be "keyword_data."
    # For Ideas and Suggestions, no prefix
```

---

### Task 13.2: Add Filter Count Warning in Frontend Response
**Priority:** LOW
**File:** `api/routers/discovery.py`

**Exact Changes:**
```python
# FIND (line 25-30):
@router.get("/discovery/available-filters")
async def get_available_filters():
    """
    Returns a curated list of available discovery modes, filters, and sorting options,
    structured to be easily consumable by the frontend.
    """

# REPLACE WITH:
@router.get("/discovery/available-filters")
async def get_available_filters():
    """
    Returns a curated list of available discovery modes, filters, and sorting options,
    structured to be easily consumable by the frontend.
    
    IMPORTANT: Per DataForSEO API, maximum 8 filters can be applied per request.
    """
```

**Then update the return structure to include this info:**

```python
# FIND (at the end of get_available_filters, around line 140):
    ]

# REPLACE WITH:
    ]
    
    # Add API constraints information for frontend validation
    api_constraints = {
        "max_filters": 8,
        "max_sorting_rules": 3,
        "max_seed_keywords": 200,
        "max_regex_length": 1000,
    }
    
    return {
        "discovery_modes": modes,  # The existing list
        "api_constraints": api_constraints
    }

# BUT WAIT - need to wrap the existing return list:
# FIND the entire return statement (line 78-140):
    return [
        {
            "id": "keyword_ideas",
            ...
        },
        ...
    ]

# REPLACE WITH:
    modes = [
        {
            "id": "keyword_ideas",
            "name": "Broad Market Research",
            "description": "Get a wide range of keyword ideas related to your topic.",
            "filters": construct_paths("", base_filters),
            "sorting": [{"name": "relevance", "label": "Relevance"}]
            + construct_paths("", base_sorting),
            "defaults": {
                "filters": [
                    {"field": "keyword_info.search_volume", "operator": ">", "value": 500},
                    {"field": "keyword_properties.keyword_difficulty", "operator": "<", "value": 30},
                ],
                "order_by": ["relevance,desc"],  # Fixed in Task 2.9
            },
        },
        {
            "id": "keyword_suggestions",
            "name": "Long-Tail Keywords",
            "description": "Find specific, multi-word keywords that are easier to rank for.",
            "filters": construct_paths("", base_filters),
            "sorting": construct_paths("", base_sorting),
            "defaults": {
                "filters": [
                    {"field": "keyword_info.search_volume", "operator": ">", "value": 100},
                    {"field": "keyword_properties.keyword_difficulty", "operator": "<", "value": 20},
                ],
                "order_by": ["keyword_info.search_volume,desc"],
            },
        },
        {
            "id": "related_keywords",
            "name": "Semantic Keyword Expansion",
            "description": "Find semantically related terms to expand content depth and discover related topics.",
            "filters": construct_paths("keyword_data.", base_filters),
            "sorting": construct_paths("keyword_data.", base_sorting),
            "defaults": {
                "filters": [
                    {"field": "keyword_data.keyword_info.search_volume", "operator": ">", "value": 100},
                ],
                "order_by": ["keyword_data.keyword_info.search_volume,desc"],
            },
        },
        {
            "id": "find_questions",
            "name": "Customer Questions",
            "description": "Find out what questions your customers are asking about your topic.",
            "filters": construct_paths("", base_filters),
            "sorting": construct_paths("", base_sorting),
            "defaults": {
                "filters": [
                    {"field": "keyword_info.search_volume", "operator": ">", "value": 50},
                ],
                "order_by": ["keyword_info.search_volume,desc"],
            },
        },
    ]
    
    # Add API constraints for frontend validation
    return {
        "modes": modes,
        "api_constraints": {
            "max_filters": 8,
            "max_sorting_rules": 3,
            "max_seed_keywords": 200,
            "max_regex_length": 1000,
        }
    }
```

---

## Phase 14: Code Quality and Consistency (Issues #26-35, #70)

### Task 14.1: Fix Inconsistent Variable Naming
**Priority:** LOW
**File:** `pipeline/step_03_prioritization/scoring_engine.py`

**Exact Changes:**
```python
# FIND (line 28-35):
    def calculate_score(
        self, opportunity: Dict[str, Any]
    ) -> Tuple[float, Dict[str, Any]]:
        """
        Calculates the final opportunity score by combining weighted scores
        from all registered scoring components.
        """
        if not isinstance(opportunity, dict):
            self.logger.warning(
                "Invalid data format passed to calculate_score. Expected a dictionary."
            )
            return 0.0, {"error": "Invalid data format."}

        breakdown = {}
        data_source = opportunity.get("full_data", opportunity)

# REPLACE WITH:
    def calculate_score(
        self, opportunity: Dict[str, Any]
    ) -> Tuple[float, Dict[str, Any]]:
        """
        Calculates the final opportunity score by combining weighted scores
        from all registered scoring components.
        """
        if not isinstance(opportunity, dict):
            self.logger.warning(
                "Invalid data format passed to calculate_score. Expected a dictionary."
            )
            return 0.0, {"error": "Invalid data format."}

        breakdown = {}
        # Use full_data if available (contains complete keyword data from discovery)
        # Otherwise use opportunity itself (for backward compatibility)
        opportunity_data = opportunity.get("full_data", opportunity)
        
        if not isinstance(opportunity_data, dict):
            self.logger.error("opportunity_data is not a dictionary after extraction")
            return 0.0, {"error": "Invalid opportunity_data structure."}
```

**Then replace all instances of `data_source` with `opportunity_data` in the rest of the method.**

---

### Task 14.2: Remove Dead Code
**Priority:** LOW
**File:** `external_apis/openai_client.py`

**Exact Changes:**
```python
# FIND (line 135-150):
    def call_image_generation(
        self,
        prompt: str,
        style_formula: str,
        quality: str,
        size: str,
        model: Optional[str] = None,
        retries: int = 3,
    ) -> Tuple[Optional[str], Optional[str], Optional[str]]:
        """
        Mocks OpenAI image generation. This function is present but *not used* in the final plan
        as Pexels is the exclusive image source. It's kept for potential future re-integration.
        """
        if model is None:
            model = self.client_cfg.get('default_image_model', 'dall-e-3')
        
        self.logger.info(
            "OpenAI image generation is configured but Pexels is prioritized. This function will not be called."
        )
        return (
            None,
            None,
            "OpenAI image generation bypassed; Pexels is the primary source.",
        )

# REPLACE WITH (or DELETE entirely):
    # REMOVED: call_image_generation method
    # OpenAI image generation is not used - Pexels is the exclusive image source.
    # If you need to re-enable OpenAI images in the future, implement from scratch
    # using the official OpenAI Images API documentation.
```

---

### Task 14.3: Add Comprehensive Docstrings
**Priority:** LOW
**File:** Multiple files - Example implementation for one critical method

**File:** `external_apis/dataforseo_client_v2.py`

**Exact Changes:**
```python
# FIND (line 380-400):
    def get_keyword_ideas(
        self,
        seed_keywords: List[str],
        location_code: int,
        language_code: str,
        client_cfg: Dict[str, Any],
        discovery_modes: List[str],
        filters: Dict[str, Any],
        order_by: Optional[Dict[str, List[str]]],
        limit: Optional[int] = None,
        depth: Optional[int] = None,
        ignore_synonyms_override: Optional[bool] = None,
        include_clickstream_override: Optional[bool] = None,
        closely_variants_override: Optional[bool] = None,
        exact_match_override: Optional[bool] = None,
        discovery_max_pages: Optional[int] = None,
    ) -> Tuple[List[Dict[str, Any]], float]:
        """
        Performs a comprehensive discovery burst using Keyword Ideas, Suggestions, and Related Keywords endpoints.
        """

# REPLACE WITH:
    def get_keyword_ideas(
        self,
        seed_keywords: List[str],
        location_code: int,
        language_code: str,
        client_cfg: Dict[str, Any],
        discovery_modes: List[str],
        filters: Dict[str, Any],
        order_by: Optional[Dict[str, List[str]]],
        limit: Optional[int] = None,
        depth: Optional[int] = None,
        ignore_synonyms_override: Optional[bool] = None,
        include_clickstream_override: Optional[bool] = None,
        closely_variants_override: Optional[bool] = None,
        exact_match_override: Optional[bool] = None,
        discovery_max_pages: Optional[int] = None,
    ) -> Tuple[List[Dict[str, Any]], float]:
        """
        Performs comprehensive keyword discovery using DataForSEO Labs API endpoints.
        
        Supports three discovery modes:
        1. Keyword Ideas: Category-based relevance search (max 200 seeds)
        2. Keyword Suggestions: Full-text search with additional words (per seed)
        3. Related Keywords: Depth-first search from "related searches" (per seed, depth 0-4)
        
        Args:
            seed_keywords: List of seed keywords (max 200 for Ideas, unlimited for others)
            location_code: DataForSEO location code (required)
            language_code: DataForSEO language code (required)
            client_cfg: Client configuration dictionary
            discovery_modes: List of modes to execute ["keyword_ideas", "keyword_suggestions", "related_keywords"]
            filters: Dict of filters per mode {"ideas": [...], "suggestions": [...], "related": [...]}
            order_by: Dict of sorting rules per mode (max 3 rules per mode)
            limit: Max results per endpoint (Ideas: default 700/max 1000, Others: default 100/max 1000)
            depth: Search depth for Related Keywords only (0-4, default 1)
            ignore_synonyms_override: Override for ignore_synonyms parameter
            include_clickstream_override: Override for include_clickstream_data (DOUBLES COST)
            closely_variants_override: Override for closely_variants (Ideas only)
            exact_match_override: Override for exact_match (Suggestions only)
            discovery_max_pages: Max pagination pages (default from config)
        
        Returns:
            Tuple of (list of keyword data dictionaries, total API cost in USD)
        
        Raises:
            ValueError: If required parameters are missing or invalid
        
        API Documentation:
            - Keyword Ideas: https://docs.dataforseo.com/v3/dataforseo_labs/google/keyword_ideas/live
            - Keyword Suggestions: https://docs.dataforseo.com/v3/dataforseo_labs/google/keyword_suggestions/live
            - Related Keywords: https://docs.dataforseo.com/v3/dataforseo_labs/google/related_keywords/live
        """
```

---

## Phase 15: Missing Imports and Dependencies

### Task 15.1: Add Missing Import in content_auditor.py
**Priority:** MEDIUM
**File:** `agents/content_auditor.py`

**Exact Changes:**
```python
# FIND (line 1-10):
import logging
import textstat
from typing import Dict, Any, List, Optional  # ADD List
from bs4 import BeautifulSoup  # ADD this for HTML parsing
import re  # ADD this for regex checks
import requests

# VERIFY all imports are present, ADD if missing:
# This looks correct, but verify requests is imported
```

---

### Task 15.2: Add Missing Import in prompt_assembler.py
**Priority:** LOW
**File:** `agents/prompt_assembler.py`

**Exact Changes:**
```python
# FIND (line 1-10):
import logging
from typing import Dict, Any, List

from backend.data_access.database_manager import DatabaseManager

# ADD:
import json

# So it becomes:
import logging
import json
from typing import Dict, Any, List

from backend.data_access.database_manager import DatabaseManager
```

---

## Phase 16: Infinite Loop and Edge Case Fixes (Issues #64, #70)

### Task 16.1: Enhance Infinite Loop Prevention in Pagination
**Priority:** HIGH
**File:** `external_apis/dataforseo_client_v2.py`

**Exact Changes:**
```python
# FIND (line 360-365, at start of post_with_paging):
    def post_with_paging(
        self,
        endpoint: str,
        initial_task: Dict[str, Any],
        max_pages: int,
        paginated: bool = True,
        tag: Optional[str] = None,
    ) -> Tuple[List[Dict[str, Any]], float]:
        """
        Executes a POST request and, if paginated=True, recursively retrieves all results using the correct pagination method.
        """
        all_items = []
        total_cost = 0.0
        current_task = initial_task.copy()

        if "filters" in current_task and (
            current_task["filters"] is None or len(current_task["filters"]) == 0
        ):
            current_task.pop("filters")

        page_count = 0
        previous_offset_token = None  # ADDED: For infinite loop prevention

# REPLACE WITH:
    def post_with_paging(
        self,
        endpoint: str,
        initial_task: Dict[str, Any],
        max_pages: int,
        paginated: bool = True,
        tag: Optional[str] = None,
    ) -> Tuple[List[Dict[str, Any]], float]:
        """
        Executes a POST request and, if paginated=True, recursively retrieves all results using the correct pagination method.
        
        Implements multiple safeguards against infinite loops:
        1. Max pages limit
        2. Duplicate offset_token detection
        3. Total results count tracking
        4. Zero items detection
        """
        all_items = []
        total_cost = 0.0
        current_task = initial_task.copy()

        if "filters" in current_task and (
            current_task["filters"] is None or len(current_task["filters"]) == 0
        ):
            current_task.pop("filters")

        page_count = 0
        previous_offset_token = None
        consecutive_empty_pages = 0  # NEW: Track empty pages
        total_results_count = None  # NEW: Track total available results
```

**Then update the pagination loop:**

```python
# FIND (in the pagination loop, around line 420-435):
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

# REPLACE WITH:
            # Multiple safeguards against infinite loops
            
            # 1. Check pagination mode
            if not paginate
            ```python
            # Multiple safeguards against infinite loops
            
            # 1. Check pagination mode
            if not paginated or page_count >= max_pages:
                self.logger.info(f"Stopping pagination: paginated={paginated}, page_count={page_count}, max_pages={max_pages}")
                break
            
            # 2. Check if we've retrieved all available results using total_count
            if total_count is not None:
                if len(all_items) >= total_count:
                    self.logger.info(
                        f"Retrieved all {total_count} available results for {endpoint}. Stopping pagination."
                    )
                    break
                
                # Also check if we're within 10% of total (API might have inconsistent counts)
                if len(all_items) >= total_count * 0.95:
                    self.logger.info(
                        f"Retrieved {len(all_items)}/{total_count} results (95%+). Stopping pagination."
                    )
                    break
            
            # 3. Check for empty pages
            if items_count == 0:
                consecutive_empty_pages += 1
                if consecutive_empty_pages >= 2:
                    self.logger.warning(
                        f"Received {consecutive_empty_pages} consecutive empty pages for {endpoint}. Stopping pagination."
                    )
                    break
            else:
                consecutive_empty_pages = 0  # Reset counter
            
            # 4. Validate offset_token exists for next page
            if not offset_token:
                self.logger.info(f"No offset_token in response for {endpoint}. End of results.")
                break
```

---

## Phase 17: Database Query Optimization (Issues #16, #20)

### Task 17.1: Add Composite Indexes for Common Queries
**Priority:** MEDIUM
**File:** Create new migration `data_access/migrations/026_add_composite_indexes.sql`

**Exact Changes:**
```sql
-- data_access/migrations/026_add_composite_indexes.sql

-- Composite index for common filtering query (client + status + score)
CREATE INDEX IF NOT EXISTS idx_opportunities_client_status_score 
ON opportunities (client_id, status, strategic_score DESC);

-- Composite index for qualified opportunities
CREATE INDEX IF NOT EXISTS idx_opportunities_qualified 
ON opportunities (client_id, blog_qualification_status, strategic_score DESC)
WHERE status NOT IN ('rejected', 'failed');

-- Composite index for date-based queries
CREATE INDEX IF NOT EXISTS idx_opportunities_client_date 
ON opportunities (client_id, date_added DESC);

-- Composite index for search functionality
CREATE INDEX IF NOT EXISTS idx_opportunities_keyword_search 
ON opportunities (client_id, keyword);

-- Index for job status queries
CREATE INDEX IF NOT EXISTS idx_jobs_status_started 
ON jobs (status, started_at DESC);

-- Index for discovery run queries
CREATE INDEX IF NOT EXISTS idx_discovery_runs_client_status 
ON discovery_runs (client_id, status, start_time DESC);

-- Index for content feedback queries
CREATE INDEX IF NOT EXISTS idx_content_feedback_opportunity 
ON content_feedback (opportunity_id, rating DESC);

-- Index for content history queries  
CREATE INDEX IF NOT EXISTS idx_content_history_opportunity_timestamp 
ON content_history (opportunity_id, timestamp DESC);
```

---

### Task 17.2: Optimize get_all_opportunities Query to Not Fetch full_data for Summaries
**Priority:** MEDIUM
**File:** `data_access/database_manager.py`

**Exact Changes:**
```python
# FIND (line 570-620, the get_all_opportunities method):
        select_columns = (
            select_columns
            if select_columns
            else "id, keyword, status, date_added, strategic_score, search_volume, keyword_difficulty, cpc, competition, main_intent, search_volume_trend_json, competitor_social_media_tags_json, competitor_page_timing_json, blog_qualification_status, latest_job_id, cluster_name, score_breakdown, full_data"
        )
        if summary and "full_data" not in select_columns:
            select_columns += ", full_data"

# REPLACE WITH:
        # Define column sets for different query types
        SUMMARY_COLUMNS = (
            "id, keyword, status, date_added, strategic_score, search_volume, "
            "keyword_difficulty, cpc, competition, main_intent, "
            "blog_qualification_status, blog_qualification_reason, latest_job_id, cluster_name"
        )
        
        FULL_COLUMNS = (
            "id, keyword, status, date_added, strategic_score, search_volume, "
            "keyword_difficulty, cpc, competition, main_intent, search_volume_trend_json, "
            "competitor_social_media_tags_json, competitor_page_timing_json, "
            "blog_qualification_status, latest_job_id, cluster_name, score_breakdown, full_data"
        )
        
        if select_columns:
            # Validate provided columns (already done in Task 3.1)
            pass
        elif summary:
            # For summary views, don't fetch heavy JSON blobs
            select_columns = SUMMARY_COLUMNS
        else:
            # For detail views, fetch everything
            select_columns = FULL_COLUMNS
```

**Then update the deserialization logic:**

```python
# FIND (line 640-655):
        # Manually extract and add search_volume and keyword_difficulty for the frontend
        for opp in opportunities:
            try:
                if opp.get("full_data"):
                    full_data = opp["full_data"]
                    opp["search_volume"] = full_data.get("keyword_info", {}).get(
                        "search_volume"
                    )
                    opp["keyword_difficulty"] = full_data.get(
                        "keyword_properties", {}
                    ).get("keyword_difficulty")
            except (KeyError, TypeError):
                opp["search_volume"] = None
                opp["keyword_difficulty"] = None

        return opportunities, total_count

# REPLACE WITH:
        # For summary queries, search_volume and keyword_difficulty are already in direct columns
        # Only extract from full_data if it exists and direct columns are null
        for opp in opportunities:
            # Ensure these fields exist (use direct columns if available)
            if opp.get("search_volume") is None and opp.get("full_data"):
                try:
                    full_data = opp["full_data"]
                    opp["search_volume"] = full_data.get("keyword_info", {}).get("search_volume")
                except (KeyError, TypeError):
                    opp["search_volume"] = None
            
            if opp.get("keyword_difficulty") is None and opp.get("full_data"):
                try:
                    full_data = opp["full_data"]
                    opp["keyword_difficulty"] = full_data.get("keyword_properties", {}).get("keyword_difficulty")
                except (KeyError, TypeError):
                    opp["keyword_difficulty"] = None

        return opportunities, total_count
```

---

## Phase 18: Final Integration and Consistency Fixes

### Task 18.1: Update Discovery Endpoint to Handle Keyword Suggestions Correctly
**Priority:** HIGH
**File:** `external_apis/dataforseo_client_v2.py`

**Action:** Fix the keyword_suggestions implementation that was started in Task 2.6

**Exact Changes:**
```python
# FIND (the keyword_suggestions section we modified in Task 2.6, around line 470-490):
            if "keyword_suggestions" in discovery_modes:
                self.logger.info("Fetching keyword suggestions...")
                suggestions_endpoint = self.LABS_KEYWORD_SUGGESTIONS
                
                # Process each seed keyword separately (Suggestions takes single keyword, not array)
                for seed in seed_keywords:
                    sanitized_suggestions_filters = self._prioritize_and_limit_filters(
                        self._convert_filters_to_api_format(filters.get("suggestions"))
                    )

# VERIFY this section is complete and add the actual API call:
# The section should look like this after all previous tasks:

            if "keyword_suggestions" in discovery_modes:
                self.logger.info("Fetching keyword suggestions...")
                suggestions_endpoint = self.LABS_KEYWORD_SUGGESTIONS
                
                all_suggestions_items = []
                
                # Process each seed keyword separately (Suggestions API takes single keyword)
                for seed in seed_keywords:
                    sanitized_suggestions_filters = self._prioritize_and_limit_filters(
                        self._convert_filters_to_api_format(filters.get("suggestions"))
                    )
                    
                    # Validate and set default limit per API docs (default: 100, max: 1000)
                    suggestions_limit = int(limit or 100)
                    if suggestions_limit > 1000:
                        self.logger.warning(f"Keyword Suggestions limit {suggestions_limit} exceeds max of 1000. Setting to 1000.")
                        suggestions_limit = 1000
                    
                    suggestions_task = {
                        "keyword": seed,  # Singular keyword, not array
                        "location_code": location_code,
                        "language_code": language_code,
                        "limit": suggestions_limit,
                        "include_serp_info": True,
                        "exact_match": exact_match,
                        "ignore_synonyms": ignore_synonyms,
                        "include_seed_keyword": True,
                        "filters": sanitized_suggestions_filters,
                        "order_by": self._validate_and_limit_order_by(
                            order_by.get("suggestions") if order_by else ["keyword_info.search_volume,desc"],
                            "Keyword Suggestions"
                        ),
                        "include_clickstream_data": include_clickstream,
                    }
                    
                    suggestions_items, cost = self.post_with_paging(
                        suggestions_endpoint,
                        suggestions_task,
                        max_pages=max_pages,
                        tag=f"discovery_suggestions:{seed[:20]}",
                    )
                    total_cost += cost
                    all_suggestions_items.extend(suggestions_items)
                
                self.logger.info(
                    f"Found {len(all_suggestions_items)} total suggestions from {len(seed_keywords)} seeds."
                )
                all_items.extend(all_suggestions_items)
```

**Make sure the old code path is removed:**

```python
# DELETE any old suggestions code that comes after this - it should not exist
# The pattern to look for and DELETE:
suggestions_items, cost = self.post_with_paging(
    suggestions_endpoint,
    suggestions_task,
    max_pages=max_pages,
    tag="discovery_suggestions",
)
total_cost += cost
for item in suggestions_items:
    item["discovery_source"] = "keyword_suggestions"
    item["depth"] = 0
    all_items.append(DataForSEOMapper.sanitize_keyword_data_item(item))
self.logger.info(
    f"Found {len(suggestions_items)} suggestions."
)

# IF this old code exists, DELETE IT entirely
```

---

### Task 18.2: Add Comprehensive Logging for API Responses
**Priority:** LOW
**File:** `external_apis/dataforseo_client_v2.py`

**Exact Changes:**
```python
# FIND (in _post_request, after receiving response, around line 100):
                response_json = response.json()
                
                # Apply comprehensive sanitization
                from backend.data_mappers.dataforseo_mapper import DataForSEOMapper
                response_json = DataForSEOMapper.sanitize_complete_api_response(
                    response_json,
                    endpoint
                )

# ADD AFTER:
                # Log response summary for debugging
                if response_json.get("tasks"):
                    task_count = len(response_json["tasks"])
                    success_count = sum(1 for t in response_json["tasks"] if t.get("status_code") == 20000)
                    self.logger.info(
                        f"API Response: {success_count}/{task_count} tasks successful, "
                        f"Cost: ${response_json.get('cost', 0.0):.4f}"
                    )
                    
                    # Log any task-level errors
                    for task in response_json["tasks"]:
                        if task.get("status_code") != 20000:
                            self.logger.warning(
                                f"Task failed: {task.get('status_code')} - {task.get('status_message')}"
                            )
```

---

## Phase 19: Error Recovery and Rollback (Issues #37, #23)

### Task 19.1: Add Transaction Rollback for Workflow Failures
**Priority:** HIGH
**File:** `pipeline/orchestrator/workflow_orchestrator.py`

**Exact Changes:**
```python
# FIND (line 25-50, in _run_full_auto_workflow_background):
        try:
            self.db_manager.update_opportunity_workflow_state(
                opportunity_id, "in_progress", "running"
            )
            self.job_manager.update_job_progress(job_id, "Workflow Started", "Starting full automation workflow.")

# REPLACE WITH:
        original_status = None
        original_workflow_step = None
        
        try:
            # Record original state for potential rollback
            opportunity = self.db_manager.get_opportunity_by_id(opportunity_id)
            if opportunity:
                original_status = opportunity.get("status")
                original_workflow_step = opportunity.get("last_workflow_step")
            
            self.db_manager.update_opportunity_workflow_state(
                opportunity_id, "in_progress", "running"
            )
            self.job_manager.update_job_progress(job_id, "Workflow Started", "Starting full automation workflow.")

# FIND (at the exception handler, around line 95-105):
        except Exception as e:
            error_msg = f"Full auto workflow for {opportunity_id} failed: {e}"
            self.logger.error(f"{error_msg}\n{traceback.format_exc()}")
            # The job's _run_job wrapper will catch this and handle the final 'failed' state.
            raise

# REPLACE WITH:
        except Exception as e:
            error_msg = f"Full auto workflow for {opportunity_id} failed: {e}"
            self.logger.error(f"{error_msg}\n{traceback.format_exc()}")
            
            # Attempt to rollback to previous state
            if original_status and original_workflow_step:
                try:
                    self.logger.info(
                        f"Rolling back opportunity {opportunity_id} to previous state: "
                        f"status={original_status}, step={original_workflow_step}"
                    )
                    self.db_manager.update_opportunity_workflow_state(
                        opportunity_id,
                        original_workflow_step,
                        original_status,
                        error_message=f"Workflow failed and rolled back: {str(e)[:200]}"
                    )
                except Exception as rollback_error:
                    self.logger.error(
                        f"Failed to rollback opportunity {opportunity_id}: {rollback_error}"
                    )
            
            # The job's _run_job wrapper will catch this and handle the final 'failed' state.
            raise
```

---

### Task 19.2: Add Compensating Transactions for Partial Failures
**Priority:** MEDIUM
**File:** `pipeline/orchestrator/content_orchestrator.py`

**Exact Changes:**
```python
# FIND (around line 230-250, in the exception handler):
        except Exception as e:
            error_msg = (
                f"Agentic content generation failed: {e}\n{traceback.format_exc()}"
            )
            self.logger.error(error_msg)
            
            # Cleanup: Remove any temporary files created during generation
            for temp_file in temp_files_to_cleanup:
                try:
                    if os.path.exists(temp_file):
                        os.remove(temp_file)
                        self.logger.info(f"Cleaned up temporary file: {temp_file}")
                except Exception as cleanup_error:
                    self.logger.warning(f"Failed to cleanup {temp_file}: {cleanup_error}")

# REPLACE WITH:
        except Exception as e:
            error_msg = (
                f"Agentic content generation failed: {e}\n{traceback.format_exc()}"
            )
            self.logger.error(error_msg)
            
            # COMPENSATING TRANSACTIONS: Clean up all artifacts from partial execution
            
            # 1. Cleanup temporary files
            for temp_file in temp_files_to_cleanup:
                try:
                    if os.path.exists(temp_file):
                        os.remove(temp_file)
                        self.logger.info(f"Cleaned up temporary file: {temp_file}")
                except Exception as cleanup_error:
                    self.logger.warning(f"Failed to cleanup {temp_file}: {cleanup_error}")
            
            # 2. Clear any partial content that might have been saved
            try:
                # Save an error state to ai_content to indicate failure
                error_content = {
                    "error": str(e)[:500],
                    "failed_at": datetime.now().isoformat(),
                    "article_body_html": None,
                }
                self.db_manager.update_opportunity_ai_content(
                    opportunity_id,
                    error_content,
                    "error_state"
                )
            except Exception as db_error:
                self.logger.error(f"Failed to save error state to database: {db_error}")
            
            # 3. Clear cost tracking for this failed workflow
            workflow_cost_id = f"generation_{opportunity_id}"
            try:
                final_cost = self.cost_tracker.get_workflow_cost(workflow_cost_id)
                self.logger.info(f"Total cost before failure: ${final_cost:.4f}")
                self.cost_tracker.clear_workflow(workflow_cost_id)
            except:
                pass
```

---

## Phase 20: Final Validation and Testing Hooks

### Task 20.1: Add Comprehensive Input Validation for Discovery Request
**Priority:** HIGH
**File:** `api/routers/discovery.py`

**Exact Changes:**
```python
# FIND (line 145-175, start_discovery_run_async endpoint):
@router.post("/clients/{client_id}/discovery-runs-async", response_model=JobResponse)
async def start_discovery_run_async(
    client_id: str,
    request: DiscoveryRunRequest,
    orchestrator: WorkflowOrchestrator = Depends(get_orchestrator),
    discovery_service: DiscoveryService = Depends(get_discovery_service),
):
    if client_id != orchestrator.client_id:
        raise HTTPException(
            status_code=403,
            detail="You do not have permission to access this client's resources.",
        )
    try:
        filters = request.filters
        limit = request.limit or 1000
        discovery_modes = request.discovery_modes
        depth = request.depth

# REPLACE WITH:
@router.post("/clients/{client_id}/discovery-runs-async", response_model=JobResponse)
async def start_discovery_run_async(
    client_id: str,
    request: DiscoveryRunRequest,
    orchestrator: WorkflowOrchestrator = Depends(get_orchestrator),
    discovery_service: DiscoveryService = Depends(get_discovery_service),
):
    if client_id != orchestrator.client_id:
        raise HTTPException(
            status_code=403,
            detail="You do not have permission to access this client's resources.",
        )
    
    # Comprehensive input validation per API constraints
    try:
        # Validate seed keywords
        if not request.seed_keywords or len(request.seed_keywords) == 0:
            raise HTTPException(
                status_code=400,
                detail="At least one seed keyword is required."
            )
        
        # Per API docs: Keyword Ideas max 200 keywords
        if "keyword_ideas" in request.discovery_modes and len(request.seed_keywords) > 200:
            raise HTTPException(
                status_code=400,
                detail=f"Keyword Ideas mode supports max 200 seed keywords. You provided {len(request.seed_keywords)}."
            )
        
        # Validate discovery modes
        valid_modes = {"keyword_ideas", "keyword_suggestions", "related_keywords", "find_questions"}
        invalid_modes = set(request.discovery_modes) - valid_modes
        if invalid_modes:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid discovery modes: {invalid_modes}. Valid modes: {valid_modes}"
            )
        
        # Validate filters count (max 8 per API)
        if request.filters:
            filter_count = sum(1 for f in request.filters if isinstance(f, dict))
            if filter_count > 8:
                raise HTTPException(
                    status_code=400,
                    detail=f"Maximum 8 filters allowed per API request. You provided {filter_count}."
                )
        
        # Validate depth for related keywords
        if request.depth is not None:
            if request.depth < 0 or request.depth > 4:
                raise HTTPException(
                    status_code=400,
                    detail=f"Related keywords depth must be between 0 and 4. You provided {request.depth}."
                )
        
        # Validate limit
        if request.limit is not None:
            if request.limit < 1 or request.limit > 1000:
                raise HTTPException(
                    status_code=400,
                    detail=f"Limit must be between 1 and 1000. You provided {request.limit}."
                )
        
        filters = request.filters
        limit = request.limit or 1000
        discovery_modes = request.discovery_modes
        depth = request.depth
```

---

### Task 20.2: Add API Response Validation Before Processing
**Priority:** HIGH
**File:** `external_apis/dataforseo_client_v2.py`

**Exact Changes:**
```python
# FIND (in post_with_paging, around line 385-395):
        if response and response.get("tasks") and response["tasks"][0].get("result"):
            result_data = response["tasks"][0]["result"][0]
            sanitized_result_data = DataForSEOMapper.sanitize_serp_overview_response(
                result_data
            )  # ADDED SANITIZATION
            return sanitized_result_data, cost

        return None, cost

# This is in get_serp_results method - REPLACE WITH:
        # Validate response structure before processing
        if not response:
            self.logger.error(f"No response received from SERP API for keyword '{keyword}'")
            return None, cost
        
        if not isinstance(response, dict):
            self.logger.error(f"SERP API response is not a dictionary: {type(response)}")
            return None, cost
        
        if response.get("status_code") != 20000:
            self.logger.error(
                f"SERP API returned error status: {response.get('status_code')} - {response.get('status_message')}"
            )
            return None, cost
        
        tasks = response.get("tasks")
        if not tasks or not isinstance(tasks, list) or len(tasks) == 0:
            self.logger.error("SERP API response contains no tasks")
            return None, cost
        
        first_task = tasks[0]
        if first_task.get("status_code") != 20000:
            self.logger.error(
                f"SERP task failed: {first_task.get('status_code')} - {first_task.get('status_message')}"
            )
            return None, cost
        
        result = first_task.get("result")
        if not result or not isinstance(result, list) or len(result) == 0:
            self.logger.error("SERP task contains no result data")
            return None, cost
        
        result_data = result[0]
        if not isinstance(result_data, dict):
            self.logger.error(f"SERP result data is not a dictionary: {type(result_data)}")
            return None, cost
        
        # Apply sanitization
        sanitized_result_data = DataForSEOMapper.sanitize_serp_overview_response(result_data)
        return sanitized_result_data, cost
```

---

## Phase 21: Documentation and Error Messages

### Task 21.1: Add Detailed Error Messages for Common Failures
**Priority:** MEDIUM
**File:** `external_apis/dataforseo_client_v2.py`

**Exact Changes:**
```python
# ADD NEW METHOD in DataForSEOClientV2 class:

    def _get_friendly_error_message(self, status_code: int, status_message: str) -> str:
        """
        Converts DataForSEO API error codes to user-friendly messages.
        
        Common error codes:
        - 40101: Authentication failed
        - 40102: Not enough credits
        - 40103: Invalid API endpoint
        - 40501: Duplicate crawl host (OnPage API)
        - 50000: Internal server error
        """
        error_map = {
            40101: "Authentication failed. Please check your DataForSEO credentials in settings.",
            40102: "Insufficient API credits. Please add credits to your DataForSEO account.",
            40103: "Invalid API endpoint. This may indicate a bug in the integration.",
            40104: "Invalid parameters sent to API. Check your filter and sorting settings.",
            40501: "Duplicate crawl host detected. Cannot crawl the same domain multiple times in one request.",
            50000: "DataForSEO internal server error. Please try again later.",
            50001: "DataForSEO service temporarily unavailable. Please try again later.",
        }
        
        friendly_message = error_map.get(status_code, status_message)
        
        return f"API Error ({status_code}): {friendly_message}"

# THEN UPDATE error logging to use this:
# FIND (in _post_request, around line 95-100):
                if response_json.get("status_code") != 20000:
                    self.logger.error(
                        f"DataForSEO API returned non-20000 status_code: {response_json.get('status_code')} - {response_json.get('status_message')}"
                    )

# REPLACE WITH:
                if response_json.get("status_code") != 20000:
                    friendly_error = self._get_friendly_error_message(
                        response_json.get("status_code"),
                        response_json.get("status_message", "Unknown error")
                    )
                    self.logger.error(friendly_error)
                    
                    # For auth and credit errors, don't retry
                    if response_json.get("status_code") in [40101, 40102, 40103]:
                        return None, 0.0
```

---

## Phase 22: Final Code Cleanup and Optimization

### Task 22.1: Remove Redundant Code in String Concatenation
**Priority:** LOW
**File:** `agents/content_auditor.py`

**Exact Changes:**
```python
# This was mentioned as issue #34 but the code shown doesn't exist in content_auditor.py
# The issue is actually in content_orchestrator.py

# File: pipeline/orchestrator/content_orchestrator.py
# FIND (around line 100):
                    full_article_context_for_conclusion += (
                        f"<h2>{node['title']}</h2>\n{content_html}\n"
                    )

# REPLACE WITH (using list accumulation):
# First, at the start of the method, add:
            full_article_parts = []  # Use list accumulation for efficiency

# Then replace the accumulation:
                    full_article_parts.append(f"<h2>{node['title']}</h2>\n{content_html}\n")

# And before generating conclusion:
# FIND:
                elif node["type"] == "conclusion":
                    content_html, cost = sectional_generator.generate_conclusion(
                        opportunity, full_article_context_for_conclusion
                    )

# REPLACE WITH:
                elif node["type"] == "conclusion":
                    # Join accumulated parts efficiently
                    full_article_context_for_conclusion = "".join(full_article_parts)
                    content_html, cost = sectional_generator.generate_conclusion(
                        opportunity, full_article_context_for_conclusion
                    )
```

---

### Task 22.2: Add Missing Error Field Validation
**Priority:** LOW
**File:** `data_access/database_manager.py`

**Exact Changes:**
```python
# FIND (in _deserialize_rows, around line 200-250):
            if "blueprint_data" in final_item:
                final_item["blueprint"] = final_item.pop("blueprint_data")
            if "ai_content_json" in final_item:
                final_item["ai_content"] = final_item.pop("ai_content_json")

            results.append(final_item)
        return results

# ADD BEFORE appending to results:
            # Ensure error_message field exists and is properly typed
            if "error_message" in final_item:
                if final_item["error_message"] is not None and not isinstance(final_item["error_message"], str):
                    self.logger.warning(
                        f"error_message for opportunity {final_item.get('id')} is not a string: {type(final_item['error_message'])}"
                    )
                    final_item["error_message"] = str(final_item["error_message"])
            
            # Rename legacy fields for consistency
            if "blueprint_data" in final_item:
                final_item["blueprint"] = final_item.pop("blueprint_data")
            if "ai_content_json" in final_item:
                final_item["ai_content"] = final_item.pop("ai_content_json")

            results.append(final_item)
        return results
```

---

## Phase 23: Create Comprehensive Test Suite

### Task 23.1: Add Unit Tests for DataForSEO Response Sanitization
**Priority:** MEDIUM
**File:** Create new file `tests/test_dataforseo_sanitization.py`

**Exact Changes:**
```python
# CREATE NEW FILE: backend/tests/test_dataforseo_sanitization.py

import pytest
import json
from backend.data_mappers.dataforseo_mapper import DataForSEOMapper


class TestDataForSEOSanitization:
    """Test suite for DataForSEO API response sanitization."""
    
    def test_se_results_count_string_to_int_conversion(self):
        """
        Test that se_results_count is converted from string to int.
        Per API docs: Keyword Ideas/Suggestions return this as string.
        """
        serp_info = {
            "se_type": "google",
            "se_results_count": "19880000000",  # String from API
            "serp_item_types": ["organic"],
            "last_updated_time": "2024-07-15 00:43:34 +00:00"
        }
        
        sanitized = DataForSEOMapper._sanitize_serp_info(serp_info)
        
        assert isinstance(sanitized["se_results_count"], int)
        assert sanitized["se_results_count"] == 19880000000
    
    def test_se_results_count_already_int(self):
        """Test that integer se_results_count is preserved."""
        serp_info = {
            "se_type": "google",
            "se_results_count": 115000000,  # Already int (Related Keywords)
            "serp_item_types": ["organic"]
        }
        
        sanitized = DataForSEOMapper._sanitize_serp_info(serp_info)
        
        assert isinstance(sanitized["se_results_count"], int)
        assert sanitized["se_results_count"] == 115000000
    
    def test_se_results_count_invalid_string(self):
        """Test handling of non-numeric