from dotenv import load_dotenv
import os

from groq_service import GroqAPI
from reddit_service import RedditService


load_dotenv()

reddit_client_id = os.getenv("REDDIT_CLIENT_ID")
reddit_client_secret = os.getenv("REDDIT_CLIENT_SECRET")
reddit_user_agent = os.getenv("REDDIT_USER_AGENT")
groq_api_key = os.getenv("GROQ_API_KEY")


login_method = {"redirect_uri": "http://localhost:8080"}

reddit_service = RedditService(
    client_id=reddit_client_id,  # Replace with your client ID
    client_secret=reddit_client_secret,  # Replace with your client secret
    user_agent=reddit_user_agent,
    login_method=login_method
)

groq_service = GroqAPI(api_key=groq_api_key)

