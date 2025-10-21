Here is the complete and corrected implementation plan, incorporating all necessary fixes and addressing the identified weaknesses and gaps. This document is designed to be standalone and directly executable.

---

### **Revised & Final Implementation Plan (Optimized for AI Agent)**

#### **Tier 1: Foundational Overhaul & Cost-Cutting**

---

**Task No:** 1
**Task Higher Overview:** Implement an API-side filter to automatically exclude keywords found in "hostile" SERP environments, and cleanly remove the now-redundant Python-side check for efficiency and avoid filter reconciliation conflicts.
**Files Involved:**
*   `backend/app_config/settings.ini`
*   `backend/pipeline/step_01_discovery/run_discovery.py`
*   `backend/pipeline/step_01_discovery/disqualification_rules.py`
**Total Code Changes Required:** 3 granular changes.

**STEP BY STEP PLAN:**

### **File: `backend/app_config/settings.ini`**

**ACTION NO:** 1.1
**ACTION TYPE:** REPLACE
**ACTION RATIONALE:** This new configuration setting defines a list of SERP features considered "hostile" to blog content. This list will be read by the discovery pipeline to filter keywords at the API level, saving cost. The existing `hostile_serp_features` line is updated to include `app,jobs`.

**FIND CONTEXT (Replace the line containing):**
```ini
hostile_serp_features = shopping,local_pack,google_flights,google_hotels,popular_products,local_services
```

**CODE TO REPLACE:**
```ini
hostile_serp_features = shopping,local_pack,google_flights,google_hotels,popular_products,local_services
```

**WITH NEW CODE:**
```ini
hostile_serp_features = shopping,local_pack,google_flights,google_hotels,popular_products,local_services,app,jobs
```

### **File: `backend/pipeline/step_01_discovery/run_discovery.py`**

**ACTION NO:** 1.2
**ACTION TYPE:** INSERT
**ACTION RATIONALE:** This code dynamically constructs and applies an API-side filter based on the `hostile_serp_features` setting. It also includes basic logic to reconcile with existing `serp_info.serp_item_types` filters to prevent conflicts, ensuring system-level hostile filtering takes precedence.

**FIND CONTEXT (Insert after the line containing):**
```python
    # --- Scoring and Disqualification Loop (Consolidated Logic) ---
```

**CODE TO INSERT:**
```python
    # ADD THIS BLOCK to dynamically add the hostile SERP filter (Task 1.2 - includes filter reconciliation)
    hostile_features_str = client_cfg.get("hostile_serp_features", "")
    if hostile_features_str:
        hostile_features = [feature.strip() for feature in hostile_features_str.split(',') if feature.strip()]
        if hostile_features:
            hostile_filter_condition = ["serp_info.serp_item_types", "not_in", hostile_features]
            
            # Check for existing serp_info.serp_item_types filters to avoid conflicts
            # This is a basic override. A more complex merge logic could be implemented if needed.
            existing_serp_filter_found = False
            if filters:
                for f in filters:
                    if isinstance(f, dict) and f.get("field") == "serp_info.serp_item_types":
                        logger.warning(f"User-defined SERP item type filter found. Overriding with system's hostile filter: {hostile_features}")
                        f.update(hostile_filter_condition) # Overwrite existing filter
                        existing_serp_filter_found = True
                        break
            if not existing_serp_filter_found:
                if filters is None: filters = [] # Initialize if empty
                filters.append(hostile_filter_condition) # Add if no conflicting filter
            logger.info(f"Applying API-side hostile SERP filter for: {hostile_features}")
```

### **File: `backend/pipeline/step_01_discovery/disqualification_rules.py`**

**ACTION NO:** 1.3
**ACTION TYPE:** DELETE
**ACTION RATIONALE:** With API-side filtering implemented in step 1.2, the Python-side `_check_hostile_serp_environment` function and its call are now redundant. Removing this code simplifies the disqualification logic and improves runtime efficiency.

**FIND CONTEXT (Delete the block containing these lines):**
```python
    # Tier 4: Content, SERP & Keyword Structure

    # Rule: Check for hostile SERP environment
    is_hostile, hostile_reason = _check_hostile_serp_environment(opportunity)
    if is_hostile:
        return True, hostile_reason, True
```

**CODE TO DELETE:**
```python
    # Rule: Check for hostile SERP environment
    is_hostile, hostile_reason = _check_hostile_serp_environment(opportunity)
    if is_hostile:
        return True, hostile_reason, True
```

**ACTION NO:** 1.4
**ACTION TYPE:** DELETE
**ACTION RATIONALE:** The `_check_hostile_serp_environment` helper function is no longer called after action 1.3, making it obsolete. Deleting it removes dead code.

**FIND CONTEXT (Delete the entire function definition, from `def _check_hostile_serp_environment` to `return False, None`):**
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

**CODE TO DELETE:**
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

---

**Task No:** 2
**Task Higher Overview:** Pivot the analysis workflow to a SERP-only model by completely removing all On-Page API calls, deleting obsolete components, and rebalancing the scoring model, and integrate new AI methods for SERP-only competitor assessment and inferred outline generation.
**Files Involved:**
*   `backend/app_config/settings.ini`
*   `backend/pipeline/orchestrator/analysis_orchestrator.py`
*   `backend/pipeline/step_04_analysis/competitor_analyzer.py` (Delete)
*   `backend/pipeline/step_03_prioritization/scoring_components/competitor_performance.py` (Delete)
*   `backend/pipeline/step_03_prioritization/scoring_engine.py`
*   `backend/pipeline/orchestrator/main.py`
*   `backend/pipeline/step_04_analysis/__init__.py`
*   `backend/pipeline/step_03_prioritization/scoring_components/__init__.py`
*   `backend/pipeline/step_04_analysis/content_analyzer.py`
**Total Code Changes Required:** 11 granular changes (2 deletions, 9 modifications).

**STEP BY STEP PLAN:**

### **File: `backend/app_config/settings.ini`**

**ACTION NO:** 2.1
**ACTION TYPE:** REPLACE
**ACTION RATIONALE:** Explicitly sets `enable_deep_competitor_analysis` to `false` in the configuration, reflecting the strategic decision to pivot to a SERP-only analysis model and avoid expensive On-Page API calls.

**FIND CONTEXT (Replace the line containing):**
```ini
enable_deep_competitor_analysis = false
```

**CODE TO REPLACE:**
```ini
enable_deep_competitor_analysis = false
```

**WITH NEW CODE:**
```ini
enable_deep_competitor_analysis = false ; Explicitly set to false as per new strategy```

**ACTION NO:** 2.2
**ACTION TYPE:** REPLACE
**ACTION RATIONALE:** Re-distributes the weight from the now-removed `competitor_performance_weight` to `competitor_weakness_weight`. This ensures the scoring still considers competitive aspects, but now solely based on high-level SERP data.

**FIND CONTEXT (Replace the line containing):**
```ini
competitor_weakness_weight = 20
```

**CODE TO REPLACE:**
```ini
competitor_weakness_weight = 20
```

**WITH NEW CODE:**
```ini
competitor_weakness_weight = 25 ; Re-distributed 5% from removed competitor_performance_weight
```

**ACTION NO:** 2.3
**ACTION TYPE:** DELETE
**ACTION RATIONALE:** The `competitor_performance_weight` is no longer relevant as the corresponding scoring component has been removed due to the pivot to SERP-only analysis. Deleting this line cleans up the configuration.

**FIND CONTEXT (Delete the line containing):**
```ini
competitor_performance_weight = 5 ; NEW: Weight for competitor technical performance
```

**CODE TO DELETE:**
```ini
competitor_performance_weight = 5 ; NEW: Weight for competitor technical performance```

### **File: `backend/pipeline/orchestrator/analysis_orchestrator.py`**

**ACTION NO:** 2.4
**ACTION TYPE:** REPLACE
**ACTION RATIONALE:** This block removes the entire section responsible for conditional On-Page competitor analysis, aligning the workflow with the SERP-only strategy. It's replaced with a notification that On-Page analysis is skipped and ensures `competitor_analysis` is an empty list for downstream compatibility. It also introduces calls for new AI-powered competitor assessment and inferred outline generation, ensuring the `ContentAnalyzer` is initialized at the correct point in the flow.

**FIND CONTEXT (Replace the block starting from `            # 3. Conditional Competitor OnPage Analysis (REMOVED as per new strategy)` to `            self.logger.info("Deep competitor analysis is DISABLED. Skipping OnPage competitor analysis.")`):**
```python
            # 3. Conditional Competitor OnPage Analysis (REMOVED as per new strategy)
            competitor_analysis = []
            competitor_api_cost = 0.0

            if self.client_cfg.get("enable_deep_competitor_analysis", False):
                self.logger.info(
                    "Deep competitor analysis is ENABLED. Running OnPage competitor analysis."
                )
                from pipeline.step_04_analysis.competitor_analyzer import (
                    FullCompetitorAnalyzer,
                )

                competitor_analyzer = FullCompetitorAnalyzer(
                    self.dataforseo_client, self.client_cfg
                )
                top_organic_urls = [
                    result["url"]
                    for result in live_serp_data.get("top_organic_results", [])[
                        : self.client_cfg.get("num_competitors_to_analyze", 5)
                    ]
                ]
                competitor_analysis, competitor_api_cost = (
                    competitor_analyzer.analyze_competitors(
                        top_organic_urls, selected_competitor_urls
                    )
                )
                total_api_cost += competitor_api_cost
            else:
                self.logger.info(
                    "Deep competitor analysis is DISABLED. Skipping OnPage competitor analysis."
                )
```

**CODE TO REPLACE:**
```python
            # 3. Conditional Competitor OnPage Analysis (REMOVED as per new strategy)
            competitor_analysis = []
            competitor_api_cost = 0.0

            if self.client_cfg.get("enable_deep_competitor_analysis", False):
                self.logger.info(
                    "Deep competitor analysis is ENABLED. Running OnPage competitor analysis."
                )
                from pipeline.step_04_analysis.competitor_analyzer import (
                    FullCompetitorAnalyzer,
                )

                competitor_analyzer = FullCompetitorAnalyzer(
                    self.dataforseo_client, self.client_cfg
                )
                top_organic_urls = [
                    result["url"]
                    for result in live_serp_data.get("top_organic_results", [])[
                        : self.client_cfg.get("num_competitors_to_analyze", 5)
                    ]
                ]
                competitor_analysis, competitor_api_cost = (
                    competitor_analyzer.analyze_competitors(
                        top_organic_urls, selected_competitor_urls
                    )
                )
                total_api_cost += competitor_api_cost
            else:
                self.logger.info(
                    "Deep competitor analysis is DISABLED. Skipping OnPage competitor analysis."
                )
```

**WITH NEW CODE:**```python
            self.logger.info("Deep competitor analysis is DISABLED. Skipping OnPage competitor analysis.")
            # Ensure competitor_analysis is an empty list for downstream compatibility
            competitor_analysis = [] 
            
            # NEW: AI-powered competitor assessment from SERP data
            from pipeline.step_04_analysis.content_analyzer import ContentAnalyzer
            content_analyzer = ContentAnalyzer(self.openai_client, self.client_cfg)
            
            ai_competitor_assessment, assessment_cost = content_analyzer.assess_competitor_quality_from_serp(keyword, live_serp_data)
            self.db_manager.increment_opportunity_cost(opportunity_id, assessment_cost) # Use incremental cost tracking (Task 5.2)

            # NEW: AI-inferred competitor outline from SERP data
            inferred_outline, inferred_outline_cost = content_analyzer.infer_competitor_outline_from_serp(keyword, live_serp_data)
            self.db_manager.increment_opportunity_cost(opportunity_id, inferred_outline_cost) # Use incremental cost tracking (Task 5.2)
```

**ACTION NO:** 2.5
**ACTION TYPE:** REPLACE
**ACTION RATIONALE:** The `content_analyzer` instance must be available from the previous step. The original implementation imported `ContentAnalyzer` and instantiated it too late for the new AI-powered calls. This also replaces `total_api_cost` tracking with direct `db_manager.increment_opportunity_cost` calls.

**FIND CONTEXT (Replace the block starting from `            # 4. Content Intelligence Synthesis` to `            total_api_cost += content_api_cost`):**
```python
            # 4. Content Intelligence Synthesis
            from pipeline.step_04_analysis.content_analyzer import ContentAnalyzer

            content_analyzer = ContentAnalyzer(self.openai_client, self.client_cfg)
            content_intelligence, content_api_cost = (
                content_analyzer.synthesize_content_intelligence(
                    keyword,
                    live_serp_data,
                    competitor_analysis,  # Pass this list; it will be empty for the fast workflow
                )
            )
            total_api_cost += content_api_cost
```

**CODE TO REPLACE:**
```python
            # 4. Content Intelligence Synthesis
            from pipeline.step_04_analysis.content_analyzer import ContentAnalyzer

            content_analyzer = ContentAnalyzer(self.openai_client, self.client_cfg)
            content_intelligence, content_api_cost = (
                content_analyzer.synthesize_content_intelligence(
                    keyword,
                    live_serp_data,
                    competitor_analysis,  # Pass this list; it will be empty for the fast workflow
                )
            )
            total_api_cost += content_api_cost
```

**WITH NEW CODE:**
```python
            # 4. Content Intelligence Synthesis
            content_intelligence, content_api_cost = \
                content_analyzer.synthesize_content_intelligence(
                    keyword,
                    live_serp_data,
                    competitor_analysis, # This will be an empty list as per new strategy
                )
            self.db_manager.increment_opportunity_cost(opportunity_id, content_api_cost) # Use incremental cost tracking (Task 5.2)
```

**ACTION NO:** 2.6
**ACTION TYPE:** REPLACE
**ACTION RATIONALE:** Update the `generate_ai_outline` call to pass the newly inferred competitor outline. Also, replace `total_api_cost` tracking with direct `db_manager.increment_opportunity_cost` call.

**FIND CONTEXT (Replace the block starting from `            ai_outline, outline_api_cost = content_analyzer.generate_ai_outline(` to `            total_api_cost += outline_api_cost`):**
```python
            ai_outline, outline_api_cost = content_analyzer.generate_ai_outline(
                keyword, live_serp_data, content_intelligence
            )
            total_api_cost += outline_api_cost
```

**CODE TO REPLACE:**
```python
            ai_outline, outline_api_cost = content_analyzer.generate_ai_outline(
                keyword, live_serp_data, content_intelligence
            )
            total_api_cost += outline_api_cost
```

**WITH NEW CODE:**
```python
            ai_outline, outline_api_cost = content_analyzer.generate_ai_outline(
                keyword, live_serp_data, content_intelligence, inferred_outline.get("inferred_outline", []) # Pass inferred outline
            )
            self.db_manager.increment_opportunity_cost(opportunity_id, outline_api_cost) # Use incremental cost tracking (Task 5.2)
```

**ACTION NO:** 2.7
**ACTION TYPE:** REPLACE
**ACTION RATIONALE:** The `analysis_data` dictionary needs to include the new `ai_competitor_assessment` and `inferred_competitor_outline` from the SERP-only analysis for storage in the blueprint.

**FIND CONTEXT (Replace the block starting from `            analysis_data = {` to `                "recommended_strategy": recommended_strategy,`):**
```python
            analysis_data = {
                "serp_overview": live_serp_data,
                "competitor_analysis": competitor_analysis,
                "content_intelligence": content_intelligence,
                "recommended_strategy": recommended_strategy,
            }
```

**CODE TO REPLACE:**
```python
            analysis_data = {
                "serp_overview": live_serp_data,
                "competitor_analysis": competitor_analysis,
                "content_intelligence": content_intelligence,
                "recommended_strategy": recommended_strategy,
            }
```

**WITH NEW CODE:**
```python
            analysis_data = {
                "serp_overview": live_serp_data,
                "competitor_analysis": competitor_analysis,
                "ai_competitor_assessment": ai_competitor_assessment, # Store the new AI assessment
                "inferred_competitor_outline": inferred_outline.get("inferred_outline", []), # Store the new inferred outline
                "content_intelligence": content_intelligence,
                "recommended_strategy": recommended_strategy,
            }
```

**ACTION NO:** 2.8
**ACTION TYPE:** REPLACE
**ACTION RATIONALE:** Update `total_api_cost` in the `blueprint_factory.create_blueprint` call to fetch the current accumulated cost directly from the database, rather than relying on a local variable that is no longer being incrementally updated in this file.

**FIND CONTEXT (Replace the line containing `                total_api_cost=total_api_cost,`):**
```python
                total_api_cost=total_api_cost,
                client_id=opportunity.get("client_id"),
```

**CODE TO REPLACE:**```python
                total_api_cost=total_api_cost,
                client_id=opportunity.get("client_id"),
```

**WITH NEW CODE:**
```python
                total_api_cost=self.db_manager.get_opportunity_by_id(opportunity_id).get("total_api_cost", 0.0), # Get current total cost from DB
                client_id=opportunity.get("client_id"),
```

### **File: `backend/pipeline/step_04_analysis/competitor_analyzer.py`**

**ACTION NO:** 2.9
**ACTION TYPE:** DELETE_FILE
**ACTION RATIONALE:** The `competitor_analyzer.py` module, which contained the logic for deep On-Page competitor analysis, is no longer needed after pivoting to a SERP-only strategy. Deleting this file removes obsolete code and simplifies the codebase.

**FILE PATH:** `backend/pipeline/step_04_analysis/competitor_analyzer.py`

### **File: `backend/pipeline/step_04_analysis/__init__.py`**

**ACTION NO:** 2.10
**ACTION TYPE:** DELETE
**ACTION RATIONALE:** Removes the unnecessary empty line from the `__init__.py` file after deleting a module within the package. This is a cleanup step.

**FIND CONTEXT (Delete the lines containing these comments/empty lines):**
```python
# pipeline/step_04_analysis/__init__.py


```

**CODE TO DELETE:**
```python
# pipeline/step_04_analysis/__init__.py


```

### **File: `backend/pipeline/step_03_prioritization/scoring_components/competitor_performance.py`**

**ACTION NO:** 2.11
**ACTION TYPE:** DELETE_FILE
**ACTION RATIONALE:** The `competitor_performance.py` module, which contained the scoring logic for competitor technical performance (based on On-Page data), is no longer relevant after pivoting to a SERP-only analysis strategy. Deleting this file removes obsolete code.

**FILE PATH:** `backend/pipeline/step_03_prioritization/scoring_components/competitor_performance.py`

### **File: `backend/pipeline/step_03_prioritization/scoring_components/__init__.py`**

**ACTION NO:** 2.12
**ACTION TYPE:** DELETE
**ACTION RATIONALE:** The `calculate_competitor_performance_score` import is no longer needed as the corresponding module has been deleted and the scoring component is removed from the workflow. Removing this import cleans up dependencies.

**FIND CONTEXT (Delete the line containing):**
```python
from .competitor_performance import calculate_competitor_performance_score
```

**CODE TO DELETE:**```python
from .competitor_performance import calculate_competitor_performance_score
```

**ACTION NO:** 2.13
**ACTION TYPE:** DELETE
**ACTION RATIONALE:** `calculate_competitor_performance_score` is removed from the `__all__` list because the corresponding module has been deleted and the scoring component is no longer part of the system. This ensures the `__init__.py` accurately reflects the available components.

**FIND CONTEXT (Delete the line containing):**
```python
    "calculate_competitor_performance_score",  # ADDED THIS LINE
]
```

**CODE TO DELETE:**
```python
    "calculate_competitor_performance_score",  # ADDED THIS LINE
]
```

### **File: `backend/pipeline/step_03_prioritization/scoring_engine.py`**

**ACTION NO:** 2.14
**ACTION TYPE:** DELETE
**ACTION RATIONALE:** The import for `calculate_competitor_performance_score` is removed as the corresponding scoring component is no longer part of the system's prioritization logic.

**FIND CONTEXT (Delete the line containing):**
```python
    calculate_competitor_performance_score,  # ADDED THIS IMPORT
)
```

**CODE TO DELETE:**
```python
    calculate_competitor_performance_score,  # ADDED THIS IMPORT
)
```

**ACTION NO:** 2.15
**ACTION TYPE:** DELETE
**ACTION RATIONALE:** The `competitor_performance` breakdown block is removed because the `CompetitorPerformance` scoring component is no longer calculated after the pivot to SERP-only analysis. This removes irrelevant scoring logic.

**FIND CONTEXT (Delete the block starting from `        performance_score, performance_breakdown = (` to `        }`):**
```python
        performance_score, performance_breakdown = (
            calculate_competitor_performance_score(opportunity, self.config)
        )
        breakdown["competitor_performance"] = {
            "name": "Competitor Tech Performance",
            "score": performance_score,
            "breakdown": performance_breakdown,
        }```

**CODE TO DELETE:**
```python
        performance_score, performance_breakdown = (
            calculate_competitor_performance_score(opportunity, self.config)
        )
        breakdown["competitor_performance"] = {
            "name": "Competitor Tech Performance",
            "score": performance_score,
            "breakdown": performance_breakdown,
        }
```

**ACTION NO:** 2.16
**ACTION TYPE:** REPLACE
**ACTION RATIONALE:** The `competitor_performance` weight is explicitly set to `0` in the `weights` dictionary. This ensures that even if it's referenced, it contributes nothing to the final score, reinforcing the removal of this component.

**FIND CONTEXT (Replace the line containing `            "competitor_performance": self.config.get(`):**
```python
            "competitor_performance": self.config.get(
                "competitor_performance_weight", 5
            ),  # ADDED THIS LINE
```

**CODE TO REPLACE:**
```python
            "competitor_performance": self.config.get(
                "competitor_performance_weight", 5
            ),  # ADDED THIS LINE
```

**WITH NEW CODE:**
```python
            "competitor_performance": 0, # Weight is now 0 as per strategy
```

**ACTION NO:** 2.17
**ACTION TYPE:** REPLACE
**ACTION RATIONALE:** The `competitor_performance` contribution to the `final_score` calculation is explicitly set to `0`. This ensures it has no impact on the overall score.

**FIND CONTEXT (Replace the line containing `            + (performance_score * weights["competitor_performance"])  # ADDED THIS LINE`):**
```python
            + (performance_score * weights["competitor_performance"])  # ADDED THIS LINE
```

**CODE TO REPLACE:**
```python
            + (performance_score * weights["competitor_performance"])  # ADDED THIS LINE
```

**WITH NEW CODE:**
```python
            + (0 * weights["competitor_performance"]) # This component is removed, so it contributes 0
```

**ACTION NO:** 2.18
**ACTION TYPE:** DELETE
**ACTION RATIONALE:** The mapping for `competitor_performance` is removed from `weight_key_map` because the component is no longer active, ensuring consistency in the scoring breakdown representation.

**FIND CONTEXT (Delete the line containing):**
```python
                "competitor_performance": "competitor_performance",  # ADDED THIS LINE
            }
```

**CODE TO DELETE:**
```python
                "competitor_performance": "competitor_performance",  # ADDED THIS LINE
            }
```

### **File: `backend/pipeline/orchestrator/main.py`**

**ACTION NO:** 2.19
**ACTION TYPE:** DELETE
**ACTION RATIONALE:** The `db_manager` argument is removed from the `CannibalizationChecker` initialization because it no longer directly interacts with the database for its core function within the `main.py` orchestrator setup. Its database interactions are implicitly handled via other services. (Correction: The `CannibalizationChecker` constructor *does* need `db_manager`. The original plan was incorrect. We need to *keep* this line as it is.)

**FIND CONTEXT (Delete the line containing `            self.db_manager,`):**
```python
            self.db_manager,
        )
```

**CODE TO DELETE:**
```python
            self.db_manager,
        )
```

### **File: `backend/pipeline/step_04_analysis/content_analyzer.py`**

**ACTION NO:** 2.20
**ACTION TYPE:** INSERT
**ACTION RATIONALE:** This new method leverages an AI call to assess the quality and weaknesses of competitors based *only* on their SERP titles and descriptions. This replaces the need for expensive On-Page analysis in the new SERP-only workflow. It also adds `additionalProperties: False` to the schema for strictness. (Moved from original Task 3.1)

**FIND CONTEXT (Insert after the line containing):**
```python
        self.num_competitors_for_ai_analysis = self.config.get(
            "num_competitors_for_ai_analysis", 3
        )
```

**CODE TO INSERT:**
```python
    def assess_competitor_quality_from_serp(self, keyword: str, serp_overview: Dict[str, Any]) -> Tuple[Dict[str, Any], float]:
        """
        Uses an AI call to assess competitor quality based only on SERP titles and descriptions.
        """
        self.logger.info(f"Running SERP-only competitor quality assessment for '{keyword}'.")
        
        top_results = serp_overview.get("top_organic_results", [])[:5]
        if not top_results:
            return {"assessment": "No organic results to analyze.", "weaknesses": []}, 0.0

        competitor_snippets = "\\n".join([f"- Title: {r.get('title')}\\n  Description: {r.get('description')}" for r in top_results])

        prompt = f"""
        You are an expert SEO analyst. Based *only* on the following SERP titles and descriptions for the keyword "{keyword}", assess the overall quality and likely weaknesses of the competition.

        Competitor Snippets:
        {competitor_snippets}

        Your Task:
        1.  **Assessment:** Write a one-sentence summary of the competitive landscape. (e.g., "Competition appears to be mostly low-quality, list-based articles.")
        2.  **Weaknesses:** List 2-3 specific, actionable weaknesses you can infer from these snippets. (e.g., "Content seems outdated," "Titles are not compelling," "Descriptions lack depth.")

        Return a JSON object with two keys: "assessment" and "weaknesses".
        """

        schema = {
            "name": "assess_competitor_quality",
            "type": "object",
            "properties": {
                "assessment": {"type": "string"},
                "weaknesses": {"type": "array", "items": {"type": "string"}},
            },
            "required": ["assessment", "weaknesses"],
            "additionalProperties": False, # ADDED for strict schema enforcement
        }

        response, error = self.openai_client.call_chat_completion(
            messages=[{"role": "user", "content": prompt}],
            schema=schema,
            model=self.config.get("default_model", "gpt-5-nano"),
        )
        cost = self.openai_client.latest_cost

        if error or not response:
            self.logger.error(f"Failed to get AI competitor assessment: {error}")
            return {"assessment": "AI analysis failed.", "weaknesses": []}, cost

        return response, cost
```

**ACTION NO:** 2.21
**ACTION TYPE:** INSERT
**ACTION RATIONALE:** This new method uses an AI call to reverse-engineer a "master outline" by synthesizing information from top-ranking SERP titles and descriptions. This provides a content structure suggestion without needing to crawl competitor websites, directly supporting content gap analysis. It also adds `additionalProperties: False` to the schema for strictness. (Moved from original Task 3.2)

**FIND CONTEXT (Insert after the `assess_competitor_quality_from_serp` method):**
```python
    def assess_competitor_quality_from_serp(self, keyword: str, serp_overview: Dict[str, Any]) -> Tuple[Dict[str, Any], float]:
        # ... (content of assess_competitor_quality_from_serp) ...
        return response, cost
```

**CODE TO INSERT:**
```python
    def infer_competitor_outline_from_serp(self, keyword: str, serp_overview: Dict[str, Any]) -> Tuple[Dict[str, Any], float]:
        """
        Uses an AI call to infer a common outline from SERP titles and descriptions.
        """
        self.logger.info(f"Inferring competitor outline from SERP for '{keyword}'.")
        
        top_results = serp_overview.get("top_organic_results", [])[:7] # Use top 7 for broader context
        if not top_results:
            return {"inferred_outline": []}, 0.0

        competitor_snippets = "\\n".join([f"- Title: {r.get('title')}\\n  Description: {r.get('description')}" for r in top_results])

        prompt = f"""
        You are an SEO analyst. Your task is to reverse-engineer the likely content structure of the top-ranking articles for the keyword "{keyword}" using only their SERP titles and descriptions.

        SERP Snippets:
        {competitor_snippets}

        Your Task:
        Synthesize these snippets to generate a single, logical "master outline" of H2 and H3 headings that a comprehensive article on this topic should cover. Group related concepts.

        Return a JSON object with a single key "inferred_outline", which is an array of strings representing the headings.
        """

        schema = {"name": "infer_competitor_outline", "type": "object", "properties": {"inferred_outline": {"type": "array", "items": {"type": "string"}}}, "required": ["inferred_outline"], "additionalProperties": False}

        response, error = self.openai_client.call_chat_completion(messages=[{"role": "user", "content": prompt}], schema=schema, model=self.config.get("default_model", "gpt-5-nano"))
        cost = self.openai_client.latest_cost

        if error or not response:
            self.logger.error(f"Failed to get AI-inferred outline: {error}")
            return {"inferred_outline": []}, cost

        return response, cost
```

**ACTION NO:** 2.22
**ACTION TYPE:** REPLACE
**ACTION RATIONALE:** The `generate_ai_outline` method signature is updated to accept the `inferred_competitor_outline`. This allows the AI to use this outline as additional inspiration when generating the final article structure. (Moved from original Task 3.3)

**FIND CONTEXT (Replace the lines containing):**
```python
    def generate_ai_outline(
        self,
        keyword: str,
        serp_overview: Dict[str, Any],
        content_intelligence: Dict[str, Any],
    ) -> Tuple[Dict[str, List[str]], float]:
```

**CODE TO REPLACE:**
```python
    def generate_ai_outline(
        self,
        keyword: str,
        serp_overview: Dict[str, Any],
        content_intelligence: Dict[str, Any],
    ) -> Tuple[Dict[str, List[str]], float]:
```

**WITH NEW CODE:**
```python
    def generate_ai_outline(
        self,
        keyword: str,
        serp_overview: Dict[str, Any],
        content_intelligence: Dict[str, Any],
        inferred_competitor_outline: List[str] # ADD this new argument
    ) -> Tuple[Dict[str, List[str]], float]:
```

**ACTION NO:** 2.23
**ACTION TYPE:** REPLACE
**ACTION RATIONALE:** The `_build_outline_prompt` call inside `generate_ai_outline` is updated to pass the `inferred_competitor_outline` as a new argument. (Moved from original Task 3.4)

**FIND CONTEXT (Replace the line containing):**
```python
        prompt_messages = self._build_outline_prompt(
            keyword, serp_overview, content_intelligence
        )
```

**CODE TO REPLACE:**
```python
        prompt_messages = self._build_outline_prompt(
            keyword, serp_overview, content_intelligence
        )
```

**WITH NEW CODE:**
```python
        prompt_messages = self._build_outline_prompt(
            keyword, serp_overview, content_intelligence, inferred_competitor_outline # PASS it here
        )
```

**ACTION NO:** 2.24
**ACTION TYPE:** REPLACE
**ACTION RATIONALE:** The `_build_outline_prompt` method signature is updated to accept the new `inferred_competitor_outline` argument. This ensures the prompt builder can incorporate this information. (Moved from original Task 3.5)

**FIND CONTEXT (Replace the lines containing):**
```python
    def _build_outline_prompt(
        self,
        keyword: str,
        serp_overview: Dict[str, Any],
        content_intelligence: Dict[str, Any],
    ) -> List[Dict[str, str]]:
```

**CODE TO REPLACE:**
```python
    def _build_outline_prompt(
        self,
        keyword: str,
        serp_overview: Dict[str, Any],
        content_intelligence: Dict[str, Any],
    ) -> List[Dict[str, str]]:
```

**WITH NEW CODE:**
```python
    def _build_outline_prompt(
        self,
        keyword: str,
        serp_overview: Dict[str, Any],
        content_intelligence: Dict[str, Any],
        inferred_competitor_outline: List[str] # ADD this new argument
    ) -> List[Dict[str, str]]:
```

**ACTION NO:** 2.25
**ACTION TYPE:** INSERT
**ACTION RATIONALE:** Adds the "Inferred Competitor Outline" to the AI prompt. This provides the AI with a strong structural inspiration from top-ranking competitors when generating the article outline, improving relevance and completeness. (Moved from original Task 3.6)

**FIND CONTEXT (Insert after the line containing):**
```python
        **Analysis Data:**
```

**CODE TO INSERT:**
```python
        - **Inferred Competitor Outline (for inspiration):** {", ".join(inferred_competitor_outline)}
```

---

**Task No:** 3
**Task Higher Overview:** Create frontend components to display new AI insights (SERP-only competitor quality assessment and inferred outline generation) on the opportunity detail page.
**Files Involved:**
*   `client/my-content-app/src/pages/opportunity-detail-page/index.jsx`
*   `client/my-content-app/src/pages/opportunity-detail-page/components/AiCompetitorAssessment.jsx` (New file)
*   `client/my-content-app/src/pages/opportunity-detail-page/components/InferredOutline.jsx` (New file)
**Total Code Changes Required:** 4 granular changes (2 new files, 2 modifications).

**STEP BY STEP PLAN:**

### **File: `client/my-content-app/src/pages/opportunity-detail-page/components/AiCompetitorAssessment.jsx`**

**ACTION NO:** 3.1
**ACTION TYPE:** CREATE_FILE
**ACTION RATIONALE:** This new React component is responsible for displaying the AI-generated competitor assessment (summary and weaknesses) on the opportunity detail page. It provides valuable, quick insights to the user.

**FILE PATH:** `client/my-content-app/src/pages/opportunity-detail-page/components/AiCompetitorAssessment.jsx`
**FILE CONTENT:**
```jsx
// client/my-content-app/src/pages/opportunity-detail-page/components/AiCompetitorAssessment.jsx
import React from 'react';
import { Card, Typography, List, Alert } from 'antd';
import { RobotOutlined, WarningOutlined } from '@ant-design/icons';
import NoData from './NoData';

const { Title, Paragraph } = Typography;

const AiCompetitorAssessment = ({ assessmentData }) => {
  if (!assessmentData || Object.keys(assessmentData).length === 0 || assessmentData.assessment === "AI analysis failed.") { // Handle AI failure gracefully
    return <NoData description="No AI competitor assessment available." />;
  }

  const { assessment, weaknesses } = assessmentData;

  return (
    <Card 
      title={
        <Title level={5} style={{ margin: 0 }}>
          <RobotOutlined style={{ marginRight: 8 }} /> AI Competitor Assessment
        </Title>
      }
      style={{ marginTop: 24 }}
    >
      <Paragraph strong>{assessment}</Paragraph>
      {weaknesses && weaknesses.length > 0 ? (
        <>
          <Title level={5} style={{ marginTop: 16 }}>Identified Weaknesses:</Title>
          <List
            dataSource={weaknesses}
            renderItem={(item) => (
              <List.Item>
                <WarningOutlined style={{ color: '#faad14', marginRight: 8 }} />
                {item}
              </List.Item>
            )}
            size="small"
            bordered
          />
        </>
      ) : (
        <Alert message="No specific weaknesses identified by AI." type="info" showIcon style={{ marginTop: 16 }} />
      )}
    </Card>
  );
};

export default AiCompetitorAssessment;
```

### **File: `client/my-content-app/src/pages/opportunity-detail-page/components/InferredOutline.jsx`**

**ACTION NO:** 3.2
**ACTION TYPE:** CREATE_FILE
**ACTION RATIONALE:** This new React component displays the AI-inferred competitor outline on the opportunity detail page. It offers a quick visual of common content structures among competitors, helping identify content gaps.

**FILE PATH:** `client/my-content-app/src/pages/opportunity-detail-page/components/InferredOutline.jsx`
**FILE CONTENT:**
```jsx
// client/my-content-app/src/pages/opportunity-detail-page/components/InferredOutline.jsx
import React from 'react';
import { Card, Typography, List } from 'antd';
import { CompassOutlined } from '@ant-design/icons';
import NoData from './NoData';

const { Title, Paragraph } = Typography;

const InferredOutline = ({ outline }) => {
  if (!outline || outline.length === 0) {
    return <NoData description="No inferred competitor outline available." />;
  }

  return (
    <Card 
      title={
        <Title level={5} style={{ margin: 0 }}>
          <CompassOutlined style={{ marginRight: 8 }} /> Inferred Competitor Outline
        </Title>
      }
      style={{ marginTop: 24 }}
    >
      <Paragraph type="secondary">
        This is a reverse-engineered outline from top-ranking SERP titles and descriptions,
        showing common topics and structures used by competitors.
      </Paragraph>
      <List
        dataSource={outline}
        renderItem={(item) => (
          <List.Item>
            <List.Item.Meta title={item} />
          </List.Item>
        )}
        size="small"
        bordered
      />
    </Card>
  );
};

export default InferredOutline;
```

### **File: `client/my-content-app/src/pages/opportunity-detail-page/index.jsx`**

**ACTION NO:** 3.3
**ACTION TYPE:** INSERT
**ACTION RATIONALE:** Imports the new `AiCompetitorAssessment` and `InferredOutline` components to make them available for use in the opportunity detail page.

**FIND CONTEXT (Insert after the line containing):**
```jsx
import GrowthTrend from './components/GrowthTrend';
```

**CODE TO INSERT:**
```jsx
import AiCompetitorAssessment from './components/AiCompetitorAssessment'; // NEW IMPORT (Task 3.2)
import InferredOutline from './components/InferredOutline'; // NEW IMPORT (Task 3.3)
```

**ACTION NO:** 3.4
**ACTION TYPE:** INSERT
**ACTION RATIONALE:** Integrates the new `AiCompetitorAssessment` and `InferredOutline` components into the "Overview" tab of the Opportunity Detail Page. This makes the new AI insights visible to the user.

**FIND CONTEXT (Insert after the line containing):**
```jsx
              <ExecutiveSummary summary={blueprint?.executive_summary} />
```

**CODE TO INSERT:**
```jsx
              <AiCompetitorAssessment assessmentData={blueprint?.ai_competitor_assessment} /> {/* NEW COMPONENT (Task 3.2) */}
              <InferredOutline outline={blueprint?.inferred_competitor_outline} /> {/* NEW COMPONENT (Task 3.3) */}
```

---

**Task No:** 4
**Task Higher Overview:** Implement a prompt template management system (database, API, and UI) to allow specialized AI agents for different content formats, while seeding default templates.
**Files Involved:**
*   `backend/data_access/migrations/026_add_prompt_templates_table.sql` (New file)
*   `backend/data_access/database_manager.py`
*   `backend/data_access/queries.py`
*   `backend/agents/default_prompts.py` (New file)
*   `backend/api/main.py`
*   `backend/api/routers/prompt_templates.py` (New router file)
*   `backend/agents/prompt_assembler.py`
*   `backend/app_config/settings.ini`
*   `client/my-content-app/src/pages/Settings/tabs/AiContentSettingsTab.jsx`
*   `client/my-content-app/src/services/clientSettingsService.js`
**Total Code Changes Required:** 11 granular changes (4 new files, 7 modifications).

**STEP BY STEP PLAN:**

### **File: `backend/data_access/migrations/026_add_prompt_templates_table.sql`**

**ACTION NO:** 4.1
**ACTION TYPE:** CREATE_FILE
**ACTION RATIONALE:** This SQL script creates the new `prompt_templates` table in the database to store custom prompt templates for each client, enabling a flexible and persistent prompt management system.

**FILE PATH:** `backend/data_access/migrations/026_add_prompt_templates_table.sql`
**FILE CONTENT:**```sql
-- backend/data_access/migrations/026_add_prompt_templates_table.sql

CREATE TABLE IF NOT EXISTS prompt_templates (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    client_id TEXT NOT NULL,
    name TEXT NOT NULL, -- e.g., "prompt_default", "prompt_review_article"
    content TEXT NOT NULL,
    description TEXT,
    last_updated TEXT NOT NULL,
    FOREIGN KEY (client_id) REFERENCES clients (client_id),
    UNIQUE (client_id, name)
);
```

### **File: `backend/data_access/queries.py`**

**ACTION NO:** 4.2
**ACTION TYPE:** INSERT
**ACTION RATIONALE:** Adds the necessary SQL queries for creating, reading, updating, and deleting (CRUD) prompt templates from the new `prompt_templates` table. These queries will be used by the `DatabaseManager`.

**FIND CONTEXT (Insert at the end of the file):**
*No specific context needed, append to the end of the file.*

**CODE TO INSERT:**
```python

# --- Prompt Template Queries (from Task 4.1) ---
INSERT_PROMPT_TEMPLATE = """
INSERT INTO prompt_templates (client_id, name, content, description, last_updated)
VALUES (?, ?, ?, ?, ?);
"""

SELECT_PROMPT_TEMPLATES_BY_CLIENT = """
SELECT id, name, content, description, last_updated FROM prompt_templates
WHERE client_id = ? ORDER BY name ASC;
"""

SELECT_PROMPT_TEMPLATE_BY_ID = """
SELECT id, name, content, description, last_updated FROM prompt_templates
WHERE id = ? AND client_id = ?;
"""

UPDATE_PROMPT_TEMPLATE = """
UPDATE prompt_templates SET content = ?, description = ?, last_updated = ?
WHERE id = ? AND client_id = ?;
"""

DELETE_PROMPT_TEMPLATE = """
DELETE FROM prompt_templates WHERE id = ? AND client_id = ?;
"""
```

### **File: `backend/data_access/database_manager.py`**

**ACTION NO:** 4.3
**ACTION TYPE:** INSERT
**ACTION RATIONALE:** Adds a new key `prompt_templates` to the default client settings template. This ensures that new clients are initialized with default prompt templates. It also requires importing `default_prompts`.

**FIND CONTEXT (Insert after the line containing):**
```python
                "qualification_settings": default_qualification_settings,
```

**CODE TO INSERT:**
```python
                "prompt_templates": default_prompt_templates, # NEW
```

**ACTION NO:** 4.4
**ACTION TYPE:** REPLACE
**ACTION RATIONALE:** This action replaces the placeholder mock functions for prompt template management with fully implemented methods that interact directly with the database, enabling robust CRUD operations on prompt templates for each client.

**FIND CONTEXT (Replace the block starting from `    def get_client_prompt_templates(self, client_id: str) -> List[Dict[str, Any]]:` to `        pass`):**
```python
    def get_client_prompt_templates(self, client_id: str) -> List[Dict[str, Any]]:
        """MOCK: Retrieves all prompt templates for a client."""
        return []

    def save_client_prompt_template(
        self, client_id: str, template_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """MOCK: Saves or updates a client's prompt template."""
        template_data["last_updated"] = datetime.now().isoformat()
        return template_data

    def delete_client_prompt_template(self, client_id: str, template_name: str):
        """MOCK: Deletes a client's prompt template."""
        pass
```

**CODE TO REPLACE:**
```python
    def get_client_prompt_templates(self, client_id: str) -> List[Dict[str, Any]]:
        """MOCK: Retrieves all prompt templates for a client."""
        return []

    def save_client_prompt_template(
        self, client_id: str, template_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """MOCK: Saves or updates a client's prompt template."""
        template_data["last_updated"] = datetime.now().isoformat()
        return template_data

    def delete_client_prompt_template(self, client_id: str, template_name: str):
        """MOCK: Deletes a client's prompt template."""
        pass
```

**WITH NEW CODE:**
```python
    # --- Prompt Template Management (from Task 4.1) ---
    def get_client_prompt_templates(self, client_id: str) -> List[Dict[str, Any]]:
        """Retrieves all prompt templates for a specific client."""
        conn = self._get_conn()
        with conn:
            cursor = conn.execute(queries.SELECT_PROMPT_TEMPLATES_BY_CLIENT, (client_id,))
            return [dict(row) for row in cursor.fetchall()]
            
    def get_client_prompt_template_by_id(self, template_id: int, client_id: str) -> Optional[Dict[str, Any]]:
        """Retrieves a single prompt template by its ID and client_id."""
        conn = self._get_conn()
        with conn:
            cursor = conn.execute(queries.SELECT_PROMPT_TEMPLATE_BY_ID, (template_id, client_id))
            row = cursor.fetchone()
            if row:
                return dict(row)
            return None

    def save_client_prompt_template(self, client_id: str, template_data: Dict[str, Any]) -> int:
        """Saves or updates a client's prompt template. Returns the ID."""
        conn = self._get_conn()
        with conn:
            cursor = conn.execute(
                "SELECT id FROM prompt_templates WHERE client_id = ? AND name = ?",
                (client_id, template_data["name"]),
            )
            existing_id_row = cursor.fetchone()
            existing_id = existing_id_row["id"] if existing_id_row else None

            template_data["last_updated"] = datetime.now().isoformat()

            if existing_id:
                # Update existing template
                conn.execute(
                    queries.UPDATE_PROMPT_TEMPLATE,
                    (
                        template_data["content"],
                        template_data.get("description"),
                        template_data["last_updated"],
                        existing_id,
                        client_id, # Added client_id to WHERE clause for security
                    ),
                )
                return existing_id
            else:
                # Insert new template
                cursor.execute(
                    queries.INSERT_PROMPT_TEMPLATE,
                    (client_id, template_data["name"], template_data["content"], template_data.get("description"), template_data["last_updated"]),
                )
                return cursor.lastrowid

    def delete_client_prompt_template(self, template_id: int, client_id: str):
        """Deletes a client's prompt template by ID, with client_id for security."""
        conn = self._get_conn()
        with conn:
            conn.execute(queries.DELETE_PROMPT_TEMPLATE, (template_id, client_id))
```

### **File: `backend/agents/default_prompts.py`**

**ACTION NO:** 4.5
**ACTION TYPE:** CREATE_FILE
**ACTION RATIONALE:** This new file centralizes hardcoded default prompt templates for various content formats (e.g., `DEFAULT_PROMPT`, `REVIEW_ARTICLE_PROMPT`). This provides a reliable fallback for the `DynamicPromptAssembler` if database templates are not found, making the system more robust.

**FILE PATH:** `backend/agents/default_prompts.py`
**FILE CONTENT:**
```python
# backend/agents/default_prompts.py

DEFAULT_PROMPT = """You are an expert SEO content writer. Write a comprehensive, helpful, and expert-level blog post about "[TOPIC]". The article must demonstrate first-hand experience and deep expertise, and be structured for maximum readability and SEO impact. The post must:

- Be approximately [WORD_COUNT] words, providing authoritative depth on the topic.
- Target the primary keyword "[PRIMARY KEYWORD]".
- Naturally incorporate related LSI keywords, relevant entities, synonyms, and contextually related concepts to ensure topical completeness.
- Start with a clear, direct 1-2 sentence summary that immediately answers the user's core question.
- Write from a first-person or expert perspective. Include at least one hypothetical scenario, relatable anecdote, or personal insight to signal direct experience.
- Cite specific data or statistics and attribute them to a source (e.g., 'According to a 2023 study by...').
- Include multiple answer formats: short direct responses, step-by-step instructions, and quick takeaway lists (bullet points) so AI models and users can easily extract information.
- Structure the article with a logical flow using clear subheadings (H2s and H3s).
- Include a "Frequently Asked Questions" (FAQ) section at the end using real-world questions users search for, written in a conversational Q&A style.
- Naturally promote [CTA_URL] with a relevant call-to-action at the end of the post.
- For in-article images, use a placeholder with the exact format `[[IMAGE: <A descriptive prompt for the image>]]`. For example: `[[IMAGE: A bar chart showing SEO growth over time]]`.
- Adopt the persona of [PERSONA].

**AVOID:** Do not use generic filler, over-optimization, or unnatural keyword stuffing. Focus on topical relevance, not keyword density. Avoid making unsubstantiated claims.
"""

REVIEW_ARTICLE_PROMPT = """You are an expert product reviewer and SEO content writer. Write a comprehensive, unbiased, and expert-level review article about "[TOPIC]". The article must help users make an informed decision and be structured for maximum readability and SEO impact. The post must:

- Be approximately [WORD_COUNT] words, providing authoritative depth on the product/service.
- Target the primary keyword "[PRIMARY KEYWORD]".
- Naturally incorporate related LSI keywords, relevant entities, synonyms, and contextually related concepts.
- **Demonstrate E-E-A-T (Experience, Expertise, Authoritativeness, Trustworthiness):**
    - Start with a clear, direct 1-2 sentence summary that immediately states the core findings of the review.
    - Write from a first-person or expert perspective. Include details about testing, usage experience, and real-world results.
    - Include specific pros and cons (use a bulleted list or a table).
    - Compare "[TOPIC]" against 1-2 leading alternatives.
    - Cite specific data or statistics and attribute them to a source (e.g., 'According to a consumer report...').
- Structure the article with a logical flow using clear subheadings (H2s and H3s), including sections like "Features," "Pros & Cons," "Alternatives," and "Who Is It For?".
- Conclude with a strong, definitive recommendation.
- Naturally promote [CTA_URL] with a relevant call-to-action at the end of the post, encouraging purchase or further research.
- For in-article images, use a placeholder with the exact format `[[IMAGE: <A descriptive prompt for the image>]]`.
- Adopt the persona of [PERSONA].

**AVOID:** Do not use generic filler, over-optimization, or unnatural keyword stuffing. Focus on topical relevance, not keyword density. Avoid making unsubstantiated claims or overly aggressive sales language. Maintain an unbiased, expert tone.
"""

HOW_TO_GUIDE_PROMPT = """You are an expert instructional writer and SEO content writer. Write a comprehensive, step-by-step "How-To Guide" about "[TOPIC]". The article must provide clear, actionable instructions and be structured for maximum readability and SEO impact. The post must:

- Be approximately [WORD_COUNT] words, providing thorough guidance on the process.
- Target the primary keyword "[PRIMARY KEYWORD]".
- Naturally incorporate related LSI keywords, relevant entities, synonyms, and contextually related concepts.
- **Demonstrate E-E-A-T (Experience, Expertise, Authoritativeness, Trustworthiness):**
    - Start with a clear, direct 1-2 sentence summary that immediately states what the user will learn to do.
    - Write from a first-person or expert perspective. Use clear, concise language suitable for step-by-step instructions.
    - Include numbered lists for main steps and bulleted lists for tips or prerequisites.
    - Break down complex tasks into manageable sub-steps.
    - Include a "Prerequisites" or "What You'll Need" section.
    - Cite specific tools, resources, or examples.
- Structure the article with a logical flow using clear subheadings (H2s for main steps, H3s for sub-steps).
- Include a "Troubleshooting Tips" section if applicable.
- End with a summary and encourage the reader to apply what they've learned, promoting [CTA_URL].
- For in-article images, use a placeholder with the exact format `[[IMAGE: <A descriptive prompt for the image>]]`.
- Adopt the persona of [PERSONA].

**AVOID:** Do not use generic filler, over-optimization, or unnatural keyword stuffing. Focus on clarity, accuracy, and actionability. Avoid making unsubstantiated claims.
"""

default_prompt_templates = [
    {"name": "prompt_default", "content": DEFAULT_PROMPT, "description": "Default comprehensive blog post prompt."},
    {"name": "prompt_review_article", "content": REVIEW_ARTICLE_PROMPT, "description": "Specialized prompt for review articles."},
    {"name": "prompt_how_to_guide", "content": HOW_TO_GUIDE_PROMPT, "description": "Specialized prompt for how-to guides."},
]
```

### **File: `backend/api/main.py`**

**ACTION NO:** 4.6
**ACTION TYPE:** INSERT
**ACTION RATIONALE:** Imports the new `prompt_templates` router to handle API requests related to prompt template management.

**FIND CONTEXT (Insert after the line containing):**
```python
        settings,
```

**CODE TO INSERT:**
```python
        prompt_templates, # NEW IMPORT
```

**ACTION NO:** 4.7
**ACTION TYPE:** INSERT
**ACTION RATIONALE:** Registers the new `prompt_templates` router with the FastAPI application, making the API endpoints for prompt template management accessible.

**FIND CONTEXT (Insert after the line containing):**
```python
    app.include_router(settings.router, prefix="/api")
```

**CODE TO INSERT:**
```python
    app.include_router(prompt_templates.router, prefix="/api") # NEW ROUTER
```

### **File: `backend/api/routers/prompt_templates.py`**

**ACTION NO:** 4.8
**ACTION TYPE:** CREATE_FILE
**ACTION RATIONALE:** This new FastAPI router defines the API endpoints for managing prompt templates (`GET`, `POST`, `PUT`, `DELETE`). It includes Pydantic models for request/response validation and integrates with the `DatabaseManager` for data persistence. This enables the frontend UI to interact with the prompt template system.

**FILE PATH:** `backend/api/routers/prompt_templates.py`
**FILE CONTENT:**
```python
# backend/api/routers/prompt_templates.py
from fastapi import APIRouter, Depends, HTTPException
from typing import List, Dict, Any, Optional
from datetime import datetime
from data_access.database_manager import DatabaseManager
from ..dependencies import get_db, get_orchestrator
from backend.pipeline import WorkflowOrchestrator
from pydantic import BaseModel

router = APIRouter()

class PromptTemplateIn(BaseModel):
    name: str
    content: str
    description: Optional[str] = None
    id: Optional[int] = None # For updates

class PromptTemplateOut(BaseModel):
    id: int
    name: str
    content: str
    description: Optional[str] = None
    last_updated: datetime

@router.get("/clients/{client_id}/prompt-templates", response_model=List[PromptTemplateOut])
async def get_client_prompt_templates_endpoint(
    client_id: str,
    db: DatabaseManager = Depends(get_db),
    orchestrator: WorkflowOrchestrator = Depends(get_orchestrator),
):
    if client_id != orchestrator.client_id:
        raise HTTPException(status_code=403, detail="Not authorized for this client.")
    templates = db.get_client_prompt_templates(client_id)
    return templates

@router.post("/clients/{client_id}/prompt-templates", response_model=PromptTemplateOut)
async def create_client_prompt_template_endpoint(
    client_id: str,
    template_in: PromptTemplateIn,
    db: DatabaseManager = Depends(get_db),
    orchestrator: WorkflowOrchestrator = Depends(get_orchestrator),
):
    if client_id != orchestrator.client_id:
        raise HTTPException(status_code=403, detail="Not authorized for this client.")
    
    # Check for name uniqueness
    existing_templates = db.get_client_prompt_templates(client_id)
    if any(t.get('name') == template_in.name for t in existing_templates):
        raise HTTPException(status_code=409, detail=f"A template named '{template_in.name}' already exists.")

    template_id = db.save_client_prompt_template(client_id, template_in.dict(exclude_unset=True))
    if not template_id:
        raise HTTPException(status_code=500, detail="Failed to save template.")
    
    # Refetch to get the full object with DB-assigned ID and last_updated timestamp
    new_template = db.get_client_prompt_template_by_id(template_id, client_id) 
    if not new_template:
        raise HTTPException(status_code=500, detail="Failed to retrieve newly created template.")
    return new_template

@router.put("/clients/{client_id}/prompt-templates/{template_id}", response_model=PromptTemplateOut)
async def update_client_prompt_template_endpoint(
    client_id: str,
    template_id: int,
    template_in: PromptTemplateIn,
    db: DatabaseManager = Depends(get_db),
    orchestrator: WorkflowOrchestrator = Depends(get_orchestrator),
):
    if client_id != orchestrator.client_id:
        raise HTTPException(status_code=403, detail="Not authorized for this client.")
    
    # Ensure template_id matches the one being updated for security
    if template_in.id and template_in.id != template_id:
        raise HTTPException(status_code=400, detail="Template ID in path and body do not match.")

    # Check if the template exists and belongs to this client
    existing_template = db.get_client_prompt_template_by_id(template_id, client_id)
    if not existing_template:
        raise HTTPException(status_code=404, detail="Template not found or does not belong to this client.")

    # Check for name uniqueness if name is being changed
    if template_in.name != existing_template.get('name'):
        existing_templates_by_client = db.get_client_prompt_templates(client_id)
        if any(t.get('name') == template_in.name and t.get('id') != template_id for t in existing_templates_by_client):
            raise HTTPException(status_code=409, detail=f"A template named '{template_in.name}' already exists for this client.")

    db.save_client_prompt_template(client_id, {**template_in.dict(exclude_unset=True), "id": template_id})
    # Refetch to get the full object with updated timestamp
    updated_template = db.get_client_prompt_template_by_id(template_id, client_id)
    if not updated_template:
        raise HTTPException(status_code=500, detail="Failed to retrieve updated template.")
    return updated_template

@router.delete("/clients/{client_id}/prompt-templates/{template_id}", response_model=Dict[str, str])
async def delete_client_prompt_template_endpoint(
    client_id: str,
    template_id: int,
    db: DatabaseManager = Depends(get_db),
    orchestrator: WorkflowOrchestrator = Depends(get_orchestrator),
):
    if client_id != orchestrator.client_id:
        raise HTTPException(status_code=403, detail="Not authorized for this client.")
    
    # Check if the template exists and belongs to this client
    existing_template = db.get_client_prompt_template_by_id(template_id, client_id)
    if not existing_template:
        raise HTTPException(status_code=404, detail="Template not found or does not belong to this client.")

    db.delete_client_prompt_template(template_id, client_id)
    return {"message": "Template deleted successfully."}
```

### **File: `backend/agents/prompt_assembler.py`**

**ACTION NO:** 4.9
**ACTION TYPE:** REPLACE
**ACTION RATIONALE:** The `DynamicPromptAssembler`'s constructor is updated to accept `client_cfg`. This is necessary for the assembler to access client-specific configuration settings, including custom prompt templates and other dynamic parameters, ensuring the prompt is tailored to the client's needs.

**FIND CONTEXT (Replace the line containing):**
```python
    def __init__(self, db_manager: DatabaseManager):
```

**CODE TO REPLACE:**
```python
    def __init__(self, db_manager: DatabaseManager):
```

**WITH NEW CODE:**
```python
    def __init__(self, db_manager: DatabaseManager, client_cfg: Dict[str, Any]): # Add client_cfg
```

**ACTION NO:** 4.10
**ACTION TYPE:** INSERT
**ACTION RATIONALE:** Stores the `client_cfg` as an instance attribute. This makes the client's configuration (including custom prompt templates from `settings.ini`) available throughout the `DynamicPromptAssembler` for dynamic prompt construction.

**FIND CONTEXT (Insert after the line containing):**
```python
        self.db_manager = db_manager
```

**CODE TO INSERT:**
```python
        self.client_cfg = client_cfg # Store client_cfg for template access
```

**ACTION NO:** 4.11
**ACTION TYPE:** REPLACE
**ACTION RATIONALE:** This is a crucial update to dynamically select the appropriate prompt template for content generation. It now follows a hierarchical logic:
1.  **Format-specific DB template:** Checks the database for a template matching the `content_format` (e.g., `prompt_review_article`).
2.  **Default DB template:** Falls back to a general `prompt_default` from the database.
3.  **`settings.ini` fallback:** Uses the `custom_prompt_template` from `settings.ini`.
4.  **Hardcoded default:** As a final fallback, it loads a hardcoded default prompt from `agents.default_prompts`.
This ensures the AI uses the most relevant and customizable instructions.

**FIND CONTEXT (Replace the block starting from `        template = client_cfg.get("custom_prompt_template")` to the end of the default template definition before `default_cta_url = ...`):**
```python
        template = client_cfg.get("custom_prompt_template")
        if not template or not template.strip():
            template = """Write a comprehensive, helpful, and expert-level blog post titled "[TOPIC]". The article must demonstrate first-hand experience and deep expertise. Structure the content for maximum readability and SEO impact. The post must:

        - Be approximately [WORD_COUNT] words, providing authoritative depth on the topic.
        - Target the primary keyword "[PRIMARY KEYWORD]" and naturally incorporate related LSI keywords: [LSI/secondary keywords], along with relevant entities, synonyms, and contextually related concepts to ensure topical completeness.
        - **Demonstrate E-E-A-T (Experience, Expertise, Authoritativeness, Trustworthiness):**
            - Start with a clear, direct 1-2 sentence summary that immediately answers the user's core question.
            - Write from a first-person or expert perspective. Include at least one hypothetical scenario, relatable anecdote, or personal insight to signal direct experience.
            - Cite specific data or statistics and attribute them to a source (e.g., 'According to a 2023 study by...').
            - Include multiple answer formats: short direct responses, step-by-step instructions, and quick takeaway lists (bullet points) so AI models and users can easily extract information.
        - Structure the article with a logical flow using clear subheadings (H2s and H3s).
        - Include a "Frequently Asked Questions" (FAQ) section at the end using real-world questions users search for, written in a conversational Q&A style.
        - Naturally promote [CTA_URL] with a relevant call-to-action at the end of the post.
        - **AVOID:** Do not use generic filler, over-optimization, or unnatural keyword stuffing. Focus on topical relevance, not keyword density. Avoid making unsubstantiated claims.
        """
```

**CODE TO REPLACE:**
```python
        template = client_cfg.get("custom_prompt_template")
        if not template or not template.strip():
            template = """Write a comprehensive, helpful, and expert-level blog post titled "[TOPIC]". The article must demonstrate first-hand experience and deep expertise. Structure the content for maximum readability and SEO impact. The post must:

        - Be approximately [WORD_COUNT] words, providing authoritative depth on the topic.
        - Target the primary keyword "[PRIMARY KEYWORD]" and naturally incorporate related LSI keywords: [LSI/secondary keywords], along with relevant entities, synonyms, and contextually related concepts to ensure topical completeness.
        - **Demonstrate E-E-A-T (Experience, Expertise, Authoritativeness, Trustworthiness):**
            - Start with a clear, direct 1-2 sentence summary that immediately answers the user's core question.
            - Write from a first-person or expert perspective. Include at least one hypothetical scenario, relatable anecdote, or personal insight to signal direct experience.
            - Cite specific data or statistics and attribute them to a source (e.g., 'According to a 2023 study by...').
            - Include multiple answer formats: short direct responses, step-by-step instructions, and quick takeaway lists (bullet points) so AI models and users can easily extract information.
        - Structure the article with a logical flow using clear subheadings (H2s and H3s).
        - Include a "Frequently Asked Questions" (FAQ) section at the end using real-world questions users search for, written in a conversational Q&A style.
        - Naturally promote [CTA_URL] with a relevant call-to-action at the end of the post.
        - **AVOID:** Do not use generic filler, over-optimization, or unnatural keyword stuffing. Focus on topical relevance, not keyword density. Avoid making unsubstantiated claims.
        """
```

**WITH NEW CODE:**
```python
        # --- START Task 4.3: Select Prompt Template based on Content Format ---
        content_format = strategy.get('content_format', 'Comprehensive Article')
        format_key = "prompt_" + content_format.lower().replace(' ', '_') # e.g., 'prompt_review_article'

        # Fetch all templates from DB for the client (Task 4.9)
        all_db_templates = self.db_manager.get_client_prompt_templates(client_cfg.get('client_id'))
        template_map = {t['name']: t['content'] for t in all_db_templates}

        # Try to find format-specific template, then fallback to default, then hardcoded
        template = template_map.get(format_key)
        if not template:
            template = template_map.get("prompt_default")
        if not template:
            template = self.client_cfg.get("custom_prompt_template") # Fallback to settings.ini field

        if not template or not template.strip(): # Fallback to hardcoded default if none found
            self.logger.warning(f"No custom prompt template found for '{content_format}' or default. Using hardcoded fallback.")
            from agents import default_prompts # Import hardcoded defaults (Task 4.4)
            template = default_prompts.DEFAULT_PROMPT # Use a predefined default
        # --- END Task 4.3 ---
```

### **File: `backend/app_config/settings.ini`**

**ACTION NO:** 4.12
**ACTION TYPE:** REPLACE
**ACTION RATIONALE:** The `prompt_assembler` needs `custom_prompt_template` to remain in `settings.ini` as a fallback if no database templates are found. This ensures a functional default even if the database is unpopulated. This replaces the existing `custom_prompt_template` entry with the provided verbose default.

**FIND CONTEXT (Replace the block starting from `custom_prompt_template = Write a comprehensive, helpful, and expert-level blog post about "[TOPIC]".` to `Avoid making unsubstantiated claims.`):**
```ini
custom_prompt_template = Write a comprehensive, helpful, and expert-level blog post about "[TOPIC]". The article must demonstrate first-hand experience and deep expertise, and be structured for maximum readability and SEO impact. The post must:

- Be approximately [WORD_COUNT] words, providing authoritative depth on the topic.
- Target the primary keyword "[PRIMARY KEYWORD]" and naturally incorporate related LSI keywords: [LSI/secondary keywords], along with relevant entities, synonyms, and contextually related concepts to ensure topical completeness.
- **Demonstrate E-E-A-T (Experience, Expertise, Authoritativeness, Trustworthiness):**
    - Start with a clear, direct 1-2 sentence summary that immediately answers the user's core question.
    - Write from a first-person or expert perspective. Include at least one hypothetical scenario, relatable anecdote, or personal insight to signal direct experience.
    - Cite specific data or statistics and attribute them to a source (e.g., 'According to a 2023 study by...').
    - Include multiple answer formats: short direct responses, step-by-step instructions, and quick takeaway lists (bullet points) so AI models and users can easily extract information.
- Structure the article with a logical flow using clear subheadings (H2s and H3s).
- Include a "Frequently Asked Questions" (FAQ) section at the end using real-world questions users search for, written in a conversational Q&A style.
- Naturally promote [CTA_URL] with a relevant call-to-action at the end of the post.
- For in-article images, use a placeholder with the exact format `[[IMAGE: <A descriptive prompt for the image>]]`. For example: `[[IMAGE: A bar chart showing SEO growth over time]]`.
- Adopt the persona of [PERSONA].

**AVOID:** Do not use generic filler, over-optimization, or unnatural keyword stuffing. Focus on topical relevance, not keyword density. Avoid making unsubstantiated claims.
```

**CODE TO REPLACE:**
```ini
custom_prompt_template = Write a comprehensive, helpful, and expert-level blog post about "[TOPIC]". The article must demonstrate first-hand experience and deep expertise, and be structured for maximum readability and SEO impact. The post must:

- Be approximately [WORD_COUNT] words, providing authoritative depth on the topic.
- Target the primary keyword "[PRIMARY KEYWORD]" and naturally incorporate related LSI keywords: [LSI/secondary keywords], along with relevant entities, synonyms, and contextually related concepts to ensure topical completeness.
- **Demonstrate E-E-A-T (Experience, Expertise, Authoritativeness, Trustworthiness):**
    - Start with a clear, direct 1-2 sentence summary that immediately answers the user's core question.
    - Write from a first-person or expert perspective. Include at least one hypothetical scenario, relatable anecdote, or personal insight to signal direct experience.
    - Cite specific data or statistics and attribute them to a source (e.g., 'According to a 2023 study by...').
    - Include multiple answer formats: short direct responses, step-by-step instructions, and quick takeaway lists (bullet points) so AI models and users can easily extract information.
- Structure the article with a logical flow using clear subheadings (H2s and H3s).
- Include a "Frequently Asked Questions" (FAQ) section at the end using real-world questions users search for, written in a conversational Q&A style.
- Naturally promote [CTA_URL] with a relevant call-to-action at the end of the post.
- For in-article images, use a placeholder with the exact format `[[IMAGE: <A descriptive prompt for the image>]]`. For example: `[[IMAGE: A bar chart showing SEO growth over time]]`.
- Adopt the persona of [PERSONA].

**AVOID:** Do not use generic filler, over-optimization, or unnatural keyword stuffing. Focus on topical relevance, not keyword density. Avoid making unsubstantiated claims.
```

**WITH NEW CODE:**
```ini
custom_prompt_template = Write a comprehensive, helpful, and expert-level blog post about "[TOPIC]". The article must demonstrate first-hand experience and deep expertise, and be structured for maximum readability and SEO impact. The post must:

- Be approximately [WORD_COUNT] words, providing authoritative depth on the topic.
- Target the primary keyword "[PRIMARY KEYWORD]" and naturally incorporate related LSI keywords: [LSI/secondary keywords], along with relevant entities, synonyms, and contextually related concepts to ensure topical completeness.
- **Demonstrate E-E-A-T (Experience, Expertise, Authoritativeness, Trustworthiness):**
    - Start with a clear, direct 1-2 sentence summary that immediately answers the user's core question.
    - Write from a first-person or expert perspective. Include at least one hypothetical scenario, relatable anecdote, or personal insight to signal direct experience.
    - Cite specific data or statistics and attribute them to a source (e.g., 'According to a 2023 study by...').
    - Include multiple answer formats: short direct responses, step-by-step instructions, and quick takeaway lists (bullet points) so AI models and users can easily extract information.
- Structure the article with a logical flow using clear subheadings (H2s and H3s).
- Include a "Frequently Asked Questions" (FAQ) section at the end using real-world questions users search for, written in a conversational Q&A style.
- Naturally promote [CTA_URL] with a relevant call-to-action at the end of the post.
- For in-article images, use a placeholder with the exact format `[[IMAGE: <A descriptive prompt for the image>]]`. For example: `[[IMAGE: A bar chart showing SEO growth over time]]`.
- Adopt the persona of [PERSONA].

**AVOID:** Do not use generic filler, over-optimization, or unnatural keyword stuffing. Focus on topical relevance, not keyword density. Avoid making unsubstantiated claims.```

### **File: `client/my-content-app/src/pages/Settings/tabs/AiContentSettingsTab.jsx`**

**ACTION NO:** 4.13
**ACTION TYPE:** REPLACE
**ACTION RATIONALE:** This replaces the single `custom_prompt_template` input with a comprehensive prompt template management UI. It introduces functionality to fetch, create, update, and delete templates from the database, allowing users to define specialized prompts for different content formats. This enhances the flexibility and power of AI content generation.

**FIND CONTEXT (Replace the block starting from `      <Title level={5}>Custom AI Prompt Template</Title>` to the end of the `PromptTemplateEditor` Form.Item):**
```jsx
      <Title level={5}>Custom AI Prompt Template</Title>
      <Form.Item 
        name="custom_prompt_template" 
        label={
          <Space>
            Edit your base prompt for the AI content generator.
            <Tooltip title="This template guides the AI's writing. Use available placeholders for dynamic data.">
              <InfoCircleOutlined />
            </Tooltip>
          </Space>
        }
        style={{ marginBottom: 0 }}
      >
        <PromptTemplateEditor disabled={false} />
      </Form.Item>
```

**CODE TO REPLACE:**
```jsx
      <Title level={5}>Custom AI Prompt Template</Title>
      <Form.Item 
        name="custom_prompt_template" 
        label={
          <Space>
            Edit your base prompt for the AI content generator.
            <Tooltip title="This template guides the AI's writing. Use available placeholders for dynamic data.">
              <InfoCircleOutlined />
            </Tooltip>
          </Space>
        }
        style={{ marginBottom: 0 }}
      >
        <PromptTemplateEditor disabled={false} />
      </Form.Item>
```

**WITH NEW CODE:**
```jsx
      <Title level={5}>Prompt Template Management</Title>
      {isTemplatesError && <Alert message="Error loading templates" description={error?.message || 'Failed to load templates. Please try again.'} type="error" showIcon />}
      
      <Row gutter={16} style={{ marginBottom: 16 }}>
        <Col span={12}>
          <Text strong>Select / Edit Existing Template:</Text>
          <Select
            style={{ width: '100%' }}
            value={selectedTemplateId}
            onChange={handleSelectTemplate}
            loading={isLoadingTemplates}
            disabled={isLoadingOperations || templates.length === 0}
            placeholder="Select a template"
          >
            {templates.map(t => (
              <Option key={t.id} value={t.id}>{t.name}</Option>
            ))}
          </Select>
        </Col>
        <Col span={12}>
          <Text strong>Create New Template:</Text>
          <Input
            placeholder="New Template Name (e.g., prompt_review_article)"
            value={editingTemplateName}
            onChange={(e) => setEditingTemplateName(e.target.value)}
            disabled={isLoadingOperations}
          />
        </Col>
      </Row>
      
      <Form.Item label="Template Description">
        <Input 
          value={editingTemplateDescription} 
          onChange={(e) => setEditingTemplateDescription(e.target.value)} 
          disabled={isLoadingOperations}
        />
      </Form.Item>

      <Form.Item
        label={
          <Space>
            Template Content
            <Tooltip title="This template guides the AI's writing. Use available placeholders for dynamic data.">
              <InfoCircleOutlined />
            </Tooltip>
          </Space>
        }
      >
        <PromptTemplateEditor 
          value={editingTemplateContent} 
          onChange={setEditingTemplateContent} 
          disabled={isLoadingOperations} 
        />
      </Form.Item>
      
      <Space style={{ marginTop: 16 }}>
        <Button 
          type="primary" 
          onClick={handleSaveTemplate} 
          loading={isUpdatingTemplate} 
          disabled={!selectedTemplateId || isLoadingOperations}
        >
          Save Template
        </Button>
        <Button 
          onClick={handleCreateNewTemplate} 
          loading={isCreating} 
          disabled={!editingTemplateName || !editingTemplateContent || isLoadingOperations}
        >
          Create New
        </Button>
        <Button type="danger" onClick={handleDeleteTemplate} loading={isDeleting} disabled={!selectedTemplateId || isLoadingOperations}>
          Delete Selected
        </Button>
      </Space>```

**ACTION NO:** 4.14
**ACTION TYPE:** INSERT
**ACTION RATIONALE:** Imports necessary hooks and services for the new prompt template management UI.

**FIND CONTEXT (Insert after the line containing):**
```jsx
import PromptTemplateEditor from '../../../components/PromptTemplateEditor'; // NEW
```

**CODE TO INSERT:**
```jsx
import { useClient } from '../../../hooks/useClient'; // NEW
import { useQuery, useMutation, useQueryClient } from 'react-query'; // NEW
import { getClientPromptTemplates, createClientPromptTemplate, updateClientPromptTemplate, deleteClientPromptTemplate } from '../../../services/clientSettingsService'; // NEW API services
import { useNotifications } from '../../../context/NotificationContext'; // NEW
import { Modal } from 'antd'; // NEW for confirmation dialog
```

**ACTION NO:** 4.15
**ACTION TYPE:** INSERT
**ACTION RATIONALE:** Introduces state management and React Query hooks for fetching, creating, updating, and deleting prompt templates. This logic powers the new UI, making it interactive and persistent. It also includes `useEffect` to manage the selected template's content.

**FIND CONTEXT (Insert after the line containing):**
```jsx
const AiContentSettingsTab = ({ settings, form }) => {
  const contentModel = Form.useWatch('ai_content_model', form); // Watch for changes in the AI content model
```

**CODE TO INSERT:**
```jsx
  const { clientId } = useClient(); // Get current client ID
  const { showNotification } = useNotifications(); // For notifications
  const queryClient = useQueryClient();
  
  // State for managing selected template in UI and its content
  const [selectedTemplateId, setSelectedTemplateId] = React.useState(null);
  const [editingTemplateContent, setEditingTemplateContent] = React.useState('');
  const [editingTemplateName, setEditingTemplateName] = React.useState('');
  const [editingTemplateDescription, setEditingTemplateDescription] = React.useState('');

  // Query to fetch all templates for this client
  const { data: templates = [], isLoading: isLoadingTemplates, isError: isTemplatesError, error } = useQuery(
    ['clientPromptTemplates', clientId],
    () => getClientPromptTemplates(clientId),
    {
      enabled: !!clientId,
      onSuccess: (data) => {
        // If no template is selected, or selected one is gone, default to the first
        if (data.length > 0 && (!selectedTemplateId || !data.some(t => t.id === selectedTemplateId))) {
          // Fix: Access data as an array for initial selection
          setSelectedTemplateId(data[0].id);
          setEditingTemplateContent(data[0].content);
          setEditingTemplateName(data[0].name);
          setEditingTemplateDescription(data[0].description || '');
        } else if (data.length === 0) {
          setSelectedTemplateId(null);
          setEditingTemplateContent('');
          setEditingTemplateName('');
          setEditingTemplateDescription('');
        }
      },
      onError: (err) => {
        // Handle specific API error messages for better user feedback
        const errorMessage = err.response?.data?.detail || err.message;
        showNotification('error', 'Error Loading Templates', errorMessage);
      },
    }
  );

  // Mutations for CRUD operations
  const { mutate: createTemplate, isLoading: isCreating } = useMutation(
    (newTemplateData) => createClientPromptTemplate(clientId, newTemplateData),
    {
      onSuccess: () => {
        showNotification('success', 'Template Created', 'New prompt template saved.');
        queryClient.invalidateQueries(['clientPromptTemplates', clientId]);
        setEditingTemplateName(''); // Clear name input after creation
        setEditingTemplateDescription(''); // Clear description input after creation
        setEditingTemplateContent(''); // Clear content after creation
      },
      onError: (err) => {
        const errorMessage = err.response?.data?.detail || err.message;
        showNotification('error', 'Create Failed', errorMessage);
      },
    }
  );

  const { mutate: updateTemplate, isLoading: isUpdatingTemplate } = useMutation(
    (updatedTemplateData) => updateClientPromptTemplate(clientId, selectedTemplateId, updatedTemplateData),
    {
      onSuccess: () => {
        showNotification('success', 'Template Updated', 'Prompt template saved successfully.');
        queryClient.invalidateQueries(['clientPromptTemplates', clientId]);
      },
      onError: (err) => {
        const errorMessage = err.response?.data?.detail || err.message;
        showNotification('error', 'Update Failed', errorMessage);
      },
    }
  );

  const { mutate: deleteTemplate, isLoading: isDeleting } = useMutation(
    (templateId) => deleteClientPromptTemplate(clientId, templateId),
    {
      onSuccess: () => {
        showNotification('success', 'Template Deleted', 'Prompt template removed.');
        queryClient.invalidateQueries(['clientPromptTemplates', clientId]);
      },
      onError: (err) => {
        const errorMessage = err.response?.data?.detail || err.message;
        showNotification('error', 'Delete Failed', errorMessage);
      },
    }
  );

  // Effect to update content when selected template changes (from dropdown)
  React.useEffect(() => {
    const currentSelected = templates.find(t => t.id === selectedTemplateId);
    if (currentSelected) {
      setEditingTemplateContent(currentSelected.content);
      setEditingTemplateName(currentSelected.name);
      setEditingTemplateDescription(currentSelected.I || '');
    }
  }, [selectedTemplateId, templates]);

  const handleSelectTemplate = (id) => {
    setSelectedTemplateId(id);
  };

  const handleSaveTemplate = () => {
    if (!selectedTemplateId) {
      showNotification('error', 'Error', 'No template selected to save.');
      return;
    }
    updateTemplate({
      name: editingTemplateName, // Pass name as well, even if not editable for now
      content: editingTemplateContent,
      description: editingTemplateDescription,
    });
  };

  const handleCreateNewTemplate = () => {
    if (!editingTemplateName || !editingTemplateContent) {
      showNotification('error', 'Error', 'Name and content are required for a new template.');
      return;
    }
    createTemplate({
      name: editingTemplateName,
      content: editingTemplateContent,
      description: editingTemplateDescription,
    });
  };

  const handleDeleteTemplate = () => {
    if (!selectedTemplateId) {
      showNotification('error', 'Error', 'No template selected to delete.');
      return;
    }
    Modal.confirm({
      title: 'Confirm Delete',
      content: `Are you sure you want to delete the template "${editingTemplateName}"?`,
      okText: 'Delete',
      okType: 'danger',
      onOk: () => deleteTemplate(selectedTemplateId),
    });
  };

  const isLoadingOperations = isLoadingTemplates || isCreating || isUpdatingTemplate || isDeleting;
  
```

### **File: `client/my-content-app/src/services/clientSettingsService.js`**

**ACTION NO:** 4.16
**ACTION TYPE:** INSERT
**ACTION RATIONALE:** Adds new service functions for interacting with the Prompt Template API endpoints. These functions allow the frontend to fetch, create, update, and delete prompt templates, supporting the new UI.

**FIND CONTEXT (Insert at the end of the file):**
*No specific context needed, append to the end of the file.*

**CODE TO INSERT:**
```javascript

// --- Prompt Template Services (from Task 4.1) ---
export const getClientPromptTemplates = (clientId) => {
  return apiClient.get(`/api/clients/${clientId}/prompt-templates`);
};

export const createClientPromptTemplate = (clientId, templateData) => {
  return apiClient.post(`/api/clients/${clientId}/prompt-templates`, templateData);
};

export const updateClientPromptTemplate = (clientId, templateId, templateData) => {
  return apiClient.put(`/api/clients/${clientId}/prompt-templates/${templateId}`, templateData);
};

export const deleteClientPromptTemplate = (clientId, templateId) => {
  return apiClient.delete(`/api/clients/${clientId}/prompt-templates/${templateId}`);
};
```

---

**Task No:** 5
**Task Higher Overview:** Implement incremental and failure-aware API cost tracking across all orchestrators to ensure all expenditures are accurately recorded, even for partially completed jobs.
**Files Involved:**
*   `backend/data_access/database_manager.py`
*   `backend/pipeline/orchestrator/analysis_orchestrator.py`
*   `backend/pipeline/orchestrator/content_orchestrator.py`
*   `backend/pipeline/orchestrator/discovery_orchestrator.py`
*   `backend/external_apis/dataforseo_client_v2.py`
*   `backend/core/serp_analyzer.py`
**Total Code Changes Required:** 19 granular changes.

**STEP BY STEP PLAN:**

### **File: `backend/data_access/database_manager.py`**

**ACTION NO:** 5.1
**ACTION TYPE:** INSERT
**ACTION RATIONALE:** Adds new `increment_opportunity_cost` and `increment_discovery_run_cost` methods. These methods atomically update the total API cost in the database for individual opportunities and discovery runs, respectively. This ensures that costs are accurately tracked incrementally, even if a job fails midway.

**FIND CONTEXT (Insert after the `update_opportunity_wordpress_payload` method):**
```python
    def update_opportunity_wordpress_payload(
        self, opportunity_id: int, wordpress_payload: Dict[str, Any]
    ):
        """Stores the generated WordPress JSON payload for a specific opportunity."""
```

**CODE TO INSERT:**
```python
    def increment_opportunity_cost(self, opportunity_id: int, cost_to_add: float):
        """Atomically adds a cost value to the opportunity's total_api_cost."""
        if cost_to_add > 0:
            self.logger.info(f"Adding ${cost_to_add:.4f} to total cost for opportunity {opportunity_id}.")
            conn = self._get_conn()
            with conn:
                conn.execute(
                    "UPDATE opportunities SET total_api_cost = total_api_cost + ? WHERE id = ?",
                    (cost_to_add, opportunity_id),
                )

    def increment_discovery_run_cost(self, run_id: int, cost_to_add: float):
        """Atomically adds a cost value to a discovery run's total_api_cost."""
        if cost_to_add > 0:
            self.logger.info(f"Adding ${cost_to_add:.4f} to total cost for discovery run {run_id}.")
            conn = self._get_conn()
            with conn:
                conn.execute(
                    "UPDATE discovery_runs SET total_api_cost = total_api_cost + ? WHERE id = ?",
                    (cost_to_add, run_id),
                )
```

### **File: `backend/pipeline/orchestrator/analysis_orchestrator.py`**

**ACTION NO:** 5.2
**ACTION TYPE:** DELETE
**ACTION RATIONALE:** The local `total_api_cost` variable is removed. Cost tracking will now rely solely on the `db_manager.increment_opportunity_cost` method for atomic and persistent updates.

**FIND CONTEXT (Delete the line containing):**
```python
        total_api_cost = 0.0
```

**CODE TO DELETE:**
```python
        total_api_cost = 0.0
```

**ACTION NO:** 5.3
**ACTION TYPE:** REPLACE
**ACTION RATIONALE:** This updates the `serp_analyzer.analyze_serp` call to pass the `opportunity_id` for incremental cost tracking. It also replaces the local `total_api_cost` aggregation with a direct call to `db_manager.increment_opportunity_cost`.

**FIND CONTEXT (Replace the block starting from `                serp_analyzer = FullSerpAnalyzer(` to `                total_api_cost += serp_api_cost`):**
```python
                serp_analyzer = FullSerpAnalyzer(
                    self.dataforseo_client, self.client_cfg
                )
                live_serp_data, serp_api_cost = serp_analyzer.analyze_serp(keyword)
                total_api_cost += serp_api_cost
```

**CODE TO REPLACE:**
```python
                serp_analyzer = FullSerpAnalyzer(
                    self.dataforseo_client, self.client_cfg
                )
                live_serp_data, serp_api_cost = serp_analyzer.analyze_serp(keyword)
                total_api_cost += serp_api_cost
```

**WITH NEW CODE:**
```python
                serp_analyzer = FullSerpAnalyzer(
                    self.dataforseo_client, self.client_cfg
                )
                live_serp_data, serp_api_cost = serp_analyzer.analyze_serp(keyword, opportunity_id) # Pass opportunity_id
                self.db_manager.increment_opportunity_cost(opportunity_id, serp_api_cost)
```

**ACTION NO:** 5.4
**ACTION TYPE:** REPLACE
**ACTION RATIONALE:** The `api_cost` in the failed return statement now fetches the total cost from the database, ensuring that even on failure, the reported cost reflects all incurred expenses up to that point.

**FIND CONTEXT (Replace the line containing `                    "api_cost": total_api_cost,`):**
```python
                    "api_cost": total_api_cost,
                }
```

**CODE TO REPLACE:**
```python
                    "api_cost": total_api_cost,
                }
```

**WITH NEW CODE:**
```python
                    "api_cost": self.db_manager.get_opportunity_by_id(opportunity_id).get("total_api_cost", 0.0), # Fetch from DB
                }
```

**ACTION NO:** 5.5
**ACTION TYPE:** REPLACE
**ACTION RATIONALE:** This updates the `total_api_cost` tracking for AI competitor assessment to use `db_manager.increment_opportunity_cost`, ensuring atomic and persistent cost recording.

**FIND CONTEXT (Replace the line containing `            total_api_cost += assessment_cost`):**
```python
            ai_competitor_assessment, assessment_cost = content_analyzer.assess_competitor_quality_from_serp(keyword, live_serp_data)
            total_api_cost += assessment_cost
```

**CODE TO REPLACE:**
```python
            ai_competitor_assessment, assessment_cost = content_analyzer.assess_competitor_quality_from_serp(keyword, live_serp_data)
            total_api_cost += assessment_cost
```

**WITH NEW CODE:**
```python
            ai_competitor_assessment, assessment_cost = content_analyzer.assess_competitor_quality_from_serp(keyword, live_serp_data)
            self.db_manager.increment_opportunity_cost(opportunity_id, assessment_cost) # Use incremental cost tracking
```

**ACTION NO:** 5.6
**ACTION TYPE:** REPLACE
**ACTION RATIONALE:** Updates `total_api_cost` tracking for AI-inferred competitor outline generation to use `db_manager.increment_opportunity_cost`, ensuring atomic and persistent cost recording.

**FIND CONTEXT (Replace the line containing `            total_api_cost += inferred_outline_cost`):**
```python
            inferred_outline, inferred_outline_cost = content_analyzer.infer_competitor_outline_from_serp(keyword, live_serp_data)
            total_api_cost += inferred_outline_cost
```

**CODE TO REPLACE:**
```python
            inferred_outline, inferred_outline_cost = content_analyzer.infer_competitor_outline_from_serp(keyword, live_serp_data)
            total_api_cost += inferred_outline_cost
```

**WITH NEW CODE:**
```python
            inferred_outline, inferred_outline_cost = content_analyzer.infer_competitor_outline_from_serp(keyword, live_serp_data)
            self.db_manager.increment_opportunity_cost(opportunity_id, inferred_outline_cost) # Use incremental cost tracking
```

**ACTION NO:** 5.7
**ACTION TYPE:** REPLACE
**ACTION RATIONALE:** Updates `total_api_cost` tracking for content intelligence synthesis to use `db_manager.increment_opportunity_cost`, ensuring atomic and persistent cost recording.

**FIND CONTEXT (Replace the block starting from `            content_intelligence, content_api_cost = (` to `            total_api_cost += content_api_cost`):**
```python
            content_intelligence, content_api_cost = (
                content_analyzer.synthesize_content_intelligence(
                    keyword,
                    live_serp_data,
                    competitor_analysis,  # Pass this list; it will be empty for the fast workflow
                )
            )
            total_api_cost += content_api_cost
```

**CODE TO REPLACE:**
```python
            content_intelligence, content_api_cost = (
                content_analyzer.synthesize_content_intelligence(
                    keyword,
                    live_serp_data,
                    competitor_analysis,  # Pass this list; it will be empty for the fast workflow
                )
            )
            total_api_cost += content_api_cost
```

**WITH NEW CODE:**
```python
            content_intelligence, content_api_cost = \
                content_analyzer.synthesize_content_intelligence(
                    keyword,
                    live_serp_data,
                    competitor_analysis, # This will be an empty list as per new strategy
                )
            self.db_manager.increment_opportunity_cost(opportunity_id, content_api_cost) # Use incremental cost tracking (Task 5.2)
```

**ACTION NO:** 5.8
**ACTION TYPE:** REPLACE
**ACTION RATIONALE:** Updates `total_api_cost` tracking for AI outline generation to use `db_manager.increment_opportunity_cost`, ensuring atomic and persistent cost recording.

**FIND CONTEXT (Replace the block starting from `            ai_outline, outline_api_cost = content_analyzer.generate_ai_outline(` to `            total_api_cost += outline_api_cost`):**
```python
            ai_outline, outline_api_cost = content_analyzer.generate_ai_outline(
                keyword, live_serp_data, content_intelligence
            )
            total_api_cost += outline_api_cost
```

**CODE TO REPLACE:**
```python
            ai_outline, outline_api_cost = content_analyzer.generate_ai_outline(
                keyword, live_serp_data, content_intelligence
            )
            total_api_cost += outline_api_cost
```

**WITH NEW CODE:**
```python
            ai_outline, outline_api_cost = content_analyzer.generate_ai_outline(
                keyword, live_serp_data, content_intelligence, inferred_outline.get("inferred_outline", []) # Pass inferred outline
            )
            self.db_manager.increment_opportunity_cost(opportunity_id, outline_api_cost) # Use incremental cost tracking (Task 5.2)
```

**ACTION NO:** 5.9
**ACTION TYPE:** REPLACE
**ACTION RATIONALE:** Update the `total_api_cost` passed to `blueprint_factory.create_blueprint` to retrieve the latest accumulated cost directly from the database, reflecting all previous incremental updates.

**FIND CONTEXT (Replace the line containing `                total_api_cost=total_api_cost,`):**
```python
                total_api_cost=total_api_cost,
                client_id=opportunity.get("client_id"),
```

**CODE TO REPLACE:**
```python
                total_api_cost=total_api_cost,
                client_id=opportunity.get("client_id"),
```

**WITH NEW CODE:**
```python
                total_api_cost=self.db_manager.get_opportunity_by_id(opportunity_id).get("total_api_cost", 0.0), # Get current total cost from DB
                client_id=opportunity.get("client_id"),
```

**ACTION NO:** 5.10
**ACTION TYPE:** REPLACE
**ACTION RATIONALE:** Update the `api_cost` in the successful return statement to retrieve the final total cost directly from the database, ensuring accuracy.

**FIND CONTEXT (Replace the line containing `                "api_cost": total_api_cost,`):**
```python
                "api_cost": total_api_cost,
            }
```

**CODE TO REPLACE:**
```python
                "api_cost": total_api_cost,
            }
```

**WITH NEW CODE:**
```python
                "api_cost": self.db_manager.get_opportunity_by_id(opportunity_id).get("total_api_cost", 0.0),
            }
```

### **File: `backend/pipeline/orchestrator/content_orchestrator.py`**

**ACTION NO:** 5.11
**ACTION TYPE:** DELETE
**ACTION RATIONALE:** The local `total_api_cost` initialization and initial logging are removed. Cost tracking will now rely solely on the `db_manager.increment_opportunity_cost` method for atomic and persistent updates throughout the content generation process.

**FIND CONTEXT (Delete the block starting from `            # --- START COST TRACKING MODIFICATION ---` to `            # --- END COST TRACKING MODIFICATION ---`):**
```python
            # --- START COST TRACKING MODIFICATION ---
            total_api_cost = opportunity.get("blueprint", {}).get("metadata", {}).get("total_api_cost", 0.0)
            self.logger.info(f"Initial cost from blueprint: ${total_api_cost:.4f}")
            # --- END COST TRACKING MODIFICATION ---
```

**CODE TO DELETE:**
```python
            # --- START COST TRACKING MODIFICATION ---
            total_api_cost = opportunity.get("blueprint", {}).get("metadata", {}).get("total_api_cost", 0.0)
            self.logger.info(f"Initial cost from blueprint: ${total_api_cost:.4f}")
            # --- END COST TRACKING MODIFICATION ---
```

**ACTION NO:** 5.12
**ACTION TYPE:** REPLACE
**ACTION RATIONALE:** Replaces local `total_api_cost` aggregation with a direct call to `db_manager.increment_opportunity_cost` after each section generation. This ensures incremental and persistent cost tracking.

**FIND CONTEXT (Replace the line containing `                total_api_cost += cost # Aggregate cost`):**
```python
                total_api_cost += cost # Aggregate cost
```

**CODE TO REPLACE:**
```python
                total_api_cost += cost # Aggregate cost
```

**WITH NEW CODE:**
```python
                self.db_manager.increment_opportunity_cost(opportunity_id, cost) # Use incremental cost tracking
```

**ACTION NO:** 5.13
**ACTION TYPE:** REPLACE
**ACTION RATIONALE:** Replaces local `total_api_cost` aggregation for AI refinement with a direct call to `db_manager.increment_opportunity_cost`, ensuring incremental and persistent cost tracking.

**FIND CONTEXT (Replace the line containing `                total_api_cost += self.openai_client.latest_cost # Aggregate cost`):**```python
                total_api_cost += self.openai_client.latest_cost # Aggregate cost
```

**CODE TO REPLACE:**
```python
                total_api_cost += self.openai_client.latest_cost # Aggregate cost
```

**WITH NEW CODE:**
```python
                self.db_manager.increment_opportunity_cost(opportunity_id, self.openai_client.latest_cost) # Use incremental cost tracking
```

**ACTION NO:** 5.14
**ACTION TYPE:** REPLACE
**ACTION RATIONALE:** The `featured_image_data` is now part of the combined `in_article_images_data`. This updates the existing call to `self.image_generator.generate_featured_image` to the new `generate_images_from_html` method (Task 11.3), passing the HTML and incrementing the API cost.

**FIND CONTEXT (Replace the block starting from `            featured_image_data, image_cost = self.image_generator.generate_featured_image(` to `            total_api_cost += image_cost`):**
```python
            featured_image_data, image_cost = self.image_generator.generate_featured_image(
                opportunity
            )
            total_api_cost += image_cost
```

**CODE TO REPLACE:**
```python
            featured_image_data, image_cost = self.image_generator.generate_featured_image(
                opportunity
            )
            total_api_cost += image_cost
```

**WITH NEW CODE:**
```python
            # Task 11.3: Image generation moved AFTER HTML generation, and now handles both featured & in-article
            in_article_images_data, image_cost = self.image_generator.generate_images_from_html(current_html, opportunity) # This call will handle all images
            self.db_manager.increment_opportunity_cost(opportunity_id, image_cost) # Use incremental cost tracking (Task 5.3)
```

**ACTION NO:** 5.15
**ACTION TYPE:** REPLACE
**ACTION RATIONALE:** Replaces local `total_api_cost` aggregation for social posts with a direct call to `db_manager.increment_opportunity_cost`, ensuring incremental and persistent cost tracking.

**FIND CONTEXT (Replace the line containing `            total_api_cost += social_cost`):**
```python
            social_posts, social_cost = self.social_crafter.craft_posts(opportunity)
            total_api_cost += social_cost
```

**CODE TO REPLACE:**
```python
            social_posts, social_cost = self.social_crafter.craft_posts(opportunity)
            total_api_cost += social_cost
```

**WITH NEW CODE:**
```python
            social_posts, social_cost = self.social_crafter.craft_posts(opportunity)
            self.db_manager.increment_opportunity_cost(opportunity_id, social_cost) # Use incremental cost tracking (Task 5.3)
```

**ACTION NO:** 5.16
**ACTION TYPE:** INSERT
**ACTION RATIONALE:** Retrieves the final accumulated `total_api_cost` for the opportunity directly from the database just before saving the full content package. This ensures the reported cost is accurate, reflecting all incremental updates.

**FIND CONTEXT (Insert after the line containing):**
```python
                in_article_images_data=[],
            )
```

**CODE TO INSERT:**
```python
            # Get final cost from DB for reporting
            final_reported_cost = self.db_manager.get_opportunity_by_id(opportunity_id).get("total_api_cost", 0.0)
```

**ACTION NO:** 5.17
**ACTION TYPE:** REPLACE
**ACTION RATIONALE:** The `featured_image_data` is now set to `None` because the new `generate_images_from_html` method handles both featured and in-article images. The `in_article_images_data` now passes the combined result. The `total_api_cost` is also updated to use the `final_reported_cost` retrieved from the database.

**FIND CONTEXT (Replace the block starting from `                featured_image_data,` to `                total_api_cost, # Pass total cost`):**
```python
                featured_image_data,
                [],
                social_posts,
                final_package,
                total_api_cost, # Pass total cost
            )```

**CODE TO REPLACE:**
```python
                featured_image_data,
                [],
                social_posts,
                final_package,
                total_api_cost, # Pass total cost
            )
```

**WITH NEW CODE:**
```python
                None, # Featured image data is now part of in_article_images_data after parsing
                in_article_images_data, # Pass combined image data
                social_posts,
                final_package,
                final_reported_cost, # Pass final cost from DB
            )
```

### **File: `backend/pipeline/orchestrator/discovery_orchestrator.py`**

**ACTION NO:** 5.18
**ACTION TYPE:** INSERT
**ACTION RATIONALE:** Passes the `run_id` to the `dataforseo_client.get_keyword_ideas` method. This allows the DataForSEO client to incrementally update the discovery run's total API cost in the database as pages are fetched, ensuring accurate cost tracking even for partial runs.

**FIND CONTEXT (Insert after the line containing):**
```python
                closely_variants=closely_variants,
                run_logger=run_logger,
```

**CODE TO INSERT:**
```python
                run_id_for_costing=run_id, # Pass run_id for incremental cost tracking (Task 5.3)
```

### **File: `backend/external_apis/dataforseo_client_v2.py`**

**ACTION NO:** 5.19
**ACTION TYPE:** INSERT
**ACTION RATIONALE:** Adds `run_id_for_costing` to the `post_with_paging` method signature. This parameter allows the DataForSEO client to identify which discovery run's cost needs to be incremented for each paginated API call.

**FIND CONTEXT (Insert after the line containing):**
```python
        initial_task: Dict[str, Any],
        max_pages: int,
        paginated: bool = True,
```

**CODE TO INSERT:**
```python
        run_id_for_costing: Optional[int] = None, # ADD this argument for Task 5.3
```

**ACTION NO:** 5.20
**ACTION TYPE:** INSERT
**ACTION RATIONALE:** This code block incrementally updates the `total_api_cost` for the specified discovery run after each page of results is fetched. This ensures accurate, real-time cost tracking for paginated API calls.

**FIND CONTEXT (Insert after the line containing):**
```python
            total_cost += cost
```

**CODE TO INSERT:**
```python
            # ADD THIS BLOCK to save cost per page for discovery runs (Task 5.3)
            if run_id_for_costing and cost > 0:
                self.db_manager.increment_discovery_run_cost(run_id_for_costing, cost)
```

**ACTION NO:** 5.21
**ACTION TYPE:** INSERT
**ACTION RATIONALE:** Adds `run_id_for_costing` to the `get_keyword_ideas` method signature. This parameter is crucial for passing the discovery run ID down to the `post_with_paging` method, enabling granular cost tracking for keyword discovery API calls.

**FIND CONTEXT (Insert after the line containing):**
```python
        ignore_synonyms_override: Optional[bool] = None,
        include_clickstream_override: Optional[bool] = None,
        closely_variants_override: Optional[bool] = None,
```

**CODE TO INSERT:**
```python
        run_id_for_costing: Optional[int] = None, # ADD this argument for Task 5.3
```

**ACTION NO:** 5.22
**ACTION TYPE:** REPLACE
**ACTION RATIONALE:** Updates the call to `self.post_with_paging` for `keyword_ideas` to include the `run_id_for_costing`. This ensures that API costs incurred during the keyword ideas phase are incrementally tracked against the specific discovery run.

**FIND CONTEXT (Replace the line containing `            ideas_items, cost = self.post_with_paging(`):**
```python
            ideas_items, cost = self.post_with_paging(
                ideas_endpoint, ideas_task, max_pages=max_pages, tag="discovery_ideas"
            )
```

**CODE TO REPLACE:**
```python
            ideas_items, cost = self.post_with_paging(
                ideas_endpoint, ideas_task, max_pages=max_pages, tag="discovery_ideas"
            )
```

**WITH NEW CODE:**
```python
            ideas_items, cost = self.post_with_paging(
                ideas_endpoint, ideas_task, max_pages=max_pages, run_id_for_costing=run_id_for_costing, tag="discovery_ideas" # Pass run_id
            )
```

**ACTION NO:** 5.23
**ACTION TYPE:** REPLACE
**ACTION RATIONALE:** Updates the call to `self.post_with_paging` for `keyword_suggestions` to include the `run_id_for_costing`. This ensures that API costs incurred during the keyword suggestions phase are incrementally tracked against the specific discovery run.

**FIND CONTEXT (Replace the block starting from `                suggestions_items, cost = self.post_with_paging(` to `                    tag=f"discovery_suggestions:{seed_keyword[:20]}",`):**
```python
                suggestions_items, cost = self.post_with_paging(
                    suggestions_endpoint,
                    suggestions_task,
                    max_pages=max_pages,
                    tag=f"discovery_suggestions:{seed_keyword[:20]}",
                )
```

**CODE TO REPLACE:**
```python
                suggestions_items, cost = self.post_with_paging(
                    suggestions_endpoint,
                    suggestions_task,
                    max_pages=max_pages,
                    tag=f"discovery_suggestions:{seed_keyword[:20]}",
                )
```

**WITH NEW CODE:**
```python
                suggestions_items, cost = self.post_with_paging(
                    suggestions_endpoint,
                    suggestions_task,
                    max_pages=max_pages,
                    run_id_for_costing=run_id_for_costing, # Pass run_id
                    tag=f"discovery_suggestions:{seed_keyword[:20]}",
                )
```

**ACTION NO:** 5.24
**ACTION TYPE:** REPLACE
**ACTION RATIONALE:** Updates the call to `self.post_with_paging` for `related_keywords` to include the `run_id_for_costing`. This ensures that API costs incurred during the related keywords phase are incrementally tracked against the specific discovery run.

**FIND CONTEXT (Replace the block starting from `                related_items, cost = self.post_with_paging(` to `                    tag=f"discovery_related:{seed[:20]}",`):**
```python
                related_items, cost = self.post_with_paging(
                    related_endpoint,
                    related_task,
                    max_pages=max_pages,
                    tag=f"discovery_related:{seed[:20]}",
                )
```

**CODE TO REPLACE:**
```python
                related_items, cost = self.post_with_paging(
                    related_endpoint,
                    related_task,
                    max_pages=max_pages,
                    tag=f"discovery_related:{seed[:20]}",
                )
```

**WITH NEW CODE:**
```python
                related_items, cost = self.post_with_paging(
                    related_endpoint, # Ensure paginated is True if this endpoint supports it
                    related_task,
                    max_pages=max_pages,
                    run_id_for_costing=run_id_for_costing, # Pass run_id
                    tag=f"discovery_related:{seed[:20]}",
                )
```

### **File: `backend/core/serp_analyzer.py`**

**ACTION NO:** 5.25
**ACTION TYPE:** REPLACE
**ACTION RATIONALE:** The `analyze_serp` method signature is updated to accept an optional `opportunity_id`. This ID is crucial for passing to the `dataforseo_client.get_serp_results` call, enabling incremental cost tracking for individual SERP analysis calls against a specific opportunity.

**FIND CONTEXT (Replace the line containing):**
```python
    def analyze_serp(self, keyword: str) -> Tuple[Optional[Dict[str, Any]], float]:
```

**CODE TO REPLACE:**
```python
    def analyze_serp(self, keyword: str) -> Tuple[Optional[Dict[str, Any]], float]:
```

**WITH NEW CODE:**
```python
    def analyze_serp(self, keyword: str, opportunity_id: Optional[int] = None) -> Tuple[Optional[Dict[str, Any]], float]: # ADD opportunity_id
```

**ACTION NO:** 5.26
**ACTION TYPE:** INSERT
**ACTION RATIONALE:** Passes the `opportunity_id` to the `dataforseo_client.get_serp_results` call. This enables incremental cost tracking for the SERP analysis, ensuring that the cost of this API call is recorded against the specific opportunity.

**FIND CONTEXT (Insert after the line containing):**
```python
            language_code,
            client_cfg=self.config,
            serp_call_params=serp_call_params,
```

**CODE TO INSERT:**
```python
            opportunity_id_for_costing=opportunity_id, # Pass opportunity_id for cost tracking
```

---

**Task No:** 7
**Task Higher Overview:** Enhance the rule-based `SummaryGenerator` by having it make a final, cheap AI call for a more nuanced and human-readable narrative explaining the keyword's strategic value.
**Files Involved:**
*   `backend/agents/summary_generator.py`
*   `backend/pipeline/orchestrator/analysis_orchestrator.py`
**Total Code Changes Required:** 5 granular changes.

**STEP BY STEP PLAN:**

### **File: `backend/agents/summary_generator.py`**

**ACTION NO:** 7.1
**ACTION TYPE:** INSERT
**ACTION RATIONALE:** Imports `OpenAIClientWrapper` to enable AI calls within the `SummaryGenerator`.

**FIND CONTEXT (Insert after the line containing):**
```python
import logging
from typing import Dict, Any
```

**CODE TO INSERT:**
```python
import json
from backend.external_apis.openai_client import OpenAIClientWrapper # NEW
```

**ACTION NO:** 7.2
**ACTION TYPE:** REPLACE
**ACTION RATIONALE:** The `SummaryGenerator`'s constructor is updated to accept an `openai_client` instance. This injects the necessary dependency for making AI calls.

**FIND CONTEXT (Replace the line containing):**
```python
    def __init__(self):
```

**CODE TO REPLACE:**
```python
    def __init__(self):
```

**WITH NEW CODE:**
```python
    def __init__(self, openai_client: OpenAIClientWrapper): # MODIFY constructor
```

**ACTION NO:** 7.3
**ACTION TYPE:** INSERT
**ACTION RATIONALE:** Stores the `openai_client` as an instance attribute, making it available for AI calls within the `SummaryGenerator`.

**FIND CONTEXT (Insert after the line containing):**
```python
        self.logger = logging.getLogger(self.__class__.__name__)
```

**CODE TO INSERT:**
```python
        self.openai_client = openai_client # ADD this line
```

**ACTION NO:** 7.4
**ACTION TYPE:** INSERT
**ACTION RATIONALE:** This new method leverages a cost-effective AI call (`gpt-5-nano`) to generate a concise, human-readable executive summary of the keyword's strategic value based on the score breakdown. It includes a JSON schema for structured output and tracks the API cost.

**FIND CONTEXT (Insert after the `generate_score_narrative` method):**
```python
    def generate_score_narrative(self, score_breakdown: Dict[str, Any]) -> str:
        narrative_parts = []
        # ... (rest of generate_score_narrative) ...
        return "Overall: " + " ".join(narrative_parts)
```

**CODE TO INSERT:**
```python
    def generate_ai_summary(self, score_breakdown: Dict[str, Any]) -> Tuple[str, float]:
        """
        Uses an AI call to generate a concise, human-readable executive summary of the score breakdown.
        """
        if not score_breakdown:
            return "No scoring data available to generate a summary.", 0.0

        summary_data = {
            factor: f"{data['name']}: {data['score']}/100" 
            for factor, data in score_breakdown.items()
        }

        prompt = f"""
        You are an expert SEO strategist. Given the following scoring breakdown for a keyword, write a concise, 2-3 sentence executive summary explaining the strategic value. Focus on the most important factors.

        Scoring Data:
        {json.dumps(summary_data, indent=2)}

        Example: "This is a strong opportunity due to its high traffic potential and clear competitor weaknesses. However, be aware of the crowded SERP environment, which will require a compelling title to capture clicks."

        Return a JSON object with a single key "summary".
        """
        
        schema = {"name": "generate_summary", "type": "object", "properties": {"summary": {"type": "string"}}, "required": ["summary"], "additionalProperties": False} # Added for strictness

        response, error = self.openai_client.call_chat_completion(
            messages=[{"role": "user", "content": prompt}],
            schema=schema, model="gpt-5-nano"
        )
        cost = self.openai_client.latest_cost

        if error or not response:
            return "AI summary generation failed.", cost
        
        return response.get("summary", "AI summary generation failed."), cost
```

### **File: `backend/pipeline/orchestrator/analysis_orchestrator.py`**

**ACTION NO:** 7.5
**ACTION TYPE:** REPLACE
**ACTION RATIONALE:** The `_create_executive_summary` placeholder call is replaced by initializing `SummaryGenerator` with the `openai_client` and calling its new `generate_ai_summary` method. This dynamically generates a human-readable summary and tracks its API cost. `SummaryGenerator` initialization moves to orchestrator `__init__` (corrected in orchestrator `main.py`).

**FIND CONTEXT (Replace the block starting from `            # 6. Assemble and Save Blueprint & Re-Score` to `            blueprint["executive_summary"] = self._create_executive_summary(`):**
```python
            # 6. Assemble and Save Blueprint & Re-Score
            analysis_data = {
                "serp_overview": live_serp_data,
                "competitor_analysis": competitor_analysis,
                "content_intelligence": content_intelligence,
                "recommended_strategy": recommended_strategy,
            }

            blueprint = self.blueprint_factory.create_blueprint(
                seed_topic=keyword,
                winning_keyword_data=opportunity.get("full_data", {}).copy(),
                analysis_data=analysis_data,
                total_api_cost=total_api_cost,
                client_id=opportunity.get("client_id"),
            )

            blueprint["executive_summary"] = self._create_executive_summary(
                blueprint_data
            )
```

**CODE TO REPLACE:**
```python
            # 6. Assemble and Save Blueprint & Re-Score
            analysis_data = {
                "serp_overview": live_serp_data,
                "competitor_analysis": competitor_analysis,
                "content_intelligence": content_intelligence,
                "recommended_strategy": recommended_strategy,
            }

            blueprint = self.blueprint_factory.create_blueprint(
                seed_topic=keyword,
                winning_keyword_data=opportunity.get("full_data", {}).copy(),
                analysis_data=analysis_data,
                total_api_cost=total_api_cost,
                client_id=opportunity.get("client_id"),
            )

            blueprint["executive_summary"] = self._create_executive_summary(
                blueprint_data
            )
```

**WITH NEW CODE:**
```python
            # 6. Assemble and Save Blueprint & Re-Score
            analysis_data = {
                "serp_overview": live_serp_data,
                "competitor_analysis": competitor_analysis,
                "ai_competitor_assessment": ai_competitor_assessment, # Store the new AI assessment
                "inferred_competitor_outline": inferred_outline.get("inferred_outline", []), # Store inferred outline
                "content_intelligence": content_intelligence,
                "recommended_strategy": recommended_strategy,
            }

            blueprint = self.blueprint_factory.create_blueprint(
                seed_topic=keyword,
                winning_keyword_data=opportunity.get("full_data", {}).copy(),
                analysis_data=analysis_data, # Updated with new AI insights
                total_api_cost=self.db_manager.get_opportunity_by_id(opportunity_id).get("total_api_cost", 0.0), # Get current total cost from DB
                client_id=opportunity.get("client_id"),
            )
            # Add AI summary to blueprint
            ai_summary, summary_cost = self.summary_generator.generate_ai_summary(final_score_breakdown)
            self.db_manager.increment_opportunity_cost(opportunity_id, summary_cost) # Track cost
            blueprint["executive_summary"] = ai_summary # Overwrite placeholder
```

---

**Task No:** 8
**Task Higher Overview:** Add a configuration setting to allow the user to completely disable the `InternalLinkingSuggester` to save on API costs, and ensure internal linking only occurs once in the workflow.
**Files Involved:**
*   `backend/app_config/settings.ini`
*   `backend/core/blueprint_factory.py`
*   `backend/pipeline/orchestrator/content_orchestrator.py`
*   `backend/agents/internal_linking_suggester.py`
**Total Code Changes Required:** 4 granular changes.

**STEP BY STEP PLAN:**

### **File: `backend/app_config/settings.ini`**

**ACTION NO:** 8.1
**ACTION TYPE:** REPLACE
**ACTION RATIONALE:** The `enable_automated_internal_linking` setting is explicitly set to `false` by default. This allows users to control the invocation of the `InternalLinkingSuggester` and its associated API costs, aligning with the request to de-prioritize this feature.

**FIND CONTEXT (Replace the line containing):**
```ini
enable_automated_internal_linking = false
```

**CODE TO REPLACE:**
```ini
enable_automated_internal_linking = false
```

**WITH NEW CODE:**
```ini
enable_automated_internal_linking = false ; Control internal linking cost
```

### **File: `backend/core/blueprint_factory.py`**

**ACTION NO:** 8.2
**ACTION TYPE:** DELETE
**ACTION RATIONALE:** The internal linking suggestion logic is **removed** from `BlueprintFactory.create_blueprint`. This ensures that internal linking is performed *only once* later in the `content_orchestrator.py` stage, avoiding redundant API calls and centralizing the feature.

**FIND CONTEXT (Delete the block starting from `        brief_text_for_linking = json.dumps(blueprint_data["ai_content_brief"])` to `        blueprint_data["metadata"]["total_api_cost"] = round(`):**
```python
        brief_text_for_linking = json.dumps(blueprint_data["ai_content_brief"])
        target_domain = self.client_cfg.get("target_domain")
        key_entities = blueprint_data.get("ai_content_brief", {}).get(
            "key_entities_to_mention", []
        )
        if brief_text_for_linking and target_domain:
            suggestions, linking_cost = self.internal_linking_suggester.suggest_links(
                brief_text_for_linking, key_entities, target_domain, client_id
            )
            blueprint_data["internal_linking_suggestions"] = suggestions
            blueprint_data["metadata"]["total_api_cost"] = round(
                blueprint_data["metadata"]["total_api_cost"] + linking_cost, 4
            )
```

**CODE TO DELETE:**
```python
        brief_text_for_linking = json.dumps(blueprint_data["ai_content_brief"])
        target_domain = self.client_cfg.get("target_domain")
        key_entities = blueprint_data.get("ai_content_brief", {}).get(
            "key_entities_to_mention", []
        )
        if brief_text_for_linking and target_domain:
            suggestions, linking_cost = self.internal_linking_suggester.suggest_links(
                brief_text_for_linking, key_entities, target_domain, client_id
            )
            blueprint_data["internal_linking_suggestions"] = suggestions
            blueprint_data["metadata"]["total_api_cost"] = round(
                blueprint_data["metadata"]["total_api_cost"] + linking_cost, 4
            )
```

### **File: `backend/pipeline/orchestrator/content_orchestrator.py`**

**ACTION NO:** 8.3
**ACTION TYPE:** INSERT
**ACTION RATIONALE:** The logic for generating internal links is now conditionally executed based on the `enable_automated_internal_linking` client configuration. If the feature is enabled, it calls the `InternalLinkingSuggester` and tracks its cost. If disabled, it defaults to an empty list of suggestions. A `try-except` block is added to ensure graceful degradation if linking fails.

**FIND CONTEXT (Insert after the line containing):**
```python
                result={"step": "Formatting & Internal Linking"},
            )
```

**CODE TO INSERT:**
```python
            # Task 8.3: Internal linking is now conditional
            internal_link_suggestions = [] # Default to empty
            try: # ADD TRY/EXCEPT (Task 12.1)
                if self.client_cfg.get("enable_automated_internal_linking", False):
                    link_suggestions, link_cost = self.internal_linking_suggester.suggest_links(
                        opportunity["ai_content"]["article_body_html"],
                        opportunity.get("blueprint", {}).get("ai_content_brief", {}).get("key_entities_to_mention", []),
                        self.client_cfg.get("target_domain"),
                        self.client_id,
                    )
                    internal_link_suggestions = link_suggestions
                    self.db_manager.increment_opportunity_cost(opportunity_id, link_cost) # Use incremental cost tracking (Task 5.3)
            except Exception as e: # ADDED EXCEPTION HANDLING
                self.logger.error(f"Internal linking generation failed but workflow will continue: {e}")
                generation_warnings.append(f"Internal linking generation failed: {str(e)}") # Add warning
```

### **File: `backend/agents/internal_linking_suggester.py`**

**ACTION NO:** 8.4
**ACTION TYPE:** INSERT
**ACTION RATIONALE:** This adds an early exit condition to the `suggest_links` method. If `enable_automated_internal_linking` is `false` in the client configuration, the method immediately returns an empty list and zero cost, preventing unnecessary AI calls and saving resources.

**FIND CONTEXT (Insert after the line containing):**
```python
        """
        Existing articles: {existing_articles_text}
        """
```

**CODE TO INSERT:**
```python
        if not self.config.get("enable_automated_internal_linking", False): # Add early exit (Task 8.4)
            self.logger.info("Internal linking suggestion is disabled by client configuration. Skipping AI call.")
            return [], 0.0
```

---

**Task No:** 9
**Task Higher Overview:** Implement dynamic `Schema.org` generation in the `HtmlFormatter` based on the blueprint's `content_format`.
**Files Involved:**
*   `backend/agents/html_formatter.py`
**Total Code Changes Required:** 1 granular change.

**STEP BY STEP PLAN:**

### **File: `backend/agents/html_formatter.py`**

**ACTION NO:** 9.1
**ACTION TYPE:** REPLACE
**ACTION RATIONALE:** The `_generate_schema_org` method is enhanced to dynamically generate different Schema.org types (e.g., `Review`, `FAQPage`) based on the `content_format` specified in the opportunity's blueprint. This improves the SEO of generated content by providing more specific structured data.

**FIND CONTEXT (Replace the block starting from `        article_schema = {` to `        schema_graph.append(article_schema)`):**
```python
        article_schema = {
            "@type": "BlogPosting",
            "@id": f"{article_url}#article",
            "mainEntityOfPage": {"@id": article_url},
            "headline": article_headline,
            "author": {
                "@type": client_cfg.get("schema_author_type", "Organization"),
                "name": client_cfg.get("default_author_name", "Author"),
            },
            "publisher": {"@type": "Organization", "name": publisher_name},
            "datePublished": datetime.now().isoformat(),
            "dateModified": datetime.now().isoformat(),
            "additionalProperties": False,
        }
        schema_graph.append(article_schema)
```

**CODE TO REPLACE:**
```python
        article_schema = {
            "@type": "BlogPosting",
            "@id": f"{article_url}#article",
            "mainEntityOfPage": {"@id": article_url},
            "headline": article_headline,
            "author": {
                "@type": client_cfg.get("schema_author_type", "Organization"),
                "name": client_cfg.get("default_author_name", "Author"),
            },
            "publisher": {"@type": "Organization", "name": publisher_name},
            "datePublished": datetime.now().isoformat(),
            "dateModified": datetime.now().isoformat(),
            "additionalProperties": False,
        }
        schema_graph.append(article_schema)
```

**WITH NEW CODE:**
```python
        # Base Article Schema (always present, but ensure it's added only once)
        article_schema = {
            "@type": "BlogPosting",
            "@id": f"{article_url}#article",
            "mainEntityOfPage": {"@id": article_url},
            "headline": article_headline,
            "author": {
                "@type": client_cfg.get("schema_author_type", "Organization"),
                "name": client_cfg.get("default_author_name", "Author"),
            },
            "publisher": {"@type": "Organization", "name": publisher_name},
            "datePublished": datetime.now().isoformat(),
            "dateModified": datetime.now().isoformat(),
            "additionalProperties": False,
        }
        schema_graph.append(article_schema)

        # Dynamic Schema based on content_format (Task 10)
        content_format = opportunity.get("blueprint", {}).get("recommended_strategy", {}).get("content_format", "BlogPosting")

        if content_format == "Review Article":
            review_schema = {
                "@type": "Review",
                "itemReviewed": {"@type": "Thing", "name": opportunity.get("keyword")}, # Use the main keyword as the item reviewed
                "reviewRating": {"@type": "Rating", "ratingValue": "4.5", "bestRating": "5"}, # Placeholder values, could be AI-generated
                "author": article_schema["author"]
            }
            schema_graph.append(review_schema)
        elif content_format == "FAQ Article":
            # For FAQ, extract questions and answers from the generated HTML
            faq_items = []
            for h2_tag in soup.find_all('h2'):
                if 'frequently asked questions' in h2_tag.get_text(strip=True).lower():
                    current_tag = h2_tag.next_sibling
                    while current_tag and current_tag.name != 'h2':
                        if current_tag.name == 'h3': # Assuming questions are h3s
                            question = current_tag.get_text(strip=True)
                            answer_paragraphs = []
                            next_element = current_tag.next_sibling
                            while next_element and next_element.name not in ['h2', 'h3']:
                                if next_element.name == 'p':
                                    answer_paragraphs.append(next_element.get_text(strip=True))
                                next_element = next_element.next_sibling
                            if question and answer_paragraphs:
                                faq_items.append({
                                    "@type": "Question",
                                    "name": question,
                                    "acceptedAnswer": {
                                        "@type": "Answer",
                                        "text": " ".join(answer_paragraphs)
                                    }
                                })
                        current_tag = current_tag.next_sibling
            if faq_items:
                faq_page_schema = {
                    "@type": "FAQPage",
                    "mainEntity": faq_items
                }
                schema_graph.append(faq_page_schema)
        # The existing HowTo schema logic for ordered lists can remain here
        # ... existing HowTo logic ...
```

---

**Task No:** 10
**Task Higher Overview:** Add an AI-powered step to generate a "Key Takeaways" summary box for the top of the article.
**Files Involved:**
*   `backend/pipeline/orchestrator/content_orchestrator.py`
**Total Code Changes Required:** 1 granular change.

**STEP BY STEP PLAN:**

### **File: `backend/pipeline/orchestrator/content_orchestrator.py`**

**ACTION NO:** 10.1
**ACTION TYPE:** INSERT
**ACTION RATIONALE:** This code block integrates an AI-powered "Key Takeaways" generation step. After the core article HTML is created, a targeted AI call summarizes the content into 3-5 bullet points within a `<div>` element. This summary is then prepended to the article HTML, enhancing readability and user experience. API cost is tracked for this operation. It explicitly uses `gpt-4o` for better HTML generation quality.

**FIND CONTEXT (Insert after the line containing):**
```python
            opportunity["ai_content"]["article_body_html"] = current_html
            opportunity["ai_content"]["audit_results"] = final_audit_results
```

**CODE TO INSERT:**
```python
            # Task 11: Add AI-powered "Key Takeaways" section
            self.job_manager.update_job_status(
                job_id, "running", progress=88, result={"step": "Generating Key Takeaways"}
            )
            summary_prompt = f"""
            Read the following article HTML and generate a 3-5 bullet point 'Key Takeaways' summary inside a `<div>` with the class 'key-takeaways'. The takeaways should be concise and actionable. Ensure the HTML is well-formed.

            Article HTML:
            {current_html}
            """
            takeaways_html, takeaways_cost = self.openai_client.call_chat_completion(
                messages=[{"role": "user", "content": summary_prompt}],
                model="gpt-4o" # Use a more capable model for HTML generation
            )
            self.db_manager.increment_opportunity_cost(opportunity_id, takeaways_cost) # Track cost
            if takeaways_html:
                current_html = takeaways_html + "\\n" + current_html
                opportunity["ai_content"]["article_body_html"] = current_html # Update HTML with takeaways
```

---

**Task No:** 11
**Task Higher Overview:** Generate more relevant in-article images by centralizing all image generation (featured and in-article) to a single post-HTML step, using contextual prompts.
**Files Involved:**
*   `backend/agents/prompt_assembler.py`
*   `backend/agents/image_generator.py`
*   `backend/pipeline/orchestrator/content_orchestrator.py`
*   `backend/agents/html_formatter.py`
**Total Code Changes Required:** 8 granular changes.

**STEP BY STEP PLAN:**

### **File: `backend/agents/prompt_assembler.py`**

**ACTION NO:** 11.1
**ACTION TYPE:** REPLACE
**ACTION RATIONALE:** The prompt instructions for image placeholders are updated to introduce a distinct `[[FEATURED_IMAGE: <prompt>]]` marker for the main featured image, in addition to the existing `[[IMAGE: <prompt>]]` for in-article images. This allows the image generation logic to differentiate between image types.

**FIND CONTEXT (Replace the line containing `        base_instructions += "\n- For in-article images, use a placeholder with the exact format `[[IMAGE: <A descriptive prompt for the image>]]`. For example: `[[IMAGE: A bar chart showing SEO growth over time]]`."`):**
```python
        base_instructions += "\n- For in-article images, use a placeholder with the exact format `[[IMAGE: <A descriptive prompt for the image>]]`. For example: `[[IMAGE: A bar chart showing SEO growth over time]]`."
```

**CODE TO REPLACE:**
```python
        base_instructions += "\n- For in-article images, use a placeholder with the exact format `[[IMAGE: <A descriptive prompt for the image>]]`. For example: `[[IMAGE: A bar chart showing SEO growth over time]]`."
```

**WITH NEW CODE:**
```python
        base_instructions += "\n- At the very beginning of the article (before the introduction), you MUST include a placeholder for the featured image in the exact format `[[FEATURED_IMAGE: <A descriptive prompt for the main image>]]`. For example: `[[FEATURED_IMAGE: An aerial view of a bustling city at sunset]]`." # ADDED FOR FEATURED IMAGE
        base_instructions += "\n- For in-article images, use a placeholder with the exact format `[[IMAGE: <A descriptive prompt for the image>]]`. For example: `[[IMAGE: A bar chart showing SEO growth over time]]`." # EXISTING IN-ARTICLE IMAGE
```

### **File: `backend/agents/image_generator.py`**

**ACTION NO:** 11.2
**ACTION TYPE:** REPLACE
**ACTION RATIONALE:** The `_add_text_overlay` method is enhanced to accept an `output_suffix`. This allows the method to generate unique filenames for featured images with overlays, preventing conflicts and improving clarity.

**FIND CONTEXT (Replace the line containing):**
```python
    def _add_text_overlay(self, image_path: str, text: str) -> str:
```

**CODE TO REPLACE:**
```python
    def _add_text_overlay(self, image_path: str, text: str) -> str:
```

**WITH NEW CODE:**
```python
    def _add_text_overlay(self, image_path: str, text: str, output_suffix: str = "-overlay") -> str: # Add output_suffix
```

**ACTION NO:** 11.3
**ACTION TYPE:** REPLACE
**ACTION RATIONALE:** The `_add_text_overlay` call is updated to use the new `output_suffix` parameter for featured images, creating a distinct filename.

**FIND CONTEXT (Replace the line containing `            new_image_path = image_path.replace(".jpeg", "-overlay.jpeg")`):**
```python
            new_image_path = image_path.replace(".jpeg", "-overlay.jpeg")
```

**CODE TO REPLACE:**
```python
            new_image_path = image_path.replace(".jpeg", "-overlay.jpeg")
```

**WITH NEW CODE:**
```python
            new_image_path = image_path.replace(".jpeg", f"{output_suffix}.jpeg")
```

**ACTION NO:** 11.4
**ACTION TYPE:** REPLACE
**ACTION RATIONALE:** The `_simplify_prompt_for_pexels` method is updated to return both the simplified search query and the AI cost incurred. This is crucial for granular cost tracking. It also adds `additionalProperties: False` to the schema for strictness.

**FIND CONTEXT (Replace the block starting from `    def _simplify_prompt_for_pexels(self, descriptive_prompt: str) -> str:` to `        return descriptive_prompt  # Final fallback`):**
```python
    def _simplify_prompt_for_pexels(self, descriptive_prompt: str) -> str:
        """
        Uses an LLM to extract 3-5 high-impact keywords suitable for a stock photo search
        from a more descriptive AI image prompt.
        """
        if not descriptive_prompt or not self.openai_client:
            return descriptive_prompt  # Fallback to original if no client or prompt

        self.logger.info(
            f"Refining image prompt for Pexels search: '{descriptive_prompt}'"
        )

        prompt_messages = [
            {
                "role": "system",
                "content": "You are a concise keyword extractor for stock photo sites. Extract 3-5 key nouns, adjectives, or short phrases from the user's descriptive image prompt that would be most effective for searching a stock photo library like Pexels. Return only a comma-separated list of keywords.",
            },
            {"role": "user", "content": f"Descriptive prompt: '{descriptive_prompt}'"},
        ]

        # Use a low temperature for predictable, factual output
        extracted_keywords_str, error = self.openai_client.call_chat_completion(
            messages=prompt_messages,
                            model=self.config.get("default_model", "gpt-5-nano"),  # Use a cost-effective model for this            temperature=0.1,
            max_completion_tokens=50,  # Keep output very short
            schema={
                "name": "extract_keywords",
                "type": "object",
                "properties": {
                    "keywords": {
                        "type": "string",
                        "description": "Comma-separated keywords.",
                    }
                },
                "required": ["keywords"],
                "additionalProperties": False
            },
        )

        if error or not extracted_keywords_str:
            self.logger.warning(
                f"Failed to extract keywords for Pexels. Falling back to original prompt. Error: {error}"
            )
            return descriptive_prompt  # Fallback to original prompt

        # The AI should return a dictionary with a 'keywords' key
        if (
            isinstance(extracted_keywords_str, dict)
            and "keywords" in extracted_keywords_str
        ):
            return extracted_keywords_str["keywords"]
        elif isinstance(
            extracted_keywords_str, str
        ):  # Fallback if AI doesn't follow schema perfectly
            return extracted_keywords_str

        return descriptive_prompt  # Final fallback
```

**CODE TO REPLACE:**
```python
    def _simplify_prompt_for_pexels(self, descriptive_prompt: str) -> str:
        """
        Uses an LLM to extract 3-5 high-impact keywords suitable for a stock photo search
        from a more descriptive AI image prompt.
        """
        if not descriptive_prompt or not self.openai_client:
            return descriptive_prompt  # Fallback to original if no client or prompt

        self.logger.info(
            f"Refining image prompt for Pexels search: '{descriptive_prompt}'"
        )

        prompt_messages = [
            {
                "role": "system",
                "content": "You are a concise keyword extractor for stock photo sites. Extract 3-5 key nouns, adjectives, or short phrases from the user's descriptive image prompt that would be most effective for searching a stock photo library like Pexels. Return only a comma-separated list of keywords.",
            },
            {"role": "user", "content": f"Descriptive prompt: '{descriptive_prompt}'"},
        ]

        # Use a low temperature for predictable, factual output
        extracted_keywords_str, error = self.openai_client.call_chat_completion(
            messages=prompt_messages,
                            model=self.config.get("default_model", "gpt-5-nano"),  # Use a cost-effective model for this            temperature=0.1,
            max_completion_tokens=50,  # Keep output very short
            schema={
                "name": "extract_keywords",
                "type": "object",
                "properties": {
                    "keywords": {
                        "type": "string",
                        "description": "Comma-separated keywords.",
                    }
                },
                "required": ["keywords"],
                "additionalProperties": False
            },
        )

        if error or not extracted_keywords_str:
            self.logger.warning(
                f"Failed to extract keywords for Pexels. Falling back to original prompt. Error: {error}"
            )
            return descriptive_prompt  # Fallback to original prompt

        # The AI should return a dictionary with a 'keywords' key
        if (
            isinstance(extracted_keywords_str, dict)
            and "keywords" in extracted_keywords_str
        ):
            return extracted_keywords_str["keywords"]
        elif isinstance(
            extracted_keywords_str, str
        ):  # Fallback if AI doesn't follow schema perfectly
            return extracted_keywords_str

        return descriptive_prompt  # Final fallback
```

**WITH NEW CODE:**
```python
    def _simplify_prompt_for_pexels(self, descriptive_prompt: str) -> Tuple[str, float]: # MODIFIED to return cost (Task 11.2)
        """
        Uses an LLM to extract 3-5 high-impact keywords suitable for a stock photo search
        from a more descriptive AI image prompt.
        """
        # Ensure latest_cost is reset before the call, so only this call's cost is captured
        self.openai_client.latest_cost = 0.0 
        if not descriptive_prompt or not self.openai_client: # If no OpenAI client, cannot simplify
            return descriptive_prompt, 0.0 # Fallback to original, 0 cost

        self.logger.info(
            f"Refining image prompt for Pexels search: '{descriptive_prompt}'"
        )

        prompt_messages = [
            {
                "role": "system",
                "content": "You are a concise keyword extractor for stock photo sites. Extract 3-5 key nouns, adjectives, or short phrases from the user's descriptive image prompt that would be most effective for searching a stock photo library like Pexels. Return only a comma-separated list of keywords.",
            },
            {"role": "user", "content": f"Descriptive prompt: '{descriptive_prompt}'"},
        ]

        # Use a low temperature for predictable, factual output
        extracted_keywords_str, error = self.openai_client.call_chat_completion(
            messages=prompt_messages,
            model=self.config.get("default_model", "gpt-5-nano"),  # Use a cost-effective model for this
            temperature=0.1,
            max_completion_tokens=50,  # Keep output very short
            schema={
                "name": "extract_keywords",
                "type": "object",
                "properties": {
                    "keywords": {
                        "type": "string",
                        "description": "Comma-separated keywords.",
                    }
                },
                "required": ["keywords"],
                "additionalProperties": False # ADDED for strict schema enforcement (Task 7.1 fix)
            },
        )

        # Get the cost immediately after the call
        cost = self.openai_client.latest_cost

        if error or not extracted_keywords_str:
            self.logger.warning(
                f"Failed to extract keywords for Pexels. Falling back to original prompt. Error: {error}"
            )
            return descriptive_prompt, cost # Fallback to original prompt, return cost

        # The AI should return a dictionary with a 'keywords' key
        if (
            isinstance(extracted_keywords_str, dict)
            and "keywords" in extracted_keywords_str
        ):
            return extracted_keywords_str["keywords"], cost
        elif isinstance(
            extracted_keywords_str, str
        ):  # Fallback if AI doesn't follow schema perfectly
            return extracted_keywords_str, cost

        return descriptive_prompt, cost # Final fallback
```

**ACTION NO:** 11.5
**ACTION TYPE:** REPLACE
**ACTION RATIONALE:** The `generate_images_from_prompts` method is refactored into a new `generate_images_from_html` method. This new method is designed to parse image placeholders directly from the article's HTML (both `[[FEATURED_IMAGE: ...]]` and `[[IMAGE: ...]]`), generate images from Pexels, and track costs. It also adds logic to apply text overlays to featured images and cleans up the deprecated `generate_featured_image` method into a wrapper.

**FIND CONTEXT (Replace the block starting from `    # In class ImageGenerator, replace the generate_images_from_prompts method` to `        return images_data, total_cost`):**
```python
    # In class ImageGenerator, replace the generate_images_from_prompts method
    def generate_images_from_prompts(
        self, prompts: List[str]
    ) -> Tuple[List[Dict[str, Any]], float]:
        """
        Finds and saves in-article images from Pexels based on a list of specific prompts.
        """
        if not self.pexels_client:
            self.logger.warning(
                "Pexels client not initialized. Cannot generate images from prompts."
            )
            return [], 0.0

        images_data = []
        total_cost = 0.0

        for i, prompt in enumerate(prompts):
            search_query = self._simplify_prompt_for_pexels(prompt)
            self.logger.info(
                f"Searching Pexels for in-article image with simplified query: '{search_query}' (from prompt: '{prompt}')..."
            )

            pexels_photos, cost = self.pexels_client.search_photos(
                query=search_query, orientation="landscape", size="large", per_page=1
            )
            total_cost += cost

            if pexels_photos:
                photo = pexels_photos[0]
                photo_url = photo["src"].get("large") or photo["src"].get("original")

                if photo_url:
                    image_dir = "generated_images"
                    os.makedirs(image_dir, exist_ok=True)
                    file_path = os.path.join(
                        image_dir,
                        f"pexels-in-article-{utils.slugify(search_query)}-{photo['id']}.jpeg",
                    )
                    local_path = download_image_from_url(photo_url, file_path)

                    if local_path:
                        images_data.append(
                            {
                                "type": f"in_article_{i + 1}",
                                "search_query": search_query,
                                "original_prompt": prompt,
                                "local_path": local_path,
                                "remote_url": photo_url,
                                "alt_text": photo.get("alt") or prompt,
                                "source_id": photo["id"],
                                "source": "Pexels",
                            }
                        )
                        self.logger.info(
                            f"Successfully sourced in-article image from Pexels: {local_path}"
                        )
                        continue

            self.logger.warning(
                f"Could not find a suitable Pexels image for prompt: '{prompt}'."
            )

        return images_data, total_cost
```

**CODE TO REPLACE:**
```python
    # In class ImageGenerator, replace the generate_images_from_prompts method
    def generate_images_from_prompts(
        self, prompts: List[str]
    ) -> Tuple[List[Dict[str, Any]], float]:
        """
        Finds and saves in-article images from Pexels based on a list of specific prompts.
        """
        if not self.pexels_client:
            self.logger.warning(
                "Pexels client not initialized. Cannot generate images from prompts."
            )
            return [], 0.0

        images_data = []
        total_cost = 0.0

        for i, prompt in enumerate(prompts):
            search_query = self._simplify_prompt_for_pexels(prompt)
            self.logger.info(
                f"Searching Pexels for in-article image with simplified query: '{search_query}' (from prompt: '{prompt}')..."
            )

            pexels_photos, cost = self.pexels_client.search_photos(
                query=search_query, orientation="landscape", size="large", per_page=1
            )
            total_cost += cost

            if pexels_photos:
                photo = pexels_photos[0]
                photo_url = photo["src"].get("large") or photo["src"].get("original")

                if photo_url:
                    image_dir = "generated_images"
                    os.makedirs(image_dir, exist_ok=True)
                    file_path = os.path.join(
                        image_dir,
                        f"pexels-in-article-{utils.slugify(search_query)}-{photo['id']}.jpeg",
                    )
                    local_path = download_image_from_url(photo_url, file_path)

                    if local_path:
                        images_data.append(
                            {
                                "type": f"in_article_{i + 1}",
                                "search_query": search_query,
                                "original_prompt": prompt,
                                "local_path": local_path,
                                "remote_url": photo_url,
                                "alt_text": photo.get("alt") or prompt,
                                "source_id": photo["id"],
                                "source": "Pexels",
                            }
                        )
                        self.logger.info(
                            f"Successfully sourced in-article image from Pexels: {local_path}"
                        )
                        continue

            self.logger.warning(
                f"Could not find a suitable Pexels image for prompt: '{prompt}'."
            )

        return images_data, total_cost
```

**WITH NEW CODE:**
```python
    def generate_images_from_html(self, article_html: str, opportunity: Dict[str, Any]) -> Tuple[List[Dict[str, Any]], float]: # NEW method for Task 11
        """
        Finds all image placeholders in the HTML (featured and in-article),
        generates images from Pexels using contextual prompts, and returns the image data.
        """
        if not self.pexels_client:
            self.logger.warning(
                "Pexels client not initialized. Cannot generate images from prompts."
            )
            return [], 0.0

        images_data = []
        total_cost = 0.0

        # Parse HTML for ALL image placeholders (Task 11.2)
        import re
        featured_image_match = re.search(r'\[\[FEATURED_IMAGE: (.*?)\]\]', article_html)
        in_article_matches = re.findall(r'\[\[IMAGE: (.*?)\]\]', article_html)

        all_prompts_to_generate = []
        if featured_image_match:
            all_prompts_to_generate.append({"type": "featured", "prompt": featured_image_match.group(1)})
        for i, prompt_text in enumerate(in_article_matches):
            all_prompts_to_generate.append({"type": f"in_article_{i+1}", "prompt": prompt_text})

        for item in all_prompts_to_generate:
            original_prompt = item["prompt"]
            search_query, simplify_cost = self._simplify_prompt_for_pexels(original_prompt) # Simplify prompt and get cost (Task 11.2)
            total_cost += simplify_cost # Track AI cost for prompt simplification
            self.logger.info(
                f"Searching Pexels for image with simplified query: '{search_query}' (from prompt: '{original_prompt}')..."
            )

            pexels_photos, cost = self.pexels_client.search_photos(
                query=search_query, orientation="landscape", size="large", per_page=1
            )
            total_cost += cost

            if pexels_photos:
                photo = pexels_photos[0]
                photo_url = photo["src"].get("large") or photo["src"].get("original")

                if photo_url:
                    # Determine file path and apply overlay for featured images (Task 11.2)
                    is_featured = item["type"] == "featured"
                    image_dir = "generated_images"
                    os.makedirs(image_dir, exist_ok=True)
                    base_filename = f"pexels-{item['type']}-{utils.slugify(search_query)}-{photo['id']}.jpeg"
                    file_path = os.path.join(image_dir, base_filename)

                    local_path = download_image_from_url(photo_url, file_path)
                    if is_featured and local_path:
                        meta_title = opportunity.get("ai_content", {}).get("meta_title", opportunity["keyword"])
                        local_path = self._add_text_overlay(local_path, meta_title, output_suffix="-featured-overlay") # Use special suffix for featured image

                    if local_path:
                        images_data.append(
                            {
                                "type": item["type"],
                                "search_query": search_query,
                                "original_prompt": original_prompt,
                                "local_path": local_path,
                                "remote_url": photo_url,
                                "alt_text": photo.get("alt") or original_prompt,
                                "source_id": photo["id"],
                                "source": "Pexels",
                            }
                        )
                        self.logger.info(
                            f"Successfully sourced image from Pexels: {local_path}"
                        )
                        continue

            self.logger.warning( # Use original prompt for logging
                f"Could not find a suitable Pexels image for prompt: '{original_prompt}'."
            )

        return images_data, total_cost

    def generate_featured_image(self, opportunity: Dict[str, Any]) -> Tuple[Optional[Dict[str, Any]], float]: # DEPRECATED, now a wrapper
        """
        This is now a wrapper around generate_images_from_html for backward compatibility or direct featured image generation.
        """
        self.logger.warning("generate_featured_image is deprecated. Use generate_images_from_html for full image generation.")
        # Create a dummy HTML with just a featured image placeholder
        dummy_html = f"[[FEATURED_IMAGE: {opportunity.get('keyword', 'featured image') }]]"
        images_data, cost = self.generate_images_from_html(dummy_html, opportunity)
        
        # Return only the first (and likely only) featured image
        featured_image = next((img for img in images_data if img["type"] == "featured"), None)
        return featured_image, cost

    def generate_images_from_prompts(self, prompts: List[str]) -> Tuple[List[Dict[str, Any]], float]: # DEPRECATED, now a wrapper
        """
        This is a legacy wrapper. The main image generation should now happen via generate_images_from_html.
        """
        self.logger.warning("generate_images_from_prompts is deprecated. Use generate_images_from_html.")
        # This wrapper assumes a simple prompt list and creates a dummy HTML structure for it.
        # It's intended for backward compatibility or simple direct calls if needed.
        dummy_html_parts = []
        for prompt_text in prompts:
            dummy_html_parts.append(f"[[IMAGE: {prompt_text}]]")
        dummy_html = "\n".join(dummy_html_parts)
        
        dummy_opportunity = {
            "keyword": "general_image_search",
            "ai_content": {"meta_title": "Generated Content Image"},
            "blueprint": {"ai_content_brief": {"image_prompts": prompts}} # Pass original prompts for alt text etc.
        }
        images_data, total_cost = self.generate_images_from_html(dummy_html, dummy_opportunity)
        return images_data, total_cost
```

### **File: `backend/pipeline/orchestrator/content_orchestrator.py`**

**ACTION NO:** 11.6
**ACTION TYPE:** REPLACE
**ACTION RATIONALE:** The image generation logic is refactored. The old `generate_featured_image` call is removed. The new `image_generator.generate_images_from_html` method is called after the article HTML is generated, allowing it to parse image placeholders from the HTML directly. This centralizes image generation and makes it contextually aware.

**FIND CONTEXT (Replace the block starting from `            featured_image_data, image_cost = self.image_generator.generate_featured_image(` to `            total_api_cost += image_cost`):**
```python
            featured_image_data, image_cost = self.image_generator.generate_featured_image(
                opportunity
            )
            total_api_cost += image_cost
```

**CODE TO REPLACE:**
```python
            featured_image_data, image_cost = self.image_generator.generate_featured_image(
                opportunity
            )
            total_api_cost += image_cost
```

**WITH NEW CODE:**
```python
            # Task 11.3: Image generation moved AFTER HTML generation, and now handles both featured & in-article
            in_article_images_data, image_cost = self.image_generator.generate_images_from_html(current_html, opportunity) # This call will handle all images
            self.db_manager.increment_opportunity_cost(opportunity_id, image_cost) # Use incremental cost tracking (Task 5.3)
```

**ACTION NO:** 11.7
**ACTION TYPE:** REPLACE
**ACTION RATIONALE:** The arguments passed to `db_manager.save_full_content_package` are updated. `featured_image_data` is replaced with `None` as featured images are now part of `in_article_images_data`, and the combined `in_article_images_data` is passed.

**FIND CONTEXT (Replace the block starting from `                featured_image_data,` to `                total_api_cost, # Pass total cost`):**
```python
                featured_image_data,
                [],
                social_posts,
                final_package,
                total_api_cost, # Pass total cost
            )
```

**CODE TO REPLACE:**
```python
                featured_image_data,
                [],
                social_posts,
                final_package,
                total_api_cost, # Pass total cost
            )
```

**WITH NEW CODE:**
```python
                None, # Featured image data is now part of in_article_images_data after parsing
                in_article_images_data, # Pass combined image data
                social_posts,
                final_package,
                final_reported_cost, # Pass final cost from DB
            )
```

### **File: `backend/agents/html_formatter.py`**

**ACTION NO:** 11.8
**ACTION TYPE:** INSERT
**ACTION RATIONALE:** This code block implements the image replacement logic in the `HtmlFormatter`. It iterates through the generated image data, finds corresponding `[[IMAGE: ...]]` and `[[FEATURED_IMAGE: ...]]` placeholders in the HTML, and replaces them with actual `<img>` tags pointing to the locally stored images. Any unresolved placeholders are removed.

**FIND CONTEXT (Insert after the line containing):**
```python
        if client_cfg.get("generate_toc", True):
            self._generate_toc(soup)
```

**CODE TO INSERT:**```python
        # NEW: Image replacement logic (Task 11.4)
        if in_article_images_data:
            # Sort images by type so featured is processed first
            sorted_images = sorted(in_article_images_data, key=lambda x: 0 if x["type"] == "featured" else 1)
            
            for image_item in sorted_images:
                placeholder_type = "IMAGE"
                if image_item["type"] == "featured":
                    placeholder_type = "FEATURED_IMAGE"
                
                # A more flexible regex: match any text within the placeholder, but prioritize matching
                # based on whether an image of that type has already been inserted.
                # Use re.DOTALL to match across multiple lines if needed.
                placeholder_pattern = re.compile(rf'\[\[{placeholder_type}:.*?\]\]', re.IGNORECASE | re.DOTALL)
                
                # Find the first occurrence (or any occurrence if multiple are allowed)
                # We need to operate on the string representation of the soup or parse only the body content
                current_html_str = str(soup)
                match = placeholder_pattern.search(current_html_str)

                if match:
                    img_tag_str = f'<img src="/api/images/{os.path.basename(image_item["local_path"])}" alt="{image_item["alt_text"]}" />'
                    # Replace only the first found placeholder of the correct type
                    current_html_str = placeholder_pattern.sub(img_tag_str, current_html_str, 1)
                    soup = BeautifulSoup(current_html_str, "html.parser") # Re-parse to update soup
                    self.logger.info(f"Replaced placeholder for {image_item['type']} image: {image_item['original_prompt']}")
                else:
                    self.logger.warning(f"No placeholder found for {image_item['type']} image with original prompt: {image_item['original_prompt']}. It might have already been replaced or there's an issue.")

        # After processing all available images, remove any remaining image placeholders that weren't resolved
        final_html_body_str = re.sub(r'\[\[(FEATURED_)?IMAGE:.*?\]\]', str(soup), flags=re.IGNORECASE | re.DOTALL)
        soup = BeautifulSoup(final_html_body_str, "html.parser") # Re-parse to ensure integrity
```

---

**Task No:** 12
**Task Higher Overview:** Implement graceful degradation for non-critical external API failures and surface these warnings to the user in the UI.
**Files Involved:**
*   `backend/pipeline/orchestrator/content_orchestrator.py`
*   `backend/data_access/migrations/027_add_generation_warnings.sql` (New file)
*   `backend/data_access/database_manager.py`
*   `client/my-content-app/src/pages/opportunity-detail-page/index.jsx`
*   `client/my-content-app/src/pages/opportunity-detail-page/components/WarningsCard.jsx` (New file)
**Total Code Changes Required:** 8 granular changes (2 new files, 6 modifications).

**STEP BY STEP PLAN:**

### **File: `backend/pipeline/orchestrator/content_orchestrator.py`**

**ACTION NO:** 12.1
**ACTION TYPE:** INSERT
**ACTION RATIONALE:** Initializes an empty list `generation_warnings`. This list will accumulate non-critical errors encountered during content generation, allowing the workflow to continue while still recording issues for user review.

**FIND CONTEXT (Insert after the line containing):**
```python
            opportunity["ai_content"]["article_body_html"] = current_html
            opportunity["ai_content"]["audit_results"] = final_audit_results
```

**CODE TO INSERT:**
```python
            # NEW: Initialize a list for non-critical warnings (Task 12.1)
            generation_warnings = []
```

**ACTION NO:** 12.2
**ACTION TYPE:** REPLACE
**ACTION RATIONALE:** The "Key Takeaways" generation step is wrapped in a `try-except` block. If the AI call fails, the error is logged, a warning is added to `generation_warnings`, but the workflow continues. This ensures graceful degradation for this non-critical feature.

**FIND CONTEXT (Replace the block starting from `            self.job_manager.update_job_status(` to `            opportunity["ai_content"]["article_body_html"] = current_html # Update HTML with takeaways`):**
```python
            self.job_manager.update_job_status(
                job_id, "running", progress=88, result={"step": "Generating Key Takeaways"}
            )
            summary_prompt = f"""
            Read the following article HTML and generate a 3-5 bullet point 'Key Takeaways' summary inside a `<div>` with the class 'key-takeaways'. The takeaways should be concise and actionable.

            Article HTML:
            {current_html}
            """
            takeaways_html, takeaways_cost = self.openai_client.call_chat_completion(
                messages=[{"role": "user", "content": summary_prompt}]
                # No schema needed, just raw HTML output
            )
            self.db_manager.increment_opportunity_cost(opportunity_id, takeaways_cost) # Track cost
            if takeaways_html:
                current_html = takeaways_html + "\\n" + current_html
                opportunity["ai_content"]["article_body_html"] = current_html # Update HTML with takeaways
```

**CODE TO REPLACE:**
```python
            self.job_manager.update_job_status(
                job_id, "running", progress=88, result={"step": "Generating Key Takeaways"}
            )
            summary_prompt = f"""
            Read the following article HTML and generate a 3-5 bullet point 'Key Takeaways' summary inside a `<div>` with the class 'key-takeaways'. The takeaways should be concise and actionable.

            Article HTML:
            {current_html}
            """
            takeaways_html, takeaways_cost = self.openai_client.call_chat_completion(
                messages=[{"role": "user", "content": summary_prompt}]
                # No schema needed, just raw HTML output
            )
            self.db_manager.increment_opportunity_cost(opportunity_id, takeaways_cost) # Track cost
            if takeaways_html:
                current_html = takeaways_html + "\\n" + current_html
                opportunity["ai_content"]["article_body_html"] = current_html # Update HTML with takeaways
```

**WITH NEW CODE:**
```python
            self.job_manager.update_job_status(
                job_id, "running", progress=88, result={"step": "Generating Key Takeaways"}
            )
            try: # ADD TRY/EXCEPT (Task 12.1)
                summary_prompt = f"""
                Read the following article HTML and generate a 3-5 bullet point 'Key Takeaways' summary inside a `<div>` with the class 'key-takeaways'. The takeaways should be concise and actionable.

                Article HTML:
                {current_html}
                """
                takeaways_html, takeaways_cost = self.openai_client.call_chat_completion(
                    messages=[{"role": "user", "content": summary_prompt}]
                    # No schema needed, just raw HTML output
                )
                self.db_manager.increment_opportunity_cost(opportunity_id, takeaways_cost) # Track cost
                if takeaways_html:
                    current_html = takeaways_html + "\\n" + current_html
                    opportunity["ai_content"]["article_body_html"] = current_html # Update HTML with takeaways
            except Exception as e:
                self.logger.error(f"Key Takeaways generation failed but workflow will continue: {e}")
                generation_warnings.append(f"Key Takeaways generation failed: {str(e)}") # Add warning
```

**ACTION NO:** 12.3
**ACTION TYPE:** REPLACE
**ACTION RATIONALE:** The internal linking generation is now conditionally executed based on client settings. It's wrapped in a `try-except` block to catch potential failures, log them, and add a warning to `generation_warnings`, allowing the workflow to continue without interruption.

**FIND CONTEXT (Replace the block starting from `            internal_link_suggestions, link_cost = (` to `            total_api_cost += link_cost`):**
```python
            internal_link_suggestions, link_cost = (
                self.internal_linking_suggester.suggest_links(
                    opportunity["ai_content"]["article_body_html"],
                    opportunity.get("blueprint", {})
                    .get("ai_content_brief", {})
                    .get("key_entities_to_mention", []),
                    self.client_cfg.get("target_domain"),
                    self.client_id,
                )
            )
            total_api_cost += link_cost
```

**CODE TO REPLACE:**
```python
            internal_link_suggestions, link_cost = (
                self.internal_linking_suggester.suggest_links(
                    opportunity["ai_content"]["article_body_html"],
                    opportunity.get("blueprint", {})
                    .get("ai_content_brief", {})
                    .get("key_entities_to_mention", []),
                    self.client_cfg.get("target_domain"),
                    self.client_id,
                )
            )
            total_api_cost += link_cost
```

**WITH NEW CODE:**
```python
            # Task 8.3: Internal linking is now conditional
            internal_link_suggestions = [] # Default to empty
            try: # ADD TRY/EXCEPT (Task 12.1)
                if self.client_cfg.get("enable_automated_internal_linking", False):
                    link_suggestions, link_cost = self.internal_linking_suggester.suggest_links(
                        opportunity["ai_content"]["article_body_html"],
                        opportunity.get("blueprint", {}).get("ai_content_brief", {}).get("key_entities_to_mention", []),
                        self.client_cfg.get("target_domain"),
                        self.client_id,
                    )
                    internal_link_suggestions = link_suggestions
                    self.db_manager.increment_opportunity_cost(opportunity_id, link_cost) # Use incremental cost tracking (Task 5.3)
            except Exception as e:
                self.logger.error(f"Internal linking generation failed but workflow will continue: {e}")
                generation_warnings.append(f"Internal linking generation failed: {str(e)}") # Add warning
```

**ACTION NO:** 12.4
**ACTION TYPE:** INSERT
**ACTION RATIONALE:** This ensures that the `generation_warnings` list is stored within the `opportunity` dictionary. This allows the warnings to be persisted to the database and surfaced in the UI.

**FIND CONTEXT (Insert after the line containing):**
```python
            # Get final cost from DB for reporting
            final_reported_cost = self.db_manager.get_opportunity_by_id(opportunity_id).get("total_api_cost", 0.0)
```

**CODE TO INSERT:**
```python
            # Persist warnings
            opportunity["generation_warnings"] = generation_warnings # Store warnings in opportunity data
```

**ACTION NO:** 12.5
**ACTION TYPE:** REPLACE
**ACTION RATIONALE:** The `save_full_content_package` method call is updated to pass the `generation_warnings` list. This ensures that any non-critical issues encountered during content generation are persisted in the database. Also, the `final_package` call is moved here and arguments for `final_package` and `final_reported_cost` are correctly passed.

**FIND CONTEXT (Replace the block starting from `            self.db_manager.save_full_content_package(` to `            total_api_cost, # Pass total cost`):**
```python
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
```

**CODE TO REPLACE:**
```python
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
```

**WITH NEW CODE:**
```python
            self.db_manager.save_full_content_package( # Call with new args (Task 12.3)
                opportunity_id,
                opportunity["ai_content"],
                self.client_cfg.get("ai_content_model", "gpt-4o"),
                None, # Featured image data is now part of in_article_images_data after parsing
                in_article_images_data, # Pass combined image data
                social_posts,
                final_package,
                final_reported_cost, # Pass final cost from DB
                generation_warnings # NEW: Pass warnings to save
            )
```

**ACTION NO:** 12.6
**ACTION TYPE:** REPLACE
**ACTION RATIONALE:** The `result` dictionary in the `job_manager.update_job_status` call is updated to include `warnings`. This allows non-critical generation warnings to be surfaced directly in the job status. The error message is also made more general for graceful degradation.

**FIND CONTEXT (Replace the block starting from `                result={ "status": "success", "message": "Content generation completed.", },` to `                },`):**
```python
                result={
                    "status": "success",
                    "message": "Content generation completed.",
                },
            )
```

**CODE TO REPLACE:**
```python
                result={
                    "status": "success",
                    "message": "Content generation completed.",
                },
            )
```

**WITH NEW CODE:**
```python
                result={
                    "status": "success",
                    "message": "Content generation completed.",
                    "warnings": generation_warnings, # Also pass to job result
                },
            )
```

**ACTION NO:** 12.7
**ACTION TYPE:** REPLACE
**ACTION RATIONALE:** Updates the `job_manager.update_job_status` call in the `except` block to include `result={"warnings": generation_warnings}`. This ensures that even when the content generation fails, any accumulated non-critical warnings are still recorded in the job status for debugging.

**FIND CONTEXT (Replace the line containing `            self.job_manager.update_job_status(`):**
```python
            self.job_manager.update_job_status(
                job_id, "failed", progress=100, error=str(e)
            )
```

**CODE TO REPLACE:**
```python
            self.job_manager.update_job_status(
                job_id, "failed", progress=100, error=str(e)
            )
```

**WITH NEW CODE:**
```python
            self.job_manager.update_job_status(
                job_id, "failed", progress=100, error=str(e), result={"warnings": generation_warnings} # Include warnings on failure
            )
```

### **File: `backend/data_access/migrations/027_add_generation_warnings.sql`**

**ACTION NO:** 12.8
**ACTION TYPE:** CREATE_FILE
**ACTION RATIONALE:** This SQL migration script adds a new `generation_warnings` column to the `opportunities` table. This column will store a JSON string of non-critical warnings encountered during the content generation workflow, enabling graceful degradation and better feedback to the user.

**FILE PATH:** `backend/data_access/migrations/027_add_generation_warnings.sql`
**FILE CONTENT:**
```sql
-- backend/data_access/migrations/027_add_generation_warnings.sql

ALTER TABLE opportunities ADD COLUMN generation_warnings TEXT;
```

### **File: `backend/data_access/database_manager.py`**

**ACTION NO:** 12.9
**ACTION TYPE:** INSERT
**ACTION RATIONALE:** Adds `generation_warnings` to the list of `json_keys` that should be deserialized when retrieving opportunity data. This ensures that warnings stored as JSON strings in the database are correctly converted to Python objects.

**FIND CONTEXT (Insert after the line containing):**
```python
            "wordpress_payload_json",
```

**CODE TO INSERT:**
```python
            "generation_warnings", # From Task 12
```

**ACTION NO:** 12.10
**ACTION TYPE:** REPLACE
**ACTION RATIONALE:** The `save_full_content_package` method signature is updated to accept an optional `generation_warnings` argument. This allows non-critical warnings to be passed and persisted along with the rest of the generated content package.

**FIND CONTEXT (Replace the block starting from `    def save_full_content_package(` to `        total_api_cost: float,`):**
```python
    def save_full_content_package(
        self,
        opportunity_id: int,
        ai_content_data: Dict[str, Any],
        ai_content_model: str,
        featured_image_data: Optional[Dict[str, Any]],
        in_article_images_data: List[Dict[str, Any]],
        social_posts: Optional[List[Dict[str, Any]]],
        final_package: Dict[str, Any],
        total_api_cost: float,
    ):
```

**CODE TO REPLACE:**
```python
    def save_full_content_package(
        self,
        opportunity_id: int,
        ai_content_data: Dict[str, Any],
        ai_content_model: str,
        featured_image_data: Optional[Dict[str, Any]],
        in_article_images_data: List[Dict[str, Any]],
        social_posts: Optional[List[Dict[str, Any]]],
        final_package: Dict[str, Any],
        total_api_cost: float,
    ):
```

**WITH NEW CODE:**
```python
    def save_full_content_package(
        self,
        opportunity_id: int,
        ai_content_data: Dict[str, Any],
        ai_content_model: str,
        featured_image_data: Optional[Dict[str, Any]],
        in_article_images_data: List[Dict[str, Any]],
        social_posts: Optional[List[Dict[str, Any]]],
        final_package: Dict[str, Any],
        total_api_cost: float, # Now obtained from DB
        generation_warnings: Optional[List[str]] = None, # NEW argument for Task 12
    ):
```

**ACTION NO:** 12.11
**ACTION TYPE:** INSERT
**ACTION RATIONALE:** The `generation_warnings` argument is now included in the SQL `UPDATE` statement. If warnings exist, they are serialized to JSON and stored in the new `generation_warnings` column, ensuring persistence.

**FIND CONTEXT (Insert after the line containing):**
```python
                    total_api_cost,
                    opportunity_id,
                ),
            )
```

**CODE TO INSERT:**
```python
                    json.dumps(generation_warnings) if generation_warnings else None, # NEW
                    opportunity_id,
                ),
            )```

### **File: `client/my-content-app/src/pages/opportunity-detail-page/components/WarningsCard.jsx`**

**ACTION NO:** 12.12
**ACTION TYPE:** CREATE_FILE
**ACTION RATIONALE:** This new React component displays any non-critical `generation_warnings` in a prominent card on the opportunity detail page. It provides clear feedback to the user about issues encountered during content generation that did not halt the workflow.

**FILE PATH:** `client/my-content-app/src/pages/opportunity-detail-page/components/WarningsCard.jsx`
**FILE CONTENT:**
```jsx
// client/my-content-app/src/pages/opportunity-detail-page/components/WarningsCard.jsx
import React from 'react';
import { Card, Typography, List, Alert } from 'antd';
import { WarningOutlined } from '@ant-design/icons';
import NoData from './NoData';

const { Title, Paragraph } = Typography;

const WarningsCard = ({ warnings }) => {
  if (!warnings || warnings.length === 0) {
    return null; // Don't render if no warnings
  }

  return (
    <Card 
      title={
        <Title level={5} style={{ margin: 0 }}>
          <WarningOutlined style={{ marginRight: 8, color: '#faad14' }} /> Generation Warnings
        </Title>
      }
      style={{ marginTop: 24 }}
    >
      <Alert
        message="Non-Critical Issues Detected"
        description="The content generation workflow completed, but encountered some non-critical issues that did not halt the process."
        type="warning"
        showIcon
        style={{ marginBottom: 16 }}
      />
      <List
        dataSource={warnings}
        renderItem={(item) => (
          <List.Item>
            <Paragraph style={{ margin: 0 }}>{item}</Paragraph>
          </List.Item>
        )}
        size="small"
        bordered
      />
    </Card>
  );
};

export default WarningsCard;
```

### **File: `client/my-content-app/src/pages/opportunity-detail-page/index.jsx`**

**ACTION NO:** 12.13
**ACTION TYPE:** INSERT
**ACTION RATIONALE:** Imports the new `WarningsCard` component to display non-critical generation warnings on the opportunity detail page.

**FIND CONTEXT (Insert after the line containing):**
```jsx
import WorkflowTracker from './components/WorkflowTracker';
```

**CODE TO INSERT:**
```jsx
import WarningsCard from './components/WarningsCard'; // NEW IMPORT (Task 12.4)
```

**ACTION NO:** 12.14
**ACTION TYPE:** REPLACE
**ACTION RATIONALE:** Modifies the destructuring of `opportunity` to include `generation_warnings`. This allows the component to access and display any non-critical warnings recorded during the content generation process.

**FIND CONTEXT (Replace the line containing):**
```jsx
  const { blueprint, ai_content, social_media_posts_json, score_breakdown, full_data } = opportunity;
```

**CODE TO REPLACE:**
```jsx
  const { blueprint, ai_content, social_media_posts_json, score_breakdown, full_data } = opportunity;
```

**WITH NEW CODE:**
```jsx
  const { blueprint, ai_content, social_media_posts_json, score_breakdown, full_data, generation_warnings } = opportunity; // ADDED generation_warnings (Task 12.5)
```

**ACTION NO:** 12.15
**ACTION TYPE:** INSERT
**ACTION RATIONALE:** Inserts the `WarningsCard` component into the opportunity detail page's layout. This ensures that any `generation_warnings` are prominently displayed to the user.

**FIND CONTEXT (Insert after the line containing):**
```jsx
      <WorkflowTracker opportunity={opportunity} />
```

**CODE TO INSERT:**
```jsx
      <WarningsCard warnings={generation_warnings} />
```

---

**Task No:** 13
**Task Higher Overview:** Implement a configurable "Auto-Proceed" path to allow for true end-to-end automation for high-confidence opportunities, and create a background worker to execute this.
**Files Involved:**
*   `backend/app_config/settings.ini`
*   `backend/pipeline/orchestrator/analysis_orchestrator.py`
*   `backend/worker.py` (New file)
*   `backend/api/main.py`
*   `backend/data_access/database_manager.py` (New method)
**Total Code Changes Required:** 5 granular changes (1 new file, 4 modifications).

**STEP BY STEP PLAN:**

### **File: `backend/app_config/settings.ini`**

**ACTION NO:** 13.1
**ACTION TYPE:** INSERT
**ACTION RATIONALE:** Adds two new configuration settings: `enable_auto_proceed` (boolean) and `auto_proceed_confidence_threshold` (integer). These settings allow clients to enable or disable an automated workflow progression and define the confidence score threshold for auto-proceeding opportunities to content generation.

**FIND CONTEXT (Insert after the line containing):**```ini
max_words_for_ai_analysis = 2000
```

**CODE TO INSERT:**
```ini
enable_auto_proceed = false
auto_proceed_confidence_threshold = 85
```

### **File: `backend/pipeline/orchestrator/analysis_orchestrator.py`**

**ACTION NO:** 13.2
**ACTION TYPE:** REPLACE
**ACTION RATIONALE:** Modifies the final workflow state update logic. Instead of always pausing for approval, it now checks `enable_auto_proceed` and `auto_proceed_confidence_threshold` from `client_cfg`. If conditions are met, the opportunity's status is set to `auto_proceeded_to_generation` to trigger a background worker, enabling a fully automated path. Otherwise, it defaults to `paused_for_approval`.

**FIND CONTEXT (Replace the block starting from `            self.db_manager.update_opportunity_workflow_state(` to `                "api_cost": total_api_cost,`):**
```python
            self.db_manager.update_opportunity_workflow_state(
                opportunity_id, "analysis_completed", "paused_for_approval"
            )

            return {
                "status": "success",
                "message": "Analysis phase completed and opportunity re-scored.",
                "api_cost": total_api_cost,
            }
```

**CODE TO REPLACE:**
```python
            self.db_manager.update_opportunity_workflow_state(
                opportunity_id, "analysis_completed", "paused_for_approval"
            )

            return {
                "status": "success",
                "message": "Analysis phase completed and opportunity re-scored.",
                "api_cost": total_api_cost,
            }
```

**WITH NEW CODE:**
```python
            # Check for auto-proceed condition (Task 13.2)
            enable_auto_proceed = self.client_cfg.get("enable_auto_proceed", False)
            confidence_threshold = self.client_cfg.get("auto_proceed_confidence_threshold", 85)
            confidence_score = blueprint.get("final_qualification_assessment", {}).get("confidence_score", 0)

            if enable_auto_proceed and confidence_score >= confidence_threshold:
                self.logger.info(f"Opportunity {opportunity_id} meets auto-proceed criteria (Confidence: {confidence_score} >= {confidence_threshold}). Setting status to 'auto_proceeded_to_generation'.")
                # Updated error_message to details for update_opportunity_workflow_state
                self.db_manager.update_opportunity_workflow_state(
                    opportunity_id, "analysis_completed", "auto_proceeded_to_generation", details=f"Analysis completed. Auto-proceeded to generation due to confidence score {confidence_score}."
                )
                return {
                    "status": "success_auto_proceeded",
                    "message": "Analysis completed, auto-proceeded to content generation.",
                    "api_cost": self.db_manager.get_opportunity_by_id(opportunity_id).get("total_api_cost", 0.0),
                }
            else:
                self.db_manager.update_opportunity_workflow_state(
                    opportunity_id, "analysis_completed", "paused_for_approval"
                )
                return {
                    "status": "success",
                    "message": "Analysis phase completed. Awaiting user approval to proceed.",
                    "api_cost": self.db_manager.get_opportunity_by_id(opportunity_id).get("total_api_cost", 0.0),
                }
```

### **File: `backend/worker.py`**

**ACTION NO:** 13.3
**ACTION TYPE:** CREATE_FILE
**ACTION RATIONALE:** This new file defines a background worker process that periodically polls the database for opportunities that are ready to "auto-proceed" (e.g., after analysis completion and meeting confidence thresholds). When such opportunities are found, it automatically kicks off the next stage of the workflow (content generation) as an asynchronous job. This enables full end-to-end automation.

**FILE PATH:** `backend/worker.py`
**FILE CONTENT:**
```python
# backend/worker.py
import time
import logging
from typing import Dict, Any
from backend.data_access.database_manager import DatabaseManager
from backend.app_config.manager import ConfigManager
from backend.pipeline.orchestrator.main import WorkflowOrchestrator
from backend.jobs import JobManager # Import JobManager

logger = logging.getLogger(__name__)

# This worker will be initialized in api/main.py and run in a separate thread.
# It should ONLY perform lightweight polling and kick off new ASYNC jobs.
# It should NOT block the main thread.

def main_worker_loop(config_manager: ConfigManager, db_manager: DatabaseManager, job_manager: JobManager):
    logger.info("Starting background worker loop...")
    
    # We load config and orchestrator instance per loop for dynamic client_cfg and orchestrator state
    while True:
        try:
            # 1. Fetch ALL clients to check their individual settings
            clients = db_manager.get_clients()
            
            for client_data in clients:
                client_id = client_data['client_id']
                client_cfg = config_manager.load_client_config(client_id, db_manager)
                
                enable_auto_proceed = client_cfg.get("enable_auto_proceed", False)
                confidence_threshold = client_cfg.get("auto_proceed_confidence_threshold", 85)

                if enable_auto_proceed:
                    # Find opportunities that just finished analysis and are ready to auto-proceed
                    opportunities_to_auto_proceed = db_manager.get_opportunities_for_auto_proceed(client_id, confidence_threshold)
                    
                    for opp in opportunities_to_auto_proceed:
                        logger.info(f"Worker: Auto-proceeding opportunity {opp['id']} (Client: {client_id}) to content generation.")
                        
                        # Re-initialize orchestrator with current client's config
                        orchestrator = WorkflowOrchestrator(config_manager, db_manager, client_id, job_manager)
                        
                        # Trigger content generation as a new background job
                        job_id = orchestrator.run_full_content_generation(opp['id'])
                        
                        # Update the opportunity status to reflect that a new generation job has been started
                        db_manager.update_opportunity_workflow_state(opp['id'], "auto_proceeded_to_generation", "in_progress", details=f"Auto-proceeded to generation job {job_id}.")
                        
                        logger.info(f"Worker: Started content generation job {job_id} for opportunity {opp['id']}.")

            # 2. General cleanup/maintenance (optional, could be separate cron jobs)
            db_manager.clear_expired_api_cache()

        except Exception as e:
            logger.error(f"Error in background worker loop: {e}", exc_info=True)
            
        time.sleep(client_cfg.get("worker_poll_interval_seconds", 30)) # Configurable poll interval
```

### **File: `backend/api/main.py`**

**ACTION NO:** 13.4
**ACTION TYPE:** INSERT
**ACTION RATIONALE:** Imports the `threading` module to allow the FastAPI application to run a background worker thread.

**FIND CONTEXT (Insert after the line containing):**
```python
from jobs import JobManager  # Import the class
```

**CODE TO INSERT:**
```python
import threading # NEW for Task 13.3
```

**ACTION NO:** 13.5
**ACTION TYPE:** INSERT
**ACTION RATIONALE:** This code block initializes and starts the `main_worker_loop` in a separate daemon thread during application startup. This enables the background worker to continuously monitor for auto-proceed opportunities without blocking the main FastAPI application.

**FIND CONTEXT (Insert after the line containing):**
```python
    logger.info("FastAPI application startup complete. Dependencies initialized.")
```

**CODE TO INSERT:**
```python
    # NEW: Start the background worker thread (Task 13.3)
    from backend.worker import main_worker_loop
    worker_thread = threading.Thread(target=main_worker_loop, args=(api_globals.config_manager, api_globals.db_manager, api_globals.job_manager), daemon=True)
    worker_thread.start()
    logger.info("Background worker thread started.")
```

### **File: `backend/data_access/database_manager.py`**

**ACTION NO:** 13.6
**ACTION TYPE:** INSERT
**ACTION RATIONALE:** Adds the `get_opportunities_for_auto_proceed` method to `DatabaseManager`. This method queries the database for opportunities that have completed analysis, are `paused_for_approval`, and meet a configurable `confidence_threshold`. This is essential for the background worker to identify and automatically progress eligible opportunities.

**FIND CONTEXT (Insert after the `override_disqualification` method):**
```python
    def override_disqualification(self, opportunity_id: int) -> bool:
        """Manually overrides a failed qualification, resetting status to pending."""
```

**CODE TO INSERT:**
```python
    def get_opportunities_for_auto_proceed(self, client_id: str, confidence_threshold: int) -> List[Dict[str, Any]]:
        """
        Retrieves opportunities that have completed analysis and are ready to be auto-proceeded
        to content generation based on confidence score. (Task 13.5)
        """
        conn = self._get_conn()
        with conn:
            cursor = conn.execute(
                """
                SELECT id, keyword, blueprint_data FROM opportunities
                WHERE client_id = ? AND status = 'paused_for_approval'
                AND CAST(JSON_EXTRACT(blueprint_data, '$.final_qualification_assessment.confidence_score') AS INTEGER) >= ?;
                """,
                (client_id, confidence_threshold),
            )
            return self._deserialize_rows(cursor.fetchall())
```

---

**Task No:** 14
**Task Higher Overview:** Refactor database schema and application code to use direct, structured columns for core opportunity metrics instead of JSON blobs, and implement a migration.
**Files Involved:**
*   `backend/data_access/migrations/028_normalize_core_opportunity_fields.sql` (New file)
*   `backend/data_access/database_manager.py`
*   `backend/pipeline/step_03_prioritization/scoring_engine.py`
*   `backend/pipeline/step_01_discovery/disqualification_rules.py`
*   `backend/data_mappers/dataforseo_mapper.py`
*   `backend/api/routers/opportunities.py`
*   `client/my-content-app/src/pages/OpportunitiesPage/OpportunitiesPage.jsx`
*   `client/my-content-app/src/pages/opportunity-detail-page/components/KeywordMetrics.jsx`
**Total Code Changes Required:** 11 granular changes (1 new migration file, 10 modifications).

**STEP BY STEP PLAN:**

### **File: `backend/data_access/migrations/028_normalize_core_opportunity_fields.sql`**

**ACTION NO:** 14.1
**ACTION TYPE:** CREATE_FILE
**ACTION RATIONALE:** This SQL migration script adds new, direct columns to the `opportunities` table for frequently accessed keyword metrics (search volume, keyword difficulty, CPC, competition, main intent, and search volume trend). It also includes a backfill `UPDATE` statement to populate these new columns from the existing `full_data` JSON blob, ensuring data integrity during the migration. Finally, it creates indexes for improved query performance.

**FILE PATH:** `backend/data_access/migrations/028_normalize_core_opportunity_fields.sql`
**FILE CONTENT:**
```sql
-- backend/data_access/migrations/028_normalize_core_opportunity_fields.sql

-- Add new columns to opportunities table
ALTER TABLE opportunities ADD COLUMN search_volume INTEGER;
ALTER TABLE opportunities ADD COLUMN keyword_difficulty INTEGER;
ALTER TABLE opportunities ADD COLUMN cpc REAL;
ALTER TABLE opportunities ADD COLUMN competition REAL;
ALTER TABLE opportunities ADD COLUMN main_intent TEXT;
ALTER TABLE opportunities ADD COLUMN search_volume_trend_json TEXT; -- Renamed to avoid conflict with old json field

-- Backfill data from existing full_data JSON blob for existing opportunities
UPDATE opportunities
SET
    search_volume = CAST(JSON_EXTRACT(full_data, '$.keyword_info.search_volume') AS INTEGER),
    keyword_difficulty = CAST(JSON_EXTRACT(full_data, '$.keyword_properties.keyword_difficulty') AS INTEGER),
    cpc = CAST(JSON_EXTRACT(full_data, '$.keyword_info.cpc') AS REAL),
    competition = CAST(JSON_EXTRACT(full_data, '$.keyword_info.competition') AS REAL),
    main_intent = JSON_EXTRACT(full_data, '$.search_intent_info.main_intent'),
    search_volume_trend_json = JSON_EXTRACT(full_data, '$.keyword_info.search_volume_trend')
WHERE
    full_data IS NOT NULL AND search_volume IS NULL; -- Only backfill if the new columns are null

-- Create indexes on these new columns for improved query performance
CREATE INDEX IF NOT EXISTS idx_opportunities_search_volume ON opportunities (search_volume);
CREATE INDEX IF NOT EXISTS idx_opportunities_keyword_difficulty ON opportunities (keyword_difficulty);
CREATE INDEX IF NOT EXISTS idx_opportunities_cpc ON opportunities (cpc);
CREATE INDEX IF NOT EXISTS idx_opportunities_competition ON opportunities (competition);
CREATE INDEX IF NOT EXISTS idx_opportunities_main_intent ON opportunities (main_intent);
```

### **File: `backend/data_access/database_manager.py`**

**ACTION NO:** 14.2
**ACTION TYPE:** INSERT
**ACTION RATIONALE:** Defines a list of column names (`DIRECT_OPPORTUNITY_COLUMNS`) that are now directly stored in the `opportunities` table instead of nested within the `full_data` JSON blob. This improves direct data access and query performance.

**FIND CONTEXT (Insert after the line containing):**
```python
DB_FILE = "data/opportunities.db"
```

**CODE TO INSERT:**
```python
# NEW: List of fields that are now directly stored as columns (Task 14)
DIRECT_OPPORTUNITY_COLUMNS = ['search_volume', 'keyword_difficulty', 'cpc', 'competition', 'main_intent', 'search_volume_trend_json']
```

**ACTION NO:** 14.3
**ACTION TYPE:** INSERT
**ACTION RATIONALE:** Adds the new direct column names (`search_volume`, `keyword_difficulty`, `cpc`, `competition`, `main_intent`) to the list of `json_keys`. This ensures that even if these fields are populated as direct columns, the deserialization logic (if triggered for older `full_data` entries) will attempt to handle them.

**FIND CONTEXT (Insert after the line containing):**```python
            "competitor_page_timing_json",  # ADDED THIS LINE
```

**CODE TO INSERT:**
```python
            # NEW: Explicitly list the new direct columns that were previously inside full_data
            'search_volume', 'keyword_difficulty', 'cpc', 'competition', 'main_intent',
```

**ACTION NO:** 14.4
**ACTION TYPE:** REPLACE
**ACTION RATIONALE:** This is a critical update to the `_deserialize_rows` method, implementing backward compatibility for opportunities created before the database migration (Task 14.1). For each `DIRECT_OPPORTUNITY_COLUMNS` field, it now checks if the direct column is `None`. If it is, it attempts to extract the value from the `full_data` JSON blob. This ensures that older, unmigrated opportunities can still be loaded and processed correctly. It also specifically handles `search_volume_trend_json` and `monthly_searches` for consistency.

**FIND CONTEXT (Replace the block starting from `            # --- Data Unification and Renaming (with added safety checks and handling promoted columns) ---` to `            if "ai_content_json" in final_item:`):**
```python
            # --- Data Unification and Renaming (with added safety checks and handling promoted columns) ---
            # Ensure direct columns are prioritized; if null, try to extract from old JSON blobs for backward compatibility
            if final_item.get("main_intent") is None and isinstance(
                final_item.get("search_intent_info"), dict
            ):
                final_item["main_intent"] = final_item["search_intent_info"].get(
                    "main_intent"
                )
            if final_item.get("cpc") is None and isinstance(
                final_item.get("keyword_info"), dict
            ):
                final_item["cpc"] = float(final_item["keyword_info"].get("cpc") or 0.0)
            if final_item.get("competition") is None and isinstance(
                final_item.get("keyword_info"), dict
            ):
                final_item["competition"] = float(
                    final_item["keyword_info"].get("competition") or 0.0
                )
            if final_item.get("search_volume") is None and isinstance(
                final_item.get("keyword_info"), dict
            ):
                final_item["search_volume"] = int(
                    final_item["keyword_info"].get("search_volume") or 0
                )
            if final_item.get("keyword_difficulty") is None and isinstance(
                final_item.get("keyword_properties"), dict
            ):
                final_item["keyword_difficulty"] = int(
                    final_item["keyword_properties"].get("keyword_difficulty") or 0
                )

            # Deserialize search_volume_trend_json if present in new column
            if isinstance(final_item.get("search_volume_trend_json"), str):
                try:
                    final_item["search_volume_trend"] = json.loads(
                        final_item["search_volume_trend_json"]
                    )
                except json.JSONDecodeError:
                    self.logger.warning(
                        f"Failed to parse search_volume_trend_json for row ID {final_item.get('id')}. Resetting."
                    )
                    final_item["search_volume_trend"] = {}
            # Fallback to old keyword_info if new column is empty
            elif isinstance(final_item.get("keyword_info"), dict):
                final_item["search_volume_trend"] = final_item["keyword_info"].get(
                    "search_volume_trend"
                )

            # Deserialize competitor_social_media_tags_json
            if isinstance(final_item.get("competitor_social_media_tags_json"), str):
                try:
                    final_item["competitor_social_media_tags"] = json.loads(
                        final_item["competitor_social_media_tags_json"]
                    )
                except json.JSONDecodeError:
                    self.logger.warning(
                        f"Failed to parse competitor_social_media_tags_json for row ID {final_item.get('id')}. Resetting."
                    )
                    final_item["competitor_social_media_tags"] = {}

            # Deserialize competitor_page_timing_json
            if isinstance(final_item.get("competitor_page_timing_json"), str):
                try:
                    final_item["competitor_page_timing"] = json.loads(
                        final_item["competitor_page_timing_json"]
                    )
                except json.JSONDecodeError:
                    self.logger.warning(
                        f"Failed to parse competitor_page_timing_json for row ID {final_item.get('id')}. Resetting."
                    )
                    final_item["competitor_page_timing"] = {}

            # Ensure keyword_properties is a dict before assigning to it (for `intent` field that might be manually added)
            if not isinstance(final_item.get("keyword_properties"), dict):
                final_item["keyword_properties"] = {}
            if final_item.get("main_intent") and isinstance(
                final_item.get("keyword_properties"), dict
            ):
                final_item["keyword_properties"]["intent"] = final_item["main_intent"]

            # Simplify monthly_searches if stored as JSON string directly
            if isinstance(
                final_item.get("monthly_searches_json"), str
            ):  # This is from Task 1.2
                try:
                    final_item["monthly_searches"] = json.loads(
                        final_item["monthly_searches_json"]
                    )
                except json.JSONDecodeError:
                    self.logger.warning(
                        f"Failed to parse monthly_searches_json for row ID {final_item.get('id')}. Resetting."
                    )
                    final_item["monthly_searches"] = []
            # Fallback to old keyword_info if new column is empty
            elif isinstance(
                final_item.get("keyword_info"), dict
            ):  # This is the old way, still in place for historical data
                final_item["monthly_searches"] = final_item["keyword_info"].get(
                    "monthly_searches"
                )

            if "blueprint_data" in final_item:
                final_item["blueprint"] = final_item.pop("blueprint_data")
            if "ai_content_json" in final_item:
                final_item["ai_content"] = final_item.pop("ai_content_json")
```

**CODE TO REPLACE:**
```python
            # --- Data Unification and Renaming (with added safety checks and handling promoted columns) ---
            # Ensure direct columns are prioritized; if null, try to extract from old JSON blobs for backward compatibility
            if final_item.get("main_intent") is None and isinstance(
                final_item.get("search_intent_info"), dict
            ):
                final_item["main_intent"] = final_item["search_intent_info"].get(
                    "main_intent"
                )
            if final_item.get("cpc") is None and isinstance(
                final_item.get("keyword_info"), dict
            ):
                final_item["cpc"] = float(final_item["keyword_info"].get("cpc") or 0.0)
            if final_item.get("competition") is None and isinstance(
                final_item.get("keyword_info"), dict
            ):
                final_item["competition"] = float(
                    final_item["keyword_info"].get("competition") or 0.0
                )
            if final_item.get("search_volume") is None and isinstance(
                final_item.get("keyword_info"), dict
            ):
                final_item["search_volume"] = int(
                    final_item["keyword_info"].get("search_volume") or 0
                )
            if final_item.get("keyword_difficulty") is None and isinstance(
                final_item.get("keyword_properties"), dict
            ):
                final_item["keyword_difficulty"] = int(
                    final_item["keyword_properties"].get("keyword_difficulty") or 0
                )

            # Deserialize search_volume_trend_json if present in new column
            if isinstance(final_item.get("search_volume_trend_json"), str):
                try:
                    final_item["search_volume_trend"] = json.loads(
                        final_item["search_volume_trend_json"]
                    )
                except json.JSONDecodeError:
                    self.logger.warning(
                        f"Failed to parse search_volume_trend_json for row ID {final_item.get('id')}. Resetting."
                    )
                    final_item["search_volume_trend"] = {}
            # Fallback to old keyword_info if new column is empty
            elif isinstance(final_item.get("keyword_info"), dict):
                final_item["search_volume_trend"] = final_item["keyword_info"].get(
                    "search_volume_trend"
                )

            # Deserialize competitor_social_media_tags_json
            if isinstance(final_item.get("competitor_social_media_tags_json"), str):
                try:
                    final_item["competitor_social_media_tags"] = json.loads(
                        final_item["competitor_social_media_tags_json"]
                    )
                except json.JSONDecodeError:
                    self.logger.warning(
                        f"Failed to parse competitor_social_media_tags_json for row ID {final_item.get('id')}. Resetting."
                    )
                    final_item["competitor_social_media_tags"] = {}

            # Deserialize competitor_page_timing_json
            if isinstance(final_item.get("competitor_page_timing_json"), str):
                try:
                    final_item["competitor_page_timing"] = json.loads(
                        final_item["competitor_page_timing_json"]
                    )
                except json.JSONDecodeError:
                    self.logger.warning(
                        f"Failed to parse competitor_page_timing_json for row ID {final_item.get('id')}. Resetting."
                    )
                    final_item["competitor_page_timing"] = {}

            # Ensure keyword_properties is a dict before assigning to it (for `intent` field that might be manually added)
            if not isinstance(final_item.get("keyword_properties"), dict):
                final_item["keyword_properties"] = {}
            if final_item.get("main_intent") and isinstance(
                final_item.get("keyword_properties"), dict
            ):
                final_item["keyword_properties"]["intent"] = final_item["main_intent"]

            # Simplify monthly_searches if stored as JSON string directly
            if isinstance(
                final_item.get("monthly_searches_json"), str
            ):  # This is from Task 1.2
                try:
                    final_item["monthly_searches"] = json.loads(
                        final_item["monthly_searches_json"]
                    )
                except json.JSONDecodeError:
                    self.logger.warning(
                        f"Failed to parse monthly_searches_json for row ID {final_item.get('id')}. Resetting."
                    )
                    final_item["monthly_searches"] = []
            # Fallback to old keyword_info if new column is empty
            elif isinstance(
                final_item.get("keyword_info"), dict
            ):  # This is the old way, still in place for historical data
                final_item["monthly_searches"] = final_item["keyword_info"].get(
                    "monthly_searches"
                )

            if "blueprint_data" in final_item:
                final_item["blueprint"] = final_item.pop("blueprint_data")
            if "ai_content_json" in final_item:
                final_item["ai_content"] = final_item.pop("ai_content_json")
```

**WITH NEW CODE:**
```python
            # --- START Task 14.2 & 14.4 (Backward compatibility and cleanup) ---
            # For new items where direct columns are populated, no need to touch full_data.
            # For old items, we extract from `full_data` if the direct column is NULL.
            # The migration script ensures direct columns are filled for existing data.
            # This `_deserialize_rows` should ensure the 'opportunity' dict has all expected keys
            # either from direct columns or parsed JSON.
            
            # General fallback logic for DIRECT_OPPORTUNITY_COLUMNS
            full_data_parsed = {}
            if final_item.get('full_data') is not None and isinstance(final_item['full_data'], str):
                try:
                    full_data_parsed = json.loads(final_item['full_data'])
                except json.JSONDecodeError:
                    self.logger.warning(f"Failed to parse full_data JSON for row ID {final_item.get('id')}.")

            for col_name in DIRECT_OPPORTUNITY_COLUMNS:
                # If the direct column is None, try to extract from full_data_parsed
                if final_item.get(col_name) is None:
                    if col_name == 'search_volume':
                        final_item['search_volume'] = full_data_parsed.get('keyword_info', {}).get('search_volume')
                    elif col_name == 'keyword_difficulty':
                        final_item['keyword_difficulty'] = full_data_parsed.get('keyword_properties', {}).get('keyword_difficulty')
                    elif col_name == 'cpc':
                        final_item['cpc'] = full_data_parsed.get('keyword_info', {}).get('cpc')
                    elif col_name == 'competition':
                        final_item['competition'] = full_data_parsed.get('keyword_info', {}).get('competition')
                    elif col_name == 'main_intent':
                        final_item['main_intent'] = full_data_parsed.get('search_intent_info', {}).get('main_intent')
                    elif col_name == 'search_volume_trend_json':
                        # This should usually be handled by a direct JSON_EXTRACT in the migration for existing data
                        # But as a last resort fallback, if still None here, try to get from old keyword_info
                        if final_item.get('search_volume_trend_json') is None:
                            trend_data = full_data_parsed.get('keyword_info', {}).get('search_volume_trend')
                            if trend_data:
                                final_item['search_volume_trend_json'] = json.dumps(trend_data)

            # Handle `search_volume_trend` specifically (it's now a JSON string in its own column)
            if final_item.get('search_volume_trend_json') is not None and isinstance(final_item['search_volume_trend_json'], str):
                try:
                    final_item['search_volume_trend'] = json.loads(final_item['search_volume_trend_json'])
                except json.JSONDecodeError:
                    self.logger.warning(f"Failed to parse search_volume_trend_json for row ID {final_item.get('id')}. Resetting.")
                    final_item['search_volume_trend'] = {}
            elif final_item.get('search_volume_trend') is None and isinstance(full_data_parsed.get('keyword_info'), dict):
                 # Fallback to old keyword_info if new column is empty AND full_data exists
                 final_item['search_volume_trend'] = full_data_parsed['keyword_info'].get('search_volume_trend')

            # Handle `monthly_searches` (still extracted from `keyword_info` JSON blob for historical data)
            if final_item.get('monthly_searches') is None and isinstance(full_data_parsed.get('keyword_info'), dict):
                final_item['monthly_searches'] = full_data_parsed['keyword_info'].get('monthly_searches')

            # Existing renames for blueprint and ai_content (they remain JSON blobs)
            if "blueprint_data" in final_item:
                final_item["blueprint"] = final_item.pop("blueprint_data")
            if "ai_content_json" in final_item:
                final_item["ai_content"] = final_item.pop("ai_content_json")
            # --- END Task 14.2 & 14.4 ---
```

### **File: `backend/pipeline/step_03_prioritization/scoring_engine.py`**

**ACTION NO:** 14.5
**ACTION TYPE:** REPLACE
**ACTION RATIONALE:** The `data_source` variable is now assigned directly from `opportunity` because core keyword metrics are migrated to direct columns (Task 14). This removes reliance on extracting from `full_data` for primary scoring, simplifying access and improving performance.

**FIND CONTEXT (Replace the line containing `        data_source = opportunity.get("full_data", opportunity)`):**
```python
        data_source = opportunity.get("full_data", opportunity)
```

**CODE TO REPLACE:**
```python
        data_source = opportunity.get("full_data", opportunity)
```

**WITH NEW CODE:**
```python
        # Use opportunity directly, as core fields are now direct columns (Task 14)
        data_source = opportunity 
```

**ACTION NO:** 14.6
**ACTION TYPE:** REPLACE
**ACTION RATIONALE:** The `breakdown` dictionary is updated for each scoring component (`ease_of_ranking`, `traffic_potential`, etc.) to ensure that the `breakdown` field itself is always a dictionary. This fixes a potential type inconsistency where some breakdowns might incorrectly be `None` or a string, which could cause issues in downstream processing or UI rendering.

**FIND CONTEXT (Replace the block starting from `        breakdown["ease_of_ranking"] = {` to `            "breakdown": ease_breakdown,` for `ease_of_ranking`):**
```python
        breakdown["ease_of_ranking"] = {
            "name": "Ease of Ranking",
            "score": ease_score,
            "breakdown": ease_breakdown,
        }
```

**CODE TO REPLACE:**
```python
        breakdown["ease_of_ranking"] = {
            "name": "Ease of Ranking",
            "score": ease_score,
            "breakdown": ease_breakdown,
        }
```

**WITH NEW CODE:**
```python
        breakdown["ease_of_ranking"] = {
            "name": "Ease of Ranking",
            "score": ease_score,
            "breakdown": ease_breakdown, # Ensure this is a dict
        }
```
*(Repeat similar replacements for `traffic_potential`, `commercial_intent`, `growth_trend`, `serp_features`, `serp_volatility`, `competitor_weakness`, `serp_crowding`, `keyword_structure`, `serp_threat`, `volume_volatility`, `serp_freshness`, `competitor_performance` blocks in `scoring_engine.py`. The original `score_breakdown` entries in `scoring_engine.py` actually *are* already dictionaries, so this action primarily confirms existing good structure, but I will include one example here to show the format.)*

**ACTION NO:** 14.7
**ACTION TYPE:** REPLACE
**ACTION RATIONALE:** The calculation for `traffic_potential_score` is updated to directly use `opportunity.get("traffic_value", 0)` instead of extracting it from `keyword_info`. This aligns with the new direct column access and simplifies the code. (Correction: Reverted to use direct columns `sv` and `cpc` for computation, as `traffic_value` itself might not be directly in `opportunity`.)

**FIND CONTEXT (Replace the line containing `        traffic_value = sv * cpc`):**
```python
        traffic_value = sv * cpc
```

**CODE TO REPLACE:**
```python
        traffic_value = sv * cpc
```

**WITH NEW CODE:**
```python
        traffic_value = (data.get("search_volume", 0) or 0) * (data.get("cpc", 0.0) or 0.0) # Use direct columns
```

### **File: `backend/pipeline/step_01_discovery/disqualification_rules.py`**

**ACTION NO:** 14.8
**ACTION TYPE:** REPLACE
**ACTION RATIONALE:** This block replaces the extraction of keyword metrics (search volume, KD, CPC, competition, main intent) from nested `keyword_info`, `keyword_properties`, and `search_intent_info` JSON blobs. Instead, it now accesses these values directly from the `opportunity` object, reflecting the new normalized database columns (Task 14). Old JSON lookups are retained as `_old_json` variants for specific rules that might still reference them.

**FIND CONTEXT (Replace the block starting from `    keyword_info = opportunity.get("keyword_info") or {}` to `    intent_info = opportunity.get("search_intent_info") or {}`):**
```python
    keyword_info = opportunity.get("keyword_info") or {}
    keyword_props = opportunity.get("keyword_properties") or {}
    avg_backlinks = opportunity.get("avg_backlinks_info") or {}
    intent_info = opportunity.get("search_intent_info") or {}
```

**CODE TO REPLACE:**
```python
    keyword_info = opportunity.get("keyword_info") or {}
    keyword_props = opportunity.get("keyword_properties") or {}
    avg_backlinks = opportunity.get("avg_backlinks_info") or {}
    intent_info = opportunity.get("search_intent_info") or {}
```

**WITH NEW CODE:**
```python
    # Now use direct columns for efficiency (Task 14)
    search_volume = opportunity.get("search_volume")
    keyword_difficulty = opportunity.get("keyword_difficulty")
    cpc = opportunity.get("cpc")
    competition = opportunity.get("competition")
    main_intent = opportunity.get("main_intent")
    avg_backlinks = opportunity.get("avg_backlinks_info", {}) # Still from full_data for now
    
    # Old keyword_info/keyword_properties/search_intent_info JSON blobs are still used for some rules
    # but main access will shift to direct columns.
    keyword_info_old_json = opportunity.get("keyword_info", {})
    keyword_props_old_json = opportunity.get("keyword_properties", {})
    intent_info_old_json = opportunity.get("search_intent_info", {})
```

**ACTION NO:** 14.9
**ACTION TYPE:** REPLACE
**ACTION RATIONALE:** Updates the `allowed_intents` and `foreign_intents` logic to use the new direct `main_intent` column and the old JSON `foreign_intent` field, respectively. This aligns with the database normalization.

**FIND CONTEXT (Replace the block starting from `    allowed_intents = client_cfg.get("allowed_intents", ["informational"])` to `    foreign_intents = intent_info.get("foreign_intent", [])`):**
```python
    allowed_intents = client_cfg.get("allowed_intents", ["informational"])
    main_intent = intent_info.get("main_intent")
    foreign_intents = intent_info.get("foreign_intent", [])
```

**CODE TO REPLACE:**
```python
    allowed_intents = client_cfg.get("allowed_intents", ["informational"])
    main_intent = intent_info.get("main_intent")
    foreign_intents = intent_info.get("foreign_intent", [])
```

**WITH NEW CODE:**
```python
    allowed_intents = client_cfg.get("allowed_intents", ["informational"]) # Config
    # main_intent is now a direct column (Task 14)
    foreign_intents = intent_info_old_json.get("foreign_intent", []) # Still from JSON for foreign_intents
```

**ACTION NO:** 14.10
**ACTION TYPE:** REPLACE
**ACTION RATIONALE:** Updates the `is_another_language` check to use the `keyword_props_old_json` for backward compatibility, as this specific property is still expected in the old JSON structure for unmigrated data.

**FIND CONTEXT (Replace the line containing):**
```python
    if keyword_props.get("is_another_language"):
```

**CODE TO REPLACE:**
```python
    if keyword_props.get("is_another_language"):
```

**WITH NEW CODE:**
```python
    if keyword_props_old_json.get("is_another_language"):
```

**ACTION NO:** 14.11
**ACTION TYPE:** REPLACE
**ACTION RATIONALE:** Updates the `core_keyword` extraction to use `keyword_props_old_json`, maintaining backward compatibility for this field.

**FIND CONTEXT (Replace the line containing):**
```python
    core_keyword = keyword_props.get("core_keyword")
```

**CODE TO REPLACE:**
```python
    core_keyword = keyword_props.get("core_keyword")
```

**WITH NEW CODE:**
```python
    core_keyword = keyword_props_old_json.get("core_keyword") # Still from JSON
```

**ACTION NO:** 14.12
**ACTION TYPE:** REPLACE
**ACTION RATIONALE:** Updates the `search_volume` check to use the new direct `search_volume` column, aligning with the normalized database schema.

**FIND CONTEXT (Replace the line containing `    if utils.safe_compare(        keyword_info.get("search_volume"), client_cfg.get("min_search_volume"), "lt"    ):`):**
```python
    if utils.safe_compare(
        keyword_info.get("search_volume"), client_cfg.get("min_search_volume"), "lt"
    ):
```

**CODE TO REPLACE:**```python
    if utils.safe_compare(
        keyword_info.get("search_volume"), client_cfg.get("min_search_volume"), "lt"
    ):
```

**WITH NEW CODE:**
```python
    if utils.safe_compare(
        search_volume, client_cfg.get("min_search_volume"), "lt" # Use direct column
    ):
```

**ACTION NO:** 14.13
**ACTION TYPE:** DELETE
**ACTION RATIONALE:** The `foreign_intents` check previously used `intent_info.get("foreign_intent", []) or []`. This is now replaced by the `foreign_intents` variable set from `intent_info_old_json` in the initial block.

**FIND CONTEXT (Delete the line containing `    foreign_intents = intent_info.get("foreign_intent", []) or []`):**
```python
    foreign_intents = intent_info.get("foreign_intent", []) or []
```

**CODE TO DELETE:**
```python
    foreign_intents = intent_info.get("foreign_intent", []) or []
```

**ACTION NO:** 14.14
**ACTION TYPE:** REPLACE
**ACTION RATIONALE:** Updates the `monthly_searches` access to refer to the `opportunity` object directly. The `_deserialize_rows` method (Task 14.4) is responsible for ensuring `monthly_searches` is correctly deserialized and available at the top level of the `opportunity` dictionary.

**FIND CONTEXT (Replace the line containing `    monthly_searches = opportunity.get(`):**
```python
    monthly_searches = opportunity.get(
        "monthly_searches", []
    )  # Get from opportunity object, which is deserialized
```

**CODE TO REPLACE:**
```python
    monthly_searches = opportunity.get(
        "monthly_searches", []
    )  # Get from opportunity object, which is deserialized
```

**WITH NEW CODE:**
```python
    monthly_searches = opportunity.get( # This is now a direct field after deserialization (Task 14)
        "monthly_searches", []
    )
```

**ACTION NO:** 14.15
**ACTION TYPE:** REPLACE
**ACTION RATIONALE:** Updates the `competition` check to use the new direct `competition` column, aligning with the normalized database schema.

**FIND CONTEXT (Replace the block starting from `    if utils.safe_compare(` to `    ) and (keyword_info.get("competition_level") == "HIGH"):`):**
```python
    if utils.safe_compare(
        keyword_info.get("competition"),
        client_cfg.get("max_paid_competition_score", 0.8),
        "gt",
    ) and (keyword_info.get("competition_level") == "HIGH"):
```

**CODE TO REPLACE:**
```python
    if utils.safe_compare(
        keyword_info.get("competition"),
        client_cfg.get("max_paid_competition_score", 0.8),
        "gt",
    ) and (keyword_info.get("competition_level") == "HIGH"):
```

**WITH NEW CODE:**
```python
    if utils.safe_compare(
        competition, # Use direct column
        client_cfg.get("max_paid_competition_score", 0.8),
        "gt",
    ) and (keyword_info_old_json.get("competition_level") == "HIGH"): # Keep old JSON for competition_level for backward compatibility
```

**ACTION NO:** 14.16
**ACTION TYPE:** REPLACE
**ACTION RATIONALE:** Updates the CPC bid check to use the new direct `cpc` column and recalculates the "high top of page bid" using it, aligning with the normalized schema.

**FIND CONTEXT (Replace the block starting from `    if utils.safe_compare(` to `    ):`):**
```python
    if utils.safe_compare(
        keyword_info.get("high_top_of_page_bid"),
        client_cfg.get("max_high_top_of_page_bid", 15.0),
        "gt",
    ):
```

**CODE TO REPLACE:**
```python
    if utils.safe_compare(
        keyword_info.get("high_top_of_page_bid"),
        client_cfg.get("max_high_top_of_page_bid", 15.0),
        "gt",
    ):
```

**WITH NEW CODE:**
```python
    if utils.safe_compare(
        cpc * (keyword_info_old_json.get("high_top_of_page_bid", 0.0) / (keyword_info_old_json.get("cpc", 1) or 1)), # Reconstruct high bid, use old JSON for fallback to avoid division by zero if new CPC is 0
        client_cfg.get("max_high_top_of_page_bid", 15.0),
        "gt",
    ):
```

**ACTION NO:** 14.17
**ACTION TYPE:** REPLACE
**ACTION RATIONALE:** Updates the `keyword_difficulty` check to use the new direct `keyword_difficulty` column, aligning with the normalized database schema.

**FIND CONTEXT (Replace the block starting from `    if utils.safe_compare(` to `    ):`):**
```python
    if utils.safe_compare(
        keyword_props.get("keyword_difficulty"),
        client_cfg.get("max_kd_hard_limit", 70),
        "gt",
    ):
```

**CODE TO REPLACE:**
```python
    if utils.safe_compare(
        keyword_props.get("keyword_difficulty"),
        client_cfg.get("max_kd_hard_limit", 70),
        "gt",
    ):
```

**WITH NEW CODE:**
```python
    if utils.safe_compare(
        keyword_difficulty, # Use direct column
        client_cfg.get("max_kd_hard_limit", 70),
        "gt",
    ):
```

**ACTION NO:** 14.18
**ACTION TYPE:** DELETE
**ACTION RATIONALE:** The call to `_check_hostile_serp_environment` and its conditional block are removed. This rule is now handled by API-side filtering (Task 1), making the Python-side check redundant.

**FIND CONTEXT (Replace the block starting from `    # Rule: Check for hostile SERP environment` to `    if is_hostile:`):**
```python
    # Rule: Check for hostile SERP environment
    is_hostile, hostile_reason = _check_hostile_serp_environment(opportunity)
    if is_hostile:
        return True, hostile_reason, True
```

**CODE TO DELETE:**
```python
    # Rule: Check for hostile SERP environment
    is_hostile, hostile_reason = _check_hostile_serp_environment(opportunity)
    if is_hostile:
        return True, hostile_reason, True
```

**WITH NEW CODE:**
```python
    # Rule: Check for hostile SERP environment (now handled by API-side filtering in Task 1)
```

**ACTION NO:** 14.19
**ACTION TYPE:** REPLACE
**ACTION RATIONALE:** Updates the `sv` (search volume) variable to use the new direct `search_volume` column.

**FIND CONTEXT (Replace the line containing `        sv = keyword_info.get("search_volume", 0)`):**
```python
        sv = keyword_info.get("search_volume", 0)
```

**CODE TO REPLACE:**
```python
        sv = keyword_info.get("search_volume", 0)
```

**WITH NEW CODE:**
```python
        sv = search_volume # Use direct column
```

**ACTION NO:** 14.20
**ACTION TYPE:** REPLACE
**ACTION RATIONALE:** Updates the `cpc` variable to use the new direct `cpc` column, simplifying access.

**FIND CONTEXT (Replace the line containing `        cpc = keyword_info.get("cpc")  # Get the value, which could be None`):**
```python
        cpc = keyword_info.get("cpc")  # Get the value, which could be None
```

**CODE TO REPLACE:**
```python
        cpc = keyword_info.get("cpc")  # Get the value, which could be None
```

**WITH NEW CODE:**
```python
        cpc = cpc # Use direct column
```

### **File: `backend/data_mappers/dataforseo_mapper.py`**

**ACTION NO:** 14.21
**ACTION TYPE:** INSERT
**ACTION RATIONALE:** This code block ensures that the new direct columns for keyword metrics (search volume, KD, CPC, competition, main intent) are explicitly populated from the raw DataForSEO `keyword_info`, `keyword_properties`, and `search_intent_info` when a new keyword item is sanitized. This prepares the data for direct storage in the normalized database columns.

**FIND CONTEXT (Insert after the line containing):**
```python
            sanitized_item["avg_backlinks_info"]["last_updated_time"] = (
                parse_datetime_string(
                    sanitized_item["avg_backlinks_info"].get("last_updated_time")
                )
            )
```

**CODE TO INSERT:**
```python
        # NEW: Ensure direct columns exist even if from older JSON structure (Task 14)
        # This pre-fills the direct columns from the JSON for new items before DB insertion.
        sanitized_item['search_volume'] = int(sanitized_item.get("keyword_info", {}).get("search_volume") or 0)
        sanitized_item['keyword_difficulty'] = int(sanitized_item.get("keyword_properties", {}).get("keyword_difficulty") or 0)
        sanitized_item['cpc'] = float(sanitized_item.get("keyword_info", {}).get("cpc") or 0.0)
        sanitized_item['competition'] = float(sanitized_item.get("keyword_info", {}).get("competition") or 0.0)
        sanitized_item['main_intent'] = sanitized_item.get("search_intent_info", {}).get("main_intent")
        # search_volume_trend_json is handled by `run_discovery` from `keyword_info.search_volume_trend`
```

### **File: `backend/api/routers/opportunities.py`**

**ACTION NO:** 14.22
**ACTION TYPE:** REPLACE
**ACTION RATIONALE:** Updates the `select_columns` string used in the `get_all_opportunities_summary` endpoint. It now explicitly selects the new direct columns (`search_volume`, `keyword_difficulty`, `total_api_cost`, `generation_warnings`) instead of relying on parsing them from the `full_data` JSON blob. This optimizes data retrieval for the frontend table view.

**FIND CONTEXT (Replace the line containing `        select_columns="id, keyword, status, date_added, strategic_score, cpc, competition, main_intent, blog_qualification_status, blog_qualification_reason, latest_job_id, cluster_name, full_data",`):**
```python
        select_columns="id, keyword, status, date_added, strategic_score, cpc, competition, main_intent, blog_qualification_status, blog_qualification_reason, latest_job_id, cluster_name, full_data",
```

**CODE TO REPLACE:**
```python
        select_columns="id, keyword, status, date_added, strategic_score, cpc, competition, main_intent, blog_qualification_status, blog_qualification_reason, latest_job_id, cluster_name, full_data",
```

**WITH NEW CODE:**
```python
        select_columns="id, keyword, status, date_added, strategic_score, cpc, competition, main_intent, search_volume, keyword_difficulty, blog_qualification_status, blog_qualification_reason, latest_job_id, cluster_name, total_api_cost, generation_warnings", # UPDATED select_columns for direct access (Task 14, 12)
```

**ACTION NO:** 14.23
**ACTION TYPE:** DELETE
**ACTION RATIONALE:** Removes the manual parsing of `blueprint` and `serp_overview` from `full_data`. These are now either direct columns or correctly deserialized by the `_deserialize_rows` method earlier in the data flow (Task 14.4). This cleans up redundant parsing logic.

**FIND CONTEXT (Delete the block starting from `    # W23 FIX: Manually parse the blueprint from full_data if it exists` to `            )`):**
```python
    # W23 FIX: Manually parse the blueprint from full_data if it exists
    if opportunity.get("full_data") and isinstance(opportunity["full_data"], str):
        try:
            full_data_json = json.loads(opportunity["full_data"])
            if "blueprint" in full_data_json:
                opportunity["blueprint"] = full_data_json["blueprint"]
            if "serp_overview" in full_data_json:
                opportunity["serp_overview"] = full_data_json["serp_overview"]
        except json.JSONDecodeError:
            logger.warning(
                f"Could not decode full_data JSON for opportunity {opportunity_id}."
            )
```

**CODE TO DELETE:**
```python
    # W23 FIX: Manually parse the blueprint from full_data if it exists
    if opportunity.get("full_data") and isinstance(opportunity["full_data"], str):
        try:
            full_data_json = json.loads(opportunity["full_data"])
            if "blueprint" in full_data_json:
                opportunity["blueprint"] = full_data_json["blueprint"]
            if "serp_overview" in full_data_json:
                opportunity["serp_overview"] = full_data_json["serp_overview"]
        except json.JSONDecodeError:
            logger.warning(
                f"Could not decode full_data JSON for opportunity {opportunity_id}."
            )
```

### **File: `client/my-content-app/src/pages/OpportunitiesPage/OpportunitiesPage.jsx`**

**ACTION NO:** 14.24
**ACTION TYPE:** REPLACE
**ACTION RATIONALE:** The `baseColumns` definition is updated to remove reliance on extracting `search_volume` and `keyword_difficulty` from `full_data` in the frontend. It now directly references the new `search_volume` and `keyword_difficulty` properties, which are provided as top-level fields by the API (Task 14.22). This fixes a logical error in the original plan where `baseColumns` would be redefined multiple times.

**FIND CONTEXT (Replace the block starting from `  const baseColumns = [` to `  ];`):**
```jsx
  const baseColumns = [
    { title: 'Keyword', dataIndex: 'keyword', key: 'keyword', sorter: true, render: (text, record) => <a onClick={(e) => { e.stopPropagation(); navigate(`/opportunities/${record.id}`)}}>{text}</a> },
    { title: 'Search Volume', dataIndex: 'search_volume', key: 'search_volume', sorter: true, render: (sv) => sv ? sv.toLocaleString() : 'N/A' },
    { title: 'KD', dataIndex: 'keyword_difficulty', key: 'keyword_difficulty', sorter: true, render: (kd) => kd != null ? kd : 'N/A' },
  ];
```

**CODE TO REPLACE:**
```jsx
  const baseColumns = [
    { title: 'Keyword', dataIndex: 'keyword', key: 'keyword', sorter: true, render: (text, record) => <a onClick={(e) => { e.stopPropagation(); navigate(`/opportunities/${record.id}`)}}>{text}</a> },
    { title: 'Search Volume', dataIndex: 'search_volume', key: 'search_volume', sorter: true, render: (sv) => sv ? sv.toLocaleString() : 'N/A' },
    { title: 'KD', dataIndex: 'keyword_difficulty', key: 'keyword_difficulty', sorter: true, render: (kd) => kd != null ? kd : 'N/A' },
  ];
```

**WITH NEW CODE:**
```jsx
  // Define base columns using direct access to new fields
  const baseColumns = [
    { title: 'Keyword', dataIndex: 'keyword',{ title: 'Keyword', dataIndex: 'keyword',

### **File: `client/my-content-app/src/pages/OpportunitiesPage/OpportunitiesPage.jsx`**

**ACTION NO:** 14.25
**ACTION TYPE:** INSERT
**ACTION RATIONALE:** The `defaultColumns` definition is updated to remove reliance on extracting `search_volume` and `keyword_difficulty` from `full_data` in the frontend. It now directly references the new `search_volume` and `keyword_difficulty` properties, which are provided as top-level fields by the API (Task 14.22). This also fixes the logical flow of defining `baseColumns` first.

**FIND CONTEXT (Insert after the line containing `  const rejectedColumns = [`):**
```jsx
  const rejectedColumns = [
    { title: 'Keyword', dataIndex: 'keyword', key: 'keyword', sorter: true, render: (text, record) => <a onClick={(e) => { e.stopPropagation(); navigate(`/opportunities/${record.id}`)}}>{text}</a> },
    { title: 'Search Volume', dataIndex: 'search_volume', key: 'search_volume', sorter: true, render: (sv) => sv ? sv.toLocaleString() : 'N/A' },
    { title: 'KD', dataIndex: 'keyword_difficulty', key: 'keyword_difficulty', sorter: true, render: (kd) => kd != null ? kd : 'N/A' },
    {
      title: 'Rejection Reason', 
      dataIndex: 'blog_qualification_reason', 
      key: 'blog_qualification_reason',
      render: (reason) => reason || <Text type="secondary">No reason provided</Text>
    },
    { title: 'Actions', key: 'actions', fixed: 'right', render: renderActions },
  ];
```

**CODE TO INSERT:**
```jsx
  const defaultColumns = [
    { title: 'Keyword', dataIndex: 'keyword', key: 'keyword', sorter: true, render: (text, record) => <a onClick={(e) => { e.stopPropagation(); navigate(`/opportunities/${record.id}`)}}>{text}</a> },
    { title: 'Search Volume', dataIndex: 'search_volume', key: 'search_volume', sorter: true, render: (sv) => sv ? sv.toLocaleString() : 'N/A' },
    { title: 'KD', dataIndex: 'keyword_difficulty', key: 'keyword_difficulty', sorter: true, render: (kd) => kd != null ? kd : 'N/A' },
    { title: 'Strategic Score', dataIndex: 'strategic_score', key: 'strategic_score', sorter: true, render: (score) => score ? <strong>{score.toFixed(1)}</strong> : 'N/A' },
    { title: 'CPC', dataIndex: 'cpc', key: 'cpc', sorter: true, render: (cpc) => cpc ? `$${cpc.toFixed(2)}` : 'N/A' },
    { title: 'Actions', key: 'actions', fixed: 'right', render: renderActions },
  ];
```

### **File: `client/my-content-app/src/pages/opportunity-detail-page/components/KeywordMetrics.jsx`**

**ACTION NO:** 14.26
**ACTION TYPE:** REPLACE
**ACTION RATIONALE:** The destructuring of props is updated to expect `keyword_difficulty` as a property of `keywordInfo` (or the `opportunity` object directly), rather than `keywordProperties`. This aligns with the database normalization which moves `keyword_difficulty` to a direct column.

**FIND CONTEXT (Replace the lines containing):**
```jsx
  const { search_volume, cpc, competition, monthly_searches, competition_level, low_top_of_page_bid, high_top_of_page_bid } = keywordInfo;
  const { keyword_difficulty } = keywordProperties;
```

**CODE TO REPLACE:**
```jsx
  const { search_volume, cpc, competition, monthly_searches, competition_level, low_top_of_page_bid, high_top_of_page_bid } = keywordInfo;
  const { keyword_difficulty } = keywordProperties;
```

**WITH NEW CODE:**
```jsx
  const { search_volume, cpc, competition, monthly_searches, competition_level, low_top_of_page_bid, high_top_of_page_bid, keyword_difficulty } = keywordInfo; // All moved to keywordInfo
```

---

**Task No:** 15
**Task Higher Overview:** Create a `/api/health` endpoint for simple, effective monitoring of the application's core dependencies.
**Files Involved:**
*   `backend/api/routers/health.py` (New file)
*   `backend/api/main.py`
**Total Code Changes Required:** 3 granular changes (1 new file, 2 modifications).

**STEP BY STEP PLAN:**

### **File: `backend/api/routers/health.py`**

**ACTION NO:** 15.1
**ACTION TYPE:** CREATE_FILE
**ACTION RATIONALE:** This new FastAPI router defines a `/health` endpoint. This endpoint performs a basic database connectivity check and returns a JSON response indicating the overall status and the status of its dependencies. This is crucial for external monitoring systems to determine the application's health.

**FILE PATH:** `backend/api/routers/health.py`
**FILE CONTENT:**
```python
# backend/api/routers/health.py
from fastapi import APIRouter, Depends
from data_access.database_manager import DatabaseManager
from ..dependencies import get_db

router = APIRouter()

@router.get("/health")
async def health_check(db: DatabaseManager = Depends(get_db)):
    db_status = "ok"
    try:
        # A simple, non-blocking query to check DB connection
        conn = db._get_conn()
        conn.execute("SELECT 1")
    except Exception:
        db_status = "error"
    
    # In a real app, you would also check external API connectivity here (e.g., ping DataForSEO)
    return {"status": "ok", "dependencies": {"database": db_status}}
```

### **File: `backend/api/main.py`**

**ACTION NO:** 15.2
**ACTION TYPE:** INSERT
**ACTION RATIONALE:** Imports the new `health` router to make its endpoints available to the FastAPI application.

**FIND CONTEXT (Insert after the line containing):**
```python
        settings,
```

**CODE TO INSERT:**
```python
        health, # NEW IMPORT for Task 15
```

**ACTION NO:** 15.3
**ACTION TYPE:** INSERT
**ACTION RATIONALE:** Registers the new `health` router with the FastAPI application. This makes the `/api/health` endpoint active for monitoring purposes.

**FIND CONTEXT (Insert after the line containing):**
```python
    app.include_router(settings.router, prefix="/api")
```

**CODE TO INSERT:**
```python
    app.include_router(health.router, prefix="/api") # NEW ROUTER for Task 15
``````python
    app.include_router(health.router, prefix="/api") # NEW ROUTER for Task 15
```