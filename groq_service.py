import requests
import os
import json
from dotenv import load_dotenv


load_dotenv()

class GroqAPI:
    """
        A class to interact with the Groq API for generating AI-driven chat responses.

        Attributes:
            api_key (str): The API key used for authentication with the Groq API.
            base_url (str): The endpoint for the Groq API.
            headers (dict): The HTTP headers used for API requests.
    """

    def __init__(self, api_key: str):
        """
            Initializes the GroqAPI class with the provided API key.

            Args:
                api_key (str): The API key required for authenticating API requests.
        """
        self.api_key = api_key
        self.base_url = "https://api.groq.com/openai/v1/chat/completions"
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

    def _send_request(self, data: dict):
        """
        A helper method to send POST requests to the Groq API.

        Args:
            data (dict): The payload to send in the POST request.

        Returns:
            dict: The JSON response from the Groq API if the request is successful.
            None: If the request fails or the response contains an error.
        """
        try:
            response = requests.post(self.base_url, headers=self.headers, data=json.dumps(data))

            if response.status_code == 200:
                return response.json()
            else:
                print(f"Error: {response.status_code} - {response.text}")
                return None
        except requests.exceptions.RequestException as e:
            print(f"Request failed: {e}")
            return None

    def generate_chat_response(self, prompt: str, model: str = "llama-3.3-70b-versatile"):
        """
                Sends a message to the Groq API and retrieves the model's response.

                Args:
                    prompt (str): The input prompt or query for the AI model.
                    model (str, optional): The model to use for generating responses. Defaults to "llama-3.3-70b-versatile".

                Returns:
                    str: The content of the response from the Groq API if successful.
                    str: An error message if the response fails.
        """
        data = {
            "messages": [{"role": "user", "content": prompt}],
            "model": model
        }

        response = self._send_request(data)
        if response:
            return response.get("choices", [{"message": {"content": "No content available."}}])[0]["message"]["content"]
        return "Failed to get a response."


if __name__ == "__main__":
    api_key = os.getenv("GROQ_API_KEY")

    if api_key is None:
        print("Error: Please set the GROQ_API_KEY environment variable.")
    else:
        groq_api = GroqAPI(api_key)
        prompt = "Tell me a joke please"

        generated_content = groq_api.generate_chat_response(prompt)
        print("Generated Content:", generated_content)
