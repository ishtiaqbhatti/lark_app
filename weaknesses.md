# 10 Weaknesses in the Keyword Discovery Implementation

Based on a review of the frontend and backend code, here are 10 weaknesses in the current implementation of the keyword discovery feature:

1.  **Hardcoded Discovery Modes:** The user has no control over which discovery modes are used. The backend always uses all three modes (`keyword_ideas`, `keyword_suggestions`, `related_keywords`), which may not be necessary or cost-effective in all cases.

2.  **Hardcoded API Parameters:** Several important API parameters are hardcoded in the backend, such as `include_clickstream_data`, `closely_variants`, `ignore_synonyms`, and `exact_match`. This limits the flexibility of the keyword discovery process.

3.  **Single Seed Keyword:** The frontend only allows the user to enter a single seed keyword. The DataForSEO API supports up to 200 seed keywords for the "Keyword Ideas" endpoint.

4.  **No Control Over Pagination:** The `discovery_max_pages` parameter is hardcoded to 1 in `get_keyword_ideas` for all modes. This means the application only ever gets the first page of results from the DataForSEO API, which could be a significant limitation.

5.  **No Control Over Depth for Related Keywords:** The `depth` parameter for the "Related Keywords" endpoint is hardcoded to 1 in `get_keyword_ideas`. This limits the depth of the related keyword search.

6.  **Inconsistent Filter Handling:** The `NewKeywordExpander` has to do extra work to add and remove the "keyword_data." prefix from the filters because the frontend provides filters in a format that is only compatible with the "Related Keywords" endpoint.

7.  **Two KeywordExpander Classes:** There are two `KeywordExpander` classes (`KeywordExpander` and `NewKeywordExpander`), which is confusing and could lead to bugs.

8.  **No Error Handling for Individual API Calls:** The `get_keyword_ideas` function in `DataForSEOClientV2` calls the three discovery APIs sequentially. If one of the API calls fails, the entire discovery process will fail. There is no mechanism to handle failures for individual API calls.

9.  **No Cost Estimation:** The frontend does not provide the user with an estimated cost for the discovery run before they start it. This could lead to unexpected costs for the user.

10. **No Way to View and Use `offset_token`:** The DataForSEO API provides an `offset_token` for pagination. The current implementation doesn't seem to expose this to the user, which means they can't manually paginate through the results if they wanted to.
