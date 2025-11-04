# backend/services/ai_clustering_service.py
import logging
from typing import List, Dict, Any, Tuple
from backend.external_apis.openai_client import OpenAIClientWrapper

class AIClusteringService:
    def __init__(self, openai_client: OpenAIClientWrapper, config: Dict[str, Any]):
        self.openai_client = openai_client
        self.config = config
        self.logger = logging.getLogger(self.__class__.__name__)

    def generate_topic_clusters(self, keywords: List[str]) -> Tuple[List[Dict[str, Any]], float]:
        """
        Uses an AI model to group a list of keywords into thematic sub-topics for an article outline.
        """
        if not keywords:
            return [], 0.0

        # Truncate if the list is too long to prevent token limit errors
        max_keywords_for_clustering = self.config.get("max_keywords_for_clustering", 200)
        if len(keywords) > max_keywords_for_clustering:
            self.logger.warning(f"Keyword list for clustering is too long ({len(keywords)}). Truncating to {max_keywords_for_clustering}.")
            keywords = keywords[:max_keywords_for_clustering]

        prompt_messages = self._build_clustering_prompt(keywords)

        schema = {
            "name": "generate_keyword_clusters",
            "type": "object",
            "properties": {
                "topic_clusters": {
                    "type": "array",
                    "description": "An array of thematic topic clusters.",
                    "items": {
                        "type": "object",
                        "properties": {
                            "topic_name": {
                                "type": "string",
                                "description": "A concise, descriptive name for the topic cluster, suitable as an H2 heading.",
                            },
                            "keywords": {
                                "type": "array",
                                "description": "A list of keywords from the original input that belong to this topic.",
                                "items": {"type": "string"},
                            },
                        },
                        "required": ["topic_name", "keywords"],
                    },
                }
            },
            "required": ["topic_clusters"],
        }

        response, error = self.openai_client.call_chat_completion(
            messages=prompt_messages,
            schema=schema,
            model=self.config.get("default_model", "gpt-5-nano"),
            temperature=0.3,
        )

        cost = self.openai_client.latest_cost

        if error or not response or "topic_clusters" not in response:
            self.logger.error(f"Failed to generate topic clusters from AI: {error}")
            return [], cost

        return response["topic_clusters"], cost

    def _build_clustering_prompt(self, keywords: List[str]) -> List[Dict[str, str]]:
        keyword_list_str = "\n".join(f"- {kw}" for kw in keywords)

        prompt = f"""
        You are an expert SEO content strategist and information architect. Your task is to analyze the following list of keywords and group them into logical, thematic sub-topics. Each sub-topic should be suitable as an H2 heading for a single, comprehensive blog post.

        **Keyword List:**
        {keyword_list_str}

        **Instructions:**
        1.  Analyze all keywords to understand the overarching theme and user intents.
        2.  Group related keywords into distinct thematic clusters.
        3.  For each cluster, create a concise and descriptive `topic_name` that would serve as an excellent H2 heading.
        4.  Ensure every keyword from the original list is assigned to exactly one cluster.
        5.  The final output must be a JSON object that strictly adheres to the provided schema.
        """
        return [{"role": "user", "content": prompt}]