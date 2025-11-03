# User Workflow for Finding Keyword Opportunities

This document outlines the typical workflow for a user of this application to discover new keyword opportunities.

## 1. Starting a Discovery Run

The user begins the process in the **Discovery Hub** section of the application.

1.  **Enter a Seed Keyword:** The user provides a single, broad topic or a specific keyword (e.g., "AI in marketing") into the "Seed Keyword" input field.

2.  **Apply Optional Filters:** To refine the search, the user can apply several pre-defined filters:
    *   **Monthly Search Volume:** Set a minimum threshold for search volume.
    *   **SEO Difficulty:** Set a maximum threshold for keyword difficulty (on a scale of 0-100).
    *   **Competition Level:** Select from "Low," "Medium," or "High" to filter by paid ad competition.
    *   **Search Intent:** Choose the type of user intent, such as "Informational," "Commercial," or "Transactional."

3.  **Initiate the Search:** The user clicks the "Find Opportunities" button to start the discovery run.

## 2. Backend Processing

Once the run is initiated, the backend performs the following steps asynchronously:

1.  **API Calls:** The system makes calls to the DataForSEO API using three different endpoints to gather a comprehensive list of keywords:
    *   **Keyword Ideas:** To get a broad list of related keywords.
    *   **Keyword Suggestions:** To get long-tail variations of the seed keyword.
    *   **Related Keywords:** To find semantically related terms.

2.  **Deduplication and Filtering:** The system filters out any keywords that already exist in the user's account to avoid duplicates.

3.  **Scoring and Qualification:** Each new keyword is then scored based on a variety of factors, including search volume, keyword difficulty, and commercial intent. The system also applies disqualification rules, such as checking for cannibalization with existing content.

4.  **Saving Opportunities:** The keywords that pass the filtering and qualification steps are saved to the database as new opportunities.

## 3. Reviewing the Results

1.  **Monitoring the Run:** The user can monitor the progress of the discovery run in the **Discovery History** section.

2.  **Viewing Opportunities:** Once the run is complete, the user can navigate to the **Opportunities Page** to view the newly discovered keyword opportunities. The results are displayed in a table, and the user can sort and filter them based on various metrics.

3.  **Detailed Analysis:** The user can click on any opportunity to view a more detailed analysis, including the full score breakdown and SERP data.
