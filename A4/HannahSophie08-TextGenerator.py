import argparse
import sys
import random

# Read input text as a single string, character mode 
def read_file_characters(filename): 
    
    if filename: 
        with open(filename, "r") as f:
            text = f.read()
    else: 
        text = sys.stdin.read()
    
    return text.replace('\n', ' ') # replace linebreaks with spaces 
        

 
# Read input text and split it into words, words mode 
def read_file_words(filename): 
    
    if filename:
        with open(filename, "r") as f:
            text = f.read()
    else:
        text = sys.stdin.read()

    return text.split()


# build markov model for character-based generation 
def build_markov_model_characters(text, k): 

    if k > len(text):
        print("Error: k is larger than the number of characters in the input text!", file=sys.stderr)
        sys.exit(1)

    dictionary = {}

    for i in range(len(text) - k):
        context = text[i:i+k]
        next_character = text[i+k]

        if context not in dictionary:
            dictionary[context] = []

        dictionary[context].append(next_character)
    
    return dictionary


# build markov model for words-based generation 
def build_markov_model_words(text, k): 
    if k > len(text):
        print("Error: k is larger than the number of words in the input text!", file=sys.stderr)
        sys.exit(1)

    dictionary = {}

    for i in range(len(text) - k):
        context = tuple(text[i:i+k])
        next_word = text[i+k]

        if context not in dictionary:
            dictionary[context] = [] 

        dictionary[context].append(next_word)
    
    return dictionary


# generate text using character-based markov model 
def generate_text_characters(text, dictionary, k, seed, max_chars = 100000): 

    if seed is not None:
        random.seed(seed)

    context = text[:k]
    result = context
    while len(result) < max_chars: 
        if context not in dictionary:
            break
        next_char = random.choice(dictionary[context])
        result += next_char
        context = context[1:] + next_char # shift context by one character

    return result 
        


# generate text using words-based markov model 
def generate_text_words(text, dictionary, k, seed, max_words = 100000):

    if seed is not None:
        random.seed(seed)

    context = tuple(text[:k])
    result = list(context)
    while len(result) < max_words: 
        if context not in dictionary:
            break
        next_word = random.choice(dictionary[context])
        result.append(next_word)
        context = context[1:] + (next_word,) # shift context by one word

    # For readability, the generated word-based output may be wrapped after approximately 70 characters per line.
    line = ""
    output = ""
    for word in result:
        if len(line) + len(word) + 1 > 70:
            output += line + "\n"
            line = word
        else: 
            line = line + " " + word if line else word
    
    output += line

    return output 



def main():

    parser = argparse.ArgumentParser()
    parser.add_argument('-o', type=int, default=1) # Markov order
    parser.add_argument('-w', action='store_true')  # word-based generation?
    parser.add_argument('-s', type=int, default=None) # seed
    parser.add_argument('-n', type=int, default=100000) # maximal output length
    parser.add_argument('-f', default=None) # output file 
    parser.add_argument('inputfile', nargs = '?', default=None) # input file 

    args = parser.parse_args()

    if args.o < 1:
        print("Error: k must be at least 1", file = sys.stderr)
        sys.exit(1)
    
    if args.w:
        text = read_file_words(args.inputfile)
        dictionary = build_markov_model_words(text, args.o)
        result = generate_text_words(text, dictionary, args.o, args.s, args.n)
    else:
        text = read_file_characters(args.inputfile)
        dictionary = build_markov_model_characters(text, args.o)
        result = generate_text_characters(text, dictionary, args.o, args.s, args.n)
    
    if args.f:
        out = open(args.f, 'w')
    else:
        out = sys.stdout

    print(result, file=out)

    if args.f:
        out.close()
  

main()