import requests
import json
from reddit_constants import default_user_agent

def get_posts(subreddits, limit, user_agent=default_user_agent):
    """Returns a specified number of posts from a specified group of subreddits."""
    all_posts = []

    for subreddit in subreddits:
        data_url = 'https://www.reddit.com/r/{}.json?limit={}'.format(subreddit, limit)
        response_data = requests.get(data_url, headers = {'User-agent': user_agent})

        posts = response_data.json()['data']['children']

        all_posts.extend(posts)

    return all_posts

def get_post_comments(post_url, user_agent=default_user_agent):
    """Returns the comment data for a specified post."""
    response_data = requests.get(post_url, headers = {'User-agent': user_agent})
    comment_data = response_data.json()[1]

    some_comments = comment_data['data']['children']
    for comment in some_comments:
        if 'body' in comment['data']:
            print(comment['data']['body'])

if __name__ == "__main__":
    subreddits = ['all', 'news', 'worldnews', 'programmerhumor']
    limit = 500
    user_agent = 'ResearchBot'

    posts = get_posts(subreddits, limit)
    
    post_url = 'https://www.reddit.com' + posts[0]['data']['permalink'] + '.json'
    print(post_url)
    get_post_comments(post_url)