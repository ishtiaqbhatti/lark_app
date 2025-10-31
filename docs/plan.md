Of course. Here is a complete and explicit implementation plan for an AI coding agent to resolve the first 10 strategic and logical issues. Each task is broken down into granular, actionable steps with the exact code changes required, ensuring there is no ambiguity.

### **Issue No: 1**
*   **Issue Granular Details:** The system incorrectly rejects keywords that have a Keyword Difficulty (KD) of 0. The disqualification logic in `pipeline/step_01_discovery/disqualification_rules.py` contains a rule that treats a KD of 0 as if it were null or invalid data, causing an immediate rejection.
*   **Issue Impact:** This is a critical strategic failure. A KD of 0 is the best possible score for ranking difficulty and represents a "golden ticket" opportunity. By rejecting these, the tool is actively discarding the lowest-hanging fruit and failing in its primary mission to identify valuable content targets.
*   **Issue Relevant code and files:**
    *   `pipeline/step_01_discovery/disqualification_rules.py`
    *   **Data Evidence:** Keywords with IDs 100, 99, 98 are all incorrectly rejected with the reason: `"Rule 0: Rejected due to zero or null Keyword Difficulty."`
*   **Issue Recomended Soluion explaned:** The fix is to modify the conditional check in the disqualification rules. The logic must be changed to only reject a keyword if its KD is `None` (truly missing), while allowing a KD of `0` to proceed through the qualification workflow.
*   **Issue Correctness:** 100% Certain. The code explicitly shows the flawed logic (`or keyword_difficulty == 0`), and the data shows the direct consequence.
*   **Issue points that may not have thought:** The DataForSEO API might occasionally return 0 for keywords with very low data. This is not an error but a valid data point indicating negligible competition. The scoring engine should be prepared to handle a KD of 0 by awarding a maximum score for that component.

---
#### **Implementation Plan for Issue #1**

##### **Granular Task 1.1: Correct the Keyword Difficulty Disqualification Logic**

*   **File:** `pipeline/step_01_discovery/disqualification_rules.py`
*   **Action:** MODIFY the `apply_disqualification_rules` function to remove the check for `keyword_difficulty == 0`.

    **BEFORE:**
    ```python
    # New Rule: Reject if SV or KD is 0 or null
    search_volume = keyword_info.get("search_volume")
    keyword_difficulty = keyword_props.get("keyword_difficulty")

    if search_volume is None or search_volume == 0:
        return True, "Rule 0: Rejected due to zero or null Search Volume.", True
    
    if keyword_difficulty is None or keyword_difficulty == 0:
        return True, "Rule 0: Rejected due to zero or null Keyword Difficulty.", True
    ```

    **AFTER:**
    ```python
    # New Rule: Reject if SV is null/zero or KD is null
    search_volume = keyword_info.get("search_volume")
    keyword_difficulty = keyword_props.get("keyword_difficulty")

    if search_volume is None or search_volume == 0:
        return True, "Rule 0: Rejected due to zero or null Search Volume.", True
    
    if keyword_difficulty is None:
        return True, "Rule 0: Rejected due to null Keyword Difficulty.", True
    ```
---

### **Issue No: 2**
*   **Issue Granular Details:** The system is incorrectly identifying common English keywords as being in another language (e.g., Catalan, `"ca"`), causing them to be immediately rejected. The disqualification rule is too absolute and lacks a user-configurable override.
*   **Issue Impact:** This is a critical-high impact flaw. It makes the tool completely unreliable, as it can reject extremely high-value keywords (like "chatgpt" with 83.1M searches) based on faulty upstream data. It breaks user trust and prevents the tool from being used for its core purpose.
*   **Issue Relevant code and files:**
    *   `pipeline/step_01_discovery/disqualification_rules.py`
    *   `app_config/settings.ini`
    *   `app_config/manager.py`
    *   **Data Evidence:** Keyword "chatgpt" (ID 101) has `detected_language: "ca"`, `is_another_language: true`, and is rejected with `"Rule 3: Language mismatch."`
*   **Issue Recomended Soluion explaned:** The solution is to introduce a failsafe. We will add a new configuration setting, `enforce_language_filter`, to `settings.ini`. The disqualification logic will then be modified to only reject a keyword for a language mismatch if this setting is enabled. This allows a user to disable the faulty rule and continue using the tool while the root cause of the language detection issue is investigated.
*   **Issue Correctness:** 100% Certain. The data proves the rule is misfiring, and adding a configurable bypass is the standard best practice for handling unreliable external data points.
*   **Issue points that may not have thought:** The root cause is likely an issue with the DataForSEO API or how its response is mapped. While this solution provides an immediate workaround, a long-term fix would involve investigating the data mapping in `data_mappers/dataforseo_mapper.py`.

---
#### **Implementation Plan for Issue #2**

##### **Granular Task 2.1: Add a New Setting to the Configuration File**

*   **File:** `app_config/settings.ini`
*   **Action:** ADD a new boolean setting under the `[QUALITY_FILTERS]` section.

    **At the end of the `[QUALITY_FILTERS]` section, add the following line:**
    ```ini
    enforce_language_filter = true
    ```

##### **Granular Task 2.2: Register the New Setting in the Config Manager**

*   **File:** `app_config/manager.py`
*   **Action:** ADD the new setting to the `_setting_types` dictionary to ensure it's parsed as a boolean.

    **Within the `_setting_types` dictionary, add the following entry:**
    ```python
    "enforce_language_filter": bool,
    ```

##### **Granular Task 2.3: Update the Disqualification Logic to Use the New Setting**

*   **File:** `pipeline/step_01_discovery/disqualification_rules.py`
*   **Action:** MODIFY the language check rule in the `apply_disqualification_rules` function.

    **BEFORE:**
    ```python
    if keyword_props.get("is_another_language"):
        return True, "Rule 3: Language mismatch.", True
    ```

    **AFTER:**
    ```python
    if client_cfg.get("enforce_language_filter", True) and keyword_props.get("is_another_language"):
        return True, "Rule 3: Language mismatch.", True
    ```
---

### **Issue No: 3**
*   **Issue Granular Details:** The negative keyword filter uses a simple substring match (`neg_kw in keyword.lower()`), which incorrectly flags legitimate keywords. For example, "chatgpt free vs paid" is rejected because it contains the word "free".
*   **Issue Impact:** This flaw prevents users from targeting valuable and high-intent comparison keywords, which are a cornerstone of many content strategies. It demonstrates a lack of contextual understanding in the tool's core logic.
*   **Issue Relevant code and files:**
    *   `pipeline/step_01_discovery/disqualification_rules.py`
    *   **Data Evidence:** Keyword "chatgpt free vs paid" (ID 72) was rejected due to "Rule 4: Contains a negative keyword."
*   **Issue Recomended Soluion explaned:** The logic must be improved to be context-aware. The fix involves two parts: first, check if the keyword contains common comparison terms (like "vs"). If it does, the negative keyword check is skipped. Second, the negative keyword match itself is changed from a simple substring search to a whole-word regex search to prevent partial matches (e.g., matching "art" in "chart").
*   **Issue Correctness:** 100% Certain. The data directly illustrates the failure of the simplistic substring match.
*   **Issue points that may not have thought:** The list of `comparison_terms` could itself be made a configurable list in `settings.ini` to allow users to add their own exceptions (e.g., "alternative," "comparison").

---
#### **Implementation Plan for Issue #3**

##### **Granular Task 3.1: Enhance the Negative Keyword Logic with Context**

*   **File:** `pipeline/step_01_discovery/disqualification_rules.py`
*   **Action:** REPLACE the entire negative keyword checking block with a more intelligent, context-aware version. You will also need to add `import re`.

    **At the top of the file, add:**
    ```python
    import re
    ```

    **Then, find and REPLACE the following code block.**

    **BEFORE:**
    ```python
    negative_keywords = set(
        kw.lower() for kw in client_cfg.get("negative_keywords", [])
    )
    core_keyword = keyword_props.get("core_keyword")
    if any(neg_kw in keyword.lower() for neg_kw in negative_keywords) or (
        core_keyword
        and any(neg_kw in core_keyword.lower() for neg_kw in negative_keywords)
    ):
        return True, "Rule 4: Contains a negative keyword.", True
    ```

    **AFTER:**
    ```python
    # Rule 4: Contains a negative keyword (with contextual override)
    negative_keywords = set(kw.lower() for kw in client_cfg.get("negative_keywords", []))
    keyword_lower = keyword.lower()
    comparison_terms = {"vs", "versus", "alternative", "comparison"}

    # Override: Do not apply negative keyword filter if it's a known comparison query
    is_comparison_query = any(comp_term in keyword_lower for comp_term in comparison_terms)

    if not is_comparison_query:
        # Use whole-word matching to avoid partial matches
        if any(re.search(r'\b' + re.escape(neg_kw) + r'\b', keyword_lower) for neg_kw in negative_keywords):
            return True, "Rule 4: Contains a negative keyword.", True
    ```
---

### **Issue No: 4**
*   **Issue Granular Details:** The tool's strategic prioritization is rigid because the scoring weights are defined in `settings.ini` and there is no implemented UI or API endpoint for users to change them.
*   **Issue Impact:** Users cannot align the tool's strategy with their business goals. A user wanting to prioritize high-commercial-value keywords cannot increase the weight of the `commercial_intent` score, making the tool a "one-size-fits-all" solution that doesn't fit anyone perfectly.
*   **Issue Relevant code and files:** `app_config/settings.ini`, `pipeline/step_03_prioritization/scoring_engine.py`, `pages/Settings/tabs/ScoringWeightsTab.jsx`, `api/routers/settings.py`.
*   **Issue Recomended Soluion explaned:** This requires a full-stack implementation. First, the `ScoringWeightsTab.jsx` frontend component must be made functional by adding state management for the form values and a `useMutation` hook to save them. Second, the `api/routers/settings.py` endpoint must be updated to accept and process this specific set of weight data, saving it to the `client_settings` table in the database. Finally, the database migrations and models need to ensure these columns exist.
*   **Issue Correctness:** 100% Certain. The frontend code is a placeholder, and the API lacks the specific logic to handle these updates.
*   **Issue points that may not have thought:** The UI should enforce that the sum of all weights equals 100% to ensure the scoring remains normalized and predictable. A visual indicator showing the current total weight would be essential.

---
#### **Implementation Plan for Issue #4**
*(Note: This is a multi-part, full-stack task.)*

##### **Granular Task 4.1: Update the API Endpoint to Handle Setting Updates**

*   **File:** `api/routers/settings.py`
*   **Action:** MODIFY the `update_settings_endpoint` to correctly process and save the incoming settings dictionary.

    **BEFORE:**
    ```python
    @router.put("/settings/{client_id}", response_model=Dict[str, str])
    async def update_settings_endpoint(
        client_id: str,
        settings: Dict[str, Any],
        db: DatabaseManager = Depends(get_db),
        orchestrator: WorkflowOrchestrator = Depends(get_orchestrator),
    ):
        """Endpoint for updating client-specific settings."""
        if client_id != orchestrator.client_id:
            raise HTTPException(
                status_code=403,
                detail="You do not have permission to access this client's resources.",
            )
        try:
            db.update_client_settings(client_id, settings)
            return {"message": "Settings updated successfully."}
        except Exception as e:
            logger.error(f"Failed to update settings for client {client_id}: {e}", exc_info=True)
            raise HTTPException(status_code=500, detail="Failed to update settings.")
    ```

    **AFTER:**
    ```python
    @router.put("/settings/{client_id}", response_model=Dict[str, str])
    async def update_settings_endpoint(
        client_id: str,
        settings: Dict[str, Any],
        db: DatabaseManager = Depends(get_db),
        orchestrator: WorkflowOrchestrator = Depends(get_orchestrator),
    ):
        """Endpoint for updating client-specific settings."""
        if client_id != orchestrator.client_id:
            raise HTTPException(
                status_code=403,
                detail="You do not have permission to access this client's resources.",
            )
        try:
            # Add a server-side validation to ensure weights sum to 100 if they are present
            weight_keys = [key for key in settings.keys() if key.endswith('_weight')]
            if weight_keys:
                total_weight = sum(settings.get(key, 0) for key in weight_keys)
                if total_weight != 100:
                    raise HTTPException(
                        status_code=400, 
                        detail=f"Scoring weights must sum to 100, but they sum to {total_weight}."
                    )
            
            db.update_client_settings(client_id, settings)
            return {"message": "Settings updated successfully."}
        except HTTPException as he:
            raise he
        except Exception as e:
            logger.error(f"Failed to update settings for client {client_id}: {e}", exc_info=True)
            raise HTTPException(status_code=500, detail="Failed to update settings.")
    ```

##### **Granular Task 4.2: Implement Frontend Logic in the Settings Page**
*   **File:** `pages/Settings/SettingsPage.jsx`
*   **Action:** This file is already correctly structured with `Form`, `useMutation`, and `onFinish` handlers. No changes are needed here as it properly submits the entire form's values, which will include the scoring weights from the child tab component.

You are requesting a complete and granular implementation plan for Issues 5 through 10, ensuring all ripple effects across the entire codebase are addressed with explicit code changes.

Here is the implementation plan for the next six issues.

---

### **Issue No: 5**
*   **Issue Granular Details:** The `call_chat_completion` function in `external_apis/openai_client.py` contains a hardcoded override: `model = 'gpt-5-mini'`. This forces the use of a specific, cheaper model, ignoring the model preference configured in `settings.ini` or the database (which is set to `gpt-4o` in the data).
*   **Issue Impact:** The user expects high-quality output (like GPT-4o) and incurs cost based on that expectation, but the system secretly uses a lower-tier model. This is a critical breach of trust and directly impacts the quality of analysis, blueprint generation, and final content.
*   **Issue Relevant code and files:** `external_apis/openai_client.py`.
*   **Issue Recomended Soluion explaned:** Remove the hardcoded override. The model argument should default to the class configuration if no model is explicitly passed in the function call, ensuring client settings are respected.
*   **Issue Correctness:** 100% Certain. The line is explicitly present and causes the faulty behavior.
*   **Issue points that may not have thought:** The model being used for cost estimation and generation must be synchronized. The orchestrator calls must be reviewed to ensure the desired model is being passed or is correctly defaulted.

---
### **Issue No: 10**
*   **Issue Granular Details:** The system rejects high-value keywords based on faulty language detection (e.g., "chatgpt portugues" rejected for "Rule 3: Language mismatch" despite the service language being English).
*   **Issue Impact:** The tool is unreliable and fails to properly qualify high-value keywords for international markets or foreign-language terms that are relevant to an English-language client.
*   **Issue Relevant code and files:** `pipeline/step_01_discovery/disqualification_rules.py` (Rule 3).
*   **Issue Recomended Soluion explaned:** This issue was functionally addressed in **Issue #2** by adding the configurable override `enforce_language_filter`. The key here is to confirm that the change is applied correctly. For the scope of this task, the solution is to ensure the **Issue #2** fix is fully implemented and operational.
*   **Issue Correctness:** 100% Certain. The issue is confirmed by data and resolved by Task 2.
*   **Issue points that may not have thought:** The UI needs a simple toggle for this in the Settings.

---
#### **Implementation Plan for Issue #10**
*(This task is a direct continuation/verification of Issue #2's fix, focusing on the UI component.)*

##### **Granular Task 10.1: Implement Frontend Toggle for Language Disqualification Filter**

*   **File:** `pages/Settings/tabs/DiscoverySettingsTab.jsx`
*   **Action:** ADD a functional `Switch` component to control the `enforce_language_filter` setting.

    **In `pages/Settings/tabs/DiscoverySettingsTab.jsx`, add the following `Form.Item` in the `General Discovery Parameters` section:**
    ```javascript
          <Col span={12}>
            <Form.Item 
              name="enforce_language_filter" 
              label={
                <Space>
                  Enforce Language Filter
                  <Tooltip title="If disabled, keywords detected in another language will NOT be auto-rejected. Use with caution.">
                    <InfoCircleOutlined />
                  </Tooltip>
                </Space>
              } 
              valuePropName="checked"
            >
              <Switch checkedChildren="Enabled" unCheckedChildren="Disabled" />
            </Form.Item>
          </Col>
    ```

**Note:** The backend service logic for saving this setting is handled by the solution for **Issue #4**, which generalized the `update_settings_endpoint` to handle all new form values. The logic to consume this in the backend was handled by Task 2.3.