import string
import argparse
import random
import time

def main():
    parser = argparse.ArgumentParser(description="Generate text using a Markov model.")
    parser.add_argument('filename', type=str, help='Input filename')
    parser.add_argument('-o', dest='k', type=int, required=True, help='Use Markov order k (int, required)')
    parser.add_argument('-s', dest='seed', type=str, default=None, help='Initialize the random number generator with seed (string)')
    parser.add_argument('-w', action='store_true', default=False, help='Use word-based generation instead of character-based')
    parser.add_argument('-i', action='store_true', default=False, help='Ignore upper/lowercase')
    parser.add_argument('-d', action='store_true', default=False, help='Enable dynamic printing')
    parser.add_argument('-max', dest='max', default=False, help='Set maximum iterations for generated text (int)')
    args = parser.parse_args()

    tokens=read_file_content(args.filename, args.w, args.i)
    model = create_markov_model(tokens, args.k)
    init_context = get_init_context(tokens, args.k)
    generate_text(model, args.w, init_context, args.d, int(args.max), args.seed)

def get_init_context(tokens, k):
    return tuple(tokens[:k])

def read_file_content(filename, w, i):
    with open(filename, 'r', encoding='utf-8') as f:
        tokens = []
        
        for line in f:
            if i: line = line.lower() # convert to lowercase if required
            if w:
                tokens.extend(line.split())
            else:
                # remove punctuation 
                line_no_punct = line.translate(str.maketrans('', '', string.punctuation))
                # replace linebreaks with spaces
                tokens.extend(list(line_no_punct.replace('\n', ' ').replace('\r', ' ')))
    return tokens

def create_markov_model(tokens, k):
    model = {}
    for i in range(len(tokens) - k):
        context = tokens[i:i+k]
        next_token = tokens[i+k]
        if tuple(context) not in model:
            model[tuple(context)] = []
        model[tuple(context)].append(next_token)
    return model

def generate_text(model, w, init_context, dynamic=False, iterations=None, seed=None):
    random.seed(seed)
    text = ''.join(init_context) if not w else ' '.join(init_context)
    context = init_context
    if dynamic:
        if w:
            print(f"{' '.join(init_context)}", end='', flush=True)
        else:
            print(f"{''.join(init_context)}", end='', flush=True)
        time.sleep(0.1)

    while tuple(context) in model:
        next_token = random.choice(model[context])
        if w:
            text = f"{text} {next_token}"
       
        else:
            text = f"{text}{next_token}"

        context = context[1:] + (next_token,)

        if dynamic:
            if w:
                print(f" {next_token}", end='', flush=True)
                time.sleep(0.1)
            else:
                print(next_token, end='', flush=True)
                time.sleep(0.05)

        if iterations:
            iterations -=1
            if iterations <= 0:
                break

    if not dynamic:
        print(text)

if __name__ == '__main__':
    main()