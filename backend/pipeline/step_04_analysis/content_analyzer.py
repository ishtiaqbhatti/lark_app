import logging
from typing import List, Dict, Any, Tuple

from external_apis.openai_client import OpenAIClientWrapper

# Keep these imports if you want to reuse them for the deep-dive path
from .content_analysis_modules.ai_intelligence_caller import get_ai_content_analysis


class ContentAnalyzer:
    """
    Orchestrates the analysis of competitor content (or SERP data) to synthesize intelligence.
    """

    def __init__(self, openai_client: OpenAIClientWrapper, config: Dict[str, Any]):
        self.openai_client = openai_client
        self.config = config
        self.logger = logging.getLogger(self.__class__.__name__)
        self.num_common_headings = self.config.get("num_common_headings", 8)
        self.num_unique_angles = self.config.get("num_unique_angles", 5)
        self.max_words_for_ai_analysis = self.config.get(
            "max_words_for_ai_analysis", 2000
        )
        self.num_competitors_for_ai_analysis = self.config.get(
            "num_competitors_for_ai_analysis", 3
        )

    # --- START MODIFICATION ---
    def synthesize_content_intelligence(
        self,
        keyword: str,
        serp_overview: Dict[str, Any],
        competitor_analysis: List[
            Dict[str, Any]
        ],  # This will be empty if deep analysis is skipped
    ) -> Tuple[Dict[str, Any], float]:
        """
        Synthesizes content intelligence by orchestrating data preparation and AI analysis.
        Conditionally uses deep competitor content or rich SERP data.
        """
        if competitor_analysis:
            from .content_analysis_modules.ai_content_preparer import (
                prepare_competitor_content_for_ai,
            )
            from .content_analysis_modules.ai_prompt_builder import (
                get_ai_prompt_messages,
            )

            self.logger.info(
                "Synthesizing intelligence from deep competitor content analysis (legacy path)."
            )

            # 1. Prepare Competitor Content for AI
            content_for_ai, using_markdown = prepare_competitor_content_for_ai(
                competitor_analysis,
                self.num_competitors_for_ai_analysis,
                self.max_words_for_ai_analysis,
            )

            # 2. Build AI Prompt (legacy)
            ai_prompt_messages = get_ai_prompt_messages(
                keyword, content_for_ai, using_markdown
            )

        else:
            self.logger.info(
                "Synthesizing intelligence from rich SERP data (new path)."
            )
            # 1. Prepare SERP Data for AI (already extracted by FullSerpAnalyzer)
            # We just need to ensure it's structured for the prompt.
            # All the new fields are already in serp_overview.

            # 2. Build AI Prompt (new, SERP-only)
            ai_prompt_messages = self._build_synthesis_prompt_from_serp(
                keyword, serp_overview
            )

        # 3. Call AI for Analysis (common to both paths)
        ai_analysis_response, error = get_ai_content_analysis(
            openai_client=self.openai_client,
            messages=ai_prompt_messages,
            model=self.config.get("default_model", "gpt-5-nano"),
            max_completion_tokens=self.config.get(
                "max_completion_tokens_for_generation", 4096
            ),
        )
        total_ai_cost = self.openai_client.latest_cost

        if error or not ai_analysis_response:
            self.logger.error(f"Failed to get deep content analysis from AI: {error}")
            return {
                "analysis_error": f"AI-powered content intelligence failed. Reason: {error}"
            }, total_ai_cost

        # 4. Assemble Final Intelligence Object
        ai_analysis_response["unique_angles_to_include"] = list(
            set(ai_analysis_response.get("unique_angles_to_include", []))
        )[: self.num_unique_angles]

        # --- NEW: Incorporate AI Overview Sources into AI Content Brief
        if (
            serp_overview.get("ai_overview_sources") and not competitor_analysis
        ):  # Only for SERP-only mode
            if "source_and_inspiration_content" not in ai_analysis_response:
                ai_analysis_response["source_and_inspiration_content"] = {}
            ai_analysis_response["source_and_inspiration_content"][
                "ai_overview_sources"
            ] = serp_overview["ai_overview_sources"]

        return ai_analysis_response, total_ai_cost

    # New private method for SERP-only prompt building
    def _build_synthesis_prompt_from_serp(
        self, keyword: str, serp_data: Dict[str, Any]
    ) -> List[Dict[str, str]]:
        """
        Builds a comprehensive prompt for AI content intelligence synthesis
        based purely on rich SERP data.
        """
        system_prompt = "You are a world-class SEO content strategist. Your task is to analyze structured SERP data to reverse-engineer a winning content strategy. Your insights must be actionable and highly specific."

        prompt_sections = [f'**Primary Keyword:** "{keyword}"\n']

        if serp_data.get("knowledge_graph_facts"):
            facts_list = '\n- '.join(serp_data['knowledge_graph_facts'])
            prompt_sections.append(
                f"**Verified Facts from Knowledge Graph (Incorporate these as core facts):**\n- {facts_list}\n"
            )

        if serp_data.get("paid_ad_copy"):
            paid_titles = [ad["title"] for ad in serp_data["paid_ad_copy"]]
            paid_descriptions = [ad["description"] for ad in serp_data["paid_ad_copy"]]
            prompt_sections.append(
                f"**High-Conversion Language from Top Paid Ads (Analyze for compelling headlines/intro/CTAs):**\n- Titles: {paid_titles}\n- Descriptions: {paid_descriptions}\n"
            )

        if serp_data.get("top_organic_sitelinks"):
            sitelinks_list = '\n- '.join(serp_data['top_organic_sitelinks'])
            prompt_sections.append(
                f"**High-Priority Subtopics from Competitor Sitelinks (Must include these as H2/H3s):**\n- {sitelinks_list}\n"
            )

        if serp_data.get("top_organic_faqs"):
            faqs_list = '\n- '.join(serp_data['top_organic_faqs'])
            prompt_sections.append(
                f"**High-Priority Questions from Competitor FAQ Snippets (Must include these in a dedicated FAQ section):**\n- {faqs_list}\n"
            )

        if serp_data.get("ai_overview_sources"):
            sources_list = '\n- '.join(serp_data['ai_overview_sources'])
            prompt_sections.append(
                f"**Authoritative Sources Used by Google's AI Overview (Give analytical priority to concepts from these sources):**\n- {sources_list}\n"
            )

        if serp_data.get("discussion_snippets"):
            snippets_list = '\n- '.join(serp_data['discussion_snippets'])
            prompt_sections.append(
                f"**Voice of the Customer from Discussions/Forums (Analyze for tone, pain points, and authentic perspective):**\n- {snippets_list}\n"
            )

        # Add basic organic results for general context
        if serp_data.get("top_organic_results"):
            org_titles_desc_list = '\n- '.join([
                f"Title: {r['title']}\nDescription: {r['description']}"
                for r in serp_data["top_organic_results"]
            ])
            prompt_sections.append(
                f"**Top Organic Result Snippets (for general content analysis):**\n- {org_titles_desc_list}\n"
            )

        if serp_data.get("people_also_ask"):
            paa_list = '\n- '.join(serp_data['people_also_ask'])
            prompt_sections.append(
                f"**People Also Ask Questions:**\n- {paa_list}\n"
            )
        if serp_data.get("related_searches"):
            related_list = '\n- '.join(serp_data['related_searches'])
            prompt_sections.append(
                f"**Related Searches:**\n- {related_list}\n"
            )
        if serp_data.get("ai_overview_content"):
            prompt_sections.append(
                f"**Google's AI Overview Content:**\n{serp_data['ai_overview_content']}\n"
            )
        if serp_data.get("featured_snippet_content"):
            prompt_sections.append(
                f"**Featured Snippet Content:**\n{serp_data['featured_snippet_content']}\n"
            )

        user_prompt_content = f"""
        Analyze the following comprehensive SERP intelligence report to generate a content strategy blueprint.

        {"".join(prompt_sections)}

        **Your Analysis Task:**
        1.  **Unique Angles & Insights:** Based on ALL the provided SERP data (Knowledge Graph, Paid Ads, FAQs, Sitelinks, AI Overview sources, discussions, organic snippets), identify 2-3 truly unique value propositions or content differentiation angles. Where are the gaps and opportunities for our content to stand out as superior?
        2.  **Key Entities:** List the 5-10 most critical entities (people, products, brands, concepts) from the entire SERP. These must be central to the topic.
        3.  **Core Questions Answered:** Synthesize the 5-7 most fundamental user questions that this keyword intends to answer, drawing from PAA, FAQ snippets, and top organic descriptions. These should form the backbone of the article's problem-solving narrative.
        4.  **Identified Content Gaps:** What specific sub-topics are implied or partially covered in the SERP, but could be expanded into full, authoritative sections in our article? What related long-tail questions (from PAA or Related Searches) are not adequately addressed by top results?

        Provide your analysis in the required structured JSON format.
        """
        return [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt_content.strip()},
        ]

    # --- END MODIFICATION ---

    def generate_ai_outline(
        self,
        keyword: str,
        serp_overview: Dict[str, Any],
        content_intelligence: Dict[str, Any],
    ) -> Tuple[Dict[str, List[str]], float]:
        """
        Uses OpenAI to generate a structured content outline with H2s and corresponding H3s.
        (This can also be refactored into a separate module if desired)
        """
        prompt_messages = self._build_outline_prompt(
            keyword, serp_overview, content_intelligence
        )

        schema = {
            "name": "generate_structured_content_outline",
            "type": "object",
            "properties": {
                "article_structure": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "h2": {
                                "type": "string",
                                "description": "The H2 heading of the section.",
                            },
                            "h3s": {
                                "type": "array",
                                "items": {"type": "string"},
                                "description": "A list of H3 subheadings for this H2 section.",
                            },
                        },
                        "required": ["h2", "h3s"],
                        "additionalProperties": False,
                    },
                }
            },
            "required": ["article_structure"],
            "additionalProperties": False,
        }

        response, error = self.openai_client.call_chat_completion(
            messages=prompt_messages,
            schema=schema,
            model=self.config.get("default_model", "gpt-5-nano"),
            max_completion_tokens=self.config.get(
                "max_completion_tokens_for_generation", 4096
            ),
        )
        total_ai_cost = self.openai_client.latest_cost

        if error or not response or not response.get("article_structure"):
            self.logger.error(f"Failed to generate structured AI outline: {error}")
            return {"article_structure": []}, total_ai_cost

        return response, total_ai_cost

    def _build_outline_prompt(
        self,
        keyword: str,
        serp_overview: Dict[str, Any],
        content_intelligence: Dict[str, Any],
    ) -> List[Dict[str, str]]:
        """Builds the prompt for the AI structured outline generation."""
        # Check if AI-generated topic clusters are available in content_intelligence
        ai_clusters = content_intelligence.get("ai_topic_clusters", [])
        
        prompt_core_instruction = ""
        if ai_clusters:
            # If AI clusters exist, prioritize them to form the core structure
            cluster_structure_description = "\n".join([
                f" - {cluster['topic_name']}: Keywords: {', '.join(cluster['keywords'])}"
                for cluster in ai_clusters
            ])
            prompt_core_instruction = f"""
            **AI-Generated Core Topic Structure (CRITICAL: Use this as the foundation for your H2s):**
            {cluster_structure_description}

            **Instructions for Outline Creation:**
            1.  **Strictly use the `topic_name` from each AI-Generated Core Topic as your primary H2 headings.**
            2.  For each H2, derive relevant H3 subheadings, possibly from the `keywords` within that cluster and other analysis data provided below.
            3.  Ensure the article flows logically and covers the keywords within each H2's cluster.
            """
            
        else:
            # Fallback to previous logic if AI clusters are not available
            prompt_core_instruction = """
            **Instructions for Outline Creation:**
            1. Create a logical flow for the article, starting with an 'Introduction' and ending with a 'Conclusion'.
            """

        prompt = f"""
        You are an expert SEO content strategist. Create a logical and comprehensive content outline for an article about "{keyword}". The output must be a structured list of sections, each with an H2 and a list of corresponding H3 subheadings.

        **Analysis Data:**
        - **Common Competitor Headings to Incorporate:** {", ".join(content_intelligence.get("common_headings_to_cover", []))}
        - **Unique Angles & Gaps to Address:** {", ".join(content_intelligence.get("unique_angles_to_include", []))}
        - **Key Entities to Mention:** {", ".join(content_intelligence.get("key_entities_from_competitors", []))}
        - **People Also Ask Questions to Answer:** {", ".join(serp_overview.get("paa_questions", []))}

        {prompt_core_instruction}

        **General Outline Rules:**
        1. The first H2 heading in the output JSON array must be "Introduction".
        2. The last H2 heading in the output JSON array must be "Conclusion".
        3. If there are 'People Also Ask' questions, create a dedicated H2 section titled 'Frequently Asked Questions' (if not already present from clusters) and use the questions as H3s.
        4. Structure the entire output as a JSON object matching the requested schema.
        """
        return [{"role": "user", "content": prompt}]
