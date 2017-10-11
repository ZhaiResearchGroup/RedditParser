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
    post_data = response_data.json()[1]

    return get_post_comments_recur(post_data, [])

def get_post_comments_recur(comment, comments):
    """Recursive helper function to gather all comments in a Reddit thread.
    
    Right now this function is only getting 200 comments because that is all is shown on the
    JSON page for the post. There are properties called 'more' with lists of id's. Perhaps 
    those can be a link to a complete set of comments.
    """
    if 'data' in comment:
        comment_data = comment['data']

        # a new comment exists at this layer, add it to the total list of comments
        if 'body' in comment_data:
            new_comment = {
                "score": comment_data['score'],
                "body": comment_data['body'],
                "subreddit": comment_data['subreddit'],
                "author": comment_data['author']
            }
            comments.append(new_comment)

        # recurse on children
        if 'children' in comment_data:
            for child in comment_data['children']:
                comments = get_post_comments_recur(child, comments)

        # recurse on replies
        if 'replies' in comment_data:
            comments = get_post_comments_recur(comment_data['replies'], comments)

    return comments

if __name__ == "__main__":
    subreddits = ['news', 'worldnews', 'programmerhumor']
    limit = 500
    user_agent = 'ResearchBot'

    posts = get_posts(subreddits, limit)
    
    post_url = 'https://www.reddit.com' + posts[0]['data']['permalink'] + '.json'

    print(post_url)

    post_comments = get_post_comments(post_url)
    print(json.dumps(post_comments))