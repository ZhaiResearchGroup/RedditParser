import sys
import argparse
from reddit_data_dump import get_reddit_data, dump_reddit_data

REDDIT_DATA_FILE = 'reddit_documents.dat'
TIMESTAMPS_FILE = 'timestamps.dat'

def main(args):
    subreddits = args.subreddits
    limit = args.limit
    reddit_data_file = args.outfile
    timestamps_file = args.timefile

    print('Fetching reddit data')
    documents, timestamps = get_reddit_data(subreddits, limit)

    print('Dumping reddit data')
    dump_reddit_data(documents, timestamps, reddit_data_file, timestamps_file)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-s", "--subreddits", nargs='+', default=['news'], type=str, help='names of subreddits')
    parser.add_argument("-l", "--limit", nargs='?', default=200, type=int, help='number of posts to retrieve from each subreddit')
    parser.add_argument("-o", "--outfile", nargs='?', default=REDDIT_DATA_FILE, type=str, help='outfile for reddit document data')
    parser.add_argument("-t", "--timefile", nargs='?', default=TIMESTAMPS_FILE, type=str, help='outfile for timestamps data')
    args = parser.parse_args()

    main(args)
