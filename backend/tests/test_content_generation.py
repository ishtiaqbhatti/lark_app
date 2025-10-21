import pytest
from unittest.mock import MagicMock, patch
from backend.external_apis.openai_client import OpenAIClientWrapper
from backend.pipeline.step_04_analysis.content_analyzer import ContentAnalyzer

@pytest.fixture
def mock_openai_client():
    """Mocks the OpenAIClientWrapper to avoid actual API calls."""
    client = MagicMock(spec=OpenAIClientWrapper)
    client.latest_cost = 0.1
    return client

@pytest.fixture
def content_analyzer(mock_openai_client):
    """Provides a ContentAnalyzer instance with a mocked OpenAI client."""
    config = {
        "default_model": "gpt-5-nano",
        "max_completion_tokens_for_generation": 8192,
    }
    return ContentAnalyzer(openai_client=mock_openai_client, config=config)

def test_openai_client_enforces_json_schema_mode():
    """
    Verifies that the OpenAI client wrapper correctly uses 'json_schema' mode
    for gpt-5-nano and gpt-5-mini when a schema is provided.
    """
    with patch('openai.OpenAI') as mock_openai:
        # Arrange
        mock_create = MagicMock()
        mock_openai.return_value.chat.completions.create = mock_create

        client_wrapper = OpenAIClientWrapper(api_key="fake_key", client_cfg={})
        messages = [{"role": "user", "content": "Test prompt"}]
        schema = {"type": "object", "properties": {"key": {"type": "string"}}}

        # Act
        client_wrapper.call_chat_completion(
            messages=messages,
            schema=schema,
            model='gpt-5-nano' # Test with one of the target models
        )

        # Assert
        mock_create.assert_called_once()
        call_args = mock_create.call_args.kwargs
        assert "response_format" in call_args
        assert call_args["response_format"]["type"] == "json_schema"
        assert "json_schema" in call_args["response_format"]

def test_full_content_analysis_and_outline_workflow(content_analyzer, mock_openai_client):
    """
    Tests the full content analysis and outline generation workflow,
    ensuring it handles mocked AI responses correctly and produces a valid output.
    """
    # Arrange: Mock the return values for the two AI calls
    mock_synthesis_response = {
        "unique_angles_to_include": ["Angle 1", "Angle 2"],
        "key_entities_from_competitors": ["Entity A", "Entity B"],
        "core_questions_answered_by_serp": ["Question 1?", "Question 2?"],
        "identified_content_gaps": ["Gap A", "Gap B"],
    }
    mock_outline_response = {
        "article_structure": [
            {"h2": "Introduction", "h3s": []},
            {"h2": "Main Topic", "h3s": ["Sub-topic 1", "Sub-topic 2"]},
            {"h2": "Conclusion", "h3s": []},
        ]
    }
    # The client will return these values in order for the two calls
    mock_openai_client.call_chat_completion.side_effect = [
        (mock_synthesis_response, None),
        (mock_outline_response, None)
    ]

    keyword = "test keyword"
    serp_overview = {"paa_questions": ["PAA Question 1?"]}

    # Act: Run the synthesis and outline generation
    content_intelligence, total_cost_synthesis = content_analyzer.synthesize_content_intelligence(
        keyword=keyword,
        serp_overview=serp_overview,
        competitor_analysis=[] # Use the SERP-only path
    )

    outline, total_cost_outline = content_analyzer.generate_ai_outline(
        keyword=keyword,
        serp_overview=serp_overview,
        content_intelligence=content_intelligence
    )

    # Assert
    assert total_cost_synthesis == 0.1
    assert total_cost_outline == 0.1
    assert "unique_angles_to_include" in content_intelligence
    assert "article_structure" in outline
    assert len(outline["article_structure"]) == 3
    assert outline["article_structure"][1]["h2"] == "Main Topic"
    assert "Sub-topic 1" in outline["article_structure"][1]["h3s"]
    assert mock_openai_client.call_chat_completion.call_count == 2

print("Test script created at backend/tests/test_content_generation.py")
print("You can run this test using pytest:")
print("pytest backend/tests/test_content_generation.py")
