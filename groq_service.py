import requests
import os
import json
from dotenv import load_dotenv


load_dotenv()

class GroqAPI:
    """
    Groq class used to interact with Groq API
    """
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://api.groq.com/openai/v1/chat/completions"
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

    def _send_request(self, data: dict):
        """Helper method to send POST requests to the Groq API."""
        try:
            response = requests.post(self.base_url, headers=self.headers, data=json.dumps(data))

            # Check for a successful response
            if response.status_code == 200:
                return response.json()  # Parse and return the JSON response
            else:
                print(f"Error: {response.status_code} - {response.text}")
                return None
        except requests.exceptions.RequestException as e:
            print(f"Request failed: {e}")
            return None

    def generate_chat_response(self, prompt: str, model: str = "llama-3.3-70b-versatile"):
        """Send a message to Groq and get the model's response."""
        # Prepare the request data based on the cURL example
        data = {
            "messages": [{"role": "user", "content": prompt}],
            "model": model
        }

        response = self._send_request(data)
        if response:
            return response.get("choices", [{"message": {"content": "No content available."}}])[0]["message"]["content"]
        return "Failed to get a response."


# Example usage
if __name__ == "__main__":
    # Load the API key from environment variables or a .env file
    api_key = os.getenv("GROQ_API_KEY")  # Ensure you have this set in your .env

    if api_key is None:
        print("Error: Please set the GROQ_API_KEY environment variable.")
    else:
        groq_api = GroqAPI(api_key)
        prompt = "Tell me a joke please"

        # Fetch generated content based on the prompt
        generated_content = groq_api.generate_chat_response(prompt)
        print("Generated Content:", generated_content)
