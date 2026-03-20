#!/usr/bin/env python3
import argparse
import re
import contractions

def main():
    # parser to obtain file name and flags
    parser = argparse.ArgumentParser(description="Count words in a text. Syntax: filename -flags")
    parser.add_argument('filename')          
    parser.add_argument("-I", "--I", dest="ignore_case", action="store_true",
                        help="ignore upper/lower case")
    parser.add_argument("-l", "--l", dest="list_words", action="store_true",
                        help="print word list with frequencies")

    args = parser.parse_args()
    print(args.filename)
    all_words = []
    with open(args.filename, "rt") as fh:
        for line in fh:
            if args.ignore_case:
                line = line.lower()
            line = contractions.fix(line) # fixes contractions lol
            print(line.rstrip())


            line = line.split()
            # print(line)

            for string in line:
                cleaned_word = "".join(re.findall(r"[^\W\d_']+", string, flags=re.UNICODE))
                if cleaned_word:                   
                        all_words.append(cleaned_word)
                # print(cleaned_word)

    unique_words = set(all_words)

    word_count = {}
    if args.list_words:
        for word in all_words:
            word_count[word] = word_count.get(word, 0) + 1 # iterates over list, adds each word as entry with default val 0, increments each word val on encounter

        for word, freq in sorted(word_count.items(), key=lambda x: (-x[1], x[0])): # sorts items of dict in priority 1=values, 0=keys "-"=reverse
            print(f"{word}\t{freq}")
    else:
        print(len(unique_words), "/", len(all_words))

if __name__ == "__main__":
    main()