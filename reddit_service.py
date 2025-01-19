import praw
from dotenv import load_dotenv
import os
import logging
from code_capture import get_authorization_code


load_dotenv()

class RedditService:
    """
    A service class to interact with Reddit's API using PRAW.

    Features:
        - Fetch top posts from a subreddit
        - Create posts in a subreddit
        - Comment on specific posts
        - Logs all its actions inside bot_running.log file
    """

    def __init__(self, client_id: str, client_secret: str, user_agent: str, login_method: dict):
        """
        Initialize the RedditService with authentication.

        Args:
            client_id (str): Reddit API client ID.
            client_secret (str): Reddit API client secret.
            user_agent (str): Reddit API user agent.
            login_method (dict): A dictionary containing login method details.
                                Use either 'redirect_uri' or 'username' and 'password'.
        """
        self.reddit_handle = None
        self._authorization_code = None
        self.refresh_token = None

        # Configure logging
        logging.basicConfig(
            level=logging.INFO,  # Set the logging level to INFO
            format="%(asctime)s - %(levelname)s - %(message)s",  # Log format
            handlers=[
                logging.FileHandler("bot_running.log", mode='a', encoding='utf-8'),
            ],
        )

        try:
            if "redirect_uri" in login_method:
                logging.info("Initializing RedditService with OAuth2 (redirect URI).")
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
                print("Authorization has been completed and refresh token has been retrieved")

            elif "username" in login_method and "password" in login_method:
                logging.info("Initializing RedditService with username/password authentication.")
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
                logging.info("Authentication successful. Refresh token obtained.")

        except Exception as e:
            logging.error(f"Error during initialization: {e}")
            raise

    def get_n_hot_posts(self, subreddit_name: str, limit: int = 5, time_filter: str = "day"):
        """
        Fetches top n hot posts from a subreddit.

        Args:
            subreddit_name (str): Name of the subreddit.
            limit (int): Number of posts to fetch (default: 5).
            time_filter (str): Time period to consider (default: "day").

        Returns:
            List of hot posts.
        """
        try:
            subreddit = self.reddit_handle.subreddit(subreddit_name)
            posts = subreddit.hot(limit=limit)
            logging.info(f"Fetched top {limit} hot posts from r/{subreddit_name}.")
            return posts
        except Exception as e:
            logging.error(f"Error fetching posts from r/{subreddit_name}: {e}")
            raise

    def comment_on_post(self, post, comment_text: str):
        """
        Comments on a specific post by its ID.

        Args:
            post: Post on which to comment
            comment_text (str): The text of the comment.
        """
        try:
            post_id = post.id
            submission = self.reddit_handle.submission(id=post_id)
            submission.reply(comment_text)
            logging.info(f"Commented on post titled: {post.title}")
        except Exception as e:
            logging.error(f"Error commenting on post {post.title}: {e}")

    def create_post(self, subreddit_name: str, title: str, content: str, post_type: str = "text"):
        """
        Creates a post in a specified subreddit.

        Args:
            subreddit_name (str): Name of the subreddit.
            title (str): Title of the post.
            content (str): Content of the post.
            post_type (str): Type of post ('text' or 'link', default: 'text').
        """
        try:
            subreddit = self.reddit_handle.subreddit(subreddit_name)
            if post_type == "text":
                subreddit.submit(title, selftext=content)
            elif post_type == "link":
                subreddit.submit(title, url=content)
            else:
                raise ValueError("Invalid post_type. Use 'text' or 'link'.")
            logging.info(f"Post created in r/{subreddit_name} with title: {title}")
        except Exception as e:
            logging.error(f"Error creating post in r/{subreddit_name}: {e}")
            raise


if __name__ == "__main__":
    reddit_client_id = os.getenv("REDDIT_CLIENT_ID")
    reddit_client_secret = os.getenv("REDDIT_CLIENT_SECRET")
    reddit_user_agent = os.getenv("REDDIT_USER_AGENT")
    groq_api_key = os.getenv("GROQ_API_KEY")

    login_method = {"redirect_uri": "http://localhost:8080"}

    try:
        reddit_service = RedditService(
            client_id=reddit_client_id,
            client_secret=reddit_client_secret,
            user_agent=reddit_user_agent,
            login_method=login_method
        )

        # Example: Create a post
        reddit_service.create_post(
            subreddit_name="ForRedditBotTesting",
            title="My First Bot Post",
            content="Hello, Reddit! This is a post made using my Python bot.",
            post_type="text"
        )

        # Example: Fetch and comment on top posts
        posts = reddit_service.get_n_hot_posts(subreddit_name='ForRedditBotTesting')
        for post in posts:
            reddit_service.comment_on_post(post=post, comment_text="Great post!")

    except Exception as e:
        logging.critical(f"Critical error in main execution: {e}")
