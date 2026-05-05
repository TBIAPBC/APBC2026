import random
import argparse

def read_input(filename):
    """
    Read text from a file and normalize it by replacing newlines with spaces.
    
    Args:
        filename (str): Path to the input text file.
        
    Returns:
        str: The file contents with newlines replaced by spaces.
    """
    
    with open(filename, 'r', encoding='utf-8') as f:
        return f.read().replace("\n", " ")

def find_cont(text_str, k, w):
    """
    Build a Markov chain model by analyzing context-to-suffix relationships.
    
    Scans through the input text and creates a dictionary mapping k-length contexts
    to lists of possible following tokens. If no natural end state exists adds a '***' marker at the end to signal
    when the text should stop generating.
    
    Args:
        text_str (str): The input text to analyze.
        k (int): The order (context length) - number of tokens to use for prediction.
        w (bool): If True, tokenize by words; if False, by characters.
        
    Returns:
        tuple: A tuple containing:
            - cont_dict (dict): Maps context tuples to lists of possible next tokens.
            - tokens (list/str): The tokenized input (list of words or string for characters).
    """
    
    contexts = []
    cont_dict= {}

    if w:
        tokens = text_str.split()
    else:
        tokens = text_str
    
    for t in range (len(tokens)-k):
        context = tuple(tokens[t:t+k])
        
        if context in cont_dict:
            cont_dict[context].append(tokens[t+k])
        else:
            cont_dict[context] = [tokens[t+k]]
        contexts.append(context)
    
    end_state_w = cont_dict.get(tuple(tokens[-k:]))
    
    if end_state_w:
        cont_dict[tuple(tokens[-k:])].append('***')
        
    return cont_dict, tokens

def gen_text(cont_dict, tokens, k, w):
    """
    Generate new text using the Markov chain model.
    
    Starts with the first k tokens and iteratively selects the next token by randomly
    choosing from the possible continuations of the current k-token context.
    Stops when it encounters the '***' end marker or has no valid continuation.
    
    Args:
        cont_dict (dict): The Markov chain model (context -> list of possible next tokens).
        tokens (list/str): The original tokenized text (used for initialization). 
        If tokens are words it's a list if it's characters it's a string
        k (int): The order (context length).
        w (bool): If True, join output with spaces; if False, concatenate. 
        Concat for characters because the spaces are in the model and don't have to be added.
        
    Returns:
        str: The generated text.
    """
    
    gen_str = []
    start = tokens[:k]

    for c in start:
        gen_str.append(c)

    while True:
        current_token = tuple(gen_str[-k:])
        check = cont_dict.get(current_token)
        
        if check:
            next_token = random.choice(cont_dict[current_token])

        else:
            if w == True:
                return ' '.join(gen_str)
            else:
                return ''.join(gen_str)
        
        if next_token == '***':
            if w == True:
                return ' '.join(gen_str)
            else:
                return ''.join(gen_str)
        
        gen_str.append(next_token)


if __name__ == '__main__':
    
    parser = argparse.ArgumentParser(prog = "Markov Text Generator by Thanos", description = 'Takes a text file as input and generates text based on a markov model made from the input file')
    parser.add_argument('filename',  help ='Path to the input text file.')
    parser.add_argument('-w', '--words', action = 'store_true', help = 'Use word mode (default: character mode). In word mode, predictions are based on preceding words.')
    parser.add_argument('-o', '--order', type = int , help = 'Context length for predictions. Default is 1. (e.g., -o 2 uses 2 preceding tokens)', default = 1)
    parser.add_argument('-s', '--seed', type = int , help = 'Set a random seed for reproducible output. (e.g., -s 42).')
    
    args = parser.parse_args()
    
    filename = args.filename
    k = args.order
    w = args.words
    
    if args.seed:
        random.seed(args.seed)
    

    read_text = read_input(filename)
    create_model = find_cont(read_text, k, w)  
    text = (gen_text(create_model[0], create_model[1], k, w))
    print(text)

     
    
                
    
            
        