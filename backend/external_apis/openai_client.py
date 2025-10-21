from openai import OpenAI
import json
import logging
from typing import Dict, Any, List, Optional, Tuple
import time


class OpenAIClientWrapper:
    """
    Provides a robust wrapper for OpenAI API calls,
    handling authentication, retries, and structured outputs (JSON object format).
    """

    def __init__(self, api_key: str, client_cfg: Dict[str, Any]):
        if not api_key:
            raise ValueError("OpenAI API key is required.")
        self.client = OpenAI(api_key=api_key)
        self.logger = logging.getLogger(self.__class__.__name__)
        self.client_cfg = client_cfg
        self.latest_cost = 0.0

    def _calculate_cost(self, usage: Dict[str, Any], model: str) -> float:
        """Calculates the cost of a chat completion based on token usage."""
        # Pricing per 1M tokens
        pricing = {
            "gpt-4o": {"input": 5.00, "output": 15.00},
            "gpt-3.5-turbo": {"input": 0.50, "output": 1.50},
        }
        model_pricing = pricing.get(
            model, pricing["gpt-4o"]
        )  # Default to gpt-4o pricing

        prompt_tokens = usage.get("prompt_tokens", 0)
        completion_tokens = usage.get("completion_tokens", 0)

        input_cost = (prompt_tokens / 1_000_000) * model_pricing["input"]
        output_cost = (completion_tokens / 1_000_000) * model_pricing["output"]

        return input_cost + output_cost
        pass

    def call_chat_completion(
        self,
        messages: List[Dict[str, str]],
        schema: Optional[Dict[str, Any]] = None,
        model: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 4096,
        retries: int = 3,
    ) -> Tuple[Optional[Dict[str, Any]], Optional[str]]:
        """
        Makes a robust OpenAI chat completion call, optionally enforcing JSON output
        and calculating the cost.
        """
        if model is None:
            model = self.client_cfg.get('default_model', 'gpt-5-nano')
        
        self.latest_cost = 0.0
        for attempt in range(retries):
            try:
                response_kwargs = {
                    "model": model,
                    "messages": messages,
                    "temperature": temperature,
                    "max_tokens": max_tokens,
                }

                # gpt-5-nano and gpt-5-mini do not support temperature
                if model in ['gpt-5-nano', 'gpt-5-mini']:
                    del response_kwargs['temperature']

                if schema:
                    if model in ['gpt-5-nano', 'gpt-5-mini']:
                        response_kwargs["response_format"] = {"type": "json_object"}
                    else:
                        response_kwargs["response_format"] = {
                            "type": "json_schema",
                            "json_schema": {
                                "name": schema.get("name", "structured_output"),
                                "schema": schema,
                                "strict": True,
                            },
                        }

                response = self.client.chat.completions.create(**response_kwargs)

                if response.choices and response.choices[0].finish_reason == "length":
                    self.logger.warning(
                        f"OpenAI API response was truncated because the token limit was reached. "
                        f"Consider increasing 'max_tokens_for_generation' in settings.ini. "
                        f"Current limit for this call: {max_tokens}."
                    )

                if response.usage:
                    self.latest_cost = self._calculate_cost(
                        response.usage.dict(), model
                    )

                if response.choices and response.choices[0].message.content:
                    if schema:
                        try:
                            parsed_output = json.loads(
                                response.choices[0].message.content
                            )
                            self.logger.info(
                                f"Successfully parsed structured output from OpenAI (Attempt {attempt + 1}/{retries}). Cost: ${self.latest_cost:.4f}"
                            )
                            return parsed_output, None
                        except json.JSONDecodeError as e:
                            self.logger.warning(
                                f"Failed to decode JSON from OpenAI (Attempt {attempt + 1}/{retries}): {e}."
                            )
                            continue
                    else:
                        return response.choices[0].message.content, None

                self.logger.warning(
                    f"OpenAI returned no content (Attempt {attempt + 1}/{retries})."
                )
                continue

            except Exception as e:
                self.logger.error(
                    f"OpenAI API call failed (Attempt {attempt + 1}/{retries}): {e}"
                )
                if attempt < retries - 1:
                    time.sleep(5 * (attempt + 1))
                    continue
                return None, str(e)

        return None, "All OpenAI API call attempts failed."

    def call_image_generation(
        self,
        prompt: str,
        style_formula: str,
        quality: str,
        size: str,
        model: Optional[str] = None,
        retries: int = 3,
    ) -> Tuple[Optional[str], Optional[str], Optional[str]]:
        """
        Mocks OpenAI image generation. This function is present but *not used* in the final plan
        as Pexels is the exclusive image source. It's kept for potential future re-integration.
        """
        if model is None:
            model = self.client_cfg.get('default_image_model', 'dall-e-3')
        
        self.logger.info(
            "OpenAI image generation is configured but Pexels is prioritized. This function will not be called."
        )
        return (
            None,
            None,
            "OpenAI image generation bypassed; Pexels is the primary source.",
        )
