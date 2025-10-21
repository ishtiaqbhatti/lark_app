# tests/test_onpage_instant_pages.py
import os
import json
import logging
import base64
import requests
from dotenv import load_dotenv

TEST_URL = "https://www.wikipedia.org/"
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


def test_instant_pages_workflow():
    load_dotenv()
    api_login = os.getenv("DATAFORSEO_LOGIN")
    api_password = os.getenv("DATAFORSEO_PASSWORD")
    assert api_login and api_password, "DATAFORSEO credentials not found in .env file."

    credentials = f"{api_login}:{api_password}"
    headers = {
        "Authorization": f"Basic {base64.b64encode(credentials.encode()).decode()}",
        "Content-Type": "application/json",
    }

    post_data = [{"url": TEST_URL, "enable_browser_rendering": True}]

    response = requests.post(
        "https://api.dataforseo.com/v3/on_page/instant_pages",
        headers=headers,
        data=json.dumps(post_data),
        timeout=120,
    )
    response.raise_for_status()
    response_json = response.json()

    assert response_json["status_code"] == 20000, "API call was not successful."
    task_result = response_json["tasks"][0]["result"][0]
    item = task_result["items"][0]

    assert "meta" in item, "Response missing 'meta' object."
    assert "content" in item["meta"], "Response missing 'meta.content' object."
    assert "plain_text_word_count" in item["meta"]["content"], (
        "Content parsing failed: word count is missing."
    )

    word_count = item["meta"]["content"]["plain_text_word_count"]
    assert isinstance(word_count, int) and word_count > 50, (
        f"Expected a valid word count, got {word_count}."
    )

    logging.info(
        f"SUCCESS: 'instant_pages' test passed. Found word count: {word_count}."
    )
    print(json.dumps(item["meta"]["content"], indent=2))


if __name__ == "__main__":
    test_instant_pages_workflow()
