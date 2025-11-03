# Step 6: Strategic Blueprint Assembly and Outline Generation

## Mandate 12 (Strategic Flaw)
*   **Analysis:** The derivation of target word count is analyzed. `BriefAssembler.py` calculates the final `target_word_count` by multiplying a fixed base word count (default 1500) by a hardcoded multiplier (e.g., `1.2`, `1.5`). This misses the opportunity to use the dynamically calculated `average_word_count` of the top-ranking competitors (data calculated in Step 4/Metric Analyzer) as the strategic basis for length, leading to arbitrary content length targets.

## Mandate 13 (Real-World Issue/UX)
*   **Analysis:** The manual outline customization feature is audited. `ContentBlueprint.jsx` allows users to manually add questions from the PAA list to the outline. This feature is limited to only adding to the 'Frequently Asked Questions' H2, restricting the user's ability to strategically integrate high-priority PAA questions directly into early sections of the article body.

## Mandate 14 (Missed Opportunity)
*   **Analysis:** There is a missing strategic integration of authoritative sources. Step 5's SERP synthesis identifies `ai_overview_sources`. Step 6/7 fails to explicitly mandate that the AI cite or reference these sources within the final content (Step 8), only offering generalized tactical guidance.
