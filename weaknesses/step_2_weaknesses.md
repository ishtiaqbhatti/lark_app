# Step 2: Initial Scoring, Filtering, and Deduping Weaknesses

1.  **Reliance on Stale Intent Data:** The system uses `search_intent_info.last_updated_time` which can be severely outdated, leading to inaccurate analysis.
2.  **Inaccurate Disqualification:** Strategic rejections based on outdated intent data (Rule 2 and 2b) are unreliable and may incorrectly disqualify valuable keywords.
3.  **Compromised Qualification Accuracy:** The use of stale data fundamentally compromises the accuracy of the initial keyword qualification process.
4.  **Inflexible Rejection of Zero SV Keywords:** **Rule 0** in `disqualification_rules.py` automatically rejects keywords with a search volume of 0.
5.  **Inflexible Rejection of Zero KD Keywords:** The same **Rule 0** also rejects keywords with a keyword difficulty of 0.
6.  **Elimination of Strategic Keywords:** The blanket rejection of zero SV/KD keywords eliminates potentially high-value long-tail, emerging, or new market keywords.
7.  **Lack of Bulk Override Functionality:** The `RunDetailsPage.jsx` only supports overriding disqualifications on a single-item basis.
8.  **Significant User Friction:** The absence of a bulk override feature creates a massive friction point for strategists who need to manage large keyword lists.
9.  **Poor Usability for Large Runs:** The UI is not designed for efficiently managing and overriding disqualifications in large-scale discovery runs.
10. **Rigid Volatility Rejection:** Rule 7's hard stop based on `std_dev_to_mean_ratio` incorrectly disqualifies valuable seasonal or trending keywords that are critical for many businesses.
