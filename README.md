# Reddit Bot

A basic Reddit bot designed for user engagement. This bot utilizes Groq AI to automatically generate content and post it to Reddit. The bot also engages with top posts in a specified subreddit by commenting on them with AI-generated responses. It integrates with Reddit’s API and Groq’s AI services for content creation and posting automation.

-----

## Features

- **Automated Post Creation**: The bot can automatically generate and post content to a subreddit using AI-generated text.
- **Top Post Commenting**: The bot comments on top posts within a specified subreddit.
- **Scheduling**: The bot supports scheduling to run daily at user-defined times.
- **Groq API Integration**: The bot leverages Groq AI to generate content for both posts and comments.

-----
## Setup Instructions

### Prerequisites

Ensure you have the following before running the bot:

1. **Python 3.9+**: This bot uses Python for execution.
2. **Reddit API Access**: Create an application in Reddit to get the necessary client credentials (Client ID, Client Secret, User Agent). You can follow [this guide](https://praw.readthedocs.io/en/latest/getting_started/authentication.html) for setting up Reddit API access.
3. **Groq API Key**: Obtain an API key from Groq for content generation.

### Installation

1. Fork the repository on github

2. Clone the repository:

    ```bash
    git clone https://github.com/yourusername/Reddit_Bot.git
    cd Reddit_Bot
    ```

3. Install the required dependencies:

    ```bash
    pip install -r requirements.txt
    ```

4. Create a `.env` file in the root of the project and add the following environment variables:

    ```bash
    REDDIT_CLIENT_ID=your_reddit_client_id
    REDDIT_CLIENT_SECRET=your_reddit_client_secret
    REDDIT_USER_AGENT=your_reddit_user_agent
    GROQ_API_KEY=your_groq_api_key
    ```

5. Make sure to set up your Reddit API and Groq API keys properly.

### Running the Bot

To start the bot, simply run the following command:

```bash
python main.py --subreddit "<Name of you subreddit>" --time "<Time in format of 12:00>" --limit <No of posts>
```

The bot will run according to the schedule you define within the script.

### Scheduling
You can configure the bot to post and comment at specific times by modifying the `time` argument while working with cli.

### Example Usage

1. **Post Creation**:
   - The bot will automatically generate a sarcastic post about everyday situations, like losing socks in the laundry or waiting in line. It uses Groq AI to create content, which is then posted to the specified subreddit.


2. **Commenting**:
   - The bot will comment on the top posts in the given subreddit with AI-generated responses, such as sarcastic comments or jokes. It retrieves the top posts based on user-defined parameters and generates comments using Groq AI.


3. **Scheduling**:
   - The bot uses the `schedule` library to run tasks automatically at user-defined times. You can configure the bot to post and comment on a schedule. For example, to run the bot daily at 12:00 PM:

 
### Logging

All actions performed by the bot, including successful posts, comments, and errors, will be logged in the `bot_running.log` file. This log file helps track bot activity and troubleshoot any issues that arise.

### Error Handling

If an error occurs while posting or commenting, the bot will print an error message and log the error in the log file for further analysis. Make sure to check the log file to monitor any issues with the bot.

-----

## Contribution

Contributions are welcome! If you’d like to improve the bot’s functionality or add new features, feel free to open issues or submit pull requests. Some potential improvements could be:

- Adding more types of content generation for posts and comments.
- Adding multi-threading or asynchronous functionality for improved performance.
- Supporting more Reddit operations, such as upvoting posts or handling media posts.
-----
## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
