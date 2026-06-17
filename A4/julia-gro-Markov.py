import sys
import random
import textwrap

def get_file():
    skip = set()
    args = sys.argv[1:]
    if '-o' in args:
        index = args.index('-o') 
        markov_order = int(args[index + 1])
        skip.add(args.index('-o'))
        skip.add(args.index('-o') + 1)
    else: 
        markov_order = 3
    word_based = '-w' in args
    if '-s' in args:
        index = args.index('-s')
        seed = int(args[index + 1])
        skip.add(args.index('-s'))
        skip.add(args.index('-s') + 1)
    else: 
        seed = None

    positional = [a for i, a in enumerate(args) if i not in skip and not a.startswith('-')]
    
    if positional: 
        with open(positional[0], "r", encoding="utf-8") as f:
            text = f.read()
    else:
        text = sys.stdin.read()
  

    return text, markov_order, word_based, seed

def prework(text, word_based):
    if word_based:        
        return text.split(), " "
    else:
        return list(text.rstrip('\r\n')), ""
    
def build_model(units, k):
    model = {}
    for i in range(len(units) - k):
        context = tuple(units[i : i+k])
        next_char = units[i+k]
        model.setdefault(context, []).append(next_char)
    return model    

def generate(units, model, k, seed, sep):
    random.seed(seed)
    context = tuple(units[:k])
    result = list(context)
    while context in model and len(result) < 2000:
        choices = model[context]
        next_char = random.choice(choices)
        result.append(next_char)
        context = context[1:] + (next_char,)

    return sep.join(result)

if __name__ == "__main__":
    text, k, word_based, seed = get_file()
    units, sep = prework(text, word_based)
    model = build_model(units, k)
    output = generate(units, model, k, seed, sep)

    if word_based:
        print(textwrap.fill(output, width=70))
    else:    
        print(output)
    
        


