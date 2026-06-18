import random 
import bisect
import argparse
import sys
import textwrap


def main():
    #read in arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('filename', type = str, help = 'Input filename')
    parser.add_argument('-o', type = int, required = True, help = 'Markov Order')
    parser.add_argument('-w', action = 'store_true', default = False, help = 'use word-based generation')
    parser.add_argument('-s', type = int, default = None, help = 'initialize random seed')
    args = parser.parse_args()
    
    with open(args.filename, 'r', encoding='utf-8') as file:
        text = file.read()
        
        if args.w:
            #splits string into a list at any whitespace 
            text = text.split()
        else:
            #line breaks -> whitespace, tabs -> ignored
            text = list(" ".join(text.split()))
            
    if args.o > len(text):
        print("Error: Markov Order is larger than text length.", file = sys.stderr)
        return
    
    #set seed
    if args.s is not None:
        random.seed(args.s)
    
    print(create_txt(text, args.o, args.w))
    


def create_txt(text, k, wordbased = False): 
    new_text = text[0:k] 
    
    #create array with all suffixes, sorted lexicographically 
    suffix_array = sorted(range(len(text)), key=lambda i: text[i:]) 
    
    #create first kontext, first k characters/words 
    context = text[0:k] 
    
    for n in range(1000): 
        #get the leftmost and rightmost+1 possible option via binary search
        left = bisect.bisect_left(suffix_array, context, key=lambda i: text[i:i+k]) 
        right = bisect.bisect_right(suffix_array, context, key=lambda i: text[i:i+k]) 
        
        matches = []
        for j in range(left, right):
            if suffix_array[j] + k < len(text):
                matches.append(suffix_array[j])
        
        #ends generating text, if there is no match anymore that stays within the text
        if not matches:
            break
        
        #chooses one index from matches randomly
        choice = random.choice(matches)
        
        #add the character/word that follows the context
        new_text.append(text[choice+k]) 
        #last k characters/words are the new context
        context = new_text[-k:]
        
    if wordbased:
        #textwrap.fill adds linebreaks after 70 characters
        return textwrap.fill(" ".join(new_text), width=70)
    else:
        return "".join(new_text)
        



if __name__ == "__main__":
    main()
    