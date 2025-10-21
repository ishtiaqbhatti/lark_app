import os
import requests
import json
import sys
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# --- Configuration ---
DATAFORSEO_LOGIN = os.getenv("DATAFORSEO_LOGIN")
DATAFORSEO_PASSWORD = os.getenv("DATAFORSEO_PASSWORD")
API_URL = "https://api.dataforseo.com/v3/on_page/content_parsing/live"


def fetch_page_content_live(url: str):
    """
    Fetches the parsed content and raw HTML for a given URL using the synchronous
    'live' endpoint of the Dataforseo On-Page Content Parsing API.

    Args:
        url: The URL of the page to analyze.

    Returns:
        A dictionary containing the API response, or None if an error occurs.
    """
    if not DATAFORSEO_LOGIN or not DATAFORSEO_PASSWORD:
        print("Error: Dataforseo credentials not found in .env file.", file=sys.stderr)
        return None

    # The request body is a list containing a dictionary for the URL.
    post_data = [
        {
            "url": url,
            "store_raw_html": True,
            "enable_javascript": False,
            "convert_to_markdown": True,
        }
    ]

    headers = {"Content-Type": "application/json"}

    try:
        print(f"Sending request for URL: {url}", file=sys.stderr)
        response = requests.post(
            API_URL,
            auth=(DATAFORSEO_LOGIN, DATAFORSEO_PASSWORD),
            headers=headers,
            json=post_data,
        )
        # Raise an exception for bad status codes (4xx or 5xx)
        response.raise_for_status()

        response_json = response.json()

        # Check the response status from the API itself
        if response_json.get("status_code") == 20000:
            print(f"Successfully received data for: {url}", file=sys.stderr)
            return response_json
        else:
            status_msg = response_json.get("status_message", "No status message.")
            print(f"API returned an error for '{url}': {status_msg}", file=sys.stderr)
            return None

    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred for URL '{url}': {http_err}", file=sys.stderr)
        print(f"Response content: {response.text}", file=sys.stderr)
        return None
    except requests.exceptions.RequestException as req_err:
        print(f"A request error occurred for URL '{url}': {req_err}", file=sys.stderr)
        return None
    except Exception as e:
        print(f"An unexpected error occurred for URL '{url}': {e}", file=sys.stderr)
        return None


if __name__ == "__main__":
    test_urls = [
        "https://www.theverge.com/2024/02/15/24074327/openai-sora-text-to-video-generator-ai",
        "https://www.wired.com/story/what-is-generative-ai/",
        "https://blog.google/technology/ai/google-gemini-ai/",
    ]

    all_results = []

    print("--- Starting On-Page Content Parsing (Live API) Tests ---", file=sys.stderr)
    for url in test_urls:
        result = fetch_page_content_live(url)
        if result:
            all_results.append(result)
        else:
            # Add a placeholder for failed requests to keep track
            all_results.append({"url": url, "error": "Failed to fetch content"})
        print("-" * 20, file=sys.stderr)

    print("\n--- All Test Results (JSON Output) ---", file=sys.stderr)
    # Use json.dumps to pretty-print the final list of results
    print(json.dumps(all_results, indent=2))
    print("--- Test Run Complete ---", file=sys.stderr)
