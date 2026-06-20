import argparse
import sys
import random


def read_input(filename):
    if filename:
        with open(filename, "r") as file:
            return file.read()
    else:
        return sys.stdin.read()


def build_character_model(text, k):
    model = {}

    for i in range(len(text) - k):
        context = text[i:i + k]
        next_character = text[i + k]

        if context not in model:
            model[context] = []
            
        model[context].append(next_character)
        
    return model



def generate_character_text(text, model, k):
    generated_text = text[:k]
    context = text[:k]

    while context in model and len(generated_text) < len(text):
        next_character = random.choice(model[context])
        generated_text += next_character
        context = generated_text[-k:]

    return generated_text


def build_word_model(words, k):
    model = {}

    for i in range(len(words) - k):
        context = tuple(words[i: i + k])
        next_word = words[i + k]
        
        if context not in model:
            model[context] = []
        
        model[context].append(next_word)

    return model


def generate_word_text(words, model, k):
    generated_words = words[:k]
    context = tuple(words[:k])

    while context in model and len(generated_words) < len(words):
        next_word = random.choice(model[context])
        generated_words.append(next_word)
        context = tuple(generated_words[-k:])

    return " ".join(generated_words)


# defining arguments
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("filename", nargs = "?")
    parser.add_argument("-o", type = int, required = True, help = "Use Markov order k")
    parser.add_argument("-w", action="store_true", help = "Use word-based generation instead of character-based generation.")
    parser.add_argument("-s", type = int, help = "Initialize the random number generator with seed.")

    args = parser.parse_args()

    if args.o <= 0:
        print("Error: Markov order must be positive.", file=sys.stderr)
        sys.exit(1)

    if args.s is not None:
        random.seed(args.s)

    text = read_input(args.filename)
    text = " ".join(text.split())

    if not text:
        print("Error: input text is empty.", file=sys.stderr)
        sys.exit(1)


    if args.w:
        words = text.split()

        if len(words) <= args.o:
            print("Error: Markov order must be smaller than the number of words in the input.", file=sys.stderr)
            sys.exit(1)

        model = build_word_model(words, args.o)
        generated_text = generate_word_text(words, model, args.o)
    else:
        if len(text) <= args.o:
            print("Error: Markov order must be smaller than the number of characters in the input.", file=sys.stderr)
            sys.exit(1)

        model = build_character_model(text, args.o)
        generated_text = generate_character_text(text, model, args.o)

    print(generated_text)


if __name__ == "__main__":
    main()