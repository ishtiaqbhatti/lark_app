# Speeding Up Article Generation

This document outlines identified bottlenecks and proposes solutions to accelerate the article generation process that occurs after a blueprint has been created.

## 1. Current Workflow Analysis

The current post-blueprint generation process, orchestrated by `ContentOrchestrator`, is highly **sequential**. This is the primary bottleneck. The workflow is as follows:

1.  **Generate Full Article (Blocking):** The `SectionalArticleGenerator` is called.
    *   It uses a `ThreadPoolExecutor` to generate the introduction and all H2 body sections in parallel. This part is efficient.
    *   However, it then waits for all sections to complete before **sequentially** generating the conclusion.
    *   The entire process blocks the orchestrator until the full HTML body is assembled.
2.  **Audit Content (Blocking):** The complete HTML is passed to the `ContentAuditor`. This involves CPU-intensive text analysis and potentially blocking network calls to check for broken links.
3.  **Self-Healing Loop (Blocking):** If the audit fails, the system enters a loop of up to three attempts to fix the content via additional LLM calls.
4.  **Generate Featured Image (Blocking):** The `ImageGenerator` makes a network call to Pexels.
5.  **Craft Social Posts (Blocking):** The `SocialMediaCrafter` makes an LLM call.
6.  **Suggest Internal Links (Blocking):** The `InternalLinkingSuggester` makes an LLM call.
7.  **Final Formatting:** The `HtmlFormatter` runs, which is the final step.

Each arrow in this chain represents a point where the entire process waits for the previous step to finish completely. The enrichment tasks (Image, Social, Links) are independent of each other but are executed one by one.

## 2. Identified Bottlenecks

*   **Sequential Execution:** The most significant bottleneck is the sequential nature of the enrichment tasks (Image Generation, Social Media Crafting, Internal Linking). These tasks are I/O-bound (network calls to LLMs or Pexels) and could be run in parallel.
*   **Blocking Article Generation:** The main orchestrator waits for the entire article body to be generated before starting any other tasks.
*   **Sequential Section Generation:** The `ContentOrchestrator` generates sections sequentially in a loop, passing the content of the previous section to the next. This prevents parallelization of the core writing task. *Correction*: The `SectionalArticleGenerator` *does* use a `ThreadPoolExecutor` to generate body sections in parallel, which is good. However, the `ContentOrchestrator` uses a sequential loop that doesn't leverage this parallel capability. The `generate_section` method in the generator takes `previous_section_content`, forcing a sequential flow. The `generate_full_article` method, however, shows the correct parallel approach. The orchestrator should be updated to use the parallel-capable method.
*   **Blocking Audit:** The content audit, especially the broken link checker, can be slow due to network latency.

## 3. Proposed Speed Improvements

### 3.1. High-Impact: Massive Parallelism

The most significant speedup can be achieved by executing all independent, I/O-bound tasks concurrently.

**Proposal:** Modify `ContentOrchestrator` to use a `ThreadPoolExecutor` to run multiple agents at once.

**New Workflow:**

1.  **Initiate Parallel Tasks:** As soon as the blueprint is available, start the following tasks in parallel threads:
    *   **Task A (Article Body):** Call `SectionalArticleGenerator.generate_full_article`.
    *   **Task B (Featured Image):** Call `ImageGenerator.generate_featured_image`.
    *   **Task C (Social Posts):** Call `SocialMediaCrafter.craft_posts`.
2.  **First Synchronization Point:** Wait for the Article Body task (Task A) to complete, as it's required for the next steps.
3.  **Initiate Dependent Parallel Tasks:** Once the article body is available, start the next set of parallel tasks:
    *   **Task D (Internal Links):** Call `InternalLinkingSuggester.suggest_links` using the generated article text.
    *   **Task E (Content Audit):** Call `ContentAuditor.audit_content`.
4.  **Final Synchronization and Assembly:**
    *   Wait for all tasks (B, C, D, E) to complete.
    *   If the audit (Task E) fails, run the self-healing loop.
    *   Once all data is gathered and the content is validated, run the final `HtmlFormatter`.

**Estimated Impact:** This could reduce the total generation time by **50-70%**, as the time taken would be determined by the longest-running task (likely the article body generation) rather than the sum of all tasks.

### 3.2. Medium-Impact: Optimize Article Generation Flow

The `ContentOrchestrator` currently generates article sections in a sequential loop. This should be updated to use the `SectionalArticleGenerator`'s built-in parallel generation capability.

**Proposal:**

1.  In `ContentOrchestrator._run_full_content_generation_background`, replace the `for` loop that calls `sectional_generator.generate_section` with a single call to `sectional_generator.generate_full_article`.
2.  The `generate_full_article` method already uses a `ThreadPoolExecutor` to generate the introduction and all body sections in parallel. It then assembles them and generates the conclusion. This is the most efficient way to generate the article body.

**Estimated Impact:** This will significantly speed up the core content writing phase, especially for articles with many sections.

### 3.3. Low-Impact: Model and Prompt Optimization

*   **Use Faster Models for Simple Tasks:** Some tasks, like generating social media posts or suggesting internal links, may not require the most powerful (and slowest) LLM.
    *   **Proposal:** In `settings.ini`, allow for specifying different models for different agents (e.g., `social_media_model = "gpt-4-turbo"`). The `SocialMediaCrafter` and `InternalLinkingSuggester` can then use these faster, cheaper models.
*   **Asynchronous Link Checking:** The broken link checker in `ContentAuditor` can be slow.
    *   **Proposal:** Move the `_check_for_broken_links` function to run in a separate background thread *after* the article has been saved. The results can be added to the audit report later. This removes a blocking network operation from the critical path.

## 4. Summary

By shifting from a sequential to a highly parallel workflow and optimizing the core article generation logic, the post-blueprint generation time can be drastically reduced. The primary focus should be on implementing the parallel execution of independent agents in the `ContentOrchestrator`.
