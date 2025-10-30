import logging
from typing import Dict, Any, Tuple, Optional, List

from external_apis.openai_client import OpenAIClientWrapper
from agents.prompt_assembler import DynamicPromptAssembler


class SectionalArticleGenerator:
    """
    An agentic generator that creates content for specific sections of an article
    based on a highly contextual prompt.
    """

    def __init__(
        self, openai_client: OpenAIWrapper, config: Dict[str, Any], db_manager
    ):
        self.openai_client = openai_client
        self.config = config
        self.logger = logging.getLogger(self.__class__.__name__)
        self.prompt_assembler = DynamicPromptAssembler(db_manager)

    def _sanitize_prompt_input(self, user_input: str, max_length: int = 5000) -> str:
        """
        Sanitizes user input before inserting into prompts to prevent injection attacks.
        """
        if not isinstance(user_input, str):
            return ""
        
        # Truncate to prevent excessive token usage
        sanitized = user_input[:max_length]
        
        # Remove or escape potential prompt injection patterns
        # Remove system-level instructions
        dangerous_patterns = [
            "ignore previous instructions",
            "ignore all previous",
            "disregard previous",
            "new instructions:",
            "system:",
            "assistant:",
            "[SYSTEM]",
            "[INST]",
        ]
        
        sanitized_lower = sanitized.lower()
        for pattern in dangerous_patterns:
            if pattern in sanitized_lower:
                self.logger.warning(f"Potential prompt injection detected: '{pattern}' in input")
                # Replace the pattern with safe text
                sanitized = sanitized.replace(pattern, "[filtered]")
                sanitized = sanitized.replace(pattern.upper(), "[filtered]")
                sanitized = sanitized.replace(pattern.title(), "[filtered]")
        
        return sanitized


    def _generate_component(
        self, messages: List[Dict[str, str]], model: str, temperature: float
    ) -> Tuple[Optional[str], float]:
        """Internal helper to call the LLM and get a raw HTML string."""
        schema = {
            "name": "generate_html_content",
            "type": "object",
            "properties": {
                "content_html": {
                    "type": "string",
                    "description": "The generated content as a clean, well-structured HTML block. Do not include the main heading tag itself.",
                }
            },
            "required": ["content_html"],
            "additionalProperties": False,
        }
        response, error = self.openai_client.call_chat_completion(
            messages=messages,
            schema=schema,
            model=model,
            max_completion_tokens=self.config.get(
                "max_completion_tokens_for_generation", 4096
            ),
        )
        cost = self.openai_client.latest_cost
        if error or not response:
            self.logger.error(f"Failed to generate content component: {error}")
            return None, cost
        return response.get("content_html"), cost

    def generate_introduction(
        self, opportunity: Dict[str, Any]
    ) -> Tuple[Optional[str], float]:
        brief = opportunity.get("blueprint", {}).get("ai_content_brief", {})
        prompt = f"""
        You are an expert copywriter. Write a compelling and hook-driven introduction for a blog post titled "{opportunity["keyword"]}".
        The introduction should be 2-3 paragraphs.
        - Immediately grab the reader's attention with a relatable problem or surprising statistic.
        - Briefly state the core problem or question the article will solve and why it matters.
        - End with a transition that clearly outlines what the reader will learn.
        - Target Audience: {brief.get("target_audience_persona")}
        - Tone: {opportunity.get("client_cfg", {}).get("brand_tone")}
        Return a JSON object with a single key "content_html" containing the HTML for the introduction (e.g., {{"content_html": "<p>...</p><p>...</p>"}}).
        """
        return self._generate_component(
            [{"role": "user", "content": prompt}],
            self.config.get("default_model", "gpt-5-nano"),
            0.75,
        )

    def generate_conclusion(
        self, opportunity: Dict[str, Any], full_article_context: str
    ) -> Tuple[Optional[str], float]:
        cta_url = opportunity.get("client_cfg", {}).get("default_cta_url", "#")
        prompt = f"""
        You are an expert copywriter. Write a powerful conclusion for the following blog post.
        The conclusion should be 2 paragraphs.
        - Briefly summarize the most important takeaways from the article.
        - Provide a final, actionable thought or encouragement for the reader.
        - End with a compelling call-to-action that encourages the reader to visit {cta_url}.
        - Tone: {opportunity.get("client_cfg", {}).get("brand_tone")}

        **Full Article Context (for summary):**
        {full_article_context}

        Return a JSON object with a single key "content_html" containing the HTML for the conclusion (e.g., {{"content_html": "<p>...</p><p>...</p>"}}).
        """
        return self._generate_component(
            [{"role": "user", "content": prompt}],
            self.config.get("default_model", "gpt-5-nano"),
            0.7,
        )

    def generate_section(
        self,
        opportunity: Dict[str, Any],
        section_title: str,
        section_sub_points: List[str],
        previous_section_content: str,
    ) -> Tuple[Optional[str], float]:
        brief = opportunity.get("blueprint", {}).get("ai_content_brief", {})
        
        # Sanitize all user-controlled inputs
        safe_keyword = self._sanitize_prompt_input(opportunity.get("keyword", ""), max_length=200)
        safe_section_title = self._sanitize_prompt_input(section_title, max_length=500)
        safe_sub_points = [self._sanitize_prompt_input(sp, max_length=200) for sp in (section_sub_points or [])]
        safe_previous_content = self._sanitize_prompt_input(previous_section_content[-1000:], max_length=1000)
        
        prompt = f"""
        You are an expert SEO content writer and subject matter expert. Your task is to write a single, detailed section for a blog post about "{safe_keyword}".

        **Current Section to Write:** "{safe_section_title}"
        **Key Sub-points to cover in this section:** {", ".join(safe_sub_points) if safe_sub_points else "N/A"}
        **Content from the Previous Section (for transition and context):**
        ...{safe_previous_content}...

        **Instructions:**
        - Write a comprehensive, in-depth section covering the topic "{safe_section_title}".
        - If provided, elaborate on all key sub-points, using them to structure the section's content.
        - Ensure a smooth, logical transition from the previous section's content.
        - Incorporate relevant entities and demonstrate expertise by using practical examples or insights.
        - Persona: {brief.get("target_audience_persona")}
        - Tone: {opportunity.get("client_cfg", {}).get("brand_tone")}
        
        Return a JSON object with a single key "content_html" containing the HTML for this section (e.g., using <p>, <ul>, <h3> tags). Do NOT include the main <h2> tag for "{safe_section_title}" itself.
        """
        return self._generate_component(
            [{"role": "user", "content": prompt}],
            self.config.get("default_model", "gpt-5-nano"),
            0.7,
        )