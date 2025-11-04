import logging
from typing import Dict, Any, List

from backend.data_access.database_manager import DatabaseManager


class DynamicPromptAssembler:
    def __init__(self, db_manager: DatabaseManager):
        self.logger = logging.getLogger(self.__class__.__name__)
        self.db_manager = db_manager

    def build_prompt(self, opportunity: Dict[str, Any]) -> List[Dict[str, str]]:
        """
        Constructs the detailed prompt for the article generation AI using a safe,
        user-configurable template, now with rich SERP data.
        """
        blueprint = opportunity.get("blueprint", {})
        brief = blueprint.get("ai_content_brief", {})
        strategy = blueprint.get("recommended_strategy", {})
        client_cfg = opportunity.get("client_cfg", {})
        num_images = client_cfg.get("num_in_article_images", 2)

        template = client_cfg.get("custom_prompt_template")
        if not template or not template.strip():
            template = """Write a comprehensive, helpful, and expert-level blog post on [TOPIC]. The article must demonstrate first-hand experience and deep expertise. Structure the content for maximum readability and SEO impact. The post must:

        - Be approximately [WORD_COUNT] words, providing authoritative depth on the topic.
        - Target the primary keyword "[PRIMARY KEYWORD]" and naturally incorporate related LSI keywords: [LSI/secondary keywords], along with relevant entities, synonyms, and contextually related concepts to ensure topical completeness.
        - **Demonstrate E-E-A-T (Experience, Expertise, Authoritativeness, Trustworthiness):**
            - Start with a clear, direct 1-2 sentence summary that immediately answers the user's core question.
            - Write from a first-person or expert perspective. Include at least one hypothetical scenario, relatable anecdote, or personal insight to signal direct experience.
            - Cite specific data or statistics and attribute them to a source (e.g., 'According to a 2023 study by...').
            - Include multiple answer formats: short direct responses, step-by-step instructions, and quick takeaway lists (bullet points) so AI models and users can easily extract information.
        - Structure the article with a logical flow using clear subheadings (H2s and H3s).
        - Include a "Frequently Asked Questions" (FAQ) section at the end using real-world questions users search for, written in a conversational Q&A style.
        - Naturally promote [CTA_URL] with a relevant call-to-action at the end of the post.
        - **AVOID:** Do not use generic filler, over-optimization, or unnatural keyword stuffing. Focus on topical relevance, not keyword density. Avoid making unsubstantiated claims.
        """

        default_cta_url = client_cfg.get(
            "default_cta_url", "https://profitparrot.com/contact/"
        )
        recommended_word_count = brief.get("target_word_count", 1000)
        expert_persona_from_brief = brief.get(
            "target_audience_persona",
            client_cfg.get("expert_persona", "an expert writer"),
        )
        replacements = {
            "[TOPIC]": brief.get("target_keyword", "the topic"),
            "[PRIMARY KEYWORD]": brief.get("target_keyword", "the topic"),
            "[LSI/secondary keywords]": ", ".join(brief.get("lsi_keywords", [])),
            "[WORD_COUNT]": str(recommended_word_count),
            "[CTA_URL]": default_cta_url,
            "%%NUM_IMAGES%%": str(num_images),
            "[PERSONA]": expert_persona_from_brief,
        }

        base_instructions = template
        for placeholder, value in replacements.items():
            base_instructions = base_instructions.replace(placeholder, str(value))

        # NEW: Incorporate AI-generated topic clusters into the base instructions
        ai_topic_clusters = blueprint.get("ai_topic_clusters", [])
        if ai_topic_clusters:
            base_instructions += "\n\n**AI-GENERATED TOPIC STRUCTURE (PRIORITY):**\n"
            base_instructions += "The following structure represents the core topics and keywords for this article. Ensure you build your sections around these:\n"
            for cluster in ai_topic_clusters:
                base_instructions += f"- **H2: {cluster['topic_name']}** (Keywords to cover in this section: {', '.join(cluster['keywords'])})\n"
            base_instructions += "Ensure these topics are covered comprehensively and use the listed keywords within their respective H2 sections.\n"

        persona = brief.get("target_audience_persona", "General audience")
        if "expert" in persona.lower() or "planner" in persona.lower():
            readability_instruction = "The tone must be highly sophisticated and authoritative. Maintain a Flesch-Kincaid Grade level of 10 or higher."
        elif "general" in persona.lower() or "beginner" in persona.lower():
            readability_instruction = "The tone must be clear and accessible. Maintain a Flesch-Kincaid Grade level between 7 and 9."
        else:
            readability_instruction = ""

        if readability_instruction:
            base_instructions += (
                f"\n- **Readability Target:** {readability_instruction}"
            )

        base_instructions += f"\n- Adopt the persona of {expert_persona_from_brief}."
        base_instructions += "\n- Include 1-2 'Expert Tips' in blockquotes."

        client_knowledge_base = client_cfg.get("client_knowledge_base")
        if client_knowledge_base and client_knowledge_base.strip():
            base_instructions += "\n\n**CLIENT KNOWLEDGE BASE (CRITICAL CONTEXT):**\n"
            base_instructions += "The following information is crucial for content accuracy and brand alignment. Incorporate relevant details naturally and factually:\n"
            base_instructions += f"{client_knowledge_base}\n"
            base_instructions += "Prioritize accuracy based on this knowledge base.\n"

        base_instructions += "\n- If the content contains data suitable for a table (e.g., comparisons, specifications, statistics), format it as a Markdown table."
        base_instructions += "\n- Include one link to a non-competing, high-authority external resource to back up a key statistic or claim."
        base_instructions += "\n- For in-article images, use a placeholder with the exact format `[[IMAGE: <A descriptive prompt for the image>]]`. For example: `[[IMAGE: A bar chart showing SEO growth over time]]`."

        # --- START MODIFICATION ---
        # NEW: Add instructions based on rich SERP data
        dynamic_serp_data_instructions = []

        if brief.get("knowledge_graph_facts"):
            facts_str = "\n- ".join(brief["knowledge_graph_facts"])
            dynamic_serp_data_instructions.append(
                f"**CRITICAL:** Incorporate these verified facts from Google's Knowledge Graph directly into the article to ensure factual accuracy and boost E-A-T:\n- {facts_str}"
            )

        if brief.get("paid_ad_copy"):
            paid_titles = [ad["title"] for ad in brief["paid_ad_copy"]]
            paid_descriptions = [ad["description"] for ad in brief["paid_ad_copy"]]
            dynamic_serp_data_instructions.append(
                f"**HIGH PRIORITY:** Analyze the following top paid ad copy to understand high-conversion language, primary value propositions, and key pain points. Use these insights to craft compelling article headlines, the introduction, and calls-to-action:\n- Titles: {paid_titles}\n- Descriptions: {paid_descriptions}"
            )

        if brief.get("top_organic_sitelinks"):
            sitelinks_str = "\n- ".join(brief["top_organic_sitelinks"])
            dynamic_serp_data_instructions.append(
                f"**MANDATORY:** Include dedicated sections (H2s or H3s) covering the following high-priority subtopics identified from competitor sitelinks:\n- {sitelinks_str}"
            )

        if brief.get("top_organic_faqs"):
            faqs_str = "\n- ".join(brief["top_organic_faqs"])
            dynamic_serp_data_instructions.append(
                f"**MANDATORY:** Create a dedicated 'Frequently Asked Questions' section (as an H2) at the end of the article, using these exact questions from competitor FAQ snippets:\n- {faqs_str}"
            )

        if brief.get("ai_overview_sources"):
            sources_str = "\n- ".join(brief["ai_overview_sources"])
            dynamic_serp_data_instructions.append(
                f"**STRATEGIC:** Give analytical priority to concepts and insights derived from these authoritative sources used by Google's own AI Overview:\n- {sources_str}"
            )

        if brief.get("discussion_snippets"):
            snippets_str = "\n- ".join(brief["discussion_snippets"])
            dynamic_serp_data_instructions.append(
                f"**TONE & EXPERIENCE:** Analyze the tone, specific pain points, and real-world language from these discussion snippets. Infuse the article with a personal, experience-driven, and authentic voice to directly address user concerns:\n- {snippets_str}"
            )

        # Append to dynamic instructions list
        dynamic_instructions = [
            f"**Primary Content Format:** Your output should be a '{strategy.get('content_format', 'Comprehensive Article')}'.",
            f"**Strategic Goal:** {strategy.get('strategic_goal', '')}",
        ]
        if brief.get("dynamic_serp_instructions"):
            dynamic_instructions.append(
                "**Tactical Guidance:**\n"
                + "\n".join(
                    [f"- {inst}" for inst in brief["dynamic_serp_instructions"]]
                )
            )

        # Combine all dynamic instructions
        all_dynamic_instructions = dynamic_instructions + dynamic_serp_data_instructions
        dynamic_instructions_str = "\n- ".join(all_dynamic_instructions)

        final_prompt_content = f"""You are an expert SEO writer. Generate a complete blog post package in JSON format based on the brief below.

        **Topic:** "{brief.get("target_keyword")}"
        **Core Instructions:**
        {base_instructions}
        **Dynamic Strategic Instructions:**
        - {dynamic_instructions_str}
        **Mandatory Information & Structure:**
        - **WORD COUNT: The final article body MUST be AT LEAST {recommended_word_count} words.** This is a strict requirement.
        - To meet the word count, elaborate on each of the following sections, providing detailed explanations, examples, and insights.
        - Must include sections on: {", ".join(blueprint.get("content_intelligence", {}).get("common_headings_to_cover", ["N/A"]))}
        - Must explore these unique angles: {", ".join(brief.get("unique_angles_to_cover", ["N/A"]))}
        - Mention these key entities: {", ".join(brief.get("key_entities_to_mention", ["N/A"]))}

        Generate a single, valid JSON object with three keys: "article_body_html", "meta_title", and "meta_description". The "article_body_html" must be well-structured HTML."""
        # --- END MODIFICATION ---

        feedback_examples_text = ""
        feedback_data = self.db_manager.get_content_feedback_examples(
            opportunity.get("client_id")
        )
        if feedback_data.get("good_examples") or feedback_data.get("bad_examples"):
            feedback_examples_text = "\n\n**Style Guide based on Past Feedback:**\n"
            if feedback_data.get("good_examples"):
                feedback_examples_text += (
                    "- **DO:** Emulate the style of these highly-rated articles:\n"
                )
                for ex in feedback_data["good_examples"]:
                    feedback_examples_text += f"  - Title: '{ex['keyword']}'. User Feedback: '{ex['comments']}' (Rated {ex['rating']}/5)\n"
            if feedback_data.get("bad_examples"):
                feedback_examples_text += "- **AVOID:** Avoid the issues found in these poorly-rated articles:\n"
                for ex in feedback_data["bad_examples"]:
                    feedback_examples_text += f"  - Title: '{ex['keyword']}'. User Feedback: '{ex['comments']}' (Rated {ex['rating']}/5)\n"

        system_message = "You are an expert SEO content strategist. Your output must be a single, valid JSON object."
        final_prompt_content = final_prompt_content + feedback_examples_text

        return [
            {"role": "system", "content": system_message},
            {"role": "user", "content": final_prompt_content},
        ]

    def flatten_prompt_for_display(self, messages: List[Dict[str, str]]) -> str:
        """Flattens the structured prompt messages into a single string for UI preview."""
        # ... (existing method, no change needed) ...
