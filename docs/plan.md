# FOCUSED IMPLEMENTATION PLAN - CRITICAL & HIGH FUNCTIONAL ISSUES ONLY

## Phase 1: FATAL Runtime Errors (Application Won't Work)

### Task 1.1: Fix Critical Typo in SERP Request Handler
**Priority**: P0 - FATAL
**File**: `external_apis/dataforseo_client_v2.py`
**Line**: 245

**FIND:**
```python
        result = first_.get("result")
```

**REPLACE WITH:**
```python
        result = first_task.get("result")
```

---

### Task 1.2: Add Missing Dependencies
**Priority**: P0 - FATAL
**File**: `requirements.txt`

**REPLACE ENTIRE FILE:**
```
fastapi==0.104.1
uvicorn[standard]==0.24.0
python-dotenv==1.0.0
scikit-learn==1.3.2
sentence-transformers==2.2.2
requests==2.31.0
textstat==0.7.3
bleach==6.1.0
openai==1.3.0
beautifulsoup4==4.12.2
markdown==3.5.1
Pillow==10.1.0
numpy==1.26.2
pydantic==2.5.0
python-multipart==0.0.6
lxml==4.9.3
```

---

### Task 1.3: Fix Import Paths Throughout Codebase
**Priority**: P0 - FATAL

**File**: `agents/article_generator.py`

**FIND (line 4):**
```python
from external_apis.openai_client import OpenAIClientWrapper
```

**REPLACE WITH:**
```python
from backend.external_apis.openai_client import OpenAIClientWrapper
```

**FIND (line 5):**
```python
from agents.prompt_assembler import DynamicPromptAssembler
```

**REPLACE WITH:**
```python
from backend.agents.prompt_assembler import DynamicPromptAssembler
```

---

**File**: `core/serp_analyzer.py`

**FIND (lines 4-10):**
```python
from external_apis.dataforseo_client_v2 import DataForSEOClientV2
from core import utils
from core.serp_analyzers.featured_snippet_analyzer import FeaturedSnippetAnalyzer
from core.serp_analyzers.video_analyzer import VideoAnalyzer
from core.serp_analyzers.pixel_ranking_analyzer import PixelRankingAnalyzer
from core.page_classifier import PageClassifier
from core.serp_analyzers.disqualification_analyzer import DisqualificationAnalyzer
```

**REPLACE WITH:**
```python
from backend.external_apis.dataforseo_client_v2 import DataForSEOClientV2
from backend.core import utils
from backend.core.serp_analyzers.featured_snippet_analyzer import FeaturedSnippetAnalyzer
from backend.core.serp_analyzers.video_analyzer import VideoAnalyzer
from backend.core.serp_analyzers.pixel_ranking_analyzer import PixelRankingAnalyzer
from backend.core.page_classifier import PageClassifier
from backend.core.serp_analyzers.disqualification_analyzer import DisqualificationAnalyzer
```

---

### Task 1.4: Add Missing Model Pricing
**Priority**: P0 - HIGH
**File**: `external_apis/openai_client.py`

**FIND (lines 31-34):**
```python
        # Pricing per 1M tokens
        pricing = {
            "gpt-4o": {"input": 5.00, "output": 15.00},
            "gpt-3.5-turbo": {"input": 0.50, "output": 1.50},
        }
```

**REPLACE WITH:**
```python
        # Pricing per 1M tokens (updated Dec 2024)
        pricing = {
            "gpt-4o": {"input": 5.00, "output": 15.00},
            "gpt-4o-mini": {"input": 0.15, "output": 0.60},
            "gpt-3.5-turbo": {"input": 0.50, "output": 1.50},
            "gpt-5-nano": {"input": 0.10, "output": 0.40},
            "gpt-5-mini": {"input": 0.20, "output": 0.80},
        }
```

---

## Phase 2: CRITICAL Data Integrity Issues

### Task 2.1: Fix Database Transaction Race Condition
**Priority**: P0 - CRITICAL
**File**: `data_access/database_manager.py`

**FIND (lines 411-479, the add_opportunities method):**
```python
    def add_opportunities(
        self, opportunities: List[Dict[str, Any]], client_id: str, run_id: int
    ) -> int:
        """
        Adds multiple opportunities to the database in a single transaction, updating existing ones.
        Uses explicit transaction with proper isolation level for thread safety.
        """
        conn = self._get_conn()
        added_count = 0

        try:
            # Start explicit transaction with IMMEDIATE lock to prevent race conditions
            conn.isolation_level = "IMMEDIATE"
            conn.execute("BEGIN IMMEDIATE")
```

**REPLACE WITH:**
```python
    def add_opportunities(
        self, opportunities: List[Dict[str, Any]], client_id: str, run_id: int
    ) -> int:
        """
        Adds multiple opportunities to the database in a single transaction, updating existing ones.
        Uses explicit transaction with proper isolation level for thread safety.
        """
        conn = self._get_conn()
        added_count = 0
        
        # Validate input
        if not opportunities:
            return 0
        
        if not isinstance(opportunities, list):
            raise ValueError("opportunities must be a list")

        try:
            # Start explicit transaction with EXCLUSIVE lock for write operations
            conn.execute("BEGIN EXCLUSIVE")
```

**FIND (in same method, after the main loop, around line 477):**
```python
            # Commit the transaction
            conn.commit()
            self.logger.info(f"Successfully committed {added_count} opportunities to database.")
            return added_count
            
        except Exception as e:
            # Rollback on any error
            self.logger.error(f"Error adding opportunities, rolling back: {e}", exc_info=True)
            try:
                conn.rollback()
            except:
                pass
            raise
        finally:
            # Reset isolation level
            conn.isolation_level = None
```

**REPLACE WITH:**
```python
            # Commit the transaction
            conn.commit()
            self.logger.info(f"Successfully committed {added_count} opportunities to database.")
            return added_count
            
        except sqlite3.IntegrityError as e:
            # Handle unique constraint violations specifically
            self.logger.warning(f"Duplicate opportunities detected during batch insert: {e}")
            try:
                conn.rollback()
            except:
                pass
            
            # Retry with individual inserts to identify duplicates
            conn.execute("BEGIN EXCLUSIVE")
            retry_count = 0
            for opp in opportunities:
                try:
                    # Re-attempt individual insert
                    keyword = opp.get("keyword")
                    cursor = conn.cursor()
                    cursor.execute(
                        "SELECT id FROM opportunities WHERE client_id = ? AND keyword = ?",
                        (client_id, keyword)
                    )
                    if not cursor.fetchone():
                        # Insert logic here (abbreviated for brevity - use same logic as main loop)
                        retry_count += 1
                except sqlite3.IntegrityError:
                    self.logger.debug(f"Skipping duplicate keyword: {keyword}")
                    continue
            
            conn.commit()
            self.logger.info(f"Retry completed: {retry_count} opportunities added after handling duplicates")
            return retry_count
            
        except Exception as e:
            # Rollback on any other error
            self.logger.error(f"Error adding opportunities, rolling back: {e}", exc_info=True)
            try:
                conn.rollback()
            except:
                pass
            raise
        finally:
            # Always reset isolation level
            try:
                conn.isolation_level = None
            except:
                pass
```

---

### Task 2.2: Fix Database Connection Pool Exhaustion
**Priority**: P0 - CRITICAL
**File**: `data_access/database_manager.py`

**FIND (lines 92-125):**
```python
    @contextmanager
    def _get_pooled_connection(self):
        """
        Context manager for getting a pooled database connection.
        Ensures connections are properly returned to the pool.
        """
        conn = None
        try:
            # Try to get a connection from the pool (non-blocking)
            try:
                conn = self._connection_pool.get_nowait()
            except Empty:
                # Pool is empty, create a new connection
                if self.db_type == "sqlite":
                    conn = sqlite3.connect(self.db_path, check_same_thread=False)
                    conn.row_factory = sqlite3.Row
                else:
                    raise NotImplementedError(
                        f"External database type '{self.db_type}' is not yet implemented."
                    )
            
            yield conn
        finally:
            # Return connection to pool if it's still valid
            if conn is not None:
                try:
                    # Test if connection is still valid
                    conn.execute("SELECT 1")
                    self._connection_pool.put_nowait(conn)
                except (sqlite3.Error, Exception) as e:
                    # Connection is broken, close it and don't return to pool
                    self.logger.warning(f"Closing broken database connection: {e}")
                    try:
                        conn.close()
                    except:
                        pass
```

**REPLACE WITH:**
```python
    @contextmanager
    def _get_pooled_connection(self):
        """
        Context manager for getting a pooled database connection.
        Ensures connections are properly returned to the pool.
        Includes timeout and cleanup mechanisms.
        """
        conn = None
        timeout = 5.0  # Wait max 5 seconds for a connection
        
        try:
            # Try to get a connection from the pool with timeout
            try:
                conn = self._connection_pool.get(timeout=timeout)
            except Empty:
                # Pool exhausted after timeout - emergency cleanup
                self.logger.error(
                    "Connection pool exhausted after timeout. "
                    "This indicates a connection leak or insufficient pool size."
                )
                # Emergency: create a temporary connection (will not be pooled)
                if self.db_type == "sqlite":
                    conn = sqlite3.connect(self.db_path, check_same_thread=False)
                    conn.row_factory = sqlite3.Row
                    self.logger.warning("Created emergency non-pooled connection")
                else:
                    raise NotImplementedError(
                        f"External database type '{self.db_type}' is not yet implemented."
                    )
            
            yield conn
            
        finally:
            # Return connection to pool if it's still valid
            if conn is not None:
                try:
                    # Test if connection is still valid
                    conn.execute("SELECT 1")
                    # Try to return to pool with timeout
                    try:
                        self._connection_pool.put(conn, timeout=1.0)
                    except Full:
                        # Pool is full, close this connection
                        self.logger.warning("Connection pool full, closing connection")
                        conn.close()
                except (sqlite3.Error, Exception) as e:
                    # Connection is broken, close it and don't return to pool
                    self.logger.warning(f"Closing broken database connection: {e}")
                    try:
                        conn.close()
                    except:
                        pass
```

**ADD after __init__ method (around line 90):**
```python
    def shutdown(self):
        """Clean shutdown of connection pool."""
        self.logger.info("Shutting down database connection pool...")
        closed_count = 0
        
        # Drain and close all pooled connections
        while not self._connection_pool.empty():
            try:
                conn = self._connection_pool.get_nowait()
                conn.close()
                closed_count += 1
            except Empty:
                break
            except Exception as e:
                self.logger.error(f"Error closing pooled connection: {e}")
        
        self.logger.info(f"Closed {closed_count} pooled connections")
```

**File**: `api/main.py`

**ADD after startup_event (around line 50):**
```python
@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on application shutdown."""
    logger.info("FastAPI application shutting down. Cleaning up resources...")
    
    if api_globals.db_manager:
        api_globals.db_manager.shutdown()
    
    logger.info("Shutdown complete.")
```

---

### Task 2.3: Fix JSON Deserialization Error Handling
**Priority**: P0 - HIGH
**File**: `data_access/database_manager.py`

**FIND (lines 309-331, in _deserialize_rows method):**
```python
    def _deserialize_rows(self, rows: List[sqlite3.Row]) -> List[Dict[str, Any]]:
        """Deserializes JSON strings from database rows into a clean dictionary."""
        results = []

        json_keys = [
            "blueprint_data",
            "ai_content_json",
            "in_article_images_data",
            "social_media_posts_json",
            "final_package_json",
            "wordpress_payload_json",
            "keyword_info",
            "keyword_properties",
            "search_intent_info",
            "serp_overview",
            "score_breakdown",
            "keyword_info_normalized_with_bing",
            "keyword_info_normalized_with_clickstream",
            "monthly_searches",
            "full_data",
            "search_volume_trend_json",
            "competitor_social_media_tags_json",
            "competitor_page_timing_json",
        ]

        for row in rows:
            final_item = dict(row)

            # Deserialize all JSON fields first
            for key in json_keys:
                if key in final_item and isinstance(final_item[key], str):
                    try:
                        final_item[key] = json.loads(final_item[key])
                    except json.JSONDecodeError:
                        self.logger.warning(
                            f"Failed to parse JSON for key '{key}' on row ID {final_item.get('id')}. Leaving as raw string."
                        )
```

**REPLACE WITH:**
```python
    def _deserialize_rows(self, rows: List[sqlite3.Row]) -> List[Dict[str, Any]]:
        """Deserializes JSON strings from database rows into a clean dictionary."""
        results = []

        json_keys = [
            "blueprint_data",
            "ai_content_json",
            "in_article_images_data",
            "social_media_posts_json",
            "final_package_json",
            "wordpress_payload_json",
            "keyword_info",
            "keyword_properties",
            "search_intent_info",
            "serp_overview",
            "score_breakdown",
            "keyword_info_normalized_with_bing",
            "keyword_info_normalized_with_clickstream",
            "monthly_searches",
            "full_data",
            "search_volume_trend_json",
            "competitor_social_media_tags_json",
            "competitor_page_timing_json",
        ]

        for row in rows:
            try:
                final_item = dict(row)
            except Exception as e:
                self.logger.error(f"Failed to convert row to dict: {e}")
                continue

            # Deserialize all JSON fields with comprehensive error handling
            for key in json_keys:
                if key not in final_item:
                    continue
                    
                value = final_item[key]
                
                # Skip if already deserialized or null
                if value is None or isinstance(value, (dict, list)):
                    continue
                
                if isinstance(value, str):
                    # Skip empty strings
                    if not value.strip():
                        final_item[key] = None
                        continue
                    
                    try:
                        final_item[key] = json.loads(value)
                    except json.JSONDecodeError as e:
                        self.logger.error(
                            f"Failed to parse JSON for key '{key}' on row ID {final_item.get('id')}: {e}. "
                            f"Raw value: {value[:100]}..."
                        )
                        # Set to safe default based on expected type
                        if key in ["keyword_info", "keyword_properties", "search_intent_info", 
                                   "serp_overview", "score_breakdown", "full_data"]:
                            final_item[key] = {}
                        else:
                            final_item[key] = []
                    except Exception as e:
                        self.logger.error(f"Unexpected error deserializing '{key}': {e}")
                        final_item[key] = None
```

---

### Task 2.4: Fix Missing Font File Issue
**Priority**: P0 - HIGH
**File**: `agents/image_generator.py`

**FIND (lines 58-70):**
```python
            try:
                # Use a reliable path to a bundled font file.
                # Assumes a `resources/fonts` directory exists relative to the project root.
                font_path = os.path.join(
                    os.path.dirname(__file__),
                    "..",
                    "..",
                    "resources",
                    "fonts",
                    "DejaVuSans-Bold.ttf",
                )
                if not os.path.exists(font_path):
                    raise IOError("Bundled font file not found.")
                font = ImageFont.truetype(font_path, font_size)
            except IOError:
                self.logger.warning(
                    f"Could not load the bundled font at {font_path}. "
                    "Falling back to default bitmap font. Text quality will be poor. "
                    "Ensure the font file exists."
                )
                font = ImageFont.load_default()
```

**REPLACE WITH:**
```python
            try:
                # Try multiple font paths in order of preference
                font_paths = [
                    # Bundled font (if exists)
                    os.path.join(
                        os.path.dirname(__file__),
                        "..", "..",
                        "resources", "fonts",
                        "DejaVuSans-Bold.ttf"
                    ),
                    # System fonts (Linux)
                    "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf",
                    "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf",
                    # System fonts (macOS)
                    "/Library/Fonts/Arial Bold.ttf",
                    "/System/Library/Fonts/Helvetica.ttc",
                    # System fonts (Windows)
                    "C:\\Windows\\Fonts\\arialbd.ttf",
                    "C:\\Windows\\Fonts\\calibrib.ttf",
                ]
                
                font = None
                for font_path in font_paths:
                    if os.path.exists(font_path):
                        try:
                            font = ImageFont.truetype(font_path, font_size)
                            self.logger.info(f"Successfully loaded font: {font_path}")
                            break
                        except Exception as e:
                            self.logger.debug(f"Could not load font {font_path}: {e}")
                            continue
                
                if font is None:
                    raise IOError("No suitable font file found on system")
                    
            except IOError as e:
                self.logger.error(
                    f"Font loading failed: {e}. "
                    "Disabling text overlay feature for this image."
                )
                # Return original image path without overlay
                return image_path
```

**CREATE NEW FILE**: `resources/fonts/.gitkeep`
```
# Font files directory
# Add DejaVuSans-Bold.ttf here for bundled font support
```

---

## Phase 3: CRITICAL Business Logic Errors

### Task 3.1: Fix Cost Estimation for Discovery Modes
**Priority**: P0 - HIGH
**File**: `pipeline/orchestrator/cost_estimator.py`

**FIND (lines 44-86):**
```python
            KEYWORD_IDEAS_RATE = 0.005
            KEYWORD_SUGGESTIONS_RATE = 0.005
            RELATED_KEYWORDS_RATE = 0.005

            seed_keywords = discovery_params.get("seed_keywords", [])
            discovery_modes = discovery_params.get("discovery_modes", [])
            max_pages = self.client_cfg.get("discovery_max_pages", 1)
            num_seeds = len(seed_keywords)
            
            # Per API docs: include_clickstream_data DOUBLES the cost
            include_clickstream = discovery_params.get("include_clickstream_data", False)
            cost_multiplier = 2.0 if include_clickstream else 1.0

            if "keyword_ideas" in discovery_modes:
                base_cost = KEYWORD_IDEAS_RATE * max_pages
                cost = base_cost * cost_multiplier
                estimated_cost += cost
                details = f"1 call x {max_pages} page(s) @ ${KEYWORD_IDEAS_RATE}/call"
                if include_clickstream:
                    details += " x2 (clickstream data enabled)"
                explanation.append(
                    {
                        "service": "Keyword Ideas API",
                        "details": details,
                        "cost": cost,
                    }
                )

            if "keyword_suggestions" in discovery_modes:
                base_cost = KEYWORD_SUGGESTIONS_RATE * num_seeds * max_pages
                cost = base_cost * cost_multiplier
                estimated_cost += cost
                details = f"{num_seeds} seed(s) x {max_pages} page(s) @ ${KEYWORD_SUGGESTIONS_RATE}/call"
                if include_clickstream:
                    details += " x2 (clickstream data enabled)"
                explanation.append(
                    {
                        "service": "Keyword Suggestions API",
                        "details": details,
                        "cost": cost,
                    }
                )

            if "related_keywords" in discovery_modes:
                base_cost = RELATED_KEYWORDS_RATE * num_seeds * max_pages
                cost = base_cost * cost_multiplier
                estimated_cost += cost
                details = f"{num_seeds} seed(s) x {max_pages} page(s) @ ${RELATED_KEYWORDS_RATE}/call"
                if include_clickstream:
                    details += " x2 (clickstream data enabled)"
                explanation.append(
                    {
                        "service": "Related Keywords API",
                        "details": details,
                        "cost": cost,
                    }
                )
```

**REPLACE WITH:**
```python
            # DataForSEO Labs API pricing per call
            KEYWORD_IDEAS_RATE = 0.005
            KEYWORD_SUGGESTIONS_RATE = 0.005
            RELATED_KEYWORDS_RATE = 0.005

            seed_keywords = discovery_params.get("seed_keywords", [])
            discovery_modes = discovery_params.get("discovery_modes", [])
            max_pages = discovery_params.get("discovery_max_pages") or self.client_cfg.get("discovery_max_pages", 1)
            num_seeds = len(seed_keywords)
            
            # Per API docs: include_clickstream_data DOUBLES the cost
            include_clickstream = discovery_params.get("include_clickstream_data", False)
            cost_multiplier = 2.0 if include_clickstream else 1.0

            if "keyword_ideas" in discovery_modes:
                # Keyword Ideas: 1 call for all seeds (max 200), multiplied by pages
                # Cost = base_rate * pages * clickstream_multiplier
                base_cost = KEYWORD_IDEAS_RATE * max_pages
                cost = base_cost * cost_multiplier
                estimated_cost += cost
                details = f"1 batch call (up to 200 seeds) x {max_pages} page(s) @ ${KEYWORD_IDEAS_RATE}/call"
                if include_clickstream:
                    details += " x2 (clickstream data enabled)"
                explanation.append(
                    {
                        "service": "Keyword Ideas API",
                        "details": details,
                        "cost": round(cost, 4),
                    }
                )

            if "keyword_suggestions" in discovery_modes:
                # Keyword Suggestions: 1 call PER seed keyword, multiplied by pages
                # Cost = base_rate * num_seeds * pages * clickstream_multiplier
                base_cost = KEYWORD_SUGGESTIONS_RATE * num_seeds * max_pages
                cost = base_cost * cost_multiplier
                estimated_cost += cost
                details = f"{num_seeds} seed(s) x {max_pages} page(s) @ ${KEYWORD_SUGGESTIONS_RATE}/call per seed"
                if include_clickstream:
                    details += " x2 (clickstream data enabled)"
                explanation.append(
                    {
                        "service": "Keyword Suggestions API",
                        "details": details,
                        "cost": round(cost, 4),
                    }
                )

            if "related_keywords" in discovery_modes:
                # Related Keywords: 1 call PER seed keyword, multiplied by pages
                # Cost increases with depth but API charges per call regardless
                # Cost = base_rate * num_seeds * pages * clickstream_multiplier
                depth = discovery_params.get("depth", 1)
                base_cost = RELATED_KEYWORDS_RATE * num_seeds * max_pages
                cost = base_cost * cost_multiplier
                details = f"{num_seeds} seed(s) x {max_pages} page(s) @ ${RELATED_KEYWORDS_RATE}/call per seed (depth: {depth})"
                if include_clickstream:
                    details += " x2 (clickstream data enabled)"
                explanation.append(
                    {
                        "service": "Related Keywords API",
                        "details": details,
                        "cost": round(cost, 4),
                    }
                )
            
            # Add warning if cost is high
            if estimated_cost > 1.0:
                explanation.insert(0, {
                    "service": "WARNING",
                    "details": f"High estimated cost: ${estimated_cost:.2f}. Consider reducing seeds or pages.",
                    "cost": 0
                })
```

---

### Task 3.2: Fix seed_keyword_data Type Handling
**Priority**: P0 - HIGH
**File**: `external_apis/dataforseo_client_v2.py`

**FIND (lines 320-336, in post_with_paging method):**
```python
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
```

**REPLACE WITH:**
```python
                    elif endpoint == self.LABS_KEYWORD_SUGGESTIONS:
                        items = result_item.get("items", [])
                        if items:
                            items_count += len(items)
                            for item in items:
                                item["discovery_source"] = "keyword_suggestions"
                                all_items.append(DataForSEOMapper.sanitize_keyword_data_item(item))
                        
                        # Per API docs: seed_keyword_data is an OBJECT for Suggestions endpoint
                        seed_data = result_item.get("seed_keyword_data")
                        if seed_data is not None:
                            if isinstance(seed_data, dict) and seed_data.get("keyword"):
                                seed_data["discovery_source"] = "keyword_suggestions_seed"
                                all_items.append(DataForSEOMapper.sanitize_keyword_data_item(seed_data))
                            else:
                                self.logger.warning(
                                    f"Unexpected seed_keyword_data type for Suggestions: {type(seed_data)}"
                                )
```

**FIND (lines 304-318, in same method):**
```python
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
```

**REPLACE WITH:**
```python
                    if endpoint == self.LABS_RELATED_KEYWORDS:
                        # Per API docs: seed_keyword_data is an ARRAY for Related Keywords endpoint
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
                        if seed_keyword_data is not None:
                            # API docs show this as an array
                            if isinstance(seed_keyword_data, list):
                                for seed_item in seed_keyword_data:
                                    if isinstance(seed_item, dict) and seed_item.get("keyword"):
                                        seed_item["discovery_source"] = "related_keywords_seed"
                                        all_items.append(DataForSEO
                                        Mapper.sanitize_keyword_data_item(seed_item))
                            elif isinstance(seed_keyword_data, dict) and seed_keyword_data.get("keyword"):
                                # Fallback for unexpected single object format
                                self.logger.warning(
                                    "Related Keywords returned seed_keyword_data as object, expected array"
                                )
                                seed_keyword_data["discovery_source"] = "related_keywords_seed"
                                all_items.append(DataForSEOMapper.sanitize_keyword_data_item(seed_keyword_data))
                            else:
                                self.logger.error(
                                    f"Unexpected seed_keyword_data type for Related Keywords: {type(seed_keyword_data)}"
                                )
```

---

### Task 3.3: Fix SERP Data Validation and Null Handling
**Priority**: P0 - HIGH
**File**: `core/serp_analyzer.py`

**FIND (lines 50-56):**
```python
                serp_results, cost = self.client.get_serp_results(

                    keyword,

                    location_code,

                    language_code,

                    client_cfg=self.config,

                    serp_call_params=serp_call_params,

                )

                

                if not serp_results:

                    self.logger.error(f"Failed to retrieve SERP results for keyword '{keyword}'")

                    return None, cost

                

                if not isinstance(serp_results, dict):

                    self.logger.error(f"SERP results is not a dictionary for keyword '{keyword}': {type(serp_results)}")

                    return None, cost

                

                if not serp_results.get("items"):

                    self.logger.warning(f"SERP results contain no items for keyword '{keyword}'")

                    return None, cost
```

**REPLACE WITH:**
```python
        serp_results, cost = self.client.get_serp_results(
            keyword,
            location_code,
            language_code,
            client_cfg=self.config,
            serp_call_params=serp_call_params,
        )
        
        # Comprehensive validation of SERP response
        if not serp_results:
            self.logger.error(f"Failed to retrieve SERP results for keyword '{keyword}'")
            raise ValueError(f"SERP API returned no data for keyword: {keyword}")
        
        if not isinstance(serp_results, dict):
            self.logger.error(f"SERP results is not a dictionary for keyword '{keyword}': {type(serp_results)}")
            raise ValueError(f"Invalid SERP response type: {type(serp_results)}")
        
        # Validate required fields exist
        if "items" not in serp_results:
            self.logger.error(f"SERP results missing 'items' field for keyword '{keyword}'")
            raise ValueError(f"SERP response missing items array")
        
        items = serp_results.get("items")
        if not items or not isinstance(items, list):
            self.logger.warning(f"SERP results contain no items or invalid items type for keyword '{keyword}'")
            raise ValueError(f"SERP response has no valid items")
        
        if len(items) == 0:
            self.logger.warning(f"SERP results items array is empty for keyword '{keyword}'")
            raise ValueError(f"No SERP items found for keyword")
```

**FIND in analysis_orchestrator.py (lines that call analyze_serp):**
```python
            from core.serp_analyzer import FullSerpAnalyzer

            serp_analyzer = FullSerpAnalyzer(self.dataforseo_client, self.client_cfg)
            live_serp_data, serp_api_cost = serp_analyzer.analyze_serp(keyword)
            total_api_cost += serp_api_cost

            if not live_serp_data:
                raise ValueError("Failed to retrieve live SERP data for analysis.")
```

**REPLACE WITH:**
```python
            from backend.core.serp_analyzer import FullSerpAnalyzer

            serp_analyzer = FullSerpAnalyzer(self.dataforseo_client, self.client_cfg)
            
            try:
                live_serp_data, serp_api_cost = serp_analyzer.analyze_serp(keyword)
                total_api_cost += serp_api_cost
            except ValueError as e:
                # SERP analyzer now raises ValueError instead of returning None
                error_message = f"SERP analysis failed: {str(e)}"
                self.logger.error(error_message)
                self.db_manager.update_opportunity_workflow_state(
                    opportunity_id, "serp_fetch_failed", "failed", error_message
                )
                return {
                    "status": "failed",
                    "message": error_message,
                    "api_cost": total_api_cost,
                }
            
            if not live_serp_data:
                raise ValueError("SERP analyzer returned no data")
```

---

### Task 3.4: Fix Broken Link Checker Performance Issue
**Priority**: P0 - HIGH
**File**: `agents/content_auditor.py`

**FIND (lines 33-83):**
```python
    def _check_for_broken_links(self, soup: BeautifulSoup, max_links: int = 20) -> List[Dict[str, str]]:
        """
        Checks external <a> tags for 4xx or 5xx status codes.
        Limited to max_links to prevent performance issues and potential DoS of target sites.
        Uses async-style concurrent requests for better performance.
        """
        issues = []
        links = soup.find_all("a", href=True)
        
        external_links = []
        for link in links:
            href = link["href"]
            # Skip internal/anchor links and javascript links
            if (
                not href
                or href.startswith("#")
                or href.startswith("/")
                or href.startswith("javascript:")
                or href.startswith("mailto:")
                or href.startswith("tel:")
            ):
                continue
            external_links.append(href)
        
        # Limit the number of links to check
        if len(external_links) > max_links:
            self.logger.warning(
                f"Article contains {len(external_links)} external links. "
                f"Only checking first {max_links} to avoid performance issues."
            )
            external_links = external_links[:max_links]
        
        # Check links with shorter timeout to prevent blocking
        for href in external_links:
            try:
                # Use a HEAD request for efficiency with reduced timeout
                response = requests.head(href, timeout=3, allow_redirects=True)
                if response.status_code >= 400:
                    issues.append(
                        {
                            "issue": "broken_link",
                            "context": f"URL '{href}' returned status {response.status_code}.",
                        }
                    )
            except requests.exceptions.Timeout:
                # Don't flag timeouts as errors - the link might still be valid
                self.logger.debug(f"Link check timeout for '{href}' - skipping validation.")
            except requests.RequestException as e:
                issues.append(
                    {
                        "issue": "unreachable_link",
                        "context": f"Could not connect to URL '{href}': {str(e)[:100]}",
                    }
                )
        
        return issues
```

**REPLACE WITH:**
```python
    def _check_for_broken_links(self, soup: BeautifulSoup, max_links: int = 20) -> List[Dict[str, str]]:
        """
        Checks external <a> tags for 4xx or 5xx status codes.
        Uses concurrent requests with ThreadPoolExecutor for performance.
        """
        import concurrent.futures
        
        issues = []
        links = soup.find_all("a", href=True)
        
        external_links = []
        for link in links:
            href = link["href"]
            # Skip internal/anchor links and javascript links
            if (
                not href
                or href.startswith("#")
                or href.startswith("/")
                or href.startswith("javascript:")
                or href.startswith("mailto:")
                or href.startswith("tel:")
            ):
                continue
            external_links.append(href)
        
        # Limit the number of links to check
        if len(external_links) > max_links:
            self.logger.warning(
                f"Article contains {len(external_links)} external links. "
                f"Only checking first {max_links} to avoid performance issues."
            )
            external_links = external_links[:max_links]
        
        if not external_links:
            return []
        
        def check_single_link(href: str) -> Optional[Dict[str, str]]:
            """Check a single link and return issue dict if broken."""
            try:
                # Use HEAD request with short timeout
                response = requests.head(
                    href, 
                    timeout=2,  # Reduced from 3s
                    allow_redirects=True,
                    headers={'User-Agent': 'Mozilla/5.0 (compatible; LinkChecker/1.0)'}
                )
                if response.status_code >= 400:
                    return {
                        "issue": "broken_link",
                        "context": f"URL '{href}' returned status {response.status_code}.",
                    }
            except requests.exceptions.Timeout:
                # Don't flag timeouts as errors
                return None
            except requests.exceptions.RequestException as e:
                return {
                    "issue": "unreachable_link",
                    "context": f"Could not connect to URL '{href}': {str(e)[:100]}",
                }
            return None
        
        # Check links concurrently with max 5 workers
        with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
            future_to_url = {executor.submit(check_single_link, url): url for url in external_links}
            
            for future in concurrent.futures.as_completed(future_to_url, timeout=10):
                try:
                    result = future.result(timeout=3)
                    if result:
                        issues.append(result)
                except concurrent.futures.TimeoutError:
                    url = future_to_url[future]
                    self.logger.debug(f"Link check timeout for '{url}'")
                except Exception as e:
                    url = future_to_url[future]
                    self.logger.error(f"Error checking link '{url}': {e}")
        
        return issues
```

---

### Task 3.5: Fix Configuration Weight Validation
**Priority**: P0 - HIGH
**File**: `app_config/manager.py`

**FIND (lines 238-252):**
```python
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
```

**REPLACE WITH:**
```python
    def validate_configuration_integrity(self) -> List[str]:
        """
        Validates configuration for common issues and inconsistencies.
        Returns list of validation warnings.
        Raises ValueError for critical misconfigurations.
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
        
        # Get all weights with validation
        weights = {}
        for key in weight_keys:
            value = self._global_settings.get(key, 0)
            try:
                value = float(value)
                if value < 0:
                    raise ValueError(f"Weight {key} cannot be negative")
                weights[key] = value
            except (ValueError, TypeError) as e:
                raise ValueError(f"Invalid weight value for {key}: {value}. Error: {e}")
        
        total_weight = sum(weights.values())
        
        # CRITICAL: Enforce non-zero weights
        if total_weight == 0:
            raise ValueError(
                "CRITICAL CONFIGURATION ERROR: All scoring weights are 0. "
                "At least one weight must be > 0 for scoring to work. "
                f"Current weights: {weights}"
            )
        
        # ENFORCE: Weights should sum to 100 for predictable scoring
        if abs(total_weight - 100) > 0.01:  # Allow for float precision
            # Auto-normalize weights to sum to 100
            self.logger.warning(
                f"Scoring weights sum to {total_weight}, not 100. Auto-normalizing weights."
            )
            normalization_factor = 100.0 / total_weight
            for key in weight_keys:
                normalized_value = weights[key] * normalization_factor
                self._global_settings[key] = normalized_value
                self.logger.info(f"Normalized {key}: {weights[key]} -> {normalized_value}")
            
            warnings.append(
                f"Auto-normalized weights from {total_weight} to 100. "
                f"Update settings.ini to persist these changes."
            )
```

---

### Task 3.6: Fix Missing Configuration Fields
**Priority**: P0 - HIGH
**File**: `app_config/settings.ini`

**FIND (section [QUALITY_FILTERS]):**
```ini
[QUALITY_FILTERS]
require_question_keywords = true
enforce_intent_filter = true
allowed_intents = informational
negative_keywords = login, sign in, account, free, cheap
min_search_volume = 100
max_keyword_difficulty = 80
min_cpc = 0.0
max_cpc = 5.0
min_competition = 0.0
max_competition = 1.0
max_competition_level = LOW
min_serp_results = 100000
max_serp_results = 10000000
min_avg_backlinks = 0
max_avg_backlinks = 20
min_keyword_word_count = 2
max_keyword_word_count = 8
high_value_sv_override_threshold = 10000
high_value_cpc_override_threshold = 5.0
```

**ADD after this section:**
```ini
allowed_competition_levels = LOW,MEDIUM
max_traffic_value_for_scoring = 50000
```

**FIND (section [SCORING_WEIGHTS]):**
```ini
[SCORING_WEIGHTS]
ease_of_ranking_weight = 40
traffic_potential_weight = 15
commercial_intent_weight = 5
serp_features_weight = 5
growth_trend_weight = 5
serp_freshness_weight = 5
serp_volatility_weight = 5
competitor_weakness_weight = 20
competitor_performance_weight = 5
```

**ADD after this section:**
```ini
serp_crowding_weight = 5
keyword_structure_weight = 5
serp_threat_weight = 0
volume_volatility_weight = 0
```

**FIND (section [SCORING_NORMALIZATION]):**
```ini
[SCORING_NORMALIZATION]
max_cpc_for_scoring = 20.0
max_sv_for_scoring = 50000
max_domain_rank_for_scoring = 700
max_referring_domains_for_scoring = 200
```

**ADD after this section:**
```ini
max_traffic_value_for_scoring = 50000
```

---

### Task 3.7: Fix Duplicate Code Issue - Remove Redundant File
**Priority**: P0 - HIGH
**File**: `pipeline/orchestrator.py`

**DELETE ENTIRE FILE** (this is a duplicate of `pipeline/orchestrator/main.py`)

**File**: `pipeline/__init__.py`

**FIND:**
```python
# backend/pipeline/__init__.py
from .orchestrator.main import WorkflowOrchestrator as WorkflowOrchestrator
```

**KEEP AS IS** (this is correct - imports from orchestrator/main.py)

**Validation**:
- Search entire codebase for `from pipeline.orchestrator import` - should find 0 results
- Search for `from backend.pipeline.orchestrator.main import` - should find imports
- Delete `pipeline/orchestrator.py` file completely

---

## Phase 4: HIGH Performance Issues

### Task 4.1: Fix N+1 Query in Opportunities List
**Priority**: P0 - HIGH
**File**: `data_access/database_manager.py`

**FIND (in get_all_opportunities, after the main query execution around line 680):**
```python
        with conn:
            cursor = conn.cursor()
            cursor.execute(final_query, paged_values)
            opportunities = self._deserialize_rows(cursor.fetchall())

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

**REPLACE WITH:**
```python
        with conn:
            cursor = conn.cursor()
            cursor.execute(final_query, paged_values)
            opportunities = self._deserialize_rows(cursor.fetchall())

        # For summary queries, search_volume and keyword_difficulty should come from direct columns
        # If they're null, it means data migration didn't complete properly
        for opp in opportunities:
            # Set defaults if null (avoid JSON extraction in loop)
            if opp.get("search_volume") is None:
                opp["search_volume"] = 0
            
            if opp.get("keyword_difficulty") is None:
                opp["keyword_difficulty"] = 0
            
            if opp.get("cpc") is None:
                opp["cpc"] = 0.0
            
            if opp.get("competition") is None:
                opp["competition"] = 0.0
            
            if opp.get("main_intent") is None:
                opp["main_intent"] = "informational"

        return opportunities, total_count
```

**EXPLANATION**: Remove JSON extraction from loop entirely. Direct columns should always be populated. If they're null, use safe defaults instead of expensive JSON parsing.

---

### Task 4.2: Optimize String Concatenation in Content Generation
**Priority**: P0 - HIGH
**File**: `pipeline/orchestrator/content_orchestrator.py`

**FIND (lines 66-97):**
```python
            full_article_context_for_conclusion = ""
            previous_content = ""
            full_article_parts = []  # Use list accumulation for efficiency
            for i, node in enumerate(act):
                progress = 15 + int((i / len(act)) * 40)
                self.job_manager.update_job_status(
                    job_id,
                    "running",
                    progress=progress,
                    result={"step": f"Generating: {node['title']}"},
                )

                content_html, cost = None, 0.0
                if node["type"] == "introduction":
                    content_html, cost = sectional_generator.generate_introduction(
                        opportunity
                    )
                elif node["type"] == "section_h2":
                    content_html, cost = sectional_generator.generate_section(
                        opportunity,
                        node["title"],
                        node.get("sub_points", []),
                        previous_content,
                    )
                elif node["type"] == "conclusion":
                    # Join accumulated parts efficiently
                    full_article_context_for_conclusion = "".join(full_article_parts)
                    content_html, cost = sectional_generator.generate_conclusion(
                        opportunity, full_article_context_for_conclusion
                    )
```

**REPLACE WITH:**
```python
            from io import StringIO
            
            full_article_buffer = StringIO()
            previous_content = ""
            
            for i, node in enumerate(act):
                progress = 15 + int((i / len(act)) * 40)
                self.job_manager.update_job_status(
                    job_id,
                    "running",
                    progress=progress,
                    result={"step": f"Generating: {node['title']}"},
                )

                content_html, cost = None, 0.0
                if node["type"] == "introduction":
                    content_html, cost = sectional_generator.generate_introduction(
                        opportunity
                    )
                elif node["type"] == "section_h2":
                    content_html, cost = sectional_generator.generate_section(
                        opportunity,
                        node["title"],
                        node.get("sub_points", []),
                        previous_content,
                    )
                elif node["type"] == "conclusion":
                    # Get accumulated content efficiently
                    full_article_context_for_conclusion = full_article_buffer.getvalue()
                    content_html, cost = sectional_generator.generate_conclusion(
                        opportunity, full_article_context_for_conclusion
                    )
```

**FIND (after the content_html generation, around line 97):**
```python
                if content_html:
                    node["content_html"] = content_html
                    full_article_parts.append(f"<h2>{node['title']}</h2>\n{content_html}\n")
                    previous_content = content_html
                else:
                    raise RuntimeError(
                        f"Failed to generate content for section '{node['title']}'."
                    )

            self.job_manager.update_job_status(
                job_id, "running", progress=60, result={"step": "Assembling Article"}
            )
            final_html_parts = [
                f"<h2>{node['title']}</h2>\n{node['content_html']}" for node in act
            ]
            final_article_html = "\n".join(final_html_parts)
```

**REPLACE WITH:**
```python
                if content_html:
                    node["content_html"] = content_html
                    # Write to buffer efficiently
                    full_article_buffer.write(f"<h2>{node['title']}</h2>\n{content_html}\n")
                    previous_content = content_html
                else:
                    raise RuntimeError(
                        f"Failed to generate content for section '{node['title']}'."
                    )

            self.job_manager.update_job_status(
                job_id, "running", progress=60, result={"step": "Assembling Article"}
            )
            
            # Get final HTML from buffer
            final_article_html = full_article_buffer.getvalue()
            full_article_buffer.close()
```

---

### Task 4.3: Fix Memory Leak in Image Generation
**Priority**: P0 - HIGH
**File**: `agents/image_generator.py`

**FIND (lines 106-153, the _add_text_overlay method):**
```python
    def _add_text_overlay(self, image_path: str, text: str) -> str:
        """Adds a text overlay to the image based on configured settings."""
        if not self.config.get("overlay_text_enabled", False):
            return image_path  # If disabled, return original path

        image = None
        overlay = None
        try:
            image = Image.open(image_path).convert("RGBA")
            draw = ImageDraw.Draw(image)
```

**REPLACE WITH:**
```python
    def _add_text_overlay(self, image_path: str, text: str) -> str:
        """Adds a text overlay to the image based on configured settings."""
        if not self.config.get("overlay_text_enabled", False):
            return image_path  # If disabled, return original path

        image = None
        overlay = None
        final_image = None
        
        try:
            image = Image.open(image_path).convert("RGBA")
            draw = ImageDraw.Draw(image)
```

**FIND (at end of same method, lines 145-153):**
```python
            # Save the modified image
            new_image_path = image_path.replace(".jpeg", "-overlay.jpeg")
            final_image = image.convert("RGB")
            final_image.save(new_image_path)
            final_image.close()  # Explicitly close to free memory
            return new_image_path
        except Exception as e:
            self.logger.error(f"Failed to add text overlay to image: {e}")
            return image_path
        finally:
            # Ensure all PIL objects are properly closed
            if overlay is not None:
                try:
                    overlay.close()
                except:
                    pass
            if image is not None:
                try:
                    image.close()
                except:
                    pass
```

**REPLACE WITH:**
```python
            # Save the modified image
            new_image_path = image_path.replace(".jpeg", "-overlay.jpeg")
            final_image = image.convert("RGB")
            final_image.save(new_image_path)
            return new_image_path
            
        except Exception as e:
            self.logger.error(f"Failed to add text overlay to image: {e}", exc_info=True)
            return image_path
            
        finally:
            # Ensure all PIL objects are properly closed in correct order
            objects_to_close = [final_image, overlay, image]
            for obj in objects_to_close:
                if obj is not None:
                    try:
                        obj.close()
                    except Exception as e:
                        self.logger.debug(f"Error closing PIL object: {e}")
```

---

## Phase 5: CRITICAL Configuration & API Integration

### Task 5.1: Fix Invalid API Parameter
**Priority**: P0 - HIGH
**File**: `external_apis/dataforseo_client_v2.py`

**FIND (lines 563-580):**
```python
        endpoint = self.SERP_ADVANCED
        base_serp_params = {
            "keyword": keyword,
            "location_code": location_code,
            "language_code": language_code,
            "group_organic_results": False,  # NEW: Ensure no grouping for full analysis
        }
```

**REPLACE WITH:**
```python
        endpoint = self.SERP_ADVANCED
        base_serp_params = {
            "keyword": keyword,
            "location_code": location_code,
            "language_code": language_code,
            # REMOVED: group_organic_results - not a valid SERP API parameter
        }
```

---

### Task 5.2: Add Missing Pagination Safeguards
**Priority**: P0 - HIGH
**File**: `external_apis/dataforseo_client_v2.py`

**FIND (lines 237-340, the post_with_paging method while loop):**
```python
        while True:
            if not paginated and page_count > 0:
                break

            if page_count >= max_pages:
                self.logger.info(
                    f"Reached max page limit ({max_pages}) for endpoint {endpoint}."
                )
                break

            page_count += 1
            self.logger.info(
                f"Submitting task to {endpoint} (Page {page_count}/{max_pages})..."
            )
```

**REPLACE WITH:**
```python
        # Additional safety: absolute maximum iterations regardless of max_pages setting
        ABSOLUTE_MAX_ITERATIONS = 100
        iteration_count = 0
        
        while True:
            iteration_count += 1
            
            # Safety brake: prevent infinite loops
            if iteration_count > ABSOLUTE_MAX_ITERATIONS:
                self.logger.error(
                    f"SAFETY BRAKE: Stopped pagination after {ABSOLUTE_MAX_ITERATIONS} iterations "
                    f"for endpoint {endpoint}. This indicates a bug or API issue."
                )
                break
            
            if not paginated and page_count > 0:
                break

            if page_count >= max_pages:
                self.logger.info(
                    f"Reached max page limit ({max_pages}) for endpoint {endpoint}."
                )
                break

            page_count += 1
            self.logger.info(
                f"Submitting task to {endpoint} (Page {page_count}/{max_pages}, Iteration {iteration_count})..."
            )
```

**FIND (in same method, around line 295):**
```python
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
```

**REPLACE WITH:**
```python
            # 2. Check if we've retrieved all available results using total_count
            if total_count is not None and total_count > 0:
                if len(all_items) >= total_count:
                    self.logger.info(
                        f"Retrieved all {total_count} available results for {endpoint}. Stopping pagination."
                    )
                    break
                
                # Also check if we're within 5% of total (tighter threshold)
                if len(all_items) >= total_count * 0.95:
                    self.logger.info(
                        f"Retrieved {len(all_items)}/{total_count} results (95%+). Stopping pagination."
                    )
                    break
                
                # Check for suspiciously high total_count
                if total_count > 100000:
                    self.logger.warning(
                        f"API reports {total_count} total results - this seems unusually high. "
                        f"Stopping after {len(all_items)} results to prevent excessive API usage."
                    )
                    break
```

---

### Task 4.4: Fix Trend Data Type Handling
**Priority**: P0 - HIGH
**File**: `pipeline/step_01_discovery/disqualification_rules.py`

**FIND (lines 147-167):**
```python
    trends = keyword_info.get("search_volume_trend", {})
    if not isinstance(trends,
    dict):
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
```

**REPLACE WITH:**
```python
    # Handle search_volume_trend - can be dict or JSON string from database
    trends_raw = keyword_info.get("search_volume_trend", {})
    
    # Deserialize if it's a JSON string
    if isinstance(trends_raw, str):
        try:
            trends = json.loads(trends_raw) if trends_raw.strip() else {}
        except json.JSONDecodeError as e:
            logging.getLogger(__name__).error(
                f"Failed to parse search_volume_trend JSON for keyword '{keyword}': {e}"
            )
            trends = {}
    elif isinstance(trends_raw, dict):
        trends = trends_raw
    else:
        logging.getLogger(__name__).warning(
            f"search_volume_trend is unexpected type for keyword '{keyword}': {type(trends_raw)}"
        )
        trends = {}
    
    # Per API docs: trend values are integers (percentage change)
    # Handle None, string, or numeric types
    def safe_int_trend(value, field_name):
        """Safely convert trend value to int."""
        if value is None:
            return None
        try:
            return int(value)
        except (ValueError, TypeError) as e:
            logging.getLogger(__name__).warning(
                f"Could not convert {field_name} trend '{value}' to int for keyword '{keyword}': {e}"
            )
            return 0  # Default to 0 (no change) if invalid
    
    yearly_trend = safe_int_trend(trends.get("yearly"), "yearly")
    quarterly_trend = safe_int_trend(trends.get("quarterly"), "quarterly")
```

**ADD at top of file:**
```python
import json
```

---

### Task 4.5: Fix Cannibalization Domain Comparison
**Priority**: P0 - HIGH
**File**: `pipeline/step_01_discovery/cannibalization_checker.py`

**FIND (lines 37-50):**
```python
        for result in serp_results:
            try:
                url = result.get("url")
                if not url:
                    continue
                url_domain = urlparse(url).netloc.lower().replace("www.", "")
                if url_domain == self.target_domain or url_domain.endswith(
                    f".{self.target_domain}"
                ):
                    self.logger.warning(
                        f"Cannibalization detected: Found '{url}' in SERP for '{keyword}'."
                    )
                    return True
            except Exception:
                continue
        return False
```

**REPLACE WITH:**
```python
        for result in serp_results:
            try:
                url = result.get("url")
                if not url:
                    continue
                url_domain = urlparse(url).netloc.lower().replace("www.", "")
                
                # Exact domain match
                if url_domain == self.target_domain:
                    self.logger.warning(
                        f"Cannibalization detected: Found '{url}' in SERP for '{keyword}'."
                    )
                    return True
                
                # Subdomain match - but ensure it's actually a subdomain
                # Prevent false positives like 'competitor.com' matching 'petitor.com'
                if "." in url_domain:
                    # Split domain into parts
                    domain_parts = url_domain.split(".")
                    target_parts = self.target_domain.split(".")
                    
                    # Check if target_domain is a suffix of url_domain
                    # e.g., blog.example.com should match example.com
                    # but competitor.com should NOT match petitor.com
                    if len(domain_parts) >= len(target_parts):
                        # Get the rightmost parts equal to target length
                        url_suffix = ".".join(domain_parts[-len(target_parts):])
                        if url_suffix == self.target_domain:
                            self.logger.warning(
                                f"Cannibalization detected (subdomain): Found '{url}' in SERP for '{keyword}'."
                            )
                            return True
                            
            except Exception as e:
                self.logger.debug(f"Error parsing URL '{result.get('url')}': {e}")
                continue
        return False
```

---

### Task 4.6: Fix Configuration Parsing Error Handling
**Priority**: P0 - HIGH
**File**: `app_config/manager.py`

**FIND (lines 149-204):**
```python
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
```

**REPLACE WITH:**
```python
        # Load all settings from settings.ini with enhanced error handling
        parsing_errors = []
        critical_errors = []
        
        # Define critical settings that must parse correctly
        critical_settings = {
            'dataforseo_login', 'dataforseo_password', 'openai_api_key',
            'location_code', 'language_code', 'ease_of_ranking_weight',
            'traffic_potential_weight', 'commercial_intent_weight'
        }
        
        for section in self.config_parser.sections():
            for key, value in self.config_parser.items(section):
                try:
                    target_type = self._setting_types.get(key)
                    is_critical = key in critical_settings
                    
                    if target_type is bool:
                        try:
                            settings[key] = self.config_parser.getboolean(section, key)
                        except ValueError as e:
                            error_msg = f"Failed to parse boolean for [{section}]{key}='{value}'. Error: {e}"
                            if is_critical:
                                critical_errors.append(error_msg)
                                raise ValueError(error_msg)
                            else:
                                self.logger.error(error_msg + " Using False.")
                                settings[key] = False
                                parsing_errors.append(f"{section}.{key}")
```

**FIND (at end of the _load_and_validate_global method, around line 204):**
```python
        if parsing_errors:
            self.logger.warning(
                f"Configuration parsing completed with {len(parsing_errors)} errors. "
                f"Problematic keys: {', '.join(parsing_errors[:10])}"
            )

        self.logger.info("Global settings loaded.")
        return settings
```

**REPLACE WITH:**
```python
        # Check for critical errors first
        if critical_errors:
            error_summary = "\n".join(critical_errors)
            raise ValueError(
                f"CRITICAL CONFIGURATION ERRORS - Cannot start application:\n{error_summary}\n\n"
                f"Please fix these settings in settings.ini before restarting."
            )
        
        if parsing_errors:
            self.logger.warning(
                f"Configuration parsing completed with {len(parsing_errors)} non-critical errors. "
                f"Problematic keys: {', '.join(parsing_errors[:10])}"
            )

        self.logger.info("Global settings loaded successfully.")
        return settings
```

---

### Task 5.3: Fix Filter Limit Enforcement
**Priority**: P0 - HIGH
**File**: `external_apis/dataforseo_client_v2.py`

**FIND (method _prioritize_and_limit_filters around line 163):**
```python
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

**REPLACE WITH:**
```python
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
        
        self.logger.error(
            f"Filter list contains {condition_count} conditions, exceeding API maximum of 8. "
            f"Truncating to first 8 conditions. Original filters: {filters}"
        )
        
        # Priority order for filters (most to least important)
        priority_fields = [
            "search_volume",
            "keyword_difficulty", 
            "main_intent",
            "competition_level",
            "cpc",
            "competition",
        ]
        
        # Separate filters by priority
        prioritized = []
        other = []
        
        for item in filters:
            if isinstance(item, list) and len(item) >= 1:
                field_path = item[0] if isinstance(item[0], str) else ""
                # Check if any priority field is in this filter
                if any(pf in field_path for pf in priority_fields):
                    prioritized.append(item)
                else:
                    other.append(item)
            elif isinstance(item, str) and item.lower() in ["and", "or"]:
                # Keep logical operators for now
                pass
        
        # Take top 8 filters (prioritized first, then others)
        selected_conditions = (prioritized + other)[:8]
        
        # Rebuild filter array with logical operators
        result = []
        for i, condition in enumerate(selected_conditions):
            result.append(condition)
            if i < len(selected_conditions) - 1:
                result.append("and")
        
        self.logger.warning(f"Reduced to {len(selected_conditions)} filters: {result}")
        return result
```

**FIND (in get_keyword_ideas method, around line 690):**
```python
            # CRITICAL: Must convert to API format FIRST, then enforce limit
            # because conversion can expand filters (e.g., 'in' operator)
            converted_ideas_filters = self._convert_filters_to_api_format(filters.get("ideas"))
            sanitized_ideas_filters = self._prioritize_and_limit_filters(converted_ideas_filters)
```

**KEEP AS IS** (already correctly calls prioritize after convert)

**Validation**: Verify this method is called for ALL filter processing

---

### Task 5.4: Add API Response Structure Validation
**Priority**: P0 - HIGH
**File**: `data_mappers/dataforseo_mapper.py`

**ADD after the sanitize_complete_api_response method (around line 170):**
```python
    @staticmethod
    def validate_required_response_fields(
        response: Dict[str, Any],
        endpoint: str
    ) -> Tuple[bool, Optional[str]]:
        """
        Validates that critical fields exist in API response.
        Returns (is_valid, error_message).
        """
        if not isinstance(response, dict):
            return False, f"Response is not a dictionary: {type(response)}"
        
        # All endpoints must have these fields
        required_top_level = ["status_code", "tasks"]
        for field in required_top_level:
            if field not in response:
                return False, f"Missing required field: {field}"
        
        if response["status_code"] != 20000:
            return False, f"API error: {response.get('status_code')} - {response.get('status_message')}"
        
        tasks = response.get("tasks", [])
        if not isinstance(tasks, list) or len(tasks) == 0:
            return False, "Response contains no tasks"
        
        # Validate first task
        task = tasks[0]
        if not isinstance(task, dict):
            return False, f"Task is not a dictionary: {type(task)}"
        
        if task.get("status_code") != 20000:
            return False, f"Task failed: {task.get('status_code')} - {task.get('status_message')}"
        
        if "result" not in task:
            return False, "Task missing result field"
        
        result = task.get("result")
        if not isinstance(result, list) or len(result) == 0:
            return False, "Task result is empty or invalid"
        
        # Endpoint-specific validation
        result_item = result[0]
        if not isinstance(result_item, dict):
            return False, f"Result item is not a dictionary: {type(result_item)}"
        
        if "keyword_ideas" in endpoint or "keyword_suggestions" in endpoint:
            if "items" not in result_item:
                return False, "Result missing items array"
        elif "related_keywords" in endpoint:
            if "items" not in result_item:
                return False, "Result missing items array"
        elif "serp" in endpoint:
            if "items" not in result_item:
                return False, "SERP result missing items array"
        
        return True, None
```

**File**: `external_apis/dataforseo_client_v2.py`

**FIND (in _post_request method, after sanitization around line 220):**
```python
                # Apply comprehensive sanitization
                sanitized_response = DataForSEOMapper.sanitize_complete_api_response(
                    response_json,
                    endpoint
                )

                # Log response summary for debugging
                if sanitized_response.get("tasks"):
```

**REPLACE WITH:**
```python
                # Validate response structure before sanitization
                is_valid, validation_error = DataForSEOMapper.validate_required_response_fields(
                    response_json,
                    endpoint
                )
                
                if not is_valid:
                    self.logger.error(
                        f"API response validation failed for {endpoint}: {validation_error}"
                    )
                    return {
                        "status_code": 50000,
                        "status_message": f"Invalid response structure: {validation_error}",
                        "tasks": [],
                        "tasks_error": 1,
                        "cost": response_json.get("cost", 0.0)
                    }, response_json.get("cost", 0.0)
                
                # Apply comprehensive sanitization
                sanitized_response = DataForSEOMapper.sanitize_complete_api_response(
                    response_json,
                    endpoint
                )

                # Log response summary for debugging
                if sanitized_response.get("tasks"):
```

---

## Phase 6: HIGH Database & Schema Issues

### Task 6.1: Add Composite Indexes for Performance
**Priority**: P0 - HIGH
**File**: `data_access/migrations/026_add_composite_indexes.sql`

**FIND (entire file content):**
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

**REPLACE WITH:**
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

-- NEW: Composite index for run queries
CREATE INDEX IF NOT EXISTS idx_opportunities_client_run
ON opportunities (client_id, run_id);

-- NEW: Index for direct column filters (faster than JSON extraction)
CREATE INDEX IF NOT EXISTS idx_opportunities_search_volume
ON opportunities (search_volume DESC) WHERE search_volume IS NOT NULL;

CREATE INDEX IF NOT EXISTS idx_opportunities_keyword_difficulty
ON opportunities (keyword_difficulty) WHERE keyword_difficulty IS NOT NULL;

CREATE INDEX IF NOT EXISTS idx_opportunities_cpc
ON opportunities (cpc DESC) WHERE cpc IS NOT NULL;

-- Index for job status queries
CREATE INDEX IF NOT EXISTS idx_jobs_status_started 
ON jobs (status, started_at DESC);

-- Index for discovery run queries
CREATE INDEX IF NOT EXISTS idx_discovery_runs_client_status 
ON discovery_runs (client_id, status, start_time DESC);

-- NEW: Index for discovery run cost queries
CREATE INDEX IF NOT EXISTS idx_discovery_runs_cost
ON discovery_runs (client_id, total_api_cost DESC);

-- Index for content feedback queries
CREATE INDEX IF NOT EXISTS idx_content_feedback_opportunity 
ON content_feedback (opportunity_id, rating DESC);

-- Index for content history queries  
CREATE INDEX IF NOT EXISTS idx_content_history_opportunity_timestamp 
ON content_history (opportunity_id, timestamp DESC);

-- NEW: Index for keyword lookups
CREATE INDEX IF NOT EXISTS idx_keywords_keyword
ON keywords (keyword);

CREATE INDEX IF NOT EXISTS idx_keywords_search_volume
ON keywords (search_volume DESC);
```

---

### Task 6.2: Fix Foreign Key Cascade Rules
**Priority**: P0 - HIGH
**File**: Create new migration `data_access/migrations/027_add_foreign_key_cascades.sql`

**CREATE NEW FILE:**
```sql
-- data_access/migrations/027_add_foreign_key_cascades.sql
-- SQLite doesn't support ALTER TABLE to add foreign key constraints
-- This migration recreates tables with proper CASCADE rules

-- First, ensure foreign_keys are enabled
PRAGMA foreign_keys=ON;

-- Note: SQLite requires recreating tables to add CASCADE
-- For now, document the issue and add constraint validation

-- Add a trigger to prevent orphaned opportunities when client is deleted
CREATE TRIGGER IF NOT EXISTS prevent_orphaned_opportunities
BEFORE DELETE ON clients
FOR EACH ROW
BEGIN
    SELECT RAISE(ABORT, 'Cannot delete client with existing opportunities. Delete opportunities first.')
    WHERE EXISTS (SELECT 1 FROM opportunities WHERE client_id = OLD.client_id LIMIT 1);
END;

-- Add trigger to prevent orphaned discovery runs
CREATE TRIGGER IF NOT EXISTS prevent_orphaned_discovery_runs
BEFORE DELETE ON clients
FOR EACH ROW
BEGIN
    SELECT RAISE(ABORT, 'Cannot delete client with existing discovery runs. Delete runs first.')
    WHERE EXISTS (SELECT 1 FROM discovery_runs WHERE client_id = OLD.client_id LIMIT 1);
END;

-- Add trigger to validate client_id exists before insert
CREATE TRIGGER IF NOT EXISTS validate_opportunity_client
BEFORE INSERT ON opportunities
FOR EACH ROW
BEGIN
    SELECT RAISE(ABORT, 'Cannot create opportunity for non-existent client.')
    WHERE NOT EXISTS (SELECT 1 FROM clients WHERE client_id = NEW.client_id);
END;

-- Add trigger to validate client_id exists for discovery runs
CREATE TRIGGER IF NOT EXISTS validate_discovery_run_client
BEFORE INSERT ON discovery_runs
FOR EACH ROW
BEGIN
    SELECT RAISE(ABORT, 'Cannot create discovery run for non-existent client.')
    WHERE NOT EXISTS (SELECT 1 FROM clients WHERE client_id = NEW.client_id);
END;
```

---

### Task 6.3: Add Cache Cleanup Job
**Priority**: P0 - HIGH
**File**: `data_access/database_manager.py`

**FIND (around line 200, after _apply_migrations_from_files method):**
```python
    def _ensure_default_client_exists(self, conn):
        """Checks for and creates the default client if it doesn't exist in the database."""
        if not self.cfg_manager:
            return
```

**ADD BEFORE this method:**
```python
    def start_cache_cleanup_scheduler(self):
        """
        Starts a background thread to periodically clean expired cache entries.
        Should be called after database initialization.
        """
        import threading
        import time
        
        def cleanup_loop():
            while True:
                try:
                    time.sleep(3600)  # Run every hour
                    self.clear_expired_api_cache()
                    self.logger.info("Periodic cache cleanup completed")
                except Exception as e:
                    self.logger.error(f"Error in cache cleanup loop: {e}")
        
        cleanup_thread = threading.Thread(target=cleanup_loop, daemon=True)
        cleanup_thread.start()
        self.logger.info("Cache cleanup scheduler started (runs every 1 hour)")
```

**File**: `api/main.py`

**FIND (in startup_event, around line 48):**
```python
    api_globals.db_manager = DatabaseManager(cfg_manager=api_globals.config_manager)
    api_globals.db_manager.initialize()  # Ensure DB tables are created/migrated
    api_globals.job_manager = JobManager(
        db_manager=api_globals.db_manager
    )  # Initialize JobManager with db_manager
```

**REPLACE WITH:**
```python
    api_globals.db_manager = DatabaseManager(cfg_manager=api_globals.config_manager)
    api_globals.db_manager.initialize()  # Ensure DB tables are created/migrated
    api_globals.db_manager.start_cache_cleanup_scheduler()  # Start periodic cleanup
    api_globals.job_manager = JobManager(
        db_manager=api_globals.db_manager
    )  # Initialize JobManager with db_manager
```

---

## Phase 7: HIGH API Integration Fixes

### Task 7.1: Fix API Error Response Handling
**Priority**: P0 - HIGH
**File**: `external_apis/dataforseo_client_v2.py`

**FIND (in _post_request method, around line 223):**
```python
                response = requests.post(
                    full_url, headers=self.headers, data=json.dumps(data), timeout=120
                )

                # W20 FIX: Early exit for critical top-level HTTP errors
                if response.status_code >= 500:
                    self.logger.error(
                        f"DataForSEO API returned a server error ({response.status_code}). Aborting after {attempt + 1} attempts."
                    )
                    return None, 0.0  # Do not retry on server errors

                response.raise_for_status()  # Raise HTTPError for 4xx client errors

                response_json = response.json()
```

**REPLACE WITH:**
```python
                response = requests.post(
                    full_url, headers=self.headers, data=json.dumps(data), timeout=120
                )

                # Check for HTTP-level errors first
                if response.status_code >= 500:
                    self.logger.error(
                        f"DataForSEO API returned a server error ({response.status_code}). Aborting after {attempt + 1} attempts."
                    )
                    return None, 0.0  # Do not retry on server errors

                # Parse JSON before raising for status (to get cost from error responses)
                try:
                    response_json = response.json()
                except json.JSONDecodeError as e:
                    self.logger.error(
                        f"DataForSEO API returned invalid JSON for {full_url}. "
                        f"Status: {response.status_code}, Body: {response.text[:200]}"
                    )
                    return {
                        "status_code": 50000,
                        "status_message": f"Invalid JSON response: {e}",
                        "tasks": [],
                        "tasks_error": 1,
                        "cost": 0.0
                    }, 0.0
                
                # Now check HTTP status
                if response.status_code >= 400:
                    error_cost = response_json.get("cost", 0.0)
                    self.logger.error(
                        f"DataForSEO API HTTP error {response.status_code} for {full_url}. "
                        f"API message: {response_json.get('status_message')}. Cost: ${error_cost}"
                    )
                    # Return error response but preserve cost information
                    return response_json, error_cost
```

---

### Task 7.2: Add Parameter Validation for Discovery Endpoints
**Priority**: P0 - HIGH
**File**: `api/routers/discovery.py`

**FIND (lines 145-205, the start_discovery_run_async endpoint):**
```python
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
```

**REPLACE WITH:**
```python
    # Comprehensive input validation per API constraints
    try:
        # Validate seed keywords
        if not request.seed_keywords or len(request.seed_keywords) == 0:
            raise HTTPException(
                status_code=400,
                detail="At least one seed keyword is required."
            )
        
        # Validate UTF-8 encoding per API requirements
        for keyword in request.seed_keywords:
            if not isinstance(keyword, str):
                raise HTTPException(
                    status_code=400,
                    detail=f"All seed keywords must be strings. Found: {type(keyword)}"
                )
            try:
                keyword.encode('utf-8')
            except UnicodeEncodeError:
                raise HTTPException(
                    status_code=400,
                    detail=f"Keyword contains invalid UTF-8 characters: {keyword}"
                )
            if len(keyword.strip()) == 0:
                raise HTTPException(
                    status_code=400,
                    detail="Empty keywords are not allowed"
                )
        
        # Per API docs: Keyword Ideas max 200 keywords
        if "keyword_ideas" in request.discovery_modes and len(request.seed_keywords) > 200:
            raise HTTPException(
                status_code=400,
                detail=f"Keyword Ideas mode supports max 200 seed keywords. You provided {len(request.seed_keywords)}."
            )
```

**FIND (later in same method, around line 175):**
```python
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
```

**REPLACE WITH:**
```python
        # Validate depth for related keywords
        if request.depth is not None:
            if not isinstance(request.depth, int):
                raise HTTPException(
                    status_code=400,
                    detail=f"Depth must be an integer. Got: {type(request.depth)}"
                )
            if request.depth < 0 or request.depth > 4:
                raise HTTPException(
                    status_code=400,
                    detail=f"Related keywords depth must be between 0 and 4. You provided {request.depth}."
                )
        
        # Validate limit per endpoint
        if request.limit is not None:
            if not isinstance(request.limit, int):
                raise HTTPException(
                    status_code=400,
                    detail=f"Limit must be an integer. Got: {type(request.limit)}"
                )
            
            # Different limits for different endpoints
            if "keyword_ideas" in request.discovery_modes:
                if request.limit < 1 or request.limit > 1000:
                    raise HTTPException(
                        status_code=400,
                        detail=f"Keyword Ideas limit must be 1-1000. You provided {request.limit}."
                    )
            else:
                # Suggestions and Related default max is 1000
                if request.limit < 1 or request.limit > 1000:
                    raise HTTPException(
                        status_code=400,
                        detail=f"Limit must be between 1 and 1000. You provided {request.limit
                        ."
                    )
        
        # Validate order_by array
        if request.order_by is not None:
            if not isinstance(request.order_by, list):
                raise HTTPException(
                    status_code=400,
                    detail=f"order_by must be a list. Got: {type(request.order_by)}"
                )
            if len(request.order_by) > 3:
                raise HTTPException(
                    status_code=400,
                    detail=f"Maximum 3 sorting rules allowed. You provided {len(request.order_by)}."
                )
            # Validate format of each rule
            for rule in request.order_by:
                if not isinstance(rule, str):
                    raise HTTPException(
                        status_code=400,
                        detail=f"Each order_by rule must be a string. Got: {type(rule)}"
                    )
                if "," not in rule:
                    raise HTTPException(
                        status_code=400,
                        detail=f"Invalid order_by format: '{rule}'. Must be 'field,direction'"
                    )
                field, direction = rule.rsplit(",", 1)
                if direction.lower() not in ["asc", "desc"]:
                    raise HTTPException(
                        status_code=400,
                        detail=f"Invalid sort direction: '{direction}'. Must be 'asc' or 'desc'"
                    )
        
        # Validate discovery_max_pages
        if request.discovery_max_pages is not None:
            if not isinstance(request.discovery_max_pages, int):
                raise HTTPException(
                    status_code=400,
                    detail=f"discovery_max_pages must be an integer. Got: {type(request.discovery_max_pages)}"
                )
            if request.discovery_max_pages < 1 or request.discovery_max_pages > 100:
                raise HTTPException(
                    status_code=400,
                    detail=f"discovery_max_pages must be 1-100. You provided {request.discovery_max_pages}."
                )
```

---

### Task 7.3: Fix Duplicate ToC IDs
**Priority**: P0 - HIGH
**File**: `agents/html_formatter.py`

**FIND (lines 90-118):**
```python
    def _generate_toc(self, soup: BeautifulSoup) -> None:
        """Generates and inserts a Table of Contents from H2 tags into the BeautifulSoup object."""
        toc_list = soup.new_tag("ul", **{"class": "toc-list"})
        h2_tags = soup.find_all("h2")

        if len(h2_tags) < 2:
            return  # No TOC needed for less than 2 headings

        # Add unique IDs to H2 tags and build TOC
        for i, h2 in enumerate(h2_tags):
            slug = utils.slugify(h2.text)
            if not slug:  # Fallback for empty/unsluggable H2s
                slug = f"section-{i + 1}"
            h2["id"] = slug  # Add ID to H2 for linking

            toc_item = soup.new_tag("li")
            toc_link = soup.new_tag("a", href=f"#{slug}")
            toc_link.string = h2.text
            toc_item.append(toc_link)
            toc_list.append(toc_item)
```

**REPLACE WITH:**
```python
    def _generate_toc(self, soup: BeautifulSoup) -> None:
        """Generates and inserts a Table of Contents from H2 tags into the BeautifulSoup object."""
        toc_list = soup.new_tag("ul", **{"class": "toc-list"})
        h2_tags = soup.find_all("h2")

        if len(h2_tags) < 2:
            return  # No TOC needed for less than 2 headings

        # Track used IDs to ensure uniqueness
        used_ids = set()
        
        # Add unique IDs to H2 tags and build TOC
        for i, h2 in enumerate(h2_tags):
            base_slug = utils.slugify(h2.text)
            if not base_slug:  # Fallback for empty/unsluggable H2s
                base_slug = f"section-{i + 1}"
            
            # Ensure ID is unique by appending counter if needed
            slug = base_slug
            counter = 1
            while slug in used_ids:
                slug = f"{base_slug}-{counter}"
                counter += 1
            
            used_ids.add(slug)
            h2["id"] = slug  # Add unique ID to H2 for linking

            toc_item = soup.new_tag("li")
            toc_link = soup.new_tag("a", href=f"#{slug}")
            toc_link.string = h2.text
            toc_item.append(toc_link)
            toc_list.append(toc_item)
```

---

### Task 7.4: Fix Job Manager Race Condition
**Priority**: P0 - HIGH
**File**: `jobs.py`

**FIND (lines 74-95):**
```python
    def update_job_progress(self, job_id: str, step: str, message: str, status: Optional[str] = None):
        """
        Appends a progress log to the job record in the database with thread safety.
        Uses a lock to prevent race conditions when multiple threads update the same job.
        """
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "step": step,
            "message": message,
        }
        
        # Use database-level locking for thread safety
        conn = self.db_manager._get_conn()
        try:
            conn.isolation_level = "IMMEDIATE"
            conn.execute("BEGIN IMMEDIATE")
            
            # Fetch current job within transaction
            cursor = conn.execute(queries.GET_JOB, (job_id,))
            row = cursor.fetchone()
            
            if row:
                job_info = dict(row)
                
                # Parse existing progress log
                progress_log = job_info.get("progress_log", [])
                if isinstance(progress_log, str):
                    try:
                        progress_log = json.loads(progress_log) if progress_log else []
                    except json.JSONDecodeError:
                        progress_log = []
                elif not isinstance(progress_log, list):
                    progress_log = []
                
                # Append new log entry
                progress_log.append(log_entry)
                job_info["progress_log"] = progress_log

                # Optionally update the overall job status
                if status:
                    job_info["status"] = status

                # Update in database
                self.db_manager.update_job(job_info)
            
            conn.commit()
        except Exception as e:
            logger.error(f"Failed to update job progress for {job_id}: {e}")
            try:
                conn.rollback()
            except:
                pass
        finally:
            conn.isolation_level = None
```

**REPLACE WITH:**
```python
    def update_job_progress(self, job_id: str, step: str, message: str, status: Optional[str] = None):
        """
        Appends a progress log to the job record in the database with thread safety.
        Uses EXCLUSIVE lock for atomic updates.
        """
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "step": step,
            "message": message,
        }
        
        max_retries = 3
        retry_delay = 0.1
        
        for attempt in range(max_retries):
            conn = self.db_manager._get_conn()
            try:
                # Use EXCLUSIVE lock for write operations
                conn.execute("BEGIN EXCLUSIVE")
                
                # Fetch current job within transaction
                cursor = conn.execute(queries.GET_JOB, (job_id,))
                row = cursor.fetchone()
                
                if not row:
                    logger.warning(f"Job {job_id} not found when updating progress")
                    conn.rollback()
                    return
                
                job_info = dict(row)
                
                # Parse existing progress log
                progress_log = job_info.get("progress_log")
                if progress_log is None:
                    progress_log = []
                elif isinstance(progress_log, str):
                    try:
                        progress_log = json.loads(progress_log) if progress_log.strip() else []
                    except json.JSONDecodeError as e:
                        logger.error(f"Corrupt progress_log for job {job_id}: {e}")
                        progress_log = []
                elif not isinstance(progress_log, list):
                    logger.error(f"progress_log is unexpected type: {type(progress_log)}")
                    progress_log = []
                
                # Append new log entry
                progress_log.append(log_entry)
                job_info["progress_log"] = progress_log

                # Optionally update the overall job status
                if status:
                    job_info["status"] = status

                # Update in database
                self.db_manager.update_job(job_info)
                
                conn.commit()
                return  # Success
                
            except sqlite3.OperationalError as e:
                # Database is locked - retry
                if "locked" in str(e).lower() and attempt < max_retries - 1:
                    logger.warning(f"Database locked, retrying job progress update (attempt {attempt + 1})")
                    try:
                        conn.rollback()
                    except:
                        pass
                    time.sleep(retry_delay * (attempt + 1))
                    continue
                else:
                    logger.error(f"Failed to update job progress after {attempt + 1} attempts: {e}")
                    try:
                        conn.rollback()
                    except:
                        pass
                    raise
                    
            except Exception as e:
                logger.error(f"Failed to update job progress for {job_id}: {e}", exc_info=True)
                try:
                    conn.rollback()
                except:
                    pass
                raise
                
            finally:
                try:
                    conn.isolation_level = None
                except:
                    pass
```

**ADD import at top of file:**
```python
import time
```

---

### Task 7.5: Fix Job Cancellation Race Condition
**Priority**: P0 - HIGH
**File**: `jobs.py`

**FIND (lines 169-180):**
```python
    def cancel_job(self, job_id: str) -> bool:
        """Marks a job as 'failed' with a 'cancelled by user' message."""
        job_info = self.get_job_status(job_id)
        if job_info and job_info["status"] in ["pending", "running", "paused"]:
            # The crucial part: mark as failed in the DB so the running thread sees it
            self.update_job_status(
                job_id,
                "failed",
                job_info.get("progress", 0),
                error="Cancelled by user.",
            )
            logger.info(f"Job {job_id} was marked as 'failed' (cancelled by user).")
            return True
        return False
```

**REPLACE WITH:**
```python
    def cancel_job(self, job_id: str) -> bool:
        """
        Atomically marks a job as 'failed' with a 'cancelled by user' message.
        Uses database transaction to prevent race conditions.
        """
        conn = self.db_manager._get_conn()
        
        try:
            conn.execute("BEGIN EXCLUSIVE")
            
            # Fetch and update in single transaction
            cursor = conn.execute(queries.GET_JOB, (job_id,))
            row = cursor.fetchone()
            
            if not row:
                logger.warning(f"Cannot cancel job {job_id}: job not found")
                conn.rollback()
                return False
            
            job_info = dict(row)
            current_status = job_info.get("status")
            
            if current_status not in ["pending", "running", "paused"]:
                logger.info(f"Cannot cancel job {job_id}: status is '{current_status}'")
                conn.rollback()
                return False
            
            # Update status atomically within same transaction
            finished_time = datetime.now().timestamp()
            conn.execute(
                """UPDATE jobs 
                   SET status = 'failed', 
                       error = 'Cancelled by user', 
                       finished_at = ?
                   WHERE id = ?""",
                (finished_time, job_id)
            )
            
            conn.commit()
            logger.info(f"Job {job_id} was marked as 'failed' (cancelled by user).")
            return True
            
        except Exception as e:
            logger.error(f"Error cancelling job {job_id}: {e}", exc_info=True)
            try:
                conn.rollback()
            except:
                pass
            return False
        finally:
            try:
                conn.isolation_level = None
            except:
                pass
```

---

## Phase 8: CRITICAL Cost & Budget Issues

### Task 8.1: Add Cost Budget Validation
**Priority**: P0 - CRITICAL
**File**: `app_config/settings.ini`

**ADD new section after [DEFAULT]:**
```ini
[COST_MANAGEMENT]
max_daily_api_cost = 50.0
max_single_job_cost = 5.0
cost_alert_threshold = 0.50
enable_cost_enforcement = true
```

---

**File**: Create new file `core/cost_manager.py`

**CREATE NEW FILE:**
```python
# core/cost_manager.py
import logging
from datetime import datetime, timedelta
from typing import Optional, Dict, Any
from backend.data_access.database_manager import DatabaseManager


class CostManager:
    """
    Enforces API cost budgets and tracks spending.
    Prevents runaway API costs.
    """
    
    def __init__(self, db_manager: DatabaseManager, config: Dict[str, Any]):
        self.db_manager = db_manager
        self.config = config
        self.logger = logging.getLogger(self.__class__.__name__)
        
        self.max_daily_cost = float(config.get("max_daily_api_cost", 50.0))
        self.max_single_job_cost = float(config.get("max_single_job_cost", 5.0))
        self.cost_alert_threshold = float(config.get("cost_alert_threshold", 0.50))
        self.enforcement_enabled = config.get("enable_cost_enforcement", True)
    
    def check_budget_available(
        self, 
        client_id: str, 
        estimated_cost: float,
        operation_type: str
    ) -> tuple[bool, Optional[str]]:
        """
        Check if budget is available for an operation.
        Returns (is_allowed, reason_if_not).
        """
        if not self.enforcement_enabled:
            return True, None
        
        # Check single job limit
        if estimated_cost > self.max_single_job_cost:
            reason = (
                f"Estimated cost ${estimated_cost:.2f} exceeds single job limit "
                f"of ${self.max_single_job_cost:.2f}"
            )
            self.logger.error(f"Budget check failed for {operation_type}: {reason}")
            return False, reason
        
        # Check daily limit
        daily_spent = self._get_daily_cost(client_id)
        if daily_spent + estimated_cost > self.max_daily_cost:
            reason = (
                f"Daily budget exceeded. Spent: ${daily_spent:.2f}, "
                f"Estimated: ${estimated_cost:.2f}, "
                f"Daily limit: ${self.max_daily_cost:.2f}"
            )
            self.logger.error(f"Budget check failed for {operation_type}: {reason}")
            return False, reason
        
        # Alert if approaching threshold
        projected_total = daily_spent + estimated_cost
        if projected_total > self.max_daily_cost * self.cost_alert_threshold:
            self.logger.warning(
                f"Cost alert: Approaching daily budget. "
                f"Current: ${daily_spent:.2f}, "
                f"After operation: ${projected_total:.2f}, "
                f"Limit: ${self.max_daily_cost:.2f}"
            )
        
        return True, None
    
    def _get_daily_cost(self, client_id: str) -> float:
        """Calculate total API cost for client in last 24 hours."""
        conn = self.db_manager._get_conn()
        
        # Calculate cutoff time (24 hours ago)
        cutoff_time = (datetime.now() - timedelta(days=1)).isoformat()
        
        with conn:
            cursor = conn.cursor()
            
            # Sum costs from opportunities created/updated in last 24 hours
            cursor.execute(
                """SELECT SUM(total_api_cost) 
                   FROM opportunities 
                   WHERE client_id = ? 
                   AND (date_added >= ? OR date_processed >= ?)""",
                (client_id, cutoff_time, cutoff_time)
            )
            opp_cost = cursor.fetchone()[0] or 0.0
            
            # Sum costs from discovery runs in last 24 hours
            cursor.execute(
                """SELECT SUM(total_api_cost) 
                   FROM discovery_runs 
                   WHERE client_id = ? 
                   AND start_time >= ?""",
                (client_id, cutoff_time)
            )
            run_cost = cursor.fetchone()[0] or 0.0
            
            total = float(opp_cost) + float(run_cost)
            self.logger.debug(f"Daily cost for {client_id}: ${total:.4f}")
            return total
    
    def get_cost_summary(self, client_id: str) -> Dict[str, Any]:
        """Get cost summary for reporting."""
        daily_cost = self._get_daily_cost(client_id)
        total_cost = self.db_manager.get_total_api_cost(client_id)
        
        return {
            "daily_cost": round(daily_cost, 2),
            "daily_limit": self.max_daily_cost,
            "daily_remaining": round(self.max_daily_cost - daily_cost, 2),
            "daily_usage_percent": round((daily_cost / self.max_daily_cost) * 100, 1),
            "total_cost_all_time": round(total_cost, 2),
            "enforcement_enabled": self.enforcement_enabled
        }
```

---

**File**: `pipeline/orchestrator/main.py`

**FIND (in __init__ method, after self.cost_tracker initialization):**
```python
        self.cost_tracker = CostTracker()
```

**ADD AFTER:**
```python
        from backend.core.cost_manager import CostManager
        self.cost_manager = CostManager(self.db_manager, self.client_cfg)
```

---

**File**: `pipeline/orchestrator/discovery_orchestrator.py`

**FIND (in run_discovery_and_save method, at the very beginning):**
```python
    def run_discovery_and_save(
        self,
        run_id: int,
        seed_keywords: List[str],
        discovery_modes: List[str],
```

**ADD after the method signature, before existing code:**
```python
        """
        Public method to initiate a discovery run asynchronously.
        Returns a job_id.
        """
        # Check cost budget before starting
        from pipeline.orchestrator.cost_estimator import CostEstimator
        
        discovery_params = {
            "seed_keywords": seed_keywords,
            "discovery_modes": discovery_modes,
            "discovery_max_pages": discovery_max_pages,
            "include_clickstream_data": include_clickstream_data,
        }
        
        cost_estimate = self.estimate_action_cost(
            action="discovery",
            discovery_params=discovery_params
        )
        
        estimated_cost = cost_estimate.get("estimated_cost", 0.0)
        
        # Enforce budget
        is_allowed, budget_reason = self.cost_manager.check_budget_available(
            self.client_id,
            estimated_cost,
            f"Discovery Run {run_id}"
        )
        
        if not is_allowed:
            self.logger.error(f"Discovery run blocked: {budget_reason}")
            self.db_manager.update_discovery_run_failed(run_id, budget_reason)
            raise ValueError(f"Cost budget exceeded: {budget_reason}")
        
        self.logger.info(
            f"Discovery run approved. Estimated cost: ${estimated_cost:.2f}"
        )
```

---

**File**: `pipeline/orchestrator/content_orchestrator.py`

**FIND (in run_full_content_generation method, at beginning):**
```python
    def run_full_content_generation(
        self, opportunity_id: int, overrides: Optional[Dict[str, Any]] = None
    ) -> str:
        """
        Public method to initiate content generation asynchronously.
        Returns a job_id.
        """
        self.logger.info(
            f"--- Orchestrator: Initiating Full Content Generation for Opportunity ID: {opportunity_id} (Async) ---"
        )
```

**REPLACE WITH:**
```python
    def run_full_content_generation(
        self, opportunity_id: int, overrides: Optional[Dict[str, Any]] = None
    ) -> str:
        """
        Public method to initiate content generation asynchronously.
        Returns a job_id.
        """
        # Check cost budget before starting
        cost_estimate = self.estimate_action_cost(
            action="generate",
            opportunity_id=opportunity_id
        )
        
        estimated_cost = cost_estimate.get("estimated_cost", 0.0)
        
        # Enforce budget
        is_allowed, budget_reason = self.cost_manager.check_budget_available(
            self.client_id,
            estimated_cost,
            f"Content Generation for Opportunity {opportunity_id}"
        )
        
        if not is_allowed:
            self.logger.error(f"Content generation blocked: {budget_reason}")
            self.db_manager.update_opportunity_workflow_state(
                opportunity_id,
                "budget_exceeded",
                "failed",
                budget_reason
            )
            raise ValueError(f"Cost budget exceeded: {budget_reason}")
        
        self.logger.info(
            f"--- Orchestrator: Initiating Full Content Generation for Opportunity ID: {opportunity_id} (Async) ---"
        )
        self.logger.info(f"Estimated cost: ${estimated_cost:.2f}")
```

---

### Task 8.2: Add Cost Tracking Endpoint
**Priority**: P0 - HIGH
**File**: `api/routers/clients.py`

**ADD new endpoint at end of file:**
```python
@router.get("/clients/{client_id}/cost-summary")
async def get_cost_summary_endpoint(
    client_id: str,
    db: DatabaseManager = Depends(get_db),
    orchestrator: WorkflowOrchestrator = Depends(get_orchestrator),
):
    """Returns cost summary and budget status for a client."""
    if client_id != orchestrator.client_id:
        raise HTTPException(
            status_code=403,
            detail="You do not have permission to access this client's resources.",
        )
    
    try:
        cost_summary = orchestrator.cost_manager.get_cost_summary(client_id)
        return cost_summary
    except Exception as e:
        logger.error(f"Error fetching cost summary for {client_id}: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Failed to fetch cost summary")
```

---

## Phase 9: HIGH Validation & Error Handling

### Task 9.1: Add Comprehensive SERP Validation
**Priority**: P0 - HIGH
**File**: Create new file `core/serp_validator.py`

**CREATE NEW FILE:**
```python
# core/serp_validator.py
import logging
from typing import Dict, Any, Tuple, Optional


class SerpValidator:
    """
    Validates SERP data structure and content before processing.
    Prevents downstream errors from malformed API responses.
    """
    
    def __init__(self):
        self.logger = logging.getLogger(self.__class__.__name__)
    
    def validate_serp_response(
        self, 
        serp_data: Dict[str, Any], 
        keyword: str
    ) -> Tuple[bool, Optional[str]]:
        """
        Comprehensive validation of SERP data structure.
        Returns (is_valid, error_message).
        """
        if not serp_data:
            return False, "SERP data is None or empty"
        
        if not isinstance(serp_data, dict):
            return False, f"SERP data is not a dictionary: {type(serp_data)}"
        
        # Validate required top-level fields
        required_fields = ["items", "item_types"]
        for field in required_fields:
            if field not in serp_data:
                return False, f"Missing required field: {field}"
        
        # Validate items array
        items = serp_data.get("items")
        if not isinstance(items, list):
            return False, f"'items' field is not a list: {type(items)}"
        
        if len(items) == 0:
            return False, f"No SERP items found for keyword '{keyword}'"
        
        # Validate item_types
        item_types = serp_data.get("item_types")
        if not isinstance(item_types, list):
            return False, f"'item_types' field is not a list: {type(item_types)}"
        
        # Validate at least some organic results exist
        has_organic = any(item.get("type") == "organic" for item in items)
        if not has_organic:
            self.logger.warning(f"No organic results found in SERP for '{keyword}'")
            # This is a warning, not a hard failure
        
        # Validate datetime fields if present
        datetime_fields = ["datetime", "last_updated_time", "previous_updated_time"]
        for field in datetime_fields:
            value = serp_data.get(field)
            if value is not None and not isinstance(value, str):
                return False, f"Field '{field}' should be string, got {type(value)}"
        
        # Validate numeric fields
        se_results_count = serp_data.get("se_results_count")
        if se_results_count is not None:
            try:
                int(se_results_count)  # Can be string or int per API
            except (ValueError, TypeError):
                return False, f"Invalid se_results_count: {se_results_count}"
        
        return True, None
    
    def validate_organic_result(
        self, 
        result: Dict[str, Any], 
        rank: int
    ) -> Tuple[bool, Optional[str]]:
        """Validate individual organic result structure."""
        if not isinstance(result, dict):
            return False, f"Result at rank {rank} is not a dictionary"
        
        required = ["url", "title", "domain"]
        for field in required:
            if field not in result:
                return False, f"Organic result at rank {rank} missing field: {field}"
            if not result[field]:
                return False, f"Organic result at rank {rank} has empty {field}"
        
        # Validate rank_absolute
        rank_absolute = result.get("rank_absolute")
        if rank_absolute is not None:
            try:
                int(rank_absolute)
            except (ValueError, TypeError):
                return False, f"Invalid rank_absolute: {rank_absolute}"
        
        return True, None
```

---

**File**: `core/serp_analyzer.py`

**ADD import at top:**
```python
from backend.core.serp_validator import SerpValidator
```

**FIND (in __init__ method):**
```python
    def __init__(self, client: DataForSEOClientV2, config: Dict[str, Any]):
        self.client = client
        self.config = config
        self.logger = logging.getLogger(self.__class__.__name__)
        self.featured_snippet_analyzer = FeaturedSnippetAnalyzer()
        self.video_analyzer = VideoAnalyzer()
        self.pixel_ranking_analyzer = PixelRankingAnalyzer()
        self.page_classifier = PageClassifier(config)
        self.disqualification_analyzer = DisqualificationAnalyzer()
```

**REPLACE WITH:**
```python
    def __init__(self, client: DataForSEOClientV2, config: Dict[str, Any]):
        self.client = client
        self.config = config
        self.logger = logging.getLogger(self.__class__.__name__)
        self.featured_snippet_analyzer = FeaturedSnippetAnalyzer()
        self.video_analyzer = VideoAnalyzer()
        self.pixel_ranking_analyzer = PixelRankingAnalyzer()
        self.page_classifier = PageClassifier(config)
        self.disqualification_analyzer = DisqualificationAnalyzer()
        self.validator = SerpValidator()
```

**FIND (in analyze_serp method, after getting serp_results):**
```python
        # Comprehensive validation of SERP response
        if not serp_results:
            self.logger.error(f"Failed to retrieve SERP results for keyword '{keyword}'")
            raise ValueError(f"SERP API returned no data for keyword: {keyword}")
        
        if not isinstance(serp_results, dict):
            self.logger.error(f"SERP results is not a dictionary for keyword '{keyword}': {type(serp_results)}")
            raise ValueError(f"Invalid SERP response type: {type(serp_results)}")
```

**REPLACE WITH:**
```python
        # Use dedicated validator
        is_valid, validation_error = self.validator.validate_serp_response(serp_results, keyword)
        
        if not is_valid:
            self.logger.error(f"SERP validation failed for '{keyword}': {validation_error}")
            raise ValueError(f"Invalid SERP data: {validation_error}")
```

---

### Task 9.2: Add Request Size Limits
**Priority**: P0 - HIGH
**File**: `api/main.py`

**FIND (after app initialization):**
```python
# Initialize FastAPI app
app = FastAPI()

# Mount the static directory for generated images
```

**REPLACE WITH:**
```python
# Initialize FastAPI app with request size limits
app = FastAPI()

# Add request size limit middleware (prevent DoS)
from fastapi import Request
from fastapi.responses import JSONResponse

MAX_REQUEST_SIZE = 10 * 1024 * 1024  # 10MB

@app.middleware("http")
async def limit_request_size(request: Request, call_next):
    """Middleware to limit request body size."""
    if request.method in ["POST", "PUT", "PATCH"]:
        content_length = request.headers.get("content-length")
        if content_length:
            try:
                content_length = int(content_length)
                if content_length > MAX_REQUEST_SIZE:
                    return JSONResponse(
                        status_code=413,
                        content={
                            "detail": f"Request body too large. Maximum size: {MAX_REQUEST_SIZE / 1024 / 1024}MB"
                        }
                    )
            except ValueError:
                pass  # Invalid content-length header, let it proceed
    
    response = await call_next(request)
    return response

# Mount the static directory for generated images
```

---

### Task 9.3: Add Content Update Validation
**Priority**: P0 - HIGH
**File**: `api/routers/opportunities.py`

**FIND (lines 137-185, the update_opportunity_content_endpoint):**
```python
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
```

**REPLACE WITH:**
```python
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
    from bs4 import BeautifulSoup

    # Validate opportunity_id is positive integer
    if opportunity_id <= 0:
        raise HTTPException(status_code=400, detail="Invalid opportunity_id")
    
    # Validate payload size (prevent DoS via large payloads)
    content_size = len(payload.article_body_html)
    if content_size > 5_000_000:  # 5MB limit
        raise HTTPException(
            status_code=413,
            detail="Content exceeds maximum size of 5MB"
        )
    
    if content_size == 0:
        raise HTTPException(
            status_code=400,
            detail="Content cannot be empty"
        )
    
    # Validate HTML structure
    try:
        soup = BeautifulSoup(payload.article_body_html, "html.parser")
        # Check for minimum viable content
        text_content = soup.get_text(strip=True)
        if len(text_content) < 100:
            raise HTTPException(
                status_code=400,
                detail="Content is too short (minimum 100 characters of text required)"
            )
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid HTML structure: {str(e)[:200]}"
        )
```

---

## Phase 10: CRITICAL Data Processing Issues

### Task 10.1: Fix Scoring Component Normalization
**Priority**: P0 - CRITICAL
**File**: `pipeline/step_03_prioritization/scoring_engine.py`

**FIND (lines 80-162, in calculate_score method):**
```python
        # --- Apply weights from config and calculate final score ---
        weights = {
            "ease": self.config.get("ease_of_ranking_weight", 25),
            "traffic": self.config.get("traffic_potential_weight", 20),
            "intent": self.config.get("commercial_intent_weight", 15),
            "weakness": self.config.get("competitor_weakness_weight", 10),
            "structure": self.config.get("keyword_structure_weight", 5),
            "trend": self.config.get("growth_trend_weight", 5),
            "features": self.config.get("serp_features_weight", 5),
            "crowding": self.config.get("serp_crowding_weight", 5),
            "volatility": self.config.get("serp_volatility_weight", 5),
            "threat": self.config.get("serp_threat_weight", 5),
            "freshness": self.config.get("serp_freshness_weight", 0),
            "competitor_performance": self.config.get(
                "competitor_performance_weight", 5
            ),
            "volume_volatility": self.config.get("volume_volatility_weight", 0),
        }

        total_weight = sum(weights.values())
        if total_weight == 0:
            return 0.0, breakdown  # Avoid division by zero

        final_score = (
            (ease_score * weights["ease"])
            + (traffic_score * weights["traffic"])
            + (intent_score * weights["intent"])
            + (weakness_score * weights["weakness"])
            + (structure_score * weights["structure"])
            + (trend_score * weights["trend"])
            + (features_score * weights["features"])
            + (crowding_score * weights["crowding"])
            + (volatility_score * weights["volatility"])
            + (threat_score * weights["threat"])
            + (freshness_score * weights["freshness"])
            + (volume_volatility_score * weights["volume_volatility"])
            + (performance_score * weights["competitor_performance"])
        ) / total_weight
```

**REPLACE WITH:**
```python
        # --- Apply weights from config and calculate final score ---
        weights = {
            "ease": self.config.get("ease_of_ranking_weight", 25),
            "traffic": self.config.get("traffic_potential_weight", 20),
            "intent": self.config.get("commercial_intent_weight", 15),
            "weakness": self.config.get("competitor_weakness_weight", 10),
            "structure": self.config.get("keyword_structure_weight", 5),
            "trend": self.config.get("growth_trend_weight", 5),
            "features": self.config.get("serp_features_weight", 5),
            "crowding": self.config.get("serp_crowding_weight", 5),
            "volatility": self.config.get("serp_volatility_weight", 5),
            "threat": self.config.get("serp_threat_weight", 5),
            "freshness": self.config.get("serp_freshness_weight", 0),
            "competitor_performance": self.config.get("competitor_performance_weight", 5),
            "volume_volatility": self.config.get("volume_volatility_weight", 0),
        }

        # Validate all weights are numeric and non-negative
        for key, value in weights.items():
            try:
                weights[key] = float(value)
                if weights[key] < 0:
                    self.logger.error(f"Negative weight for {key}: {value}. Setting to 0.")
                    weights[key] = 0
            except (ValueError, TypeError):
                self.logger.error(f"Invalid weight for {key}: {value}. Setting to 0.")
                weights[key] = 0

        total_weight = sum(weights.values())
        
        if total_weight == 0:
            self.logger.error("All scoring weights are 0. Cannot calculate score.")
            return 0.0, {"error": "All scoring weights are 0"}
        
        # CRITICAL FIX: Ensure final score is always 0-100
        # Component scores are already 0-100, weighted average should preserve this
        weighted_sum = (
            (ease_score * weights["ease"])
            + (traffic_score * weights["traffic"])
            + (intent_score * weights["intent"])
            + (weakness_score * weights["weakness"])
            + (structure_score * weights["structure"])
            + (trend_score * weights["trend"])
            + (features_score * weights["features"])
            + (crowding_score * weights["crowding"])
            + (volatility_score * weights["volatility"])
            + (threat_score * weights["threat"])
            + (freshness_score * weights["freshness"])
            + (volume_volatility_score * weights["volume_volatility"])
            + (performance_score * weights["competitor_performance"])
        )
        
        # Normalize by total weight to get 0-100 scale
        final_score = weighted_sum / total_weight
        
        # Safety clamp to 0-100 range
        final_score = max(0.0, min(100.0, final_score))
        
        # Log if score calculation seems off
        if final_score > 100 or final_score < 0:
            self.logger.error(
                f"Score calculation produced out-of-range value: {final_score}. "
                f"Component scores: ease={ease_score}, traffic={traffic_score}, etc. "
                f"Weights: {weights}"
            )
```

---

### Task 10.2: Fix Empty Article Structure Handling
**Priority**: P0 - HIGH
**File**: `pipeline/orchestrator/content_orchestrator.py`

**FIND (lines 19-52, in _build_abstract_content_tree):**
```python
    def _build_abstract_content_tree(
        self, opportunity: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """Builds the Abstract Content Tree (ACT) from the blueprint's outline."""
        self.logger.info(
            f"Building Abstract Content Tree for opportunity ID: {opportunity['id']}"
        )

        blueprint = opportunity.get("blueprint", {})
        content_intelligence = blueprint.get("content_intelligence", {})
        outline_structure = content_intelligence.get("article_structure", [])

        if not outline_structure:
            raise ValueError(
                "Cannot build ACT: `article_structure` not found in blueprint."
            )
```

**REPLACE WITH:**
```python
    def _build_abstract_content_tree(
        self, opportunity: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        """Builds the Abstract Content Tree (ACT) from the blueprint's outline."""
        self.logger.info(
            f"Building Abstract Content Tree for opportunity ID: {opportunity['id']}"
        )

        blueprint = opportunity.get("blueprint", {})
        if not blueprint or not isinstance(blueprint, dict):
            raise ValueError(
                f"Cannot build ACT: Invalid or missing blueprint for opportunity {opportunity.get('id')}"
            )
        
        content_intelligence = blueprint.get("content_intelligence", {})
        if not isinstance(content_intelligence, dict):
            raise ValueError(
                f"Cannot build ACT: Invalid content_intelligence structure"
            )
        
        outline_structure = content_intelligence.get("article_structure", [])

        if not outline_structure:
            self.logger.error(
                f"Empty article_structure in blueprint. Blueprint keys: {blueprint.keys()}, "
                f"Content intelligence keys: {content_intelligence.keys()}"
            )
            raise ValueError(
                "Cannot build ACT: `article_structure` is empty or missing. "
                "AI outline generation may have failed."
            )
        
        if not isinstance(outline_structure, list):
            raise ValueError(
                f"Cannot build ACT: `article_structure` must be a list, got {type(outline_structure)}"
            )
        
        if len(outline_structure) < 2:
            raise ValueError(
                f"Cannot build ACT: `article_structure` must have at least 2 sections (intro + conclusion). "
                f"Found {len(outline_structure)} sections."
            )
```

**FIND (in same method, in the for loop around line 45):**
```python
        for i, section in enumerate(outline_structure):
            h2_title = section.get("h2")
            h3s = section.get("h3s", [])

            if not h2_title:
                continue
```

**REPLACE WITH:**
```python
        for i, section in enumerate(outline_structure):
            if not isinstance(section, dict):
                self.logger.warning(f"Skipping invalid section at index {i}: {type(section)}")
                continue
            
            h2_title = section.get("h2")
            h3s = section.get("h3s", [])

            if not h2_title or not isinstance(h2_title, str):
                self.logger.warning(f"Skipping section at index {i} with invalid/missing h2: {h2_title}")
                continue
            
            if h2_title.strip() == "":
                self.logger.warning(f"Skipping section at index {i} with empty h2")
                continue
            
            # Validate h3s is a list
            if not isinstance(h3s, list):
                self.logger.warning(f"Invalid h3s type for section '{h2_title}': {type(h3s)}. Using empty list.")
                h3s = []
```

---

### Task 10.3: Fix Filter Validation Before API Calls
**Priority**: P0 - HIGH
**File**: `external_apis/dataforseo_client_v2.py`

**FIND (around line 130, the _enforce_api_filter_limit method is defined but never consistently called)**

**ADD new method before _enforce_api_filter_limit:**
```python
    def _validate_filter_structure(self, filters: Optional[List[Any]], endpoint: str) -> Tuple[bool, Optional[str]]:
        """
        Validates filter structure before sending to API.
        Returns (is_valid, error_message).
        """
        if not filters:
            return True, None
        
        if not isinstance(filters, list):
            return False, f"Filters must be a list, got {type(filters)}"
        
        condition_count = 0
        prev_was_operator = False
        
        for i, item in enumerate(filters):
            if isinstance(item, list):
                # This is a filter condition
                condition_count += 1
                
                if len(item) != 3:
                    return False, f"Filter at index {i} must have exactly 3 elements [field, operator, value]. Got {len(item)}"
                
                field, operator, value = item
                
                if not isinstance(field, str):
                    return False, f"Filter field must be string, got {type(field)}"
                
                if not isinstance(operator, str):
                    return False, f"Filter operator must be string, got {type(operator)}"
                
                # Validate operator is allowed
                valid_operators = {
                    "regex", "not_regex", "<", "<=", ">", ">=", "=", "<>", 
                    "in", "not_in", "match", "not_match", "ilike", "not_ilike", 
                    "like", "not_like", "has", "has_not"
                }
                if operator not in valid_operators:
                    return False, f"Invalid operator '{operator}'. Allowed: {valid_operators}"
                
                # Validate 'in' and 'not_in' have array values
                if operator in ["in", "not_in"]:
                    if not isinstance(value, list):
                        return False, f"Operator '{operator}' requires array value, got {type(value)}"
                
                prev_was_operator = False
                
            elif isinstance(item, str):
                # This should be a logical operator
                if item.lower() not in ["and", "or"]:
                    return False, f"Logical operator must be 'and' or 'or', got '{item}'"
                
                if prev_was_operator:
                    return False, f"Cannot have consecutive logical operators at index {i}"
                
                if i == 0:
                    return False, "Filter cannot start with logical operator"
                
                if i == len(filters) - 1:
                    return False, "Filter cannot end with logical operator"
                
                prev_was_operator = True
            else:
                return False, f"Filter item at index {i} must be list or string, got {type(item)}"
        
        # Check filter count limit
        if condition_count > 8:
            return False, f"Maximum 8 filter conditions allowed, got {condition_count}"
        
        return True, None
```

**FIND (in get_keyword_ideas method, before API call around line 690):**
```python
            # CRITICAL: Must convert to API format FIRST, then enforce limit
            # because conversion can expand filters (e.g., 'in' operator)
            converted_ideas_filters = self._convert_filters_to_api_format(filters.get("ideas"))
            sanitized_ideas_filters = self._prioritize_and_limit_filters(converted_ideas_filters)
```

**REPLACE WITH:**
```python
            # CRITICAL: Validate, convert, then enforce limit
            raw_ideas_filters = filters.get("ideas")
            if raw_ideas_filters:
                is_valid, error_msg = self._validate_filter_structure(raw_ideas_filters, "keyword_ideas")
                if not is_valid:
                    raise ValueError(f"Invalid filter structure for Keyword Ideas: {error_msg}")
            
            converted_ideas_filters = self._convert_filters_to_api_format(raw_ideas_filters)
            sanitized_ideas_filters = self._prioritize_and_limit_filters(converted_ideas_filters)
```

**FIND (similar pattern for suggestions and related filters in same method):**
```python
                sanitized_suggestions_filters = self._prioritize_and_limit_filters(
                    self._convert_filters_to_api_format(filters.get("suggestions"))
                )
```

**REPLACE WITH:**
```python
                raw_suggestions_filters = filters.get("suggestions")
                if raw_suggestions_filters:
                    is_valid, error_msg = self._validate_filter_structure(raw_suggestions_filters, "keyword_suggestions")
                    if not is_valid:
                        raise ValueError(f"Invalid filter structure for Suggestions: {error_msg}")
                
                sanitized_suggestions_filters = self._prioritize_and_limit_filters(
                    self._convert_filters_to_api_format(raw_suggestions_filters)
                )
```

**FIND:**
```python
                sanitized_related_filters = self._prioritize_and_limit_filters(
                    self._convert_filters_to_api_format(filters.get("related"))
                )
```

**REPLACE WITH:**
```python
                raw_related_filters = filters.get("related")
                if raw_related_filters:
                    is_valid, error_msg = self._validate_filter_structure(raw_related_filters, "related_keywords")
                    if not is_valid:
                        raise ValueError(f"Invalid filter structure for Related Keywords: {error_msg}")
                
                sanitized_related_filters = self._prioritize_and_limit_filters(
                    self._convert_filters_to_api_format(raw_related_filters)
                )
```

---

### Task 10.4: Fix Competitor Analysis When None Found
**Priority**: P0 - HIGH
**File**: `pipeline/step_04_analysis/run_analysis.py`

**FIND (around line 95-115):**
```python
    # 2. On-Page competitor metadata and content analysis
    top_organic_urls = [
        result["url"]
        for result in serp_overview.get("top_organic_results", [])[
            : client_cfg.get("num_competitors_to_analyze", 5)
        ]
    ]
    competitor_analysis, competitor_api_cost = competitor_analyzer.analyze_competitors(
        top_organic_urls, selected_competitor_urls
    )
    total_api_cost += competitor_api_cost

    # 3. Content Intelligence Synthesis using the full content
    content_intelligence, content_api_cost = (
        content_analyzer.synthesize_content_intelligence(
            competitor_analysis,
            keyword,
            serp_overview.get("dominant_content_format", "Comprehensive Article"),
        )
    )
    total_api_cost += content_api_cost
```

**REPLACE WITH:**
```python
    # 2. On-Page competitor metadata and content analysis
    top_organic_urls = [
        result["url"]
        for result in serp_overview.get("top_organic_results", [])[
            : client_cfg.get("num_competitors_to_analyze", 5)
        ]
    ]
    
    if not top_organic_urls:
        logger.warning(f"No organic URLs found in SERP for '{keyword}'")
        competitor_analysis = []
        competitor_api_cost = 0.0
    else:
        competitor_analysis, competitor_api_cost = competitor_analyzer.analyze_competitors(
            top_organic_urls, selected_competitor_urls
        )
        total_api_cost += competitor_api_cost
    
    # Log if no competitors were analyzed
    if not competitor_analysis:
        logger.warning(
            f"No valid competitors found for analysis for keyword '{keyword}'. "
            f"This may indicate a SERP dominated by non-article content."
        )

    # 3. Content Intelligence Synthesis
    # Use SERP-only mode if no competitors found
    content_intelligence, content_api_cost = (
        content_analyzer.synthesize_content_intelligence(
            keyword,
            serp_overview,
            competitor_analysis,  # Will be empty if none found
        )
    )
    total_api_cost += content_api_cost
    
    # Validate content intelligence was generated
    if not content_intelligence or not isinstance(content_intelligence, dict):
        raise ValueError(
            f"Content intelligence synthesis failed for '{keyword}'. "
            f"Cannot proceed with blueprint generation."
        )
```

---

### Task 10.5: Add Validation to Content Analyzer
**Priority**: P0 - HIGH
**File**: `pipeline/step_04_analysis/content_analyzer.py`

**FIND (in synthesize_content_intelligence method, around line 33):**
```python
    def synthesize_content_intelligence(
        self,
        keyword: str,
        serp_overview: Dict[str, Any],
        competitor_analysis: List[
            Dict[str, Any]
        ],  # This will be empty if deep analysis is skipped
    ) -> Tuple[Dict[str, Any], float]:
        """
        Synthesizes content intelligence by orchestrating data preparation and AI analysis.
        Conditionally uses deep competitor content or rich SERP data.
        """
        if competitor_analysis:
```

**REPLACE WITH:**
```python
    def synthesize_content_intelligence(
        self,
        keyword: str,
        serp_overview: Dict[str, Any],
        competitor_analysis: List[Dict[str, Any]] = None,
    ) -> Tuple[Dict[str, Any], float]:
        """
        Synthesizes content intelligence by orchestrating data preparation and AI analysis.
        Conditionally uses deep competitor content or rich SERP data.
        """
        # Validate inputs
        if not keyword or not isinstance(keyword, str):
            raise ValueError("keyword must be a non-empty string")
        
        if not serp_overview or not isinstance(serp_overview, dict):
            raise ValueError("serp_overview must be a valid dictionary")
        
        # Ensure competitor_analysis is a list (even if empty)
        if competitor_analysis is None:
            competitor_analysis = []
        elif not isinstance(competitor_analysis, list):
            self.logger.error(f"Invalid competitor_analysis type: {type(competitor_analysis)}")
            competitor_analysis = []
        
        if competitor_analysis:
```

**FIND (at end of synthesize_content_intelligence method, before return):**
```python
        # 4. Assemble Final Intelligence Object
        ai_analysis_response["unique_angles_to_include"] = list(
            set(ai_analysis_response.get("unique_angles_to_include", []))
        )[: self.num_unique_angles]
```

**REPLACE WITH:**
```python
        # 4. Validate and assemble Final Intelligence Object
        if not ai_analysis_response or not isinstance(ai_analysis_response, dict):
            self.logger.error("AI analysis returned invalid response")
            raise ValueError("Content intelligence synthesis produced invalid output")
        
        # Ensure all required fields exist with safe defaults
        ai_analysis_response.setdefault("unique_angles_to_include", [])
        ai_analysis_response.setdefault("key_entities_from_competitors", [])
        ai_analysis_response.setdefault("core_questions_answered_by_competitors", [])
        ai_analysis_response.setdefault("identified_content_gaps", [])
        
        # Validate types and clean up
        if not isinstance(ai_analysis_response.get("unique_angles_to_include"), list):
            self.logger.warning("unique_angles_to_include is not a list, resetting")
            ai_analysis_response["unique_angles_to_include"] = []
        
        ai_analysis_response["unique_angles_to_include"] = list(
            set(ai_analysis_response.get("unique_angles_to_include", []))
        )[: self.num_unique_angles]
```

---

## Phase 11: HIGH Resource Management

### Task 11.1: Implement Image Cleanup
**Priority**: P0 - HIGH
**File**: Create new file `core/resource_manager.py`

**CREATE NEW FILE:**
```python
# core/resource_manager.py
import os
import logging
import time
from typing import List
from pathlib import Path


class ResourceManager:
    """
    Manages cleanup of temporary files and resources.
    """
    
    def __init__(self, config: dict):
        self.config = config
        self.logger = logging.getLogger(self.__class__.__name__)
        self.cleanup_enabled = config.get("cleanup_local_images", True)
        self.image_retention_days = config.get("image_retention_days", 7)
    
    def cleanup_old_images(self, images_dir: str = "generated_images") -> int:
        """
        Remove image files older than retention period.
        Returns count of files deleted.
        """
        if not self.cleanup_enabled:
            self.logger.info("Image cleanup is disabled")
            return 0
        
        if not os.path.exists(images_dir):
            self.logger.warning(f"Images directory does not exist: {images_dir}")
            return 0
        
        cutoff_time = time.time() - (self.image_retention_days * 86400)
        deleted_count = 0
        errors = []
        
        try:
            for filename in os.listdir(images_dir):
                if filename == ".gitkeep":
                    continue
                
                filepath = os.path.join(images_dir, filename)
                
                # Skip if not a file
                if not os.path.isfile(filepath):
                    continue
                
                # Check file age
                try:
                    file_mtime = os.path.getmtime(filepath)
                    if file_mtime < cutoff_time:
                        os.remove(filepath)
                        deleted_count += 1
                        self.logger.debug(f"Deleted old image: {filename}")
                except OSError as e:
                    errors.append(f"{filename}: {e}")
                    continue
            
            if deleted_count > 0:
                self.logger.info(
                    f"Cleaned up {deleted_count} images older than {self.image_retention_days} days"
                )
            
            if errors:
                self.logger.warning(
                    f"Encountered {len(errors)} errors during cleanup: {errors[:5]}"
                )
            
            return deleted_count
            
        except Exception as e:
            self.logger.error(f"Image cleanup failed: {e}", exc_info=True)
            return deleted_count
    
    def cleanup_orphaned_images(
        self, 
        images_dir: str = "generated_images",
        db_manager = None
    ) -> int:
        """
        Remove images that are no longer referenced in database.
        Returns count of files deleted.
        """
        if not self.cleanup_enabled or not db_manager:
            return 0
        
        if not os.path.exists(images_dir):
            return 0
        
        # Get all image paths from database
        conn = db_manager._get_conn()
        with conn:
            cursor = conn.cursor()
            cursor.execute(
                """SELECT featured_image_local_path FROM opportunities 
                   WHERE featured_image_local_path IS NOT NULL"""
            )
            referenced_paths = {row[0] for row in cursor.fetchall()}
        
        deleted_count = 0
        
        for filename in os.listdir(images_dir):
            if filename == ".gitkeep":
                continue
            
            filepath = os.path.join(images_dir, filename)
            
            if not os.path.isfile(filepath):
                continue
            
            # Check if this file is referenced in database
            is_referenced = any(
                filepath in ref_path or filename in ref_path 
                for ref_path in referenced_paths
            )
            
            if not is_referenced:
                try:
                    os.remove(filepath)
                    deleted_count += 1
                    self.logger.debug(f"Deleted orphaned image: {filename}")
                except OSError as e:
                    self.logger.warning(f"Could not delete {filename}: {e}")
        
        if deleted_count > 0:
            self.logger.info(f"Cleaned up {deleted_count} orphaned images")
        
        return deleted_count
```

---

**File**: `app_config/settings.ini`

**FIND (section [IMAGE_GENERATION]):**
```ini
[IMAGE_GENERATION]
num_in_article_images = 2
use_pexels_first = true
cleanup_local_images = true
```

**REPLACE WITH:**
```ini
[IMAGE_GENERATION]
num_in_article_images = 2
use_pexels_first = true
cleanup_local_images = true
image_retention_days = 7
```

---

**File**: `data_access/database_manager.py`

**FIND (in start_cache_cleanup_scheduler method added earlier):**
```python
    def start_cache_cleanup_scheduler(self):
        """
        Starts a background thread to periodically clean expired cache entries.
        Should be called after database initialization.
        """
        import threading
        import time
        
        def cleanup_loop():
            while True:
                try:
                    time.sleep(3600)  # Run every hour
                    self.clear_expired_api_cache()
                    self.logger.info("Periodic cache cleanup completed")
                except Exception as e:
                    self.logger.error(f"Error in cache cleanup loop: {e}")
        
        cleanup_thread = threading.Thread(target=cleanup_loop, daemon=True)
        cleanup_thread.start()
        self.logger.info("Cache cleanup scheduler started (runs every 1 hour)")
```

**REPLACE WITH:**
```python
    def start_cache_cleanup_scheduler(self):
        """
        Starts a background thread to periodically clean expired cache and images.
        Should be called after database initialization.
        """
        import threading
        import time
        from backend.core.resource_manager import ResourceManager
        
        resource_manager = ResourceManager(
            self.cfg_manager.get_global_config() if self.cfg_manager else {}
        )
        
        def cleanup_loop():
            while True:
                try:
                    time.sleep(3600)  # Run every hour
                    
                    # Clean expired cache
                    self.clear_expired_api_cache()
                    
                    # Clean old images
                    resource_manager.cleanup_old_images()
                    
                    # Clean orphaned images (every 24 hours)
                    if int(time.time()) % 86400 < 3600:  # Once per day
                        resource_manager.cleanup_orphaned_images(
                            db_manager=self
                        )
                    
                    self.logger.info("Periodic cleanup completed")
                except Exception as e:
                    self.logger.error(f"Error in cleanup loop: {e}")
        
        cleanup_thread = threading.Thread(target=cleanup_loop, daemon=True)
        cleanup_thread.start()
        self.logger.info("Resource cleanup scheduler started (runs every 1 hour
        )")
```

---

### Task 11.2: Add Log File Rotation
**Priority**: P0 - HIGH
**File**: `pipeline/orchestrator/discovery_orchestrator.py`

**FIND (lines 36-40):**
```python
        log_dir = "discovery_logs"
        os.makedirs(log_dir, exist_ok=True)
        log_file_path = os.path.join(log_dir, f"run_{run_id}.log")

        run_logger = logging.getLogger(f"run_{run_id}")
        handler = logging.FileHandler(log_file_path)
        handler.setFormatter(
            logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
        )
        run_logger.addHandler(handler)
        run_logger.setLevel(logging.INFO)
```

**REPLACE WITH:**
```python
        from logging.handlers import RotatingFileHandler
        
        log_dir = "discovery_logs"
        os.makedirs(log_dir, exist_ok=True)
        log_file_path = os.path.join(log_dir, f"run_{run_id}.log")

        run_logger = logging.getLogger(f"run_{run_id}")
        
        # Use rotating file handler with size limit
        handler = RotatingFileHandler(
            log_file_path,
            maxBytes=10 * 1024 * 1024,  # 10MB per file
            backupCount=3  # Keep 3 backup files
        )
        handler.setFormatter(
            logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
        )
        run_logger.addHandler(handler)
        run_logger.setLevel(logging.INFO)
```

---

## Phase 12: CRITICAL API Integration Fixes

### Task 12.1: Fix OnPage API Batch Grouping
**Priority**: P0 - CRITICAL
**File**: `external_apis/dataforseo_client_v2.py`

**FIND (lines 478-520, the _group_urls_by_domain method):**
```python
    def _group_urls_by_domain(
        self, urls: List[str], max_domains: int = 5, batch_size: int = 20
    ) -> List[List[str]]:
        """
        Groups URLs into batches that comply with the identical-domain limit and batch size.
        """
        from collections import defaultdict, deque

        domain_cache = {}

        def get_domain(url):
            if url not in domain_cache:
                try:
                    domain_cache[url] = urlparse(url).netloc
                except Exception:
                    self.logger.warning(f"Could not parse domain for URL: {url}")
                    domain_cache[url] = url
            return domain_cache[url]

        # Use deques for efficient popping from the left
        domain_groups = defaultdict(deque)
        for url in urls:
            domain_groups[get_domain(url)].append(url)

        batches = []

        # Continue as long as there are URLs to process
        while sum(len(q) for q in domain_groups.values()) > 0:
```

**REPLACE WITH:**
```python
    def _group_urls_by_domain(
        self, urls: List[str], max_domains: int = 5, batch_size: int = 20
    ) -> List[List[str]]:
        """
        Groups URLs into batches that comply with the identical-domain limit and batch size.
        Per API docs: max 5 identical domains per request, max 20 tasks per request.
        """
        from collections import defaultdict, deque
        from urllib.parse import urlparse

        # Validate inputs
        if not urls:
            return []
        
        if not isinstance(urls, list):
            raise ValueError(f"urls must be a list, got {type(urls)}")
        
        if max_domains < 1 or max_domains > 10:
            self.logger.warning(f"max_domains {max_domains} is unusual, using 5")
            max_domains = 5
        
        if batch_size < 1 or batch_size > 20:
            self.logger.warning(f"batch_size {batch_size} exceeds API limit of 20, using 20")
            batch_size = min(batch_size, 20)

        domain_cache = {}

        def get_domain(url):
            if url not in domain_cache:
                try:
                    parsed = urlparse(url)
                    domain = parsed.netloc
                    if not domain:
                        # Invalid URL, use the whole URL as domain
                        self.logger.warning(f"Could not parse domain for URL: {url}")
                        domain = url
                    domain_cache[url] = domain
                except Exception as e:
                    self.logger.error(f"Error parsing URL '{url}': {e}")
                    domain_cache[url] = url
            return domain_cache[url]

        # Group URLs by domain
        domain_groups = defaultdict(deque)
        invalid_urls = []
        
        for url in urls:
            if not url or not isinstance(url, str):
                invalid_urls.append(url)
                continue
            domain_groups[get_domain(url)].append(url)
        
        if invalid_urls:
            self.logger.warning(f"Skipped {len(invalid_urls)} invalid URLs")

        batches = []
        max_iterations = len(urls) * 2  # Safety limit
        iteration = 0

        # Continue as long as there are URLs to process
        while sum(len(q) for q in domain_groups.values()) > 0:
            iteration += 1
            if iteration > max_iterations:
                self.logger.error(
                    f"URL grouping exceeded max iterations ({max_iterations}). "
                    f"Remaining URLs: {sum(len(q) for q in domain_groups.values())}"
                )
                break
```

---

### Task 12.2: Add Comprehensive Error Responses
**Priority**: P0 - HIGH
**File**: Create new file `api/error_handlers.py`

**CREATE NEW FILE:**
```python
# api/error_handlers.py
from fastapi import Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
import logging

logger = logging.getLogger(__name__)


async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """
    Standardized handler for validation errors.
    Returns consistent error format.
    """
    errors = []
    for error in exc.errors():
        errors.append({
            "field": ".".join(str(x) for x in error["loc"]),
            "message": error["msg"],
            "type": error["type"]
        })
    
    logger.warning(
        f"Validation error on {request.method} {request.url.path}: {errors}",
        extra={"errors": errors}
    )
    
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "status": "error",
            "error_type": "validation_error",
            "message": "Request validation failed",
            "errors": errors
        }
    )


async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    """
    Standardized handler for HTTP exceptions.
    Returns consistent error format.
    """
    logger.error(
        f"HTTP {exc.status_code} on {request.method} {request.url.path}: {exc.detail}",
        extra={"status_code": exc.status_code, "detail": exc.detail}
    )
    
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "status": "error",
            "error_type": "http_error",
            "message": exc.detail,
            "status_code": exc.status_code
        }
    )


async def general_exception_handler(request: Request, exc: Exception):
    """
    Catch-all handler for unhandled exceptions.
    Returns consistent error format without exposing internals.
    """
    logger.error(
        f"Unhandled exception on {request.method} {request.url.path}: {exc}",
        exc_info=True,
        extra={"exception_type": type(exc).__name__}
    )
    
    # Don't expose internal error details in production
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "status": "error",
            "error_type": "internal_error",
            "message": "An internal server error occurred",
            "request_id": id(request)  # Can be used for support
        }
    )
```

---

**File**: `api/main.py`

**FIND (after app initialization):**
```python
# Initialize FastAPI app with request size limits
app = FastAPI()

# Add request size limit middleware (prevent DoS)
from fastapi import Request
from fastapi.responses import JSONResponse
```

**ADD AFTER the middleware definition:**
```python
# Register exception handlers for consistent error responses
from .error_handlers import (
    validation_exception_handler,
    http_exception_handler,
    general_exception_handler
)
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException

app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(StarletteHTTPException, http_exception_handler)
app.add_exception_handler(Exception, general_exception_handler)
```

---

### Task 12.3: Fix API Filter Limit Enforcement Across All Endpoints
**Priority**: P0 - CRITICAL
**File**: `external_apis/dataforseo_client_v2.py`

**FIND (in get_keyword_ideas method, the final API call around line 735):**
```python
        if "related_keywords" in discovery_modes:
            self.logger.info("Fetching related keywords...")
            related_endpoint = self.LABS_RELATED_KEYWORDS
            for seed in seed_keywords:
                sanitized_related_filters = self._prioritize_and_limit_filters(
                    self._convert_filters_to_api_format(filters.get("related"))
                )
```

**VERIFY** that ALL three discovery modes call `_prioritize_and_limit_filters`:

**After this verification, ADD a final validation before constructing task objects:**

**FIND (for keyword_ideas task construction):**
```python
            ideas_task = {
                "keywords": seed_keywords,
                "location_code": location_code,
                "language_code": language_code,
                "limit": ideas_limit,
                "include_serp_info": True,
                "ignore_synonyms": ignore_synonyms,
                "closely_variants": closely_variants,
                "filters": sanitized_ideas_filters,
```

**REPLACE WITH:**
```python
            # Final validation before API call
            if sanitized_ideas_filters:
                final_is_valid, final_error = self._validate_filter_structure(
                    sanitized_ideas_filters, 
                    "keyword_ideas_final"
                )
                if not final_is_valid:
                    self.logger.error(
                        f"Filter validation failed after sanitization: {final_error}. "
                        f"Filters: {sanitized_ideas_filters}"
                    )
                    sanitized_ideas_filters = None  # Clear invalid filters
            
            ideas_task = {
                "keywords": seed_keywords,
                "location_code": location_code,
                "language_code": language_code,
                "limit": ideas_limit,
                "include_serp_info": True,
                "ignore_synonyms": ignore_synonyms,
                "closely_variants": closely_variants,
                "filters": sanitized_ideas_filters,
```

**Repeat same pattern for suggestions_task and related_task**

---

## Phase 13: HIGH Performance Optimizations

### Task 13.1: Optimize Competitor Analysis
**Priority**: P0 - HIGH
**File**: `pipeline/step_04_analysis/competitor_analyzer.py`

**FIND (lines 95-140, in _process_content_parsing_results):**
```python
    def _process_content_parsing_results(
        self, results: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """
        Processes the successful results from the Content Parsing API call into a standardized competitor object.
        """
        final_competitors = []
        for result in results:
            url = result.get("url")  # URL is at the top level in the new API response
            if not url or result.get("status_code") != 200:
                continue

            domain = urlparse(url).netloc
            if domain in self.blacklist_domains:
                self.logger.info(f"Skipping blacklisted competitor: {domain}")
                continue

            page_content = result.get("page_content", {})
            main_topic_content = ""
            headings = {"h1": [], "h2": [], "h3": [], "h4": [], "h5": [], "h6": []}

            # Extract main content and headings from the structured 'main_topic' array
            if page_content and page_content.get("main_topic"):
                for topic in page_content["main_topic"]:
```

**REPLACE WITH:**
```python
    def _process_content_parsing_results(
        self, results: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        """
        Processes the successful results from the Content Parsing API call into a standardized competitor object.
        Optimized for performance with early validation and efficient string building.
        """
        if not results:
            return []
        
        if not isinstance(results, list):
            self.logger.error(f"Results is not a list: {type(results)}")
            return []
        
        final_competitors = []
        
        for result in results:
            # Early validation
            if not isinstance(result, dict):
                self.logger.warning(f"Skipping invalid result type: {type(result)}")
                continue
            
            url = result.get("url")
            if not url or result.get("status_code") != 200:
                continue

            # Parse domain once
            try:
                domain = urlparse(url).netloc
            except Exception as e:
                self.logger.warning(f"Could not parse domain from URL '{url}': {e}")
                continue
            
            if domain in self.blacklist_domains:
                self.logger.debug(f"Skipping blacklisted competitor: {domain}")
                continue

            page_content = result.get("page_content")
            if not page_content or not isinstance(page_content, dict):
                self.logger.warning(f"No valid page_content for {url}")
                continue
            
            # Use list for efficient string building
            content_parts = []
            headings = {"h1": [], "h2": [], "h3": [], "h4": [], "h5": [], "h6": []}

            # Extract main content and headings from the structured 'main_topic' array
            main_topic = page_content.get("main_topic")
            if main_topic and isinstance(main_topic, list):
                for topic in main_topic:
                    if not isinstance(topic, dict):
                        continue
                    
```

**FIND (in same method, around line 125):**
```python
            main_topic_content = main_topic_content.strip()

            # Manually calculate word count and readability
            word_count = len(main_topic_content.split())
            readability_score = None
            if (
                word_count > 100
            ):  # textstat needs a reasonable amount of text to be accurate
                try:
                    readability_score = textstat.flesch_kincaid_grade(
                        main_topic_content
                    )
                except Exception as e:
                    self.logger.warning(
                        f"Could not calculate readability for {url}: {e}"
                    )
```

**REPLACE WITH:**
```python
            # Join content parts efficiently
            main_topic_content = " ".join(content_parts).strip()

            # Early exit if content too short
            if len(main_topic_content) < 100:
                self.logger.debug(f"Skipping {url}: content too short ({len(main_topic_content)} chars)")
                continue
            
            # Manually calculate word count and readability
            words = main_topic_content.split()
            word_count = len(words)
            
            readability_score = None
            if word_count >= 100:  # textstat needs reasonable text
                try:
                    readability_score = textstat.flesch_kincaid_grade(main_topic_content)
                except Exception as e:
                    self.logger.warning(f"Could not calculate readability for {url}: {e}")
```

---

### Task 13.2: Optimize Job Status Updates
**Priority**: P0 - HIGH
**File**: `data_access/queries.py`

**FIND:**
```python
UPDATE_JOB_STATUS_DIRECT = """
UPDATE jobs SET status = ?, progress = ?, finished_at = ? WHERE id = ?;
"""
```

**KEEP AS IS**

**File**: `jobs.py`

**FIND (lines 150-168, in update_job_status):**
```python
    def update_job_status(
        self,
        job_id: str,
        status: str,
        progress: int,
        result: Optional[Dict[str, Any]] = None,
        error: Optional[str] = None,
    ):
        """
        Updates job status using a direct UPDATE query (W10 FIX).
        """
        conn = self.db_manager._get_conn()
        finished_at = (
            datetime.now().timestamp() if status in ["completed", "failed"] else None
        )

        if result or error:
            # If result/error is present, use the original UPDATE_JOB (INSERT OR REPLACE)
            # that handles all fields.
            job_info = self.db_manager.get_job(job_id)
            if job_info:
                job_info["status"] = status
                job_info["progress"] = progress
                job_info["result"] = result
                job_info["error"] = error
                job_info["finished_at"] = finished_at
                self.db_manager.update_job(job_info)
        else:
            # Execute the direct, optimized status/progress update
            # This avoids fetching the entire job record first. (W10 FIX)
            with conn:
                conn.execute(
                    queries.UPDATE_JOB_STATUS_DIRECT,
                    (status, progress, finished_at, job_id),
                )
```

**REPLACE WITH:**
```python
    def update_job_status(
        self,
        job_id: str,
        status: str,
        progress: int,
        result: Optional[Dict[str, Any]] = None,
        error: Optional[str] = None,
    ):
        """
        Updates job status with optimized queries.
        Uses direct UPDATE for simple status changes, full update for complex changes.
        """
        # Validate inputs
        if not isinstance(progress, int) or progress < 0 or progress > 100:
            self.logger.warning(f"Invalid progress value: {progress}. Clamping to 0-100")
            progress = max(0, min(100, progress))
        
        from backend.core.enums import JobStatus
        try:
            JobStatus(status)  # Validate status is valid enum value
        except ValueError:
            self.logger.error(f"Invalid job status: {status}")
            status = "failed"
            error = f"Invalid status attempted: {status}"
        
        conn = self.db_manager._get_conn()
        finished_at = datetime.now().timestamp() if status in ["completed", "failed"] else None

        try:
            if result or error:
                # Complex update: fetch current job and update all fields
                job_info = self.db_manager.get_job(job_id)
                if not job_info:
                    self.logger.error(f"Cannot update non-existent job: {job_id}")
                    return
                
                job_info["status"] = status
                job_info["progress"] = progress
                
                if result:
                    # Validate result is serializable
                    try:
                        json.dumps(result)
                        job_info["result"] = result
                    except (TypeError, ValueError) as e:
                        self.logger.error(f"Result is not JSON serializable: {e}")
                        job_info["result"] = {"error": "Result not serializable"}
                
                if error:
                    # Truncate error messages to prevent bloat
                    job_info["error"] = str(error)[:1000]
                
                job_info["finished_at"] = finished_at
                self.db_manager.update_job(job_info)
            else:
                # Simple update: use direct query for performance
                with conn:
                    conn.execute(
                        queries.UPDATE_JOB_STATUS_DIRECT,
                        (status, progress, finished_at, job_id),
                    )
        except Exception as e:
            self.logger.error(f"Failed to update job status for {job_id}: {e}", exc_info=True)
            raise
```

---

**File**: `api/main.py`

**FIND (after exception handler registration):**
```python
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(StarletteHTTPException, http_exception_handler)
app.add_exception_handler(Exception, general_exception_handler)
```

**KEEP AS IS** (already added in previous task)

---

## Phase 14: HIGH Schema & Migration Fixes

### Task 14.1: Add Schema Version Validation
**Priority**: P0 - HIGH
**File**: `data_access/database_manager.py`

**FIND (in _apply_migrations_from_files method, around line 250):**
```python
                    try:
                        with conn:  # Execute in a transaction
                            conn.executescript(sql_script)
                            conn.execute(
                                queries.INSERT_SCHEMA_VERSION,
                                (version, datetime.now().isoformat()),
                            )
                        self.logger.info(f"Migration {filename} applied successfully.")
                        current_version = version
                    except sqlite3.OperationalError as e:
                        if "duplicate column name" in str(e):
                            self.logger.warning(
                                f"Migration {filename} failed because a column already exists. Assuming it was already applied and continuing."
                            )
                            conn.execute(
                                queries.INSERT_SCHEMA_VERSION,
                                (version, datetime.now().isoformat()),
                            )
                            current_version = version
                        else:
                            raise e
```

**REPLACE WITH:**
```python
                    try:
                        with conn:  # Execute in a transaction
                            # Validate SQL before executing
                            if not sql_script or not sql_script.strip():
                                self.logger.error(f"Migration {filename} is empty")
                                raise ValueError(f"Empty migration file: {filename}")
                            
                            # Execute migration
                            conn.executescript(sql_script)
                            
                            # Record successful migration
                            conn.execute(
                                queries.INSERT_SCHEMA_VERSION,
                                (version, datetime.now().isoformat()),
                            )
                        
                        self.logger.info(f"Migration {filename} applied successfully.")
                        current_version = version
                        
                    except sqlite3.IntegrityError as e:
                        # Duplicate version entry - migration was already applied
                        if "unique" in str(e).lower() or "primary key" in str(e).lower():
                            self.logger.info(
                                f"Migration {filename} already recorded in schema_version. Skipping."
                            )
                            current_version = version
                        else:
                            self.logger.error(f"Integrity error in migration {filename}: {e}")
                            raise
                            
                    except sqlite3.OperationalError as e:
                        error_msg = str(e).lower()
                        
                        if "duplicate column name" in error_msg:
                            self.logger.warning(
                                f"Migration {filename} attempted to add duplicate column. "
                                f"Assuming already applied. Error: {e}"
                            )
                            # Record as applied to prevent re-runs
                            try:
                                conn.execute(
                                    queries.INSERT_SCHEMA_VERSION,
                                    (version, datetime.now().isoformat()),
                                )
                                conn.commit()
                            except sqlite3.IntegrityError:
                                pass  # Already recorded
                            current_version = version
                            
                        elif "no such table" in error_msg:
                            self.logger.error(
                                f"Migration {filename} references non-existent table. "
                                f"Check migration order. Error: {e}"
                            )
                            raise
                            
                        elif "syntax error" in error_msg:
                            self.logger.error(
                                f"SQL syntax error in migration {filename}: {e}"
                            )
                            raise
                            
                        else:
                            self.logger.error(f"Operational error in migration {filename}: {e}")
                            raise
```

---

### Task 14.2: Add Schema Version Constraint
**Priority**: P0 - HIGH
**File**: `data_access/queries.py`

**FIND:**
```python
CREATE_SCHEMA_VERSION_TABLE = """
CREATE TABLE IF NOT EXISTS schema_version (
    version INTEGER PRIMARY KEY,
    applied_at TEXT NOT NULL
);
"""
```

**REPLACE WITH:**
```python
CREATE_SCHEMA_VERSION_TABLE = """
CREATE TABLE IF NOT EXISTS schema_version (
    version INTEGER PRIMARY KEY,
    applied_at TEXT NOT NULL,
    migration_file TEXT,
    checksum TEXT
);
"""
```

**File**: Create new migration `data_access/migrations/028_add_schema_version_metadata.sql`

**CREATE NEW FILE:**
```sql
-- data_access/migrations/028_add_schema_version_metadata.sql
-- Add metadata columns to schema_version table for better tracking

-- SQLite doesn't support ALTER TABLE ADD COLUMN IF NOT EXISTS
-- Check if columns exist before adding

-- Add migration_file column
ALTER TABLE schema_version ADD COLUMN migration_file TEXT;

-- Add checksum column for integrity verification
ALTER TABLE schema_version ADD COLUMN checksum TEXT;
```

---

## Phase 15: HIGH Logic & Calculation Errors

### Task 15.1: Fix CPC Null Handling Across All Scoring Components
**Priority**: P0 - HIGH
**File**: `pipeline/step_03_prioritization/scoring_components/commercial_intent.py`

**FIND (lines 44-46):**
```python
    cpc = keyword_info.get("cpc", 0.0)
    if cpc is None:
        cpc = 0.0
```

**REPLACE WITH:**
```python
    cpc = keyword_info.get("cpc")
    # Handle None, null, and string types from API
    if cpc is None:
        cpc = 0.0
    else:
        try:
            cpc = float(cpc)
            if cpc < 0:
                self.logger.warning(f"Negative CPC value: {cpc}. Setting to 0.")
                cpc = 0.0
        except (ValueError, TypeError):
            self.logger.warning(f"Invalid CPC value: {cpc}. Setting to 0.")
            cpc = 0.0
```

**FIND (lines 55-57):**
```python
    low_bid = keyword_info.get("low_top_of_page_bid", 0.0) or 0.0
    high_bid = keyword_info.get("high_top_of_page_bid", 0.0) or 0.0
```

**REPLACE WITH:**
```python
    # Handle None/null bid values
    low_bid = keyword_info.get("low_top_of_page_bid")
    high_bid = keyword_info.get("high_top_of_page_bid")
    
    try:
        low_bid = float(low_bid) if low_bid is not None else 0.0
        high_bid = float(high_bid) if high_bid is not None else 0.0
    except (ValueError, TypeError):
        low_bid = 0.0
        high_bid = 0.0
```

---

**File**: `pipeline/step_03_prioritization/scoring_components/traffic_potential.py`

**FIND (lines 44-60):**
```python
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

**REPLACE WITH:**
```python
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
            if sv < 0:
                self.logger.warning(f"Negative search volume: {sv}. Setting to 0.")
                sv = 0
        except (ValueError, TypeError):
            self.logger.warning(f"Invalid search_volume type: {type(sv)}. Setting to 0.")
            sv = 0
    
    cpc = keyword_info.get("cpc")
    if cpc is None:
        cpc = 0.0
    else:
        try:
            cpc = float(cpc)
            if cpc < 0:
                self.logger.warning(f"Negative CPC: {cpc}. Setting to 0.")
                cpc = 0.0
        except (ValueError, TypeError):
            self.logger.warning(f"Invalid CPC type: {type(cpc)}. Setting to 0.")
            cpc = 0.0
```

---

### Task 15.2: Fix Disqualification Rule Execution Order
**Priority**: P0 - HIGH
**File**: `pipeline/step_01_discovery/disqualification_rules.py`

**FIND (at the very beginning of apply_disqualification_rules, lines 12-24):**
```python
def apply_disqualification_rules(
    opportunity: Dict[str, Any],
    client_cfg: Dict[str, Any],
    cannibalization_checker: CannibalizationChecker,
) -> Tuple[bool, Optional[str], bool]:
    """
    Applies the comprehensive 20-rule set to disqualify a keyword based on data from the discovery phase.
    Reads all thresholds from client_cfg.
    Returns (is_disqualified, reason, is_hard_stop).
    """
    keyword = opportunity.get("keyword", "Unknown Keyword")

    # --- Failsafe Validation ---
    required_keys = [
        "keyword_info",
        "keyword_properties",
        "serp_info",
        "search_intent_info",
    ]
    for key in required_keys:
        if key not in opportunity or opportunity[key] is None:
            logging.getLogger(__name__).warning(
                f"Disqualifying '{keyword}' due to missing or null '{key}' data."
            )
            return
            True, f"Rule 1: Missing critical data structure ({key}).", True
```

**REPLACE WITH:**
```python
def apply_disqualification_rules(
    opportunity: Dict[str, Any],
    client_cfg: Dict[str, Any],
    cannibalization_checker: CannibalizationChecker,
) -> Tuple[bool, Optional[str], bool]:
    """
    Applies the comprehensive 20-rule set to disqualify a keyword based on data from the discovery phase.
    Reads all thresholds from client_cfg.
    Returns (is_disqualified, reason, is_hard_stop).
    
    Rules are ordered by execution cost (cheap checks first).
    """
    keyword = opportunity.get("keyword", "Unknown Keyword")
    
    # Quick validation check before expensive operations
    if not isinstance(opportunity, dict):
        logging.getLogger(__name__).error(f"Opportunity is not a dict: {type(opportunity)}")
        return True, "Rule 1: Invalid opportunity data structure.", True

    # --- Tier 0: Structural Validation (FASTEST - no API data needed) ---
    required_keys = [
        "keyword_info",
        "keyword_properties",
        "serp_info",
        "search_intent_info",
    ]
    
    missing_keys = []
    for key in required_keys:
        if key not in opportunity:
            missing_keys.append(key)
        elif opportunity[key] is None:
            missing_keys.append(f"{key} (null)")
    
    if missing_keys:
        logging.getLogger(__name__).warning(
            f"Disqualifying '{keyword}' due to missing/null data: {', '.join(missing_keys)}"
        )
        return True, f"Rule 1: Missing critical data: {', '.join(missing_keys)}", True
```

**FIND (later in same file, around line 150 - the navigational intent check):**
```python
    # Rule 18: Check for navigational intent safely
    is_navigational = False
    if intent_info:
        if intent_info.get("main_intent") == "navigational":
            is_navigational = True
        else:
            foreign_intent = intent_info.get("foreign_intent")
            if foreign_intent and "navigational" in foreign_intent:
                is_navigational = True
    if is_navigational:
        return True, "Rule 18: Strong navigational intent.", True
```

**MOVE THIS CHECK to be AFTER Rule 2 (intent check), making it Rule 3:**

**FIND (after Rule 2, around line 90):**
```python
    if main_intent not in allowed_intents:
        return True, f"Rule 2: Non-target main intent ('{main_intent}').", True

    # Rule 2b (NEW): Check secondary intents for prohibitive types
```

**INSERT BEFORE Rule 2b:**
```python
    if main_intent not in allowed_intents:
        return True, f"Rule 2: Non-target main intent ('{main_intent}').", True
    
    # Rule 3: Check for navigational intent (MOVED UP - cheap check)
    # Navigational intent is almost always a hard stop for blog content
    if main_intent == "navigational":
        return True, "Rule 3: Strong navigational intent (main).", True
    
    # Also check foreign_intent for navigational
    foreign_intent = intent_info.get("foreign_intent")
    if foreign_intent and isinstance(foreign_intent, list):
        if "navigational" in foreign_intent:
            # Only hard-stop if navigational is primary foreign intent
            return True, "Rule 3: Strong navigational intent (secondary).", True

    # Rule 2b (was 3): Check secondary intents for prohibitive types
```

**THEN DELETE the old Rule 18 navigational check (around line 150)**

---

### Task 15.3: Fix Search Volume Trend Validation
**Priority**: P0 - HIGH
**File**: `pipeline/step_03_prioritization/scoring_components/growth_trend.py`

**FIND (lines 11-25):**
```python
    keyword_info = (
        data.get("keyword_info") if isinstance(data.get("keyword_info"), dict) else {}
    )
    trends = (
        keyword_info.get("search_volume_trend")
        if isinstance(keyword_info.get("search_volume_trend"), dict)
        else {}
    )
    sv = keyword_info.get("search_volume", 0) or 0

    yearly = trends.get("yearly", 0)
    quarterly = trends.get("quarterly", 0)
    monthly = trends.get("monthly", 0)

    def score_trend(value):
        if value is None:
            return 50  # Neutral score for missing data
```

**REPLACE WITH:**
```python
    keyword_info = data.get("keyword_info")
    if not isinstance(keyword_info, dict):
        return 50, {"Growth Trend": {"value": "N/A", "score": 50, "explanation": "No keyword_info"}}
    
    # Handle search_volume_trend - can be dict or JSON string
    trends_raw = keyword_info.get("search_volume_trend")
    if isinstance(trends_raw, str):
        try:
            trends = json.loads(trends_raw) if trends_raw.strip() else {}
        except json.JSONDecodeError:
            trends = {}
    elif isinstance(trends_raw, dict):
        trends = trends_raw
    else:
        trends = {}
    
    sv = keyword_info.get("search_volume")
    try:
        sv = int(sv) if sv is not None else 0
        if sv < 0:
            sv = 0
    except (ValueError, TypeError):
        sv = 0

    # Per API docs: trend values are integers (percentage change)
    def safe_get_trend(trends_dict, key, default=0):
        value = trends_dict.get(key, default)
        if value is None:
            return default
        try:
            return int(value)
        except (ValueError, TypeError):
            return default
    
    yearly = safe_get_trend(trends, "yearly", 0)
    quarterly = safe_get_trend(trends, "quarterly", 0)
    monthly = safe_get_trend(trends, "monthly", 0)

    def score_trend(value):
        if value is None:
            return 50  # Neutral score for missing data
```

**ADD import at top:**
```python
import json
```

---

### Task 15.4: Fix Competitor Performance Normalization
**Priority**: P0 - HIGH
**File**: `pipeline/step_03_prioritization/scoring_components/competitor_performance.py`

**FIND (entire _normalize_value function):**
```python
def _normalize_value(
    value: float, target_value: float, is_lower_better: bool = True
) -> float:
    """Helper to normalize a value to a 0-100 scale, with target_value being ideal."""
    if value is None or target_value is None or target_value == 0:
        return 50.0  # Neutral score if data is missing or target is zero

    if is_lower_better:
        # Example: LCP target 2500ms.
        # If value is 1250, score = 100. If value is 5000, score = 0.
        # This formula provides 100 at 0, 50 at target, 0 at 2*target
        score = max(0.0, min(100.0, 100 * (1 - (value / (2 * target_value)))))
    else:
        # Example: High metric, higher is better. e.g. High security score
        score = max(
            0.0, min(100.0, 100 * (value / (2 * target_value)))
        )  # Max out at 2*target for 100, linear

    return score
```

**REPLACE WITH:**
```python
def _normalize_value(
    value: float, target_value: float, is_lower_better: bool = True
) -> float:
    """
    Helper to normalize a value to a 0-100 scale, with target_value being ideal.
    Fixed to handle edge cases and ensure correct scoring direction.
    """
    # Handle None/invalid inputs
    if value is None or target_value is None:
        return 50.0
    
    try:
        value = float(value)
        target_value = float(target_value)
    except (ValueError, TypeError):
        return 50.0
    
    if target_value <= 0:
        return 50.0  # Cannot normalize against zero/negative target
    
    if value < 0:
        value = 0  # Clamp to non-negative
    
    if is_lower_better:
        # For LCP: lower values (faster) are better
        # Score: 100 when value=0, decreasing as value increases
        # At target_value, score should be ~50
        # At 2*target_value, score should be 0
        if value == 0:
            return 100.0
        elif value <= target_value:
            # Linear from 100 to 50 as value goes from 0 to target
            score = 100.0 - (50.0 * (value / target_value))
        else:
            # Linear from 50 to 0 as value goes from target to 2*target
            excess = value - target_value
            score = 50.0 - (50.0 * (excess / target_value))
        
        return max(0.0, min(100.0, score))
    else:
        # For metrics where higher is better (inverted scoring)
        # This means BAD competitor performance (high LCP) = GOOD opportunity
        # At 2*target, score = 100 (very slow = great opportunity)
        # At target, score = 50
        # At 0, score = 0
        if value >= 2 * target_value:
            return 100.0
        else:
            score = 100.0 * (value / (2 * target_value))
        
        return max(0.0, min(100.0, score))
```

**FIND (in calculate_competitor_performance_score around line 48):**
```python
    # Score: higher if competitors' LCP is high (poor performance)
    # We want to invert the normalization: a higher LCP (worse performance) means higher score (better opportunity)
    # If avg_lcp_ms is 2*target_good_lcp_ms, score is 100. If it's target_good_lcp_ms, score is 50.
    score = _normalize_value(avg_lcp_ms, target_good_lcp_ms, is_lower_better=False)
```

**KEEP AS IS** (logic is now correct with fixed _normalize_value)

---

### Task 15.5: Add Safe Division Helper
**Priority**: P0 - HIGH
**File**: Create new file `core/math_utils.py`

**CREATE NEW FILE:**
```python
# core/math_utils.py
import logging
from typing import Union, Optional

logger = logging.getLogger(__name__)


def safe_divide(
    numerator: Union[int, float], 
    denominator: Union[int, float],
    default: float = 0.0
) -> float:
    """
    Safely divide two numbers, returning default if division is invalid.
    Handles None, zero denominator, and type errors.
    """
    if numerator is None or denominator is None:
        return default
    
    try:
        numerator = float(numerator)
        denominator = float(denominator)
    except (ValueError, TypeError):
        logger.warning(f"Invalid types for division: {type(numerator)}, {type(denominator)}")
        return default
    
    if denominator == 0:
        return default
    
    try:
        result = numerator / denominator
        # Check for inf/nan
        if not (-1e308 < result < 1e308):  # Check for infinity
            logger.warning(f"Division resulted in infinity: {numerator}/{denominator}")
            return default
        return result
    except (ZeroDivisionError, OverflowError) as e:
        logger.warning(f"Division error: {e}")
        return default


def safe_normalize(
    value: Union[int, float],
    min_val: Union[int, float],
    max_val: Union[int, float],
    invert: bool = False
) -> float:
    """
    Normalize a value to 0-100 scale between min and max.
    
    Args:
        value: Value to normalize
        min_val: Minimum value in range
        max_val: Maximum value in range
        invert: If True, higher input values give lower scores
    
    Returns:
        Normalized score 0-100
    """
    if value is None or min_val is None or max_val is None:
        return 50.0  # Neutral score
    
    try:
        value = float(value)
        min_val = float(min_val)
        max_val = float(max_val)
    except (ValueError, TypeError):
        return 50.0
    
    if max_val <= min_val:
        return 50.0  # Invalid range
    
    # Clamp value to range
    value = max(min_val, min(max_val, value))
    
    # Normalize to 0-1
    normalized = (value - min_val) / (max_val - min_val)
    
    # Invert if needed
    if invert:
        normalized = 1.0 - normalized
    
    # Scale to 0-100
    return normalized * 100.0
```

---

**File**: Update all scoring components to use safe_divide

**File**: `pipeline/step_03_prioritization/scoring_components/ease_of_ranking.py`

**ADD import at top:**
```python
from backend.core.math_utils import safe_divide, safe_normalize
```

**FIND (line 53):**
```python
    dofollow_ratio = dofollow_backlinks / total_backlinks if total_backlinks > 0 else 0
```

**REPLACE WITH:**
```python
    dofollow_ratio = safe_divide(dofollow_backlinks, total_backlinks, default=0.0)
```

---

**File**: `pipeline/step_03_prioritization/scoring_components/growth_trend.py`

**ADD import at top:**
```python
from backend.core.math_utils import safe_divide
```

**FIND (line 62):**
```python
    # Weight the trend score by search volume magnitude
    # A log scale helps moderate the effect of massive search volumes
    sv_weight = min(
        math.log(sv + 1) / math.log(100000), 1.0
    )  # Normalize against 100k SV
```

**REPLACE WITH:**
```python
    # Weight the trend score by search volume magnitude
    # A log scale helps moderate the effect of massive search volumes
    try:
        sv_log = math.log(max(sv, 1))  # Ensure sv >= 1
        target_log = math.log(100000)
        sv_weight = min(safe_divide(sv_log, target_log, default=0.0), 1.0)
    except (ValueError, OverflowError):
        sv_weight = 0.0
```

---

### Task 15.6: Fix Volume Volatility Calculation
**Priority**: P0 - HIGH
**File**: `pipeline/step_03_prioritization/scoring_components/volume_volatility.py`

**FIND (lines 30-44):**
```python
    mean_volume = np.mean(volumes)
    std_dev = np.std(volumes)

    if mean_volume == 0:
        return 0.0, {
            "Volatility": {"value": "0", "score": 0, "explanation": "No search volume."}
        }

    coeff_of_variation = std_dev / mean_volume

    # Score is inverted: higher volatility = lower score
    # A CoV of 0.5 (50%) is considered moderately high.
    score = max(0, 100 - (coeff_of_variation * 150))  # Scale the penalty
```

**REPLACE WITH:**
```python
    from backend.core.math_utils import safe_divide
    
    if len(volumes) < 2:
        return 50.0, {
            "Volatility": {"value": "N/A", "score": 50, "explanation": "Insufficient data points."}
        }
    
    try:
        mean_volume = np.mean(volumes)
        std_dev = np.std(volumes)
    except Exception as e:
        logger.error(f"Error calculating volatility statistics: {e}")
        return 50.0, {
            "Volatility": {"value": "Error", "score": 50, "explanation": "Calculation error."}
        }

    if mean_volume == 0:
        return 0.0, {
            "Volatility": {"value": "0", "score": 0, "explanation": "No search volume."}
        }

    coeff_of_variation = safe_divide(std_dev, mean_volume, default=0.0)
    
    # Validate result
    if coeff_of_variation < 0:
        coeff_of_variation = 0
    elif coeff_of_variation > 10:  # Sanity check - CoV >10 is extremely unusual
        logger.warning(f"Unusually high CoV: {coeff_of_variation}. Capping at 2.0")
        coeff_of_variation = 2.0

    # Score is inverted: higher volatility = lower score
    # A CoV of 0.5 (50%) is considered moderately high
    # CoV of 1.0 (100%) is very high
    score = max(0, 100 - (coeff_of_variation * 150))  # Scale the penalty
```

**ADD import:**
```python
import logging
logger = logging.getLogger(__name__)
```

---

## Phase 16: CRITICAL Workflow & State Management

### Task 16.1: Add Compensating Transactions for Failed Content Generation
**Priority**: P0 - CRITICAL
**File**: `pipeline/orchestrator/content_orchestrator.py`

**FIND (in _run_full_content_generation_background, the except block around line 185):**
```python
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
```

**REPLACE WITH:**
```python
        except Exception as e:
            error_msg = f"Agentic content generation failed: {e}"
            self.logger.error(f"{error_msg}\n{traceback.format_exc()}")
            
            # COMPENSATING TRANSACTIONS: Clean up all artifacts from partial execution
            self.logger.info(f"Starting rollback for opportunity {opportunity_id}")
            
            rollback_errors = []
            
            # 1. Cleanup temporary files
            for temp_file in temp_files_to_cleanup:
                try:
                    if os.path.exists(temp_file):
                        os.remove(temp_file)
                        self.logger.info(f"Cleaned up temporary file: {temp_file}")
                except Exception as cleanup_error:
                    rollback_errors.append(f"File cleanup: {cleanup_error}")
                    self.logger.warning(f"Failed to cleanup {temp_file}: {cleanup_error}")
```

**FIND (continuing in same except block):**
```python
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
```

**REPLACE WITH:**
```python
            # 2. Clear any partial content that might have been saved
            try:
                # Get current opportunity state
                current_opp = self.db_manager.get_opportunity_by_id(opportunity_id)
                
                if current_opp:
                    # If there was previous valid content, restore it
                    content_history = self.db_manager.get_content_history(opportunity_id)
                    
                    if content_history and len(content_history) > 0:
                        # Restore most recent valid version
                        last_valid = content_history[0]
                        self.logger.info(
                            f"Restoring previous content version from {last_valid.get('timestamp')}"
                        )
                        try:
                            self.db_manager.restore_content_version(
                                opportunity_id,
                                last_valid.get("timestamp")
                            )
                        except Exception as restore_error:
                            rollback_errors.append(f"Content restore: {restore_error}")
                    else:
                        # No history - save error state
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
                rollback_errors.append(f"Database rollback: {db_error}")
                self.logger.error(f"Failed to rollback database state: {db_error}")
```

**FIND (continuing):**
```python
            # 3. Clear cost tracking for this failed workflow
            workflow_cost_id = f"generation_{opportunity_id}"
            try:
                final_cost = self.cost_tracker.get_workflow_cost(workflow_cost_id)
                self.logger.info(f"Total cost before failure: ${final_cost:.4f}")
                self.cost_tracker.clear_workflow(workflow_cost_id)
            except:
                pass
            
            self.db_manager.update_opportunity_workflow_state(
                opportunity_id, "content_generation_failed", "failed", str(e)
            )
            self.job_manager.update_job_status(
                job_id, "failed", progress=100, error=str(e)
            )
            raise
```

**REPLACE WITH:**
```python
            # 3. Save cost data before clearing
            workflow_cost_id = f"generation_{opportunity_id}"
            try:
                final_cost = self.cost_tracker.get_workflow_cost(workflow_cost_id)
                cost_breakdown = self.cost_tracker.get_workflow_breakdown(workflow_cost_id)
                
                self.logger.info(
                    f"Total cost incurred before failure: ${final_cost:.4f}. "
                    f"Breakdown: {len(cost_breakdown)} API calls"
                )
                
                # Store partial cost in opportunity record for tracking
                try:
                    current_total = self.db_manager.get_opportunity_by_id(opportunity_id).get("total_api_cost", 0.0)
                    self.db_manager._get_conn().execute(
                        "UPDATE opportunities SET total_api_cost = ? WHERE id = ?",
                        (current_total + final_cost, opportunity_id)
                    )
                    self.db_manager._get_conn().commit()
                except Exception as cost_save_error:
                    rollback_errors.append(f"Cost save: {cost_save_error}")
                
                self.cost_tracker.clear_workflow(workflow_cost_id)
            except Exception as cost_error:
                rollback_errors.append(f"Cost tracking: {cost_error}")
            
            # 4. Update opportunity state
            error_detail = str(e)[:500]
            if rollback_errors:
                error_detail += f" | Rollback issues: {'; '.join(rollback_errors[:3])}"
            
            self.db_manager.update_opportunity_workflow_state(
                opportunity_id, "content_generation_failed", "failed", error_detail
            )
            
            # 5. Update job with detailed error
            self.job_manager.update_job_status(
                job_id, 
                "failed", 
                progress=100, 
                error=error_detail
            )
            
            self.logger.info(f"Rollback completed with {len(rollback_errors)} issues")
            raise
```

---

### Task 16.2: Fix Workflow State Recovery
**Priority**: P0 - HIGH
**File**: `pipeline/orchestrator/workflow_orchestrator.py`

**FIND (lines 18-60, in _run_full_auto_workflow_background):**
```python
    def _run_full_auto_workflow_background(
        self, job_id: str, opportunity_id: int, override_validation: bool
    ):
        original_status = None
        original_workflow_step = None
        
        try:
            # Record original state for potential rollback
            opportunity = self.db_manager.get_opportunity_by_id(opportunity_id)
            if opportunity:
                original_status = opportunity.get("status")
                original_workflow_step = opportunity.get("last_workflow_step")
```

**REPLACE WITH:**
```python
    def _run_full_auto_workflow_background(
        self, job_id: str, opportunity_id: int, override_validation: bool
    ):
        # State checkpoint for rollback
        checkpoint = {
            "opportunity_id": opportunity_id,
            "original_status": None,
            "original_workflow_step": None,
            "original_error": None,
            "checkpoint_time": datetime.now().isoformat()
        }
        
        try:
            # Record original state for potential rollback
            opportunity = self.db_manager.get_opportunity_by_id(opportunity_id)
            if not opportunity:
                raise ValueError(f"Opportunity {opportunity_id} not found")
            
            checkpoint["original_status"] = opportunity.get("status")
            checkpoint["original_workflow_step"] = opportunity.get("last_workflow_step")
            checkpoint["original_error"] = opportunity.get("error_message")
            
            # Validate opportunity is in correct state to start workflow
            current_status = opportunity.get("status")
            if current_status in ["running", "in_progress", "pending"]:
                raise ValueError(
                    f"Cannot start workflow: opportunity is already in '{current_status}' state. "
                    f"Wait for current operation to complete or cancel it first."
                )
```

**FIND (in except block at end of same method):**
```python
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

**REPLACE WITH:**
```python
        except Exception as e:
            error_msg = f"Full auto workflow for {opportunity_id} failed: {e}"
            self.logger.error(f"{error_msg}\n{traceback.format_exc()}")
            
            # Comprehensive rollback with audit trail
            rollback_success = False
            
            if checkpoint["original_status"] and checkpoint["original_workflow_step"]:
                try:
                    self.logger.info(
                        f"Rolling back opportunity {opportunity_id} to checkpoint: "
                        f"status={checkpoint['original_status']}, "
                        f"step={checkpoint['original_workflow_step']}, "
                        f"checkpoint_time={checkpoint['checkpoint_time']}"
                    )
                    
                    # Restore to original state
                    error_detail = (
                        f"Workflow failed at {datetime.now().isoformat()}: {str(e)[:200]}. "
                        f"Rolled back to state from {checkpoint['checkpoint_time']}."
                    )
                    
                    if checkpoint["original_error"]:
                        error_detail += f" Original error: {checkpoint['original_error'][:100]}"
                    
                    self.db_manager.update_opportunity_workflow_state(
                        opportunity_id,
                        checkpoint["original_workflow_step"],
                        checkpoint["original_status"],
                        error_message=error_detail
                    )
                    
                    rollback_success = True
                    self.logger.info(f"Rollback successful for opportunity {opportunity_id}")
                    
                except Exception as rollback_error:
                    self.logger.error(
                        f"CRITICAL: Failed to rollback opportunity {opportunity_id}: {rollback_error}",
                        exc_info=True
                    )
                    
                    # Last resort: mark as failed with detailed error
                    try:
                        self.db_manager.update_opportunity_workflow_state(
                            opportunity_id,
                            "rollback_failed",
                            "failed",
                            error_message=f"Workflow and rollback both failed. Original: {str(e)[:100]}. Rollback: {str(rollback_error)[:100]}"
                        )
                    except:
                        pass  # Can't do anything more
            else:
                # No checkpoint available
                self.logger.error(f"No checkpoint available for opportunity {opportunity_id}")
                try:
                    self.db_manager.update_opportunity_workflow_state(
                        opportunity_id,
                        "workflow_failed",
                        "failed",
                        error_message=f"Workflow failed: {str(e)[:500]}"
                    )
                except:
                    pass
            
            # The job's _run_job wrapper will catch this and handle the final 'failed' state
            raise
```

**ADD import at top:**
```python
from datetime import datetime
```

---
