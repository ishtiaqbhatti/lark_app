# 🔍 Complete Code Audit & Optimization Plan

## 📋 Issues Found

### **Critical Issues (Must Fix)**

1. **Filter Structure Mismatch** - Frontend sends structured filters, backend expects flat list
2. **8-Filter Limit Not Enforced** - Backend has safeguard but frontend allows more
3. **Negative Keywords Creates Invalid Filters** - Adds extra "and" operators incorrectly
4. **Missing Error Boundaries** - Frontend crashes propagate to user
5. **No Transaction Management** - Database operations aren't atomic
6. **Filter Sanitization Too Late** - Happens after conversion, should be before
7. **CPC Filter Missing from Available Filters** - Frontend can't select it
8. **Backlinks/Referring Domains Missing** - Not exposed in filter builder
9. **Discovery Modes Not Validated** - Empty array causes silent failures

### **High Priority Issues**

10. **No Rate Limiting** - API can be overwhelmed
11. **Inefficient Deduplication** - O(n²) complexity in keyword processing
12. **Missing Database Indexes** - Slow queries on large datasets
13. **No Caching Strategy** - Repeated calls to expensive endpoints
14. **Cost Tracking Inaccurate** - Multiple API calls not summed correctly
15. **Regex Not Validated** - Can cause catastrophic backtracking
16. **CORS Too Permissive** - Security risk
17. **No Input Sanitization** - XSS and injection risks

### **Medium Priority Issues**

18. **Inconsistent Error Handling** - Some places return None, others raise
19. **Missing Loading States** - Poor UX during long operations
20. **No Retry Logic** - Transient failures aren't handled
21. **Pagination Incomplete** - offset_token not properly utilized
22. **Form Validation Incomplete** - Can submit invalid data
23. **Modal State Management** - Multiple modals create state bugs
24. **API Client Error Parsing** - Doesn't extract all error details
25. **No Logging Levels** - Everything logs at same level

### **Low Priority Issues (Nice to Have)**

26. **Missing TypeScript** - No type safety in frontend
27. **No Unit Tests** - Zero test coverage
28. **Unused Imports** - Code bloat
29. **Inconsistent Naming** - snake_case vs camelCase mixing
30. **Missing Docstrings** - Hard to maintain
31. **No Code Splitting** - Large bundle size
32. **Legend Truncation** - Long text not handled well
33. **Date Formatting** - Inconsistent across components

---

# 🎯 Step-by-Step Implementation Plan for AI Agent

## Phase 1: Critical Fixes (Do First)

### **Step 1.1: Fix Filter Structure Mismatch**

**File: `backend/api/routers/discovery.py`**

```python
# CURRENT PROBLEM: 
# Frontend sends: [{ field: 'keyword_info.search_volume', operator: '>', value: 500 }]
# Backend expects: [['keyword_info.search_volume', '>', 500], 'and', ...]

# ADD THIS HELPER FUNCTION AT TOP OF FILE:
def convert_frontend_filters_to_api_format(frontend_filters: List[Dict[str, Any]]) -> List[Any]:
    """
    Converts structured frontend filters to DataForSEO API format.
    
    Frontend format: [{ field: 'path.to.field', operator: '>', value: 123 }]
    API format: [['path.to.field', '>', 123], 'and', ['next.field', '<', 456]]
    """
    if not frontend_filters or len(frontend_filters) == 0:
        return None
    
    api_filters = []
    for i, f in enumerate(frontend_filters):
        # Validate required fields
        if not all(k in f for k in ['field', 'operator', 'value']):
            logger.warning(f"Skipping invalid filter: {f}")
            continue
        
        # Handle 'in' operator specially
        if f['operator'] == 'in' and isinstance(f['value'], list):
            api_filters.append([f['field'], 'in', f['value']])
        else:
            api_filters.append([f['field'], f['operator'], f['value']])
        
        # Add 'and' between conditions (not after last one)
        if i < len(frontend_filters) - 1:
            api_filters.append('and')
    
    return api_filters if api_filters else None

# UPDATE THE ENDPOINT:
@router.post("/clients/{client_id}/discovery-runs-async", response_model=JobResponse)
async def start_discovery_run_async(
    client_id: str,
    request: DiscoveryRunRequest,
    orchestrator: WorkflowOrchestrator = Depends(get_orchestrator),
    discovery_service: DiscoveryService = Depends(get_discovery_service),
):
    # ... existing validation ...
    
    # CONVERT FILTERS FIRST:
    filters = request.filters
    if filters and len(filters) > 8:
        raise HTTPException(
            status_code=400,
            detail="Maximum 8 filter conditions allowed. Please reduce filters."
        )
    
    # Convert to API format
    api_filters = convert_frontend_filters_to_api_format(filters)
    
    parameters = {
        "seed_keywords": request.seed_keywords,
        "negative_keywords": request.negative_keywords,
        "discovery_modes": discovery_modes,
        "filters": api_filters,  # USE CONVERTED FILTERS
        # ... rest of parameters
    }
    
    # ... rest of function
```

---

### **Step 1.2: Enforce 8-Filter Maximum (Frontend)**

**File: `client/my-content-app/src/pages/DiscoveryPage/components/FilterBuilder.jsx`**

```javascript
// UPDATE THE FilterBuilder COMPONENT:

const FilterBuilder = ({ value = [], onChange, availableFilters }) => {
  const filters = value;
  const MAX_FILTERS = 8;

  const triggerChange = (newFilters) => {
    onChange?.(newFilters);
  };

  const addFilter = () => {
    if (filters.length >= MAX_FILTERS) {
      // DON'T ADD - already at max
      return;
    }
    const newFilters = [...filters, { field: null, operator: null, value: null }];
    triggerChange(newFilters);
  };

  // ... rest of component ...

  return (
    <div>
      {filters.length >= MAX_FILTERS && (
        <Alert
          message="Maximum Filters Reached"
          description="You've reached the maximum of 8 filter conditions. Remove a filter to add a new one."
          type="warning"
          showIcon
          style={{ marginBottom: 16 }}
        />
      )}
      
      {filters.map((filter, index) => (
        // ... existing filter rows ...
      ))}
      
      <Button 
        type="dashed" 
        onClick={addFilter} 
        icon={<PlusOutlined />} 
        disabled={filters.length >= MAX_FILTERS}
        block
      >
        Add Filter ({filters.length}/{MAX_FILTERS})
      </Button>
    </div>
  );
};
```

---

### **Step 1.3: Fix Negative Keywords Filter Injection**

**File: `backend/api/routers/discovery.py`**

```python
@router.post("/clients/{client_id}/discovery-runs-async", response_model=JobResponse)
async def start_discovery_run_async(
    client_id: str,
    request: DiscoveryRunRequest,
    # ... dependencies ...
):
    # ... existing code ...
    
    # CONVERT FILTERS FIRST:
    api_filters = convert_frontend_filters_to_api_format(request.filters)
    
    # NOW INJECT NEGATIVE KEYWORDS CORRECTLY:
    if request.negative_keywords:
        # If we have existing filters, we need to combine them
        if api_filters:
            # api_filters is already in correct format: [['field', 'op', 'val'], 'and', ...]
            # Just append to it
            for neg_kw in request.negative_keywords:
                api_filters.append('and')  # Add operator before new filter
                api_filters.append(['keyword', 'not_match', neg_kw.strip()])
        else:
            # No existing filters, create new list
            api_filters = []
            for i, neg_kw in enumerate(request.negative_keywords):
                api_filters.append(['keyword', 'not_match', neg_kw.strip()])
                if i < len(request.negative_keywords) - 1:
                    api_filters.append('and')
    
    # NOW CREATE STRUCTURED FILTERS FOR DIFFERENT MODES:
    structured_filters = {
        "ideas": api_filters.copy() if api_filters else None,
        "suggestions": api_filters.copy() if api_filters else None,
        "related": None  # Will be converted later
    }
    
    # Convert for related_keywords (needs keyword_data. prefix)
    if api_filters:
        related_filters = []
        for item in api_filters:
            if isinstance(item, list):
                # This is a filter condition
                field = item[0]
                # Add prefix if not already present and not 'keyword' field
                if not field.startswith('keyword_data.') and field != 'keyword':
                    field = f'keyword_data.{field}'
                related_filters.append([field, item[1], item[2]])
            else:
                # This is an operator
                related_filters.append(item)
        structured_filters["related"] = related_filters
    
    parameters = {
        "seed_keywords": request.seed_keywords,
        "negative_keywords": request.negative_keywords,
        "discovery_modes": discovery_modes,
        "filters": structured_filters,  # USE STRUCTURED FORMAT
        # ... rest
    }
```

---

### **Step 1.4: Add Error Boundaries (Frontend)**

**File: `client/my-content-app/src/components/ErrorBoundary.jsx` (NEW FILE)**

```javascript
import React from 'react';
import { Result, Button } from 'antd';

class ErrorBoundary extends React.Component {
  constructor(props) {
    super(props);
    this.state = { hasError: false, error: null, errorInfo: null };
  }

  static getDerivedStateFromError(error) {
    return { hasError: true };
  }

  componentDidCatch(error, errorInfo) {
    console.error('ErrorBoundary caught an error:', error, errorInfo);
    this.setState({ error, errorInfo });
  }

  handleReset = () => {
    this.setState({ hasError: false, error: null, errorInfo: null });
    window.location.reload();
  };

  render() {
    if (this.state.hasError) {
      return (
        <div style={{ padding: '50px' }}>
          <Result
            status="error"
            title="Something went wrong"
            subTitle="We're sorry, but something unexpected happened. Please try refreshing the page."
            extra={[
              <Button type="primary" key="reload" onClick={this.handleReset}>
                Reload Page
              </Button>,
            ]}
          >
            {process.env.NODE_ENV === 'development' && (
              <div style={{ marginTop: 16, textAlign: 'left' }}>
                <details style={{ whiteSpace: 'pre-wrap' }}>
                  <summary>Error Details (Development Only)</summary>
                  {this.state.error && this.state.error.toString()}
                  <br />
                  {this.state.errorInfo && this.state.errorInfo.componentStack}
                </details>
              </div>
            )}
          </Result>
        </div>
      );
    }

    return this.props.children;
  }
}

export default ErrorBoundary;
```

**File: `client/my-content-app/src/App.jsx` (UPDATE)**

```javascript
import ErrorBoundary from './components/ErrorBoundary';

function App() {
  return (
    <ErrorBoundary>
      {/* ... existing app content ... */}
    </ErrorBoundary>
  );
}
```

---

### **Step 1.5: Add Transaction Management (Backend)**

**File: `backend/api/routers/discovery.py`**

```python
from sqlalchemy.exc import SQLAlchemyError

@router.post("/clients/{client_id}/discovery-runs-async", response_model=JobResponse)
async def start_discovery_run_async(
    client_id: str,
    request: DiscoveryRunRequest,
    orchestrator: WorkflowOrchestrator = Depends(get_orchestrator),
    discovery_service: DiscoveryService = Depends(get_discovery_service),
):
    if client_id != orchestrator.client_id:
        raise HTTPException(status_code=403, detail="Permission denied")
    
    try:
        # ... prepare parameters ...
        
        # USE TRANSACTION:
        try:
            run_id = discovery_service.create_discovery_run(
                client_id=client_id, 
                parameters=parameters
            )
            
            job_id = orchestrator.run_discovery_and_save(
                run_id,
                request.seed_keywords,
                discovery_modes,
                # ... rest of params
            )
            
            # Commit happens automatically if no exception
            return {"job_id": job_id, "message": f"Discovery run job {job_id} started."}
            
        except SQLAlchemyError as db_error:
            # Rollback happens automatically
            logger.error(f"Database error: {db_error}", exc_info=True)
            raise HTTPException(
                status_code=500, 
                detail="Failed to create discovery run due to database error."
            )
    
    except ValueError as ve:
        logger.error(f"Validation error: {ve}", exc_info=True)
        raise HTTPException(status_code=400, detail=str(ve))
    
    except Exception as e:
        logger.error(f"Unexpected error: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Failed to start discovery run: {str(e)}")
```

---

### **Step 1.6: Move Filter Sanitization Earlier**

**File: `backend/external_apis/dataforseo_client_v2.py`**

```python
def get_keyword_ideas(
    self,
    seed_keywords: List[str],
    location_code: int,
    language_code: str,
    client_cfg: Dict[str, Any],
    discovery_modes: List[str],
    filters: Dict[str, Any],  # ALREADY STRUCTURED
    order_by: Optional[Dict[str, List[str]]],
    limit: Optional[int] = None,
    depth: Optional[int] = None,
    ignore_synonyms_override: Optional[bool] = None,
    include_clickstream_override: Optional[bool] = None,
    closely_variants_override: Optional[bool] = None,
    exact_match_override: Optional[bool] = None,
) -> Tuple[List[Dict[str, Any]], float]:
    """
    Performs comprehensive discovery burst.
    """
    all_items = []
    total_cost = 0.0

    # SANITIZE FILTERS IMMEDIATELY:
    from pipeline.step_01_discovery.keyword_discovery.filters import sanitize_filters_for_api
    
    sanitized_filters = {}
    if filters:
        for mode, mode_filters in filters.items():
            if mode_filters:
                # SANITIZE BEFORE PRIORITY/LIMIT:
                clean_filters = sanitize_filters_for_api(mode_filters)
                # THEN PRIORITIZE/LIMIT:
                limited_filters = self._prioritize_and_limit_filters(clean_filters)
                sanitized_filters[mode] = limited_filters
            else:
                sanitized_filters[mode] = None
    else:
        sanitized_filters = {"ideas": None, "suggestions": None, "related": None}

    # ... rest of function uses sanitized_filters ...
```

---

### **Step 1.7: Add Missing Filters to Frontend**

**File: `backend/api/routers/discovery.py`**

```python
@router.get("/discovery/available-filters")
async def get_available_filters():
    """
    Returns all available filters for the frontend.
    """
    base_filters = [
        {
            "name": "search_volume",
            "label": "Search Volume",
            "type": "number",
            "operators": [">", "<", "=", ">=", "<="],
        },
        {
            "name": "keyword_difficulty",
            "label": "Keyword Difficulty",
            "type": "number",
            "operators": [">", "<", "=", ">=", "<="],
        },
        {
            "name": "main_intent",
            "label": "Search Intent",
            "type": "select",
            "options": ["informational", "navigational", "commercial", "transactional"],
            "operators": ["=", "in"],
        },
        {
            "name": "competition_level",
            "label": "Competition Level",
            "type": "select",
            "options": ["LOW", "MEDIUM", "HIGH"],
            "operators": ["=", "in"],
        },
        {
            "name": "cpc",
            "label": "CPC (Cost Per Click)",
            "type": "number",
            "operators": [">", "<", "=", ">=", "<="],
        },
        {
            "name": "competition",
            "label": "Competition Score",
            "type": "number",
            "operators": [">", "<", "=", ">=", "<="],
        },
        # ADD THESE:
        {
            "name": "backlinks",
            "label": "Average Backlinks (Top 10)",
            "type": "number",
            "operators": [">", "<", "=", ">=", "<="],
        },
        {
            "name": "referring_domains",
            "label": "Referring Domains (Top 10)",
            "type": "number",
            "operators": [">", "<", "=", ">=", "<="],
        },
    ]

    def construct_paths(prefix, items):
        new_items = []
        for item in items:
            new_item = item.copy()
            base_name = new_item["name"]
            
            # MAP TO CORRECT PATHS:
            if base_name == "search_volume":
                new_item["name"] = f"{prefix}keyword_info.search_volume"
            elif base_name == "keyword_difficulty":
                new_item["name"] = f"{prefix}keyword_properties.keyword_difficulty"
            elif base_name == "main_intent":
                new_item["name"] = f"{prefix}search_intent_info.main_intent"
            elif base_name == "competition_level":
                new_item["name"] = f"{prefix}keyword_info.competition_level"
            elif base_name == "cpc":
                new_item["name"] = f"{prefix}keyword_info.cpc"
            elif base_name == "competition":
                new_item["name"] = f"{prefix}keyword_info.competition"
            elif base_name == "backlinks":
                new_item["name"] = f"{prefix}avg_backlinks_info.backlinks"
            elif base_name == "referring_domains":
                new_item["name"] = f"{prefix}avg_backlinks_info.referring_domains"
            
            new_items.append(new_item)
        return new_items

    return [
        {
            "id": "keyword_ideas",
            "name": "Broad Market Research",
            "description": "Wide range of keyword ideas related to your topic.",
            "filters": construct_paths("", base_filters),
            "sorting": [{"name": "relevance", "label": "Relevance"}]
            + construct_paths("", base_sorting),
            "defaults": {
                "filters": [
                    {"field": "keyword_info.search_volume", "operator": ">=", "value": 500},
                    {"field": "keyword_info.search_volume", "operator": "<=", "value": 50000},
                    {"field": "keyword_properties.keyword_difficulty", "operator": "<=", "value": 40},
                    {"field": "keyword_info.competition_level", "operator": "in", "value": ["LOW", "MEDIUM"]},
                    {"field": "search_intent_info.main_intent", "operator": "=", "value": "informational"},
                    {"field": "avg_backlinks_info.backlinks", "operator": "<=", "value": 100},
                    {"field": "avg_backlinks_info.referring_domains", "operator": "<=", "value": 50},
                    {"field": "keyword_info.cpc", "operator": ">=", "value": 0.30},
                ],
                "order_by": ["keyword_info.search_volume,desc"],
            },
        },
        # ... other modes ...
    ]
```

---

### **Step 1.8: Validate Discovery Modes**

**File: `backend/api/routers/discovery.py`**

```python
@router.post("/clients/{client_id}/discovery-runs-async", response_model=JobResponse)
async def start_discovery_run_async(
    client_id: str,
    request: DiscoveryRunRequest,
    # ... dependencies ...
):
    # ADD VALIDATION:
    discovery_modes = request.discovery_modes
    
    if not discovery_modes or len(discovery_modes) == 0:
        raise HTTPException(
            status_code=400,
            detail="At least one discovery mode must be selected."
        )
    
    valid_modes = ["keyword_ideas", "keyword_suggestions", "related_keywords"]
    invalid_modes = [m for m in discovery_modes if m not in valid_modes]
    
    if invalid_modes:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid discovery modes: {', '.join(invalid_modes)}. "
                   f"Valid modes are: {', '.join(valid_modes)}"
        )
    
    # ... rest of function ...
```

---

### **Step 1.9: Add Optimal Preset to Frontend**

**File: `client/my-content-app/src/pages/DiscoveryPage/components/DiscoveryForm.jsx`**

```javascript
const goalPresets = [
  {
    key: 'optimal_easy_rank',
    label: '🎯 Optimal: Easy to Rank + Good Traffic',
    description: 'Scientifically optimized for blog content. Balances traffic potential with ranking feasibility using 8 proven filters.',
    filters: [
      { field: 'keyword_info.search_volume', operator: '>=', value: 500 },
      { field: 'keyword_info.search_volume', operator: '<=', value: 50000 },
      { field: 'keyword_properties.keyword_difficulty', operator: '<=', value: 40 },
      { field: 'keyword_info.competition_level', operator: 'in', value: ['LOW', 'MEDIUM'] },
      { field: 'search_intent_info.main_intent', operator: '=', value: 'informational' },
      { field: 'avg_backlinks_info.backlinks', operator: '<=', value: 100 },
      { field: 'avg_backlinks_info.referring_domains', operator: '<=', value: 50 },
      { field: 'keyword_info.cpc', operator: '>=', value: 0.30 },
    ],
  },
  {
    key: 'quick_wins',
    label: '🍎 Quick Wins (Ultra Easy)',
    description: 'Very low competition keywords you can rank for quickly.',
    filters: [
      { field: 'keyword_properties.keyword_difficulty', operator: '<=', value: 20 },
      { field: 'keyword_info.search_volume', operator: '>=', value: 200 },
      { field: 'keyword_info.competition_level', operator: '=', value: 'LOW' },
      { field: 'search_intent_info.main_intent', operator: 'in', value: ['informational', 'commercial'] },
      { field: 'keyword_info.cpc', operator: '>=', value: 0.10 },
    ],
  },
  {
    key: 'high_traffic',
    label: '📈 High-Volume Content',
    description: 'Target high search volume informational keywords.',
    filters: [
      { field: 'keyword_info.search_volume', operator: '>=', value: 2000 },
      { field: 'search_intent_info.main_intent', operator: '=', value: 'informational' },
      { field: 'keyword_properties.keyword_difficulty', operator: '<=', value: 50 },
      { field: 'keyword_info.competition_level', operator: 'in', value: ['LOW', 'MEDIUM'] },
    ],
  },
  {
    key: 'commercial_value',
    label: '💰 High Commercial Value',
    description: 'Keywords with strong monetization potential.',
    filters: [
      { field: 'search_intent_info.main_intent', operator: 'in', value: ['commercial', 'transactional'] },
      { field: 'keyword_info.cpc', operator: '>=', value: 2.00 },
      { field: 'keyword_info.competition', operator: '>=', value: 0.6 },
      { field: 'keyword_properties.keyword_difficulty', operator: '<=', value: 60 },
      { field: 'keyword_info.search_volume', operator: '>=', value: 500 },
    ],
  },
  {
    key: 'niche_topics',
    label: '🎣 Underserved Niches',
    description: 'Low competition, specific topics with dedicated audiences.',
    filters: [
      { field: 'keyword_properties.keyword_difficulty', operator: '<=', value: 15 },
      { field: 'keyword_info.search_volume', operator: '>=', value: 50 },
      { field: 'keyword_info.search_volume', operator: '<=', value: 500 },
      { field: 'keyword_info.competition_level', operator: '=', value: 'LOW' },
    ],
  },
];

// UPDATE DEFAULT:
initialValues={{
  limit: 1000,
  goal: 'optimal_easy_rank', // CHANGED
  filters: goalPresets.find(p => p.key === 'optimal_easy_rank').filters,
  discovery_modes: ['keyword_ideas', 'keyword_suggestions', 'related_keywords'],
  depth: 3,
  discovery_max_pages: 1,
}}
```

---

## Phase 2: High Priority Fixes

### **Step 2.1: Add Rate Limiting**

**File: `backend/main.py` (or create `backend/middleware/rate_limiter.py`)**

```python
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# ADD TO REQUIREMENTS.TXT:
# slowapi==0.1.9
```

**File: `backend/api/routers/discovery.py`**

```python
from slowapi import Limiter
from fastapi import Request

limiter = Limiter(key_func=lambda request: request.state.client_id)

@router.post("/clients/{client_id}/discovery-runs-async", response_model=JobResponse)
@limiter.limit("10/minute")  # MAX 10 DISCOVERY RUNS PER MINUTE
async def start_discovery_run_async(
    request: Request,  # ADD THIS
    client_id: str,
    discovery_request: DiscoveryRunRequest,  # RENAMED TO AVOID CONFLICT
    # ... rest ...
):
    request.state.client_id = client_id  # SET FOR RATE LIMITING
    # ... rest of function ...
```

---

### **Step 2.2: Optimize Deduplication**

**File: `backend/pipeline/step_01_discovery/keyword_expander.py`**

```python
def expand_seed_keyword(
    self,
    seed_keywords: List[str],
    discovery_modes: List[str],
    filters: Optional[List[Any]],
    order_by: Optional[List[str]],
    existing_keywords: set,
    limit: Optional[int] = None,
    depth: Optional[int] = None,
    ignore_synonyms: Optional[bool] = False,
) -> Dict[str, Any]:
    """
    Efficient keyword expansion with O(1) deduplication.
    """
    self.logger.info(f"Starting expansion with {len(seed_keywords)} seeds")

    # ... prepare filters ...

    results = self.expander.expand(
        seed_keywords,
        discovery_modes,
        structured_filters,
        structured_orderby,
        existing_keywords,
        limit,
        depth,
        ignore_synonyms,
    )

    # EFFICIENT DEDUPLICATION USING SET:
    final_keywords_deduplicated = []
    seen_keywords = set(existing_keywords)  # Start with existing
    
    raw_counts = {"keyword_ideas": 0, "suggestions": 0, "related": 0}
    
    for item in results.get("final_keywords", []):
        kw_text = item.get("keyword", "").lower()
        
        # O(1) LOOKUP:
        if kw_text and kw_text not in seen_keywords:
            final_keywords_deduplicated.append(item)
            seen_keywords.add(kw_text)  # O(1) INSERT
            
            source = item.get("discovery_source")
            if source in raw_counts:
                raw_counts[source

```python
                raw_counts[source] += 1

    self.logger.info(
        f"Deduplication complete. {len(final_keywords_deduplicated)} unique keywords from {len(results.get('final_keywords', []))} total."
    )

    return {
        **results,
        "total_unique_count": len(final_keywords_deduplicated),
        "final_keywords": final_keywords_deduplicated,
        "raw_counts": raw_counts,
    }
```

---

### **Step 2.3: Add Database Indexes**

**File: `backend/alembic/versions/add_performance_indexes.py` (NEW MIGRATION)**

```python
"""Add performance indexes for discovery queries

Revision ID: performance_indexes_001
Revises: previous_migration_id
Create Date: 2024-01-XX XX:XX:XX.XXXXXX

"""
from alembic import op
import sqlalchemy as sa

revision = 'performance_indexes_001'
down_revision = 'previous_migration_id'  # UPDATE THIS
branch_labels = None
depends_on = None

def upgrade():
    # Index on search_history for client queries
    op.create_index(
        'idx_search_history_client_created',
        'search_history',
        ['client_id', 'created_at'],
        postgresql_using='btree'
    )
    
    # Index on keyword_results for search_id lookups
    op.create_index(
        'idx_keyword_results_search_id',
        'keyword_results',
        ['search_id'],
        postgresql_using='btree'
    )
    
    # Index on keyword_results for keyword lookups (deduplication)
    op.create_index(
        'idx_keyword_results_keyword_lower',
        'keyword_results',
        [sa.text('LOWER(keyword)')],
        postgresql_using='btree'
    )
    
    # Composite index for status filtering
    op.create_index(
        'idx_keyword_results_search_status',
        'keyword_results',
        ['search_id', 'blog_qualification_status'],
        postgresql_using='btree'
    )
    
    # Index for opportunity score sorting
    op.create_index(
        'idx_keyword_results_opp_score',
        'keyword_results',
        ['opportunity_score'],
        postgresql_using='btree'
    )

def downgrade():
    op.drop_index('idx_search_history_client_created', table_name='search_history')
    op.drop_index('idx_keyword_results_search_id', table_name='keyword_results')
    op.drop_index('idx_keyword_results_keyword_lower', table_name='keyword_results')
    op.drop_index('idx_keyword_results_search_status', table_name='keyword_results')
    op.drop_index('idx_keyword_results_opp_score', table_name='keyword_results')
```

**Run migration:**
```bash
alembic upgrade head
```

---

### **Step 2.4: Implement Caching Strategy**

**File: `backend/data_access/database_manager.py`**

```python
import hashlib
import json
from typing import Optional, Dict, Any
from datetime import datetime, timedelta

class DatabaseManager:
    # ... existing code ...
    
    def get_api_cache(self, cache_key: str, ttl_seconds: int = 3600) -> Optional[Dict[str, Any]]:
        """
        Retrieves cached API response if still valid.
        
        Args:
            cache_key: MD5 hash of the request
            ttl_seconds: Time-to-live in seconds
        
        Returns:
            Cached response or None if expired/not found
        """
        try:
            query = """
                SELECT response_data, created_at 
                FROM api_cache 
                WHERE cache_key = ? 
                LIMIT 1
            """
            result = self.conn.execute(query, (cache_key,)).fetchone()
            
            if not result:
                return None
            
            response_data, created_at = result
            created_datetime = datetime.fromisoformat(created_at)
            
            # Check if expired
            if datetime.utcnow() - created_datetime > timedelta(seconds=ttl_seconds):
                self.logger.debug(f"Cache expired for key {cache_key[:8]}...")
                return None
            
            self.logger.info(f"Cache HIT for key {cache_key[:8]}...")
            return json.loads(response_data)
            
        except Exception as e:
            self.logger.error(f"Cache retrieval error: {e}")
            return None
    
    def set_api_cache(self, cache_key: str, response_data: Dict[str, Any]) -> None:
        """
        Stores API response in cache.
        """
        try:
            query = """
                INSERT INTO api_cache (cache_key, response_data, created_at)
                VALUES (?, ?, ?)
                ON CONFLICT(cache_key) DO UPDATE SET
                    response_data = excluded.response_data,
                    created_at = excluded.created_at
            """
            self.conn.execute(
                query, 
                (cache_key, json.dumps(response_data), datetime.utcnow().isoformat())
            )
            self.conn.commit()
            self.logger.debug(f"Cached response for key {cache_key[:8]}...")
        except Exception as e:
            self.logger.error(f"Cache storage error: {e}")
```

**File: `backend/alembic/versions/add_api_cache_table.py` (NEW MIGRATION)**

```python
"""Add API cache table

Revision ID: api_cache_001
Revises: performance_indexes_001
Create Date: 2024-01-XX XX:XX:XX.XXXXXX

"""
from alembic import op
import sqlalchemy as sa

revision = 'api_cache_001'
down_revision = 'performance_indexes_001'
branch_labels = None
depends_on = None

def upgrade():
    op.create_table(
        'api_cache',
        sa.Column('cache_key', sa.String(32), primary_key=True),
        sa.Column('response_data', sa.Text, nullable=False),
        sa.Column('created_at', sa.DateTime, nullable=False, server_default=sa.func.now()),
        sa.Column('endpoint', sa.String(255), nullable=True),  # For debugging
    )
    
    # Index for cleanup of old cache entries
    op.create_index(
        'idx_api_cache_created',
        'api_cache',
        ['created_at'],
        postgresql_using='btree'
    )

def downgrade():
    op.drop_index('idx_api_cache_created', table_name='api_cache')
    op.drop_table('api_cache')
```

---

### **Step 2.5: Fix Cost Tracking**

**File: `backend/pipeline/step_01_discovery/run_discovery.py`**

```python
def run_discovery_phase(
    seed_keywords: List[str],
    dataforseo_client: DataForSEOClientV2,
    db_manager: "DatabaseManager",
    client_id: str,
    client_cfg: Dict[str, Any],
    discovery_modes: List[str],
    filters: Optional[List[Any]],
    order_by: Optional[List[str]],
    limit: Optional[int] = None,
    depth: Optional[int] = None,
    ignore_synonyms: Optional[bool] = False,
    include_clickstream_data: Optional[bool] = None,
    closely_variants: Optional[bool] = None,
    negative_keywords: Optional[List[str]] = None,
    run_logger: Optional[logging.Logger] = None,
) -> Dict[str, Any]:
    logger = run_logger or logging.getLogger(__name__)
    logger.info("--- Starting Discovery Phase ---")

    # INITIALIZE COST TRACKER:
    total_api_cost = 0.0
    cost_breakdown = {
        "keyword_ideas": 0.0,
        "keyword_suggestions": 0.0,
        "related_keywords": 0.0,
    }

    expander = KeywordExpander(dataforseo_client, client_cfg, logger)
    cannibalization_checker = CannibalizationChecker(
        client_cfg.get("target_domain"), dataforseo_client, client_cfg, db_manager
    )
    scoring_engine = ScoringEngine(client_cfg)

    existing_keywords = set(db_manager.get_all_processed_keywords_for_client(client_id))
    logger.info(f"Found {len(existing_keywords)} existing keywords to exclude.")

    # Expansion
    expansion_result = expander.expand_seed_keyword(
        seed_keywords,
        discovery_modes,
        filters,
        order_by,
        existing_keywords,
        limit,
        depth,
        ignore_synonyms,
    )

    all_expanded_keywords = expansion_result.get("final_keywords", [])
    
    # ADD EXPANSION COST:
    expansion_cost = expansion_result.get("total_cost", 0.0)
    total_api_cost += expansion_cost
    
    # DISTRIBUTE COST BY SOURCE:
    for source, count in expansion_result.get("raw_counts", {}).items():
        if count > 0:
            # Estimate cost per source based on count proportion
            proportion = count / max(expansion_result.get("total_raw_count", 1), 1)
            cost_breakdown[source] = expansion_cost * proportion

    logger.info(f"Expansion cost: ${expansion_cost:.4f}")

    # Scoring and Qualification
    processed_opportunities = []
    disqualification_reasons = {}
    status_counts = {"qualified": 0, "review": 0, "rejected": 0}

    for opp in all_expanded_keywords:
        # ... existing scoring logic ...
        processed_opportunities.append(opp)

    passed_count = status_counts.get("qualified", 0) + status_counts.get("review", 0)
    rejected_count = status_counts.get("rejected", 0)

    logger.info(f"Scoring complete. Passed: {passed_count}, Rejected: {rejected_count}")
    logger.info(f"Total API cost: ${total_api_cost:.4f}")

    stats = {
        **expansion_result,
        "disqualification_reasons": disqualification_reasons,
        "disqualified_count": rejected_count,
        "final_qualified_count": passed_count,
        "cost_breakdown": cost_breakdown,  # ADD THIS
    }

    return {
        "stats": stats,
        "total_cost": total_api_cost,  # ACCURATE TOTAL
        "opportunities": processed_opportunities,
    }
```

---

### **Step 2.6: Validate Regex Patterns**

**File: `backend/api/routers/discovery.py`**

```python
import re
from typing import List, Dict, Any

def validate_regex_filter(filters: List[Dict[str, Any]]) -> None:
    """
    Validates regex filters to prevent catastrophic backtracking.
    
    Raises:
        HTTPException: If regex is invalid or dangerous
    """
    if not filters:
        return
    
    # Dangerous regex patterns
    DANGEROUS_PATTERNS = [
        r'(.*)*',        # Nested quantifiers
        r'(.*)+',        # Nested quantifiers
        r'(a+)+',        # Polynomial regex
        r'(a|a)*',       # Alternation with overlap
        r'(a|ab)*',      # Alternation with overlap
    ]
    
    for f in filters:
        if f.get('operator') in ['regex', 'not_regex']:
            pattern = f.get('value', '')
            
            # Check for dangerous patterns
            for dangerous in DANGEROUS_PATTERNS:
                if dangerous in pattern:
                    raise HTTPException(
                        status_code=400,
                        detail=f"Regex pattern '{pattern}' contains dangerous construct '{dangerous}' that could cause catastrophic backtracking."
                    )
            
            # Validate regex syntax
            try:
                re.compile(pattern)
            except re.error as e:
                raise HTTPException(
                    status_code=400,
                    detail=f"Invalid regex pattern '{pattern}': {str(e)}"
                )
            
            # Length limit
            if len(pattern) > 1000:
                raise HTTPException(
                    status_code=400,
                    detail="Regex pattern exceeds maximum length of 1000 characters."
                )

@router.post("/clients/{client_id}/discovery-runs-async", response_model=JobResponse)
async def start_discovery_run_async(
    client_id: str,
    request: DiscoveryRunRequest,
    # ... dependencies ...
):
    # ... existing validation ...
    
    # VALIDATE REGEX:
    if request.filters:
        validate_regex_filter(request.filters)
    
    # ... rest of function ...
```

---

### **Step 2.7: Tighten CORS Configuration**

**File: `backend/config.py`**

```python
from pydantic_settings import BaseSettings
from typing import List
import os
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    # ... existing settings ...
    
    # CORS - Be explicit about allowed origins
    CORS_ORIGINS: List[str] = [
        "http://localhost:5173",
        "http://localhost:3000",
        "http://127.0.0.1:5173",
        "http://127.0.0.1:3000"
    ]
    
    # In production, load from environment variable
    if os.getenv("ENVIRONMENT") == "production":
        CORS_ORIGINS = os.getenv("ALLOWED_ORIGINS", "").split(",")
    
    # Other CORS settings
    CORS_ALLOW_CREDENTIALS: bool = True
    CORS_ALLOW_METHODS: List[str] = ["GET", "POST", "PUT", "DELETE", "OPTIONS"]
    CORS_ALLOW_HEADERS: List[str] = ["*"]
    CORS_MAX_AGE: int = 600  # 10 minutes
    
    class Config:
        case_sensitive = True

settings = Settings()
```

**File: `backend/app/main.py`**

```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .config import settings

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    debug=settings.DEBUG,
    lifespan=lifespan
)

# STRICTER CORS:
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,  # Explicit list only
    allow_credentials=settings.CORS_ALLOW_CREDENTIALS,
    allow_methods=settings.CORS_ALLOW_METHODS,
    allow_headers=settings.CORS_ALLOW_HEADERS,
    max_age=settings.CORS_MAX_AGE,
)
```

---

### **Step 2.8: Add Input Sanitization**

**File: `backend/utils/sanitization.py` (NEW FILE)**

```python
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
```

**File: `backend/api/routers/discovery.py`**

```python
from utils.sanitization import sanitize_keyword_list, sanitize_filters

@router.post("/clients/{client_id}/discovery-runs-async", response_model=JobResponse)
async def start_discovery_run_async(
    client_id: str,
    request: DiscoveryRunRequest,
    # ... dependencies ...
):
    # ... existing validation ...
    
    # SANITIZE INPUTS:
    seed_keywords = sanitize_keyword_list(request.seed_keywords)
    negative_keywords = sanitize_keyword_list(request.negative_keywords or [])
    
    if request.filters:
        filters = sanitize_filters(request.filters)
        validate_regex_filter(filters)
    else:
        filters = None
    
    # ... rest of function uses sanitized inputs ...
```

---

## Phase 3: Medium Priority Fixes

### **Step 3.1: Consistent Error Handling**

**File: `backend/utils/exceptions.py` (NEW FILE)**

```python
"""
Custom exceptions for consistent error handling.
"""

from fastapi import HTTPException
from typing import Optional, Dict, Any

class BaseAPIException(HTTPException):
    """Base exception for API errors."""
    
    def __init__(
        self, 
        status_code: int, 
        detail: str,
        error_code: Optional[str] = None,
        extra: Optional[Dict[str, Any]] = None
    ):
        super().__init__(status_code=status_code, detail=detail)
        self.error_code = error_code
        self.extra = extra or {}

class ValidationException(BaseAPIException):
    """Raised when input validation fails."""
    
    def __init__(self, detail: str, field: Optional[str] = None):
        super().__init__(
            status_code=400,
            detail=detail,
            error_code="VALIDATION_ERROR",
            extra={"field": field} if field else {}
        )

class ResourceNotFoundException(BaseAPIException):
    """Raised when a requested resource is not found."""
    
    def __init__(self, resource_type: str, resource_id: Any):
        super().__init__(
            status_code=404,
            detail=f"{resource_type} with ID {resource_id} not found.",
            error_code="RESOURCE_NOT_FOUND",
            extra={"resource_type": resource_type, "resource_id": str(resource_id)}
        )

class DataForSEOAPIException(BaseAPIException):
    """Raised when DataForSEO API call fails."""
    
    def __init__(self, detail: str, status_code: int = 502):
        super().__init__(
            status_code=status_code,
            detail=f"DataForSEO API error: {detail}",
            error_code="EXTERNAL_API_ERROR"
        )

class RateLimitException(BaseAPIException):
    """Raised when rate limit is exceeded."""
    
    def __init__(self, retry_after: int = 60):
        super().__init__(
            status_code=429,
            detail=f"Rate limit exceeded. Please try again in {retry_after} seconds.",
            error_code="RATE_LIMIT_EXCEEDED",
            extra={"retry_after": retry_after}
        )
```

**File: `backend/api/routers/discovery.py`**

```python
from utils.exceptions import (
    ValidationException,
    ResourceNotFoundException,
    DataForSEOAPIException,
    RateLimitException
)

@router.post("/clients/{client_id}/discovery-runs-async", response_model=JobResponse)
async def start_discovery_run_async(
    client_id: str,
    request: DiscoveryRunRequest,
    # ... dependencies ...
):
    if client_id != orchestrator.client_id:
        raise ValidationException("Permission denied", field="client_id")
    
    try:
        # ... existing code ...
        
        discovery_modes = request.discovery_modes
        if not discovery_modes or len(discovery_modes) == 0:
            raise ValidationException(
                "At least one discovery mode must be selected.",
                field="discovery_modes"
            )
        
        # ... rest of validation ...
        
    except ValidationException:
        raise  # Re-raise custom exceptions
    except SQLAlchemyError as db_error:
        logger.error(f"Database error: {db_error}", exc_info=True)
        raise BaseAPIException(
            status_code=500,
            detail="Database operation failed.",
            error_code="DATABASE_ERROR"
        )
    except Exception as e:
        logger.error(f"Unexpected error: {e}", exc_info=True)
        raise BaseAPIException(
            status_code=500,
            detail="An unexpected error occurred.",
            error_code="INTERNAL_SERVER_ERROR"
        )
```

---

### **Step 3.2: Add Loading States**

**File: `client/my-content-app/src/pages/DiscoveryPage/components/DiscoveryForm.jsx`**

```javascript
const DiscoveryForm = ({ isSubmitting, onSubmit }) => {
  const [form] = Form.useForm();
  const { filtersData, isLoading: isLoadingFilters } = useDiscoveryFilters();
  const [selectedDiscoveryModes, setSelectedDiscoveryModes] = useState([
    'keyword_ideas', 'keyword_suggestions', 'related_keywords'
  ]);
  const { clientId } = useClient();
  const [isValidating, setIsValidating] = useState(false);
  const [validationStatus, setValidationStatus] = useState('');
  const [validationMessage, setValidationMessage] = useState('');

  // ... existing validation logic ...

  // SHOW SKELETON WHEN LOADING:
  if (isLoadingFilters) {
    return (
      <Card>
        <Skeleton active paragraph={{ rows: 8 }} />
      </Card>
    );
  }

  return (
    <Form 
      form={form} 
      layout="vertical" 
      onFinish={onFinish} 
      onValuesChange={handleValuesChange}
      initialValues={{
        // ... existing initial values ...
      }}
    >
      {/* ... existing form fields ... */}

      <Row justify="end" align="middle" style={{ marginTop: '24px' }}>
        <Col>
          <Button 
            type="primary" 
            htmlType="submit" 
            icon={<RocketOutlined />} 
            loading={isSubmitting} 
            size="large" 
            disabled={isValidating || validationStatus === 'error'}
          >
            {isSubmitting ? 'Finding Opportunities...' : 'Find Opportunities'}
          </Button>
        </Col>
      </Row>
    </Form>
  );
};
```

---

### **Step 3.3: Add Retry Logic**

**File: `backend/external_apis/dataforseo_client_v2.py`**

```python
import time
from typing import Tuple, Optional, Dict, Any, List

class DataForSEOClientV2:
    # ... existing code ...
    
    def _post_request_with_retry(
        self, 
        endpoint: str, 
        data: List[Dict[str, Any]], 
        tag: Optional[str] = None,
        max_retries: int = 3,
        backoff_factor: float = 2.0
    ) -> Tuple[Optional[Dict[str, Any]], float]:
        """
        POST request with exponential backoff retry logic.
        """
        last_exception = None
        
        for attempt in range(max_retries):
            try:
                return self._post_request(endpoint, data, tag)
            
            except requests.exceptions.Timeout as e:
                last_exception = e
                if attempt < max_retries - 1:
                    wait_time = backoff_factor ** attempt
                    self.logger.warning(
                        f"Timeout on attempt {attempt + 1}/{max_retries}. "
                        f"Retrying in {wait_time}s..."
                    )
                    time.sleep(wait_time)
                continue
            
            except requests.exceptions.ConnectionError as e:
                last_exception = e
                if attempt < max_retries - 1:
                    wait_time = backoff_factor ** attempt
                    self.logger.warning(
                        f"Connection error on attempt {attempt + 1}/{max_retries}. "
                        f"Retrying in {wait_time}s..."
                    )
                    time.sleep(wait_time)
                continue
            
            except requests.exceptions.HTTPError as e:
                # Don't retry on 4xx errors (client errors)
                if e.response.status_code < 500:
                    raise
                
                last_exception = e
                if attempt < max_retries - 1:
                    wait_time = backoff_factor ** attempt
                    self.logger.warning(
                        f"Server error {e.response.status_code} on attempt {attempt + 1}/{max_retries}. "
                        f"Retrying in {wait_time}s..."
                    )
                    time.sleep(wait_time)
                continue
        
        # If we get here, all retries failed
        self.logger.error(
            f"All {max_retries} retry attempts failed for {endpoint}. "
            f"Last error: {last_exception}"
        )
        raise last_exception
```

---

### **Step 3.4: Improve Pagination**

**File: `backend/external_apis/dataforseo_client_v2.py`**

```python
def post_with_paging(
    self,
    endpoint: str,
    initial_task: Dict[str, Any],
    total_limit: Optional[int] = None,
    tag: Optional[str] = None,
) -> Tuple[List[Dict[str, Any]], float]:
    """
    Executes POST with proper pagination using offset_token.
    Stops when:
    1. No more offset_token
    2. Reached total_limit
    3. No new items returned
    4. Duplicate offset_token (infinite loop protection)
    """
    all_items = []
    total_cost = 0.0
    current_task = initial_task.copy()

    # Remove None values
    if "filters" in current_task and (
        current_task["filters"] is None or len(current_task["filters"]) == 0
    ):
        current_task.pop("filters")

    page_count = 0
    previous_offset_token = None
    consecutive_empty_pages = 0
    MAX_EMPTY_PAGES = 3  # Stop after 3 consecutive empty pages

    while True:
        # Stop if we've reached our limit
        if total_limit is not None and len(all_items) >= total_limit:
            self.logger.info(f"Reached target limit of {total_limit} items.")
            break

        page_count += 1
        self.logger.info(f"Fetching page {page_count} from {endpoint}...")

        request_tag = (
            tag + f":p{page_count}"
            if tag
            else endpoint.split("/")[-1] + f":p{page_count}"
        )
        
        response, cost = self._post_request_with_retry(
            endpoint, [current_task], tag=request_tag
        )
        total_cost += cost

        if (
            not response
            or response.get("status_code") != 20000
            or response.get("tasks_error", 0) > 0
        ):
            self.logger.error(
                f"Paging failed on page {page_count}. "
                f"Status: {response.get('status_code') if response else 'No response'}"
            )
            break

        tasks = response.get("tasks", [])
        if not tasks or "result" not in tasks[0]:
            self.logger.info(f"No 'result' in task for page {page_count}. Stopping.")
            break

        task_result = tasks[0].get("result")
        if not task_result:
            self.logger.info(f"Empty result for page {page_count}. Stopping.")
            break

        items_count = 0
        offset_token = None
        
        if task_result and isinstance(task_result, list) and len(task_result) > 0:
            offset_token = task_result[0].get("offset_token")
            
            for result_item in task_result:
                items = result_item.get("items")
                if items:
                    items_count += len(items)
                    all_items.extend(items)

                # Handle seed keyword data for suggestions
                if endpoint == self.LABS_KEYWORD_SUGGESTIONS:
                    seed_data = result_item.get("seed_keyword_data")
                    if isinstance(seed_data, dict) and seed_data.get("keyword"):
                        seed_data["discovery_source"] = "keyword_suggestions_seed"
                        all_items.append(seed_data)

        # TRACK EMPTY PAGES:
        if items_count == 0:
            consecutive_empty_pages += 1
            if consecutive_empty_pages >= MAX_EMPTY_PAGES:
                self.logger.warning(
                    f"Received {MAX_EMPTY_PAGES} consecutive empty pages. Stopping pagination."
                )
                break
        else:
            consecutive_empty_pages = 0

        # NO OFFSET TOKEN:
        if not offset_token:
            self.logger.info(f"No offset_token on page {page_count}. Pagination complete.")
            break

        # DUPLICATE TOKEN PROTECTION:
        if offset_token == previous_offset_token:
            self.logger.warning(
                f"Duplicate offset_token detected. Breaking to prevent infinite loop."
            )
            break
        
        previous_offset_token = offset_token

        # PREPARE NEXT PAGE:
        current_task = {
            "offset_token": offset_token,
            "limit": initial_task.get("limit", 1000),
        }

        # Rate limiting between pages
        time.sleep(0.5)

    # Trim to exact limit if needed
    if total_limit is not None:
        all_items = all_items[:total_limit]

    self.logger.info(
        f"Pagination complete. Fetched {len(all_items)} items across {page_count} pages. "
        f"Total cost: ${total_cost:.4f}"
    )

    return all_items, total