# Granular Keyword Discovery Workflow

This document outlines a detailed plan for using the DataForSEO "Keyword Ideas", "Keyword Suggestions", and "Related Keywords" APIs to build a comprehensive keyword discovery workflow.

## Overall Strategy

The goal is to move from broad topic discovery to specific, actionable keyword opportunities. The workflow is as follows:

1.  **Broad Exploration (Keyword Ideas):** Start with a few high-level seed keywords to discover related topics and content pillars.
2.  **Long-Tail Expansion (Keyword Suggestions):** Use the most promising keywords from the "Ideas" step to generate long-tail variations and specific article ideas.
3.  **Topical Deep Dive (Related Keywords):** Further refine your keyword list by finding what Google considers to be closely related searches, helping you build content clusters and ensure topical authority.

---

## 1. Keyword Ideas API: Broad Exploration

**Objective:** To discover new, conceptually related keyword categories.

### Flow:

1.  **Initial Brainstorming:** Start with 1-5 core "seed" keywords that represent your main business areas (e.g., "content marketing", "seo services").
2.  **API Request:** Make a `POST` request to `https://api.dataforseo.com/v3/dataforseo_labs/google/keyword_ideas/live`.
3.  **Analyze Results:** Look for keywords that belong to interesting or unexpected categories. Pay attention to the `categories` field in the response.
4.  **Iterate:** Take the most promising keywords from the results and use them as new seed keywords in a subsequent "Keyword Ideas" request to explore those topics more deeply.

### Granular Request Parameters:

*   `keywords`: An array of your seed keywords. Start with a small, focused list.
*   `location_code`: Essential for getting geographically relevant data.
*   `language_code`: Ensure this matches your target audience.
*   `include_serp_info`: Set to `true` to get a sense of the SERP landscape for each keyword idea. This is crucial for early qualification.
*   `filters`: Use filters to narrow down the results to the most promising opportunities.
    *   `["keyword_info.search_volume", ">", 1000]`: Filter for a minimum search volume to focus on keywords with significant traffic potential.
    *   `["keyword_info.competition_level", "=", "LOW"]`: Find keywords with less competition in paid search, which can sometimes indicate lower organic competition as well.
    *   `["keyword_difficulty", "<", 40]`: Filter for keywords that are easier to rank for.
*   `order_by`: Sort the results to prioritize the best opportunities.
    *   `["keyword_info.search_volume", "desc"]`: See the highest volume keywords first.
    *   `["relevance", "desc"]`: Start with the most relevant ideas.

### Example Workflow:

1.  **Request 1:**
    *   `keywords`: `["content marketing"]`
    *   `filters`: `[["keyword_info.search_volume", ">", 500], "and", ["keyword_difficulty", "<", 50]]`
2.  **Analysis:** The results might include "email marketing platforms" and "social media analytics".
3.  **Request 2 (Iteration):**
    *   `keywords`: `["email marketing platforms"]`
    *   `filters`: (same as above)
4.  **Outcome:** You have now explored a new, related topic and have a list of viable keywords within it.

---

## 2. Keyword Suggestions API: Long-Tail Expansion

**Objective:** To generate specific, long-tail keywords and content ideas from the promising keywords discovered in the previous step.

### Flow:

1.  **Select Keywords:** Choose the most relevant and high-potential keywords from the "Keyword Ideas" results.
2.  **API Request:** For each selected keyword, make a `POST` request to `https://api.dataforseo.com/v3/dataforseo_labs/google/keyword_suggestions/live`.
3.  **Analyze Results:** Look for question-based keywords (e.g., "how to...", "what is...") and other long-tail phrases that indicate specific user intent.

### Granular Request Parameters:

*   `keyword`: The single seed keyword you are expanding on.
*   `include_seed_keyword`: Set to `true` to get data for your original keyword in the response for comparison.
*   `exact_match`: Set to `true` to get suggestions that contain your exact seed keyword phrase. This is useful for finding highly relevant long-tail variations.
*   `filters`:
    *   `["keyword", "regex", "^(who|what|where|when|why|how)"]`: Use a regex filter to find question-based keywords, which are excellent for blog posts.
    *   `["keyword_info.search_volume", ">", 100]`: Filter out very low-volume long-tail keywords.
*   `order_by`:
    *   `["keyword_info.search_volume", "desc"]`: Prioritize the long-tail keywords with the most traffic potential.

### Example Workflow:

1.  **Select Keyword:** From the "Keyword Ideas" step, you chose "email marketing platforms".
2.  **Request:**
    *   `keyword`: `"email marketing platforms"`
    *   `filters`: `[["keyword", "regex", "^(what|best|how)"], "and', ["keyword_info.search_volume", ">", 200]]`
3.  **Analysis:** The results might include "what are the best email marketing platforms for small businesses" or "how to choose an email marketing platform".
4.  **Outcome:** You now have specific, intent-driven topics for articles.

---

## 3. Related Keywords API: Topical Deep Dive

**Objective:** To find keywords that Google's algorithm considers closely related to your target keywords, helping you build topical authority.

### Flow:

1.  **Select Final Keywords:** Take your primary target keywords for a piece of content (likely a mix of head terms and long-tail keywords).
2.  **API Request:** For each primary keyword, make a `POST` request to `https://api.dataforseo.com/v3/dataforseo_labs/google/related_keywords/live`.
3.  **Analyze Results:** These are the keywords you should consider including in your content as subheadings or secondary keywords to create a comprehensive piece that fully covers the topic.

### Granular Request Parameters:

*   `keyword`: Your primary target keyword.
*   `depth`: This is a powerful parameter.
    *   `depth: 1`: Gets the immediate related searches for your keyword.
    *   `depth: 2`: Gets the related searches for your keyword, *and then* gets the related searches for each of those results. This is excellent for building out content clusters and topic maps. Use with caution as it can generate a large number of keywords.
*   `limit`: Keep this reasonable, especially when using a higher `depth`, to avoid an overwhelming number of results.

### Example Workflow:

1.  **Select Keyword:** You are writing an article on "best email marketing platforms for small businesses".
2.  **Request:**
    *   `keyword`: `"best email marketing platforms for small businesses"`
    *   `depth`: `2`
3.  **Analysis:** The results might include "email marketing pricing", "free email marketing tools", and "Mailchimp vs. Constant Contact".
4.  **Outcome:** You now have a list of subtopics to include in your article to make it more comprehensive and authoritative in the eyes of Google.

---

## Combined Workflow Summary

1.  **Start Broad:** Use `Keyword Ideas` with a few core terms to map out your main content pillars.
2.  **Get Specific:** Feed the best ideas into `Keyword Suggestions` with regex filters to find question-based and long-tail article topics.
3.  **Build Authority:** For each article topic, use `Related Keywords` with `depth: 2` to find all the necessary subtopics to include, ensuring your content is comprehensive and ranks well.
