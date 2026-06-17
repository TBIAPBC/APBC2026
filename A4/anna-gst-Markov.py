### Last Update: 03.05.2026
### Author: Anna Gsteu
### Description: A4 - Markov Text Generator.
###              Reads a training text (file or input) and generates new text using a Markov model.
###              Supports character-based and word-based generation.
###              Flags: -o k for Markov order, -w for word mode,
###              -s seed for reproducible output, -i for case insensitive, 
###              -l for maximum length.


import sys
import argparse
import random
import textwrap


def read_text(input_file, k, word_mode=False, ignore_case=False):
    """Reads input text from file or stdin."""
    
    if input_file:
        try:
            with open(input_file, "r", encoding="utf-8") as file:
                text = file.read()
        except OSError as e:
            print(f"Error: Cannot open file: {e}", file=sys.stderr)
            sys.exit(1)
    else:
        text = sys.stdin.read()

    if ignore_case:
        text = text.lower()

    if not text.strip():
        print("Error: Input text is empty", file=sys.stderr)
        sys.exit(1)

    if word_mode:
        text = text.split()  # splits into words and treats newlines as whitespace
    else:
        text = text.replace("\n", " ")

    if len(text) <= k:
        print(f"Error: Input text must be longer than k={k}", file=sys.stderr)
        sys.exit(1)

    return text


def build_markov_dictionary(text, k, word_mode=False):
    """Builds a dictionary from each context to its possible next characters or words."""    
    dictionary = {}

    for i in range(len(text) - k):
        if word_mode:
            key = tuple(text[i:i+k])  # stores as tuple so it can be a dict key
        else:
            key = text[i:i+k]
        item = text[i+k]
        if key not in dictionary:
            dictionary[key] = []
        dictionary[key].append(item)

    return dictionary


def generate_text(text, dictionary, k, seed, n, word_mode=False):
    """Generates text by choosing random next characters or words from the Markov dictionary."""    
    if seed is not None:
        random.seed(seed)

    if word_mode:
        result = list(text[:k])  # starts with first k words
        while tuple(result[-k:]) in dictionary and len(result) < n:
            context = tuple(result[-k:])
            next_item = random.choice(dictionary[context])
            result.append(next_item)    # w
        return textwrap.fill(" ".join(result), width=70)
    
    else:
        result = list(text[:k])  # list append is more efficient tahn results += next_item 
        while "".join(result[-k:]) in dictionary and len(result) < n:
            context = "".join(result[-k:])
            next_item = random.choice(dictionary[context])
            result.append(next_item)
        return "".join(result)


def main():
    parser = argparse.ArgumentParser(description='Markov Text Generator')
    parser.add_argument(
        'inputfile',
        nargs='?',
        default=None,
        help='input file'
    )
    parser.add_argument(
        '-o',
        help='Markov order',
        type=int,
        default=1
    )
    parser.add_argument(
        '-w',
        help='Switch to word mode',
        action='store_true'
    )
    parser.add_argument(
        '-s',
        help='Set a random seed',
        type=int,
        default=None
    )
    # flag added since text generation was taking too long for special cases
    parser.add_argument(
        '-l',
        help='Maximum output length',
        type=int,
        default=10000
    )
    # flag for ignoring cases as discussed in lecture
    parser.add_argument(
        '-i',
        help='Ignore case (treat upper and lowercase as the same)',
        action='store_true'
    )
    args = parser.parse_args()

    # Error messages before running command
    if args.o < 1:
        print("Error: Markov order (-o) must be at least 1", file=sys.stderr)
        sys.exit(1)

    if args.l < 1:
        print("Error: Maximum output length (-l) must be at least 1", file=sys.stderr)
        sys.exit(1)
        
    if args.l < args.o:
        print(f"Error: Maximum output length (-l={args.l}) is less than Markov order (-o={args.o})", file=sys.stderr)
        sys.exit(1)

    text = read_text(args.inputfile, args.o, args.w, args.i)
    dictionary = build_markov_dictionary(text, args.o, args.w)
    result = generate_text(text, dictionary, args.o, args.s, args.l, args.w)
    print(result)


if __name__ == "__main__":
    main()