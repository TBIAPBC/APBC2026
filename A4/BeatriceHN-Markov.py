import sys
import textwrap
import numpy as np
import argparse

def char_markov_chain(text, k):

    markov_chain = {}
    
    for i in range(len(text) - k):
        key = text[i:i+k]
        next_char = text[i+k]
        if key not in markov_chain:
            markov_chain[key] = []
        markov_chain[key].append(next_char)

    return markov_chain

def output_char_markov_chain(text, k, markov_chain, max_len=None):
    current_context = text[:k]
    output = [text[:k]] 

    chars_count = k

    while True:
        if max_len is not None and len(output) >= max_len:
            break

        options = markov_chain.get(current_context)
        if not options:
            break
        next_char = np.random.choice(options)
        output.append(next_char)
        current_context = current_context[1:] + next_char
        chars_count += 1

    print(''.join(output))


def word_markov_chain(text, k):
    words = text.split()
    markov_chain = {}
    
    for i in range(len(words) - k):
        key = tuple(words[i:i+k])
        next_word = words[i+k]
        
        if key not in markov_chain:
            markov_chain[key] = []
        markov_chain[key].append(next_word)
        
    return markov_chain, words

def output_word_markov_chain(k, markov_chain, words, max_len=None):
    current_context = tuple(words[:k])
    output = list(words[:k])

    while True:
        if max_len is not None and len(output) >= max_len:
            break

        options = markov_chain.get(current_context)
        if not options:
            break
        next_word = np.random.choice(options)
        output.append(next_word)
        current_context = current_context[1:] + (next_word,)

    generated_text = ' '.join(output)
    print(textwrap.fill(generated_text, width=70))

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Markov Chain Text Generator')
    
    parser.add_argument('input_file', nargs='?', type=argparse.FileType('r', encoding='utf-8', errors='ignore'), default=sys.stdin, help='Input text file (reads from stdin if omitted)')
    parser.add_argument('-o', '--markov_order_k', type=int, default=1, help='Order of the Markov chain (default: 1)')
    parser.add_argument('-w', '--word_based_generation', action='store_true', help='Generate text based on words instead of characters')
    parser.add_argument('-s', '--seed_for_random_number_generator', type=int, default=None, help='Seed for the random number generator (default: None)')
    parser.add_argument('-l', '--max_length', type=int, default=None, help='Maximum length of generated text (default: None)')

    args = parser.parse_args()
    
    red = '\033[31m'
    reset = '\033[0m'

    if args.max_length is None:
        print(f'{red}Warning: No maximum length specified. \nThe program may run indefinitely if the Markov chain has cycles.\n{reset}', file=sys.stderr)


    text = args.input_file.read()

    if args.seed_for_random_number_generator is not None:
        np.random.seed(args.seed_for_random_number_generator)

    if args.word_based_generation:
        markov_chain, words = word_markov_chain(text, args.markov_order_k)
        output_word_markov_chain(args.markov_order_k, markov_chain, words, args.max_length)
    else:
        markov_chain = char_markov_chain(text, args.markov_order_k)
        output_char_markov_chain(text, args.markov_order_k, markov_chain, args.max_length)
