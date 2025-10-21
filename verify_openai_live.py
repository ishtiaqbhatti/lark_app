import os
import sys
import asyncio
from backend.app_config.manager import ConfigManager
from backend.external_apis.openai_client import OpenAIClientWrapper

# Add the project root to the Python path to allow imports
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

async def run_live_openai_test():
    """
    Performs a live test of the OpenAIClientWrapper to verify that
    it correctly uses json_schema mode and receives a structured response.
    """
    print("--- Starting Live OpenAI Verification Test ---")

    try:
        # 1. Load Configuration
        print("Loading configuration from .env and settings.ini...")
        config_manager = ConfigManager()
        global_config = config_manager.get_global_config()
        api_key = global_config.get("openai_api_key")

        if not api_key:
            print("\nERROR: OPENAI_API_KEY not found in .env file.")
            print("Please ensure the .env file exists in the project root and contains your key.")
            return

        print("Configuration loaded successfully.")

        # 2. Initialize the Real OpenAI Client
        print("Initializing OpenAIClientWrapper...")
        # Pass a minimal client_cfg, as it's not the focus of this test
        client_wrapper = OpenAIClientWrapper(api_key=api_key, client_cfg={"default_model": "gpt-5-nano"})
        print("Client initialized.")

        # 3. Define a Simple Prompt and Schema
        messages = [
            {"role": "system", "content": "You are a helpful assistant designed to output JSON."}, 
            {"role": "user", "content": "Extract the user's name and age from the following sentence: 'My name is John and I am 30 years old.'"}
        ]
        schema = {
            "name": "user_details",
            "type": "object",
            "properties": {
                "name": {"type": "string", "description": "The name of the user."},
                "age": {"type": "integer", "description": "The age of the user."}
            },
            "required": ["name", "age"]
        }
        print("\nDefined test prompt and schema.")

        # 4. Make the Live API Call
        print("Making a real API call to OpenAI using json_schema mode...")
        response, error = client_wrapper.call_chat_completion(
            messages=messages,
            schema=schema,
            model="gpt-5-nano" # Using a fast and cheap model for the test
        )

        # 5. Verify the Result
        print("\n--- Test Result ---")
        if error:
            print(f"API call failed with an error: {error}")
        elif response:
            print("API call successful!")
            print(f"Received structured data: {response}")
            print(f"Cost for this call: ${client_wrapper.latest_cost:.6f}")

            # Assertions to programmatically verify the result
            assert isinstance(response, dict), "Response is not a dictionary."
            assert "name" in response, "Response is missing the 'name' key."
            assert "age" in response, "Response is missing the 'age' key."
            assert response["name"] == "John", f"Incorrect name extracted: {response['name']}"
            assert response["age"] == 30, f"Incorrect age extracted: {response['age']}"
            print("\nVerification PASSED: The response is a valid, structured JSON object with the correct data.")
        else:
            print("API call returned no response and no error.")

    except Exception as e:
        print(f"\nAn unexpected error occurred during the test: {e}")

if __name__ == "__main__":
    # This allows running the async function from a simple script
    asyncio.run(run_live_openai_test())
