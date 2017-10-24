from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation as LDA
import numpy as np
import reddit_parser

from datetime import datetime, timedelta
import sys
from matplotlib import pyplot as plt

def get_bodies(items):
    """Gets all of the bodies associated with inputted posts or comments"""
    return [item['body'] for item in items]

def concatenate_comments_to_post(post_body, comments):
    """Returns a combined document of a post body and comment bodies"""
    comment_bodies = get_bodies(comments)
    document = post_body

    for comment in comment_bodies:
        document += "\n" + comment

    return document

def build_documents(post_pairs):
    """Combines the body and comments of a post into a single document
    Returns a list of documents
    """
    documents = []

    for post, post_body in post_pairs:
        comments = reddit_parser.get_post_comments(post)
        documents.append(concatenate_comments_to_post(post_body, comments))

    return documents

def get_min_max_time(posts):
    """Returns the oldest and newest times for any post in the set"""
    min = sys.maxsize
    max = -sys.maxsize - 1

    for post in posts:
        if post['created'] < min:
            min = post['created']
        if post['created'] > max:
            max = post['created']

    return (min, max)

def generate_time_range(min_time, max_time, num_topics):
    """Create an empty map of the time ranges from the min time to the max time"""
    times = {}

    while min_time < max_time:
        times[min_time] = np.zeros(num_topics)
        min_time += timedelta(hours = 1)

    return times

def increment_time_range_for_topic(time_topic_distribution, topic, timestamp):
    """Increments the topic count at a specific time in the distribution"""
    for time in time_topic_distribution:
        if timestamp < time:
            time_topic_distribution[time][topic] += 1
            break

def format_topic_counts(time_topic_distribution):
    topic_counts = [[], [], [], [], []]
    for time in time_topic_distribution:
        topics = time_topic_distribution[time]
        for i in range(0, len(topics)):
            topic_counts[i].append(topics[i])

    return topic_counts

if __name__ == "__main__":
    subreddits = ['news']
    limit = 100
    user_agent = "ResearchBot"
    num_topics = 5
    num_words = 10

    posts = reddit_parser.format_posts(reddit_parser.get_posts(subreddits, limit))
    post_bodies = get_bodies(posts)
    timestamps = [post["created"] for post in posts]
    datetime_stamps = [str(datetime.fromtimestamp(timestamp)) for timestamp in timestamps]

    documents = build_documents(zip(posts, post_bodies))

    # michael's code
    vectorizer = CountVectorizer()
    vectorizer.fit(documents)
    document_word_vectors = vectorizer.transform(documents)

    word_to_index = vectorizer.vocabulary_
    index_to_word = np.chararray(len(word_to_index), itemsize=100)
    for word in word_to_index:
        index = word_to_index[word]
        try:
            index_to_word[index] = word
        except UnicodeEncodeError:
            print("")

    lda = LDA(n_topics=num_topics)
    lda.fit(document_word_vectors)

    # p(word|topic)  (n_topics X n_words)
    w_z = lda.components_ / lda.components_.sum(axis=1)[:, np.newaxis]

    # p(topic|document)  (n_documents X n_topics)
    z_d = lda.transform(document_word_vectors)

    top_word_args = np.argsort(w_z, axis=1)[:,-1*num_words:]
    top_words = np.chararray((w_z.shape[0], num_words, 2), itemsize=100)
    for i in range(0, num_topics):
        top_words[i,:,0] = index_to_word[top_word_args[i]]
        top_words[i,:,1] = w_z[i,top_word_args[i]]
    # end michael's code

    min_time, max_time = get_min_max_time(posts)

    datetime_min_time = datetime.fromtimestamp(min_time)
    datetime_max_time = datetime.fromtimestamp(max_time)

    time_topic_distribution = generate_time_range(datetime_min_time, datetime_max_time, num_topics)

    document_topics = np.argmax(z_d, axis = 1)

    for i in range(0, len(z_d)):
        doc_timestamp = timestamps[i]
        doc_datetime = datetime.fromtimestamp(doc_timestamp)
        document_topic = document_topics[i]

        increment_time_range_for_topic(time_topic_distribution, document_topic, doc_datetime)

    print(time_topic_distribution)

    # plotting is messed up.

    topic_counts = format_topic_counts(time_topic_distribution)

    num_bars = len(timestamps)
    width = .35
    for topic_count in topic_counts:
        plt.hist(num_bars, topic_count, width)

    plt.xlabel('Times')
    plt.ylabel('Topic Counts')
    plt.xticks(np.arange(num_bars), datetime_stamps)
    plt.yticks(np.arange(0, 10, 1))
    plt.show()