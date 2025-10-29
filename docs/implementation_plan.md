# Implementation Plan: Discovery Process Enhancement

This document outlines a phased implementation plan to address the weaknesses and capitalize on the missed opportunities identified in `discovery_analysis.md` and validated in `critique_of_analysis.md`. The plan is divided into three phases, prioritizing foundational backend changes, followed by significant UI/UX improvements, and concluding with advanced feature development.

---

## Phase 1: Backend Refactoring & Foundational Improvements

**Goal:** Strengthen the backend, improve efficiency, and lay the groundwork for future UI enhancements.

### Task 1.1: Optimize API Usage & Efficiency

*   **Action:** Modify the backend to handle API interactions more intelligently.
*   **Files to Modify:**
    *   `lark_app/backend/pipeline/step_01_discovery/run_discovery.py`:
        *   Integrate negative keywords into the initial API filter using `not_match` or `not_regex` to avoid post-fetch filtering.
    *   `lark_app/backend/external_apis/dataforseo_client_v2.py`:
        *   Refactor the `get_keyword_ideas` method to use the `offset_token` for pagination as recommended by the API docs, replacing the current `discovery_max_pages` loop.
    *   `lark_app/backend/pipeline/step_01_discovery/keyword_discovery/expander.py`:
        *   Remove the brittle logic that adds/removes the `keyword_data.` prefix. Instead, pass the appropriate filter structure directly based on the `discovery_mode`.

### Task 1.2: Decouple and Expose Run Parameters

*   **Action:** Move hardcoded settings to the API layer and prepare for user configuration.
*   **Files to Modify:**
    *   `lark_app/backend/api/routers/discovery.py`:
        *   Modify the `run_discovery_job` endpoint to accept new optional parameters from the request body: `order_by`, `disqualification_rules_override` (a dictionary of values), and `include_clickstream_data`.
    *   `lark_app/backend/pipeline/step_01_discovery/run_discovery.py`:
        *   Update the function signature to accept these new parameters.
        *   Pass `order_by` to the `KeywordExpander`.
        *   Merge the `disqualification_rules_override` dictionary with the base `client_cfg` before passing it to `apply_disqualification_rules`.
    *   `lark_app/backend/pipeline/step_01_discovery/disqualification_rules.py`:
        *   No changes needed immediately, as it already reads from the `client_cfg` dictionary which will now contain the user's overrides.

---

## Phase 2: User Interface & Control Enhancements

**Goal:** Empower the user with greater control over the discovery process and improve usability.

### Task 2.1: Implement Multi-Seed Keyword Input

*   **Action:** Upgrade the seed keyword input to accept multiple keywords.
*   **Files to Modify:**
    *   `lark_app/client/my-content-app/src/pages/DiscoveryPage/components/DiscoveryForm.jsx`:
        *   Replace the single `<Input />` for `keyword` with an `<Input.TextArea />` that accepts a list of keywords (one per line).
        *   Update the `onFinish` handler to split the text area value into an array of strings and pass it as `seed_keywords`.
        *   Update the `preCheckKeywords` logic to handle multiple keywords.

### Task 2.2: Integrate the Interactive Filter Builder

*   **Action:** Replace the static filter inputs with the existing but unused `FilterBuilder` component.
*   **Files to Modify:**
    *   `lark_app/client/my-content-app/src/pages/DiscoveryPage/components/DiscoveryForm.jsx`:
        *   Remove the hardcoded `InputNumber` and `Select` components for filters.
        *   Import and render the `FilterBuilder` component.
        *   Pass the `filtersData` from the `useDiscoveryFilters` hook to the `FilterBuilder`.
        *   In the `onFinish` handler, retrieve the filter array from the `FilterBuilder`'s state and pass it to the backend.

### Task 2.3: Add Sorting and Advanced Options UI

*   **Action:** Add UI elements for sorting, match types, and advanced data fetching.
*   **Files to Modify:**
    *   `lark_app/client/my-content-app/src/pages/DiscoveryPage/components/DiscoveryForm.jsx`:
        *   Add a `Select` component to allow the user to choose `order_by` fields (e.g., "Search Volume (desc)", "CPC (desc)").
        *   Make the `closely_variants` and `exact_match` switches context-aware, disabling them if the selected `discovery_modes` do not support them.
        *   Add a new `Switch` for `include_clickstream_data`, with a tooltip explaining the extra cost and benefits (audience data).

---

## Phase 3: Advanced Features & Strategic Insights

**Goal:** Introduce new features that provide deeper strategic value and analysis.

### Task 3.1: Implement Thematic Clustering

*   **Action:** Process and display keywords grouped by their API-provided categories.
*   **Files to Modify:**
    *   **Backend:**
        *   `lark_app/backend/services/opportunities_service.py` (or a new service): Create a function that processes a list of opportunities and groups them by the `categories` field.
        *   `lark_app/backend/api/routers/opportunities.py`: Add a new endpoint to return these clustered results for a given run ID.
    *   **Frontend:**
        *   `lark_app/client/my-content-app/src/pages/DiscoveryPage/components/RunDetailsPage.jsx`:
            *   Instead of a simple table, create a new view (e.g., a tab or a new page) that displays keywords in collapsible panels, where each panel header is a category name.

### Task 3.2: Utilize Core Keyword & Synonym Data

*   **Action:** Group keyword variations and provide a clearer view of topics.
*   **Files to Modify:**
    *   **Backend:**
        *   Update the opportunity processing logic to use the `core_keyword` field as a primary grouping key.
    *   **Frontend:**
        *   `lark_app/client/my-content-app/src/pages/DiscoveryPage/components/RunDetailsPage.jsx`:
            *   Modify the results table to be groupable. Display the `core_keyword` as the parent row, with all its synonyms/variations as expandable child rows.

### Task 3.3: Introduce a "Keyword Basket"

*   **Action:** Develop a new feature to allow users to collect and manage keywords across multiple runs.
*   **Files to Modify:**
    *   **Backend:**
        *   `lark_app/backend/data_access/models.py`: Create a new database model for the "Keyword Basket".
        *   `lark_app/backend/api/routers/`: Create a new router (`basket.py`) with endpoints to add/remove keywords from the basket and retrieve the current basket.
    *   **Frontend:**
        *   `lark_app/client/my-content-app/src/pages/DiscoveryPage/components/RunDetailsPage.jsx`: Add a checkbox to each row and a button to "Add selected to Basket".
        *   Create a new page/component to display the contents of the Keyword Basket, allowing for final review, analysis, and export.
