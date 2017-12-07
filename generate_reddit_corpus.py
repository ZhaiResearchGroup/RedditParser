import nltk
from nltk.corpus import stopwords
from reddit_data_reader import read_reddit_data_and_timestamps
from reddit_data_dump import get_reddit_data, dump_reddit_data

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

if __name__ == "__main__":
    documents, timestamps, unique_words = read_reddit_data_and_timestamps('reddit_documents.txt', 'timestamps.txt', 'stopwords.txt')
    sentences = extract_sentences(documents)
    dump_sentences(sentences, 'reddit_corpus.dat')
