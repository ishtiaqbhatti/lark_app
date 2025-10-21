import logging
from typing import Dict, Any, List, Tuple

from backend.external_apis.openai_client import OpenAIClientWrapper
from backend.data_access.database_manager import DatabaseManager


class InternalLinkingSuggester:
    def __init__(
        self,
        openai_client: OpenAIClientWrapper,
        config: Dict[str, Any],
        db_manager: DatabaseManager,
    ):
        self.openai_client = openai_client
        self.config = config
        self.db_manager = db_manager
        self.logger = logging.getLogger(self.__class__.__name__)

    def suggest_links(
        self,
        article_text: str,
        key_entities: List[str],
        target_domain: str,
        client_id: str,
    ) -> Tuple[List[Dict[str, str]], float]:
        existing_articles = self._fetch_existing_articles(client_id)
        if not existing_articles:
            return [], 0.0

        prompt_messages = self._build_suggestion_prompt(
            article_text, key_entities, existing_articles
        )

        schema = {
            "name": "suggest_contextual_internal_links",
            "type": "object",
            "properties": {
                "internal_links": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "anchor_text": {
                                "type": "string",
                                "description": "The exact, natural phrase from the paragraph to be used as anchor text.",
                            },
                            "url": {
                                "type": "string",
                                "description": "The corresponding relative URL from the available articles list.",
                            },
                            "context_paragraph_text": {
                                "type": "string",
                                "description": "The full, exact text of the paragraph where the anchor text was found. This will be used to pinpoint the link location.",
                            },
                        },
                        "required": ["anchor_text", "url", "context_paragraph_text"],
                        "additionalProperties": False,
                    },
                }
            },
            "required": ["internal_links"],
            "additionalProperties": False,
        }

        response, error = self.openai_client.call_chat_completion(
            messages=prompt_messages,
            schema=schema,
            model=self.config.get("default_model", "gpt-5-nano"),
        )

        if error or not response:
            self.logger.error(
                f"Failed to get contextual internal linking suggestions from AI: {error}"
            )
            return [], self.openai_client.latest_cost

        return response.get("internal_links", []), self.openai_client.latest_cost

    def _fetch_existing_articles(self, client_id: str) -> List[Dict[str, str]]:
        """
        Fetches a list of already 'generated' articles for the given client from the local DB.
        """
        self.logger.info(
            f"Fetching existing published articles for internal linking for client: {client_id}."
        )

        if not self.config.get("enable_automated_internal_linking", False):
            self.logger.info(
                "Automated internal linking is disabled by client configuration."
            )
            return []

        existing_articles = self.db_manager.get_published_articles_for_linking(
            client_id
        )

        if not existing_articles:
            self.logger.warning(
                f"No existing 'published' articles found for client '{client_id}' to use for internal linking suggestions."
            )
            return []

        self.logger.info(
            f"Found {len(existing_articles)} published articles for internal linking."
        )
        return existing_articles

    def _build_suggestion_prompt(
        self,
        linking_context: str,
        key_entities: List[str],
        existing_articles: List[Dict[str, str]],
    ) -> List[Dict[str, str]]:
        """Builds the prompt for context-aware AI internal linking suggestion."""

        existing_articles_text = "\n".join(
            [
                f'- Title: "{article["title"]}", Relative URL: {article["url"]}'
                for article in existing_articles
            ]
        )

        prompt = f"""
        You are an expert SEO strategist. Your task is to analyze a new blog post and identify the most semantically relevant opportunities to link to existing articles on the site.

        **Main Article Text (as HTML):**
        ```html
        {linking_context}
        ```

        **Available Published Articles to Link To:**
        {existing_articles_text}

        **Instructions:**
        1. Read the main article HTML thoroughly to understand its context and structure.
        2. For each available published article, identify the single BEST paragraph in the main article to place a link. The best location is one that is highly contextually and semantically related to the title of the published article.
        3. From that best location, extract a natural, compelling phrase of 3-7 words to use as the anchor text.
        4. Suggest a maximum of 3-5 of the most relevant internal links.
        5. Return your suggestions in the required JSON format. For 'context_paragraph_text', provide the full, clean text content of the paragraph where the link should be placed.
        """
        return [{"role": "user", "content": prompt}]
