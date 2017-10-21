from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation as LDA
import numpy as np
import reddit_parser

import sys


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

if __name__ == "__main__":
    subreddits = ['news']
    limit = 10
    user_agent = "ResearchBot"
    num_topics = 5
    num_words = 10

    posts = reddit_parser.format_posts(reddit_parser.get_posts(subreddits, limit))
    post_bodies = get_bodies(posts)
    timestamps = [post["created"] for post in posts]

    documents = build_documents(zip(posts, post_bodies))
    document_time_pairs = zip(documents, timestamps)

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
    # end michael's code

    lda = LDA(n_topics=num_topics)
    lda.fit(document_word_vectors)

    # michael's code
    w_z = lda.components_ / lda.components_.sum(axis=1)[:, np.newaxis]
    z_d = lda.transform(document_word_vectors)

    top_word_args = np.argsort(w_z, axis=1)[:,-1*num_words:]
    top_words = np.chararray((w_z.shape[0], num_words, 2), itemsize=100)
    for i in range(0, num_topics):
        top_words[i,:,0] = index_to_word[top_word_args[i]]
        top_words[i,:,1] = w_z[i,top_word_args[i]]
    # end michael's code

    print(top_words)