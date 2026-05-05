import argparse
import random
import sys


def parse_args():
    parser = argparse.ArgumentParser(
        description="Generate text from an input text using a Markov model."
    )
    parser.add_argument("-o", type=int, required=True, metavar="k",
                        help="use Markov order k")
    parser.add_argument("-w", action="store_true",
                        help="use word-based generation instead of character-based generation")
    parser.add_argument("-s", type=int, metavar="seed",
                        help="initialize the random number generator with seed")
    parser.add_argument("inputfile", nargs="?",
                        help="input file (if omitted, read from standard input)")
    args = parser.parse_args()

    if args.o < 0:
        parser.error("Markov order k must be non-negative")

    return args


def read_input(filename=None):
    if filename is None:
        return sys.stdin.read()
    try:
        with open(filename, "r", encoding="utf-8") as f:
            return f.read()
    except OSError as e:
        print(f"Error reading input file: {e}", file=sys.stderr)
        sys.exit(1)

#each k length gets context list, as in hints
def build_char_model(text, k):
    model = {}
    for i in range(len(text) - k):
        context = text[i:i + k]
        next_char = text[i + k]
        model.setdefault(context, []).append(next_char)
    return model

# matches word to next word, as in hints
def build_word_model(words, k):
    model = {}
    for i in range(len(words) - k):
        context = tuple(words[i:i + k])
        next_word = words[i + k]
        model.setdefault(context, []).append(next_word)#appened observed word
    return model

#choose one outgoing transition like edge and switches window to next, here only until max_chars!! but repeated
def generate_chars(text, k, rng, max_chars=1000):#stops then not like in assignment asked but not specified
    if len(text) < k:
        return

    model = build_char_model(text, k)

    if k == 0:
        context = ""
        count = 0
        while True:# change to count< max char to make ended loop
            choices = model.get(context, [])
            if not choices:
                break
            next_char = rng.choice(choices)
            print(next_char, end="", flush=True)
            count += 1
        print()
        return

    context = text[:k]
    print(context, end="", flush=True)

    count = k
    while True:#to run without just change to while True
        choices = model.get(context, [])
        if not choices:
            break
        next_char = rng.choice(choices)
        print(next_char, end="", flush=True)
        context = context[1:] + next_char
        count += 1

    print()

#same for words
def generate_words(text, k, rng, max_words=200, width=70):#also stops
    words = text.split()

    if len(words) < k:
        return

    model = build_word_model(words, k)

    if k == 0:
        context = ()
        line_len = 0
        count = 0
        while True:#to run with end make while count< max words
            choices = model.get(context, [])
            if not choices:
                break
            word = rng.choice(choices)
            if line_len == 0:
                print(word, end="", flush=True)
                line_len = len(word)
            elif line_len + 1 + len(word) <= width:
                print(" " + word, end="", flush=True)
                line_len += 1 + len(word)
            else:
                print()
                print(word, end="", flush=True)
                line_len = len(word)
            count += 1
        print()
        return

    context = tuple(words[:k])
    output_words = list(context)

    line_len = 0
    for i, word in enumerate(output_words):
        sep = "" if i == 0 else " "
        if line_len == 0:
            print(word, end="", flush=True)
            line_len = len(word)
        else:
            print(sep + word, end="", flush=True)
            line_len += len(sep) + len(word)

    count = k
    while True:#here same hing
        choices = model.get(context, [])
        if not choices:
            break
        next_word = rng.choice(choices)

        if line_len + 1 + len(next_word) <= width:
            print(" " + next_word, end="", flush=True)
            line_len += 1 + len(next_word)
        else:
            print()
            print(next_word, end="", flush=True)
            line_len = len(next_word)

        output_words.append(next_word)
        context = tuple(output_words[-k:])
        count += 1

    print()


def main():
    args = parse_args()
    text = read_input(args.inputfile)
    rng = random.Random(args.s)

    if args.w:
        generate_words(text, args.o, rng)
    else:
        generate_chars(text, args.o, rng)


if __name__ == "__main__":
    main()

