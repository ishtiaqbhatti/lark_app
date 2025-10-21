import logging
from typing import Dict, Any


class BriefAssembler:
    """
    Assembles the final AI content brief from the blueprint data.
    This agent acts as a transformation layer between the analysis blueprint
    and the actionable brief for the content generation AI.
    """

    def __init__(self, openai_client):
        self.logger = logging.getLogger(self.__class__.__name__)
        self.openai_client = openai_client

    def _generate_dynamic_brief_attributes(self, blueprint: Dict[str, Any], client_cfg: Dict[str, Any]) -> Dict[str, Any]:
        """Uses an AI call to generate dynamic persona and goal."""
        try:
            target_keyword = blueprint.get("winning_keyword", {}).get("keyword", "the target topic")
            serp_overview = blueprint.get("serp_overview", {})
            
            prompt = f"""
            Based on the following SERP data for the keyword '{target_keyword}', define a target audience persona and a primary goal for a new piece of content.

            SERP Data:
            - Dominant Content Format: {serp_overview.get('dominant_content_format', 'N/A')}
            - People Also Ask: {', '.join(serp_overview.get('people_also_ask', []))}
            - Related Searches: {', '.join(serp_overview.get('related_searches', []))}

            Client's Brand Voice: "{client_cfg.get('brand_voice', 'expert and informative')}"

            Return a JSON object with two keys: 'target_audience_persona' and 'primary_goal'.
            The persona should be a brief, descriptive summary of the ideal reader.
            The goal should be a concise statement about what the content aims to achieve for that reader.
            """
            
            messages = [{"role": "user", "content": prompt}]
            schema = {
                "name": "generate_brief_attributes",
                "description": "Generates a target audience persona and primary goal for a piece of content.",
                "type": "object",
                "properties": {
                    "target_audience_persona": {
                        "type": "string",
                        "description": "A brief, descriptive summary of the ideal reader."
                    },
                    "primary_goal": {
                        "type": "string",
                        "description": "A concise statement about what the content aims to achieve for that reader."
                    }
                },
                "required": ["target_audience_persona", "primary_goal"],
                "additionalProperties": False
            }

            response_json, error = self.openai_client.call_chat_completion(
                messages=messages,
                model="gpt-5-nano",
                schema=schema
            )

            if error:
                raise Exception(f"AI call failed: {error}")

            return response_json

        except Exception as e:
            self.logger.error(f"Failed to generate dynamic brief attributes: {e}")
            # Fallback to static values
            return {
                "target_audience_persona": self._determine_persona("Blog Post", client_cfg),
                "primary_goal": f"To provide a comprehensive and helpful resource that ranks for '{target_keyword}'.",
            }

    def assemble_brief(
        self, blueprint: Dict[str, Any], client_id: str, client_cfg: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Constructs the AI content brief by extracting and structuring
        information from the blueprint.
        """
        winning_keyword_data = blueprint.get("winning_keyword", {})
        serp_overview = blueprint.get("serp_overview", {})
        content_intelligence = blueprint.get("content_intelligence", {})
        content_type = blueprint.get("recommended_strategy", {}).get(
            "content_format", "Blog Post"
        )
        
        dynamic_attrs = self._generate_dynamic_brief_attributes(blueprint, client_cfg)
        
        word_count_multiplier = self._get_word_count_multiplier(
            content_type, client_cfg
        )
        base_word_count = content_intelligence.get("recommended_word_count", 1500)
        target_word_count = int(base_word_count * word_count_multiplier)

        brief = {
            "target_keyword": winning_keyword_data.get("keyword"),
            "content_type": content_type,
            "target_audience_persona": dynamic_attrs.get("target_audience_persona"),
            "primary_goal": dynamic_attrs.get("primary_goal"),
            "target_word_count": target_word_count,
            "mandatory_sections": content_intelligence.get(
                "common_headings_to_cover", []
            ),
            "unique_angles_to_cover": content_intelligence.get(
                "unique_angles_to_include", []
            ),
            "questions_to_answer_directly": serp_overview.get("paa_questions", []),
            "key_entities_to_mention": content_intelligence.get(
                "key_entities_from_competitors", []
            ),
            "compelling_arguments_to_integrate": content_intelligence.get(
                "unique_arguments_from_competitors", []
            ),
            "core_questions_competitors_answer": content_intelligence.get(
                "core_questions_answered_by_competitors", []
            ),
            "related_topics_to_include": serp_overview.get("related_searches", []),
            "google_preferred_answers": serp_overview.get(
                "extracted_serp_features", []
            ),
            "dynamic_serp_instructions": self._get_dynamic_serp_instructions(
                serp_overview, content_intelligence, blueprint
            ),
            "source_and_inspiration_content": {
                "competitors_urls": [
                    comp["url"]
                    for comp in blueprint.get("competitor_analysis", [])
                    if "url" in comp
                ]
            },
            "client_id": client_id,
        }

        # --- START MODIFICATION ---
        # NEW: Add all the rich SERP data to the brief
        if serp_overview.get("knowledge_graph_facts"):
            brief["knowledge_graph_facts"] = serp_overview["knowledge_graph_facts"]
        if serp_overview.get("paid_ad_copy"):
            brief["paid_ad_copy"] = serp_overview["paid_ad_copy"]
        if serp_overview.get("ai_overview_sources"):
            brief["ai_overview_sources"] = serp_overview["ai_overview_sources"]
        if serp_overview.get("top_organic_faqs"):
            brief["top_organic_faqs"] = serp_overview["top_organic_faqs"]
        if serp_overview.get("top_organic_sitelinks"):
            brief["top_organic_sitelinks"] = serp_overview["top_organic_sitelinks"]
        if serp_overview.get("discussion_snippets"):
            brief["discussion_snippets"] = serp_overview["discussion_snippets"]

        all_about_search_terms = []
        all_about_related_terms = []
        for res in blueprint.get("serp_overview", {}).get("top_organic_results", []):
            if res.get("about_this_result_search_terms"):
                all_about_search_terms.extend(res["about_this_result_search_terms"])
            if res.get("about_this_result_related_terms"):
                all_about_related_terms.extend(res["about_this_result_related_terms"])

        if all_about_search_terms:
            brief["google_understanding_search_terms"] = list(
                set(all_about_search_terms)
            )
        if all_about_related_terms:
            brief["google_understanding_related_terms"] = list(
                set(all_about_related_terms)
            )
        # --- END MODIFICATION ---

        self.logger.info(f"Assembled AI content brief for '{brief['target_keyword']}'.")
        return brief

    def _get_dynamic_serp_instructions(
        self,
        serp_overview: Dict[str, Any],
        content_intelligence: Dict[str, Any],
        blueprint: Dict[str, Any],
    ) -> list[str]:
        """Generates specific instructions for the AI based on SERP features and content intelligence."""
        instructions = []
        if serp_overview.get("extracted_serp_features"):
            instructions.append(
                "Pay close attention to the 'google_preferred_answers' section. This contains content that Google has already featured in rich snippets, so it's a strong indication of what Google considers a good answer. Use it as a primary source of inspiration."
            )
        if serp_overview.get("serp_has_featured_snippet"):
            instructions.append(
                "Create a concise, clear paragraph early in the article that directly answers the main query to target the featured snippet."
            )
        if serp_overview.get("serp_has_ai_overview"):
            instructions.append(
                "The content must be exceptionally high-quality, original, and provide unique insights to stand out against Google's AI Overview."
            )
        if serp_overview.get("has_video_carousel"):
            instructions.append(
                "Structure content in a way that is easily adaptable into a video script, as video is a key format for this topic."
            )
        if serp_overview.get("knowledge_graph_facts"):
            instructions.append(
                f"Incorporate the key facts from the Knowledge Graph: {', '.join(serp_overview['knowledge_graph_facts'])}."
            )

        top_results_with_context = [
            r
            for r in serp_overview.get("top_organic_results", [])
            if r.get("about_this_result_source_info")
        ]
        if top_results_with_context:
            context_info = top_results_with_context[0]["about_this_result_source_info"]
            instructions.append(
                f"Google's 'About this Result' panel says the top result is relevant because: '{context_info}'. Use this to understand the core topic."
            )

        if serp_overview.get("discussions_and_forums_snippets"):
            instructions.append(
                f"Address user pain points from forum discussions: {' | '.join(serp_overview['discussions_and_forums_snippets'])}."
            )

        days_ago = serp_overview.get("serp_last_updated_days_ago")
        if days_ago is not None:
            if days_ago <= 30:
                instructions.append(
                    f"The SERP is fresh ({days_ago} days old). Ensure content reflects the latest information."
                )
            elif days_ago > 180:
                instructions.append(
                    f"The SERP is outdated ({days_ago} days old). This is an opportunity to publish a more current and comprehensive article."
                )

        # Instructions from content intelligence (including competitor weaknesses)
        if content_intelligence.get("key_entities_from_competitors"):
            instructions.append(
                f"Mention key entities identified from competitors: {', '.join(content_intelligence['key_entities_from_competitors'])}."
            )

            # Summarize competitor weaknesses based on new granular scores
            competitor_analysis = blueprint.get("competitor_analysis", [])
            if competitor_analysis and all(
                "overall_strength_score" in c
                for c in competitor_analysis
                if c.get("url")
            ):
                tech_scores = [
                    c.get("technical_strength_score", 100)
                    for c in competitor_analysis
                    if c.get("url")
                ]
                content_scores = [
                    c.get("content_quality_score", 100)
                    for c in competitor_analysis
                    if c.get("url")
                ]

                # NEW: Add specific technical weaknesses if identified
                all_tech_warnings = []
                for comp in competitor_analysis:
                    all_tech_warnings.extend(comp.get("technical_warnings", []))

                unique_issues_to_highlight = list(set(all_tech_warnings))[
                    :3
                ]  # Limit to top 3
                if unique_issues_to_highlight:
                    formatted_warnings = ", ".join(
                        [w.replace("_", " ") for w in unique_issues_to_highlight]
                    )
                    instructions.append(
                        f"EXPLOIT WEAKNESS: Top competitors exhibit specific technical flaws such as: {formatted_warnings}. Your content must be technically superior."
                    )
                elif tech_scores:  # Fallback to general if no specific warnings
                    avg_tech_score = sum(tech_scores) / len(tech_scores)
                    if avg_tech_score < 65:
                        instructions.append(
                            "EXPLOIT WEAKNESS: Top competitors are generally technically poor (e.g., slow page speed, render-blocking resources). A fast, well-built page has a strong advantage."
                        )

                if content_scores:
                    avg_content_score = sum(content_scores) / len(content_scores)
                    if avg_content_score < 65:
                        instructions.append(
                            "EXPLOIT WEAKNESS: Ranking content is low-quality, thin, or outdated. Win by providing significantly more depth and fresh information."
                        )

        return instructions

    def _determine_persona(self, content_type: str, client_cfg: Dict[str, Any]) -> str:
        """Determines the persona to use based on client config."""
        base_persona = client_cfg.get("expert_persona", "an expert writer")
        return f"{base_persona} who writes like a human"

    def _get_word_count_multiplier(
        self, content_type: str, client_cfg: Dict[str, Any]
    ) -> float:
        """
        Gets the word count multiplier for a given content type from the client config,
        falling back to a default if not found.
        """
        # Sanitize the content_type to match the keys in settings.ini
        # e.g., "Comprehensive Article" -> "comprehensive_article"
        sanitized_format = content_type.lower().replace(" ", "_")

        # Look up the specific multiplier, or use the default multiplier if not found
        return client_cfg.get(
            sanitized_format, client_cfg.get("default_multiplier", 1.2)
        )
