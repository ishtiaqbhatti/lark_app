# Step 1: Discovery Run and Keyword Expansion

## Mandate 1 (Real-World Issue)
*   **Analysis:** The front-end flexibility is limited. The core discovery form (`DiscoveryForm.jsx`) restricts users to only four basic filter fields (SV, KD, Competition, Intent), severely limiting the strategic power available via the DataForSEO API.

## Mandate 2 (Weakness/Flaw)
*   **Analysis:** The filter path assembly in the UI is brittle. `DiscoveryForm.jsx` constructs filters using a hardcoded `filterPathPrefix = 'keyword_data.'`. This logic is incorrect for all discovery modes except 'related_keywords', leading to potential silent API errors or non-comprehensive results for other modes.

## Mandate 3 (Missed Opportunity)
*   **Analysis:** High-value data is omitted from the discovery request. The `DiscoveryCostParams` model supports `include_clickstream_data`, but this rich data is not integrated into the Phase 1 scoring or filtering logic, missing a chance to qualify keywords based on real user behavior.
