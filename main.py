from dotenv import load_dotenv
import os

from groq_service import GroqAPI
from reddit_service import RedditService
from schedular import Scheduler

load_dotenv()

reddit_client_id = os.getenv("REDDIT_CLIENT_ID")
reddit_client_secret = os.getenv("REDDIT_CLIENT_SECRET")
reddit_user_agent = os.getenv("REDDIT_USER_AGENT")
groq_api_key = os.getenv("GROQ_API_KEY")

SUBREDDIT = "ForRedditBotTesting" # Private Subreddit


login_method = {"redirect_uri": "http://localhost:8080"}

reddit_service = RedditService(
    client_id=reddit_client_id,  # Replace with your client ID
    client_secret=reddit_client_secret,  # Replace with your client secret
    user_agent=reddit_user_agent,
    login_method=login_method
)

groq_service = GroqAPI(api_key=groq_api_key)

def comment_on_top_posts(subreddit:str = SUBREDDIT, time_filter:str = "day", limit:int = 5):
    posts = reddit_service.get_top_posts(subreddit_name=subreddit,time_filter=time_filter,limit=limit)
    for post in posts:
        try:
            prompt = _generate_comment_prompt(post)
            generated_content = groq_service.generate_chat_response(prompt).replace("\"","")
            reddit_service.comment_on_post(post_id=post.id, comment_text=generated_content)
        except Exception as e:
            print(f"Error while commenting on post {post.id}: {e}")


def _generate_comment_prompt(post) -> str:
    _prompt = ("Assume you are a usual reddit, I want you to write a dad joke comment or sarcastic comment or a joke"
               f" underneath the following post. The post title is {post.title} and message is {post.selftext}")
    return _prompt

def create_posts(subreddit:str = SUBREDDIT, ):
    prompt = ("Generate a sarcastic Reddit post filled with puns that looks like it was written by someone who is "
              "incredibly tired of life’s absurdities. It should be about a common everyday experience, "
              "like waiting in line, losing socks in the laundry, or trying to get an answer from tech support. "
              "The tone should be dry, full of ironic humor, and a bit ridiculous, as if the person has given "
              "up on life but still finds humor in its chaos. Divide it into clear parts with title "
              "starting from 'title:' and text of post starting from 'text:'")
    generated_content = groq_service.generate_chat_response(prompt).replace("\"","")

    lines = generated_content.split("\n")

    # Assuming the title is the first line, the rest is the text
    title = str(lines[0])
    title = title[7:] if title.startswith("title:") else title
    text = "\n".join(lines[1:]).strip()
    text = text[6:] if text.startswith("text:") else text

    reddit_service.create_post(
        subreddit_name=subreddit,
        title=title,
        content=text,
        post_type="text"
    )


def create_engagement():
    comment_on_top_posts()
    create_posts()

Scheduler.start_scheduler(create_engagement)
