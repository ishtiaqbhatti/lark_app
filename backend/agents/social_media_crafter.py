# agents/social_media_crafter.py
import logging
from typing import Dict, Any, Tuple, Optional, List

from bs4 import BeautifulSoup

from backend.external_apis.openai_client import OpenAIClientWrapper


class SocialMediaCrafter:
    """
    AI agent for crafting social media posts based on the generated article.
    """

    def __init__(self, openai_client: OpenAIClientWrapper, config: Dict[str, Any]):
        self.openai_client = openai_client
        self.config = config
        self.logger = logging.getLogger(self.__class__.__name__)

    def craft_posts(
        self, opportunity: Dict[str, Any]
    ) -> Tuple[Optional[List[Dict[str, Any]]], float]:
        """
        Generates social media blurbs for different platforms.
        """
        prompt_messages = self._build_crafting_prompt(opportunity)

        schema = {
            "type": "object",
            "properties": {
                "social_media_posts": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "platform": {
                                "type": "string",
                                "description": "The social media platform (e.g., 'Twitter', 'LinkedIn').",
                            },
                            "content": {
                                "type": "string",
                                "description": "The content of the social media post.",
                            },
                        },
                        "required": ["platform", "content"],
                        "additionalProperties": False,
                    },
                }
            },
            "required": ["social_media_posts"],
            "additionalProperties": False,
        }

        response, error = self.openai_client.call_chat_completion(
            messages=prompt_messages,
            schema=schema,
            model=self.config.get("default_model", "gpt-5-nano"),
        )

        # Get the actual cost from the client after the API call
        cost = self.openai_client.latest_cost

        if error or not response:
            self.logger.error(f"Failed to craft social media posts: {error}")
            return None, cost  # Return the actual cost even on failure

        return response.get("social_media_posts"), cost

    def _build_crafting_prompt(
        self, opportunity: Dict[str, Any]
    ) -> list[Dict[str, str]]:
        """Constructs the prompt for the social media crafting AI."""
        ai_content = opportunity.get("ai_content", {})
        article_title = ai_content.get("meta_title", "Untitled")
        article_summary = ai_content.get("meta_description", "No summary available.")
        article_body_html = ai_content.get(
            "article_body_html", ""
        )  # NEW: Get full HTML for parsing

        client_cfg = opportunity.get("client_cfg", {})
        platforms = ", ".join(client_cfg.get("platforms", ["Twitter", "LinkedIn"]))

        # --- Extract key information from the generated article's HTML ---
        soup = BeautifulSoup(article_body_html, "html.parser")

        h1_tag = soup.find("h1")
        # W17 FIX: Ensure h1 extraction is guarded, falling back to a modified title if necessary
        h1_text = (
            h1_tag.get_text(strip=True)
            if h1_tag
            else f"The Article on {article_title.replace(':', ' - ')}"
        )

        # W17 FIX: Extract H2s robustly, filtering out any empty tags
        h2_texts = [
            h.get_text(strip=True)
            for h in soup.find_all("h2")
            if h.get_text(strip=True)
        ]

        key_entities = (
            opportunity.get("blueprint", {})
            .get("ai_content_brief", {})
            .get("key_entities_to_mention", [])
        )

        # --- Social Media Tag Analysis (existing logic) ---
        competitor_social_tags = []
        for competitor in opportunity.get("blueprint", {}).get(
            "competitor_analysis", []
        )[:3]:
            if competitor.get("social_media_tags"):
                tags = competitor["social_media_tags"]
                key_tags = {
                    "og:title": tags.get("og:title"),
                    "og:description": tags.get("og:description"),
                    "twitter:title": tags.get("twitter:title"),
                    "twitter:description": tags.get("twitter:description"),
                }
                competitor_social_tags.append(
                    {
                        "url": competitor["url"],
                        "tags": {k: v for k, v in key_tags.items() if v},
                    }
                )

        competitor_examples = ""
        if competitor_social_tags:
            competitor_examples = (
                "\n**Competitor Social Media Examples (for inspiration):**\n"
            )
            for item in competitor_social_tags:
                competitor_examples += f"- For {item['url']}:\n"
                for tag, value in item["tags"].items():
                    competitor_examples += f"  - {tag}: {value}\n"

        prompt = f"""
        You are a social media marketing expert. Your task is to create engaging social media posts to promote a new blog article.

        **Article Details:**
        - **Primary Headline (H1):** {h1_text} # Now guaranteed to be populated
        - **Key Sections (H2s):** {", ".join(h2_texts[:5]) if h2_texts else "N/A (No subheadings found)"} # Now guaranteed text if available
        - **Summary:** {article_summary}
        - **Key Entities/Topics:** {", ".join(key_entities) if key_entities else "N/A"}
        - **Link (use placeholder):** [LINK]
        {competitor_examples}
        **Instructions:**
        1.  Create a unique post for each of the following platforms: {platforms}.
        2.  Analyze the competitor examples to understand how they frame their content on social media.
        3.  Tailor the tone and length of each post to the specific platform.
        4.  Include relevant hashtags.
        5.  End each post with a call to action and the [LINK] placeholder.
        6.  Ensure posts directly reference information present in the article's headlines and key entities.

        Provide the output in the required JSON format.
        """
        return [{"role": "user", "content": prompt}]
