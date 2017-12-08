import argparse
import nltk
from nltk.corpus import stopwords
from reddit_data_reader import read_reddit_data_and_timestamps

CORPUS_FILE = 'reddit_corpus.dat'
REDDIT_DATA_FILE = 'reddit_documents.dat'
TIMESTAMPS_FILE = 'timestamps.dat'
STOPWORDS_FILE = 'stopwords.txt'

def extract_sentences(documents):
    '''
        Extracts all the sentences from a list of reddit-data documents
    '''
    sentences = []
    for document in documents:
        words = [str(word, 'utf-8') for word in document]
        text_document = ' '.join(words)
        sentences += nltk.sent_tokenize(text_document)

    return sentences

def dump_sentences(sentences, file_path):
    '''
        Dumps a list of sentences into the specified file path
    '''
    with open(file_path, 'w') as out_file:
        for sentence in sentences:
            out_file.write(sentence + '\n')
        out_file.close()

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

def main(args):
    corpus_file = args.outfile
    reddit_data_file = args.datafile
    timestamps_file = args.timefile
    stopwords_file = args.stopfile

    documents, timestamps, unique_words = read_reddit_data_and_timestamps(reddit_data_file, timestamps_file, stopwords_file)
    sentences = extract_sentences(documents)
    dump_sentences(sentences, corpus_file)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-o", "--outfile", nargs='?', default=CORPUS_FILE, type=str, help='outfile for corpus data')
    parser.add_argument("-d", "--datafile", nargs='?', default=REDDIT_DATA_FILE, type=str, help='datafile for reddit document data')
    parser.add_argument("-t", "--timefile", nargs='?', default=TIMESTAMPS_FILE, type=str, help='datafile for timestamps data')
    parser.add_argument("-s", "--stopfile", nargs='?', default=STOPWORDS_FILE, type=str, help='datafile of stopwords')
    args = parser.parse_args()

    main(args)
