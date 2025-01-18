from builtins import str

import praw
from dotenv import load_dotenv
import os

from code_capture import get_authorization_code

load_dotenv()

class RedditService:
    """
    A reddit Service class with the function to interact with reddit
    """
    def __init__(self, client_id: str, client_secret: str, user_agent: str, login_method: dict):
        self.reddit_handle = None
        self._authorization_code = None
        self.refresh_token = None

        if "redirect_uri" in login_method:
            self.reddit_handle = praw.Reddit(
                client_id=client_id,
                client_secret=client_secret,
                user_agent=user_agent,
                redirect_uri=login_method["redirect_uri"]
            )

            auth_url = self.reddit_handle.auth.url(
                scopes=["identity", "submit", "read"],
                state="random_state",
                duration="permanent"
            )
            print(f"Open this URL to authorize: {auth_url}")

            self._authorization_code = get_authorization_code()
            self.refresh_token = self.reddit_handle.auth.authorize(self._authorization_code)

        elif "username" in login_method and "password" in login_method:
            self.reddit_handle = praw.Reddit(
                client_id=client_id,
                client_secret=client_secret,
                user_agent=user_agent,
                username=login_method["username"],
                password=login_method["password"]
            )
            self.refresh_token = self.reddit_handle.auth.authorize()

        if self.refresh_token:
            self.reddit_handle.refresh_token = self.refresh_token


    def get_top_posts(self, subreddit_name: str, limit: int = 5, time_filter:str = "day"):
        """Fetches the top posts from a specified subreddit."""
        subreddit = self.reddit_handle.subreddit(subreddit_name)
        return subreddit.top(limit=limit, time_filter=time_filter)


    def comment_on_post(self, post_id: str, comment_text: str):
        """Comments on a specific post by its ID."""
        submission = self.reddit_handle.submission(id=post_id)
        submission.reply(comment_text)
        print(f"Commented on post: {post_id}")


    def create_post(self, subreddit_name: str, title: str, content: str, post_type: str = "text"):
        """Creates a post in the specified subreddit."""
        subreddit = self.reddit_handle.subreddit(subreddit_name)
        if post_type == "text":
            subreddit.submit(title, selftext=content)
        elif post_type == "link":
            subreddit.submit(title, url=content)
        else:
            raise ValueError("Invalid post_type. Use 'text' or 'link'.")
        print(f"Post created in r/{subreddit_name}: {title}")




if __name__ == "__main__":
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

    # reddit_service.create_post(
    #     subreddit_name="ForRedditBotTesting",
    #     title="My First Bot Post",
    #     content="Hello, Reddit! This is a post made using my Python bot.",
    #     post_type="text"
    # )

    posts = reddit_service.get_top_posts(
        subreddit_name='ForRedditBotTesting',
    )

    for post in posts:
        reddit_service.comment_on_post(post_id = post.id, comment_text="Great post!")
