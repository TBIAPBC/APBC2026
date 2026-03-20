import argparse
import re
import sys

# defining arguments
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-I", action="store_true", help = "Ignore case when counting words (by converting all upper case to lower case)")
    parser.add_argument("-l", action="store_true", help = "Prints a list of words, sorted by word frequency, starting with the most common words.")
    parser.add_argument("filename", nargs="?")
    parser.add_argument("-out", help = "define output file [OUTPUT.out] instead of printing to terminal.")

    args = parser.parse_args()



    # if the -out argument is used the output will be written to a file
    if args.out:
        out = open(args.out, "w")
    else:
        out = sys.stdout # if -out is not used, the output is printed to the terminal



    # open the given file, either by passing a as filename or by STDIN (<)
    if args.filename:
        with open(args.filename) as r:
            text = r.read()
    else:
        text = sys.stdin.read()
    
    words = re.findall(r"[A-Za-zÄÖÜäöüß]+", text) #split the text at every point we encounter a non letter


    # action for argument -I, turning all upper case letters to lower case
    if args.I:
        words = [w.lower() for w in words]




    total_words = len(words)
    different_words = len(set(words))

    # default mode, if no argument is used, we get the total and different words counts
    if not args.l:
        print("Total Words: ", total_words, file=out)
        print("Different Words: ", different_words, file=out)



    # counting words
    counts = {}

    for w in words:
        if w in counts:
            counts[w] += 1
        else:
            counts[w] = 1

    # sort words by frequency
    sorted_words = sorted(counts.items(), key=lambda x: (-x[1], x[0]))

    # action for argument -l, printing words and their count
    if args.l:
        for word, count in sorted_words:
            print(f"{word}\t{count}", file=out)


    if args.out:
        out.close()




if __name__ == "__main__":
    main()