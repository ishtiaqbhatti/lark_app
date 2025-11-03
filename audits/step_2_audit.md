# Step 2: Initial Scoring, Filtering, and Deduping

## Mandate 4 (Data Flaw)
*   **Analysis:** Stale search intent data is used. `search_intent_info.last_updated_time` can be months or over a year old. Making strategic rejections (Rule 2, Rule 2b) based on outdated intent compromises the accuracy of initial qualification.

## Mandate 5 (Strategic Flaw)
*   **Analysis:** There is a blanket rejection rule for low difficulty/volume. **Rule 0** in `disqualification_rules.py` disqualifies keywords if `search_volume == 0` or `keyword_difficulty == 0`. This inflexible rule eliminates strategic targets like long-tail, emerging, or new market keywords where data latency is common but value is high.

## Mandate 6 (Real-World Issue/Gap)
*   **Analysis:** There is a lack of bulk action usability. `RunDetailsPage.jsx` only supports single-item manual override of a disqualification. This presents a massive friction point if a human strategist needs to override a faulty disqualification rule for hundreds of keywords found in a run.

## Mandate 7 (Weakness)
*   **Analysis:** The logic of the volatility rejection is rigid. Rule 7's hard stop is based on `std_dev_to_mean_ratio`. This rigid rule wrongly disqualifies highly valuable, high-traffic seasonal or trending keywords that are essential for many commercial clients.
