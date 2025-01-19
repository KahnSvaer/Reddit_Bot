import argparse
from dotenv import load_dotenv
import os

from groq_service import GroqAPI
from reddit_service import RedditService
from schedular import Scheduler

load_dotenv()

# Initialize API keys and constants (Note: You would need to create a .env and fill in the details)
reddit_client_id = os.getenv("REDDIT_CLIENT_ID")
reddit_client_secret = os.getenv("REDDIT_CLIENT_SECRET")
reddit_user_agent = os.getenv("REDDIT_USER_AGENT")
groq_api_key = os.getenv("GROQ_API_KEY")

login_method = {"redirect_uri": "http://localhost:8080"}


reddit_service = RedditService(
    client_id=reddit_client_id,
    client_secret=reddit_client_secret,
    user_agent=reddit_user_agent,
    login_method=login_method
)

groq_service = GroqAPI(api_key=groq_api_key)


def comment_on_top_posts(subreddit: str, time_filter: str, limit: int):
    """
        Fetches top posts from a subreddit and posts comments on them.

        Args:
            subreddit (str): The name of the subreddit to fetch posts from.
            time_filter (str): The time filter for fetching posts (e.g., 'day', 'week').
            limit (int): The maximum number of posts to fetch and comment on.
    """
    posts = reddit_service.get_n_hot_posts(subreddit_name=subreddit, time_filter=time_filter, limit=limit)
    for post in posts:
        prompt = _generate_comment_prompt(post)
        generated_content = groq_service.generate_chat_response(prompt).replace("\"", "")
        reddit_service.comment_on_post(post=post, comment_text=generated_content)


def _generate_comment_prompt(post) -> str:
    """
    Generates a prompt for the Groq API to create a comment.

    Args:
        post: The Reddit post object.

    Returns:
        str: A prompt string formatted for the Groq API.
    """
    return (f"Assume you are a usual Redditor. Write a dad joke, sarcastic comment, or a joke "
            f"underneath the following post. The post title is '{post.title}' and message is '{post.selftext}'.")


def create_posts(subreddit: str):
    """
    Generates and posts content to a subreddit.

    Args:
        subreddit (str): The subreddit where the post will be created.
    """
    prompt = ("Generate a sarcastic Reddit post filled with puns that looks like it was written by someone who is "
              "incredibly tired of life’s absurdities. It should be about a common everyday experience, "
              "like waiting in line, losing socks in the laundry, or trying to get an answer from tech support. "
              "The tone should be dry, full of ironic humor, and a bit ridiculous, as if the person has given "
              "up on life but still finds humor in its chaos. Divide it into clear parts with "
              "title as the first paragraph and text in the next")
    generated_content = groq_service.generate_chat_response(prompt).replace("\"", "")

    lines = generated_content.split("\n")
    title = lines[0][7:] if lines[0].startswith("title:") else lines[0]
    text = "\n".join(lines[1:]).strip()[6:] if lines[1].startswith("text:") else "\n".join(lines[1:]).strip()

    reddit_service.create_post(
        subreddit_name=subreddit,
        title=title,
        content=text,
        post_type="text"
    )


def create_engagement(subreddit: str, limit: int):
    """
        Engages with a subreddit by commenting on posts and creating a new post
        The main function of the entire bot that enables everything else.

        Args:
            subreddit (str): The subreddit to engage with.
            limit (int): The number of posts to comment on.
        """
    comment_on_top_posts(subreddit, "day", limit)
    create_posts(subreddit)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Reddit bot powered by Groq API for posting and commenting.")
    parser.add_argument("--subreddit", type=str, default="ForRedditBotTesting", help="Subreddit to engage with.")
    parser.add_argument("--time", type=str, default="12:00", help="Time for scheduled engagement (HH:MM format).")
    parser.add_argument("--limit", type=int, default=5, help="Number of posts to comment on.")
    args = parser.parse_args()

    Scheduler.start_daily_scheduler(lambda: create_engagement(args.subreddit, args.limit), args.time)
