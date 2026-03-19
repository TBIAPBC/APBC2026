import sys
import argparse
import re
from collections import Counter

def main():
    

    parser = argparse.ArgumentParser()
    parser.add_argument("filename", nargs='?', default='-')
    parser.add_argument("-I", action="store_true", help="Ignore case when counting words")
    parser.add_argument("-l", action="store_true", help="List all words and their frequencies")
    args = parser.parse_args()

    try:
        if args.filename == "-":
            text = sys.stdin.read()
        else:
            with open(args.filename, "r", encoding="utf-8") as f:
                text = f.read()
    except OSError as e:
        print(f"Error opening file: {e}", file=sys.stderr)
        sys.exit(1)


    if args.I:
        words = re.findall(r"\b\w+\b", text.lower())
    else:
        words = re.findall(r"\b\w+\b", text)


    total_words = len(words)
    word_counts = Counter(words)
    unique_words = set(words)

    if args.l:
        for word in sorted(unique_words, key=lambda x: (-word_counts[x], x)):
            print(f"{word}\t{word_counts[word]}")
    else:
        print(f"{len(unique_words)} / {total_words}")

if __name__ == "__main__":
    main()