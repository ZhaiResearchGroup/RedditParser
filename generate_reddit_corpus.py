import json
from pprint import pprint
import nltk
from nltk.corpus import stopwords

def load_comments(file_path):
    '''
        Takes a 'post comments' file from reddit_parser.py and loads it in
    '''
    with open(file_path) as comments_file:
        comments = json.load(comments_file)
        comments_file.close()

    return comments

def build_document(comments):
    '''
        Takes a list of comment jsons and builds a document from it

        Returns a string of the entire document
    '''
    comment_strings = [_get_clean_body(comment) for comment in comments]
    return ' '.join(comment_strings)

def extract_sentences(document):
    '''
        Extract sentences from a document using nltk
    '''
    return nltk.sent_tokenize(document)

def dump_sentences(sentences, file_path):
    '''
        Dumps a list of sentences into the specified file path
    '''
    with open(file_path, 'w') as out_file:
        for sentence in sentences:
            out_file.write(sentence + '\n')
        out_file.close()

def _get_clean_body(comment):
    '''
        Takes a comment object and returns a cleaned body
    '''
    return comment['body'].replace('\n', ' ').strip()

def _remove_stopwords_and_clean_sentences(sentences):
    '''
        Parameter sentences is a list of strings.

        Returns a list of lists, where each list is a list of words in the sentence.

        **Taken from document_extraction.py in abstractive_summarization.
        TODO: make a separate utils file so this can be reused
    '''
    cleaned_sentences = []
    english_stopwords = set(stopwords.words('english'))

    for sentence in sentences:
        cleaned_sentences.append(' '.join([word for word in sentence.lower().split() if word not in english_stopwords]))

    return cleaned_sentences

if __name__ == "__main__":
    comments = load_comments('output.json')
    document = build_document(comments)
    sentences = extract_sentences(document)
    dump_sentences(sentences, 'corpus.dat')
