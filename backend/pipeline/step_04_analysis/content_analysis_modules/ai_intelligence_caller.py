from typing import List, Dict, Any, Tuple
from external_apis.openai_client import OpenAIClientWrapper


def get_ai_content_analysis(
    openai_client: OpenAIClientWrapper,
    messages: List[Dict[str, str]],
    model: str,
    max_completion_tokens: int,
) -> Tuple[Dict[str, Any], str]:
    """
    Calls the OpenAI API to get content analysis and returns the response and any error.
    """
    schema = {
        "name": "extract_deep_content_insights",
        "type": "object",
        "properties": {
            "unique_angles_to_include": {"type": "array", "items": {"type": "string"}},
            "key_entities_from_competitors": {
                "type": "array",
                "items": {"type": "string"},
            },
            "core_questions_answered_by_competitors": {
                "type": "array",
                "items": {"type": "string"},
            },
            "identified_content_gaps": {"type": "array", "items": {"type": "string"}},
        },
        "required": [
            "unique_angles_to_include",
            "key_entities_from_competitors",
            "core_questions_answered_by_competitors",
            "identified_content_gaps",
        ],
        "additionalProperties": False,
    }

    response, error = openai_client.call_chat_completion(
        messages=messages,
        schema=schema,
        model=model,
        max_completion_tokens=max_completion_tokens,
    )

    return response, error
