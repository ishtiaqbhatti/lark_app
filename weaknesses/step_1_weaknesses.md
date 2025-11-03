# Step 1: Discovery Run and Keyword Expansion Weaknesses

1.  **Limited UI Filtering:** The discovery form in `DiscoveryForm.jsx` only allows filtering by four basic fields (SV, KD, Competition, Intent), preventing users from leveraging more advanced filtering capabilities.
2.  **Inability to Use Advanced Filters:** Users cannot access the full strategic power of the DataForSEO API's filtering options through the UI.
3.  **Reduced Strategic Power:** The limited filtering options significantly reduce the user's ability to perform targeted and strategic keyword discovery.
4.  **Brittle Filter Path Logic:** The UI hardcodes a `filterPathPrefix = 'keyword_data.'`, which is only correct for the 'related_keywords' discovery mode.
5.  **Risk of Silent API Errors:** The incorrect filter path logic for modes other than 'related_keywords' can lead to silent API errors that are not surfaced to the user.
6.  **Incomplete Discovery Results:** Due to the faulty filter path, discovery modes like 'keyword_ideas' and 'keyword_suggestions' may return incomplete or unfiltered results.
7.  **Omission of Clickstream Data:** The workflow fails to utilize the `include_clickstream_data` parameter supported by the `DiscoveryCostParams` model.
8.  **Missed Qualification Opportunity:** By not using clickstream data, the system misses a key opportunity to qualify keywords based on real user behavior and engagement metrics.
9.  **Less Accurate Initial Scoring:** The initial Phase 1 scoring is less accurate because it lacks the rich context provided by clickstream data.
10. **Underutilization of Data Models:** The system does not make full use of the available data models, such as `DiscoveryCostParams`, limiting its strategic depth.
