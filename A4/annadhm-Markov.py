"""
     This Python script generates new text from an input text using a Markov model. 
     It reads the text, finds repeated contexts in it, and randomly choose one of the continuations that actually occur in the text.

     This scipt has two modes:
        - character-based generation (default)
        - word-based generation

    The order k of the markov model is configurable from the command line. If no order is set, order 1 is used as default. 

    To execute this script use:
        python annadhm-Markov.py [options] [inputfile]

    The following options are available:
        -o k   use Markov order k (default = 1).
        -w     use word-based generation instead of character-based. 
        -s seed initialize the random number generator with seed
    
    The flags can be combined. 
    To use a Markov order of 10 in the word-based mode use:
        python annadhm-Markov.py -o 10 - w [inputfile]
    To use a Markov order of 2 in the word-based mode, with random seed 7 use:
        python annadhm-Markov.py -o 2 -w  -s 7 [inputfile]

    For more informations have a look in the README-A4.md

"""
import argparse
import random
import sys
import textwrap

def read_input(file):
    try:
        if file:
            with open(file, "r") as f:
                return f.read()
        else:
            return sys.stdin.read()
    except Exception as e:
        print(f"🤖 We have a problem with your input file here: {e}", file=sys.stderr)
        sys.exit(1)

def build_markov_char(text, k):
    model = {}

    for i in range(len(text) -k):
        context = text[i:i+k]
        next_char = text[i+k]

        model.setdefault(context, []).append(next_char)
    
    return model

def build_markov_word(words, k):
    model = {}

    for i in range(len(words) - k): 
        context = tuple(words[i:i+k])
        next_word = words[i+k]

        model.setdefault(context, []).append(next_word)
    
    return model

def generate_char(model, text, k):
    if len(text) < k:
        return ""
    
    context = text[:k]
    output = list(context)
    max_len = len(text) * 5 

    while context in model and len(output) < max_len:
        next_char = random.choice(model[context])
        output.append(next_char)
        context= "".join(output)[-k:] 

    return "".join(output)

def generate_word(model, words, k):
    if len(words) < k:
        return ""
    
    context = tuple(words[:k])
    output = list(context)
    max_len = len(words) * 5 # safety net for circular input like 'banana' 

    while context in model and len(output) < max_len:
        next_word = random.choice(model[context])
        output.append(next_word)
        context = tuple(output[-k:])
    
    return " ".join(output)

def main():

    parser = argparse.ArgumentParser(description= "Markov Generator")

    parser.add_argument("-w", action="store_true")
    parser.add_argument("-o", type=int, default=1, help="Markov order (integer)")
    parser.add_argument("-s", type=int, default=None, help="Seed for random number generator")  
    parser.add_argument("input_file", nargs="?", help="Input file")

    args  = parser.parse_args()

    if args.o <= 0:
        print("✋ Stop - You need to use a non-negative number bigger than zero for k", file=sys.stderr)
        sys.exit(1)
    
    #set seed
    if args.s is not None:
        random.seed(args.s)
    
    # read input text
    text = read_input(args.input_file)

    # find whitespaces
    text = " ".join(text.split())

    if not text:
        print("⚠️ Ups - seems that your input file is empty...", file=sys.stderr)
        sys.exit(1)
    
    if args.w:
        words = text.split()
        
        if len(words) <= args.o:
            print("⚠️ Hold on - the input is too short for the k you choose", file=sys.stderr)
            sys.exit(1)

        model = build_markov_word(words, args.o)
        result = generate_word(model, words, args.o)
    
    else:
        if len(text) <= args.o:
            print("⚠️ Hold on - the input is too short for the k you choose", file=sys.stderr)
            sys.exit(1)

        model =build_markov_char(text, args.o)
        result = generate_char(model, text, args.o)
    
    # use textwrap to format output
    print(textwrap.fill(result, width=70))
    

if __name__ == "__main__":
    main()