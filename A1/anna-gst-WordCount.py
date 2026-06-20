### Date: 19.03.26
### Author: Anna Gsteu
### Description: A1 - word count

import sys
import argparse
import re

def main():
    
    # parse command line arguments
    parser = argparse.ArgumentParser(description='Counts total and unique words in a text file.')
    parser.add_argument(
        'filename',
        nargs='?',
        default='-',
        help='input text file'
        )
    parser.add_argument(
        '-I',
        action='store_true',
        help='case insensitive',
        )
    parser.add_argument(
        '-l',
        action='store_true',
        help='prints a list of words',
        )
    args = parser.parse_args()

    # read input from file or stdin
    try:
        if args.filename == "-":
            text = sys.stdin.read()
        else:
            with open(args.filename, encoding="utf-8") as f:
                text = f.read()
    except OSError as e:
        print(f'Error opening file: {e}')
        sys.exit(1)

    # normalize case if -I flag is set
    if args.I:
        text = text.lower()

    # remove punctuation and split into words
    text = re.sub('[^a-zA-Z0-9ÄäÖöÜüß]', ' ', text)
    words = text.split()

    # count word freq.
    word_counts = {}
    for word in words:
        if word in word_counts:
            word_counts[word] += 1
        else:
            word_counts[word] = 1

    WC_unique = len(word_counts)
    WC_all = sum(word_counts.values())

    # print results and define l
    print(f'{WC_unique} / {WC_all}')
    if args.l:
        sorted_word_counts = sorted(word_counts.items(), key=lambda x: (-x[1], x[0]))
        for key, value in sorted_word_counts:
            print(f'{key}\t{value}')

if __name__ == "__main__":
    main()