import requests
import json
import uuid
from reddit_constants import default_user_agent

# example JSON is available in post.json, subreddit.json, and output.json

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

    # right now this gets the title, eventually convert to unique id for each title
    post_id = response_data.json()[0]['data']['children'][0]['data']['title']

    return get_post_comments_recur(post_data, [], -1, post_id)

def get_post_comments_recur(comment, comments, parent_comment_id, parent_post_id):
    """Recursive helper function to gather all comments in a Reddit thread.
    
    Right now this function is only getting 200 comments because that is all is shown on the
    JSON page for the post. There are properties called 'more' with lists of id's. Perhaps 
    those can be a link to a complete set of comments.
    """
    if 'data' in comment:
        comment_data = comment['data']

        new_comment = None

        # a new comment exists at this layer, add it to the total list of comments
        if 'body' in comment_data:
            new_comment = {
                "score": comment_data['score'],
                "body": comment_data['body'],
                "subreddit": comment_data['subreddit'],
                "author": comment_data['author'],
                "parent_comment_id": parent_comment_id,
                "parent_post_id": parent_post_id,
                "id": str(uuid.uuid4())
            }
            comments.append(new_comment)

        next_parent_comment_id = parent_comment_id if new_comment is None else new_comment['id']

        # recurse on children
        if 'children' in comment_data:
            for child in comment_data['children']:
                comments = get_post_comments_recur(child, comments, next_parent_comment_id, parent_post_id)

        # recurse on replies
        if 'replies' in comment_data:
            comments = get_post_comments_recur(comment_data['replies'], comments, next_parent_comment_id, parent_post_id)

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