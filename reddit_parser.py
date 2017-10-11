import praw
from reddit_api_keys import client_id, client_secret, password, user_agent, username

if __name__ == "__main__":
    reddit = praw.Reddit(client_id=client_id,
                     client_secret=client_secret,
                     password=password,
                     user_agent=user_agent,
                     username=username)